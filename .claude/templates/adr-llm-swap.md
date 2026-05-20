# ADR: LLM Profile Swap — {{ADR_NUMBER}}

**Status**: Draft | Proposed | Accepted | Superseded
**Date**: {{YYYY-MM-DD}}
**Author**: swan
**Related**: `_meta/llm-config.yaml`, AGENTS.md §"LLM 호출 규약"

## Context

본 ADR 의 트리거 (해당 항목 체크):
- [ ] 신규 alias 추가 (`_meta/llm-config.yaml` models 블록)
- [ ] 기존 profile default 교체 (`profiles.<name>` swap)
- [ ] alias supersede (deprecated=true, fallback redirect)
- [ ] cost_tier 임계 변경 (daily_call_cap)

배경 (1-2 문단): 무엇이·왜 변하는가.

## Decision

변경 요약:

| 변경점 | Before | After |
|---|---|---|
| profile `<name>` | `<old-alias>` | `<new-alias>` |
| 또는 models 블록 | (해당 시) | (해당 시) |

## 7-step 절차 체크리스트 (Panel C B5)

skip 금지. 모든 step 통과 후 PR 머지.

- [ ] (1) **ADR 작성** — 본 문서. 변경 사유·영향 범위·rollback 절차.
- [ ] (2) **신규 alias 추가 PR** — `_meta/llm-config.yaml` models 블록 추가. profiles 는 아직 미swap.
- [ ] (3) **Smoke gate** — `python3 scripts/llm_smoke.py --alias <new-alias>` 통과. (응답 형식·토큰·latency 기본 검증)
- [ ] (4) **1주 dogfood** — 사용자 dev 환경에서 신규 alias 만 사용. lint warn / 사용자 dogfood 보고 0 이어야.
- [ ] (5) **profiles default swap PR** — `_meta/llm-config.yaml` profiles.<name> 을 신규 alias 로 swap.
- [ ] (6) **1주 모니터링** — `scripts/llm_usage.py` 일일 호출 추적 + runtime canary 1일 주기.
- [ ] (7) **구 alias deprecated** — `models.<old-alias>.deprecated: true` 추가. 1주 grace period 후 삭제 PR.

## 비용 추정 (Panel C B5 산식)

`{{cost_tier base price}} × {{예상 일일 호출 수}} × 7 = {{7일 비용 추정}}`

예시 (Sonnet → Opus default swap, profile=ingest):
- Opus cost_tier=high, base ≈ $0.015 / 1k output tokens
- 예상 일일 호출 = 100 (daily_call_cap 동일)
- 평균 응답 = 2k output tokens
- 7일 추정: $0.015 × 2 × 100 × 7 = $21
- Max plan 5시간 한도 burning 추가 영향: (Opus 한도 무관 — Max plan 내 호출)

## Fallback Chain 검증

```bash
python3 scripts/llm_config.py fallback {{profile}}
```

`fallback_max_tier` 위반 (cost ceiling) 없음 확인.

## Rollback 절차

1. `_meta/llm-config.yaml` 변경 git revert (1 commit)
2. `python3 scripts/llm_config.py invalidate` 호출 (cache 30s TTL — 자동 회복도 가능)
3. 신규 alias 사용 plugin / skill 의 frontmatter `model_profile` 영향 확인

## 검증 — Smoke gate 결과

```
{{smoke gate output paste}}
```

## 검증 — 1주 dogfood 결과

- lint warn 발생 횟수:
- 사용자 dogfood 보고 (불만 / 응답 품질 / latency):
- runtime canary alert:

## 검증 — 1주 모니터링 결과

- 일일 호출 평균:
- daily_call_cap 초과 횟수:
- 사용자 불만:

## Decision 확정 사유

(체크리스트 통과 + 비용·품질 정합 시 작성)

## Supersedes / Superseded by

- (있을 시 ADR link)

## 참고

- Panel C 결정: `~/.claude/panel-debate/20260520-140056-llm-wiki-C/`
- `_meta/llm-config.yaml`
- `AGENTS.md` §"Scope 분리 (B0)"
