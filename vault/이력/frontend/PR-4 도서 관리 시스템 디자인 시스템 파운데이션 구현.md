---
type: "이력"
repo: "frontend"
kind: "pr"
number: 4
change: "feat"
issues: [3]
state: "MERGED"
merged_at: "2026-08-10T07:10:11Z"
branch: "feat/#3"
files: [".gitignore", "eslint.config.mjs", "src/app/globals.css", "src/app/layout.tsx", "src/app/page.tsx", "src/components/README.md", "src/components/icons/index.tsx", "src/components/library/dday-card.tsx", "src/components/library/nav-items.tsx", "src/components/library/sidebar.tsx", "src/components/library/stat-card.tsx", "src/components/library/status-badge.tsx", "src/components/ui/.gitkeep", "src/components/ui/badge.tsx", "src/components/ui/button.tsx", "src/components/ui/card.tsx", "src/components/ui/data-table.tsx", "src/components/ui/icon-box.tsx", "src/components/ui/input.tsx", "src/components/ui/pagination.tsx", "src/lib/dday.ts", "src/lib/utils.ts"]
---
# frontend PR #4 feat(#3): 도서 관리 시스템 디자인 시스템 파운데이션 구현

## 증상·요구 (연결 이슈)
### 이슈 #3 도서 관리 시스템 디자인 시스템 구현 (토큰 + 8개 재사용 컴포넌트)
## 배경
Claude Design 프로젝트 "도서 관리 시스템 Design System"(https://claude.ai/design/p/307f4357-35a5-463d-9674-9b2fefff09fa)을 DesignSync로 읽어와, 디자인 시스템 파운데이션을 Next.js + Tailwind v4 코드로 구현한다.

## 범위
- 디자인 토큰: colors / typography / spacing / radius / shadows → `globals.css` `@theme`
- 재사용 컴포넌트 8종:
  - core: Button, Badge, Input, Card
  - display: StatCard, DdayCard
  - data: DataTable (정렬/페이지네이션 없는 기본형 → prompt 스펙대로 pageSize 지원)
  - navigation: Sidebar (7개 nav 아이템 + 아이콘 세트)
- `src/components/README.md` 컴포넌트 인벤토리 갱신

## 범위 밖 (후속 이슈)
- 8개 화면(로그인/대시보드/도서 등록/소장본 등록/대출 등록/반납 처리/대출 내역 조회/연체 목록) 페이지 구현

## 완료 조건
- [ ] 토큰이 `globals.css`에 반영되고 컴포넌트가 하드코딩 없이 토큰만 사용
- [ ] 8개 컴포넌트가 cva variant + `cn()` 패턴으로 TS 구현
- [ ] `tsc`/`next build` 통과
- [ ] README 컴포넌트 인벤토리 갱신

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #3

## 작업 사항
- Claude Design 프로젝트("도서 관리 시스템 Design System", DesignSync로 조회)의 디자인 토큰(색상/타이포/스페이싱/반경/그림자)을 `src/app/globals.css`의 `@theme`에 반영
- 재사용 컴포넌트 8종 구현 (`class-variance-authority` + `cn()` 기반)
  - core: `Button`, `Badge`, `Input`, `Card`
  - display: `StatCard`, `DdayCard`
  - data: `DataTable` (+ `Pagination` 독립 프리미티브로 승격)
  - navigation: `Sidebar` (7개 nav 아이템 + 아이콘 세트)
  - 공용: `IconBox` (StatCard/DdayCard/로고/아바타 4곳의 "컬러 배경+중앙 아이콘" 패턴 통합)
- 원본 디자인의 중복 패턴 통합: Badge↔D-day pill 시각 패턴 합성, hover/pressed를 JS state에서 Tailwind CSS 상태 변형(`:hover`/`:active`/`focus-visible`)으로 전환
- `focus-visible` 접근성 스타일 추가 (원본 디자인엔 없던 갭 보완)
- `src/components/README.md` 컴포넌트 인벤토리 갱신
- `src/lib/utils.ts`의 `cn()`에 커스텀 `@theme` 토큰(rounded/font-size/leading/shadow/spacing)을 `tailwind-merge`에 등록해 클래스 병합 정확성 확보

## 범위 밖 (후속 이슈)
- 8개 화면(로그인/대시보드/도서 등록/소장본 등록/대출 등록/반납 처리/대출 내역 조회/연체 목록) 페이지 구현

## 테스트
- [x] 타입체크 통과 (`npx tsc --noEmit`)
- [x] 빌드 통과 (`npm run build`)
- [x] 린트 통과 (`npm run lint`)
- [ ] 로컬 실행 확인 (`npm run dev`) — 화면이 없어 별도 렌더 검증은 후속 이슈에서 진행

## 주의 사항 및 참고사항
- 원본 디자인 소스(readme.md)와 실제 코드(.jsx/.d.ts) 간 서술 불일치 발견 — 코드를 신뢰 소스로 채택함:
  - Badge 상태: readme는 5종 서술하나 코드는 7종(`lost`, `disposed` 포함) — 7종 그대로 구현
  - Sidebar 7번째 nav 아이템: readme는 "알림(bell)"이라 서술하나 코드는 "연체 목록"(`overdue`) — 코드대로 구현
- D-day 카운트 pill을 Badge `lg` 사이즈로 정규화하면서 원본 대비 높이 +3px 차이 발생 (일관성 우선 판단)
- 반응형 브레이크포인트는 원본 디자인에 정의가 없어 데스크톱 전용으로 구현 — 최소 지원 해상도 확인 필요
- `_workspace/`는 이번 파이프라인 산출물(디자인 스펙·설계·구현·QA 리포트)이며 `.gitignore`에 추가해 커밋 대상에서 제외함

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## 변경 파일
- `.gitignore` (+3/-0)
- `eslint.config.mjs` (+3/-0)
- `src/app/globals.css` (+140/-22)
- `src/app/layout.tsx` (+13/-15)
- `src/app/page.tsx` (+1/-1)
- `src/components/README.md` (+22/-1)
- `src/components/icons/index.tsx` (+138/-0)
- `src/components/library/dday-card.tsx` (+88/-0)
- `src/components/library/nav-items.tsx` (+35/-0)
- `src/components/library/sidebar.tsx` (+168/-0)
- `src/components/library/stat-card.tsx` (+101/-0)
- `src/components/library/status-badge.tsx` (+50/-0)
- `src/components/ui/.gitkeep` (+0/-0)
- `src/components/ui/badge.tsx` (+99/-0)
- `src/components/ui/button.tsx` (+88/-0)
- `src/components/ui/card.tsx` (+89/-0)
- `src/components/ui/data-table.tsx` (+185/-0)
- `src/components/ui/icon-box.tsx` (+56/-0)
- `src/components/ui/input.tsx` (+94/-0)
- `src/components/ui/pagination.tsx` (+152/-0)
- `src/lib/dday.ts` (+33/-0)
- `src/lib/utils.ts` (+27/-1)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/4
