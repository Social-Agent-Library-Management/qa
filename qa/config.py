from pathlib import Path

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

    backend_port: int = 8081
    frontend_port: int = 3001

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
