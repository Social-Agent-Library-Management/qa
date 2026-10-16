"""자연어 요청 → 실행할 시나리오와 검증 대상 ref."""

from dataclasses import dataclass

from qa.intent import catalog, claude

SYSTEM = """너는 도서관 관리 시스템 QA 봇의 요청 해석기다.
사용자의 자연어 요청을 보고 카탈로그에서 실행할 시나리오 id를 고른다.

규칙:
- 카탈로그에 있는 id만 고른다. 요청과 관련된 시나리오는 빠짐없이 고른다.
- "전체", "다", "전부", "회귀" 같은 요청이면 모든 시나리오를 고른다.
- 카탈로그로 검증할 수 없는 요청이면 빈 배열을 돌려주고 reason에 무엇이 없는지 적는다.
- 프론트/백엔드 브랜치·커밋을 언급하면 front_ref/back_ref에 그 문자열을 그대로 넣는다. 언급이 없으면 null.
- reason은 한국어 한 문장으로, 왜 그 시나리오를 골랐는지 적는다."""


@dataclass
class Intent:
    scenarios: list[str]
    front_ref: str | None
    back_ref: str | None
    reason: str


def map_request(text: str) -> Intent:
    scenarios = catalog.load()
    listing = "\n".join(f"- {s.id}: {s.title} — {s.description}" for s in scenarios)
    schema = {
        "type": "object",
        "properties": {
            # enum으로 묶어 카탈로그 밖의 id가 나올 수 없게 한다.
            "scenarios": {"type": "array", "items": {"type": "string", "enum": [s.id for s in scenarios]}},
            "front_ref": {"type": ["string", "null"]},
            "back_ref": {"type": ["string", "null"]},
            "reason": {"type": "string"},
        },
        "required": ["scenarios", "front_ref", "back_ref", "reason"],
        "additionalProperties": False,
    }
    out = claude.structured(f"카탈로그:\n{listing}\n\n요청: {text}", schema, SYSTEM)
    known = {s.id for s in scenarios}
    return Intent(
        scenarios=[s for s in dict.fromkeys(out["scenarios"]) if s in known],
        front_ref=out.get("front_ref") or None,
        back_ref=out.get("back_ref") or None,
        reason=out["reason"],
    )
