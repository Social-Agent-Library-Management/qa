---
type: "이력"
repo: "backend"
kind: "pr"
number: 6
change: "feat"
issues: [3]
state: "MERGED"
merged_at: "2026-08-07T01:38:51Z"
branch: "feat/#3"
files: ["build.gradle", "mysql/index.sql", "src/main/kotlin/org/library/book/application/CreateBookService.kt", "src/main/kotlin/org/library/book/application/DeleteBookService.kt", "src/main/kotlin/org/library/book/application/GetBookService.kt", "src/main/kotlin/org/library/book/application/UpdateBookService.kt", "src/main/kotlin/org/library/book/controller/BookController.kt", "src/main/kotlin/org/library/book/domain/Book.kt", "src/main/kotlin/org/library/book/domain/BookRepository.kt", "src/main/kotlin/org/library/book/domain/error/BookError.kt", "src/main/kotlin/org/library/book/dto/BookResponse.kt", "src/main/kotlin/org/library/core/exception/CommonErrorCode.kt", "src/main/kotlin/org/library/core/exception/SystemExceptionHandler.kt"]
---
# backend PR #6 feat(#3): 도서 CRUD API 구현

## 증상·요구 (연결 이슈)
### 이슈 #3 도서 CRUD API 구현
## 연관 이슈
- Epic: #1
- 선행: #2

## 구현 계획
- `POST /books` — 등록
  - 대량 등록 MVP 기능 구현 이후 개발
  - 공유 응답 DTO(`BookResponse`)를 첫 사용처인 이 시점에 추가

- `GET /books/{id}` — 단건 조회

- `PATCH /books/{id}` — 수정
  - 전체 교체가 아니므로 PUT이 아닌 PATCH

- `DELETE /books/{id}` — 삭제
  - 물리 삭제 대신 소프트 삭제

### ISBN 정책 (기획 확정)
- 빈값 허용 — 미입력 시 `null` 로 저장하며, 미입력 도서는 여러 건 공존 가능
- 값이 있는 경우 활성 도서 중 중복 금지 (409 `DUPLICATE_ISBN`)
- 수정 가능 — `PATCH` 로 변경할 수 있고, 중복 검사에서 자기 자신은 제외


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #3

## 작업 사항
- `feat(#3): 도서 등록 API 추가`
    - ISBN이 있는 경우에만 활성 도서 중 중복을 검사
- `feat(#3): 도서 단건 조회 API 추가`
- `feat(#3): 도서 수정 API 추가`
- `feat(#3): 도서 삭제 API 추가`

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
-

## 변경 파일
- `build.gradle` (+1/-0)
- `mysql/index.sql` (+4/-0)
- `src/main/kotlin/org/library/book/application/CreateBookService.kt` (+42/-0)
- `src/main/kotlin/org/library/book/application/DeleteBookService.kt` (+23/-0)
- `src/main/kotlin/org/library/book/application/GetBookService.kt` (+23/-0)
- `src/main/kotlin/org/library/book/application/UpdateBookService.kt` (+47/-0)
- `src/main/kotlin/org/library/book/controller/BookController.kt` (+81/-0)
- `src/main/kotlin/org/library/book/domain/Book.kt` (+8/-0)
- `src/main/kotlin/org/library/book/domain/BookRepository.kt` (+4/-0)
- `src/main/kotlin/org/library/book/domain/error/BookError.kt` (+15/-0)
- `src/main/kotlin/org/library/book/dto/BookResponse.kt` (+29/-0)
- `src/main/kotlin/org/library/core/exception/CommonErrorCode.kt` (+1/-0)
- `src/main/kotlin/org/library/core/exception/SystemExceptionHandler.kt` (+15/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/6
