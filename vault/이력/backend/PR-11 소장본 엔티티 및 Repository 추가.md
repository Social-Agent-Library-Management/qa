---
type: "이력"
repo: "backend"
kind: "pr"
number: 11
change: "feat"
issues: [9]
state: "MERGED"
merged_at: "2026-08-07T07:32:02Z"
branch: "feat/#9"
files: ["src/main/kotlin/org/library/book/domain/BookItem.kt", "src/main/kotlin/org/library/book/domain/BookItemRepository.kt", "src/main/kotlin/org/library/book/domain/BookItemStatus.kt"]
---
# backend PR #11 feat(#9): 소장본 엔티티 및 Repository 추가

## 증상·요구 (연결 이슈)
### 이슈 #9 소장본 엔티티 및 Repository 추가
## 연관 이슈
- Epic: #8 

## 구현 계획
- `BookItem` 엔티티, `BookItemRepository` 구현


## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #9

## 작업 사항
- BookItem 엔티티 추가
    - 관리번호(managementNumber)가 정규표현식(포맷)으로 검증

## 테스트
- [X] 로컬 서버 테스트 완료

## 주의 사항 및 참고사항
- 

## 변경 파일
- `src/main/kotlin/org/library/book/domain/BookItem.kt` (+44/-0)
- `src/main/kotlin/org/library/book/domain/BookItemRepository.kt` (+7/-0)
- `src/main/kotlin/org/library/book/domain/BookItemStatus.kt` (+8/-0)

원본: https://github.com/Social-Agent-Library-Management/backend/pull/11
