---
type: "이력"
repo: "backend"
kind: "pr"
number: 29
change: "feat"
issues: [28]
state: "MERGED"
merged_at: "2026-08-17T03:10:41Z"
branch: "feat/#28"
files: ["src/main/kotlin/org/library/book/application/DeleteBookService.kt", "src/main/kotlin/org/library/bookitem/application/CreateBookItemService.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt"]
---
# backend PR #29 feat(#28): 도서 삭제 시 소장본 cascade soft-delete 처리

## 증상·요구 (연결 이슈)
### 이슈 #28 도서 삭제 시 소장본 cascade soft-delete 처리
## 문제 상황(배경)
> #22(소장본 검색 API) 작업 중 발견
> 
> `DeleteBookService`가 도서를 soft-delete할 때 해당 도서의 소장본(BookItem)에는 아무 처리를 하지 않아 "도서는 삭제됐지만 소장본은 살아있는" 상태가 발생

## 해결 방안(구현 계획)
- `DeleteBookService`: 도서 삭제 시 해당 도서의 소장본 전체를 `softDelete()` cascade 처리
- `BookItemRepository.findByManagementNumberForUpdate`: `bi.deletedAt is null` 조건 추가 (삭제된 소장본으로 대출 생성 방지)
- `BookItemRepository.findByManagementNumber`: `bi.deletedAt is null` 조건 추가 (관리번호 재사용 가능하게)


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #28

## 작업 사항
- `DeleteBookService`: 도서 삭제 시 해당 도서의 소장본 전체를 `softDelete()` cascade 처리

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- PR #17에서 [HIGH] 리뷰 건 해결
- 소장본 삭제(DELETE) API X
    - 소장본의 경우 기획상에 삭제가 존재하지 않고 상태 변경(`PATCH /bookitems/{id}/status`)으로 사용자가 직접 트리거하여 관리만 가능


## 변경 파일
- `src/main/kotlin/org/library/book/application/DeleteBookService.kt` (+3/-0)
- `src/main/kotlin/org/library/bookitem/application/CreateBookItemService.kt` (+1/-1)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+2/-2)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/29
