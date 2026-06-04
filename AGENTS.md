# LLM Wiki Operating Schema — cs-study

본 파일은 AI 에이전트 (Claude Code / Cursor / Codex / Gemini 등) 가 본 vault 에서 동작할 때의 운영 규약이다. CLAUDE.md 가 사람 (사용자) 의 룰이라면 AGENTS.md 는 LLM 의 룰이다. 두 파일이 충돌 시 CLAUDE.md 가 우선.

## Mission

- 본 vault 는 사용자의 **개인 학습 위키 (CS · 보안 · 개발 · 코딩테스트 · 도구)** 이자 **LLM 학습/RAG ground truth** 이다.
- AI 에이전트는 vault 의 합성 페이지 (`wiki/`) 를 ground truth 로 소비할 수 있어야 한다. 정확도·전문성·일관성·논리성·정합성·재현성·시의성 + 규칙·원칙 준수 보장이 필수.

## Scope 분리 (B0 — Panel C 핵심 결정)

본 schema 는 **외부 LLM 호출** 만 통제한다. Claude Code 본체와 9 portfolio subagent 는 harness 영역.

| Layer | 모델 결정 주체 | 변경 방식 |
|---|---|---|
| Claude Code 본체 + 9 portfolio subagent (arch-cycle-detector, logic-proposition-checker, grounding-verifier 등) | harness 자동 | 사용자 `/model` 명령 |
| Ollama + 외부 LLM API 호출 (scripts/, Smart Connections plugin, LLM Tagger plugin) | `_meta/llm-config.yaml` profile alias | YAML 1곳 수정 |
| Hybrid (subagent 가 외부 LLM 호출) | 해당 subagent 의 prompt 가 `_meta/llm-config.yaml` alias 인용 | 동상 |

## Layered Architecture

| 등급 | 위치 | 변경권 (write) | 역할 |
|---|---|---|---|
| **raw** | `raw/sources/{papers,web,conversations,urls,video}/`, `raw/assets/` | LLM + 사용자 (Web Clipper / Paper Importer / ingest-url / claude-history-ingest / video importer) | 외부 1차 자료. 원본 불변. wiki 합성 source |
| **authored** | `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` | **사용자 only** (LLM read-only) | 사용자 1차 학습 노트. wiki 합성 source |
| **synthesis** | `wiki/{overview,index,log,domains/<domain>/,global/,staging/,archive/,templates/}` | **LLM only** (사용자 review · 승인) | LLM 합성 페이지. AI ground truth |
| **schema** | `_meta/`, `scripts/`, `AGENTS.md` | 사용자 + LLM 공진화 | 운영 규약 |

**중요**:
- LLM 은 `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` 의 어떤 파일도 수정·생성·삭제할 수 없다 (PreToolUse hook 강제).
- LLM 은 `raw/sources/` 에 인용 보존 목적의 작은 frontmatter 보강만 가능하다 (본문 무수정).
- 사용자는 `wiki/` 를 직접 수정할 수 있다 (LLM 의 합성 결과 검토·정정).

## SoT 규약

- **cs/, development/ = authored SoT** (사람 1차 사실). frontmatter `tier: human-note`
- **wiki/ = synthesis SoT** (LLM 합성, AI ground truth). frontmatter `tier: llm-synthesis`
- 같은 사실이 양쪽에 존재 시: cs/ = 원본 사실, wiki/ = 합성·정제·인용 추적. wiki/ 페이지는 `source_paths:` 에 cs/ 경로 명시.

## Cross-link

- **단방향 only**: `wiki/ → cs/development/` 인용 가능. 역방향 (`cs/ → wiki/`) 자동 link 금지 (사용자 명시 commit 만 허용).
- `_meta/backlinks.json` 외부 인덱스로 cs/ 노트의 wiki/ 역참조 매핑. `.gitignore` 처리 (재생성 가능 artifact).
- Obsidian graph view 가 사람용 UX 시각화.

## Ingest

ingest universe = `raw/sources/` + `cs/` + `development/`. source_tier 가중치 (raw=0 / cs=1 / dev=1 / wiki=2). **wiki/ 자체 재-ingest 금지** (hallucination loop 방지).

### Ingest 순서 (단일 source 처리)
1. raw/ 또는 cs/ source 파일 read
2. domain 분류 (low confidence → `wiki/staging/domain-review/` 후 사람 검토)
3. 주요 claim·entity·concept 추출
4. wiki/domains/<domain>/sources/ 에 source summary 페이지 생성
5. wiki/domains/<domain>/{entities,concepts}/ 페이지 신규·갱신
6. wiki/index.md + wiki/log.md 갱신
7. `scripts/commit_wiki.sh` 호출 (author=swan-bot, subject `[wiki-bot]` prefix)

## Query

1. `wiki/index.md` 읽고 관련 domain·페이지 식별
2. domain-local 페이지 우선, global 페이지는 link 시만
3. 답변에 인용 path inline
4. 유의미한 답변은 `wiki/domains/<domain>/queries/` 또는 `wiki/queries/` 에 file-back

## Lint

`scripts/lint.py` 가 6축 + AGENTS.md directive 자동 검증. 사람 호출: `python3 scripts/lint.py`.

## Quality Bar — 6축 + directive

상세는 `_meta/quality-bar.md`. 요약:

| 축 | hard / soft | 자동 도구 |
|---|---|---|
| 1. 정확도 | hard | lint.py + grounding-verifier |
| 2. 전문성 | soft (LLM judge) | LLM judge (수동·주기) |
| 3. 일관성 | hard | lint.py + logic-proposition-checker (D2) |
| 4. 논리성 (페이지 간) | hard | logic-proposition-checker (D3 changed pages + 1-hop) |
| 4. 논리성 (페이지 내부) | soft (사람 review) | 사람 게이트 |
| 5. 정합성 | hard | lint.py + cross-linker |
| 6. 재현성·시의성 | warn ≥6m / hard ≥2y (evergreen=true 면제) | lint.py |
| + directive | hard | lint.py |

## 사람 review 게이트

4 시점에 사람 review 필수:
1. PR 단위 1회
2. raw → wiki 승격 시점 (staging/domain-review/ → domains/)
3. provenance:ambiguous 해소 시점
4. taxonomy supersede 시점 (ADR + alias)

페이지 단위·commit 단위 강제 게이트 금지.

## Frontmatter spec

상세는 `_meta/frontmatter-spec.md`. wiki 페이지는 14 필드 필수. raw 페이지는 최소 4 필드. cs/, development/ 는 lazy fallback (`_meta/defaults.yaml` default 추정).

## Page type

상세는 `_meta/page-type-spec.md`. enum: `concept | entity | comparison | benchmark | dataset | method`. 각 type 별 표준 섹션 + 섹션 순서 고정.

## Taxonomy

상세는 `_meta/taxonomy.md`. controlled vocabulary 만 tag 허용. supersede 시 ADR + alias.

## Naming

- 파일명: lowercase kebab-case
- 디렉토리: 동일
- 동음이의 시 disambiguation suffix

## LLM 호출 규약

- `model_id` 직접 인용 금지 — **LLM 호출 설정·프롬프트(scripts/)** 한정 (ADR-0001). `_meta/llm-config.yaml` profile alias 만 사용
- 페이지 본문(raw·wiki)의 모델명은 검열하지 않음 — `taxonomy.md` 가 모델명을 entity vocab 으로 요구 (ADR-0001, model_id 본문 grep 폐기)
- 자기 추론 어휘 (`I am Claude`, `I am Opus`, ...) 는 **prompt 본문** 에 등장 금지 (페이지 본문 grep 아님)
- runtime canary 가 1일 주기 검증

## Commit 규약

- wiki/ commit author = `swan-bot` (자동 — `git config` + `scripts/commit_wiki.sh`)
- wiki/ commit subject prefix = `[wiki-bot]`
- cs/, development/ commit author = 사용자 (`swan`)
- Conventional commits, 영어 (project CLAUDE.md 따름)

## Quality 보장

- 페이지 새로 만들기보다 기존 페이지 갱신 우선
- 인용 누락 페이지 거부
- 변형 표현 (같은 사실 다른 표기) 거부
- 페이지 간 명제 모순 거부
- 모든 op 후 vault 가 이전보다 더 정합된 상태여야 함

## 참고

- Karpathy LLM Wiki gist (2026-04-04): 본 패턴의 원형
- Panel-debate A/B/C 결정 (2026-05-20): 본 schema 의 합의 근거
- ~/.claude/panel-debate/20260520-*-llm-wiki-{A,B,C}/ : 세션 로그
