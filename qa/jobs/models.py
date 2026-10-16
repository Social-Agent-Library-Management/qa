from typing import Literal

from pydantic import BaseModel, Field


class JobRequest(BaseModel):
    """채널(Slack·PR·수동)과 무관한 공통 작업 형식. 입구(n8n)가 이 형식으로 변환해 넘긴다."""

    source: Literal["slack", "github_pr", "api"] = "api"
    request: str = Field(default="", description="원문 요청(자연어). 실패 분석·리포트에 그대로 남긴다.")
    front_ref: str = "HEAD"
    back_ref: str = "HEAD"
    scenarios: list[str] | None = Field(default=None, description="생략 시 전체 (3단계부터 자연어로 결정)")
    reply_to: dict | None = Field(default=None, description="결과를 돌려보낼 곳. 엔진은 해석하지 않고 콜백에 그대로 싣는다.")


class JobAccepted(BaseModel):
    job_id: str
    position: int
    front_sha: str
    back_sha: str


class JobStatus(BaseModel):
    job_id: str
    status: str
    position: int | None
    request: JobRequest
    front_sha: str
    back_sha: str
    enqueued_at: str | None
    started_at: str | None
    ended_at: str | None
    result: dict | None
    error: str | None
