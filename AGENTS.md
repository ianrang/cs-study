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
| **raw** | immutable bundle `raw/sources/<source_type>/<source_id>/<digest>/`, legacy curated page `raw/sources/{papers,web,conversations,urls,video}/`, `raw/assets/` | LLM + 사용자 (capture / Web Clipper / legacy importer) | 외부 1차 자료. 원본 불변. wiki 합성 source |
| **authored** | `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` | **사용자 only** (LLM read-only) | 사용자 1차 학습 노트. wiki 합성 source |
| **synthesis** | `wiki/{overview,index,log,domains/<domain>/,global/,staging/,archive/,templates/}` | 사용자 검토·정정 + deterministic pipeline (LLM은 semantic draft만 생성) | 합성 페이지. canonical knowledge |
| **project** | `projects/<project>/` | 사용자 + LLM | 실행 코드·테스트·프로젝트 문서. wiki 합성 대상이 아니며 필요한 지식 원본은 repo-relative path로 단방향 참조 |
| **schema** | `_meta/`, `scripts/`, `AGENTS.md` | 사용자 + LLM 공진화 | 운영 규약 |

**중요**:
- LLM 은 `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` 의 어떤 파일도 수정·생성·삭제할 수 없다 (PreToolUse hook 강제).
- LLM 은 legacy curated `raw/sources/*.md`에 인용 보존 목적의 작은 frontmatter 보강만 가능하다. content-addressed bundle은 기존 bytes 수정 없이 새 digest revision만 추가한다.
- 사용자는 legacy `wiki/`를 검토·정정할 수 있다. target pipeline 전환 후 canonical write는 승인된 semantic plan을 deterministic renderer가 수행한다.
- `projects/` 는 `wiki/` migration·materialization·knowledge check 입력에 포함하지 않는다.
- `projects/**/*.md`는 일반 프로젝트 문서이며 `wiki/` frontmatter를 사용하지 않는다. 프로젝트 계약은 문서 본문과 실행 가능한 테스트가 소유한다.

## SoT 규약

- **cs/, development/ = authored SoT** (사람 1차 사실). frontmatter `tier: human-note`
- **wiki/ = synthesis SoT**. 실제 migration 전 legacy 페이지는 기존 15필드 계약을 유지하고, 승인된 migration 이후 `_meta/knowledge.schema.json`의 최소 properties 계약으로 전환한다.
- **projects/ = executable SoT**. 실행 코드·테스트·프로젝트 계약을 소유하며 canonical knowledge를 복제하지 않는다.
- **_meta/domains.yaml = domain registry SoT**. wiki domain 목록, active/inactive 상태, source root hint 는 이 파일에서만 관리한다.
- **_meta/taxonomy.md = vocabulary SoT**. tag/entity/concept controlled vocabulary 를 관리하며 domain registry 와 병합하지 않는다.
- **_meta/knowledge.schema.json = 현재 지식 문서·ArtifactManifest·SemanticPlan schema SoT**. `_meta/wiki-ingest-write-plan.schema.json`은 superseded v1 회귀 fixture이며 현재 CLI 입력이 아니다.
- **_meta/knowledge-migration-plan.schema.json = 전역 schema migration resolved-plan SoT**. unresolved decision 0, exact universe·digest·rendered bytes가 없으면 backup·apply를 거부한다.
- 같은 사실이 양쪽에 존재 시 cs/는 authored 원본, wiki/는 합성·정제·인용 추적을 소유한다. target `source_paths`는 capture된 artifact manifest만 허용하며 authored 원본도 capture 후 인용한다.

## Cross-link

- **단방향 only**: legacy `wiki/ → cs/development/` 인용은 migration 전까지 보존한다. target wiki는 artifact manifest만 인용하며 `cs/development/ → wiki/` 자동 link는 금지한다.
- backlink와 inverse relation은 checker·Obsidian view가 계산한다. `_meta/backlinks.json` 선언은 순서 9 제거 대상인 inactive legacy 규약이며 신규 pipeline이 생성·소비하지 않는다.
- Obsidian graph view가 사람용 UX 시각화를 소유한다.

## Ingest

target ingest universe는 사용자가 명시한 artifact manifest 목록뿐이다. `raw/`, `cs/`, `development/`의 암묵 scan과 `wiki/` 재-ingest를 금지한다. 현재 legacy ingest 설명은 migration 전 기록이며 신규 CLI 규약이 아니다.

### Ingest 순서 (단일 source 최종 wiki 반영)

아래 순서는 source 가 wiki ground truth 로 최종 반영되는 일반 lifecycle 이다. 특정 MVP stage 는 이 순서의 일부만 수행할 수 있으며, 해당 stage 의 설계 문서가 범위를 더 좁게 제한하면 그 제한을 따른다.
1. raw/ 또는 cs/ source 파일 read
2. `_meta/domains.yaml` 기반 domain 분류 (low confidence, missing/inactive domain → `wiki/staging/domain-review/` 후 사람 검토)
3. 주요 claim·entity·concept 추출
4. wiki/domains/<domain>/sources/ 에 source summary 페이지 생성
5. wiki/domains/<domain>/{entities,concepts}/ 페이지 신규·갱신
6. 순서 8 이후 materializer가 index·overview를 derived-only로 재생성한다. 그 전 stage는 generated surface를 직접 갱신하지 않는다.
7. full check와 사용자 review 뒤 프로젝트 커밋 규약을 따른다.

과거 YouTube MVP의 source summary·candidate report·verification roll-up과 `wiki/log.md` 직접 갱신 절차는 target pipeline에서 inactive다. target lifecycle은 위 1–7과 materializer의 index·overview derived-only 생성만 따른다.

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
| 6. 재현성·시의성 | legacy lint는 기존 필드를 검사하고 target checker는 immutable artifact digest·manifest 존재를 검사한다 | lint.py + target checker |
| + directive | hard | lint.py |

## 사람 review 게이트

4 시점에 사람 review 필수:
1. PR 단위 1회
2. raw → wiki 승격 시점 (staging/domain-review/ → domains/)
3. legacy `provenance: ambiguous` 또는 target claim conflict 해소 시점
4. taxonomy supersede 시점 (ADR + alias)

페이지 단위·commit 단위 강제 게이트 금지.

## Frontmatter spec

상세 수명은 `_meta/frontmatter-spec.md`가 정의한다. 실제 migration 전 legacy wiki content는 15필드 계약을 유지한다. migration target은 `_meta/knowledge.schema.json`의 7개 필수 properties와 조건부 필드만 허용한다. 두 계약을 같은 tree에 동시에 적용하지 않는다.

## Page type

실제 migration 전 legacy enum 6종과 섹션은 `_meta/page-type-spec.md`가 소유한다. migration target enum 8종과 섹션은 `_meta/knowledge.schema.json`만 소유하며 두 계약을 동시에 적용하지 않는다.

## Taxonomy

상세는 `_meta/taxonomy.md`. controlled vocabulary 만 tag 허용. supersede 시 ADR + alias. domain 추가·비활성화는 `_meta/domains.yaml` 변경에서 시작하며, taxonomy 확장이 필요하면 별도 review 로 처리한다.

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
- taxonomy alias는 canonical 대체값을 MEDIUM으로 안내하고, taxonomy 미등재 tag·entity와 잘못된 stable ID는 거부한다. 의미상 paraphrase처럼 자동 판정할 수 없는 변형은 soft-review 대상으로 둔다.
- 표시되지 않은 페이지 간 명제 모순은 거부한다. `provenance: ambiguous`와 Open Questions로 명시한 충돌은 보존 가능한 review 상태다.
- 모든 op 후 vault 가 이전보다 더 정합된 상태여야 함

## 참고

- Karpathy LLM Wiki gist (2026-04-04): 본 패턴의 원형
- Panel-debate A/B/C 결정 (2026-05-20): 본 schema 의 합의 근거
- ~/.claude/panel-debate/20260520-*-llm-wiki-{A,B,C}/ : 세션 로그
