"""시나리오 카탈로그 = scenarios/test_*.py의 테스트 함수와 docstring.

별도 목록 파일을 두지 않는다 — 테스트를 추가하면 docstring이 곧 자연어 매핑 대상이 된다.
docstring 첫 줄은 "제목: 설명" 형식이다.
"""

import ast
from dataclasses import dataclass

from qa.runner import SCENARIO_DIR


@dataclass(frozen=True)
class Scenario:
    id: str          # "<파일명에서 test_ 뺀 이름>::<함수명>" — runner가 그대로 받는다
    title: str
    description: str


def load() -> list[Scenario]:
    scenarios = []
    for path in sorted(SCENARIO_DIR.glob("test_*.py")):
        module = path.stem.removeprefix("test_")
        for node in ast.parse(path.read_text()).body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                doc = (ast.get_docstring(node) or node.name).strip().splitlines()[0]
                title, _, desc = doc.partition(":")
                scenarios.append(Scenario(f"{module}::{node.name}", title.strip(), desc.strip() or title.strip()))
    return scenarios


def by_id() -> dict[str, Scenario]:
    return {s.id: s for s in load()}
