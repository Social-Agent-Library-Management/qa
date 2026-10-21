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
테스트마다 마지막 화면 스크린샷과 녹화 영상(`video.mp4`, AI 탐색은 `video/*.mp4` 1.5배속),
실패 시 `playwright/**/trace.zip` (`uv run playwright show-trace <trace.zip>`).
영상은 Slack 재생용으로 H.264 mp4로 변환한다 — ffmpeg는 `imageio-ffmpeg`에 포함된 바이너리를 쓴다.

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

## Slack 연동 (n8n + ngrok)
```
#qa에서 @Library QA <자연어 요청>
  → ngrok(공개 주소, Slack 입구 경로만 허용) → n8n「QA · Slack 입구」→ POST /jobs → 접수 안내 답글
  → 워커 실행 → QA_CALLBACK_URL → n8n「QA · 결과 출구」→ 결과 답글 + 스크린샷 첨부
```
- **요청 해석**: 맞는 시나리오가 있으면 시나리오 테스트, 없으면 AI 탐색 테스트로 실행한다.
- **n8n에는 로직을 두지 않는다.** 메시지 문구(`report.text`)와 첨부 목록은 QA 서비스가 만들고 n8n은 전달만 한다.
- **공개 범위**: `ngrok/policy.yml`이 Slack 입구 웹훅 경로만 통과시킨다. n8n 편집 화면·출구 웹훅은 로컬 전용.
  입구는 Slack Signing Secret으로 서명을 검증해 위조 요청을 401로 거부한다.

처음 설정:
1. `docker compose -f compose.qa.yml up -d n8n ngrok` → http://localhost:5678 에서 관리자 계정 생성
2. Credentials → Slack API 자격증명 `Slack · Library QA` (Bot token + Signing Secret)
3. `./n8n/import.sh` — 워크플로 등록·게시 (자격증명 ID는 이름으로 찾아 치환)
4. Slack 앱 Event Subscriptions Request URL:
   `https://<QA_PUBLIC_DOMAIN>/webhook/074f0964-db8e-4290-9a75-e558650b96f1/webhook`, bot event `app_mention`

## 시드
매 테스트 전 `qa/seed/reset.py`가 테이블을 TRUNCATE하고 `books` 인덱스를 재생성한 뒤
`qa/seed/fixtures.yaml`을 **백엔드 REST API로** 적재한다. 날짜는 실행일 기준 오프셋이라 연체 시드가 날짜와 무관하게 유지된다.

## 시나리오
`scenarios/test_<name>.py`. 테스트 docstring이 시나리오 설명이다(자연어 요청 매핑에 사용 예정).
로케이터는 role·label 기반만 쓴다 — 스타일 변경에는 깨지지 않고 사용자가 보는 문구가 바뀌면 깨진다.
