import subprocess

from fastapi import FastAPI, HTTPException, status
from rq.exceptions import NoSuchJobError
from rq.job import Job

from qa import runner
from qa.config import settings
from qa.jobs import tasks
from qa.jobs.models import JobAccepted, JobRequest, JobStatus
from qa.jobs.queue import JOB_TIMEOUT, RESULT_TTL, queue, redis
from qa.stack.checkout import resolve_sha

app = FastAPI(title="library-qa")


def _iso(dt) -> str | None:
    return dt.isoformat(timespec="seconds") if dt else None


@app.get("/health")
def health() -> dict:
    redis().ping()
    return {"status": "ok"}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED, response_model=JobAccepted)
def create_job(req: JobRequest) -> JobAccepted:
    # 잘못된 요청은 큐에 넣기 전에 거른다 — 몇 분 기다린 뒤에 실패를 알게 되지 않도록.
    try:
        runner.scenario_paths(req.scenarios or [])
    except FileNotFoundError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    # ref는 접수 시점에 sha로 고정한다. 대기 중에 main이 움직여도 요청한 그 커밋을 검증한다.
    try:
        front_sha = resolve_sha(settings.frontend_dir, req.front_ref)
        back_sha = resolve_sha(settings.backend_dir, req.back_ref)
    except subprocess.CalledProcessError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"알 수 없는 ref: front={req.front_ref} back={req.back_ref}")

    q = queue()
    job = q.enqueue(
        tasks.run_job, req.model_dump(), front_sha, back_sha,
        job_timeout=JOB_TIMEOUT, result_ttl=RESULT_TTL, failure_ttl=RESULT_TTL,
        meta={"front_sha": front_sha, "back_sha": back_sha},
    )
    return JobAccepted(job_id=job.id, position=q.count, front_sha=front_sha, back_sha=back_sha)


@app.get("/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str) -> JobStatus:
    try:
        job = Job.fetch(job_id, connection=redis())
    except NoSuchJobError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "작업 없음")

    request, front_sha, back_sha = job.args
    return JobStatus(
        job_id=job.id,
        status=job.get_status(refresh=True).value,
        position=job.get_position(),
        request=JobRequest(**request),
        front_sha=front_sha,
        back_sha=back_sha,
        enqueued_at=_iso(job.enqueued_at),
        started_at=_iso(job.started_at),
        ended_at=_iso(job.ended_at),
        result=job.return_value(),
        error=(job.latest_result().exc_string if job.is_failed and job.latest_result() else None),
    )
