import argparse
import json

from qa import runner
from qa.seed import reset
from qa.stack import apps


def main() -> None:
    parser = argparse.ArgumentParser(prog="qa")
    sub = parser.add_subparsers(dest="cmd", required=True)

    stack = sub.add_parser("stack", help="검증 대상 백엔드·프론트 기동/정지")
    stack.add_argument("action", choices=["up", "down"])
    stack.add_argument("--front-ref", default="HEAD")
    stack.add_argument("--back-ref", default="HEAD")

    sub.add_parser("reset", help="QA DB·검색 인덱스를 시드 상태로 되돌림")

    run = sub.add_parser("run", help="시나리오 실행")
    run.add_argument("scenarios", nargs="*", help="예: loan_return (생략 시 전체)")
    run.add_argument("--front-ref", default="HEAD")
    run.add_argument("--back-ref", default="HEAD")

    sub.add_parser("api", help="작업 접수 API 서버")
    sub.add_parser("worker", help="작업 실행 워커 (하나만 띄운다)")

    args = parser.parse_args()
    if args.cmd == "api":
        import uvicorn

        from qa.config import settings
        uvicorn.run("qa.api.app:app", host="0.0.0.0", port=settings.api_port)
    elif args.cmd == "worker":
        import logging

        from rq import SimpleWorker

        from qa.jobs.queue import queue, redis
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
        # fork 없이 같은 프로세스에서 실행한다 — macOS의 fork 안전성 문제를 피하고,
        # 실제 무거운 일(빌드·브라우저)은 어차피 하위 프로세스가 한다.
        SimpleWorker([queue()], connection=redis()).work()
    elif args.cmd == "stack":
        if args.action == "up":
            print(json.dumps(apps.up(args.front_ref, args.back_ref), indent=2))
        else:
            apps.down()
    elif args.cmd == "reset":
        reset.reset()
        print("reset 완료")
    elif args.cmd == "run":
        summary = runner.run(args.scenarios, args.front_ref, args.back_ref)
        for t in summary["tests"]:
            print(f"{t['outcome'].upper():7} {t['name']}")
        print(f"\n{'PASS' if summary['passed'] else 'FAIL'} — artifacts/{summary['run_id']}/summary.json")
        raise SystemExit(0 if summary["passed"] else 1)
