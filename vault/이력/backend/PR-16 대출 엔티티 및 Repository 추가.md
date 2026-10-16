---
type: "이력"
repo: "backend"
kind: "pr"
number: 16
change: "feat"
issues: [14]
state: "MERGED"
merged_at: "2026-08-08T13:27:05Z"
branch: "feat/#14"
files: ["src/main/kotlin/org/library/loan/domain/Loan.kt", "src/main/kotlin/org/library/loan/domain/LoanRepository.kt", "src/main/kotlin/org/library/loan/domain/LoanStatus.kt"]
---
# backend PR #16 feat(#14): 대출 엔티티 및 Repository 추가

## 증상·요구 (연결 이슈)
### 이슈 #14 대출 엔티티 및 Repository 추가
## 연관 이슈
- Epic: #13

## 구현 계획
- `Loan` 엔티티, `LoanRepository` 구현
- 반납 예정일(dueDate) = 대여일 + 14일 자동 계산

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #14

## 작업 사항
- `feat(#14): 대출 엔티티 및 Repository 추가`
    - `dueDate` = 대여일 + 14일 자동 계산
    - `overdueDays`연체 여부는 저장하지 않고 조회 시점에 파생 계산

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
-


## 변경 파일
- `src/main/kotlin/org/library/loan/domain/Loan.kt` (+87/-0)
- `src/main/kotlin/org/library/loan/domain/LoanRepository.kt` (+7/-0)
- `src/main/kotlin/org/library/loan/domain/LoanStatus.kt` (+6/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/16
