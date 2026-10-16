"""작업 큐.

테스트 환경(QA DB·검색 인덱스)은 하나이고 시나리오마다 TRUNCATE로 초기화한다.
두 작업이 동시에 돌면 서로의 시드를 지우므로 실행은 반드시 한 번에 하나다.
- 큐 하나 + 워커 하나로 순서대로 꺼내 실행하고,
- 워커를 실수로 여러 개 띄워도 겹치지 않도록 실행 구간을 Redis 락(ENV_LOCK)으로 한 번 더 막는다.
"""

from redis import Redis
from rq import Queue

from qa.config import settings

QUEUE_NAME = "qa"
ENV_LOCK = "qa:test-env-lock"
JOB_TIMEOUT = 30 * 60
RESULT_TTL = 30 * 24 * 3600  # 지표 집계를 위해 결과를 30일 보관


def redis() -> Redis:
    return Redis.from_url(settings.redis_url)


def queue() -> Queue:
    return Queue(QUEUE_NAME, connection=redis())
