---
type: "이력"
repo: "backend"
kind: "pr"
number: 36
change: "feat"
issues: [35]
state: "MERGED"
merged_at: "2026-08-24T04:01:03Z"
branch: "feat/#35"
files: ["docker-compose.yml", "mysql/index.sql", "src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt", "src/devtools/kotlin/org/library/devtools/generator/OpenSearchIndexGenerator.kt", "src/main/kotlin/org/library/book/adapter/MysqlFullTextBookSearchAdapter.kt", "src/main/kotlin/org/library/book/adapter/MysqlLikeBookSearchAdapter.kt", "src/main/kotlin/org/library/book/adapter/OpenSearchBookSearchAdapter.kt", "src/main/kotlin/org/library/book/application/CreateBookService.kt", "src/main/kotlin/org/library/book/application/DeleteBookService.kt", "src/main/kotlin/org/library/book/application/GetBookService.kt", "src/main/kotlin/org/library/book/application/UpdateBookService.kt", "src/main/kotlin/org/library/book/application/event/BookChangedEvent.kt", "src/main/kotlin/org/library/book/application/port/BookDocument.kt", "src/main/kotlin/org/library/book/domain/entity/Book.kt", "src/main/kotlin/org/library/book/domain/entity/BookOpenSearchOutbox.kt", "src/main/kotlin/org/library/book/domain/repository/BookOpenSearchOutboxRepository.kt", "src/main/kotlin/org/library/book/domain/repository/BookRepository.kt", "src/main/kotlin/org/library/book/dto/BookResponse.kt", "src/main/kotlin/org/library/bookitem/application/CreateBookItemService.kt", "src/main/kotlin/org/library/bookitem/application/SearchBookItemsService.kt", "src/main/kotlin/org/library/core/config/AsyncConfig.kt", "src/main/kotlin/org/library/core/config/SchedulingConfig.kt", "src/main/kotlin/org/library/external/opensearch/config/OpenSearchConfig.kt", "src/main/kotlin/org/library/external/opensearch/dto/BookIndexDocument.kt", "src/main/kotlin/org/library/external/opensearch/index/BookIndex.kt", "src/main/kotlin/org/library/external/opensearch/sync/BookIndexSyncListener.kt", "src/main/kotlin/org/library/external/opensearch/sync/BookIndexSynchronizer.kt", "src/main/kotlin/org/library/external/opensearch/sync/BookOpenSearchOutboxScheduler.kt", "src/main/kotlin/org/library/external/opensearch/sync/OpenSearchBookIndexer.kt", "src/main/kotlin/org/library/loan/application/CreateLoanService.kt", "src/main/resources/opensearch/books_index.json"]
---
# backend PR #36 feat(#35): 도서 변경 시 OpenSearch 실시간 동기화

## 증상·요구 (연결 이슈)
### 이슈 #35 도서 변경 시 OpenSearch 실시간 동기화
## 문제 상황(배경)
- #32 에서 `search.engine=opensearch` 로 검색을 전환했지만 읽기 경로만 분리된 상태
    - `CreateBookService`, `UpdateBookService`, `DeleteBookService` RDB만 연결
    - `books` 인덱스를 채우는 경로는 devtools 의 일회성 스크립트(`OpenSearchIndexGenerator`)만 존재
    - 실제 사용 환경에서 MySQL 과 검색 인덱스와 충돌
        - 새로 등록한 도서가 검색되지 않음
        - 수정한 제목,저자가 검색 결과에 반영되지 않음
        - 삭제한 도서가 계속 검색에 노출됨 (결과를 눌러 들어가면 404)

## 구현 계획
- MySQL에서 커밋된 변경만 OpenSearch 에 반영

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #35

## 작업 사항
- `refactor(#35): 검색 어댑터·OpenSearch 연동 패키지 구조 정리`
    - 검색 어댑터 3종을 `book/adapter`로 이동 OpenSearch 연동은 `external/opensearch`로 분리
- `feat(#35): 도서 색인 동기화 기반 구조 추가`
    - `book_opensearch_outbox`: 쓰기 트랜잭션 안에서 색인 대상 기록 → 커밋 후 비동기 색인 → 성공 시 행 삭제
    - `BookOpenSearchOutboxScheduler`: 실패분 재시도 (10초~10분, 10회 초과 시 ERROR 로그)
- `feat(#35): 도서 등록,수정,삭제 시 색인 이벤트 발행`
    - 세 서비스에서 `BookChangedEvent` 발행 

## 테스트
- [X] 로컬 서버 테스트 완료
- [X] 도서 등록·수정·삭제 후 검색 반영 확인
- [X] `search.engine=mysql` 회귀 확인 (OpenSearch 없이 정상 기동)

## 주의 사항 및 참고사항
- 색인이 비동기라 등록 API 응답과 검색 반영 사이에 100ms 안팎의 간격이 있음
- [PR 관련 기술 블로그](https://chanyoung-kwon.notion.site/RDB-OpenSearch-Outbox-3c1e5ea23d6b80139304c2b747dd5adc?source=copy_link)


## 변경 파일
- `docker-compose.yml` (+1/-0)
- `mysql/index.sql` (+5/-0)
- `src/devtools/kotlin/org/library/devtools/benchmark/ExplainAnalyzer.kt` (+1/-1)
- `src/devtools/kotlin/org/library/devtools/generator/OpenSearchIndexGenerator.kt` (+20/-31)
- `src/main/kotlin/org/library/book/adapter/MysqlFullTextBookSearchAdapter.kt` (+2/-2)
- `src/main/kotlin/org/library/book/adapter/MysqlLikeBookSearchAdapter.kt` (+2/-2)
- `src/main/kotlin/org/library/book/adapter/OpenSearchBookSearchAdapter.kt` (+3/-2)
- `src/main/kotlin/org/library/book/application/CreateBookService.kt` (+6/-2)
- `src/main/kotlin/org/library/book/application/DeleteBookService.kt` (+5/-1)
- `src/main/kotlin/org/library/book/application/GetBookService.kt` (+2/-2)
- `src/main/kotlin/org/library/book/application/UpdateBookService.kt` (+6/-2)
- `src/main/kotlin/org/library/book/application/event/BookChangedEvent.kt` (+3/-0)
- `src/main/kotlin/org/library/book/application/port/BookDocument.kt` (+1/-1)
- `src/main/kotlin/org/library/book/domain/entity/Book.kt` (+2/-2)
- `src/main/kotlin/org/library/book/domain/entity/BookOpenSearchOutbox.kt` (+42/-0)
- `src/main/kotlin/org/library/book/domain/repository/BookOpenSearchOutboxRepository.kt` (+13/-0)
- `src/main/kotlin/org/library/book/domain/repository/BookRepository.kt` (+3/-2)
- `src/main/kotlin/org/library/book/dto/BookResponse.kt` (+1/-1)
- `src/main/kotlin/org/library/bookitem/application/CreateBookItemService.kt` (+1/-1)
- `src/main/kotlin/org/library/bookitem/application/SearchBookItemsService.kt` (+1/-1)
- `src/main/kotlin/org/library/core/config/AsyncConfig.kt` (+38/-0)
- `src/main/kotlin/org/library/core/config/SchedulingConfig.kt` (+8/-0)
- `src/main/kotlin/org/library/external/opensearch/config/OpenSearchConfig.kt` (+1/-1)
- `src/main/kotlin/org/library/external/opensearch/dto/BookIndexDocument.kt` (+36/-0)
- `src/main/kotlin/org/library/external/opensearch/index/BookIndex.kt` (+12/-0)
- `src/main/kotlin/org/library/external/opensearch/sync/BookIndexSyncListener.kt` (+35/-0)
- `src/main/kotlin/org/library/external/opensearch/sync/BookIndexSynchronizer.kt` (+71/-0)
- `src/main/kotlin/org/library/external/opensearch/sync/BookOpenSearchOutboxScheduler.kt` (+36/-0)
- `src/main/kotlin/org/library/external/opensearch/sync/OpenSearchBookIndexer.kt` (+57/-0)
- `src/main/kotlin/org/library/loan/application/CreateLoanService.kt` (+1/-1)
- `src/main/resources/opensearch/books_index.json` (+0/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/36
