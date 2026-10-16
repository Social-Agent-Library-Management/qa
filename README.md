# library-qa

도서관 관리 시스템(프론트엔드·백엔드)을 **사용자 관점에서 풀스택으로 검증**하는 독립 QA 서비스.
구현(AI 하네스)과 검증을 분리하기 위해 대상 레포와 별도로 관리한다.

## 구성
| 구성요소 | 포트 | 비고 |
|---|---|---|
| MySQL (tmpfs) | 3307 | `compose.qa.yml`, 개발용 3306과 분리 |
| OpenSearch (tmpfs) | 9201 | 백엔드 `docker/opensearch` 이미지 재사용 |
| 백엔드 | 8081 | 지정 커밋을 `.work/backend/<sha>` worktree로 빌드 |
| 프론트엔드 | 3001 | 지정 커밋을 `.work/frontend/<sha>` worktree로 `next build` + `next start` |
| Redis (볼륨) | 6380 | 작업 큐(RQ) + 테스트 환경 락. 작업 이력 30일 보관 |
| 작업 API | 8090 | `qa api` (FastAPI) |

백엔드 `application.yml`은 레포에서 gitignore라 커밋 체크아웃에 없다. `QA_BACKEND_DIR`의 로컬 설정을
`--spring.config.location`으로 쓰고, DB·포트·CORS만 환경변수로 QA 값을 덮는다.

## 사용법
```bash
cp .env.example .env          # 대상 레포 경로·JDK 21 경로
uv sync && uv run playwright install chromium
docker compose -f compose.qa.yml up -d --build --wait

uv run qa run loan_return                       # 스택 기동(재사용) → 시드 리셋 → 시나리오 실행
uv run qa run --front-ref main --back-ref dev   # 특정 커밋 검증, 생략 시 HEAD
uv run qa stack down
```

결과는 `artifacts/<run_id>/`에 남는다: `summary.json`, `junit.xml`, `network/*.jsonl`(백엔드 요청·응답),
실패 시 `playwright/**/trace.zip`·스크린샷 (`uv run playwright show-trace <trace.zip>`).

## 작업 API (비동기 실행)
```bash
uv run qa api       # POST /jobs, GET /jobs/{id}
uv run qa worker    # 하나만 띄운다

curl -XPOST localhost:8090/jobs -H 'content-type: application/json' \
  -d '{"source":"api","request":"대출 반납 확인","scenarios":["loan_return"],"front_ref":"main"}'
# → 202 {"job_id", "position", "front_sha", "back_sha"}
curl localhost:8090/jobs/<job_id>   # status · enqueued/started/ended_at · result(summary)
```
- **실행은 한 번에 하나.** 테스트 환경(QA DB·인덱스)이 하나이고 시나리오마다 TRUNCATE하므로,
  큐 하나 + 워커 하나로 순서대로 실행하고 실행 구간을 Redis 락으로 한 번 더 막는다.
- **ref는 접수 시점에 sha로 고정**한다. 대기 중 브랜치가 움직여도 요청한 커밋을 검증한다.
  잘못된 시나리오·ref는 큐에 넣기 전에 400으로 거른다.
- 완료 시 `QA_CALLBACK_URL`(n8n 출구 웹훅)로 `{job_id, request, reply_to, summary | error}`를 보낸다.
  `reply_to`는 엔진이 해석하지 않고 그대로 싣는다 — 채널 지식은 입구·출구(n8n)에만 있다.

## 시드
매 테스트 전 `qa/seed/reset.py`가 테이블을 TRUNCATE하고 `books` 인덱스를 재생성한 뒤
`qa/seed/fixtures.yaml`을 **백엔드 REST API로** 적재한다. 날짜는 실행일 기준 오프셋이라 연체 시드가 날짜와 무관하게 유지된다.

## 시나리오
`scenarios/test_<name>.py`. 테스트 docstring이 시나리오 설명이다(자연어 요청 매핑에 사용 예정).
로케이터는 role·label 기반만 쓴다 — 스타일 변경에는 깨지지 않고 사용자가 보는 문구가 바뀌면 깨진다.
