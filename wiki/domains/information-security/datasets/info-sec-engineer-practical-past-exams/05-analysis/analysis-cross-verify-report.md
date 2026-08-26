---
title: 정보보안기사 실기 패턴·빈도 분석 교차검증 리포트
page_type: dataset
tags:
- information-security
- certification
- exam-analysis
- verification
date_created: '2026-07-03'
date_updated: '2026-07-07'
source_paths:
- raw/sources/clipping/b2636bd9f4e0c45c8015893061e20a2f81c6cc9ddeb72e819f4459b613398966/06cd95cdb5be9eeeadabd30a1b74760ac9f1c8f58adfeec80d6590408cd81fcc/manifest.json
summary: 패턴·빈도·재출제·유의미성 분석 산출물이 분류 상세, 매트릭스, 문항-근거 맵과 수량상 정합하는지 검증한 리포트.
---

## Overview









# 정보보안기사 실기 패턴·빈도 분석 교차검증 리포트

### Verdict
- Round count consistency: pass. `index.md`, `subject-type-classification-detail.md`, round reconstruction files 기준 1~31회 총 513문항이 닫힌다.
- Matrix consistency: pass. `subject-type-classification-detail.md`와 `subject-type-matrix.md`의 positive subject/type cell diff는 0건이다.
- Reference-map consistency: pass. 23~30회 `item-reference-map.md`는 144행이고 confidence는 high 140, medium 4, low 0으로 coverage 표와 일치한다.
- Prompt completeness dependency: pass. `source prompt ... unavailable` 회차 파일 잔여는 0건이다.
- Scope limit: 1~28회 thodi-lab/blog-source PDF compilation was unlocked and cross-checked, but KCA official exact wording is not claimed.

### Check Results
| check | result |
|---|---|
| classification detail total | 513 |
| matrix total | 513 |
| detail vs matrix positive cell diffs | 0 |
| round counts vs index | pass |
| item-reference-map rows, 23~30회 | 144 |
| reference confidence | high 140 / medium 4 / low 0 |
| lint | previous `udemy/` frontmatter gaps were isolated under `drafts/udemy/`; rerun current lint for live status |

### Cross-Document Trace
| analysis output | source of truth | verification |
|---|---|---|
| `frequency-analysis.md` | `subject-type-classification-detail.md`, `subject-type-matrix.md`, `item-reference-map.md` | totals and per-cell counts recomputed |
| `recurrence-analysis.md` | round prompt/answer rows + classification evidence | keyword concept groups recomputed from source text |
| `pattern-analysis.md` | `frequency-analysis.md`, `recurrence-analysis.md` | summary statements tied to counted tables |
| `significance-review.md` | `frequency-analysis.md`, `recurrence-analysis.md`, `item-reference-map.md` | priority uses frequency + recency + confidence |

### Known Limits
- Recurrence groups are keyword-based concept clusters. They are suitable for study strategy but not for claiming identical official wording.
- `recurrence-analysis.md` still preserves its original 1~30회 keyword-cluster scope. 31회 is reflected in subject/type frequency and pattern summaries, but not yet in recurrence keyword counts.
- Four recent reference-map rows remain medium confidence: `R24-Q4`, `R28-Q6`, `R30-Q11`, `R30-Q15`.
- 31회 has not yet been expanded into `item-reference-map.md`; criteria/reference frequency remains 23~30회 scope by design.
- KCA official source cross-check remains a future quality upgrade, not a blocker for concept-level frequency and recurrence analysis.

## Schema / Composition

## Usage

## Limitations / Biases

## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|


## Relations

| type | target | notes |
|---|---|---|


## Sources

- `raw/sources/clipping/b2636bd9f4e0c45c8015893061e20a2f81c6cc9ddeb72e819f4459b613398966/06cd95cdb5be9eeeadabd30a1b74760ac9f1c8f58adfeec80d6590408cd81fcc/manifest.json`
