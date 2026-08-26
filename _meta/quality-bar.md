# Quality Bar — 6축 명제 + AGENTS.md directive

본 문서는 wiki 페이지가 canonical knowledge로 신뢰 가능하기 위한 6축 검증 관점을 정의한다. frontmatter·page type·recency의 legacy/target 수명은 `_meta/frontmatter-spec.md`와 `_meta/knowledge.schema.json`이 소유한다. `wiki/log.md` 직접 갱신과 `_meta/backlinks.json` materialization은 target pipeline에서 inactive이며 아래 정합성 규칙에 포함하지 않는다.

## 등급 별 적용 매트릭스

| 축 | raw | cs/ (authored) | wiki/ (synthesis) |
|---|---|---|---|
| 1. 정확도 | **hard** (`source_url` 비어 있지 않음) | lazy fallback | **hard** (`source_paths` ≥1 + `provenance: extracted\|inferred\|ambiguous`) |
| 2. 전문성 | 면제 | 면제 | soft (LLM judge) |
| 3. 일관성 | 면제 (원본 보존) | lazy fallback | **hard** (taxonomy controlled vocab) |
| 4. 논리성 (페이지 간) | 면제 | 면제 | **hard** (logic-proposition-checker D3 changed pages + 1-hop) |
| 4. 논리성 (페이지 내부) | 면제 | 면제 | soft (사람 review) |
| 5. 정합성 | **hard** (broken link 0) | hard (broken link 0) | **hard** (broken link 0 / relation cycle 0 / generated index parity) |
| 6. 재현성·시의성 | **hard** (source_date 필수) | lazy fallback | **hard ≥730d** (last_verified age ≥180d=warn, ≥730d=hard-fail. concept의 evergreen=true만 730d 면제) |
| + AGENTS.md directive | hard | hard | **hard** (lint.py 자동 검증) |

## 축 1 — 정확도 (Accuracy)

**명제**: raw 페이지는 원출처 식별자인 `source_url`을 비어 있지 않게 보존한다. 승격 wiki 페이지의 모든 사실 주장은 `source_paths:` frontmatter에 인용 ≥1과 `provenance: extracted | inferred | ambiguous`를 명시한다. authored 페이지는 자기 원문을 source로 사용하는 lazy fallback 대상이다.

| Provenance | 의미 | 적용 |
|---|---|---|
| `extracted` | source에 직접 존재하는 사실. authored 페이지에서는 그 페이지의 사람 작성 원문 자체가 source이고, wiki 페이지에서는 `source_paths`가 가리키는 원문이 source다. | wiki 페이지 기본값 |
| `inferred` | LLM 합성·추론. source 에 명시되지 않음 | 추론 영역 별도 표기 |
| `ambiguous` | source 간 충돌 또는 불확실 | Open Questions 섹션 의무 |

**검증 도구**: `scripts/lint.py` (source_paths 누락 grep) + `grounding-verifier` subagent (citation 유효성).

**hard-fail 조건**: raw 페이지에서 `source_url`이 비거나 누락되면 거부한다. 승격 wiki 페이지에서 `source_paths: []`이거나 누락되면 거부한다. cs/development authored 페이지의 lazy fallback은 이 조건의 대상이 아니다.

## 축 2 — 전문성 (Expertise)

**명제**: 페이지 type 별 표준 섹션 + 섹션 순서 고정. 상세는 `page-type-spec.md`.

**검증 도구**: Templater (작성 시 강제) + `scripts/lint.py` (섹션 존재 grep). 섹션 *내용 품질* 은 자동 검증 불가 → soft-warn.

**soft-warn 조건**: 일반 표준 섹션 누락 시 PR comment. 단, `provenance: ambiguous` 페이지의 `Open Questions` 누락은 충돌 표시 요건 위반이므로 HIGH hard-fail이다.

## 축 3 — 일관성 (Consistency)

**명제**: 동일 entity·concept 의 명칭·표기·약자가 vault 전체 동일. `_meta/taxonomy.md` 의 controlled vocabulary 만 tag 허용.

**검증 도구**: `wiki-lint` (vocab grep) + `logic-proposition-checker` subagent (D2 intra-group / 그룹 내 페이지 boundary).

**hard-fail 조건**: taxonomy 미등재 vocab 사용 시 ingest 거부. supersede 는 ADR + alias 필드 (taxonomy.md 가 canonical).

## 축 4 — 논리성 (Logical coherence)

### 4a. 페이지 간 모순 (hard)

**명제**: 표시되지 않은 페이지 간 명제 모순 0. 동일 사실 두 페이지가 다른 결론이면 `provenance: ambiguous` + Open Questions로 충돌을 명시해야 하며, 이렇게 명시된 충돌은 HIGH가 아니다.

**검증 도구**: `logic-proposition-checker` subagent (D3 inter-group / cross-group). **scope = changed pages + 현재 outgoing edge에서 계산한 direct inbound/outbound 1-hop neighbor**. persistent backlink cache는 사용하지 않는다.

**hard-fail 조건**: 미표시 페이지 간 모순 등 HIGH severity finding ≥1 시 ingest 거부. `provenance: ambiguous` + Open Questions로 명시된 충돌은 거부 대상이 아니다.

### 4b. 페이지 내부 논리 흐름 (soft)

**명제**: 주장 → 근거 → 결론 흐름 유지. 단 LLM 자동 검출 부정확 → 사람 review.

**soft-warn 조건**: 사람 review 게이트에서 검토.

## 축 5 — 정합성 (Integrity)

**명제**: broken link 0 / 누락 cross-ref 0 / directed relation cycle 0. 순서 8 이후 materializer가 active page 100%를 index·overview에 반영하고 temp bytes와 committed bytes의 parity를 검증한다. `wiki/log.md`는 target integrity surface가 아니다.

**검증 도구**: `scripts/lint.py` orphan/broken-link 알고리즘 + `cross-linker` skill + `grounding-verifier`.

**그래프 알고리즘**:
- canonical wiki page의 markdown link·wikilink·typed outgoing relation을 전수 스캔한다.
- inverse·backlink view는 저장하지 않고 outgoing edge에서 계산한다.
- `broader`, `prerequisite-of`, `followed-by`별 directed cycle과 전역 ID·target 해석을 검사한다.

**hard-fail 조건**: broken link, ambiguous target, directed relation cycle 또는 순서 8 이후 generated parity drift가 1건 이상이면 거부한다. authored page의 inbound 부재는 사람 의도를 보존해 경고하지 않는다.

## 축 6 — 재현성·시의성 (Reproducibility & Recency)

**명제**: 모든 source 페이지에 `source_date` (출처 발행일) + `last_verified` (최종 확인 timestamp) + `superseded` (다음 버전 alias) 필드.

**검증 도구**: `scripts/lint.py` timestamp 비교 + 자동 갱신 (URL HEAD check, content hash 변경 감지).

| 임계 | 조건 | 결과 |
|---|---|---|
| `last_verified` 부재 | source 페이지 | hard-fail |
| `last_verified` age ≥180일 | 일반 페이지 | warn |
| `last_verified` age ≥730일 | 일반 페이지 | hard-fail |
| concept의 `evergreen: true` 명시 | foundational paper (예: Transformer 2017) | 730일 hard-fail 임계 면제 |
| `superseded: <alias>` | 새 버전 alias 명시 | retract 자동 표기 |

## AGENTS.md directive 준수

**명제**: AGENTS.md 의 모든 규약 (write scope · ingest 순서 · commit 규약 · LLM 호출 alias 등) 준수.

**검증 도구**: `scripts/lint.py` 정규식 grep.

**대표 grep 룰**:
- write scope 위반: cs/, development/, coding-test/, lang/, tools/ 의 변경이 swan-bot author commit 일 시 거부

**ADR-0001 (2026-06-04)**: `model_id` 직접 인용·자기추론 어휘의 **페이지 본문 grep 규칙은 폐기**. 모델명은 `taxonomy.md` 가 wiki entity vocab 으로 요구(예: `gpt-5`, `claude-opus-4-7`)하므로 본문 grep 은 taxonomy 와 모순이며 raw verbatim 원본 보존도 위반. `model_id` alias 규율은 **LLM 호출 site(scripts/)** 코드 규약으로만 유지(마크다운 검사 아님).

## hard-fail / soft-warn 분리 원칙

- **hard-fail**: 객관 측정 가능 + false positive 낮음. lint.py 또는 subagent HIGH count 자동 차단.
- **soft-warn**: 주관 판단 잔여 (섹션 내용 품질 · 페이지 내부 논리 흐름 · 자동 판정 불가능한 의미상 paraphrase 등). PR comment, 머지 차단 없음. taxonomy alias는 canonical 대체값을 MEDIUM으로 안내하고, taxonomy 미등재 tag·entity와 잘못된 stable ID는 hard-fail이다.

## Calibration

- 차단 임계: `HIGH ≥1`. `MEDIUM`과 soft-warn은 개수와 내용을 보고하되 단독으로 머지를 차단하지 않는다.
- **2주 dogfood + PR 10+ 표본 + abstain rate 측정 후 임계 재조정**.
- 정확도 / 재현성 / 페이지 간 모순 축은 P50 무관 hard 유지.

## 사람 review 게이트 (4 시점)

1. PR 단위 1회
2. raw → wiki 승격 시점 (`wiki/staging/domain-review/` → `wiki/domains/`)
3. provenance:ambiguous 해소 시점
4. taxonomy supersede 시점 (ADR + alias)

페이지 단위·commit 단위 강제 게이트 금지.

## 비용 cap

- 인프라·클라우드 외부 결제 비용 0 (Panel B D2=인프라 비용만 고려).
- Max 5시간 한도 burning 만 모니터링 (`scripts/llm_usage.py` profile 별 일일 호출 추적).
- LLM judge (전문성 + 페이지 내부 논리) 호출은 wiki 승격 시점 한정 — commit 단위 호출 금지.

## 참고

- 결정 출처: `~/.claude/panel-debate/20260520-134649-llm-wiki-B/`
- 관련 문서: `AGENTS.md`, `frontmatter-spec.md`, `page-type-spec.md`, `taxonomy.md`, `defaults.yaml`
