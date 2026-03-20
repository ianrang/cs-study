# Claude Code 기본 사용법

## 1. 개요

- CLI(터미널) 기반 개발 환경으로, 다양한 IDE 사용 환경에서 공통으로 사용 가능
- Opus 4.6 기준 1M 컨텍스트 윈도우 지원 (Max, Team, Enterprise)

## 2. 요금제 및 사용량

| 플랜 | 모델 | 5시간당 사용량 |
|------|------|----------------|
| Pro ($20/월) | Sonnet 4만 지원 | 약 45 메시지 / 10~40 프롬프트 |
| Max | Opus 포함, 5배 이상 | 사실상 Max 플랜에서 원활한 사용 |

- 리셋: 5시간 롤링 윈도우, 시간(Hour) 단위만 적용
  - 예: 6시 59분 첫 메시지 → 11시 리셋, 7시 1분 첫 메시지 → 12시 리셋
  - 정각 직전 첫 메시지로 리셋 시간을 한 시간 앞당길 수 있음
- 경고: 제한 근접 시 노란색 표시, 2~3 메시지 여유
- 사용량 확인: CCUA (`pnpm dlx ccua usage` 등)로 대략적 누적 사용량 확인 가능 (공식 도구 아님)

## 3. 핵심 기능

### Plan Mode (Shift+Tab)
- 코드를 바로 수정하지 않고 계획을 세우는 모드
- 파일명·변수명을 몰라도 진입점만 알려주면 코드 검색 후 수정 위치 파악
- 계획 없이 수정 시 UI 레이아웃 등 주변 요소가 깨질 수 있으므로 활용 권장

### 터미널
- `!` 접두사로 명령어 즉시 실행 (예: `!ls`)
- 여러 터미널을 열어 동시 작업 가능
- ESC: 진행 중 작업 중단 / ESC 두 번: 이전 응답을 되감기(Rewind/Summarize)

### 편집
- Vim 모드: 0, W, DD 등 제한적 지원

### 이미지 인식
- 드래그앤드롭, 클립보드 붙여넣기(Ctrl+V), 스크린샷 캡처 후 터미널에 붙여넣어 분석 가능

## 4. 명령어

| 명령어 | 용도 |
|--------|------|
| `/init` | 코드베이스 학습 → CLAUDE.md 생성 |
| `/compact` | 불필요한 컨텍스트 제거, 토큰 절약 |
| `/clear` | 컨텍스트 완전 초기화 |
| `/continue` | 최신 대화로 이어서 진행 |
| `/resume` | 이전 대화 기록 중 선택해 복귀 |
| `/memory` | Auto Memory 확인/편집 |
| `/mcp` | MCP 서버 상태 확인 및 인증 관리 |
| `/hooks` | 설정된 hooks 목록 확인 |
| `/model` | LLM 모델 변경 |
| `/config` | 설정 옵션 관리 |
| `#` | 메모 즉시 저장 |

## 5. 실전 활용

### 플랜 모드 활용
- 와이어프레임을 캡처해 첨부
- 수정/삭제/생성될 파일 리스트를 꼼꼼히 확인
- 여러 번 계획을 수정한 뒤 승인(Accept)

### 프롬프팅 팁
- `think hard`, `ultra think` → 신중한 분석·구체적 계획 유도
- `read entire file` → 파일 전체 읽기 요청
- `short` → 짧은 답변 유도

### 캘리브레이션
- one shot, two shot으로 가능 범위를 파악
- 한 번에 완성하기보다 단계적 접근 권장

## 6. 환경 설정

- MCP 연동: `claude mcp add-from-claude-desktop`로 Claude Desktop에 설치된 MCP를 터미널에서 사용

---

고급 기능(Simplify, Batch, Remote Control, Ralph Loop 등)은 [update.md](update.md) 참조.

## 7. 메모리 시스템

| 계층 | 파일 | 역할 | 로딩 |
|------|------|------|------|
| 프로젝트 지침 | `CLAUDE.md` 또는 `.claude/CLAUDE.md` | 프로젝트 구조, 코딩 규칙, 명령어 | 매 세션 자동 로딩 |
| 규칙 파일 | `.claude/rules/*.md` | 주제별 분리된 보조 규칙 | 매 세션 자동 탐색 (path 스코핑 가능) |
| Auto Memory | `~/.claude/projects/<project>/memory/` | 대화 중 Claude가 자동 학습한 내용 | MEMORY.md 첫 200줄 자동 로딩 |
| 세션 이어가기 | `claude -c` 또는 `/resume` | 이전 대화 복원 | 명시적 호출 시 |

- `/memory` 명령으로 Auto Memory 확인/편집 가능
- CLAUDE.md는 200줄 이내 권장, 상세 내용은 `.claude/rules/`나 별도 파일로 분리
