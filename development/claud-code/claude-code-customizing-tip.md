# Claude Code 커스터마이징 팁 (검증 기반 정리본)

## 1) 목적과 범위

이 문서는 Claude Code의 커스터마이징 포인트를 실무 관점에서 빠르게 적용할 수 있도록 정리한 가이드다.  
설정 계층, 주요 명령, 팀 공유 방식, 버전 유의사항만 다루며, 모든 항목은 공식 문서 기준으로 정리했다.

## 2) 설정 계층과 파일 위치

Claude Code 설정은 스코프별로 적용된다.

- `Managed`: 조직 정책(사용자/프로젝트 설정보다 우선)
- `User`: `~/.claude/settings.json` (개인 전역)
- `Project`: `.claude/settings.json` (저장소 공유)
- `Local`: `.claude/settings.local.json` (프로젝트 개인 설정, gitignore)

핵심 포인트:

- 팀 공통 정책은 `.claude/settings.json`에 저장한다.
- 개인 실험/개인 취향은 `.claude/settings.local.json`에 저장한다.
- 환경 변수는 `settings.json`의 `env` 필드로 세션 공통 적용 가능하다.

## 3) 커스터마이징 영역별 가이드

### 3.1 터미널/입력

- `/config` 또는 `/theme`로 테마를 조정한다.
- 줄바꿈은 기본적으로 `Ctrl+J`가 동작하며, 일부 터미널에서는 `/terminal-setup`으로 `Shift+Enter`를 설정한다.
- Vim 입력 모드는 `/config -> Editor mode`에서 설정한다. (`/vim` 명령은 최신 버전에서 제거됨)
- 완료 알림은 터미널 지원 기능 또는 `Notification` 훅으로 구성한다.

### 3.2 모델/effort

- 모델 변경: `/model`
- 추론 강도 변경: `/effort` (`low`, `medium`, `high`, `xhigh`, `max`)
- 모델에 따라 지원 가능한 effort 레벨이 다르다.
- `settings.json`의 `model`, `effortLevel`, `availableModels`로 기본 동작을 정책화할 수 있다.

### 3.3 플러그인/마켓플레이스

- 플러그인 관리 시작점: `/plugin`
- 공식 마켓플레이스는 기본 제공되며, 추가 마켓플레이스도 등록 가능하다.
- 설치 스코프는 user/project/local로 분리된다.
- 팀 표준 플러그인은 프로젝트 설정(`.claude/settings.json`)으로 공유한다.

### 3.4 서브에이전트

- 관리 시작점: `/agents`
- 파일 기반 정의 위치:
  - 프로젝트: `.claude/agents/`
  - 사용자 전역: `~/.claude/agents/`
- 에이전트 파일(frontmatter)에서 `name`, `description`, `tools`, `model`, `permissionMode`, `color` 등을 설정할 수 있다.
- 기본 메인 에이전트는 `settings.json`의 `agent` 필드 또는 `--agent` 플래그로 지정 가능하다.

### 3.5 권한/샌드박스

- 권한 관리 시작점: `/permissions`
- 권한 규칙은 `allow`, `ask`, `deny` 기반으로 설정하며 와일드카드 패턴을 지원한다.
- 샌드박스 토글: `/sandbox` (지원 플랫폼에서 사용)
- 샌드박스는 Bash 명령과 자식 프로세스에 대해 파일/네트워크 접근을 OS 레벨로 제한한다.
- 권한 규칙과 샌드박스는 대체 관계가 아니라 보완 관계다.

### 3.6 상태표시줄/키바인딩/훅/출력 스타일

- 상태표시줄: `/statusline` 또는 `settings.json`의 `statusLine`
- 키바인딩: `/keybindings` (`~/.claude/keybindings.json`, 저장 시 자동 반영)
- 훅: `settings.json`의 `hooks` (Notification, PreToolUse, PostToolUse 등 이벤트 기반 자동화)
- 스피너 문구: `spinnerVerbs`, `spinnerTipsOverride`
- 출력 스타일:
  - 선택: `/config -> Output style`
  - 기본 제공: `Default`, `Explanatory`, `Learning`
  - 커스텀 파일: `.claude/output-styles/` 또는 `~/.claude/output-styles/`

## 4) 팀 공유 전략 (실무 권장)

- 프로젝트 공통: `.claude/settings.json` (권한 정책, 팀 플러그인, 훅)
- 개인 취향: `.claude/settings.local.json` (개인 키, 실험 설정, 개인 출력 스타일)
- 에이전트/스타일은 “프로젝트 공용”과 “사용자 전역”을 분리해 운영한다.
- 변경 시 `settings` 스코프 우선순위와 managed 정책 충돌 여부를 먼저 확인한다.

## 5) 버전 유의사항

- `/vim`은 최신 버전에서 제거되었고, Editor mode는 `/config`에서 관리한다.
- effort 레벨 및 모델 관련 옵션은 버전에 따라 기본값/지원 범위가 달라질 수 있다.
- 명령 가용성은 플랫폼/요금제/환경에 따라 일부 차이가 있을 수 있다.

## 6) 검증 링크

- Settings: https://code.claude.com/docs/en/settings.md
- Commands: https://code.claude.com/docs/en/commands.md
- Terminal config: https://code.claude.com/docs/en/terminal-config.md
- Model config: https://code.claude.com/docs/en/model-config.md
- Discover plugins: https://code.claude.com/docs/en/discover-plugins.md
- Sub-agents: https://code.claude.com/docs/en/sub-agents.md
- Permissions: https://code.claude.com/docs/en/permissions.md
- Sandboxing: https://code.claude.com/docs/en/sandboxing.md
- Status line: https://code.claude.com/docs/en/statusline.md
- Keybindings: https://code.claude.com/docs/en/keybindings.md
- Hooks: https://code.claude.com/docs/en/hooks.md
- Output styles: https://code.claude.com/docs/en/output-styles.md
