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

    args = parser.parse_args()
    if args.cmd == "stack":
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
