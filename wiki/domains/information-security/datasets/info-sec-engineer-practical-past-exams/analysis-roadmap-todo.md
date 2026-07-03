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
  - "item-reference-map.md"
  - "subject-type-matrix.md"
  - "subject-type-classification-detail.md"
  - "subject-type-cross-verify-report.md"
source_count: 8
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
| 1-2 | 저신뢰 회차 보강 | 진행 중 | 보강된 회차 파일 | Naver 카테고리에서 확인 가능한 13~29회 보강 완료, 1~12회는 Information Security Tistory 직접 복원글로 보강 완료 |
| 2 | 기출 문제 분류 | 진행 중 | `subject-type-classification-detail.md`, `subject-type-matrix.md` | 5개 과목 + 단답형/서술형/실무형 분류와 근거 기록 |
| 2-1 | 분류 교차검증 | 진행 중 | `subject-type-cross-verify-report.md` | 미분류 HIGH finding 해소, 남은 source_quality/keyword conflict 검토 |
| 3 | 출제기준 및 참고문서 카탈로그 작성 | 완료 | `exam-criteria-and-reference-catalog.md` | KCA 출제기준, 법령/고시/가이드 후보 상태 분리 |
| 3-0 | 참고문서 패칭 범위 확정 | 완료 | `reference-source-index.md` | 필수 1차 문서 중 KCA/PIPC/ISMS-P/기반시설/시큐어코딩 패칭 완료 |
| 3-1 | 참고문서 원문 URL/파일 확보 | 완료 | `reference-source-index.md` | 각 문서별 공식 URL, 버전, 발행기관, 적용일 기록 |
| 3-2 | 참고문서 텍스트 추출 | 완료 | raw asset + extraction status | 패칭 완료 PDF는 `pdftotext` 성공 |
| 4 | 문항-출제기준-참고문서 연결 | 진행 중 | `item-reference-map.md` | 23~30회 144개 문항 1차 매핑 완료, medium confidence 행 원천 보강 필요 |
| 4-1 | 직접 연결 문항 식별 | 진행 중 | direct-reference table | 23~30회에서 ISMS-P, 시큐어코딩, 기반시설 상세가이드 등 직접 연결 후보 반영 |
| 4-2 | 개념 연결 문항 식별 | 진행 중 | conceptual-reference table | 23~30회 키워드/개념 기준 연결, confidence high/medium 표시 |
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
| 1 | `subject-type-cross-verify-report.md`의 잔여 finding 검토 | 1~12회 source_quality finding은 해소됐고, 남은 항목은 공식 PDF 미검증 및 일부 keyword conflict 판단임 |
| 2 | medium confidence 행의 보조 원천 보강 | OWASP/CVE/CWE/법령/모바일/위협 모델 세부 원천이 보강되면 문항-근거 연결 신뢰도가 올라감 |
| 3 | 참고문서 패칭 범위 확정 및 원문 URL 확보 | 문항-근거 연결의 기준점이 필요하고, 최신 법령·고시·가이드 변경이 시험 대비 정확도에 직접 영향을 줌 |
| 4 | `item-reference-map.md` 유지보수 | 기출과 공식/준공식 문서 연결의 핵심 산출물 |
| 5 | 공식 PDF 대조 또는 추가 독립 원천 보강 | 현재 1~12회는 Tistory 직접 복원글로 보강됐으나 공식 PDF 원문 대조는 아직 미완료 |
| 6 | 빈도·재출제 분석 | 전략 학습과 예상문제 생성을 위한 통계 기반 |
| 7 | 2026년 2회 예상문제 생성 | 최종 학습 산출물 |

## 현재 리스크

| 리스크 | 영향 | 대응 |
|---|---|---|
| 1~28회 PDF 암호화 | 공식 원문 대조 불가 | 비밀번호 확보 또는 독립 복원 원천 추가 |
| 1~12회 공식 PDF 원문 미대조 | Information Security Tistory 직접 복원글로 문항/답안은 보강됐지만 공식 PDF는 암호화됨 | 비밀번호 확보 시 원문 문구와 최종 대조 |
| 일부 회차 웹 복원 품질 낮음 | 빈도 분석 왜곡 | 회차별 confidence 반영, 저신뢰 회차는 통계에서 별도 가중치 |
| 참고문서가 KCA 공식 참고문헌인지 공개 확인 불가 | `KCA가 참고했다`는 단정 불가 | `출제기준/기출과 연결 가능한 참고문서`로 표현 제한 |
| 법령·고시 개정 | 최신 시험 대비 오류 가능 | 문서별 적용일/시행일 필드 유지 |
| 예상문제 과신 | 학습 범위 왜곡 | 예상문제마다 근거와 확신도 표기 |

## 다음 작업 후보

1. `subject-type-cross-verify-report.md` 잔여 MEDIUM finding 판단 또는 저신뢰 회차 원천 보강.
2. OWASP/CVE/CWE 계열 참고문서 패칭 필요성 결정.
3. 23~30회 medium confidence 행의 원천 보강.
4. 공식 PDF 비밀번호 확보 시 1~28회 원문 문구 최종 대조.
5. 2026년 2회 대비 우선 학습 주제 초안 작성.
