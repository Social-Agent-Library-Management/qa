"""실패 분석: 왜 실패했고 어디를 고치면 되는지.

검증 AI와 분리된 분석 AI가 실패 증거(화면·API 로그)와 근거 문서(기획서·디자인 스펙·과거 이력),
그리고 **검증한 그 커밋의 코드**(worktree)를 직접 읽고 원인을 분류한다.
추천한 파일·라인이 실제로 존재하는지 기계적으로 확인해 지어낸 위치를 걸러낸다.
"""

import json
import time
from pathlib import Path

from qa.config import settings
from qa.intent import claude
from qa.rag import context
from qa.runner import SCENARIO_DIR

CATEGORIES = {
    "LOCATOR_DRIFT": "화면 문구·구조만 바뀌어 테스트가 깨짐 (기능은 정상, 테스트 수정 필요)",
    "CONTRACT_DRIFT": "프론트·백엔드 API 계약 불일치 (요청·응답 형태가 서로 다름)",
    "REAL_BUG": "기능 결함 또는 기대 동작 미구현",
    "FLAKY": "타이밍·환경에 따라 달라지는 불안정한 실패",
    "TEST_DATA": "시드·테스트 데이터가 기대와 맞지 않음",
}

SYSTEM = """너는 도서관 관리 시스템의 실패 분석가다. QA 테스트가 실패한 원인을 찾고 수정 위치를 추천한다.

코드 위치 (검증한 바로 그 커밋):
- frontend: {front}  (Next.js)
- backend: {back}  (Spring Boot / Kotlin)
- vault(기획서·디자인 스펙·과거 이력): {vault}

진행:
1. 실패 증거를 읽는다. 스크린샷은 Read로 열어 직접 본다. API 로그로 화면 문제인지 응답 문제인지 가른다.
2. 근거 문서로 기대 동작을 확인한다. 비슷한 과거 이력이 있으면 그때 바꾼 파일을 먼저 본다.
3. Grep·Read로 실제 코드를 따라가 원인을 찾는다. 추측이 아니라 읽은 코드로 말한다.

분류 기준:
{categories}

수정 후보의 file은 repo 루트 기준 상대 경로, line은 그 파일에서 실제로 고칠 줄 번호다.
코드를 끝까지 확인하지 못했으면 confidence를 low로 두고 그 이유를 cause에 적는다."""

SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": list(CATEGORIES)},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "cause": {"type": "string", "description": "원인 두세 문장"},
        "fix_candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "enum": ["frontend", "backend", "qa"]},
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                    "reason": {"type": "string"},
                },
                "required": ["repo", "file", "line", "reason"],
                "additionalProperties": False,
            },
        },
        "similar_history": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "why": {"type": "string"}},
                "required": ["path", "why"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["category", "confidence", "cause", "fix_candidates", "similar_history"],
    "additionalProperties": False,
}


def _worktree(name: str, sha: str) -> Path:
    return settings.work_dir / name / sha[:12]


def _failures(summary: dict, run_dir: Path) -> tuple[str, str]:
    """(검색 질의, 프롬프트에 넣을 실패 증거)"""
    if summary.get("mode") == "explore":
        steps = "\n".join(f"- {s['action']} → {s['observation']}"
                          + (f" (스크린샷: {run_dir / 'screens' / s['screenshot']})" if s.get("screenshot") else "")
                          for s in summary["steps"])
        evidence = f"AI 탐색 테스트 판정: {summary['verdict']}\n판정 이유: {summary['explanation']}\n\n단계:\n{steps}"
        return f"{summary['request']} {summary['explanation']}", evidence

    parts, queries = [], []
    for t in summary["tests"]:
        if t["outcome"] != "failed":
            continue
        func = t["name"].split("[")[0]
        network = next((run_dir / "network").glob(f"{t['name'].replace('[', '_').replace(']', '_')}*.jsonl"), None)
        shots = [str(run_dir / a) for a in t["artifacts"] if a.endswith(".png")]
        parts.append(f"## 실패 테스트 {t['file']}::{func}\n"
                     f"테스트 코드: {SCENARIO_DIR / (t['file'].split('.')[-1] + '.py')}\n"
                     f"오류:\n{t['message']}\n스크린샷: {', '.join(shots) or '없음'}\n"
                     f"API 로그(JSONL): {network or '없음'}")
        queries.append(f"{func} {(t['message'] or '').splitlines()[0]}")
    return " ".join(queries), "\n\n".join(parts)


def _verify(candidates: list[dict], front: Path, back: Path) -> None:
    roots = {"frontend": front, "backend": back, "qa": SCENARIO_DIR.parent}
    for c in candidates:
        path = roots[c["repo"]] / c["file"]
        lines = path.read_text(errors="ignore").count("\n") + 1 if path.is_file() else 0
        c["verified"] = 0 < c["line"] <= lines


def run(summary: dict, timeout: float = 600) -> dict:
    run_dir = settings.artifacts_dir / summary["run_id"]
    front, back = _worktree("frontend", summary["frontend_sha"]), _worktree("backend", summary["backend_sha"])
    query, evidence = _failures(summary, run_dir)
    hits = context.retrieve(query)

    system = SYSTEM.format(front=front, back=back, vault=context.search.index.VAULT,
                           categories="\n".join(f"- {k}: {v}" for k, v in CATEGORIES.items()))
    prompt = (f"검증 요청: {summary.get('request') or ', '.join(summary.get('scenarios', []))}\n\n"
              f"# 실패 증거\n{evidence}\n\n# 근거 문서 (검색 결과)\n{context.for_prompt(hits)}")
    dirs = [str(front), str(back), str(run_dir), str(context.search.index.VAULT), str(SCENARIO_DIR)]
    started = time.monotonic()
    try:
        result = claude.structured(
            prompt, SCHEMA, system, tools="Read,Grep,Glob", effort="medium", timeout=timeout,
            extra_args=["--allowedTools", "Read,Grep,Glob", "--add-dir", *dirs], cwd=run_dir,
        )
    except claude.ClaudeError as e:
        return {"error": str(e)}
    _verify(result["fix_candidates"], front, back)
    result["retrieved"] = [h.path for h in hits]
    result["duration_s"] = round(time.monotonic() - started, 1)
    (run_dir / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def needed(summary: dict) -> bool:
    if summary.get("mode") == "explore":
        return summary.get("verdict") == "fail"
    return any(t["outcome"] == "failed" for t in summary.get("tests", []))
