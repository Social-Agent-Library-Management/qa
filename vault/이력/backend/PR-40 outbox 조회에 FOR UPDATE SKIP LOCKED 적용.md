---
type: "이력"
repo: "backend"
kind: "pr"
number: 40
change: "refactor"
issues: [39]
state: "MERGED"
merged_at: "2026-08-28T08:27:49Z"
branch: "refactor/#39"
files: ["src/main/kotlin/org/library/book/domain/repository/BookOpenSearchOutboxRepository.kt", "src/main/kotlin/org/library/external/opensearch/sync/BookIndexSynchronizer.kt"]
---
# backend PR #40 refactor(#39): outbox 조회에 FOR UPDATE SKIP LOCKED 적용

## 증상·요구 (연결 이슈)
### 이슈 #39 outbox 동기화 동시성 제어(FOR UPDATE SKIP LOCKED) 적용
## 문제 상황(배경)
> #35에서 outbox 기반 색인 동기화(즉시 동기화 + 스케줄러 재시도) 작업에서 두 경로가 같은 bookId를 동시에 처리하는 상황에 대한 동시성 제어가 없음

## 해결 방안(구현 계획)
- outbox row 조회 시 `FOR UPDATE`로 해당 bookId의 row에  비관적 락(배타적 락)을 걸어 동시 처리를 막음


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #39

## 작업 사항
- `@Lock(PESSIMISTIC_WRITE)` +`jakarta.persistence.lock.timeout=-2`(Hibernate SKIP_LOCKED) 적용
    - 이미 잠긴 row는 다른 워커가 처리 중이라는 뜻이므로 `SKIP LOCKED`를 함께 적용해 락이 즉시 건너뛰도록 제작

## 테스트
- [X] 로컬 서버 테스트 완료
    - 즉시 동기화가 락을 획득 후 5초 동안(테스트 시 `sleep(5)`) 스케줄러가 두 번 폴링해도 `rows=0`으로 반환됨을 로그로 확인 

## 주의 사항 및 참고사항
- 락을 OpenSearch 호출까지 유지하여서 OpenSearch 장애 시 그 시간만큼 DB 커넥션 풀 점유가 길어짐 (현재 배치 규모에서는 허용 가능하다고 판단하여 현재 상태 유지)


## 변경 파일
- `src/main/kotlin/org/library/book/domain/repository/BookOpenSearchOutboxRepository.kt` (+10/-1)
- `src/main/kotlin/org/library/external/opensearch/sync/BookIndexSynchronizer.kt` (+3/-1)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/40
