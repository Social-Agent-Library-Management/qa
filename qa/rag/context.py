"""검증 요청에 붙일 근거 문서(기획서·디자인 스펙·과거 이력)를 찾아 프롬프트용으로 만든다."""

from pathlib import Path

from qa.config import settings
from qa.rag import design, search

# 디자인 스펙 노트는 18개라 상위 결과를 독차지하기 쉽다 — 기획서·이력이 밀려나지 않게 상한을 둔다.
MAX_DESIGN_NOTES = 2
OTHER_SOURCES = ["기획서", "이력", "QA 리포트"]


def retrieve(request: str, notes: int = 5) -> list[search.Hit]:
    method = search.METHODS[settings.rag_method]
    # 노트당 청크가 여러 개라 넉넉히 뽑은 뒤 노트 단위로 줄인다.
    out, designs, screen = [], 0, None
    for h in search.unique_notes(method(request, k=notes * 20)):
        if design.image_for(h.path):
            screen = screen or h          # 화면 시안은 아래에서 따로 한 자리를 준다
            continue
        if h.path.startswith("디자인/"):
            if designs >= MAX_DESIGN_NOTES:
                continue
            designs += 1
        out.append(h)
        if len(out) == notes:
            break
    # 디자인 청크가 후보를 다 차지해 자리가 남으면, 디자인 외 출처에서 따로 찾아 채운다.
    if len(out) < notes:
        seen = {h.path for h in out}
        extra = [h for src in OTHER_SOURCES for h in search.unique_notes(method(request, k=notes * 4, source=src))
                 if h.path not in seen]
        out += sorted(extra, key=lambda h: -h.score)[:notes - len(out)]
    # 관련 디자인 스펙이 있으면 그 화면의 시안(이미지)을 함께 붙인다 — 기획서처럼 판정 근거로 쓰게 한다.
    spec = next((h for h in out if h.path.startswith("디자인/")), None)
    if spec and not screen and (path := design.screen_note_for(spec.path)):
        screen = search.Hit(path, Path(path).stem, "", (design.VAULT / path).read_text(), spec.score)
    return out + ([screen] if screen else [])


def for_prompt(hits: list[search.Hit]) -> str:
    if not hits:
        return "(관련 문서를 찾지 못했다)"
    blocks = []
    for i, h in enumerate(hits, 1):
        image = design.image_for(h.path)
        # 화면 시안은 이미지가 본체다 — 경로를 주고 직접 열어 보게 한다.
        note = f"\n(디자인 시안 이미지: {image} — Read로 열어 구현 화면과 비교)" if image else ""
        blocks.append(f"### [{i}] {h.path}{note}\n{h.text.strip()}")
    return "\n\n".join(blocks)
