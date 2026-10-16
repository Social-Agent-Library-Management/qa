---
type: "이력"
repo: "frontend"
kind: "pr"
number: 50
change: "fix"
issues: [49]
state: "MERGED"
merged_at: "2026-09-29T01:55:15Z"
branch: "fix/#49"
files: ["src/components/README.md", "src/components/library/book-search-result-card.tsx", "src/components/library/book-search-section.tsx", "src/lib/api/books.ts"]
---
# frontend PR #50 fix(#49): 도서 검색 오타 제안 API 스펙(suggestions 배열) 대응

## 증상·요구 (연결 이슈)
### 이슈 #49 fix: 도서 검색 오타 제안 API 스펙 변경(suggestions 배열) 대응
## 문제 상황(배경)
> 백엔드 `GET /books/search` 응답(`SearchBooksService.Response`)의 오타 교정 필드가 단일 `suggestion: String?`에서 `suggestions: List<String>`(최대 3개, 없으면 빈 배열)으로 변경되었다. 프론트는 단수 필드를 읽고 있어 제안 배너가 뜨지 않는다.

## 해결 방안(구현 계획)
- `lib/api/books.ts`의 `BookSearchResult.suggestion` → `suggestions: string[]`
- `BookSearchResultCard`의 `SuggestionInfo`를 `suggestions` 배열로 전환, 빈 배열이면 배너 미노출
- `BookSearchSection` 배너가 후보 최대 3개를 각각 재검색 버튼으로 렌더(후보별 조사 계산)
- `src/components/README.md` 인벤토리의 단수 `suggestion` 표기 갱신

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #49

## 작업 사항
- `BookSearchResult.suggestion: string | null` → `suggestions: string[]`로 변경 (백엔드 `SearchBooksService.Response` 1:1)
- `BookSearchResultCard`: `SuggestionInfo.suggestions`로 전환, 빈 배열이면 배너 미노출
  - 폴백은 모듈 상수 `NO_SUGGESTIONS`로 두어 참조를 안정화하고(이펙트 재실행 방지), 필드가 없는 구 서버 응답도 방어
- `BookSearchSection`: 배너가 후보(최대 3개)마다 재검색 버튼을 렌더하고, 조사(으로/로)를 후보별로 계산. key에 인덱스를 섞어 중복 후보 대비
- `src/components/README.md` 인벤토리의 단수 `suggestion` 표기를 복수로 갱신

## 테스트
- [x] 로컬 실행 확인 (`npm run dev`)
- [x] 타입체크 / 빌드 통과 (`npm run build`)

## 주의 사항 및 참고사항
- QA(qa-inspector) 1차 FIX 3건(undefined 방어, `[]` 폴백 참조, React key 중복)을 반영했고 재검증 결과 PASS입니다. `tsc`·`lint`(경고 0)·`build` 모두 통과했습니다.
- 실제 백엔드 응답을 붙인 브라우저 확인은 하지 않았습니다.
- 후보 구분자 ` / `는 디자인에 명시되지 않은 임시 표기입니다.
- 워킹트리의 `sidebar.tsx` `prefetch={false}` 변경(#47 관련)은 이 PR에 포함하지 않았습니다.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## 변경 파일
- `src/components/README.md` (+2/-2)
- `src/components/library/book-search-result-card.tsx` (+13/-5)
- `src/components/library/book-search-section.tsx` (+17/-9)
- `src/lib/api/books.ts` (+5/-4)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/50
