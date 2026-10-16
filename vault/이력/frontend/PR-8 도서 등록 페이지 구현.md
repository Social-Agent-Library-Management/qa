---
type: "이력"
repo: "frontend"
kind: "pr"
number: 8
change: "feat"
issues: [7]
state: "MERGED"
merged_at: "2026-08-11T06:19:45Z"
branch: "feat/#7"
files: [".env.example", ".gitignore", "src/app/books/new/page.tsx", "src/app/layout.tsx", "src/components/README.md", "src/components/icons/index.tsx", "src/components/library/book-list-card.tsx", "src/components/library/book-register-form.tsx", "src/components/library/book-register-section.tsx", "src/components/ui/data-table.tsx", "src/components/ui/page-header.tsx", "src/components/ui/page-placeholder.tsx", "src/components/ui/toast.tsx", "src/lib/api/books.ts", "src/lib/api/client.ts", "src/lib/utils.ts"]
---
# frontend PR #8 feat(#7): 도서 등록 페이지 구현

## 증상·요구 (연결 이슈)
### 이슈 #7 feat: 도서 등록 페이지 구현
## 배경
디자인 시스템(Claude Design `ui_kits/library/index.html`의 `BookRegistrationScreen`)을 Next.js로 구현한다.

## 범위
- 라우트: `/books/new` (현재 `PagePlaceholder`)
- 새 도서 등록 폼(도서명·저자·ISBN) + 등록된 도서 목록(DataTable)
- API: `POST /books`, `GET /books/search` (백엔드 Kotlin `org.library.book` 도메인 직접 확인)
- 재사용: 기존 `Input`/`Button`/`Card`/`DataTable`/`AppSidebar` 셸 활용

## 참고
- 디자인 목업의 `출판사`/`소장본 수` 필드는 백엔드 API에 없어 제외하고 실제 계약대로 구현한다.

Generated with design-to-frontend harness (Claude Opus 4.8)

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #7

## 작업 사항
- `POST /books` / `GET /books/search` 연동 API 클라이언트 계층 신규 (`src/lib/api/client.ts`, `books.ts`) — 소장본/대출/반납 등 후속 화면도 재사용 가능
- 재사용 프리미티브 신규 추출: `PageHeader`(제목 영역, `PagePlaceholder`도 합성해 중복 제거), `Toast`(성공/실패 알림, tone variant)
- `DataTable`에 `serverPagination`/`loading` 지원 추가 (기존 클라이언트 페이지네이션 `pageSize` 동작은 보존)
- 도서 등록 화면(`/books/new`) 구현: 등록 폼(`BookRegisterForm`) + 목록 카드(`BookListCard`) + 상태 연결(`BookRegisterSection`)
- `Card`/`Input`/`Button`/`Badge`/`DataTable` 등 기존 컴포넌트 전량 재사용, `CountBadge`/`Grid2`/별도 페이지네이션 배선 신규 생성 없음
- `src/components/README.md` 컴포넌트 인벤토리·합성 관계 갱신

## 디자인 ↔ 백엔드 계약 갭
디자인 목업(Claude Design `ui_kits/library/index.html`)의 `출판사`, `소장본 수` 필드/컬럼은 백엔드 `POST /books`·`GET /books/search` 계약(`org.library.book`)에 없어 **제외**하고 구현했습니다. 레이아웃(2열 폼, 카드 2개, 하단 테이블, 토스트)은 유지했습니다.

## 테스트
- [x] 타입체크 통과 (`npx tsc --noEmit`)
- [x] 린트 통과 (`npm run lint`)
- [x] 빌드 통과 (`npm run build`, 8개 라우트 정적 프리렌더)
- [x] 기존 placeholder 6개 화면 회귀 없음 확인 (소스 diff 0, 프리렌더 HTML 대조)
- [x] 브라우저 실제 API 왕복(등록 성공/409 중복/목록 페이지 이동) — 아래 참고 참조, 미검증

## 주의 사항 및 참고사항
- **백엔드 CORS 미설정** — 프론트 dev 서버(다른 origin)에서 `/books` 호출 시 브라우저가 차단합니다. 백엔드에 CORS 허용 설정이 필요합니다(이번 PR 범위 밖).
- 로컬 검증 시 MySQL(3306)이 기동돼 있지 않아 `GET /books/search`가 응답하지 않았습니다(Hikari 커넥션 타임아웃으로 추정) — 코드 결함이 아닌 로컬 환경 문제로 보입니다. 프론트는 이 경우 "서버에 연결할 수 없습니다" + 다시 시도 버튼으로 정상 처리합니다.
- 위 두 가지 때문에 실제 등록/조회 API 왕복은 이 환경에서 end-to-end 검증하지 못했습니다. 타입·빌드·SSR 마크업 수준까지 검증됨.
- 추가한 `@theme` 토큰 없음(기존 토큰으로 전부 표현).

Generated with design-to-frontend harness (Claude Opus 4.8)

## 변경 파일
- `.env.example` (+3/-0)
- `.gitignore` (+2/-0)
- `src/app/books/new/page.tsx` (+13/-2)
- `src/app/layout.tsx` (+6/-1)
- `src/components/README.md` (+16/-3)
- `src/components/icons/index.tsx` (+43/-0)
- `src/components/library/book-list-card.tsx` (+125/-0)
- `src/components/library/book-register-form.tsx` (+155/-0)
- `src/components/library/book-register-section.tsx` (+32/-0)
- `src/components/ui/data-table.tsx` (+51/-8)
- `src/components/ui/page-header.tsx` (+45/-0)
- `src/components/ui/page-placeholder.tsx` (+5/-6)
- `src/components/ui/toast.tsx` (+101/-0)
- `src/lib/api/books.ts` (+66/-0)
- `src/lib/api/client.ts` (+181/-0)
- `src/lib/utils.ts` (+1/-1)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/8
