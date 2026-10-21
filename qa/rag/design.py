"""디자인 원본(design/) → vault 화면 시안 노트(이미지 + 화면 구성).

design/은 Claude Design 사본(HTML·JS)이라 Obsidian에서 볼 수 없고 RAG로 검색할 텍스트도 없다.
화면마다 QA 캡처와 같은 1440×900으로 렌더링해 이미지로 남기고, 접근성 트리를 텍스트로 붙여
기획서·디자인 스펙과 같은 방식으로 검색·인용되게 한다. 노트는 생성물이므로 손으로 고치지 않는다.
"""

import functools
import http.server
import threading
from pathlib import Path

from qa.config import ROOT, settings
from qa.rag.index import VAULT

DESIGN_DIR = ROOT / "design"
OUT_DIR = VAULT / "디자인" / "화면"
ENTRY = "ui_kits/library/index.html"

# 화면 ID(design/ui_kits/library/index.html) → 노트 이름, 관련 디자인 스펙 노트
SCREENS = {
    "dashboard": ("대시보드", ["2026-09-08 대시보드", "2026-09-29 대시보드 최근 활동 패널"]),
    "book-search": ("도서 검색", ["2026-08-16 도서 검색", "2026-09-01 도서 검색 오타 교정 제안"]),
    "loan-register": ("대출 등록", ["2026-08-12 대출 등록"]),
    "return": ("반납 처리", ["2026-08-13 반납 처리"]),
    "book-register": ("관리자 도서 등록", ["2026-08-11 도서 등록", "2026-08-14 도서 등록 출판사 필드·목록 컬럼 확장",
                                     "2026-09-07 관리자 도서 목록 검색바", "2026-09-01 사이드바 개편·관리자 페이지"]),
    "copy-register": ("관리자 소장본 등록", ["2026-08-12 소장본 등록", "2026-08-24 소장본 목록·상태 변경"]),
    "loan-history": ("관리자 대출 내역 조회", ["2026-08-13 대출 내역 조회", "2026-08-14 대출 내역 반납일 컬럼·연체 필터",
                                        "2026-08-14 연체 목록"]),
    "excel-import": ("관리자 엑셀 일괄 등록", ["2026-08-26 엑셀 일괄 등록·내보내기"]),
    "data-export": ("관리자 내보내기", ["2026-08-26 엑셀 일괄 등록·내보내기"]),
}
COMMON_SPECS = ["2026-08-10 공용 앱 셸", "2026-08-10 디자인 시스템 파운데이션 (토큰·재사용 컴포넌트)"]


def _serve() -> tuple[http.server.ThreadingHTTPServer, str]:
    # file://에서는 localStorage·상대 경로 스크립트가 브라우저마다 다르게 동작해 로컬 HTTP로 연다.
    handler = functools.partial(_QuietHandler, directory=str(DESIGN_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args) -> None:
        pass


def _note(screen_id: str, name: str, specs: list[str], aria: str) -> str:
    links = "\n".join(f"- [[{s}]]" for s in specs + COMMON_SPECS)
    return f"""---
type: 디자인
kind: 화면 시안
screen_id: {screen_id}
source: "design/{ENTRY}"
---
# {name} 디자인 시안

Claude Design 프로토타입을 QA 캡처와 같은 {settings.viewport_width}×{settings.viewport_height}로 렌더링한 화면이다.
목업 데이터는 QA 시드와 다르므로 구현 화면과는 **배치·구성·스타일**로만 비교한다(글자·숫자 값 차이는 결함이 아니다).

![[{name}.png]]

## 관련 디자인 스펙
{links}

## 화면 구성 (본문 접근성 트리, 공통 사이드바 제외)
```yaml
{aria.strip()}
```
"""


def render() -> list[Path]:
    """모든 화면을 렌더링해 vault 노트·이미지를 다시 만든다. 이후 `qa rag sync`로 색인한다."""
    from playwright.sync_api import sync_playwright

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    server, base = _serve()
    written = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for screen_id, (name, specs) in SCREENS.items():
                ctx = browser.new_context(viewport={"width": settings.viewport_width,
                                                    "height": settings.viewport_height})
                ctx.add_init_script(f"localStorage.setItem('lib_ds_loggedIn','1');"
                                    f"localStorage.setItem('lib_ds_screen','{screen_id}');")
                page = ctx.new_page()
                errors: list[str] = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(f"{base}/{ENTRY}", wait_until="networkidle")
                # 프로토타입은 브라우저에서 JSX를 변환해 그린다 — 사이드바가 보일 때까지 기다린다.
                page.get_by_role("navigation").first.wait_for(timeout=15_000)
                page.wait_for_timeout(500)
                if errors:
                    raise RuntimeError(f"디자인 화면 렌더링 오류 ({screen_id}): {errors[0]}")
                page.screenshot(path=OUT_DIR / f"{name}.png")
                note = OUT_DIR / f"{name}.md"
                # 사이드바는 모든 화면에 반복돼 검색을 흐리므로 본문(main)만 텍스트로 남긴다.
                note.write_text(_note(screen_id, name, specs, page.locator("main").aria_snapshot()))
                written.append(note)
                ctx.close()
            browser.close()
    finally:
        server.shutdown()
    return written


def image_for(note_path: str) -> Path | None:
    """화면 시안 노트(vault 상대 경로) → 시안 이미지 절대 경로."""
    path = VAULT / note_path
    if path.parent != OUT_DIR:
        return None
    image = path.with_suffix(".png")
    return image if image.is_file() else None


def screen_note_for(note_path: str) -> str | None:
    """디자인 스펙 노트(vault 상대 경로) → 그 스펙을 반영한 화면 시안 노트 경로. 첫 번째 화면을 쓴다."""
    stem = Path(note_path).stem
    for name, specs in SCREENS.values():
        if stem in specs and (OUT_DIR / f"{name}.md").is_file():
            return str((OUT_DIR / f"{name}.md").relative_to(VAULT))
    return None
