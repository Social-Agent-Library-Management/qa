"""시나리오 실행 한 건 = 스택 준비 → pytest → 결과 요약(summary.json)."""

import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from qa.config import ROOT, settings
from qa.stack import apps

SCENARIO_DIR = ROOT / "scenarios"


def scenario_paths(names: list[str]) -> list[str]:
    if not names or names == ["all"]:
        return [str(SCENARIO_DIR)]
    paths = []
    for name in names:
        path = SCENARIO_DIR / f"test_{name}.py"
        if not path.exists():
            raise FileNotFoundError(f"시나리오 없음: {name} ({path})")
        paths.append(str(path))
    return paths


def _parse_junit(path: Path, run_dir: Path) -> list[dict]:
    tests = []
    for case in ET.parse(path).getroot().iter("testcase"):
        failure = case.find("failure")
        if failure is None:
            failure = case.find("error")
        name = case.get("name", "")
        tests.append({
            "name": name,
            "file": case.get("classname", ""),
            "duration_s": float(case.get("time", 0)),
            "outcome": "skipped" if case.find("skipped") is not None else ("failed" if failure is not None else "passed"),
            "message": (failure.get("message") or "")[:2000] if failure is not None else None,
            # pytest-playwright는 실패 테스트마다 output 하위 폴더에 trace·스크린샷을 둔다.
            "artifacts": sorted(str(p.relative_to(run_dir)) for p in (run_dir / "playwright").rglob("*")
                                if p.is_file() and name.split("[")[0].replace("_", "-") in str(p)),
        })
    return tests


def run(names: list[str], front_ref: str = "HEAD", back_ref: str = "HEAD") -> dict:
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = settings.artifacts_dir / run_id
    run_dir.mkdir(parents=True)
    started = datetime.now().isoformat(timespec="seconds")

    shas = apps.up(front_ref=front_ref, back_ref=back_ref)

    junit = run_dir / "junit.xml"
    cmd = [
        sys.executable, "-m", "pytest", *scenario_paths(names),
        "--base-url", settings.frontend_url,
        "--browser", "chromium",
        "--tracing", "retain-on-failure",
        "--screenshot", "only-on-failure",
        "--output", str(run_dir / "playwright"),
        "--junitxml", str(junit),
        "-p", "no:cacheprovider",
    ]
    with open(run_dir / "pytest.log", "w") as log:
        subprocess.run(cmd, cwd=ROOT, env={**os.environ, "QA_RUN_DIR": str(run_dir)},
                       stdout=log, stderr=subprocess.STDOUT)

    tests = _parse_junit(junit, run_dir) if junit.exists() else []
    summary = {
        "run_id": run_id,
        "scenarios": names or ["all"],
        **shas,
        "started_at": started,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "passed": bool(tests) and all(t["outcome"] != "failed" for t in tests),
        "tests": tests,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary
