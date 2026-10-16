---
type: "이력"
repo: "backend"
kind: "pr"
number: 48
change: "feat"
issues: [42]
state: "MERGED"
merged_at: "2026-09-08T06:46:39Z"
branch: "feat/#42"
files: ["build.gradle", "mysql/index.sql", "src/main/kotlin/org/library/book/domain/repository/BookRepository.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/core/exception/SystemExceptionHandler.kt", "src/main/kotlin/org/library/excel/application/ImportExcelService.kt", "src/main/kotlin/org/library/excel/controller/ExcelController.kt", "src/main/kotlin/org/library/excel/domain/ExcelImportRowJudgement.kt", "src/main/kotlin/org/library/excel/domain/error/ExcelImportError.kt", "src/main/kotlin/org/library/excel/domain/error/ExcelImportRejectedException.kt", "src/main/kotlin/org/library/excel/dto/ExcelImportRowResult.kt", "src/main/kotlin/org/library/excel/mapping/ExcelColumnMapper.kt", "src/main/kotlin/org/library/excel/reader/ExcelWorkbookReader.kt", "src/main/kotlin/org/library/excel/validation/ExcelImportRowValidator.kt", "src/main/kotlin/org/library/excel/validation/IdentityKeyNormalizer.kt", "src/main/kotlin/org/library/excel/validation/ManagementNumberNormalizer.kt"]
---
# backend PR #48 feat(#42): 엑셀 일괄 등록 API 추가

## 증상·요구 (연결 이슈)
### 이슈 #42 엑셀 일괄 등록 API 추가
## 연관 이슈
- Epic: #41

## 구현 계획
- 오류 행이 하나라도 있으면 전체 등록 실패 (오류 행 목록을 응답으로 반환)


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #42

## 작업 사항
- `POST /imports/excel` 신규 API 추가
      - 엑셀 파일의 모든 시트를 검증 후 도서/소장본으로 일괄 등록오(류 행이 하나라도 있으면 전체 등록 취소)
      - 헤더(도서번호/도서명/출판사명/저자명)를 자동 매핑, 필수 컬럼(도서번호/도서명) 없으면 400
      - 필수값 누락 → 관리번호 형식 오류 → 파일 내 중복 → DB 중복 → 동일 도서(제목+출판사+저자) 매칭 시 소장본만 추가(WARN) → 저자/출판사 공백 순으로 판정
      - 관리번호 형식이 어긋나면 자동 보정하지 않고 ERROR 처리 (사용자가 직접 수정하도록 유도)

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
-  동일 도서 매칭(`identityIndex`)이 매 요청마다 활성 도서 전체를 메모리로 로딩하는 방식이라 도서 수가 늘어날 경우 대응 필요

---
## 코드 리뷰 참고
### 토큰 한도 문제로 CI/CD 자동 코드리뷰 대신 로컬에서 리뷰를 진행
- `[MEDIUM] Book/BookItem이 GenerationType.IDENTITY라 배치 insert 불가 + outbox 이벤트까지 겹쳐 한 트랜잭션 안에서 수천 건 개별 insert`
    → [수정 X] `BaseEntity`가 `GenerationType.IDENTITY`를 쓰는 한 `hibernate.jdbc.batch_size`를 설정해도 배치 `insert`가 구조적으로 적용되지 않아 별도 이슈로 수정

- `[MEDIUM] ExcelController가 outcome is Rejected로 201/409를 직접 분기 `
    → [수정 O] 오류 행이 남아있으면 `ImportExcelService`에서 `ExcelImportRejectedException`을 던지고 `SystemExceptionHandler`에 전용 `@ExceptionHandler`를 추가해 처리


## 변경 파일
- `build.gradle` (+3/-0)
- `mysql/index.sql` (+2/-1)
- `src/main/kotlin/org/library/book/domain/repository/BookRepository.kt` (+10/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+3/-0)
- `src/main/kotlin/org/library/core/exception/SystemExceptionHandler.kt` (+8/-0)
- `src/main/kotlin/org/library/excel/application/ImportExcelService.kt` (+219/-0)
- `src/main/kotlin/org/library/excel/controller/ExcelController.kt` (+35/-0)
- `src/main/kotlin/org/library/excel/domain/ExcelImportRowJudgement.kt` (+18/-0)
- `src/main/kotlin/org/library/excel/domain/error/ExcelImportError.kt` (+18/-0)
- `src/main/kotlin/org/library/excel/domain/error/ExcelImportRejectedException.kt` (+11/-0)
- `src/main/kotlin/org/library/excel/dto/ExcelImportRowResult.kt` (+22/-0)
- `src/main/kotlin/org/library/excel/mapping/ExcelColumnMapper.kt` (+53/-0)
- `src/main/kotlin/org/library/excel/reader/ExcelWorkbookReader.kt` (+79/-0)
- `src/main/kotlin/org/library/excel/validation/ExcelImportRowValidator.kt` (+101/-0)
- `src/main/kotlin/org/library/excel/validation/IdentityKeyNormalizer.kt` (+32/-0)
- `src/main/kotlin/org/library/excel/validation/ManagementNumberNormalizer.kt` (+34/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/48
