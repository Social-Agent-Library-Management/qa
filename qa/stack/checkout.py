"""검증 대상 레포를 커밋 단위 git worktree로 체크아웃한다.

개발자의 작업 트리(실행 중인 dev 서버, 빌드 산출물)를 건드리지 않고,
"어느 커밋을 검증했는가"를 결과에 남기기 위해 항상 sha로 고정한다.
"""

import subprocess
from pathlib import Path

from qa.config import settings


def resolve_sha(repo: Path, ref: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", f"{ref}^{{commit}}"],
        check=True, capture_output=True, text=True,
    )
    return out.stdout.strip()


def checkout(name: str, repo: Path, ref: str) -> tuple[str, Path]:
    sha = resolve_sha(repo, ref)
    path = settings.work_dir / name / sha[:12]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "-C", str(repo), "worktree", "add", "--detach", str(path), sha],
            check=True, capture_output=True, text=True,
        )
    return sha, path
