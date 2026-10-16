"""검증 대상 백엔드·프론트엔드를 지정 커밋으로 빌드해 QA 포트에 띄운다."""

from pathlib import Path

from qa.config import settings
from qa.stack import checkout, process


def _backend_env() -> dict[str, str]:
    # application.yml 값을 relaxed binding으로 덮어쓴다 — 백엔드 코드는 수정하지 않는다.
    return {
        "JAVA_HOME": str(settings.java_home),
        "SERVER_PORT": str(settings.backend_port),
        "SPRING_DATASOURCE_URL": f"jdbc:mysql://{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db}",
        "SPRING_DATASOURCE_USERNAME": settings.mysql_user,
        "SPRING_DATASOURCE_PASSWORD": settings.mysql_password,
        "OPENSEARCH_HOST": "localhost",
        "OPENSEARCH_PORT": str(settings.opensearch_port),
        "CORS_ALLOWED_ORIGINS": settings.frontend_url,
    }


def _build_backend(path: Path) -> Path:
    jars = [j for j in (path / "build/libs").glob("*.jar") if not j.name.endswith("-plain.jar")] \
        if (path / "build/libs").exists() else []
    if not jars:
        process.run(["./gradlew", "bootJar", "-x", "test", "--quiet"], cwd=path,
                    env={"JAVA_HOME": str(settings.java_home)}, log_name="backend-build")
        jars = [j for j in (path / "build/libs").glob("*.jar") if not j.name.endswith("-plain.jar")]
    return jars[0]


def _build_frontend(path: Path) -> None:
    api_url = settings.backend_url
    marker = path / ".qa-build-api-url"
    if not (path / "node_modules").exists():
        process.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=path, log_name="frontend-install")
    # NEXT_PUBLIC_*는 빌드 시점에 박히므로 API 주소가 바뀌면 다시 빌드한다.
    if not (path / ".next/BUILD_ID").exists() or not marker.exists() or marker.read_text() != api_url:
        process.run(["npm", "run", "build"], cwd=path,
                    env={"NEXT_PUBLIC_API_BASE_URL": api_url}, log_name="frontend-build")
        marker.write_text(api_url)


def up(front_ref: str = "HEAD", back_ref: str = "HEAD") -> dict:
    state = process.load_state()

    back_sha, back_path = checkout.checkout("backend", settings.backend_dir, back_ref)
    back = state.get("backend")
    if not (back and back["sha"] == back_sha and process.is_alive(back["pid"])):
        if back:
            process.stop(back["pid"])
        jar = _build_backend(back_path)
        java = str(settings.java_home / "bin/java")
        # application.yml은 백엔드 레포에서 gitignore(비밀번호 포함)라 커밋 체크아웃에는 없다.
        # 개발자 로컬 설정을 그대로 쓰고, DB·포트·CORS는 위 환경변수가 우선해 QA 값으로 덮인다.
        config = settings.backend_dir / "src/main/resources/application.yml"
        pid = process.spawn("backend", [java, "-jar", str(jar), f"--spring.config.location=file:{config}"],
                            cwd=back_path, env=_backend_env())
        state["backend"] = {"sha": back_sha, "pid": pid}
        process.save_state(state)
    # 검색 API는 books 인덱스(시드 리셋이 생성)에 의존하므로 DB만 타는 대출 목록으로 준비를 확인한다.
    process.wait_http("backend", f"{settings.backend_url}/loans?pageSize=1",
                      state["backend"]["pid"], timeout=180)

    front_sha, front_path = checkout.checkout("frontend", settings.frontend_dir, front_ref)
    front = state.get("frontend")
    if not (front and front["sha"] == front_sha and process.is_alive(front["pid"])):
        if front:
            process.stop(front["pid"])
        _build_frontend(front_path)
        pid = process.spawn("frontend", ["npm", "run", "start", "--", "-p", str(settings.frontend_port)],
                            cwd=front_path, env={})
        state["frontend"] = {"sha": front_sha, "pid": pid}
        process.save_state(state)
    process.wait_http("frontend", settings.frontend_url, state["frontend"]["pid"], timeout=60)

    return {"backend_sha": back_sha, "frontend_sha": front_sha}


def down() -> None:
    state = process.load_state()
    for name in ("frontend", "backend"):
        if name in state:
            process.stop(state[name]["pid"])
    process.save_state({})
