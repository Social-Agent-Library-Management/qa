---
type: "이력"
repo: "backend"
kind: "pr"
number: 17
change: "feat"
issues: [15]
state: "MERGED"
merged_at: "2026-08-09T12:38:37Z"
branch: "feat/#15"
files: ["src/main/kotlin/org/library/bookitem/domain/BookItem.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/loan/application/CreateLoanService.kt", "src/main/kotlin/org/library/loan/application/ReturnLoanService.kt", "src/main/kotlin/org/library/loan/application/SearchLoansService.kt", "src/main/kotlin/org/library/loan/controller/LoanController.kt", "src/main/kotlin/org/library/loan/domain/LoanRepository.kt", "src/main/kotlin/org/library/loan/domain/error/LoanError.kt"]
---
# backend PR #17 feat(#15): 대출 등록·반납·검색 API 구현

## 증상·요구 (연결 이슈)
### 이슈 #15 대출 등록·반납·검색 API 구현
## 연관 이슈
- Epic: #13
- 선행: #14

## 구현 계획
- `POST /loans` — 대출 등록
- `POST /loans/{loanId}/return` — 반납 처리 
- `GET /loans` — 대출 내역 검색·목록
    - 도서명,대출자,부서·상태 조합 필터

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #15

## 작업 사항
- `feat(#15): 대출 등록 API 추가`
    - 소장본 조회 시 `@Lock(PESSIMISTIC_WRITE)`로 비관적 락을 걸어 동시에 같은 관리번호로 대출 요청이 들어와도 하나만 성공하도록 처리
- `feat(#15): 반납 처리 API 추가`
- `feat(#15): 대출 내역 검색·목록 API 추가`
    - `bookTitle`/`borrowerName`/`department`는 모두 부분 일치(LIKE) +  전부 AND 조합
    - `loanDate desc` 기본 정렬

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- Loan 검색의 `bookTitle`은 현재 MySQL LIKE 기반으로 Book 검색이 추후 `OpenSearch`로 전환되면 해당 부분도 리펙토링 필요


## 변경 파일
- `src/main/kotlin/org/library/bookitem/domain/BookItem.kt` (+10/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+8/-0)
- `src/main/kotlin/org/library/loan/application/CreateLoanService.kt` (+111/-0)
- `src/main/kotlin/org/library/loan/application/ReturnLoanService.kt` (+75/-0)
- `src/main/kotlin/org/library/loan/application/SearchLoansService.kt` (+80/-0)
- `src/main/kotlin/org/library/loan/controller/LoanController.kt` (+79/-0)
- `src/main/kotlin/org/library/loan/domain/LoanRepository.kt` (+26/-0)
- `src/main/kotlin/org/library/loan/domain/error/LoanError.kt` (+17/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/17
