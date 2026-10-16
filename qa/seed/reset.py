"""QA DB와 검색 인덱스를 fixtures.yaml 상태로 되돌린다.

데이터는 SQL로 직접 넣지 않고 백엔드 REST API로 적재한다 — 시드 적재 자체가
등록 API 계약을 한 번 더 통과시키고, 도서 색인도 실제 경로(이벤트 → OpenSearch)로 일어난다.
"""

import json
import time
from datetime import date, timedelta
from pathlib import Path

import httpx
import pymysql
import yaml

from qa.config import settings
from qa.stack import process

FIXTURES = Path(__file__).with_name("fixtures.yaml")
TABLES = ["loan", "book_item", "book", "book_opensearch_outbox"]
INDEX = "books"


def _backend_path() -> Path:
    back = process.load_state().get("backend")
    if not back:
        raise RuntimeError("백엔드가 떠 있지 않다 — `qa stack up` 먼저")
    return settings.work_dir / "backend" / back["sha"][:12]


def _connect():
    return pymysql.connect(
        host=settings.mysql_host, port=settings.mysql_port, user=settings.mysql_user,
        password=settings.mysql_password, database=settings.mysql_db, autocommit=True,
    )


def _index_sql_statements(path: Path) -> list[str]:
    body = "\n".join(line for line in path.read_text().splitlines() if not line.lstrip().startswith("#"))
    return [s.strip() for s in body.split(";") if s.strip()]


def reset_mysql(backend: Path) -> None:
    with _connect() as conn, conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in TABLES:
            cur.execute(f"TRUNCATE TABLE {table}")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        # 스키마는 Hibernate가 만들지만 index.sql(유니크·FULLTEXT)은 수동 적용이 전제다.
        cur.execute("SHOW INDEX FROM book_item WHERE Key_name = 'ux_book_item_management_number'")
        if not cur.fetchall():
            for stmt in _index_sql_statements(backend / "mysql/index.sql"):
                cur.execute(stmt)


def reset_opensearch(backend: Path) -> None:
    # 앱은 인덱스를 만들지 않고 auto_create_index=false다 — 매핑으로 직접 재생성한다.
    mapping = json.loads((backend / "src/main/resources/opensearch/books_index.json").read_text())
    with httpx.Client(base_url=settings.opensearch_url, timeout=10) as os_client:
        os_client.delete(f"/{INDEX}")
        os_client.put(f"/{INDEX}", json=mapping).raise_for_status()


def load_fixtures() -> dict:
    data = yaml.safe_load(FIXTURES.read_text())
    today = date.today()
    with httpx.Client(base_url=settings.backend_url, timeout=10) as api:
        for book in data["books"]:
            res = api.post("/books", json={k: book[k] for k in ("title", "author", "publisher")})
            res.raise_for_status()
            book_id = res.json()["id"]
            for number in book["items"]:
                api.post(f"/books/{book_id}/bookitems", json={"managementNumber": number}).raise_for_status()
        for loan in data["loans"]:
            api.post("/loans", json={
                "managementNumber": loan["management_number"],
                "borrowerName": loan["borrower_name"],
                "department": loan["department"],
                "loanDate": (today + timedelta(days=loan["loan_date_offset_days"])).isoformat(),
            }).raise_for_status()
    return data


def wait_indexed(expected: int, timeout: float = 15) -> None:
    # 색인은 커밋 후 비동기 리스너가 한다 — 검색 화면 시나리오가 빈 결과를 보지 않도록 반영을 기다린다.
    deadline = time.monotonic() + timeout
    with httpx.Client(base_url=settings.opensearch_url, timeout=5) as os_client:
        while time.monotonic() < deadline:
            os_client.post(f"/{INDEX}/_refresh")
            if os_client.get(f"/{INDEX}/_count").json().get("count") == expected:
                return
            time.sleep(0.3)
    raise TimeoutError(f"OpenSearch 색인 반영 대기 시간 초과 (기대 {expected}건)")


def reset() -> dict:
    backend = _backend_path()
    reset_mysql(backend)
    reset_opensearch(backend)
    data = load_fixtures()
    wait_indexed(len(data["books"]))
    return data
