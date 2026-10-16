"""백그라운드 프로세스 기동·정지와 준비 대기."""

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import httpx

from qa.config import settings

STATE_FILE = settings.work_dir / "stack.json"
LOG_DIR = settings.work_dir / "logs"


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def spawn(name: str, cmd: list[str], cwd: Path, env: dict[str, str]) -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log = open(LOG_DIR / f"{name}.log", "w")
    proc = subprocess.Popen(
        cmd, cwd=cwd, env={**os.environ, **env},
        stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
    )
    return proc.pid


def stop(pid: int) -> None:
    if not is_alive(pid):
        return
    # 세션 리더로 띄웠으므로 그룹 전체(npm → node 자식 포함)를 내린다.
    os.killpg(pid, signal.SIGTERM)
    for _ in range(50):
        if not is_alive(pid):
            return
        time.sleep(0.2)
    os.killpg(pid, signal.SIGKILL)


def wait_http(name: str, url: str, pid: int, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not is_alive(pid):
            raise RuntimeError(f"{name} 프로세스가 종료됨 — 로그: {LOG_DIR / f'{name}.log'}")
        try:
            if httpx.get(url, timeout=2).status_code < 500:
                return
        except httpx.HTTPError:
            pass
        time.sleep(1)
    raise TimeoutError(f"{name} 준비 대기 시간 초과 ({url})")


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None, log_name: str | None = None) -> None:
    """빌드처럼 끝나야 하는 명령. 실패 시 로그 경로를 알려준다."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{log_name or cmd[0]}.log"
    with open(log_path, "w") as log:
        result = subprocess.run(cmd, cwd=cwd, env={**os.environ, **(env or {})}, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise RuntimeError(f"`{' '.join(cmd)}` 실패 — 로그: {log_path}")
