# Claude Code 업데이트 요약

> 기준 버전: v2.1.80 (2026-03-19)

---

## 모델 및 컨텍스트

| 모델 | 용도 | 비고 |
|------|------|------|
| Claude Opus 4.6 | 복잡한 추론, 설계, 고급 작업 | Max/Team/Enterprise 기본 모델, 1M 컨텍스트 지원 |
| Claude Sonnet 4.6 | 범용 코딩, 균형 잡힌 성능 | Pro 기본 모델, 1M 컨텍스트 지원 |
| Claude Haiku 4.5 | 빠른 경량 작업, 백그라운드 | hook의 prompt 타입 등에서 사용 |

### Effort Level

모델의 추론 깊이를 조절할 수 있다. `/effort` 명령 또는 `--effort` 플래그로 설정.

| 레벨 | 설명 |
|------|------|
| low | 가장 빠름, 단순 작업 |
| medium | 균형 (Opus 기본값) |
| high | 깊은 추론 |
| max | 최대 추론, 토큰 제한 없음 (Opus 4.6 전용) |

---

## 코어 기능

| 기능 | 명령어 | 목적 |
|------|--------|------|
| Simplify | `/simplify` | 변경된 코드의 재사용성, 품질, 효율성 리뷰 |
| Batch | `/batch` | 5~30개 단위로 분해하여 git worktree 병렬 실행 |
| Loop | `/loop` | 반복 작업 스케줄 (`/loop 5m check deploy`) |
| Remote Control | `/remote-control` | CLI와 claude.ai/code 간 세션 브릿지 |
| Worktree | `--worktree` | 격리된 git worktree에서 작업 |
| Auto Memory | `/memory` | 세션 간 자동 학습 내용 관리 |
| Hooks | `/hooks` | 생명주기 이벤트에 자동화 명령 연결 |
| Agent Teams | 자연어 요청 | 여러 Claude 인스턴스 팀 협업 (experimental) |

---

## 플러그인 기능

코어에 포함되지 않으며, 별도 설치가 필요한 기능.

| 기능 | 플러그인 | 목적 |
|------|----------|------|
| Ralph Loop | `ralph-loop` | 완료 조건 기반 자동 반복 피드백 루프 |
| Superpowers | `superpowers` | Simplify/Batch 확장, 브레인스토밍, 플랜 작성 |
| Code Review | `code-review` | PR 자동 리뷰 |
| Frontend Design | `frontend-design` | UI 컴포넌트 자동 생성 |
| Skill Creator | `skill-creator` | 커스텀 스킬 생성/테스트/벤치마크 |

---

## 최근 주요 변경 사항

### v2.1.80 (2026-03-19)
- Rate Limits 상태 표시 (statusline에 5시간/7일 사용량)
- 인라인 플러그인 선언 (`settings.json`에서 `source: 'settings'`)
- 스킬 effort 프론트매터 지원
- Message Channels (Research Preview): MCP 서버가 세션에 메시지 푸시

### v2.1.79
- 1M 컨텍스트 윈도우 기본 활성화 (Opus 4.6)
- Sonnet 4.6 출시
- `--worktree` 플래그 및 sparse checkout 지원
- Agent Teams (Research Preview)
- 음성 모드 10개 언어 추가 (총 20개)

### 성능 개선
- macOS 시작 시간 ~60ms 단축
- `--resume` 최대 45% 빨라짐
- 대형 레포(250k+ 파일) 메모리 ~80MB 절감
