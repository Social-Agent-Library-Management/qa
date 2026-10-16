---
type: "이력"
repo: "backend"
kind: "pr"
number: 5
change: "feat"
issues: [2]
state: "MERGED"
merged_at: "2026-08-06T07:17:23Z"
branch: "feat/#2"
files: ["src/main/kotlin/org/library/book/domain/Book.kt", "src/main/kotlin/org/library/book/domain/BookRepository.kt"]
---
# backend PR #5 feat(#2): 도서 엔티티 및 Repository 추가

## 증상·요구 (연결 이슈)
### 이슈 #2 도서 도메인 구축
## 연관 이슈
- Epic: #1

## 구현 계획
- `Book` 엔티티, `BookRepository` 구현
- 응답 DTO는 첫 사용처가 생기는 #3에서 추가


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #2

## 작업 사항
- `Book` 엔티티 추가
    - ISBN은 미입력을 허용하므로 nullable(`String?`)

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- 

## 변경 파일
- `src/main/kotlin/org/library/book/domain/Book.kt` (+37/-0)
- `src/main/kotlin/org/library/book/domain/BookRepository.kt` (+6/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/5
