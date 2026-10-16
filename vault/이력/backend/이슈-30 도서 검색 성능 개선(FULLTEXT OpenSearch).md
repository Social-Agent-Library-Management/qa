---
type: "이력"
repo: "backend"
kind: "issue"
number: 30
change: "기타"
state: "CLOSED"
---
# backend 이슈 #30 도서 검색 성능 개선(FULLTEXT/OpenSearch)

## 배경
- 기존 LKE 검색이 대량 데이터에서 풀스캔 발생
    - 대안 비교 후 적용 (#4에서 검색 포트/어댑터 구조 사용)

## 구현 계획
- MySQL FULLTEXT, OpenSearch 추가
- LIKEFULLTEXT/OpenSearch 성능 비교용 devtools 도구 추가


원본: https://github.com/Social-Agent-Library-Management/backend/issues/30
