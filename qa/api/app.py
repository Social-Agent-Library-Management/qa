import logging
import subprocess

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from rq.exceptions import NoSuchJobError
from rq.job import Job

from qa import runner
from qa.config import settings
from qa.intent import catalog, claude, mapper
from qa.jobs import tasks
from qa.jobs.models import JobAccepted, JobRejected, JobRequest, JobStatus
from qa.jobs.queue import JOB_TIMEOUT, RESULT_TTL, queue, redis
from qa.stack.checkout import resolve_sha

log = logging.getLogger(__name__)
app = FastAPI(title="library-qa")


def _iso(dt) -> str | None:
    return dt.isoformat(timespec="seconds") if dt else None


def _reject(code: int, message: str) -> JSONResponse:
    # 거절도 사람에게 보여줄 message를 담는다 — 입구(n8n)는 성공·실패 구분 없이 message만 전달하면 된다.
    return JSONResponse(JobRejected(message=message).model_dump(), status_code=code)


@app.get("/health")
def health() -> dict:
    redis().ping()
    return {"status": "ok"}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED, response_model=JobAccepted,
          responses={400: {"model": JobRejected}})
def create_job(req: JobRequest):
    scenarios, reason, front_ref, back_ref = req.scenarios, None, req.front_ref, req.back_ref

    # 시나리오를 명시하지 않으면 자연어로 정한다. 맞는 시나리오가 없으면 AI 탐색으로 검증한다.
    if scenarios is None and req.request.strip():
        try:
            intent = mapper.map_request(req.request)
            scenarios, reason = intent.scenarios, intent.reason
            front_ref, back_ref = front_ref or intent.front_ref, back_ref or intent.back_ref
        except claude.ClaudeError as e:
            log.warning("요청 해석 실패 — AI 탐색으로 진행: %s", e)
            scenarios, reason = [], f"요청 해석에 실패해 AI 탐색으로 진행합니다 ({e})"
    mode = "scenario" if scenarios or not req.request.strip() else "explore"

    try:
        runner.scenario_paths(scenarios or [])
    except FileNotFoundError as e:
        return _reject(400, str(e))
    # ref는 접수 시점에 sha로 고정한다. 대기 중에 main이 움직여도 요청한 그 커밋을 검증한다.
    front_ref, back_ref = front_ref or "HEAD", back_ref or "HEAD"
    try:
        front_sha = resolve_sha(settings.frontend_dir, front_ref)
        back_sha = resolve_sha(settings.backend_dir, back_ref)
    except subprocess.CalledProcessError:
        return _reject(400, f"브랜치·커밋을 찾을 수 없습니다: front `{front_ref}` · back `{back_ref}`")

    q = queue()
    job = q.enqueue(
        tasks.run_job, req.model_dump(), front_sha, back_sha, mode, scenarios,
        job_timeout=JOB_TIMEOUT, result_ttl=RESULT_TTL, failure_ttl=RESULT_TTL,
    )
    position = q.count
    return JobAccepted(
        job_id=job.id, mode=mode, scenarios=scenarios or [], reason=reason, position=position,
        front_sha=front_sha, back_sha=back_sha,
        message=_accepted_message(mode, scenarios or [], reason, position,
                                  f"front `{front_ref}`({front_sha[:7]}) · back `{back_ref}`({back_sha[:7]})"),
    )


def _accepted_message(mode: str, scenarios: list[str], reason: str | None, position: int, target: str) -> str:
    queue_note = "바로 시작합니다" if position <= 1 else f"앞에 {position - 1}건이 있어 순서대로 실행합니다"
    if mode == "explore":
        body = ("등록된 시나리오 중 맞는 것이 없어 *AI가 브라우저로 직접 확인*합니다. (보통 1~3분)\n"
                + (f"> {reason}" if reason else ""))
    else:
        titles = catalog.by_id()
        listed = "\n".join(f"• {titles[s].title}" if s in titles else f"• {s}" for s in scenarios) or "• 전체"
        body = f"*시나리오 테스트*로 확인합니다.\n{listed}" + (f"\n> {reason}" if reason else "")
    return f"🧪 접수했습니다 — {queue_note}.\n{body}\n대상: {target}"


@app.get("/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str) -> JobStatus:
    try:
        job = Job.fetch(job_id, connection=redis())
    except NoSuchJobError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "작업 없음")

    request, front_sha, back_sha, *rest = job.args
    return JobStatus(
        job_id=job.id,
        status=job.get_status(refresh=True).value,
        position=job.get_position(),
        request=JobRequest(**request),
        mode=rest[0] if rest else "scenario",
        front_sha=front_sha,
        back_sha=back_sha,
        enqueued_at=_iso(job.enqueued_at),
        started_at=_iso(job.started_at),
        ended_at=_iso(job.ended_at),
        result=job.return_value(),
        error=(job.latest_result().exc_string if job.is_failed and job.latest_result() else None),
    )


@app.get("/artifacts/{run_id}/{path:path}")
def get_artifact(run_id: str, path: str) -> FileResponse:
    """출구(n8n)가 스크린샷을 내려받아 첨부하는 용도. 산출물 폴더 밖은 열지 않는다."""
    base = settings.artifacts_dir.resolve()
    target = (base / run_id / path).resolve()
    if not target.is_relative_to(base) or not target.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "산출물 없음")
    return FileResponse(target)
