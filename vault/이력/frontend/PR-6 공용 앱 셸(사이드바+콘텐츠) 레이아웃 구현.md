---
type: "이력"
repo: "frontend"
kind: "pr"
number: 6
change: "feat"
issues: [5]
state: "MERGED"
merged_at: "2026-08-10T08:07:53Z"
branch: "feat/#5"
files: [".gitignore", "eslint.config.mjs", "src/app/books/new/page.tsx", "src/app/copies/new/page.tsx", "src/app/layout.tsx", "src/app/loans/history/page.tsx", "src/app/loans/new/page.tsx", "src/app/overdue/page.tsx", "src/app/page.tsx", "src/app/returns/page.tsx", "src/components/README.md", "src/components/library/app-sidebar.tsx", "src/components/library/nav-items.tsx", "src/components/ui/page-placeholder.tsx"]
---
# frontend PR #6 feat(#5): 공용 앱 셸(사이드바+콘텐츠) 레이아웃 구현

## 증상·요구 (연결 이슈)
### 이슈 #5 feat: 공용 앱 셸(사이드바+콘텐츠) 레이아웃 구현
## 구현 계획
- 기존 src/components/library/sidebar.tsx의 Sidebar, nav-items.tsx의 LIBRARY_NAV_ITEMS를 그대로 재사용
- src/app/layout.tsx에 Sidebar + 콘텐츠 영역으로 구성된 공용 앱 셸 조립 (모든 화면이 셸 공유, 라우트 그룹 분리 없음)
- 로그인/인증 화면 없음(MVP 범위 밖) — 01-login 제외
- nav-items에 각 화면 라우트(href)를 채우고, 최소 placeholder 페이지(후속 이슈로 실제 콘텐츠 구현) 생성
- usePathname 기반으로 현재 라우트에 맞는 네비 활성 상태(activeId) 계산
- 스코프: 셸/레이아웃 골격 + 네비 활성 상태까지. 각 화면 실제 콘텐츠는 후속 이슈

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #5

## 작업 사항
- `src/app/layout.tsx`에 사이드바+콘텐츠 영역 공용 앱 셸 조립 (모든 화면이 하나의 셸 공유, 라우트 그룹 분리 없음)
- 기존 `Sidebar`(`library/sidebar.tsx`)는 **무수정 재사용** — `LIBRARY_NAV_ITEMS`(id/label/Icon/순서 불변)에 `href`만 채워 라우팅 활성화
- `resolveActiveNavId()`(nav-items.tsx) 순수 함수로 pathname → activeId 매칭(정확 일치 우선, 최장 접두 일치, 루트 `/` 예외 처리)
- `AppSidebar`(신규, library) — `usePathname`을 쓰는 유일한 클라이언트 경계. `Sidebar`는 여전히 라우터에 결합되지 않은 순수 프레젠테이션 컴포넌트로 유지
- `PagePlaceholder`(신규, ui, `Card` 재사용) — 화면 7종 공통 "준비 중" 스텁, 실제 콘텐츠는 후속 이슈
- 라우트 7개 생성: `/`, `/books/new`, `/copies/new`, `/loans/new`, `/returns`, `/loans/history`, `/overdue`
- `src/components/README.md` 컴포넌트 인벤토리·합성 관계 동기화
- (하우스키핑) `_workspace_*/` 아카이브 폴더가 `npm run lint`에 걸리던 문제를 `.gitignore`/`eslint.config.mjs` ignore 패턴 정리로 해결

## 테스트
- [x] 로컬 실행 확인 (`npm run dev`) — 7개 라우트 + 미등록 경로(`/nope`)에서 활성 nav 개수(1개/0개) 및 라벨 실측 확인
- [x] 타입체크 / 빌드 통과 (`npm run build`, `npx tsc --noEmit`)
- [x] `npm run lint` 통과

## 주의 사항 및 참고사항
- 로그인/인증 화면(01-login)은 이번 MVP 범위 밖이라 제외했습니다. `Sidebar`의 `onLogout`을 전달하지 않아 로그아웃 버튼은 렌더되지 않습니다.
- nav 7번째 항목은 기존 코드("연체 목록")를 그대로 유지했습니다 — Claude Design 원본 SVG(`uploads/02-dashboard.svg`)의 마지막 항목은 "알림 설정"으로 표기가 다르지만, 이번 이슈 지시사항("nav-items를 그대로 활용")에 따라 항목 구성은 변경하지 않았습니다. 필요하면 별도 이슈로 논의 부탁드립니다.
- 각 화면의 실제 콘텐츠(통계 카드/폼/테이블 등)는 후속 이슈에서 구현됩니다. 이번 PR은 셸/레이아웃 골격 + 네비 활성 상태까지입니다.
- 반응형 대응은 하지 않았습니다(디자인이 데스크톱 고정폭 기준).
- 신규 디자인 토큰은 없습니다 — 셸에 필요한 값(`--spacing-sidebar`, `--color-canvas`, `--spacing-page-x/y` 등)이 이미 존재했습니다.

## 변경 파일
- `.gitignore` (+1/-0)
- `eslint.config.mjs` (+3/-2)
- `src/app/books/new/page.tsx` (+9/-0)
- `src/app/copies/new/page.tsx` (+9/-0)
- `src/app/layout.tsx` (+21/-2)
- `src/app/loans/history/page.tsx` (+9/-0)
- `src/app/loans/new/page.tsx` (+9/-0)
- `src/app/overdue/page.tsx` (+9/-0)
- `src/app/page.tsx` (+8/-63)
- `src/app/returns/page.tsx` (+9/-0)
- `src/components/README.md` (+8/-0)
- `src/components/library/app-sidebar.tsx` (+31/-0)
- `src/components/library/nav-items.tsx` (+81/-8)
- `src/components/ui/page-placeholder.tsx` (+35/-0)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/6
