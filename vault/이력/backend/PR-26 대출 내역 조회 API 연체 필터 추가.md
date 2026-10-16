---
type: "이력"
repo: "backend"
kind: "pr"
number: 26
change: "feat"
issues: [23]
state: "MERGED"
merged_at: "2026-08-14T03:46:15Z"
branch: "feat/#23"
files: ["src/main/kotlin/org/library/loan/application/SearchLoansService.kt", "src/main/kotlin/org/library/loan/controller/LoanController.kt", "src/main/kotlin/org/library/loan/domain/LoanRepository.kt"]
---
# backend PR #26 feat(#23): 대출 내역 조회 API 연체 필터 추가

## 증상·요구 (연결 이슈)
### 이슈 #23 대출 내역 조회 API 연체 필터 추가
## 구현 계획
- `GET /loans`의 `status` 필터에 연체 추가


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #23

## 작업 사항
- `GET /loans`의 status 필터에 OVERDUE(연체)를 추가
    - DB에 저장되는 LoanStatus(ON_LOAN/RETURNED) 컬럼은 변경하지 않음
        "연체를 status enum에 영속 컬럼으로 추가하면 전이 배치가 없어 데이터 정합성이 깨지기 때문에 저장 상태를 건드리지 않고 조회 시점 계산

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- 기존에 status=ON_LOAN으로 조회하던 페이지에서 연체건은 제외되어서 대응 필요


## 변경 파일
- `src/main/kotlin/org/library/loan/application/SearchLoansService.kt` (+17/-2)
- `src/main/kotlin/org/library/loan/controller/LoanController.kt` (+3/-3)
- `src/main/kotlin/org/library/loan/domain/LoanRepository.kt` (+7/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/26
