---
type: "이력"
repo: "frontend"
kind: "pr"
number: 46
change: "fix"
issues: [45]
state: "MERGED"
merged_at: "2026-09-14T04:44:15Z"
branch: "fix/#45"
files: ["src/components/README.md", "src/components/library/dashboard-section.tsx", "src/components/library/loan-table.ts", "src/components/library/recent-loans-card.tsx", "src/lib/README.md", "src/lib/api/dashboard.ts", "src/lib/api/loans.ts", "src/lib/relative-time.ts"]
---
# frontend PR #46 fix(#45): 대시보드 최근 활동 API 스펙·디자인 변경 대응

## 증상·요구 (연결 이슈)
### 이슈 #45 fix: 대시보드 최근 활동 API 스펙 변경 및 디자인 변경 대응
## 배경
백엔드 `GET /dashboard/summary` 응답 스펙이 변경되었다(백엔드 커밋 `0b06a42`, feat(NONE): 대시보드 최근 활동 조회로 변경).

- 쿼리 파라미터: `recentLoanLimit` → `recentActivityLimit`
- 응답 필드: `recentLoans: LoanSummary[]` → `recentActivities: LoanActivity[]`
- `LoanActivity`는 대출·반납 활동을 모두 포함하고 `activityAt`(LocalDateTime, 정렬 기준)을 새로 갖는다. 정렬 기준도 대여일(`loanDate`) 내림차순 → 활동 시각(`activityAt`) 내림차순으로 바뀌었다.

디자인(Claude Design `ui_kits/library/index.html`)도 함께 바뀌었다:
- "최근 활동" 표에서 대여일 컬럼 제거
- 활동 시각을 "N분 전"/"N시간 전"/"어제"/"N일 전" 형태의 상대 시간으로 표시(`timeAgo`)
- 카드 제목 "최근 대출 활동" → "최근 활동" (반납 활동도 섞이므로)

## 변경 범위
- `src/lib/api/dashboard.ts`: `recentLoans`/`RECENT_LOAN_LIMIT` → `recentActivities`/새 타입, 쿼리 파라미터명 변경
- `src/components/library/recent-loans-card.tsx`: 대여일 컬럼 제거, 상대 시간 컬럼 추가, 제목·caption 문구 수정
- `src/components/library/loan-table.ts`: 대시보드 컬럼셋을 `LoanActivity` 행 타입에 맞게 조정
- `src/components/library/dashboard-section.tsx`: 응답 필드명 변경 반영
- 상대 시간 포맷 유틸 신규 추가 필요

## 참고
- 디자인: https://claude.ai/design/p/307f4357-35a5-463d-9674-9b2fefff09fa?file=ui_kits%2Flibrary%2Findex.html
- 백엔드: `/Users/chanyoung/Desktop/library` (`RecentLoanActivitiesService.kt`, `GetDashboardSummaryService.kt`, `DashboardController.kt`)

Generated with design-to-frontend harness (Claude Opus 4.8)

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #45

## 문제 상황(배경)
백엔드 `/dashboard/summary`(Kotlin, `RecentLoanActivitiesService` 도입 커밋)가 다음과 같이 바뀌었다.

- 쿼리 파라미터: `recentLoanLimit` → `recentActivityLimit`
- 응답 필드: `recentLoans: LoanSummary[]`(대여일 내림차순, 대출 건만) → `recentActivities: LoanActivity[]`(활동 시각 `activityAt` 내림차순, 대출·반납 모두 포함)

디자인(Claude Design `ui_kits/library/index.html`)도 함께 바뀌어, 대시보드 "최근 활동" 카드에서 대여일 컬럼이 사라지고 활동 시각을 "N분 전"류 상대 시간으로 보여준다. 카드 제목도 "최근 대출 활동" → "최근 활동"으로 바뀐다(반납 활동이 섞이므로).

## 해결 방안(구현 계획)
- `src/lib/api/loans.ts`: 신규 `LoanActivity` 타입 추가(서버 전용 타입, `LoanSummary`에서 파생시키지 않음 — 기존 `OverdueLoanSummary` 선례를 따름)
- `src/lib/api/dashboard.ts`: `recentActivities`/`RECENT_ACTIVITY_LIMIT`/쿼리 키 `recentActivityLimit`로 갱신
- `src/components/library/loan-table.ts`: 대시보드 전용 컬럼만 갈라지는 `ACTIVITY_COLUMN_DEFS` 신설, `DASHBOARD_LOAN_COLUMNS`를 `LoanActivity` 행 타입 기준 5컬럼(도서명·대출자·부서·활동·시간)으로 재구성. 기존 `LOAN_COLUMNS`/`LOAN_HISTORY_COLUMNS`/`loanColumns()`/`toLoanBadgeStatus`는 본문 무변경
- `src/lib/relative-time.ts`(신규): `formatRelativeTime()` — 방금 전/N분 전/N시간 전/어제/N일 전/N주 전/그 이상 날짜 표기. `dday.ts`와 동일한 "순수 함수 + 별도 파일" 패턴
- `src/components/library/recent-loans-card.tsx`: 행 타입 `LoanActivity`로 교체, 카드 제목·caption·emptyText 문구 갱신, 반납 건 배지 라벨을 호출부에서 "반납"으로 오버라이드(다른 화면의 "반납완료" 기본 라벨은 유지), 반납 건 대출자는 기존 `EmptyCell` 패턴 유지(디자인 목업의 단순 "-" 대신)
- `src/components/library/dashboard-section.tsx`: `summary?.recentActivities` 배선 1줄
- `src/components/README.md`, `src/lib/README.md`: 합성 관계·상수명 서술 동기화(신규 재사용 컴포넌트는 없어 인벤토리 표 자체는 변경 없음)

design-to-frontend 하네스(디자인 해석 → 컴포넌트 재사용 설계 → 구현 → QA) 전 과정을 거쳤다. 산출물은 `_workspace/`에 보존.

## 테스트
- [x] 타입체크 통과 (`npx tsc --noEmit`)
- [x] 린트 통과 (`npm run lint`)
- [x] 빌드 통과 (`npm run build`, Next.js 16.2.12/Turbopack)
- [x] QA 에이전트 독립 재검증 PASS(`_workspace/04_qa-report.md`) — 컬럼 폭 합계 100%, 기존 컬럼셋 본문 diff 0줄, `STATUS_MAP` 무변경 등 체크포인트 전항 통과
- [ ] 실제 브라우저 확인 — 로컬 백엔드가 아직 이전 스펙(`recentLoans`)을 내려주는 환경이라면 카드가 빈 상태로 보일 수 있음(백엔드 배포 순서 의존)

## 주의 사항 및 참고사항
- 백엔드가 실제로 `recentActivities`/`activityAt`을 응답하는지는 이 PR 범위에서 런타임 확인하지 않았다(정적 검증만). 백엔드 배포와 순서를 맞춰야 한다.
- `formatRelativeTime`의 "현재 시각" 기준은 렌더 시점 1회 계산이며, 별도 주기 갱신(`setInterval`)은 의도적으로 넣지 않았다(요약 뷰 성격상 과잉 엔지니어링으로 판단).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## 변경 파일
- `src/components/README.md` (+3/-3)
- `src/components/library/dashboard-section.tsx` (+1/-1)
- `src/components/library/loan-table.ts` (+52/-17)
- `src/components/library/recent-loans-card.tsx` (+38/-9)
- `src/lib/README.md` (+4/-3)
- `src/lib/api/dashboard.ts` (+11/-7)
- `src/lib/api/loans.ts` (+40/-0)
- `src/lib/relative-time.ts` (+40/-0)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/46
