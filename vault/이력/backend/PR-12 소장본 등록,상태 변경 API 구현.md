---
type: "이력"
repo: "backend"
kind: "pr"
number: 12
change: "feat"
issues: [10]
state: "MERGED"
merged_at: "2026-08-08T12:24:23Z"
branch: "feat/#10"
files: ["mysql/index.sql", "src/main/kotlin/org/library/bookitem/application/ChangeBookItemStatusService.kt", "src/main/kotlin/org/library/bookitem/application/CreateBookItemService.kt", "src/main/kotlin/org/library/bookitem/controller/BookItemController.kt", "src/main/kotlin/org/library/bookitem/domain/BookItem.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/bookitem/domain/error/BookItemError.kt"]
---
# backend PR #12 feat(#10): 소장본 등록,상태 변경 API 구현

## 증상·요구 (연결 이슈)
### 이슈 #10 소장본 등록,상태 변경 API 구현
## 연관 이슈
- Epic: #8
- 선행: #9 

## 구현 계획
- `POST /books/{bookId}/bookitems` — 등록
    - 관리번호는 `(주제)-(번호)` 형식(예: `문학-0001`), 전체 고유
    - 등록 시 상태 기본값 `AVAILABLE`
- `PATCH /bookitems/{bookItemId}/status` — 상태 변경
    - `LOST` 또는 `DISPOSED`로만 변경 가능
    - 물리 삭제 대신 상태 전환으로 이력 보존


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #10 

## 작업 사항
- `feat(#10): 소장본 등록 API 추가`
    - 관리번호는 `(주제)-(번호)` 형식 검증, 전체 고유 여부 검사
- `feat(#10): 소장본 상태 변경 API 추가`
    - `LOST` 또는 `DISPOSED`로만 변경 가능하도록 검증
    - 물리 삭제 대신 상태 전환으로 이력 보존

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- X

## 변경 파일
- `mysql/index.sql` (+5/-0)
- `src/main/kotlin/org/library/bookitem/application/ChangeBookItemStatusService.kt` (+55/-0)
- `src/main/kotlin/org/library/bookitem/application/CreateBookItemService.kt` (+70/-0)
- `src/main/kotlin/org/library/bookitem/controller/BookItemController.kt` (+60/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItem.kt` (+7/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+1/-0)
- `src/main/kotlin/org/library/bookitem/domain/error/BookItemError.kt` (+18/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/12
