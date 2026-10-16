"""실행 결과 → 사람이 읽는 리포트.

채널에 무관한 텍스트와 첨부 목록만 만든다. 어디로 보낼지는 출구(n8n)가 정한다.
굵게(*...*)·코드(`...`)·인용(>)만 써서 Slack mrkdwn과 일반 마크다운 양쪽에서 읽힌다.
"""

from datetime import datetime

from qa.config import settings
from qa.intent import catalog

ICON = {"pass": "✅", "fail": "❌", "inconclusive": "⚠️"}
LABEL = {"pass": "통과", "fail": "실패", "inconclusive": "판단 불가"}


def _duration(summary: dict) -> str:
    sec = int((datetime.fromisoformat(summary["finished_at"]) - datetime.fromisoformat(summary["started_at"])).total_seconds())
    return f"{sec // 60}분 {sec % 60}초" if sec >= 60 else f"{sec}초"


def _target(summary: dict) -> str:
    return f"front `{summary['frontend_sha'][:7]}` · back `{summary['backend_sha'][:7]}`"


def _attachment(run_id: str, rel: str, title: str) -> dict:
    path = settings.artifacts_dir / run_id / rel
    return {
        "title": title,
        "filename": path.name,
        "bytes": path.stat().st_size,
        "url": f"{settings.api_url_for_n8n}/artifacts/{run_id}/{rel}",
    }


def _scenario_report(summary: dict) -> tuple[str, list[dict]]:
    tests = summary["tests"]
    passed = sum(t["outcome"] == "passed" for t in tests)
    verdict = "pass" if summary["passed"] else "fail"
    titles = {s.id.split("::")[1]: s.title for s in catalog.load()}
    lines = [f"{ICON[verdict]} *{LABEL[verdict]}* {passed}/{len(tests)} · 시나리오 테스트 · {_duration(summary)}",
             f"대상: {_target(summary)}", ""]
    attachments = []
    for t in tests:
        func = t["name"].split("[")[0]
        title = titles.get(func, func)
        failed = t["outcome"] == "failed"
        if failed:
            first = (t["message"] or "").strip().splitlines()[:2]
            lines.append(f"• ❌ {title}\n> {' / '.join(first)}")
        else:
            lines.append(f"• ✅ {title}")
        attachments += [_attachment(summary["run_id"], a, f"{'❌' if failed else '✅'} {title} — 마지막 화면")
                        for a in t["artifacts"] if a.endswith(".png")]
    return "\n".join(lines), attachments


def _explore_report(summary: dict) -> tuple[str, list[dict]]:
    v = summary["verdict"]
    lines = [f"{ICON[v]} *{LABEL[v]}* · AI 탐색 테스트 · {_duration(summary)}",
             f"대상: {_target(summary)}", "",
             f"*판정 근거* {summary['explanation']}", ""]
    refs = summary.get("references") or []
    if refs:
        lines.append("*📘 근거 문서* (vault)")
        for ref in refs:
            mark = "" if ref.get("verified") else " ⚠️ 인용문 확인 안 됨"
            lines.append(f"• `{ref['path']}`{mark}\n> {ref['quote']}")
        lines.append("")
    lines.append("*확인한 화면*")
    attachments = []
    for i, step in enumerate(summary["steps"], 1):
        mark = " 📸" if step.get("screenshot") and not step.get("screenshot_missing") else ""
        lines.append(f"{i}. {step['action']} — {step['observation']}{mark}")
        if mark:
            attachments.append(_attachment(summary["run_id"], f"screens/{step['screenshot']}", f"{i}. {step['action']}"))
    return "\n".join(lines), attachments


def _analysis_section(a: dict) -> str:
    if "error" in a:
        return f"\n*🔎 실패 분석* 실행하지 못했습니다\n> {a['error'][:300]}"
    from qa.analyze import CATEGORIES
    lines = ["", f"*🔎 실패 분석* `{a['category']}` ({CATEGORIES[a['category']].split(' (')[0]}) · 확신도 {a['confidence']}",
             f"> {a['cause']}"]
    if a["fix_candidates"]:
        lines.append("*🔧 수정 후보*")
        for c in a["fix_candidates"]:
            mark = "" if c.get("verified") else " ⚠️ 위치 확인 안 됨"
            lines.append(f"• {c['repo']} `{c['file']}:{c['line']}`{mark} — {c['reason']}")
    if a["similar_history"]:
        lines.append("*🕘 비슷한 과거 사례*")
        lines += [f"• `{h['path']}` — {h['why']}" for h in a["similar_history"]]
    return "\n".join(lines)


def build(summary: dict) -> dict:
    text, attachments = (_explore_report if summary.get("mode") == "explore" else _scenario_report)(summary)
    if summary.get("analysis"):
        text += "\n" + _analysis_section(summary["analysis"])
    return {"text": text, "attachments": attachments}


def build_error(error: str) -> dict:
    return {"text": f"⚠️ *검증을 실행하지 못했습니다*\n> {error[:500]}", "attachments": []}
