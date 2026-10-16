---
type: "이력"
repo: "backend"
kind: "pr"
number: 49
change: "feat"
issues: [43]
state: "MERGED"
merged_at: "2026-09-08T06:56:46Z"
branch: "feat/#43"
files: ["src/main/kotlin/org/library/book/domain/repository/BookRepository.kt", "src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt", "src/main/kotlin/org/library/excel/application/ExportExcelService.kt", "src/main/kotlin/org/library/excel/application/ImportExcelService.kt", "src/main/kotlin/org/library/excel/controller/ExcelController.kt", "src/main/kotlin/org/library/excel/domain/error/ExcelError.kt", "src/main/kotlin/org/library/excel/domain/error/ExcelImportRejectedException.kt", "src/main/kotlin/org/library/excel/writer/ExcelWorkbookWriter.kt", "src/main/kotlin/org/library/loan/domain/LoanRepository.kt"]
---
# backend PR #49 feat(#43): 엑셀 내보내기 API 추가

## 증상·요구 (연결 이슈)
### 이슈 #43 데이터 내보내기 API 추가
## 연관 이슈
- Epic: #41
- 선행: #42

## 구현 계획
- 대용량 데이터도 메모리 문제 없이 처리하도록 스트리밍 방식(SXSSFWorkbook)으로 생성

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #43

## 작업 사항
- `GET /exports/excel` 신규 API 추가
    - 도서/소장본/대여 중 선택한 시트를 정규화된 엑셀 파일로 즉시 생성해 다운로드
- `ExcelWorkbookWriter` 추가 (`SXSSFWorkbook` 기반 스트리밍 방식)

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- 

---
## 코드 리뷰 참고
### 토큰 한도 문제로 CI/CD 자동 코드리뷰 대신 로컬에서 리뷰를 진행
- `[HIGH] 엑셀 셀 값에 사용자 입력을 그대로 기록 → 수식 삽입(Formula/CSV Injection) 위험`
  → [수정 O] 셀 값이 =, +, -, @, 탭, CR로 시작하면 앞에 '를 붙여 텍스트로 강제하는 sanitize()를 writeCell에 추가

- `[MEDIUM] 대용량 데이터 전체를 메모리에 적재`
  → [수정 X] 도서/소장본/대여를 페이지네이션 없이 List로 전체 조회하는 구조라 규모가 커지면 메모리 사용량이 늘어나는데 스트리밍 방식으로의 변경은 후속 이슈 변경 예정

- `[LOW] 날짜 범위 검증이 LOANS 시트 선택 여부와 무관하게 항상 실행됨`
  → [수정 O] `ExcelExportSheetType.LOANS in sheets` 조건을 추가해 LOANS 시트를 선택했을 때만 날짜 범위를 검증하도록 수정

## 변경 파일
- `src/main/kotlin/org/library/book/domain/repository/BookRepository.kt` (+2/-0)
- `src/main/kotlin/org/library/bookitem/domain/BookItemRepository.kt` (+4/-0)
- `src/main/kotlin/org/library/excel/application/ExportExcelService.kt` (+95/-0)
- `src/main/kotlin/org/library/excel/application/ImportExcelService.kt` (+8/-8)
- `src/main/kotlin/org/library/excel/controller/ExcelController.kt` (+37/-2)
- `src/main/kotlin/org/library/excel/domain/error/ExcelError.kt` (+3/-1)
- `src/main/kotlin/org/library/excel/domain/error/ExcelImportRejectedException.kt` (+2/-2)
- `src/main/kotlin/org/library/excel/writer/ExcelWorkbookWriter.kt` (+73/-0)
- `src/main/kotlin/org/library/loan/domain/LoanRepository.kt` (+15/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/49
