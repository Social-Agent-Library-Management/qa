"""AI 탐색 테스트: 자연어 요청을 Claude Code가 브라우저(Playwright MCP)로 직접 수행하고 증거와 함께 판정한다.

미리 작성된 시나리오가 없을 때 쓰는 경로다. 판정은 반드시 스크린샷 증거를 동반해야 하며,
증거 파일이 실제로 없으면 '판단 불가'로 강등한다 — 확인하지 않고 통과라고 말하는 것을 막는다.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import yaml

from qa.config import settings
from qa.intent import claude
from qa.rag import context
from qa.seed import reset
from qa.stack import apps

PLAYWRIGHT_MCP = "@playwright/mcp@0.0.83"

SYSTEM = """너는 도서관 관리 시스템의 QA 테스터다. 사람이 하듯이 브라우저로 화면을 직접 조작해 요청을 검증한다.

환경:
- 프론트엔드: {base_url} (관리자 화면, 로그인 없음)
- 데이터는 방금 아래 시드 상태로 초기화되었다. 자유롭게 등록·대출·반납해도 된다.
{seed}

판정 근거 문서 (vault의 기획서·과거 이력에서 요청과 관련된 것을 찾아 붙였다):
{references}

기대 동작은 위 문서에서 찾는다. 기획서와 이력이 다르면 더 최근에 구현된 이력을 우선한다.
판정에 쓴 문서는 references에 경로와 근거 문장을 그대로 인용해 남긴다.
문서에 기대 동작이 없으면 상식으로 추측하지 말고, 그 사실을 summary에 밝힌다.

진행 규칙:
- 브라우저 도구만 사용한다. URL을 직접 추측하기보다 화면의 메뉴와 링크를 따라간다.
- 검증 대상과 관련된 화면은 빠짐없이 둘러본다. 사람이 놓치기 쉬운 화면(대시보드, 다른 목록 화면)도 확인한다.
- 판정에 쓰는 화면마다 browser_take_screenshot으로 캡처하고 filename을 "NN-설명.png"(예: 03-대출내역-반납완료.png)로 지정한다.
- 화면의 실제 텍스트(스냅샷)로 확인한 사실만 적는다. 추측으로 판정하지 않는다.

판정:
- pass: 요청한 동작이 모든 관련 화면에서 기대대로임을 스크린샷으로 확인함
- fail: 기대와 다른 화면을 하나 이상 발견함 (어느 화면에서 무엇이 보였는지 적는다)
- inconclusive: 조작이 막히거나 기대 동작이 불분명해 판단할 수 없음
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "fail", "inconclusive"]},
        "summary": {"type": "string", "description": "판정 이유 한두 문장"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {"type": "string"},
                    "observation": {"type": "string", "description": "화면에서 실제로 확인한 내용"},
                    "screenshot": {"type": ["string", "null"], "description": "캡처 파일명"},
                },
                "required": ["action", "observation", "screenshot"],
                "additionalProperties": False,
            },
        },
        "references": {
            "type": "array",
            "description": "판정에 사용한 근거 문서",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "근거 문서 목록에 있는 경로 그대로"},
                    "quote": {"type": "string", "description": "문서에서 그대로 옮긴 근거 문장"},
                },
                "required": ["path", "quote"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["verdict", "summary", "steps", "references"],
    "additionalProperties": False,
}


def _normalize(text: str) -> str:
    # 마크다운 기호·공백 차이로 정상 인용이 불일치 처리되지 않도록 비교용으로만 정규화한다.
    return re.sub(r"[\s*`>|#_\-]+", "", text)


def _seed_description(data: dict) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def run(request: str, front_ref: str = "HEAD", back_ref: str = "HEAD", job_id: str | None = None,
        timeout: float = 600) -> dict:
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = settings.artifacts_dir / run_id
    shots = run_dir / "screens"
    shots.mkdir(parents=True)
    started = datetime.now().isoformat(timespec="seconds")

    shas = apps.up(front_ref=front_ref, back_ref=back_ref)
    seed = reset.reset()

    mcp_config = run_dir / "mcp.json"
    mcp_config.write_text(json.dumps({"mcpServers": {"playwright": {
        "command": "npx",
        "args": ["-y", PLAYWRIGHT_MCP, "--headless", "--isolated", "--browser", "chromium",
                 "--viewport-size", "1440,900", "--output-dir", str(shots)],
    }}}))

    hits = context.retrieve(request)
    system = SYSTEM.format(base_url=settings.frontend_url, seed=_seed_description(seed),
                           references=context.for_prompt(hits))
    error = None
    try:
        result = claude.structured(
            f"검증 요청: {request}", SCHEMA, system,
            tools="", effort="medium", timeout=timeout,
            extra_args=["--mcp-config", str(mcp_config), "--allowedTools", "mcp__playwright__*"],
            # 파일명을 지정한 스크린샷은 --output-dir가 아니라 MCP 프로세스의 작업 폴더에 저장된다.
            cwd=shots,
        )
    except claude.ClaudeError as e:
        result, error = {"verdict": "inconclusive", "summary": str(e), "steps": [], "references": []}, str(e)

    # 근거 검증: 제공하지 않은 문서를 인용했거나 인용문이 그 문서에 없으면 지어낸 근거로 본다.
    provided = {h.path: h.text for h in hits}
    for ref in result["references"]:
        source = provided.get(ref["path"])
        ref["verified"] = bool(source) and _normalize(ref["quote"]) in _normalize(source)

    # 증거 검증: 언급한 스크린샷이 실제로 없으면 그 판정은 믿을 수 없다.
    existing = {p.name for p in shots.rglob("*.png")}
    for step in result["steps"]:
        if step["screenshot"] and Path(step["screenshot"]).name not in existing:
            step["screenshot_missing"] = True
    cited = [s for s in result["steps"] if s["screenshot"] and not s.get("screenshot_missing")]
    if result["verdict"] != "inconclusive" and not cited:
        result["summary"] = f"[증거 없음 → 판단 불가로 강등] {result['summary']}"
        result["verdict"] = "inconclusive"

    summary = {
        "run_id": run_id,
        "job_id": job_id,
        "mode": "explore",
        "request": request,
        **shas,
        "started_at": started,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "passed": result["verdict"] == "pass",
        "verdict": result["verdict"],
        "explanation": result["summary"],
        "steps": result["steps"],
        "references": result["references"],
        "retrieved": [h.path for h in hits],
        "screenshots": sorted(str(p.relative_to(run_dir)) for p in shots.rglob("*.png")),
        "error": error,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary
