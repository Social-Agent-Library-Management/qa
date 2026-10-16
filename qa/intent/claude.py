"""Claude Code 헤드리스 호출.

API 키 대신 구독 OAuth 토큰(CLAUDE_CODE_OAUTH_TOKEN)으로 Claude Code CLI를 실행한다.
구독 토큰은 Claude Code 전용이라 SDK로 API를 직접 부르지 않고 CLI를 거친다.
"""

import json
import os
import subprocess
from pathlib import Path

from qa.config import settings


class ClaudeError(RuntimeError):
    pass


# 개발자 환경(훅·MCP·스킬·CLAUDE.md)이 검증 판단에 섞이지 않도록 격리한다.
# --bare는 OAuth 토큰을 읽지 않으므로 쓰지 않는다.
ISOLATION = [
    "--setting-sources", "",
    "--strict-mcp-config",
    "--no-session-persistence",
    "--disable-slash-commands",
]


def structured(prompt: str, schema: dict, system: str, tools: str = "", effort: str = "low",
               timeout: float = 120, extra_args: list[str] | None = None, cwd: Path | None = None) -> dict:
    if not settings.claude_code_oauth_token:
        raise ClaudeError("CLAUDE_CODE_OAUTH_TOKEN 미설정 (.env)")
    cwd = cwd or settings.work_dir / "claude"
    cwd.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # API 키가 있으면 토큰보다 우선한다
    env["CLAUDE_CODE_OAUTH_TOKEN"] = settings.claude_code_oauth_token
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--json-schema", json.dumps(schema, ensure_ascii=False),
        "--system-prompt", system,
        "--tools", tools,
        "--effort", effort,
        *ISOLATION,
        *(extra_args or []),
    ]
    try:
        out = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise ClaudeError(f"Claude Code 응답 시간 초과 ({timeout}s)") from e
    try:
        result = json.loads(out.stdout)
    except json.JSONDecodeError as e:
        raise ClaudeError(f"Claude Code 출력 파싱 실패: {out.stderr[-500:] or out.stdout[-500:]}") from e
    if result.get("is_error") or result.get("structured_output") is None:
        raise ClaudeError(f"Claude Code 실패: {result.get('subtype')} {str(result.get('result'))[:300]}")
    return result["structured_output"]
