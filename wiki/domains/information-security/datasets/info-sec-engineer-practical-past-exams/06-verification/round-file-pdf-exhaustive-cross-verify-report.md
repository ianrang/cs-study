---
title: 정보보안기사 실기 회차 파일 PDF 전수 교차검증 리포트
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
- pdf-source
- verification
date_created: '2026-07-06'
date_updated: '2026-07-16'
source_paths:
- raw/sources/clipping/b458541ca2c57a5d164c2eceee0b6b32a1de2e25a2e006df720e13b211d8a211/48e821aec119eab2de564c6b9527944044e11156f436ff986c43bfbd3b243b4b/manifest.json
summary: 정보보안기사 실기 1~28회 회차별 md 복원 파일 459문항을 thodi-lab/blog-source PDF 편집본과 전수 대조하고,
  30회 사용자 제공 PDF를 별도 대조한 검증 결과.
---

## Overview































# 정보보안기사 실기 회차 파일 PDF 전수 교차검증 리포트

### Verdict
1~28회 회차 파일 459문항을 PDF 편집본의 단답형·서술형 `문제+답` 추출 텍스트와 전수 대조했다. PDF는 KCA 공식 원문이 아니라 thodi-lab/blog-source 편집본이므로, 이 검증은 `KCA 공식 문구 보장`이 아니라 `현재 보유 PDF 편집본 기준의 회차 파일 정합성 검증`이다.

전수 검토 결과, PDF 기준으로 실제 답안·문항 조건이 달라 보이는 항목 2건을 수정했다. 그 외 낮은 자동 매칭 항목은 대부분 PDF 텍스트 추출이 여러 문제를 한 블록으로 합치거나, md가 표·이미지 문항을 paraphrase하여 생긴 점수 저하로 판정했다. 29회는 제공 PDF 범위 밖이다. 30회는 2026-07-07 사용자 제공 PDF를 별도 텍스트 추출해 기존 회차 파일과 대조했다. 이후 2026-07-16에는 1~100번의 기술 정확성을 별도 검토해 PDF 대조와 성격이 다른 12개 기술 정정을 반영했다. 상세는 `first-100-content-review-2026-07-16.md`를 따른다.

### Method
| step | description |
|---|---|
| PDF extraction | 사용자 제공 비밀번호로 1~28회 단답형·서술형 `문제+답` PDF를 열고 `pdftotext -raw`로 텍스트화했다. 비밀번호 값은 문서에 보존하지 않는다. |
| md parsing | `2013-01-practical-01.md`부터 `2025-01-practical-28.md`까지 `## Reconstruction` 표의 459행을 파싱했다. |
| automated matching | 각 md 행의 `reconstructed prompt + answer`를 PDF 전체 문제 블록과 정규화된 문자열 유사도 및 답안 키워드 겹침으로 비교했다. |
| manual review | 자동 점수가 낮은 1~13회·22회·28회 후보는 PDF raw 텍스트에서 키워드 주변 줄을 직접 확인했다. |
| correction | PDF 문항 조건과 답안이 명확히 다른 항목만 회차 파일에 반영했다. |

### Coverage
| scope | count | result |
|---|---:|---|
| 1~28회 md reconstruction rows | 459 | all parsed |
| PDF `문제+답` extracted blocks | 350 | 단답형 241, 서술형 109; 일부 블록은 PDF 줄바꿈 때문에 여러 문제를 포함 |
| high automated match rounds | 14~27회 | strong alignment |
| manual-review-heavy rounds | 1~13회, 22회, 28회 | low score does not equal error; direct keyword review applied |
| PDF-scope-excluded rounds | 29회 | provided 1~28회 PDF does not cover this round |
| Additional user-provided PDF | 30회 | extracted with `pdftotext -layout`; 18 items aligned with current reconstruction and answer details were tightened |

### Corrected Items
| file | no | issue | correction |
|---|---:|---|---|
| `2015-01-practical-05.md` | 5 | md answer was `5년 / 월 1회 / 6개월`, while PDF item 201 states `3년 / 월 1회 / 1년`. | Answer corrected to `A : 3년 B : 월 1회 C : 1년`. |
| `2018-01-practical-11.md` | 8 | md prompt/answer used `정보통신망법` and `5년 / 1회 / 6개월`, while the adjacent PDF sequence after SNMP item states 개인정보 안전성 확보조치 기준 with `3년 / 1회 / 1년`. | Prompt and answer corrected to 개인정보 안전성 확보조치 기준 제5조/접속기록 기준 and `A : 3 B : 1 C : 1`. |

PDF 대조에서 수정한 위 2건과, 기술 표준·공식 문서 대조에서 수정한 항목은 서로 다른 검증 축이다. 후자는 [1~100번 기술 정확성 교차검증](first-100-content-review-2026-07-16.md)을 단일 기록으로 사용한다.

### Reviewed Low-Score Classes
| class | examples | decision |
|---|---|---|
| PDF block merge | 2015-01 #15, 2015-01 #16, 2025-01 #17~18 | PDF extraction merged neighboring essay blocks; raw keyword search confirms corresponding PDF content exists. |
| paraphrased image/table prompt | 2016-02 #6, 2017-02 #14, 2018-02 #14 | md reconstructs values from diagrams/tables; PDF raw text loses layout, so exact string score is low. No answer contradiction confirmed. |
| short answer with minimal tokens | 2016-01 #8, 2019-01 #4, 2025-01 #12 | Short answers such as `Cyber Kill Chain`, `Memcached`, `Deep link` have low overlap in long PDF blocks but are present by direct search. |
| law-retention values | 2015-01 #5, 2018-01 #8 | Two confirmed contradictions were corrected. |

### Round-Level Result
| range | result |
|---|---|
| 1~12회 | Cross-checked against PDF compilation plus Information Security Tistory lineage. Two law-retention answer defects corrected. Remaining low scores are explainable by paraphrase/layout loss. |
| 13회 | Cross-checked; no additional answer contradiction confirmed. |
| 14~21회 | Strong automated alignment with PDF compilation. No correction required in this pass. |
| 22회 | Several low/mid scores caused by short answers and PDF block merge; no answer contradiction confirmed. |
| 23~27회 | Strong automated alignment with PDF compilation. No correction required in this pass. |
| 28회 | Automatic scores remain lower because the PDF uses terse final blocks, but manual confirmation already verifies all 18 core items. No correction required in this pass. |

### Remaining Limits
- This report does not claim KCA official wording. It only validates the md files against the local thodi-lab/blog-source PDF compilation and accessible web reconstruction lineage.
- `pdftotext -raw` loses image/table geometry. For litigation-grade wording or exact table layout, the original PDF page image must be inspected item by item.
- 29회 is outside the available PDF ranges and remains governed by its own web-source boundary.
- 31회 was added from a user-provided HTML table, not from the 1~28회 PDF compilation.
- 32회 still has no verified restoration source in this dataset.

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

- `raw/sources/clipping/b458541ca2c57a5d164c2eceee0b6b32a1de2e25a2e006df720e13b211d8a211/48e821aec119eab2de564c6b9527944044e11156f436ff986c43bfbd3b243b4b/manifest.json`
