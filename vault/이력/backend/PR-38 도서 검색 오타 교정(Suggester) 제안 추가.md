---
type: "이력"
repo: "backend"
kind: "pr"
number: 38
change: "feat"
issues: [37]
state: "MERGED"
merged_at: "2026-08-27T00:03:49Z"
branch: "feat/#37"
files: ["src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt", "src/devtools/kotlin/org/library/devtools/benchmark/KeywordCases.kt", "src/devtools/kotlin/org/library/devtools/benchmark/SuggestAnalyzer.kt", "src/main/kotlin/org/library/book/adapter/MysqlFullTextBookSearchAdapter.kt", "src/main/kotlin/org/library/book/adapter/MysqlLikeBookSearchAdapter.kt", "src/main/kotlin/org/library/book/adapter/OpenSearchBookSearchAdapter.kt", "src/main/kotlin/org/library/book/application/SearchBooksService.kt", "src/main/kotlin/org/library/book/application/port/BookSearchPort.kt", "src/main/kotlin/org/library/external/opensearch/index/BookIndex.kt", "src/main/resources/opensearch/books_index.json"]
---
# backend PR #38 feat(#37): 도서 검색 오타 교정(Suggester) 제안 추가

## 증상·요구 (연결 이슈)
### 이슈 #37 도서 검색 오타 교정(Suggester) 제안 추가
## 연관 이슈
- 선행: #32

## 문제 상황(배경)
- #32에서 OpenSearch(nori) 검색으로 전환하며 `fuzziness: AUTO`로 오타 보정을 시도했지만, 실측 결과 한글 오타에는 동작하지 않음
    - `fuzziness: AUTO`는 토큰 길이로 허용 편집거리를 정하는데 쪼개진 조각이 1~2글자라 애초에 fuzzy 확장이 일어나지 않음
    - 편집거리를 올리면(`fuzziness: 2`) 10만 건 중 8만 건이 걸려서 사용 불가

## 구현 계획
- OpenSearch Phrase Suggester로 오타 교정 후보를 생성 API 적용 예정
- 검색 결과가 0건일 때만 제안을 응답에만 노출


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #37

## 작업 사항
- `feat(#37): 도서 검색에 오타 교정 제안 추가`
    - `BookSearchPort.search()`가 `BookSearchResult(page, suggestion)`을 반환하도록 변경
        - `OpenSearchBookSearchAdapter`: 검색 쿼리와 Phrase Suggester를 한 요청에 반환
        - `SearchBooksService`: 검색 결과가 0건일 때만 `suggestion`을 응답에 노출
    - LIKE/FULLTEXT 어댑터는 오타 교정 후보 (`suggestion`) 항상 null
- `feat(#37): opensearch suggester 오타 교정 devtools 벤치마크 추가`
    - `SuggestAnalyzer`: Phrase Suggester로 한글 오타 교정 후보 생성,채점을 검증하는 devtools 도구 추가

## 테스트
- [X] 로컬 서버 테스트 완료
- [X] devtools `SuggestAnalyzer` 실행해 5개 케이스 오타 교정 결과 확인

## 주의 사항 및 참고사항
- 매핑에 `title.suggest`/`title.trigram` 서브필드가 추가되어 재색인 필요
- [PR 관련 기술 블로그](https://chanyoung-kwon.notion.site/blog-2-suggester-3c8e5ea23d6b80aa96dbe66074bd9bcc?source=copy_link)


## 변경 파일
- `src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt` (+1/-9)
- `src/devtools/kotlin/org/library/devtools/benchmark/KeywordCases.kt` (+16/-0)
- `src/devtools/kotlin/org/library/devtools/benchmark/SuggestAnalyzer.kt` (+151/-0)
- `src/main/kotlin/org/library/book/adapter/MysqlFullTextBookSearchAdapter.kt` (+6/-4)
- `src/main/kotlin/org/library/book/adapter/MysqlLikeBookSearchAdapter.kt` (+6/-4)
- `src/main/kotlin/org/library/book/adapter/OpenSearchBookSearchAdapter.kt` (+38/-3)
- `src/main/kotlin/org/library/book/application/SearchBooksService.kt` (+6/-3)
- `src/main/kotlin/org/library/book/application/port/BookSearchPort.kt` (+6/-1)
- `src/main/kotlin/org/library/external/opensearch/index/BookIndex.kt` (+5/-0)
- `src/main/resources/opensearch/books_index.json` (+25/-1)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/38
