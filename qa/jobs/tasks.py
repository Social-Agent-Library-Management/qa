"""워커가 실행하는 작업 본체."""

import logging

import httpx
from rq import get_current_job

from qa import analyze, explore, report, runner
from qa.config import settings
from qa.jobs.queue import ENV_LOCK, JOB_TIMEOUT, redis
from qa.rag import journal

log = logging.getLogger(__name__)


def _callback(payload: dict) -> None:
    if not settings.callback_url:
        log.info("callback_url 미설정 — 결과 전송 생략: job=%s\n%s", payload["job_id"], payload["report"]["text"])
        return
    try:
        httpx.post(settings.callback_url, json=payload, timeout=10).raise_for_status()
    except httpx.HTTPError:
        # 콜백 실패가 검증 결과를 무효로 만들지 않는다 — 결과는 GET /jobs/{id}로 다시 조회할 수 있다.
        log.exception("콜백 전송 실패: job=%s", payload["job_id"])


def run_job(request: dict, front_sha: str, back_sha: str, mode: str = "scenario",
            scenarios: list[str] | None = None) -> dict:
    job = get_current_job()
    payload = {"job_id": job.id, "request": request, "reply_to": request.get("reply_to")}

    with redis().lock(ENV_LOCK, timeout=JOB_TIMEOUT, blocking_timeout=JOB_TIMEOUT):
        try:
            if mode == "explore":
                summary = explore.run(request["request"], front_ref=front_sha, back_ref=back_sha, job_id=job.id)
            else:
                summary = runner.run(scenarios or request.get("scenarios") or [], front_ref=front_sha,
                                     back_ref=back_sha, job_id=job.id)
        except Exception as e:
            # 빌드 실패·기동 실패는 시나리오 실패와 구분해 알린다.
            _callback({**payload, "error": f"{type(e).__name__}: {e}", "report": report.build_error(str(e))})
            raise
        # 분석은 테스트 환경을 쓰지 않지만(코드·로그만 읽음) 결과를 한 번에 보내기 위해 락 안에서 끝낸다.
        if analyze.needed(summary):
            summary["analysis"] = analyze.run(summary)

    built = report.build(summary)
    _callback({**payload, "summary": summary, "report": built})
    # 회신이 먼저다 — 리포트 기록·재인덱싱(임베딩)은 요청자를 기다리게 하지 않는다.
    try:
        summary["journal"] = str(journal.write(summary, built["text"], request))
    except Exception:
        log.exception("QA 리포트 기록 실패: job=%s", job.id)
    return summary
