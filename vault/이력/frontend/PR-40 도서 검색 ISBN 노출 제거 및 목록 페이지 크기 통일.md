---
type: "이력"
repo: "frontend"
kind: "pr"
number: 40
change: "fix"
issues: [39]
state: "MERGED"
merged_at: "2026-09-08T01:34:20Z"
branch: "fix/#39"
files: ["src/components/README.md", "src/components/library/book-copies-card.tsx", "src/components/library/book-list-card.tsx", "src/components/library/book-register-form.tsx", "src/components/library/book-search-result-card.tsx", "src/components/library/book-table.ts", "src/components/library/copy-list-card.tsx", "src/components/library/loan-list-card.tsx", "src/lib/api/bookitems.ts", "src/lib/api/books.ts", "src/lib/api/loans.ts"]
---
# frontend PR #40 fix(#39): 도서 검색 ISBN 노출 제거 및 목록 페이지 크기 통일

## 증상·요구 (연결 이슈)
### 이슈 #39 fix: 도서 검색 ISBN 노출 제거 및 목록 페이지 크기 통일
## 문제 상황(배경)
- 도서 검색 결과 표에 ISBN 컬럼이 노출되어 있어 제거가 필요하다.
- 도서검색/대출등록/관리자(도서·소장본 등록) 목록은 페이지당 20건 기본값(20)이 아니라 10건으로, 이미 20인 반납처리/대출내역 조회와 기본값이 갈라져 있다.

## 해결 방안(구현 계획)
- `book-table.ts`에 ISBN을 제외한 `BOOK_SEARCH_COLUMNS`를 신설하고 `BookSearchResultCard`가 이를 사용하도록 변경(관리자 도서 목록 `BookListCard`는 ISBN 유지).
- `BookSearchResultCard`/`LoanListCard`/`BookListCard`/`CopyListCard`의 `pageSize` 기본값을 10 → 20으로 통일(이미 20인 `ReturnListCard`/`LoanHistoryCard`와 일치).
- `src/components/README.md` 컴포넌트 인벤토리 갱신.

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #39

## 작업 사항
- 도서 검색 결과 표에서 ISBN 컬럼 제거. 검색 자체는 여전히 ISBN 값을 지원한다(백엔드 `q` 파라미터) — 표시만 뺐다.
- 도서검색/대출등록/관리자(도서·소장본 등록) 목록의 `pageSize` 기본값을 10 → 20으로 통일(이미 20인 반납처리/대출내역 조회와 일치).
- 도서 등록 폼(`/admin/books/new`)에서 ISBN 입력 필드 제거 — 백엔드 `POST /books`는 여전히 선택 필드로 지원하지만 값을 보내지 않는다.
- 등록된 도서 목록(`BookListCard`)에서도 ISBN 컬럼 제거. 도서 검색 결과와 컬럼 집합이 다시 같아져 `book-table.ts`의 컬럼 배열을 `BOOK_COLUMNS` 하나로 통합.
- 도서 상세의 소장본 패널(`BookCopiesCard`)에서도 ISBN 메타 행 제거 — 이제 어느 화면에도 ISBN이 노출되지 않는다.
- 더 이상 트리거될 수 없는 `DUPLICATE_ISBN` 필드 에러 처리, 소비처가 없어진 `formatIsbn` 제거.
- `src/components/README.md` 컴포넌트 인벤토리 갱신.

## 테스트
- [x] 타입체크 통과 (`npx tsc --noEmit`)
- [x] 빌드 통과 (`npm run build`)

## 주의 사항 및 참고사항
- 초기 요청은 "10 → 15"였으나, 반납처리(`ReturnListCard`)·대출내역 조회(`LoanHistoryCard`)가 이미 20 기본값이라는 점을 확인 후 사용자와 협의해 전체를 20으로 통일했다.
- ISBN은 백엔드 `Book` 도메인에서 여전히 선택 필드로 존재한다(응답 타입 `BookListItem.isbn`/`BookDetail.isbn`은 그대로 유지) — 프론트 어디에서도 입력·표시만 하지 않는다.

## 변경 파일
- `src/components/README.md` (+2/-2)
- `src/components/library/book-copies-card.tsx` (+1/-6)
- `src/components/library/book-list-card.tsx` (+3/-8)
- `src/components/library/book-register-form.tsx` (+10/-32)
- `src/components/library/book-search-result-card.tsx` (+4/-5)
- `src/components/library/book-table.ts` (+7/-11)
- `src/components/library/copy-list-card.tsx` (+2/-2)
- `src/components/library/loan-list-card.tsx` (+2/-2)
- `src/lib/api/bookitems.ts` (+1/-1)
- `src/lib/api/books.ts` (+0/-4)
- `src/lib/api/loans.ts` (+1/-1)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/40
