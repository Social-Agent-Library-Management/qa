---
type: "이력"
repo: "backend"
kind: "pr"
number: 47
change: "feat"
issues: [46]
state: "MERGED"
merged_at: "2026-09-07T08:13:11Z"
branch: "feat/#46"
files: ["build.gradle", "src/main/kotlin/org/library/book/domain/repository/BookRepository.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/core/config/CacheConfig.kt", "src/main/kotlin/org/library/dashboard/application/GetDashboardCountsService.kt", "src/main/kotlin/org/library/dashboard/application/GetDashboardSummaryService.kt", "src/main/kotlin/org/library/dashboard/controller/DashboardController.kt", "src/main/kotlin/org/library/loan/domain/LoanRepository.kt"]
---
# backend PR #47 feat(#46): 대시보드 요약 API 추가

## 증상·요구 (연결 이슈)
### 이슈 #46 대시보드 요약 API 추가
## 구현 계획
- 전체 도서 수, 소장본 수, 대출 가능 수, 대출 중 건수, 연체 건수와 최근 대출·연체 목록을 한 번에 보여주는 요약 API
- 한 요청에서 여러 테이블에 쿼리가 발생하며 대시보드 특성상 초 단위 최신성이 필요 없다고 판단하여 TTL 캐싱 적용 예정


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #46

## 작업 사항
- `GET /dashboard/summary` 신규 API 추가
    - 전체 도서 수, 소장본 수, 대출 가능 소장본 수, 대출 중 건수, 연체 건수를 한 번에 반환
- 요약 조회가 count 4회 + 목록 조회 2회로 쿼리 수가 많은 구조라, Caffeine 기반 캐싱 적용 (`@Cacheable`, `expireAfterWrite` 5분)
    - 대시보드 특성상 초 단위 최신성이 필요 없다고 판단 반복 호출 시 DB 부하 절감 목적

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- 인스턴스가 여러 대로 늘어나면 인스턴스별로 캐시 동기화되지 않음 (현재 단일 인스턴스 배포에서는 문제 없지만 추후 스케일아웃 시 공유 캐시 검토 필요)



## 변경 파일
- `build.gradle` (+2/-0)
- `src/main/kotlin/org/library/book/domain/repository/BookRepository.kt` (+2/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+4/-0)
- `src/main/kotlin/org/library/core/config/CacheConfig.kt` (+28/-0)
- `src/main/kotlin/org/library/dashboard/application/GetDashboardCountsService.kt` (+48/-0)
- `src/main/kotlin/org/library/dashboard/application/GetDashboardSummaryService.kt` (+62/-0)
- `src/main/kotlin/org/library/dashboard/controller/DashboardController.kt` (+30/-0)
- `src/main/kotlin/org/library/loan/domain/LoanRepository.kt` (+5/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/47
