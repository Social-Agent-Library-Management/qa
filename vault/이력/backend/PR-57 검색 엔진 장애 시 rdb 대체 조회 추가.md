---
type: "이력"
repo: "backend"
kind: "pr"
number: 57
change: "feat"
issues: [56]
state: "OPEN"
merged_at: null
branch: "feat/#56"
files: ["build.gradle", "src/main/kotlin/org/library/book/adapter/FallbackBookSearchAdapter.kt", "src/main/kotlin/org/library/book/adapter/MysqlLikeBookSearchAdapter.kt", "src/main/kotlin/org/library/book/adapter/OpenSearchBookSearchAdapter.kt"]
---
# backend PR #57 feat(#56): 검색 엔진 장애 시 rdb 대체 조회 추가

## 증상·요구 (연결 이슈)
### 이슈 #56 검색 엔진 장애 시 rdb 대체 조회 추가
## 구현 계획
- OpenSearch(search.engine = opensearch) 장애 시 도서 검색이 실패하지 않도록 RDB(LIKE) 대체 조회 추가


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #56

## 작업 사항
- OpenSearch 검색 실패 시 RDB(LIKE) 대체 조회 (`FallbackBookSearchAdapter`)
- Resilience4j 서킷 브레이커 적용
    - HALF_OPEN 상태에서 허용된 호출(1건)이 끝나지 않아도 30초 뒤 다시 OPEN(차단)으로 전환 

## 테스트
- [X] 로컬 서버 동작 테스트
- [X] 장애 주입 통합 테스트 (로컬 실행)

## 주의 사항 및 참고사항
- `application.yml` 설정값 추가
- 대체 조회 중에는 오타 추천과 관련도 정렬 없이 최신순으로 응답

## 변경 파일
- `build.gradle` (+1/-0)
- `src/main/kotlin/org/library/book/adapter/FallbackBookSearchAdapter.kt` (+86/-0)
- `src/main/kotlin/org/library/book/adapter/MysqlLikeBookSearchAdapter.kt` (+2/-2)
- `src/main/kotlin/org/library/book/adapter/OpenSearchBookSearchAdapter.kt` (+20/-3)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/57
