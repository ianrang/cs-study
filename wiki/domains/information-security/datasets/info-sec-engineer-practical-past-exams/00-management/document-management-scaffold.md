---
title: 정보보안기사 실기 문서 관리 스캐폴드
page_type: dataset
tags:
- information-security
- certification
- documentation-architecture
- scaffold
date_created: '2026-07-03'
date_updated: '2026-07-09'
source_paths:
- raw/sources/clipping/b5f8e13310da21d9f9b84fe22b371758ffbe0c5fdd0aeef526f83e4c6f1b3206/da85dce163492b152fcd12908d9bb5ecda98daf124694b9c4970784f35718357/manifest.json
summary: 정보보안기사 실기 기출 분석 문서군의 역할별 분류, 진입점, 변경 규칙, 검증 게이트를 관리한다.
---

## Overview






# 정보보안기사 실기 문서 관리 스캐폴드

### 목적
문서군을 복잡하게 나누기보다, 응집도와 변경 이유를 기준으로 문서 역할을 고정한다. 이 문서는 문서 탐색과 변경 진입점을 관리하며, 분석 본문이나 기출 문항 원문을 보관하지 않는다.

### 관리 원칙
- 응집도: 같은 변경 이유를 가진 문서만 같은 그룹으로 본다.
- SSOT: 원문, 분류, 매핑, 분석, 전략, 예상문제는 각각 하나의 원본 문서군만 가진다.
- 원자성: 한 변경은 하나의 주 문서군에서 시작하고, 파생 문서는 변경 절차에 따라 갱신한다.
- 정합성: 모든 파생 문서는 상위 근거 문서의 ID, 파일명, 집계값을 재사용한다.
- 보수성: 링크와 `source_paths`를 깨뜨릴 수 있는 물리 이동은 별도 마이그레이션 작업으로만 수행한다.

### 진입점

| 목적 | 먼저 열 문서 | 다음 문서 | 금지 |
|---|---|---|---|
| 전체 상태 파악 | `index.md` | `analysis-roadmap-todo.md` | 회차 파일을 임의 순회하며 상태를 추론하지 않는다. |
| 문서 규칙 확인 | `document-architecture.md` | 이 문서, `document-physical-migration-plan.md` | 분석 본문을 관리 문서에 복제하지 않는다. |
| 회차별 기출 확인 | 해당 `*-practical-*.md` | `prompt-completeness-cross-verify-report.md` | 전략·예상문제를 회차 파일에 넣지 않는다. |
| 과목/유형 확인 | `subject-type-matrix.md` | `subject-type-classification-detail.md` | 분류 근거 없이 매트릭스만 수정하지 않는다. |
| 참고문서 근거 확인 | `reference-source-index.md` | `exam-criteria-and-reference-catalog.md`, `item-reference-map.md` | KCA 공식 참고문헌이라고 단정하지 않는다. |
| 분석 결과 확인 | `frequency-analysis.md` | `recurrence-analysis.md`, `pattern-analysis.md`, `session-slot-pattern-analysis.md` | 회차별 원문을 분석 문서에 다시 복제하지 않는다. |
| 학습 실행 | `study-strategy-2026-02.md`, `hands-on-integrated-study-roadmap-2026-02.md` | `predicted-practical-questions-2026-02.md` | 예상문제를 실제 출제 보장처럼 표현하지 않는다. |
| 품질 검증 | 관련 `*-cross-verify-report.md` 또는 `prediction-validation-report.md` | `analysis-roadmap-todo.md` | 검증 리포트에서 원문을 임의 보정하지 않는다. |

### 문서 그룹

| 그룹 | 문서 | 응집 기준 | 주 변경 이유 |
|---|---|---|---|
| Management | `document-architecture.md`, `document-management-scaffold.md`, `document-physical-migration-plan.md`, `analysis-roadmap-todo.md` | 문서 운영 규칙, 물리 이동 계획, 작업 상태 | 문서군의 역할, 절차, 작업 순서, 물리 스캐폴딩 계획이 바뀔 때 |
| Navigation | `index.md` | 회차 복원 파일과 전체 커버리지 탐색 | 회차 파일이 추가·이동·상태 변경될 때 |
| Round Reconstruction | `2013-01-practical-01.md` through `2026-01-practical-31.md` | 회차별 문항·답안·출처·확신도 | 기출 복원 원천이 보강되거나 문항 오류가 발견될 때 |
| Reference Registry | `reference-source-index.md`, `exam-criteria-and-reference-catalog.md`, `reference-patching-review.md` | 참고문서 원천, 출제기준, 패칭 검토 | 공식 URL, 버전, 패칭 상태, 참고문서 후보 상태가 바뀔 때 |
| Classification | `subject-type-classification-detail.md`, `subject-type-matrix.md`, `subject-type-cross-verify-report.md` | 과목/문제유형 분류와 검증 | 문항 분류 기준 또는 분류값이 바뀔 때 |
| Mapping | `item-reference-map.md` | 문항과 출제기준·참고문서 연결 | 기출 문항과 근거문서 연결이 바뀔 때 |
| Analysis | `frequency-analysis.md`, `recurrence-analysis.md`, `pattern-analysis.md`, `significance-review.md`, `session-slot-pattern-analysis.md`, `analysis-cross-verify-report.md` | 빈도, 반복, 패턴, 유의미성, 회차 슬롯 분석 | 분류·매핑 입력 또는 분석 해석이 바뀔 때 |
| Verification | `pdf-source-cross-verify-report.md`, `prompt-completeness-cross-verify-report.md`, `round-file-pdf-exhaustive-cross-verify-report.md`, `prediction-validation-report.md` | 원천, PDF, 지시문, 예측 품질의 report-only 검증 | 원문 대조, 누락, 과압축, 예측 검증 상태가 바뀔 때 |
| Study Output | `study-strategy-2026-02.md`, `integrated-study-guide-2026-02.md`, `hands-on-integrated-study-roadmap-2026-02.md`, `hands-on-lab-feasibility-deep-research.md`, `learning-priority-and-prediction-validity-2026-02.md`, `privacy-safety-ismsp-cheatsheet-2026-07.md` | 학습 전략, 통합 가이드, 실습 로드맵, 암기표 | 시험 대비 전략, 독립 실습 계획, 법령·ISMS-P 학습표가 바뀔 때 |
| Prediction | `predicted-practical-questions-2026-02.md` | 예상문제와 채점 포인트 | 예상문제 세트가 바뀔 때 |

### 변경 절차

| 변경 유형 | 원자적 시작점 | 파생 갱신 | 검증 |
|---|---|---|---|
| 회차 문항 수정 | 해당 `*-practical-*.md` | `subject-type-classification-detail.md`, `subject-type-matrix.md`, `item-reference-map.md` | `prompt-completeness-cross-verify-report.md` 또는 신규 검증 메모 |
| 문항 분류 수정 | `subject-type-classification-detail.md` | `subject-type-matrix.md`, `frequency-analysis.md` 계열 | `subject-type-cross-verify-report.md` |
| 참고문서 상태 수정 | `reference-source-index.md` | `exam-criteria-and-reference-catalog.md`, `item-reference-map.md` | `reference-patching-review.md` |
| 매핑 수정 | `item-reference-map.md` | `frequency-analysis.md`, `recurrence-analysis.md`, `pattern-analysis.md`, 학습 산출물 | `analysis-cross-verify-report.md` |
| 분석 해석 수정 | 해당 분석 문서 | `study-strategy-2026-02.md`, `predicted-practical-questions-2026-02.md` | `analysis-cross-verify-report.md`, `prediction-validation-report.md` |
| 학습 전략 수정 | `study-strategy-2026-02.md` | 없음 또는 예상문제 보정 | `prediction-validation-report.md` |
| 예상문제 수정 | `predicted-practical-questions-2026-02.md` | `prediction-validation-report.md` | 문항 수, 근거, confidence 정합 확인 |
| 물리 스캐폴딩 수정 | `document-physical-migration-plan.md` | `index.md`, `document-architecture.md`, 이 문서 | dataset 문서 수, 회차 파일 수, 링크 정합 확인 |

### 물리 스캐폴딩 정책
- 현재 `document-physical-migration-plan.md`의 계획 대상 문서 물리 분리를 완료했다. 이후 새 문서는 같은 책임 그룹에 배치하고, 링크·frontmatter·인덱스 검증을 동반한다.
- 물리 디렉터리 분리는 `document-physical-migration-plan.md`를 기준으로 링크·frontmatter·인덱스 마이그레이션을 동반하는 별도 작업으로만 한다.
- 새 문서는 기존 그룹 중 하나에 먼저 배정한다.
- 새 그룹은 기존 그룹의 변경 이유로 설명할 수 없을 때만 만든다.
- 임시 조사 결과는 permanent 문서로 승격하기 전 `analysis-roadmap-todo.md`에 상태와 폐기 조건을 먼저 남긴다.

### 신규 문서 생성 규칙

| 질문 | 생성 허용 기준 |
|---|---|
| 기존 문서의 책임과 다른가? | 다르면 생성 가능, 같으면 기존 문서 갱신 |
| 원본 사실을 새로 보관하는가? | SSOT가 없을 때만 생성 가능 |
| 파생 분석인가? | 입력 문서와 검증 문서를 명시할 수 있을 때만 생성 가능 |
| 시험 대비 산출물인가? | 시험 회차, 근거 문서, confidence 정책을 명시할 때만 생성 가능 |
| 검증 리포트인가? | 수정 권한 없이 report-only 성격이면 생성 가능 |

### 검증 체크리스트

| 항목 | 기준 |
|---|---|
| 문서 그룹 | 모든 문서가 하나의 주 그룹에 속한다. |
| 변경 시작점 | 수정 이유별 시작 문서가 하나로 결정된다. |
| 역참조 | 회차 파일은 분석·전략·예상문제를 참조하지 않는다. |
| 중복 | 문항 원문, 참고문서 원문, 분석 집계, 예상문제 본문을 다른 문서에 재복제하지 않는다. |
| 보류 근거 | 현재 근거로 수행하지 않기로 한 작업은 `analysis-roadmap-todo.md`에 남긴다. |

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

- `raw/sources/clipping/b5f8e13310da21d9f9b84fe22b371758ffbe0c5fdd0aeef526f83e4c6f1b3206/da85dce163492b152fcd12908d9bb5ecda98daf124694b9c4970784f35718357/manifest.json`
