# ADR-0001: 페이지 본문 model_id/자기추론 grep 규칙 폐기 (LLM 호출·프롬프트 한정으로 정정)

- Status: **Proposed** (사용자 승인 대기 — 스키마 공진화 게이트, AGENTS.md:27 / PRD NFR-6)
- Date: 2026-06-04
- 관련: PRD FR-10, business-logic P-ADR-1/2, Claude 메모리 `project-youtube-script` 이연 검증 항목
- 정정 이력: 초안은 "raw 한정 advisory 강등" 이었으나, 사용자 검토(2026-06-04)에서 본 규칙이 *사용자 커밋 규칙이 아니며* cs-study 자체 directive의 **과잉 적용**임이 확인되어 "본문 grep 규칙 폐기"로 정정.

## Context

### 두 규칙 혼동 정정
- **사용자 전역 커밋 규칙**(`~/.claude/CLAUDE.md §커밋 규칙`)은 **커밋 메시지 본문**에 AI/모델 식별자를 넣지 말라는 것 — *페이지 내용과 무관*.
- 본 ADR이 다루는 "페이지 본문에 model_id 금지"는 **cs-study 자체 directive**(`AGENTS.md:113-118` "LLM 호출 규약", `quality-bar.md:91-100`)이며 출처는 panel-debate B(AGENTS.md:138, 2026-05-20). 사용자가 "본문 검열"을 명시 결정한 기록은 없음.

### 규칙의 본래 의도 vs 실제 구현
- 본래 의도(좁음): `AGENTS.md:113-118` 제목 "LLM **호출 규약**" — LLM을 호출할 때 model_id 하드코딩 금지·`llm-config.yaml` alias 사용(모델 변경 단일 지점). 자기추론 어휘도 "**prompt 본문**" 한정(AGENTS.md:116).
- 실제 구현(과잉): `lint.py`(스스로 "skeleton" — lint.py:20)의 `check_directive_model_id_grep`(lint.py:179-193)·`check_directive_self_referential`(lint.py:196-204)가 `collect_findings`(lint.py:233)에서 **모든 .md 본문**에 grep을 적용 → 의도(호출·프롬프트)를 넘어 페이지 내용까지 검열.

### 결정적 모순 — taxonomy와 충돌
`taxonomy.md`는 모델명을 **wiki 페이지가 써야 할 controlled vocabulary(entity)**로 명시한다:
- `taxonomy.md:118` `gpt-5`, `:119` `claude-opus-4-7`, `:120` `claude-sonnet-4-6`, `:121` `claude-haiku-4-5`, `:126` `qwen-2.5`

그런데 `MODEL_ID_PATTERN`(lint.py:44-48)이 정확히 그 문자열들을 차단한다. ⇒ taxonomy가 쓰라고 한 entity 때문에 wiki entity 페이지가 lint 거절. **규칙이 raw뿐 아니라 wiki에서도 틀렸음**을 증명.

## Decision

**페이지 본문에 대한 model_id·자기추론 grep 규칙을 폐기한다(raw·wiki 공통). model_id alias 규율은 LLM 호출 site·프롬프트에만 유지한다.**

1. `scripts/lint.py`: `check_directive_model_id_grep`·`check_directive_self_referential`의 **페이지 본문 grep 적용을 제거**(또는 LLM 호출/prompt 텍스트 검사로 scope 한정). `collect_findings`에서 호출 제거.
2. `_meta/quality-bar.md`:
   - matrix(`quality-bar.md:16`) `+ AGENTS.md directive` 행에서 **"model_id 본문 인용 차단"을 directive 항목에서 제외**(write scope·ingest 순서 등 나머지 directive는 유지).
   - 대표 grep 룰(`quality-bar.md:97-99`)에서 model_id·자기추론 본문 grep 항목 삭제.
3. `AGENTS.md`(113-118): "model_id 직접 인용 금지"의 적용 대상을 **"LLM 호출 설정·프롬프트"** 로 명시(페이지 본문 비적용). taxonomy entity로서의 모델명은 허용.

### 유지되는 것 (약화 없음)
- model_id alias 단일 지점 통제는 `scripts/`가 `LLMResolver.resolve(...)`(llm_config.py)로 호출하는 코드 규약으로 유지 — 마크다운 grep과 무관.
- raw·wiki의 **나머지 lint 전부 유지**: `last_verified`(축6, lint.py:159-161), broken link(축5, lint.py:132-147), source_paths·provenance(축1), taxonomy vocab(축3), write scope directive 등.

## Consequences

- (+) taxonomy가 요구하는 모델 entity를 wiki에서 정상 사용 가능 — 내부 모순 해소.
- (+) 영상/논문 raw verbatim 원문의 모델명이 ingest를 막지 않음(FR-9). 원본 불변(AGENTS.md:24) 정합.
- (+) 실제 모델 통제(alias)는 호출 코드 레벨에 그대로 — 보안·일관성 약화 0.
- (−) 페이지 본문에 model_id가 자유롭게 등장 가능 — 단 taxonomy가 canonical 표기를 관리하므로 표기 일관성은 축3(vocab)으로 별도 보장.

## 대안 (기각)
- **raw만 grep 제외**(초안) — 기각: wiki도 taxonomy와 모순이므로 raw 한정은 모순을 절반만 해소.
- **현행 유지** — 기각: taxonomy ↔ lint 내부 모순 + 사용자 미결정 규칙 + skeleton 과잉 적용.
- raw 본문 model명 마스킹 — 기각: verbatim 정확성·원본 보존 위반.
