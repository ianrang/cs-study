---
title: "정보보안기사 실기 기출 분석 및 2026년 2회 대비 로드맵 TODO"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-strategy, todo]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "reference-patching-review.md"
  - "reference-source-index.md"
  - "document-architecture.md"
  - "exam-criteria-and-reference-catalog.md"
  - "subject-type-matrix.md"
  - "subject-type-classification-detail.md"
  - "subject-type-cross-verify-report.md"
source_count: 7
provenance: inferred
summary: "정보보안기사 실기 합격 전략을 위해 기출 복원부터 예상문제 생성까지 단계별 작업을 추적한다."
evergreen: false
---

# 정보보안기사 실기 기출 분석 및 2026년 2회 대비 로드맵 TODO

## 목표
2026년 2회 정보보안기사 실기 시험 대비를 위해, 기출 문제를 정확히 복원·분류하고 공식 출제기준 및 참고문서와 연결한 뒤, 재출제 빈도와 패턴을 기반으로 학습 전략과 예상문제를 만든다.

## 원칙
- 누락된 문제는 추론으로 채우지 않는다.
- 원문·출처·근거가 불명확한 항목은 `미확인`, `후보`, `검증 필요`로 표시한다.
- 공식 출제기준과 법령/고시/공공 가이드는 최신성을 확인한다.
- 예상문제는 `기출 기반 예측`이며 실제 출제를 보장하지 않는다고 명시한다.

## 단계별 TODO

| 단계 | 작업 | 상태 | 산출물 | 완료 기준 |
|---:|---|---|---|---|
| 0 | 문서 아키텍처 고정 | 완료 | `document-architecture.md` | SSOT, 단일 책임, 참조 방향, 중복 방지 규칙 정의 |
| 1 | 기출 문제 복원 | 진행 중 | 회차별 `*-practical-*.md` | 각 회차 문항 원문/답/출처/확신도 기록 |
| 1-1 | PDF 비밀번호 확보 또는 대체 원천 확보 | 진행 중 | source update notes | PDF/웹/문제집 등 원천별 신뢰도 기록 |
| 1-2 | 저신뢰 회차 보강 | 대기 | 보강된 회차 파일 | 11회, 15회, 19~22회 등 미분류·제외 비율 높은 회차 개선 |
| 2 | 기출 문제 분류 | 진행 중 | `subject-type-classification-detail.md`, `subject-type-matrix.md` | 5개 과목 + 단답형/서술형/실무형 분류와 근거 기록 |
| 2-1 | 분류 교차검증 | 진행 중 | `subject-type-cross-verify-report.md` | 명백한 오분류/HIGH finding 해소 |
| 3 | 출제기준 및 참고문서 카탈로그 작성 | 완료 | `exam-criteria-and-reference-catalog.md` | KCA 출제기준, 법령/고시/가이드 후보 상태 분리 |
| 3-0 | 참고문서 패칭 범위 확정 | 진행 중 | `reference-source-index.md` | 필수 1차 문서 중 KCA/PIPC/ISMS-P/기반시설은 패칭 완료, 시큐어코딩 공식 원천 확인 필요 |
| 3-1 | 참고문서 원문 URL/파일 확보 | 진행 중 | `reference-source-index.md` | 각 문서별 공식 URL, 버전, 발행기관, 적용일 기록 |
| 3-2 | 참고문서 텍스트 추출 | 진행 중 | raw asset + extraction status | 패칭 완료 PDF는 `pdftotext` 성공, 시큐어코딩 문서는 원문 확보 후 수행 |
| 4 | 문항-출제기준-참고문서 연결 | 대기 | `item-reference-map.md` | 각 문항에 KCA 주요항목/세부항목/세세항목 + 참고문서 연결 |
| 4-1 | 직접 연결 문항 식별 | 대기 | direct-reference table | 문항에 문서명/법령명/고시명이 직접 등장한 항목 분리 |
| 4-2 | 개념 연결 문항 식별 | 대기 | conceptual-reference table | 키워드/개념 기준 연결, 확신도 high/medium/low 표시 |
| 5 | 기출 패턴과 유형 검토 | 대기 | `pattern-analysis.md` | 과목별·문항유형별·출제기준 항목별 반복 패턴 정리 |
| 5-1 | 빈도 수 분석 | 대기 | `frequency-analysis.md` | 회차별/연도별/과목별/참고문서별 빈도 표 생성 |
| 5-2 | 재출제/변형출제 분석 | 대기 | `recurrence-analysis.md` | 동일 개념 반복, 변형 패턴, 출제 간격 기록 |
| 5-3 | 유의미성 검토 | 대기 | `significance-review.md` | 단순 빈도와 최근성, 출제기준 중요도, 법령 개정성을 함께 평가 |
| 6 | 학습 전략 수립 | 대기 | `study-strategy-2026-02.md` | 고득점 우선순위, 단기 암기표, 서술형 템플릿, 실무형 대응 전략 |
| 7 | 예상 기출 문제 생성 | 대기 | `predicted-practical-questions-2026-02.md` | 근거 문서/기출 패턴/출제기준 항목을 붙인 예상문제 작성 |
| 7-1 | 예상문제 정답·채점포인트 작성 | 대기 | answer key | 단답형 키워드, 서술형 채점요소, 실무형 절차 답안 포함 |
| 7-2 | 예상문제 검증 | 대기 | prediction-validation report | 근거 없는 문제 제거, 문서 연결 누락 보정 |

## 우선순위

| 우선순위 | 작업 | 이유 |
|---:|---|---|
| 1 | `subject-type-cross-verify-report.md`의 HIGH finding 수정 | 현재 분류표에 명백한 오분류/미분류가 있어 이후 빈도 분석을 왜곡함 |
| 2 | 참고문서 패칭 범위 확정 및 원문 URL 확보 | 문항-근거 연결의 기준점이 필요하고, 최신 법령·고시·가이드 변경이 시험 대비 정확도에 직접 영향을 줌 |
| 3 | `item-reference-map.md` 작성 | 기출과 공식/준공식 문서 연결의 핵심 산출물 |
| 4 | 23~30회 고신뢰 회차부터 문항-문서 연결 | 최근 출제 경향과 2026년 대비 관련성이 큼 |
| 5 | 저신뢰 회차 보강 | 장기 빈도/재출제 분석 정확도 향상 |
| 6 | 빈도·재출제 분석 | 전략 학습과 예상문제 생성을 위한 통계 기반 |
| 7 | 2026년 2회 예상문제 생성 | 최종 학습 산출물 |

## 현재 리스크

| 리스크 | 영향 | 대응 |
|---|---|---|
| 1~28회 PDF 암호화 | 공식 원문 대조 불가 | 비밀번호 확보 또는 독립 복원 원천 추가 |
| 일부 회차 웹 복원 품질 낮음 | 빈도 분석 왜곡 | 회차별 confidence 반영, 저신뢰 회차는 통계에서 별도 가중치 |
| 참고문서가 KCA 공식 참고문헌인지 공개 확인 불가 | `KCA가 참고했다`는 단정 불가 | `출제기준/기출과 연결 가능한 참고문서`로 표현 제한 |
| 법령·고시 개정 | 최신 시험 대비 오류 가능 | 문서별 적용일/시행일 필드 유지 |
| 예상문제 과신 | 학습 범위 왜곡 | 예상문제마다 근거와 확신도 표기 |

## 다음 작업 후보

1. `subject-type-cross-verify-report.md` HIGH finding 수정.
2. KISA/PIPC/시큐어코딩/OWASP/CVE 계열 참고문서 패칭 범위 확정.
3. 참고문서 원문 URL/발행기관/버전 확인용 `reference-source-index.md` 생성.
4. 최근 23~30회부터 `item-reference-map.md` 작성.
5. 2026년 2회 대비 우선 학습 주제 초안 작성.
