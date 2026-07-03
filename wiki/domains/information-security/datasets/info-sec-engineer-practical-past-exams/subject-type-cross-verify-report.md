---
title: "정보보안기사 실기 과목/유형 매트릭스 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction, verification]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "subject-type-matrix.md"
  - "subject-type-classification-detail.md"
  - "index.md"
source_count: 3
provenance: inferred
summary: "회차별 과목/문제유형 매트릭스와 상세 분류의 내부 정합성 및 Tistory 1~28회 교차검증 결과."
evergreen: false
---

# 정보보안기사 실기 과목/유형 매트릭스 교차검증 리포트

## Verdict
- Internal consistency: pass. Round files, index counts, item-level classification, and matrix totals close against the same 495-question dataset.
- Blog-source verification: pass for structural cross-check. 1~28회 Tistory posts were parsed by sequential question number and answer marker; no missing answer block was found.
- Corrected discrepancy: 13회 was corrected from 16 rows to the 15-question Information Security Tistory source.
- Official-problem verification: not claimed. Local official PDFs are password-protected, so exact official wording remains outside the current verification scope by user decision.
- Classification status: pass for completeness. No unclassified item remains after the 2026-07-03 Tistory/Naver classification cleanup.

## Finding Summary
| severity | count |
|---|---:|
| HIGH | 0 |
| MEDIUM | 0 |

| category | count |
|---|---:|
| source_count_mismatch | 0 |
| missing_answer_block | 0 |
| unclassified_with_clear_evidence | 0 |
| subject_keyword_conflict | 0 |
| source_quality_low | 0 |
| official_pdf_unavailable_scope_limit | 1 |

## Resolved in 2026-07-03 Tistory Cross-Check
- `source_count_mismatch`: 13회 → Tistory 원문 기준 15문항으로 회차 파일, index, detail, matrix를 정정.
- `detail_evidence_pollution`: 14회 #16, 16회 #16, 17회 #16, 18회 #16 → 블로그 분석 문구가 섞인 prompt evidence를 회차 파일의 문항 evidence로 교체.
- `unclassified_with_clear_evidence`: 17회 #4/#5/#6, 18회 #3/#4/#7, 25회 #13, 26회 #5, 27회 #9, 30회 #9 → 회차 파일 prompt/answer 기준으로 과목 확정.
- `subject_keyword_conflict`: 18회 #16 → DNS Amplification/DRDoS 문항이므로 네트워크 보안으로 정정.

## Scope Limit
- 공식 PDF는 비밀번호를 알 수 없어 직접 대조하지 않았다. 현재 판정은 Information Security Tistory 및 기존 Naver 교차 확인 가능한 블로그 복원본 기준의 정합성 판정이다.

## Method
- Parsed all same-directory `*-practical-*.md` reconstruction tables.
- Parsed Information Security Tistory 1~28회 pages by sequential question number and answer marker.
- Parsed `subject-type-classification-detail.md` item rows.
- Parsed `subject-type-matrix.md` matrix cells and unclassified/excluded rows.
- Checked that each matrix cell item list equals the corresponding item-level detail list.
- Checked that classified + unclassified + excluded row counts close against source reconstruction row counts.
- Checked that `index.md` item counts match actual round reconstruction row counts.
