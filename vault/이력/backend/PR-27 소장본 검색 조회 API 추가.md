---
type: "이력"
repo: "backend"
kind: "pr"
number: 27
change: "feat"
issues: [22]
state: "MERGED"
merged_at: "2026-08-16T08:21:52Z"
branch: "feat/#22"
files: ["src/main/kotlin/org/library/book/domain/BookRepository.kt", "src/main/kotlin/org/library/bookitem/application/SearchBookItemsService.kt", "src/main/kotlin/org/library/bookitem/controller/BookItemController.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt"]
---
# backend PR #27 feat(#22): 소장본 검색 조회 API 추가

## 증상·요구 (연결 이슈)
### 이슈 #22 소장본 목록 조회 API 구현
## 구현 계획
- 도서의 소장본 목록 조회


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #22

## 작업 사항
- 소장본 검색·목록 조회(`GET /bookitems`)
    - 도서명(`bookTitle`) 부분 일치 검색 (Book과 조인, 삭제된 도서는 제외)
    - 관리번호(`managementNumber`) 부분 일치 검색

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- BookItem에는 도서명 필드가 없어 Book과 JPQL join으로 필터링 (관련 인덱스는 추후 성능 튜닝 시 검토 예정)

## 변경 파일
- `src/main/kotlin/org/library/book/domain/BookRepository.kt` (+10/-0)
- `src/main/kotlin/org/library/bookitem/application/SearchBookItemsService.kt` (+70/-0)
- `src/main/kotlin/org/library/bookitem/controller/BookItemController.kt` (+18/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+16/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/27
