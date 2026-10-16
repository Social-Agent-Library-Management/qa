---
type: "이력"
repo: "backend"
kind: "pr"
number: 7
change: "feat"
issues: [4]
state: "MERGED"
merged_at: "2026-08-07T07:17:25Z"
branch: "feat/#4"
files: ["src/main/kotlin/org/library/book/application/SearchBooksService.kt", "src/main/kotlin/org/library/book/application/port/BookDocument.kt", "src/main/kotlin/org/library/book/application/port/BookSearchPort.kt", "src/main/kotlin/org/library/book/controller/BookController.kt", "src/main/kotlin/org/library/book/domain/BookRepository.kt", "src/main/kotlin/org/library/external/search/opensearch/OpenSearchBookSearchAdapter.kt", "src/main/kotlin/org/library/external/search/rdb/RdbBookSearchAdapter.kt"]
---
# backend PR #7 feat(#4): 도서 목록·검색 API 추가

## 증상·요구 (연결 이슈)
### 이슈 #4 도서 목록·검색 API + 검색 포트/어댑터
## 연관 이슈
- Epic: #1
- 선행: #2

## 구현 계획
- `GET /books/search?q=&page=&pageSize=`
    - 검색 조건이 없는 경우 전체 조회 값이 있으면 제목·저자 부분 일치 검색
    - 등록 최신순 고정 정렬 결과 없는 경우 빈 배열로 응답

### 포트/어댑터
- 우아한형제들 [헥사고날 아키텍처 사례](https://techblog.woowahan.com/12720/) 를 참고해 검색 엔진 교체가 가능한 확장 구조로 개발


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #4

## 작업 사항
- `GET /books/search?q=&page=&pageSize=`
    - `q` 가 없거나 공백이면 전체 조회, 값이 있으면 제목·저자 부분 일치 검색
- 포트/어댑터
    - MVP 개발 이후 검색 엔진 교체가 설정 한 줄로 끝나도록 유스케이스,도메인을 엔진에서 격리
    - `search.engine` 값만 바꿔 RDB / OpenSearch를 번갈아 확인할 수 있어 MVP 전후 테스트 가능한 구조로 설계

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- [우아한형제들 헥사고날 아키텍처 사례](https://techblog.woowahan.com/12720/)
    멀티모듈 전면 적용이 아니라 변동성이 큰 검색에만 부분 적용


## 변경 파일
- `src/main/kotlin/org/library/book/application/SearchBooksService.kt` (+28/-0)
- `src/main/kotlin/org/library/book/application/port/BookDocument.kt` (+8/-0)
- `src/main/kotlin/org/library/book/application/port/BookSearchPort.kt` (+9/-0)
- `src/main/kotlin/org/library/book/controller/BookController.kt` (+21/-0)
- `src/main/kotlin/org/library/book/domain/BookRepository.kt` (+16/-0)
- `src/main/kotlin/org/library/external/search/opensearch/OpenSearchBookSearchAdapter.kt` (+19/-0)
- `src/main/kotlin/org/library/external/search/rdb/RdbBookSearchAdapter.kt` (+38/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/7
