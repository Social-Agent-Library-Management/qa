---
type: "이력"
repo: "frontend"
kind: "pr"
number: 48
change: "infra"
issues: [47]
state: "MERGED"
merged_at: "2026-09-14T05:34:28Z"
branch: "infra/#47"
files: ["next.config.ts", "public/icon-192.png", "public/icon-512.png", "public/icon.svg", "public/manifest.webmanifest", "src/app/layout.tsx"]
---
# frontend PR #48 infra(#47): 오프라인 배포용 정적 export 빌드 지원

## 증상·요구 (연결 이슈)
### 이슈 #47 infra: 오프라인 배포용 정적 export 빌드 지원
## 구현 계획

인터넷이 없는 윈도우 PC에 배포하기 위해, 프론트엔드를 Node.js 런타임 없이 실행 가능한 정적 파일로 빌드할 수 있게 한다.

- `next.config.ts`에 `OFFLINE_EXPORT` 환경변수 분기 추가
  - `OFFLINE_EXPORT=1` → `output: "export"` + `trailingSlash: true`
  - 미설정 시 기존 동작 그대로 (서버 배포 영향 없음)
- PWA 매니페스트·아이콘 추가
  - 배포 PC에서 Edge 앱 모드(주소창·탭 없는 독립 창)로 띄울 때 이름·아이콘이 제대로 표시되도록

### 배경

이 프로젝트는 API 라우트·미들웨어·동적 세그먼트·서버 사이드 fetch가 없고 데이터 요청이 전부 클라이언트 컴포넌트에서 일어나므로 정적 export가 가능하다. 덕분에 배포 대상 PC에서 Node.js를 통째로 걷어내고, 백엔드 실행용으로 이미 들어가는 JDK의 내장 `jwebserver`로 서빙할 수 있다.

`trailingSlash`는 필수다. `out/books/search/index.html` 구조로 떨어져야 `jwebserver`가 디렉터리 요청을 `index.html`로 해석한다.

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #47

## 작업 사항
- `next.config.ts`에 `OFFLINE_EXPORT` 환경변수 분기 추가
  - `OFFLINE_EXPORT=1` → `output: "export"` + `trailingSlash: true`
  - 미설정 시 기존 서버 빌드 그대로 (동작 변화 없음)
- PWA 매니페스트·아이콘 추가 (`manifest.webmanifest`, `icon-192/512.png`, 원본 `icon.svg`)
- `layout.tsx`에 매니페스트·아이콘 링크 및 `viewport.themeColor` 추가

## 테스트
- [x] 타입체크 / 빌드 통과 (`npm run build`)
- [x] 정적 export 빌드 통과 (`OFFLINE_EXPORT=1 npm run build`)

두 경로를 모두 실행해 확인했습니다.

| 명령 | 산출물 | 결과 |
|---|---|---|
| `npm run build` | `.next/` (out 없음) | 기존 서버 빌드 그대로 |
| `OFFLINE_EXPORT=1 npm run build` | `out/` 259개 파일 5.7MB | 정적 export |

정적 빌드 산출물 검증:
- `out/index.html`, `out/manifest.webmanifest`, `out/icon-192.png` 생성 확인
- `out/books/search/index.html` — `trailingSlash` 구조 확인
- HTML에 `<link rel="manifest">`, `<meta name="theme-color" content="#007aff">` 주입 확인

## 주의 사항 및 참고사항

**왜 정적 export가 가능한가**
API 라우트·미들웨어·동적 세그먼트·서버 사이드 fetch가 없고 데이터 요청이 전부 `"use client"` 컴포넌트에서 일어납니다. 덕분에 배포 대상 PC에서 Node.js 런타임을 걷어내고, 백엔드 실행용으로 이미 포함되는 JDK의 내장 `jwebserver`로 서빙할 수 있습니다.

**`trailingSlash`를 빼면 안 됩니다**
`out/books/search/index.html` 구조로 떨어져야 `jwebserver`가 디렉터리 요청을 `index.html`로 해석합니다. 빼면 하위 페이지가 404가 납니다.

**`themeColor`의 위치**
Next 14부터 `metadata`가 아닌 `viewport`로 분리됐습니다. `metadata`에 두면 빌드 경고가 납니다.

**`NEXT_PUBLIC_API_BASE_URL`은 빌드 시점에 고정됩니다**
정적 export라 런타임에 바꿀 수 없습니다. 현재 기본값 `http://localhost:8080` 기준이며, 다른 주소로 배포하려면 해당 값으로 다시 빌드해야 합니다.

**브라우저 실행 검증 범위**
빌드 산출물의 구조와 주입된 태그는 확인했으나, 배포 대상 윈도우 PC에서의 실제 실행은 이 PR 범위 밖입니다.

**미검증: PWA 설치 동작**
Edge의 "앱으로 설치"가 매니페스트를 읽어 아이콘·이름을 표시하는지는 실제 윈도우 환경에서 확인하지 못했습니다.

## 변경 파일
- `next.config.ts` (+18/-3)
- `public/icon-192.png` (+0/-0)
- `public/icon-512.png` (+0/-0)
- `public/icon.svg` (+35/-0)
- `public/manifest.webmanifest` (+32/-0)
- `src/app/layout.tsx` (+18/-1)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/48
