---
type: "이력"
repo: "backend"
kind: "pr"
number: 34
change: "feat"
issues: [32]
state: "MERGED"
merged_at: "2026-08-20T16:16:07Z"
branch: "feat/#32"
files: [".gitignore", "build.gradle", "docker-compose.yml", "docker/opensearch/Dockerfile", "opensearch/books_index.json", "src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt", "src/devtools/kotlin/org/library/devtools/db/OpenSearchConfig.kt", "src/devtools/kotlin/org/library/devtools/generator/OpenSearchIndexGenerator.kt", "src/main/kotlin/org/library/adapter/book/search/mysql/MysqlFullTextBookSearchAdapter.kt", "src/main/kotlin/org/library/adapter/book/search/mysql/MysqlLikeBookSearchAdapter.kt", "src/main/kotlin/org/library/adapter/book/search/opensearch/OpenSearchBookSearchAdapter.kt", "src/main/kotlin/org/library/book/application/port/BookDocument.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/core/config/OpenSearchConfig.kt", "src/main/kotlin/org/library/external/search/opensearch/OpenSearchBookSearchAdapter.kt"]
---
# backend PR #34 feat(#32): 도서 검색 opensearch 옵션 추가

## 증상·요구 (연결 이슈)
### 이슈 #32 도서 검색 OpenSearch 옵션 추가
## 연관 이슈
- 선행: #4

## 구현 계획
- book 조회 시 한글 형태소 분석(nori) + fuzzy 매칭이 가능한 OpenSearch 전환 (`search.engine=opensearch`)
- LIKE/FULLTEXT/OpenSearch 성능 비교 비교 후 결과 정리

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #32

## 작업 사항
- `feat(#32): 도서 검색 opensearch 옵션 추가`
    - `OpenSearchBookSearchAdapter`: nori 형태소 분석 + fuzziness 기반 multi_match 검색 추가
    - `search.engine=opensearch`로 활성화 
- `feat(#32): 검색 성능 비교 (opensearch) devtools`
    - `ExplainAnalyzer`: LIKE / FULLTEXT(MySQL) / OpenSearch 실측 응답시간 비교 추가
    - `OpenSearchIndexGenerator`: MySQL book 데이터를 OpenSearch `books` 인덱스로 색인하는 devtool 추가

## 테스트
- [X] 로컬 서버 테스트 완료
- [X] devtools `ExplainAnalyzer` 실행해 LIKE/FULLTEXT/OpenSearch 3-way 비교 확인 ([관련 노션](https://chanyoung-kwon.notion.site/LIKE-MySQL-FULLTEXT-OpenSearch-3bfe5ea23d6b80a18f4fde092eca891f?source=copy_link) - 4장)

## 주의 사항 및 참고사항
- 해당 PR의 OpenSearch로 실행하려면 yml 파일 `search.engine=opensearch` 수정

## 변경 파일
- `.gitignore` (+4/-1)
- `build.gradle` (+1/-0)
- `docker-compose.yml` (+16/-0)
- `docker/opensearch/Dockerfile` (+3/-0)
- `opensearch/books_index.json` (+26/-0)
- `src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt` (+52/-13)
- `src/devtools/kotlin/org/library/devtools/db/OpenSearchConfig.kt` (+18/-0)
- `src/devtools/kotlin/org/library/devtools/generator/OpenSearchIndexGenerator.kt` (+96/-0)
- `src/main/kotlin/org/library/adapter/book/search/mysql/MysqlFullTextBookSearchAdapter.kt` (+4/-17)
- `src/main/kotlin/org/library/adapter/book/search/mysql/MysqlLikeBookSearchAdapter.kt` (+4/-17)
- `src/main/kotlin/org/library/adapter/book/search/opensearch/OpenSearchBookSearchAdapter.kt` (+79/-0)
- `src/main/kotlin/org/library/book/application/port/BookDocument.kt` (+11/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+7/-0)
- `src/main/kotlin/org/library/core/config/OpenSearchConfig.kt` (+20/-0)
- `src/main/kotlin/org/library/external/search/opensearch/OpenSearchBookSearchAdapter.kt` (+0/-19)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/34
