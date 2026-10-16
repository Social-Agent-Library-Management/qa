"""검증 요청에 붙일 근거 문서(기획서·디자인 스펙·과거 이력)를 찾아 프롬프트용으로 만든다."""

from qa.config import settings
from qa.rag import search


def retrieve(request: str, notes: int = 5) -> list[search.Hit]:
    method = search.METHODS[settings.rag_method]
    # 노트당 청크가 여러 개라 넉넉히 뽑은 뒤 노트 단위로 줄인다.
    return search.unique_notes(method(request, k=notes * 4))[:notes]


def for_prompt(hits: list[search.Hit]) -> str:
    if not hits:
        return "(관련 문서를 찾지 못했다)"
    return "\n\n".join(f"### [{i}] {h.path}\n{h.text.strip()}" for i, h in enumerate(hits, 1))
