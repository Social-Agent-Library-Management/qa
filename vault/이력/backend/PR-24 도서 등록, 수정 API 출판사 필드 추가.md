---
type: "이력"
repo: "backend"
kind: "pr"
number: 24
change: "feat"
issues: [20]
state: "MERGED"
merged_at: "2026-08-14T01:01:57Z"
branch: "feat/#20"
files: ["src/main/kotlin/org/library/book/application/CreateBookService.kt", "src/main/kotlin/org/library/book/application/UpdateBookService.kt", "src/main/kotlin/org/library/book/domain/Book.kt", "src/main/kotlin/org/library/book/dto/BookResponse.kt"]
---
# backend PR #24 feat(#20): 도서 등록, 수정 API 출판사 필드 추가

## 증상·요구 (연결 이슈)
### 이슈 #20 도서 등록, 수정 API 출판사 필드 추가
## 구현 계획
- `Book` 엔티티 `publisher` 필드 추가 및 관련 API 수정


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #20 

## 작업 사항
- Book 엔티티에 publisher(출판사) 필드 추가
    - title/author와 동일하게 필수값

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- `publisher` 필수값이라 프론트 대응 필요

## 변경 파일
- `src/main/kotlin/org/library/book/application/CreateBookService.kt` (+4/-1)
- `src/main/kotlin/org/library/book/application/UpdateBookService.kt` (+4/-1)
- `src/main/kotlin/org/library/book/domain/Book.kt` (+9/-1)
- `src/main/kotlin/org/library/book/dto/BookResponse.kt` (+3/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/24
