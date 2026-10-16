---
type: "이력"
repo: "frontend"
kind: "pr"
number: 2
change: "chore"
issues: [1]
state: "MERGED"
merged_at: "2026-08-06T04:45:31Z"
branch: "chore/#1"
files: [".claude/agents/component-architect.md", ".claude/agents/design-interpreter.md", ".claude/agents/frontend-implementer.md", ".claude/agents/qa-inspector.md", ".claude/skills/component-reuse-design/SKILL.md", ".claude/skills/design-spec-extraction/SKILL.md", ".claude/skills/design-to-frontend/SKILL.md", ".claude/skills/frontend-qa-verification/SKILL.md", ".claude/skills/git-pr-workflow/SKILL.md", ".claude/skills/nextjs-implementation/SKILL.md", ".github/ISSUE_TEMPLATE/bug.md", ".github/ISSUE_TEMPLATE/feature.md", ".github/ISSUE_TEMPLATE/infra.md", ".github/ISSUE_TEMPLATE/refactor.md", ".github/ISSUE_TEMPLATE/task.md", ".github/PULL_REQUEST_TEMPLATE.md", "CLAUDE.md", "package-lock.json", "package.json", "src/app/globals.css", "src/components/README.md", "src/components/ui/.gitkeep", "src/lib/utils.ts"]
---
# frontend PR #2 chore(#1): Design→Frontend 하네스 및 커밋/PR 자동화 구축

## 증상·요구 (연결 이슈)
### 이슈 #1 chore: Design→Frontend 하네스 및 커밋/PR 자동화 구축
## 구현 계획
- Claude Design → Next.js 구현 하네스 구성 (에이전트 4 + 스킬 5)
- Next.js 16 / React 19 / Tailwind v4 골대 (`cn()` 유틸, 컴포넌트 2계층 규약)
- Quizly 백엔드 컨벤션 기반 Git/PR 자동화
  - `git-pr-workflow` 스킬 + `.github/` 이슈·PR 템플릿
  - 하네스 사용 시 이슈 → `type/#이슈` 브랜치 → 커밋 → `main` PR 발행 (머지는 사람)
  - 하네스 표기 트레일러(B안) 부착

## 변경 내용 (PR 본문)
## 연관 이슈
- 이 PR이 해결하는 이슈: #1

## 작업 사항
- **하네스 구성**: 에이전트 4(design-interpreter / component-architect / frontend-implementer / qa-inspector) + 스킬 5로 디자인 해석 → 재사용 설계 → 구현 → QA 파이프라인 구성
- **Next.js 골대**: Next.js 16 / React 19 / Tailwind v4(`@theme` 토큰), `cn()` 유틸, `ui/` + `{domain}/` 컴포넌트 2계층 규약
- **Git/PR 자동화** (Quizly 백엔드 컨벤션 기준)
  - `git-pr-workflow` 스킬: 이슈 → `type/#이슈` 브랜치 → `type(#이슈): 설명` 커밋 → `main` PR 발행 (머지는 사람)
  - `.github/` 이슈 템플릿(feature/bug/refactor/infra/task) + PR 템플릿
  - 커밋에 하네스 표기 트레일러(B안: `Generated with … harness` + `Co-Authored-By: Claude`) 부착
  - 오케스트레이터에 Phase 5(Git & PR 발행) 통합

## 테스트
- [x] 타입체크 통과 (`npx tsc --noEmit`)
- [x] 빌드 통과 (`npm run build`, Next.js 16 Turbopack)

## 주의 사항 및 참고사항
- 커밋 트레일러 모델명(`Claude Opus 4.8`)은 실제 사용 모델로 갱신됨
- 이 PR은 하네스 자체를 새 컨벤션대로 발행한 **첫 데모** — 이후 화면/컴포넌트는 요청 시 동일 플로우로 발행됩니다

## 변경 파일
- `.claude/agents/component-architect.md` (+63/-0)
- `.claude/agents/design-interpreter.md` (+52/-0)
- `.claude/agents/frontend-implementer.md` (+58/-0)
- `.claude/agents/qa-inspector.md` (+98/-0)
- `.claude/skills/component-reuse-design/SKILL.md` (+130/-0)
- `.claude/skills/design-spec-extraction/SKILL.md` (+106/-0)
- `.claude/skills/design-to-frontend/SKILL.md` (+152/-0)
- `.claude/skills/frontend-qa-verification/SKILL.md` (+96/-0)
- `.claude/skills/git-pr-workflow/SKILL.md` (+133/-0)
- `.claude/skills/nextjs-implementation/SKILL.md` (+172/-0)
- `.github/ISSUE_TEMPLATE/bug.md` (+12/-0)
- `.github/ISSUE_TEMPLATE/feature.md` (+9/-0)
- `.github/ISSUE_TEMPLATE/infra.md` (+9/-0)
- `.github/ISSUE_TEMPLATE/refactor.md` (+12/-0)
- `.github/ISSUE_TEMPLATE/task.md` (+9/-0)
- `.github/PULL_REQUEST_TEMPLATE.md` (+12/-0)
- `CLAUDE.md` (+21/-0)
- `package-lock.json` (+35/-1)
- `package.json` (+4/-1)
- `src/app/globals.css` (+25/-10)
- `src/components/README.md` (+22/-0)
- `src/components/ui/.gitkeep` (+0/-0)
- `src/lib/utils.ts` (+12/-0)

원본: https://github.com/Social-Agent-Library-Management/frontend/pull/2
