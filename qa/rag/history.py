"""프론트·백엔드 GitHub 이력(PR + 연결 이슈)을 vault 노트로 수집한다.

PR 하나 = 노트 하나. 연결된 이슈 본문(증상)과 PR 본문(원인·해결), 변경 파일 목록을 함께 담는다 —
실패 분석에서 "비슷한 증상을 예전에 어디를 고쳐서 해결했나"를 찾기 위한 문서다.
PR로 이어지지 않은 이슈는 별도 노트로 남긴다.
"""

import json
import re
import subprocess

from qa.config import ROOT

VAULT = ROOT / "vault"
REPOS = {"frontend": "Social-Agent-Library-Management/frontend",
         "backend": "Social-Agent-Library-Management/backend"}
PR_FIELDS = "number,title,body,state,mergedAt,createdAt,headRefName,url,files,closingIssuesReferences,labels"
ISSUE_FIELDS = "number,title,body,state,createdAt,url,labels"


def _gh(*args: str) -> list[dict]:
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return json.loads(out.stdout)


def _safe(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|#\[\]^]', " ", name).strip()[:80]


TITLE = re.compile(r"^(\w+)(?:\(([^)]*)\))?:\s*(.+)$")  # type(#이슈): 설명


def _change_type(title: str) -> str:
    m = TITLE.match(title)
    return m.group(1) if m else "기타"


def _subject(title: str) -> str:
    m = TITLE.match(title)
    return m.group(3) if m else title


def _issue_refs(pr: dict) -> list[int]:
    # 팀 컨벤션은 PR 제목 type(#이슈)로 이슈를 잇는다 — closing 키워드가 없어도 제목에서 찾는다.
    refs = {r["number"] for r in pr.get("closingIssuesReferences") or []}
    m = TITLE.match(pr["title"])
    if m and m.group(2):
        refs.update(int(n) for n in re.findall(r"#(\d+)", m.group(2)))
    return sorted(refs)


def _write(path, frontmatter: dict, body: str) -> None:
    fm = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in frontmatter.items())
    path.write_text(f"---\n{fm}\n---\n{body.strip()}\n")


def collect() -> dict:
    counts = {}
    for repo_key, repo in REPOS.items():
        out_dir = VAULT / "이력" / repo_key
        out_dir.mkdir(parents=True, exist_ok=True)
        for old in out_dir.glob("*.md"):
            old.unlink()  # GitHub이 원본이므로 매번 새로 만든다

        issues = {i["number"]: i for i in _gh("issue", "list", "-R", repo, "--state", "all",
                                               "--limit", "500", "--json", ISSUE_FIELDS)}
        prs = _gh("pr", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", PR_FIELDS)
        linked = set()
        for pr in prs:
            refs = _issue_refs(pr)
            linked.update(refs)
            issue_text = "\n\n".join(
                f"### 이슈 #{n} {issues[n]['title']}\n{issues[n].get('body') or ''}" for n in refs if n in issues)
            files = "\n".join(f"- `{f['path']}` (+{f['additions']}/-{f['deletions']})" for f in pr.get("files") or [])
            body = (f"# {repo_key} PR #{pr['number']} {pr['title']}\n\n"
                    + (f"## 증상·요구 (연결 이슈)\n{issue_text}\n\n" if issue_text else "")
                    + f"## 변경 내용 (PR 본문)\n{pr.get('body') or ''}\n\n"
                    + f"## 변경 파일\n{files or '- (없음)'}\n\n원본: {pr['url']}")
            _write(out_dir / f"PR-{pr['number']} {_safe(_subject(pr['title']))}.md", {
                "type": "이력", "repo": repo_key, "kind": "pr", "number": pr["number"],
                "change": _change_type(pr["title"]), "issues": refs, "state": pr["state"],
                "merged_at": pr.get("mergedAt"), "branch": pr["headRefName"],
                "files": [f["path"] for f in pr.get("files") or []],
            }, body)
        standalone = [i for n, i in issues.items() if n not in linked]
        for issue in standalone:
            _write(out_dir / f"이슈-{issue['number']} {_safe(_subject(issue['title']))}.md", {
                "type": "이력", "repo": repo_key, "kind": "issue", "number": issue["number"],
                "change": _change_type(issue["title"]), "state": issue["state"],
            }, f"# {repo_key} 이슈 #{issue['number']} {issue['title']}\n\n{issue.get('body') or ''}\n\n원본: {issue['url']}")
        counts[repo_key] = {"pr": len(prs), "issue_only": len(standalone)}
    return counts
