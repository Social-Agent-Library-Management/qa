---
type: "이력"
repo: "backend"
kind: "pr"
number: 33
change: "feat"
issues: [31]
state: "MERGED"
merged_at: "2026-08-20T14:25:28Z"
branch: "feat/#31"
files: ["build.gradle", "mysql/index.sql", "src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt", "src/devtools/kotlin/org/library/devtools/db/MysqlConfig.kt", "src/devtools/kotlin/org/library/devtools/generator/MysqlDataGenerator.kt", "src/main/kotlin/org/library/adapter/book/search/mysql/MysqlFullTextBookSearchAdapter.kt", "src/main/kotlin/org/library/adapter/book/search/mysql/MysqlLikeBookSearchAdapter.kt", "src/main/kotlin/org/library/book/domain/BookRepository.kt"]
---
# backend PR #33 feat(#31): 도서 검색 MySQL FULLTEXT 옵션 추가

## 증상·요구 (연결 이슈)
### 이슈 #31 도서 검색 MySQL FULLTEXT 옵션 추가
## 연관 이슈
- 선행: #4

## 구현 계획
- book 조회 시 MATCH AGAINST 기반 네이티브 쿼리 전환 (`search.engine=mysql_fulltext`)
- LIKE vs FULLTEXT 실행계획(EXPLAIN ANALYZE) 비교 후 결과 정리

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #31

## 작업 사항
- `feat(#31): 도서 검색 MySQL FULLTEXT 옵션 추가`
    - `BookRepository.searchFullText()`: MATCH AGAINST 기반 네이티브 쿼리 추가 
    - `search.engine=mysql_fulltext`로 활성화
- `feat(#31): 검색 성능 비교 (FULLTEXT) devtools`
    - `ExplainAnalyzer`(LIKE vs FULLTEXT `EXPLAIN ANALYZE` 비교)
    - 테스트 용 `MysqlDataGenerator`대량 더미데이터 생성 추가

## 테스트
- [X] 로컬 서버 테스트 완료
- [X] devtools `ExplainAnalyzer` 실행해 LIKE vs FULLTEXT 실행계획 비교 확인 ([관련 노션](https://chanyoung-kwon.notion.site/LIKE-MySQL-FULLTEXT-OpenSearch-3bfe5ea23d6b80a18f4fde092eca891f?source=copy_link) - 3장)

## 주의 사항 및 참고사항
- `WITH PARSER ngram` FULLTEXT 인덱스는 `ddl-auto`로 자동 생성 X
    - 테스트 데이터의 경우 `MysqlDataGenerator` 실행 시 함께 생성
    - 실데이터가 있는 경우 `ALTER TABLE book ADD FULLTEXT INDEX idx_book_title_author_ft (title, author) WITH PARSER ngram;` 실행
- 해당 PR에서 작업한 FULLTEXT로 실행하려면 yml 파일 `search.engine=mysql_fulltext` 수정


## 변경 파일
- `build.gradle` (+13/-0)
- `mysql/index.sql` (+4/-0)
- `src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt` (+82/-0)
- `src/devtools/kotlin/org/library/devtools/db/MysqlConfig.kt` (+36/-0)
- `src/devtools/kotlin/org/library/devtools/generator/MysqlDataGenerator.kt` (+306/-0)
- `src/main/kotlin/org/library/adapter/book/search/mysql/MysqlFullTextBookSearchAdapter.kt` (+50/-0)
- `src/main/kotlin/org/library/adapter/book/search/mysql/MysqlLikeBookSearchAdapter.kt` (+3/-3)
- `src/main/kotlin/org/library/book/domain/BookRepository.kt` (+30/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/33
