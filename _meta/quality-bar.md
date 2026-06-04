# Quality Bar — 6축 명제 + AGENTS.md directive

본 문서는 wiki 페이지가 AI 에이전트 ground truth 로 신뢰 가능하기 위한 6축 명제와 검증 규약을 정의한다. Panel-debate B (2026-05-20) 만장 합의.

## 등급 별 적용 매트릭스

| 축 | raw | cs/ (authored) | wiki/ (synthesis) |
|---|---|---|---|
| 1. 정확도 | **hard** (source_paths ≥1) | lazy fallback | **hard** (source_paths ≥1 + provenance:extracted) |
| 2. 전문성 | 면제 | 면제 | soft (LLM judge) |
| 3. 일관성 | 면제 (원본 보존) | lazy fallback | **hard** (taxonomy controlled vocab) |
| 4. 논리성 (페이지 간) | 면제 | 면제 | **hard** (logic-proposition-checker D3 changed pages + 1-hop) |
| 4. 논리성 (페이지 내부) | 면제 | 면제 | soft (사람 review) |
| 5. 정합성 | **hard** (broken link 0) | hard (broken link 0) | **hard** (orphan 0 / broken link 0 / index 등재 / log 추적) |
| 6. 재현성·시의성 | **hard** (source_date 필수) | lazy fallback | **hard ≥2y** (last_verified ≥6m=warn, ≥2y=hard-fail. evergreen=true 면제) |
| + AGENTS.md directive | hard | hard | **hard** (lint.py 자동 검증) |

## 축 1 — 정확도 (Accuracy)

**명제**: 모든 사실 주장은 `source_paths:` frontmatter 에 인용 ≥1 + `provenance: extracted | inferred | ambiguous` 명시.

| Provenance | 의미 | 적용 |
|---|---|---|
| `extracted` | source 에서 직접 추출된 사실 | wiki 페이지 기본값 |
| `inferred` | LLM 합성·추론. source 에 명시되지 않음 | 추론 영역 별도 표기 |
| `ambiguous` | source 간 충돌 또는 불확실 | Open Questions 섹션 의무 |

**검증 도구**: `scripts/lint.py` (source_paths 누락 grep) + `grounding-verifier` subagent (citation 유효성).

**hard-fail 조건**: `source_paths: []` 또는 누락 시 ingest 거부.

## 축 2 — 전문성 (Expertise)

**명제**: 페이지 type 별 표준 섹션 + 섹션 순서 고정. 상세는 `page-type-spec.md`.

**검증 도구**: Templater (작성 시 강제) + `scripts/lint.py` (섹션 존재 grep). 섹션 *내용 품질* 은 자동 검증 불가 → soft-warn.

**soft-warn 조건**: 표준 섹션 누락 시 PR comment.

## 축 3 — 일관성 (Consistency)

**명제**: 동일 entity·concept 의 명칭·표기·약자가 vault 전체 동일. `_meta/taxonomy.md` 의 controlled vocabulary 만 tag 허용.

**검증 도구**: `wiki-lint` (vocab grep) + `logic-proposition-checker` subagent (D2 intra-group / 그룹 내 페이지 boundary).

**hard-fail 조건**: taxonomy 미등재 vocab 사용 시 ingest 거부. supersede 는 ADR + alias 필드 (taxonomy.md 가 canonical).

## 축 4 — 논리성 (Logical coherence)

### 4a. 페이지 간 모순 (hard)

**명제**: 페이지 간 명제 모순 0. 동일 사실 두 페이지 다른 결론 시 `provenance: ambiguous` + Open Questions 강제.

**검증 도구**: `logic-proposition-checker` subagent (D3 inter-group / cross-group). **scope = changed pages + `_meta/backlinks.json` 기반 1-hop neighbor** (Panel B D1=A). nightly 전체 sweep 폐기.

**hard-fail 조건**: HIGH severity finding ≥1 시 ingest 거부.

### 4b. 페이지 내부 논리 흐름 (soft)

**명제**: 주장 → 근거 → 결론 흐름 유지. 단 LLM 자동 검출 부정확 → 사람 review.

**soft-warn 조건**: 사람 review 게이트에서 검토.

## 축 5 — 정합성 (Integrity)

**명제**: orphan 0 / broken link 0 / 누락 cross-ref 0. `wiki/index.md` 가 모든 active 페이지 등재. `wiki/log.md` 가 모든 변경 추적.

**검증 도구**: `scripts/lint.py` orphan/broken-link 알고리즘 + `cross-linker` skill + `grounding-verifier`.

**Orphan 알고리즘** (Panel B):
- wiki/ 페이지 전수 스캔 → markdown link / wikilink 추출
- raw/ + cs/ + development/ → wiki/ 인용 매핑 자동 갱신 (`_meta/backlinks.json`)
- wiki/ 페이지 중 다른 wiki 페이지에서 link 받지 못한 페이지 = orphan (단, overview/index 제외)

**hard-fail 조건**: wiki/ orphan ≥1 또는 broken link ≥1 시 ingest 거부. cs/ 측 orphan 은 **무경고** (사람 의도 보존).

## 축 6 — 재현성·시의성 (Reproducibility & Recency)

**명제**: 모든 source 페이지에 `source_date` (출처 발행일) + `last_verified` (최종 확인 timestamp) + `superseded` (다음 버전 alias) 필드.

**검증 도구**: `scripts/lint.py` timestamp 비교 + 자동 갱신 (URL HEAD check, content hash 변경 감지).

| 임계 | 조건 | 결과 |
|---|---|---|
| `last_verified` 부재 | source 페이지 | hard-fail |
| `last_verified` < 현재 - 6개월 | 일반 페이지 | warn |
| `last_verified` < 현재 - 2년 | 일반 페이지 | hard-fail |
| `evergreen: true` 명시 | foundational paper (예: Transformer 2017) | 2년 임계 면제 |
| `superseded: <alias>` | 새 버전 alias 명시 | retract 자동 표기 |

## AGENTS.md directive 준수

**명제**: AGENTS.md 의 모든 규약 (write scope · ingest 순서 · commit 규약 · LLM 호출 alias 등) 준수.

**검증 도구**: `scripts/lint.py` 정규식 grep.

**대표 grep 룰**:
- write scope 위반: cs/, development/, coding-test/, lang/, tools/ 의 변경이 swan-bot author commit 일 시 거부

**ADR-0001 (2026-06-04)**: `model_id` 직접 인용·자기추론 어휘의 **페이지 본문 grep 규칙은 폐기**. 모델명은 `taxonomy.md` 가 wiki entity vocab 으로 요구(예: `gpt-5`, `claude-opus-4-7`)하므로 본문 grep 은 taxonomy 와 모순이며 raw verbatim 원본 보존도 위반. `model_id` alias 규율은 **LLM 호출 site(scripts/)** 코드 규약으로만 유지(마크다운 검사 아님).

## hard-fail / soft-warn 분리 원칙

- **hard-fail**: 객관 측정 가능 + false positive 낮음. lint.py 또는 subagent HIGH count 자동 차단.
- **soft-warn**: 주관 판단 잔여 (섹션 내용 품질 · 페이지 내부 논리 흐름 · 변형 표현 등). PR comment, 머지 차단 없음.

## Calibration

- 초기 임계: `warn ≥5` OR `HIGH ≥1` 시 차단.
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
