---
type: "이력"
repo: "backend"
kind: "pr"
number: 25
change: "feat"
issues: [21]
state: "MERGED"
merged_at: "2026-08-14T01:31:18Z"
branch: "feat/#21"
files: ["src/main/kotlin/org/library/book/application/GetBookService.kt", "src/main/kotlin/org/library/book/application/port/BookDocument.kt", "src/main/kotlin/org/library/book/controller/BookController.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/external/search/rdb/RdbBookSearchAdapter.kt"]
---
# backend PR #25 feat(#21): 도서 조회 API 출판사,소장본 추가

## 증상·요구 (연결 이슈)
### 이슈 #21 도서 조회 API 출판사,소장본 수 추가
## 구현 계획
- `GET /books/{id}` 응답(`BookResponse`)에 `publisher`, `bookItemCount` 추가


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #21 

## 작업 사항
- 도서 목록·검색(`GET /books/search`)
    - 응답에 publisher, bookItemCount 추가
    - bookItemCount는 소장본 보유 수량(AVAILABLE+ON_LOAN, LOST+DISPOSED 제외) 기준
- 도서 단건 조회(`GET /books/{id}`)
    - 소장본 상세 목록(bookItems: bookItemId, managementNumber, status, createdAt) 반환
    - 상태 필터링 없이 전체 이력(폐기분 포함) 노출

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- X

## 변경 파일
- `src/main/kotlin/org/library/book/application/GetBookService.kt` (+61/-3)
- `src/main/kotlin/org/library/book/application/port/BookDocument.kt` (+2/-0)
- `src/main/kotlin/org/library/book/controller/BookController.kt` (+2/-2)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+21/-0)
- `src/main/kotlin/org/library/external/search/rdb/RdbBookSearchAdapter.kt` (+14/-2)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/25
