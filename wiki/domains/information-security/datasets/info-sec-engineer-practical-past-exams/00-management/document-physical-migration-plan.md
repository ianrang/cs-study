---
title: 정보보안기사 실기 문서 물리 스캐폴딩 마이그레이션 계획
page_type: dataset
tags:
- information-security
- certification
- documentation-architecture
- migration-plan
date_created: '2026-07-09'
date_updated: '2026-07-09'
source_paths:
- raw/sources/clipping/19d50f60525ef98a49c133733fee8428eafd17794ed4e6e10f771716edb58049/1bcc5441f989c67a1decd166cf1b6ef227131caf4441d28222ed694a162602aa/manifest.json
summary: 정보보안기사 실기 기출 분석 문서군을 책임별 폴더로 분리하기 위한 단계별 물리 마이그레이션 계획과 파일별 목적지 매핑을 정의한다.
---

## Overview





# 정보보안기사 실기 문서 물리 스캐폴딩 마이그레이션 계획

### 목적
현재 `datasets/info-sec-engineer-practical-past-exams/`에는 회차 복원, 문서 운영, 참고문서, 분류, 매핑, 분석, 검증, 학습, 예측 산출물이 같은 디렉터리에 있다. 이 계획은 기출문제 유실과 링크 파손을 방지하면서 문서의 책임과 변경 이유에 맞게 물리 폴더를 분리하기 위한 실행 순서와 검증 기준을 고정한다.

이 문서는 이동 계획과 단계별 진행 상태를 함께 관리한다. 실제 파일 이동은 이 문서의 파일별 목적지 매핑과 검증 절차를 기준으로 작은 배치 단위로 수행한다.

### 이동 불변 조건
- 기출 회차 파일은 31개를 유지한다.
- 전체 dataset 문서 수는 60개를 유지한다. 이는 기존 59개 문서에 이 계획 문서 1개를 더한 수다.
- `*-practical-*.md` 파일명은 바꾸지 않는다.
- `index.md`는 dataset 루트 진입점으로 유지한다.
- 회차 파일 본문은 이동 단계에서 수정하지 않는다. 링크와 `source_paths` 보정만 별도 단계에서 수행한다.
- 실행형 실습 자산은 독립 경계이므로 `datasets/` 내부로 합치지 않는다.
- `drafts/udemy/` 문서는 기출 분석 산출물로 확정하기 전까지 회차·분석·레퍼런스 문서군과 섞지 않는다.
- `.sandbox/` 생성물은 이동 대상이 아니며 git 추적 대상도 아니다.

### 목표 디렉터리

| 디렉터리 | 책임 | 포함 기준 | 제외 기준 |
|---|---|---|---|
| dataset root | 전체 진입점 | `index.md` | 세부 분석 본문 |
| `00-management/` | 문서 운영 규칙, 작업 상태, 물리 이동 계획 | 아키텍처, 스캐폴드, 로드맵, 마이그레이션 계획 | 분석 본문, 기출 원문 |
| `01-rounds/` | 회차별 기출 복원 | `YYYY-NN-practical-XX.md` | 분류·해설·예측 통합 문서 |
| `02-references/` | 공식/후보 레퍼런스와 출제기준 메타데이터 | 출처 색인, 기준 카탈로그, 패칭 검토 | 문항별 전체 매핑 |
| `03-classification/` | 과목·유형 분류와 분류 검증 | 분류 상세, 매트릭스, 분류 cross-verify | 레퍼런스 연결, 예측 |
| `04-mapping/` | 문항-기준-레퍼런스 연결 | item-reference map | 원문 전체 복제, 빈도 분석 |
| `05-analysis/` | 빈도·반복·패턴·유의미성 분석 | 분석 결과와 분석 검증 | 학습 실행표, 예상문제 |
| `06-verification/` | 원천·PDF·프롬프트·예측 검증 리포트 | report-only 검증 문서 | 원문 보정의 SSOT |
| `07-study/` | 실제 학습 전략과 암기·실습 로드맵 | 전략, 통합 가이드, 치트시트, 실습 타당성 | 기출 회차 원문 |
| `08-prediction/` | 예상문제와 예측 산출물 | 예상문제 세트 | 확정 기출로 표현되는 문서 |
| `archive/` | 폐기·대체 문서 | superseded 문서만 | 활성 SSOT 문서 |

### 단계별 실행 순서

| 단계 | 작업 | 성공 기준 | 중단 조건 |
|---|---|---|---|
| 1 | 이 계획 문서 생성 및 인덱스 연결 | dataset 문서 60개와 회차 31개가 문서화된다. | 현재 파일 수와 계획 파일 수가 맞지 않는다. |
| 2 | `00-management/`만 이동 | 관리 문서가 모두 이동되고 새 위치에서 서로 링크된다. | `index.md`에서 관리 문서 링크가 깨진다. |
| 3 | `02-references/`, `03-classification/`, `04-mapping/` 이동 | 레퍼런스-분류-매핑 문서가 새 위치에서 단방향 참조를 유지한다. | `item-reference-map.md`의 참조 문서 링크가 깨진다. |
| 4 | `05-analysis/`, `06-verification/` 이동 | 분석과 검증 문서가 분리되고 기존 분석 입력 문서를 찾을 수 있다. | 분석 문서가 검증 리포트의 본문을 복제해야만 읽히는 상태가 된다. |
| 5 | `07-study/`, `08-prediction/` 이동 | 학습 산출물과 예측 산출물이 분리된다. | 예상문제가 학습 문서나 회차 문서에 중복 저장된다. |
| 6 | `01-rounds/` 회차 파일 이동 | 회차 파일 31개가 모두 존재하고 item count 표가 유지된다. | 회차 파일 수가 31개가 아니거나 파일명이 바뀐다. |
| 7 | 최종 링크·frontmatter 검증 | 이전 경로 잔여 참조가 의도된 호환 링크 외에는 없다. | 깨진 링크나 누락 파일이 발견된다. |

### 진행 상태

| 단계 | 상태 | 근거 |
|---|---|---|
| 1 | done | `document-physical-migration-plan.md`를 생성하고 `index.md`, `document-architecture.md`, `document-management-scaffold.md`에 연결했다. |
| 2 | done | `analysis-roadmap-todo.md`, `document-architecture.md`, `document-management-scaffold.md`, `document-physical-migration-plan.md`를 `00-management/`로 이동했다. |
| 3 | done | `reference-source-index.md`, `exam-criteria-and-reference-catalog.md`, `reference-patching-review.md`, `subject-type-classification-detail.md`, `subject-type-cross-verify-report.md`, `subject-type-matrix.md`, `item-reference-map.md`를 목적 폴더로 이동했다. |
| 4 | done | 분석 문서 6개와 검증 문서 4개를 `05-analysis/`, `06-verification/`으로 이동했다. |
| 5 | done | 학습 문서 6개를 `07-study/`로, 예상문제 문서 1개를 `08-prediction/`으로 이동했다. |
| 6 | done | 회차 파일 31개를 `01-rounds/`로 이동했고 파일명은 유지했다. |
| 7 | done | dataset 문서 수 60개, 회차 파일 31개, 상대 Markdown 링크 0건 오류, dataset 내부 `source_paths` 0건 오류를 확인했다. |

### 파일별 목적지 매핑

### dataset root
| 현재 파일 | 목표 파일 |
|---|---|
| `index.md` | `index.md` |

### 00-management
| 현재 파일 | 목표 파일 |
|---|---|
| `analysis-roadmap-todo.md` | `00-management/analysis-roadmap-todo.md` |
| `document-architecture.md` | `00-management/document-architecture.md` |
| `document-management-scaffold.md` | `00-management/document-management-scaffold.md` |
| `document-physical-migration-plan.md` | `00-management/document-physical-migration-plan.md` |

### 01-rounds
| 현재 파일 | 목표 파일 |
|---|---|
| `2013-01-practical-01.md` | `01-rounds/2013-01-practical-01.md` |
| `2013-02-practical-02.md` | `01-rounds/2013-02-practical-02.md` |
| `2014-01-practical-03.md` | `01-rounds/2014-01-practical-03.md` |
| `2014-02-practical-04.md` | `01-rounds/2014-02-practical-04.md` |
| `2015-01-practical-05.md` | `01-rounds/2015-01-practical-05.md` |
| `2015-02-practical-06.md` | `01-rounds/2015-02-practical-06.md` |
| `2016-01-practical-07.md` | `01-rounds/2016-01-practical-07.md` |
| `2016-02-practical-08.md` | `01-rounds/2016-02-practical-08.md` |
| `2017-01-practical-09.md` | `01-rounds/2017-01-practical-09.md` |
| `2017-02-practical-10.md` | `01-rounds/2017-02-practical-10.md` |
| `2018-01-practical-11.md` | `01-rounds/2018-01-practical-11.md` |
| `2018-02-practical-12.md` | `01-rounds/2018-02-practical-12.md` |
| `2019-01-practical-13.md` | `01-rounds/2019-01-practical-13.md` |
| `2019-02-practical-14.md` | `01-rounds/2019-02-practical-14.md` |
| `2020-01-practical-15.md` | `01-rounds/2020-01-practical-15.md` |
| `2020-02-practical-16.md` | `01-rounds/2020-02-practical-16.md` |
| `2021-01-practical-17.md` | `01-rounds/2021-01-practical-17.md` |
| `2021-02-practical-18.md` | `01-rounds/2021-02-practical-18.md` |
| `2022-01-practical-19.md` | `01-rounds/2022-01-practical-19.md` |
| `2022-02-practical-20.md` | `01-rounds/2022-02-practical-20.md` |
| `2022-04-practical-21.md` | `01-rounds/2022-04-practical-21.md` |
| `2023-01-practical-22.md` | `01-rounds/2023-01-practical-22.md` |
| `2023-02-practical-23.md` | `01-rounds/2023-02-practical-23.md` |
| `2023-04-practical-24.md` | `01-rounds/2023-04-practical-24.md` |
| `2024-01-practical-25.md` | `01-rounds/2024-01-practical-25.md` |
| `2024-02-practical-26.md` | `01-rounds/2024-02-practical-26.md` |
| `2024-04-practical-27.md` | `01-rounds/2024-04-practical-27.md` |
| `2025-01-practical-28.md` | `01-rounds/2025-01-practical-28.md` |
| `2025-02-practical-29.md` | `01-rounds/2025-02-practical-29.md` |
| `2025-04-practical-30.md` | `01-rounds/2025-04-practical-30.md` |
| `2026-01-practical-31.md` | `01-rounds/2026-01-practical-31.md` |

### 02-references
| 현재 파일 | 목표 파일 |
|---|---|
| `exam-criteria-and-reference-catalog.md` | `02-references/exam-criteria-and-reference-catalog.md` |
| `reference-patching-review.md` | `02-references/reference-patching-review.md` |
| `reference-source-index.md` | `02-references/reference-source-index.md` |

### 03-classification
| 현재 파일 | 목표 파일 |
|---|---|
| `subject-type-classification-detail.md` | `03-classification/subject-type-classification-detail.md` |
| `subject-type-cross-verify-report.md` | `03-classification/subject-type-cross-verify-report.md` |
| `subject-type-matrix.md` | `03-classification/subject-type-matrix.md` |

### 04-mapping
| 현재 파일 | 목표 파일 |
|---|---|
| `item-reference-map.md` | `04-mapping/item-reference-map.md` |

### 05-analysis
| 현재 파일 | 목표 파일 |
|---|---|
| `analysis-cross-verify-report.md` | `05-analysis/analysis-cross-verify-report.md` |
| `frequency-analysis.md` | `05-analysis/frequency-analysis.md` |
| `pattern-analysis.md` | `05-analysis/pattern-analysis.md` |
| `recurrence-analysis.md` | `05-analysis/recurrence-analysis.md` |
| `session-slot-pattern-analysis.md` | `05-analysis/session-slot-pattern-analysis.md` |
| `significance-review.md` | `05-analysis/significance-review.md` |

### 06-verification
| 현재 파일 | 목표 파일 |
|---|---|
| `pdf-source-cross-verify-report.md` | `06-verification/pdf-source-cross-verify-report.md` |
| `prompt-completeness-cross-verify-report.md` | `06-verification/prompt-completeness-cross-verify-report.md` |
| `round-file-pdf-exhaustive-cross-verify-report.md` | `06-verification/round-file-pdf-exhaustive-cross-verify-report.md` |
| `prediction-validation-report.md` | `06-verification/prediction-validation-report.md` |

### 07-study
| 현재 파일 | 목표 파일 |
|---|---|
| `hands-on-integrated-study-roadmap-2026-02.md` | `07-study/hands-on-integrated-study-roadmap-2026-02.md` |
| `hands-on-lab-feasibility-deep-research.md` | `07-study/hands-on-lab-feasibility-deep-research.md` |
| `integrated-study-guide-2026-02.md` | `07-study/integrated-study-guide-2026-02.md` |
| `learning-priority-and-prediction-validity-2026-02.md` | `07-study/learning-priority-and-prediction-validity-2026-02.md` |
| `privacy-safety-ismsp-cheatsheet-2026-07.md` | `07-study/privacy-safety-ismsp-cheatsheet-2026-07.md` |
| `study-strategy-2026-02.md` | `07-study/study-strategy-2026-02.md` |

### 08-prediction
| 현재 파일 | 목표 파일 |
|---|---|
| `predicted-practical-questions-2026-02.md` | `08-prediction/predicted-practical-questions-2026-02.md` |

### 별도 유지 대상

| 경로 | 처리 | 이유 |
|---|---|---|
| `labs/` | 현재 구조 유지 | 독립 실행 가능한 실습 세트이며 `datasets/`와 책임이 다르다. |
| `drafts/udemy/` | draft 격리 완료 | 강의 기반 학습 노트로 보관하고, 기출 복원·분석 산출물로 쓰려면 별도 검증 후 승격한다. |

### 검증 명령

이동 전후 다음 조건을 확인한다.

```bash
rg --files datasets/info-sec-engineer-practical-past-exams | wc -l
rg --files datasets/info-sec-engineer-practical-past-exams | rg '/[0-9]{4}-[0-9]{2}-practical-[0-9]{2}\.md$' | wc -l
rg -P ']\((?!https?://|/)' datasets/info-sec-engineer-practical-past-exams
git diff --check
```

실습 실행물의 경로 변경 검증은 해당 실행 프로젝트가 소유하며 dataset migration 검증과 결합하지 않는다.

### 완료 기준
- dataset 문서 수가 계획 대상 수와 일치한다.
- 회차 파일 31개가 모두 존재한다.
- `index.md`에서 모든 문서 진입점이 새 경로를 가리킨다.
- `document-architecture.md`와 `document-management-scaffold.md`가 새 디렉터리 구조를 설명한다.
- 회차 파일 본문은 이동 전후 내용 변경이 없어야 한다.
- `labs/` 실습 세트는 그대로 실행 가능해야 한다.

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

- `raw/sources/clipping/19d50f60525ef98a49c133733fee8428eafd17794ed4e6e10f771716edb58049/1bcc5441f989c67a1decd166cf1b6ef227131caf4441d28222ed694a162602aa/manifest.json`
