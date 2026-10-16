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

## 시드
매 테스트 전 `qa/seed/reset.py`가 테이블을 TRUNCATE하고 `books` 인덱스를 재생성한 뒤
`qa/seed/fixtures.yaml`을 **백엔드 REST API로** 적재한다. 날짜는 실행일 기준 오프셋이라 연체 시드가 날짜와 무관하게 유지된다.

## 시나리오
`scenarios/test_<name>.py`. 테스트 docstring이 시나리오 설명이다(자연어 요청 매핑에 사용 예정).
로케이터는 role·label 기반만 쓴다 — 스타일 변경에는 깨지지 않고 사용자가 보는 문구가 바뀌면 깨진다.
