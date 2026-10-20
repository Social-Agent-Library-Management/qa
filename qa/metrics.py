"""운영 지표: artifacts/*/summary.json을 오프라인으로 집계한다.

실행 중에는 기록만 하고 집계는 여기서 따로 한다 — 집계 코드의 버그가 검증 실행을 깨뜨리지 않게.
지표는 이력서·포트폴리오 수치의 출처이므로 '무엇을 셌는지'를 리포트에 함께 적는다.
"""

import json
import statistics
from collections import Counter
from datetime import datetime

from qa.config import ROOT, settings
from qa.intent import catalog


def _load() -> list[dict]:
    runs = []
    for path in sorted(settings.artifacts_dir.glob("*/summary.json")):
        s = json.loads(path.read_text())
        analysis = path.with_name("analysis.json")
        if "analysis" not in s and analysis.exists():
            s["analysis"] = json.loads(analysis.read_text())
        runs.append(s)
    return runs


def _seconds(a: str | None, b: str | None) -> float | None:
    if not a or not b:
        return None
    return (datetime.fromisoformat(b) - datetime.fromisoformat(a)).total_seconds()


def _verdict(s: dict) -> str:
    return s.get("verdict") or ("pass" if s.get("passed") else "fail")


def _median(xs: list[float]) -> str:
    xs = [x for x in xs if x is not None]
    if not xs:
        return "-"
    m = statistics.median(xs)
    return f"{m / 60:.1f}분" if m >= 90 else f"{m:.0f}초"


def _pct(n: int, d: int) -> str:
    return f"{n}/{d} ({n / d:.0%})" if d else "-"


def build() -> str:
    runs = _load()
    requests = [s for s in runs if s.get("job_id")]       # 큐로 접수된 요청
    manual = [s for s in runs if not s.get("job_id")]      # CLI 직접 실행
    explores = [s for s in runs if s.get("mode") == "explore"]
    scenarios = [s for s in runs if s.get("mode") != "explore"]
    analyses = [s["analysis"] for s in runs if s.get("analysis") and "error" not in s["analysis"]]

    by_mode = Counter(s.get("mode", "scenario") for s in requests)
    by_source = Counter(s.get("source") or "기록 없음(계측 전)" for s in requests)
    lines = [
        "# QA 서비스 운영 지표", "",
        f"> 생성: `qa metrics` — {datetime.now():%Y-%m-%d %H:%M} · 원천: `artifacts/*/summary.json` {len(runs)}건", "",
        "## 요청",
        f"- 접수된 검증 요청: **{len(requests)}건** (출처: "
        + ", ".join(f"{k} {v}" for k, v in by_source.most_common()) + ")",
        f"  - 시나리오 테스트 {by_mode.get('scenario', 0)} · AI 탐색 {by_mode.get('explore', 0)}",
        f"- CLI 직접 실행: {len(manual)}건",
        f"- 대기 시간 중앙값(접수→시작): {_median([_seconds(s.get('enqueued_at'), s.get('job_started_at')) for s in requests])}",
        f"- 현재 시나리오 수: {len(catalog.load())}개",
        "",
        "## 판정",
        "| 방식 | 실행 | 통과 | 실패 | 판단 불가 | 실행 시간 중앙값 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label, group in (("시나리오 테스트", scenarios), ("AI 탐색", explores)):
        v = Counter(_verdict(s) for s in group)
        lines.append(f"| {label} | {len(group)} | {v['pass']} | {v['fail']} | {v['inconclusive']} | "
                     f"{_median([_seconds(s['started_at'], s['finished_at']) for s in group])} |")

    refs = [r for s in explores for r in s.get("references", [])]
    downgraded = sum(1 for s in explores if s.get("explanation", "").startswith("[증거 없음"))
    lines += [
        "",
        "## AI 탐색 근거",
        f"- 스크린샷 증거 수 중앙값: "
        + (f"{statistics.median(len(s.get('screenshots', [])) for s in explores):.0f}장" if explores else "-"),
        f"- 근거 문서 인용 원문 일치: {_pct(sum(bool(r.get('verified')) for r in refs), len(refs))}",
        f"- 증거 없음으로 '판단 불가' 강등: {downgraded}건",
        "",
        "## 실패 분석",
        f"- 분석 실행: {len(analyses)}건 · 소요 중앙값 {_median([a.get('duration_s') for a in analyses])}",
        "- 분류: " + (", ".join(f"`{k}` {v}" for k, v in Counter(a['category'] for a in analyses).most_common()) or "-"),
    ]
    cands = [c for a in analyses for c in a.get("fix_candidates", [])]
    lines += [f"- 수정 후보 위치 실존 확인: {_pct(sum(bool(c.get('verified')) for c in cands), len(cands))}", ""]
    return "\n".join(lines)


def write() -> str:
    text = build()
    (ROOT / "metrics.md").write_text(text)
    return text
