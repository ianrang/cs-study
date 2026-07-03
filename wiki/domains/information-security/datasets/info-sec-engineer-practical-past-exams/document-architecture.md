---
title: "정보보안기사 실기 분석 문서 아키텍처"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, documentation-architecture]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "reference-patching-review.md"
  - "reference-source-index.md"
  - "analysis-roadmap-todo.md"
  - "exam-criteria-and-reference-catalog.md"
  - "subject-type-matrix.md"
  - "subject-type-classification-detail.md"
source_count: 6
provenance: inferred
summary: "정보보안기사 실기 기출 분석 문서군의 SSOT, 책임 경계, 참조 방향, 중복 방지 규칙을 정의한다."
evergreen: false
---

# 정보보안기사 실기 분석 문서 아키텍처

## 목적
문서가 늘어나도 유지보수 가능한 구조를 유지하기 위해, 각 문서의 단일 책임과 단방향 참조 규칙을 고정한다.

## 설계 원칙
- SSOT: 같은 사실은 한 문서에만 원본으로 기록한다.
- 단일 책임: 각 문서는 하나의 질문에만 답한다.
- 단방향 참조: 상위 분석 문서는 하위 근거 문서를 참조하지만, 하위 문서는 상위 분석 결과를 역참조하지 않는다.
- OCP: 새 참고문서, 새 회차, 새 분석 결과는 기존 문서를 복제하지 않고 전용 행이나 전용 문서로 확장한다.
- 독립성: 원문 보존, 문항 분류, 참고문서 연결, 통계 분석, 학습 전략은 서로 다른 변경 이유를 갖는다.
- 최소 중복: 문항 원문, 참고문서 목차, 빈도 결과, 예상문제는 각각 한 곳에만 본문을 둔다.

## 문서 레이어

| 레이어 | 역할 | 문서 | 책임 |
|---|---|---|---|
| Source | 원천 보존 | `raw/sources/` 원문 파일 | PDF/HWP/HTML 등 원문 보존. wiki 문서가 원문을 장문 복제하지 않는다. |
| Source Index | 원천 메타데이터 | `reference-source-index.md` | 공식 URL, 발행기관, 버전, 시행일, 저장 경로, 추출 가능 여부만 관리한다. |
| Criteria Catalog | 출제기준/참고문서 의미 카탈로그 | `exam-criteria-and-reference-catalog.md` | KCA 출제기준 구조와 참고문서 후보의 상태·우선순위를 관리한다. |
| Round Source | 회차별 기출 복원 | `*-practical-*.md` | 회차별 문항, 답, 출처, 확신도만 관리한다. 과목 통계나 예측을 넣지 않는다. |
| Classification | 문항 분류 | `subject-type-classification-detail.md`, `subject-type-matrix.md` | 문항의 과목/유형 분류와 회차별 집계만 관리한다. 참고문서 연결은 넣지 않는다. |
| Verification | 품질 검증 | `subject-type-cross-verify-report.md` | 분류·원천·매트릭스의 오류와 한계를 report-only로 관리한다. |
| Mapping | 문항-근거 연결 | `item-reference-map.md` | 문항별 KCA 세부항목과 참고문서 연결 근거를 관리한다. |
| Analysis | 패턴·빈도·재출제 분석 | `pattern-analysis.md`, `frequency-analysis.md`, `recurrence-analysis.md` | 매핑과 분류를 입력으로 분석 결과만 관리한다. |
| Strategy | 학습 전략 | `study-strategy-2026-02.md` | 분석 결과를 바탕으로 학습 우선순위와 답안 전략을 관리한다. |
| Prediction | 예상문제 | `predicted-practical-questions-2026-02.md` | 예측 문제, 근거, 확신도, 채점 포인트만 관리한다. |
| Roadmap | 작업 상태 | `analysis-roadmap-todo.md` | 작업 순서와 상태만 관리한다. 분석 본문을 넣지 않는다. |

## 참조 방향

```text
raw/sources/
  -> reference-source-index.md
  -> exam-criteria-and-reference-catalog.md
  -> item-reference-map.md
  -> pattern-analysis.md / frequency-analysis.md / recurrence-analysis.md
  -> study-strategy-2026-02.md
  -> predicted-practical-questions-2026-02.md

*-practical-*.md
  -> subject-type-classification-detail.md
  -> subject-type-matrix.md
  -> item-reference-map.md
  -> analysis documents
```

역방향 참조는 금지한다. 예를 들어 `*-practical-*.md`는 `predicted-practical-questions-2026-02.md`를 참조하지 않는다.

## SSOT 규칙

| 사실 | SSOT | 다른 문서에서의 허용 방식 |
|---|---|---|
| 원문 파일 위치와 버전 | `reference-source-index.md` | 파일명 또는 문서 ID만 참조 |
| KCA 출제기준 구조 | `exam-criteria-and-reference-catalog.md` | criteria ID 또는 항목명만 참조 |
| 회차별 문항 원문/답 | `*-practical-*.md` | round + item_no만 참조 |
| 과목/문제유형 분류 | `subject-type-classification-detail.md` | subject/type 값만 참조 |
| 회차별 집계 | `subject-type-matrix.md` | 집계 결과 인용만 허용 |
| 문항-참고문서 연결 | `item-reference-map.md` | reference ID와 confidence만 참조 |
| 빈도/재출제 계산 결과 | `frequency-analysis.md`, `recurrence-analysis.md` | 결과 표 인용만 허용 |
| 학습 우선순위 | `study-strategy-2026-02.md` | 전략 문서에서만 본문 관리 |
| 예상문제 | `predicted-practical-questions-2026-02.md` | 예상문제 문서에서만 본문 관리 |

## 문서 ID 규칙

| 대상 | ID 형식 | 예시 |
|---|---|---|
| 회차 문항 | `R{round}-Q{no}` | `R23-Q17` |
| 참고문서 | `REF-{domain}-{slug}` | `REF-PRIVACY-SAFETY-MEASURES` |
| KCA 출제기준 항목 | `KCA-P-{major}.{detail}.{micro}` | `KCA-P-4.1.4` |
| 분석 finding | `FIND-{type}-{seq}` | `FIND-CLASSIFICATION-001` |
| 예상문제 | `PRED-2026-02-{seq}` | `PRED-2026-02-001` |

## 중복 방지 규칙

- 참고문서 원문 본문은 wiki에 장문 복제하지 않는다.
- 문항 원문은 회차 파일에만 둔다.
- `item-reference-map.md`에는 문항 원문 전체가 아니라 짧은 evidence와 ID만 둔다.
- 통계 문서는 계산 결과만 보관하고, 분류표를 다시 복제하지 않는다.
- 전략 문서는 학습 우선순위만 보관하고, 기출 전체 목록을 다시 복제하지 않는다.
- 예상문제는 근거 ID를 붙이되 기출 문항을 그대로 복제하지 않는다.

## 변경 절차

| 변경 유형 | 먼저 수정할 문서 | 이후 갱신 문서 |
|---|---|---|
| 새 원문 참고문서 확보 | `reference-source-index.md` | `exam-criteria-and-reference-catalog.md`, `item-reference-map.md` |
| 기출 문항 복원 수정 | 해당 `*-practical-*.md` | `subject-type-classification-detail.md`, `subject-type-matrix.md`, `item-reference-map.md` |
| 과목 분류 수정 | `subject-type-classification-detail.md` | `subject-type-matrix.md`, 검증 리포트 |
| 참고문서 연결 수정 | `item-reference-map.md` | 분석 문서, 전략 문서, 예상문제 |
| 빈도 계산 수정 | `frequency-analysis.md` | 전략 문서, 예상문제 |
| 예상문제 수정 | `predicted-practical-questions-2026-02.md` | 없음 |

## 검증 체크리스트

| 항목 | 기준 | 상태 |
|---|---|---|
| 순환 참조 | 참조 방향이 Source에서 Prediction으로만 흐른다. | pass |
| SSOT | 같은 사실의 본문 원본이 하나의 문서에만 있다. | pass |
| OCP | 새 문서는 기존 문서 본문 복제 없이 ID/행 추가로 연결된다. | pass |
| 단일 책임 | 각 문서는 하나의 변경 이유만 가진다. | pass |
| 복잡성 | 분석 문서와 전략 문서를 분리해 장문 단일 문서화를 피한다. | pass |

## 금지 사항

- 회차 파일에 학습 전략이나 예상문제를 넣지 않는다.
- 참고문서 카탈로그에 문항별 전체 매핑을 넣지 않는다.
- 빈도 분석 문서에 참고문서 원문 요약을 넣지 않는다.
- 예상문제 문서에서 KCA가 특정 문서를 참고했다고 단정하지 않는다.
- 공식 원문이 확인되지 않은 문서를 `확인됨` 상태로 올리지 않는다.
