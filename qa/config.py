from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QA_", env_file=ROOT / ".env", extra="ignore")

    backend_dir: Path
    frontend_dir: Path
    java_home: Path = Path("/opt/homebrew/opt/openjdk@21")

    # compose.qa.yml과 짝을 이루는 값 — 바꾸면 양쪽을 같이 바꾼다.
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3307
    mysql_user: str = "root"
    mysql_password: str = "qa"
    mysql_db: str = "library_qa"
    opensearch_port: int = 9201
    redis_url: str = "redis://localhost:6380/0"

    backend_port: int = 8081
    frontend_port: int = 3001
    api_port: int = 8090

    # 캡처 화면 크기 — 시나리오 테스트와 AI 탐색이 같은 값을 써야 스크린샷끼리(디자인 비교 포함) 맞댈 수 있다.
    viewport_width: int = 1440
    viewport_height: int = 900

    # 작업 완료 결과를 받을 곳(n8n 출구 웹훅). 비어 있으면 로그만 남긴다.
    callback_url: str | None = None
    # n8n(컨테이너)이 산출물(스크린샷)을 내려받을 때 쓰는 이 API의 주소
    api_url_for_n8n: str = "http://host.docker.internal:8090"

    # 근거 문서 검색 방식 (vector | keyword | agentic) — 측정 결과로 정한다
    rag_method: str = "vector"

    # Claude Code 헤드리스 호출용 구독 토큰 (`claude setup-token`)
    claude_code_oauth_token: str | None = Field(default=None, validation_alias="CLAUDE_CODE_OAUTH_TOKEN")

    work_dir: Path = ROOT / ".work"
    artifacts_dir: Path = ROOT / "artifacts"

    @property
    def backend_url(self) -> str:
        return f"http://localhost:{self.backend_port}"

    @property
    def frontend_url(self) -> str:
        return f"http://localhost:{self.frontend_port}"

    @property
    def opensearch_url(self) -> str:
        return f"http://localhost:{self.opensearch_port}"


settings = Settings()
