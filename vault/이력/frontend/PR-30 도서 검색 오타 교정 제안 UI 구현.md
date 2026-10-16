---
type: "이력"
repo: "frontend"
kind: "pr"
number: 30
change: "feat"
issues: [29]
state: "MERGED"
merged_at: "2026-08-27T00:04:42Z"
branch: "feat/#29"
files: ["src/components/README.md", "src/components/library/book-search-result-card.tsx", "src/components/library/book-search-section.tsx", "src/components/ui/data-table.tsx", "src/lib/api/books.ts", "src/lib/korean-particle.ts"]
---
# frontend PR #30 feat(#29): 도서 검색 오타 교정 제안 UI 구현

## 증상·요구 (연결 이슈)
### 이슈 #29 feat: 도서 검색 오타 교정 제안 UI 구현
## 배경
백엔드 `GET /books/search`는 검색 결과가 0건일 때 `suggestion`(오타 교정 제안어, 없으면 null) 필드를 함께 내려준다(`SearchBooksService`). OpenSearch 엔진(phrase suggester, max_edits=2)을 쓸 때만 채워지고, MySQL 엔진이거나 적절한 제안이 없으면 항상 null이다 — 프론트는 이 차이를 몰라도 되고 **null이면 아무것도 보여주지 않는다**는 한 가지 규칙만 지키면 된다.

현재 프론트 `BookSearchResult` 타입과 `BookSearchResultCard`에는 이 필드가 전혀 반영되어 있지 않다.

## 작업
- `lib/api/books.ts`의 `BookSearchResult`에 `suggestion: string | null` 추가
- `BookSearchResultCard`: 검색 결과 0건 + `suggestion` 존재 시 디자인(`ui_kits/library/index.html`의 `BookSearchScreen`)대로 '혹시 "OO"(을/를) 찾으셨나요?' 안내 + 재검색 버튼 표시. `suggestion`이 없으면 기존 빈 상태 그대로.
- 재검색 클릭 시 `BookSearchSection`의 검색어를 제안어로 교체

## 참고
- 디자인: Claude Design '도서 관리 시스템 Design System' > ui_kits/library/index.html > BookSearchScreen
- 백엔드: `org.library.book.application.SearchBooksService`, `OpenSearchBookSearchAdapter`

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #29

## 작업 사항
- `lib/api/books.ts`의 `BookSearchResult`에 `suggestion: string | null` 필드 추가 (백엔드 `SearchBooksService.Response.suggestion` 1:1 매핑)
- `ui/data-table.tsx`의 `emptyText` prop 타입을 `string` → `React.ReactNode`로 확대(기존 5개 호출부 무변경, 하위 호환)
- `lib/korean-particle.ts` 신설 — 받침 판정(`hasBatchim`)과 조사 선택(`withEul`=을/를, `withEuro`=으로/로, ㄹ받침 예외 포함) 순수 함수
- `BookSearchResultCard`: 검색 결과 0건 + `suggestion` 있을 때 "혹시 'OO'을 찾으셨나요? [OO(으)로 다시 검색]" 렌더, 없으면 기존 빈 상태 그대로
- `BookSearchSection`: 검색어 교체 로직(`setSearch` + `setSelected(null)`) 중복 제거해 `applySearch(term)`으로 통합, 재검색 버튼과 배선
- `components/README.md`의 `BookSearchResultCard`/`DataTable` 합성 관계 설명 갱신

## 설계 배경
"오타 교정 제한"은 별도 임계값 로직이 아니라, 백엔드 응답의 `suggestion` 필드 유무만으로 판단한다(사용자 확정). OpenSearch를 쓸 때만 채워지고 MySQL이거나 적절한 후보가 없으면 항상 `null`이며, 프론트는 이 차이를 몰라도 되게 설계돼 있다.

design-to-frontend 하네스로 진행: design-interpreter 대체(직접 스펙 작성) → component-architect → frontend-implementer → qa-inspector. `_workspace/01~04` 참고.

## 테스트
- [x] 타입체크 / 빌드 통과 (`npx tsc --noEmit`, `npm run build`, `npm run lint`)
- [x] 로컬 실행 확인 (`npm run dev`) — 브라우저 수동 확인은 아직 안 함. 실제 `suggestion`이 채워지려면 백엔드가 `search.engine=opensearch`로 켜져 있고 결과 0건 + 근접 후보가 있어야 함(로컬 기본은 MySQL이라 늘 null)

## 주의 사항 및 참고사항
- QA에서 발견한 비차단 항목(헬퍼 중복)은 커밋에 반영해 정리함
- 머지는 직접 진행해 주세요

## 변경 파일
- `src/components/README.md` (+4/-3)
- `src/components/library/book-search-result-card.tsx` (+70/-1)
- `src/components/library/book-search-section.tsx` (+10/-8)
- `src/components/ui/data-table.tsx` (+7/-2)
- `src/lib/api/books.ts` (+10/-0)
- `src/lib/korean-particle.ts` (+81/-0)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/30
