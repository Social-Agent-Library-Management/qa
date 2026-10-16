"""검증 결과를 vault의 QA 리포트 노트로 남기고 인덱스에 반영한다.

리포트가 쌓이면 다음 실패 분석에서 '비슷한 과거 사례'로 검색된다.
근거 문서·과거 이력은 [[위키링크]]로 걸어 Obsidian 그래프에서 기획서 ↔ 이력 ↔ 검증 결과가 이어지게 한다.
"""

import json
import re
from datetime import datetime
from pathlib import Path

from qa.rag import index

REPORT_DIR = index.VAULT / "QA 리포트"


def _wikilink(path: str) -> str:
    return f"[[{Path(path).stem}]]"


def _linkify(text: str) -> str:
    # 리포트 본문의 `기획서/05 연체 관리.md` 같은 경로 표기를 위키링크로 바꾼다.
    return re.sub(r"`((?:기획서|이력|QA 리포트)/[^`]+?\.md)`", lambda m: _wikilink(m.group(1)), text)


def write(summary: dict, report_text: str, request: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    verdict = summary.get("verdict") or ("pass" if summary.get("passed") else "fail")
    asked = (request.get("request") or ", ".join(summary.get("scenarios", []))).strip()
    started = datetime.fromisoformat(summary["started_at"])
    name = re.sub(r'[\\/:*?"<>|#\[\]^]', " ", f"{started:%Y-%m-%d %H%M} {verdict} {asked}")[:90].strip()
    analysis = summary.get("analysis") or {}
    related = sorted({_wikilink(p) for p in
                      [r["path"] for r in summary.get("references", [])]
                      + [h["path"] for h in analysis.get("similar_history", [])]})
    frontmatter = {
        "type": "QA 리포트", "verdict": verdict, "mode": summary.get("mode", "scenario"),
        "request": asked, "source": request.get("source"), "frontend_sha": summary["frontend_sha"],
        "backend_sha": summary["backend_sha"], "job_id": summary.get("job_id"), "run_id": summary["run_id"],
        "category": analysis.get("category"),
    }
    body = (f"# QA {verdict} · {asked}\n\n"
            + _linkify(report_text)
            + (f"\n\n## 관련 노트\n" + " · ".join(related) if related else "")
            + f"\n\n산출물(스크린샷·trace): `qa/artifacts/{summary['run_id']}/`\n")
    path = REPORT_DIR / f"{name}.md"
    fm = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in frontmatter.items())
    path.write_text(f"---\n{fm}\n---\n{body}")
    index.sync()  # 바뀐 노트(이 리포트)만 임베딩된다
    return path
