import json
import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, Response, expect

from qa.config import settings
from qa.seed import reset

# 토스트가 2.8초 뒤 닫히므로 기본 5초 대기면 충분하다. 검색 디바운스(250ms)도 이 안에 들어온다.
expect.set_options(timeout=5_000)


@pytest.fixture(autouse=True)
def seed() -> dict:
    """매 테스트를 동일한 시드 상태에서 시작한다."""
    return reset.reset()


@pytest.fixture(autouse=True)
def network_log(page: Page, request: pytest.FixtureRequest):
    """백엔드 API 요청·응답을 JSONL로 남긴다 — 실패 분석에서 '화면 문제인지 API 계약 문제인지'를 가르는 근거."""
    run_dir = Path(os.environ.get("QA_RUN_DIR", settings.artifacts_dir / "adhoc"))
    out = run_dir / "network" / f"{re.sub(r'[^A-Za-z0-9_.-]', '_', request.node.name)}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    def on_response(res: Response) -> None:
        if not res.url.startswith(settings.backend_url):
            return
        try:
            body = res.json()
        except Exception:
            body = None
        lines.append(json.dumps({
            "method": res.request.method,
            "url": res.url,
            "status": res.status,
            "request_body": res.request.post_data,
            "response_body": body,
        }, ensure_ascii=False))

    page.on("response", on_response)
    yield
    out.write_text("\n".join(lines) + ("\n" if lines else ""))
