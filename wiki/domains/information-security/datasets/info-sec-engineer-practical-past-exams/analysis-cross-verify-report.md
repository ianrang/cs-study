---
title: "정보보안기사 실기 패턴·빈도 분석 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-analysis, verification]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "frequency-analysis.md"
  - "recurrence-analysis.md"
  - "pattern-analysis.md"
  - "significance-review.md"
  - "subject-type-classification-detail.md"
  - "subject-type-matrix.md"
  - "item-reference-map.md"
source_count: 7
provenance: inferred
summary: "패턴·빈도·재출제·유의미성 분석 산출물이 분류 상세, 매트릭스, 문항-근거 맵과 수량상 정합하는지 검증한 리포트."
evergreen: false
---

# 정보보안기사 실기 패턴·빈도 분석 교차검증 리포트

## Verdict
- Round count consistency: pass. `index.md`, `subject-type-classification-detail.md`, round reconstruction files 기준 1~30회 총 495문항이 닫힌다.
- Matrix consistency: pass. `subject-type-classification-detail.md`와 `subject-type-matrix.md`의 positive subject/type cell diff는 0건이다.
- Reference-map consistency: pass. 23~30회 `item-reference-map.md`는 144행이고 confidence는 high 140, medium 4, low 0으로 coverage 표와 일치한다.
- Prompt completeness dependency: pass. `source prompt ... unavailable` 회차 파일 잔여는 0건이다.
- Scope limit: official PDF exact wording remains unverified because local PDFs are password-protected.

## Check Results
| check | result |
|---|---|
| classification detail total | 495 |
| matrix total | 495 |
| detail vs matrix positive cell diffs | 0 |
| round counts vs index | pass |
| item-reference-map rows, 23~30회 | 144 |
| reference confidence | high 140 / medium 4 / low 0 |
| lint | `HIGH=0, MEDIUM=0` |

## Cross-Document Trace
| analysis output | source of truth | verification |
|---|---|---|
| `frequency-analysis.md` | `subject-type-classification-detail.md`, `subject-type-matrix.md`, `item-reference-map.md` | totals and per-cell counts recomputed |
| `recurrence-analysis.md` | round prompt/answer rows + classification evidence | keyword concept groups recomputed from source text |
| `pattern-analysis.md` | `frequency-analysis.md`, `recurrence-analysis.md` | summary statements tied to counted tables |
| `significance-review.md` | `frequency-analysis.md`, `recurrence-analysis.md`, `item-reference-map.md` | priority uses frequency + recency + confidence |

## Known Limits
- Recurrence groups are keyword-based concept clusters. They are suitable for study strategy but not for claiming identical official wording.
- Four recent reference-map rows remain medium confidence: `R24-Q4`, `R28-Q6`, `R30-Q11`, `R30-Q15`.
- Official PDF cross-check remains a future quality upgrade, not a blocker for concept-level frequency and recurrence analysis.
