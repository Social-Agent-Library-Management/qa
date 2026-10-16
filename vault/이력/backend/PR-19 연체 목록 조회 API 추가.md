---
type: "이력"
repo: "backend"
kind: "pr"
number: 19
change: "feat"
issues: [16]
state: "MERGED"
merged_at: "2026-08-09T14:16:06Z"
branch: "feat/#16"
files: ["src/main/kotlin/org/library/loan/application/OverdueLoansService.kt", "src/main/kotlin/org/library/loan/controller/LoanController.kt", "src/main/kotlin/org/library/loan/domain/Loan.kt", "src/main/kotlin/org/library/loan/domain/LoanRepository.kt"]
---
# backend PR #19 feat(#16): 연체 목록 조회 API 추가

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #16

## 작업 사항
- `GET /loans/overdue?department=&page=&size=` 구현
    - 대출 중(`ON_LOAN`)이며 반납 예정일이 지난 대출 건을 연체 경과일 내림차순으로 조회
    - 유예 기간 없이 반납 예정일 익일부터 즉시 연체로 집계 (`dueDate < today`)
    - 정렬은 `dueDate` 오름차순(= 연체 경과일 내림차순과 동치) + `id` 보조 정렬로 동률 시 페이지네이션 순서를 결정론적으로 고정

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- 


## 변경 파일
- `src/main/kotlin/org/library/loan/application/OverdueLoansService.kt` (+68/-0)
- `src/main/kotlin/org/library/loan/controller/LoanController.kt` (+14/-0)
- `src/main/kotlin/org/library/loan/domain/Loan.kt` (+5/-0)
- `src/main/kotlin/org/library/loan/domain/LoanRepository.kt` (+16/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/19
