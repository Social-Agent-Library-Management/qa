---
type: "이력"
repo: "frontend"
kind: "pr"
number: 32
change: "feat"
issues: [31]
state: "MERGED"
merged_at: "2026-09-01T03:44:22Z"
branch: "feat/#31"
files: ["src/app/admin/books/new/page.tsx", "src/app/admin/copies/new/page.tsx", "src/app/admin/data-export/page.tsx", "src/app/admin/excel-import/page.tsx", "src/app/admin/layout.tsx", "src/app/admin/loans/history/page.tsx", "src/app/admin/page.tsx", "src/app/layout.tsx", "src/components/README.md", "src/components/icons/index.tsx", "src/components/library/admin-tabs.tsx", "src/components/library/nav-items.tsx"]
---
# frontend PR #32 feat(#31): 사이드바·관리자 페이지 UI 개편

## 증상·요구 (연결 이슈)
### 이슈 #31 사이드바·관리자 페이지 UI 개편 (관리자 탭 허브 신설)
## 배경
Claude Design "도서 관리 시스템 Design System" > `ui_kits/library/index.html` / `components/navigation/Sidebar.jsx`가 사이드바·관리자 화면 구조를 개편했다.

## 변경 내용
- 사이드바 최상위 nav 7개 → 5개(대시보드/도서 검색/대출 등록/반납 처리/**관리자 페이지**)
- 기존 "도서 등록"·"소장본 등록"·"대출 내역 조회"는 최상위 nav에서 제거, `/admin` 하위 탭 허브로 이동
  - `/books/new` → `/admin/books/new`
  - `/copies/new` → `/admin/copies/new`
  - `/loans/history` → `/admin/loans/history`
- 관리자 탭 허브에 신규 탭 2개(엑셀 일괄 등록/내보내기) 추가 — 백엔드 API 미구현 상태이므로 이번 작업에서는 `PagePlaceholder`로만 반영, 실제 기능 연동은 범위 밖
- 기존 폼/목록 로직, API 연동은 변경 없음(위치 이동만)

## 범위 밖
- 엑셀 일괄 등록/내보내기 실제 기능(업로드·검증·다운로드)

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #31

## 작업 사항
- 사이드바 최상위 nav 7개 → 5개(대시보드/도서 검색/대출 등록/반납 처리/**관리자 페이지**)로 축소, `IconAdmin` 신규 추가
- 관리자 페이지 탭 허브 신설(`AdminTabs`, `src/app/admin/layout.tsx`) — 상단 탭 5개(도서 등록/소장본 등록/대출 내역 조회/엑셀 일괄 등록/내보내기)가 하위 라우트 전환에도 유지됨
- 기존 3개 화면을 라우트만 이동(내용 무변경, `git mv`로 rename 처리): `/books/new`→`/admin/books/new`, `/copies/new`→`/admin/copies/new`, `/loans/history`→`/admin/loans/history`
- `/admin` 루트는 첫 탭(`/admin/books/new`)으로 리다이렉트
- 신규 탭 2개(엑셀 일괄 등록/내보내기)는 백엔드 API 미구현이라 `PagePlaceholder`로만 반영 — 실제 기능(업로드/다운로드) 연동은 이번 범위 밖
- 사이드바 활성 판정은 `resolveActiveNavId`를 그대로 재사용(로직 무변경, 매개변수 타입만 `NavMatchable`로 확장) — `/admin/**` 전체에서 "관리자 페이지"가 정확히 활성화됨을 확인
- `src/components/README.md` 컴포넌트 인벤토리·합성 관계 동기화

## 테스트
- [x] `npx tsc --noEmit`
- [x] `npm run lint`
- [x] `npm run build` (라우트 목록에 `/admin/**` 6개 확인, `/books/new`·`/copies/new`·`/loans/history` 부재(의도된 404) 확인)
- [x] 로컬 실행(`npm run dev`) + 브라우저로 사이드바 5개, 관리자 탭 5개 전환, 플레이스홀더 2종, 구 URL 404 직접 확인

## 주의 사항 및 참고사항
- 기존 URL(`/books/new` 등)에 대한 리다이렉트는 만들지 않았습니다 — 사이드바가 유일한 진입점이라 외부 공유 링크 영향이 없다고 판단했습니다.
- `IconImport`/`IconExport` 아이콘은 추가하지 않았습니다 — 탭 바가 텍스트 전용이라 지금 추가하면 사용처가 없는 코드가 됩니다. 엑셀 일괄 등록/내보내기 기능이 실제로 구현될 때 함께 추가할 것을 권장합니다.
- `IconAdmin` 아이콘은 디자인 원문 SVG 사본이 저장소에 없어 프로젝트의 20px 격자·1.5 stroke 규격으로 재작도했습니다 — 형태(기어) 일치 여부만 확인 부탁드립니다.
- 탭 바 배경은 디자인 원문(`bg-surface` 풀블리드 스트립)과 달리 `border-line` 밑줄만 적용했습니다 — 페이지 여백을 `<main>`이 단일 소유하는 기존 여백 모델과 충돌하지 않도록 한 의도적 편차입니다.

## 변경 파일
- `src/app/admin/books/new/page.tsx` (+0/-0)
- `src/app/admin/copies/new/page.tsx` (+0/-0)
- `src/app/admin/data-export/page.tsx` (+18/-0)
- `src/app/admin/excel-import/page.tsx` (+18/-0)
- `src/app/admin/layout.tsx` (+23/-0)
- `src/app/admin/loans/history/page.tsx` (+0/-0)
- `src/app/admin/page.tsx` (+15/-0)
- `src/app/layout.tsx` (+1/-1)
- `src/components/README.md` (+5/-3)
- `src/components/icons/index.tsx` (+17/-0)
- `src/components/library/admin-tabs.tsx` (+100/-0)
- `src/components/library/nav-items.tsx` (+60/-24)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/32
