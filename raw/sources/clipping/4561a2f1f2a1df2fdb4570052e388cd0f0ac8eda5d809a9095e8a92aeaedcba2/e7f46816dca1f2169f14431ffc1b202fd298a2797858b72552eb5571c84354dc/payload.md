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
date_updated: 2026-07-09
source_paths:
  - "../02-references/reference-patching-review.md"
  - "../02-references/reference-source-index.md"
  - "document-architecture.md"
  - "document-management-scaffold.md"
  - "../02-references/exam-criteria-and-reference-catalog.md"
  - "../04-mapping/item-reference-map.md"
  - "../03-classification/subject-type-matrix.md"
  - "../03-classification/subject-type-classification-detail.md"
  - "../03-classification/subject-type-cross-verify-report.md"
  - "../06-verification/prompt-completeness-cross-verify-report.md"
  - "../05-analysis/frequency-analysis.md"
  - "../05-analysis/recurrence-analysis.md"
  - "../05-analysis/pattern-analysis.md"
  - "../05-analysis/significance-review.md"
  - "../05-analysis/analysis-cross-verify-report.md"
  - "../05-analysis/session-slot-pattern-analysis.md"
  - "../07-study/study-strategy-2026-02.md"
  - "../08-prediction/predicted-practical-questions-2026-02.md"
  - "../06-verification/prediction-validation-report.md"
  - "../06-verification/pdf-source-cross-verify-report.md"
source_count: 20
provenance: inferred
summary: "정보보안기사 실기 합격 전략을 위해 기출 복원부터 예상문제 생성까지 단계별 작업을 추적하고, 검증된 복원 원천이 없는 회차는 생성하지 않도록 관리한다."
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
| 0-1 | 문서 관리 스캐폴딩 고정 | 완료 | `document-management-scaffold.md` | 문서 그룹, 진입점, 변경 시작점, 물리 이동 보류 기준 정의 |
| 1 | 기출 문제 복원 | 진행 중 | 회차별 `*-practical-*.md` | 각 회차 문항 원문/답/출처/확신도 기록 |
| 1-1 | PDF 편집본 원천 대조 및 대체 원천 확보 | 완료 | `pdf-source-cross-verify-report.md` | 1~28회 thodi-lab/blog-source PDF 편집본 열람·텍스트 추출·교차대조 기록 |
| 1-2 | 저신뢰 회차 보강 | 진행 중 | 보강된 회차 파일 | Naver 카테고리에서 확인 가능한 13~29회 보강 완료, 1~12회는 Information Security Tistory 직접 복원글로 보강 완료 |
| 1-3 | 문항 설명 완전성 교차검증 | 완료 | `prompt-completeness-cross-verify-report.md` | 설명 누락·과압축 후보 48건 스캔 후 회차 파일 보강, 사용자 제공 원천 이미지로 known-limited 2건 해소 |
| 1-4 | 32회 verified restoration source 확보 | 차단 | `prompt-completeness-cross-verify-report.md` | 31회는 사용자 제공 문제·정답 표로 추가 완료. 32회는 실제 복원 원천 확인 전까지 회차 파일 생성 금지; 예상문제·대비요약·후기는 제외 |
| 2 | 기출 문제 분류 | 진행 중 | `subject-type-classification-detail.md`, `subject-type-matrix.md` | 5개 과목 + 단답형/서술형/실무형 분류와 근거 기록 |
| 2-1 | 분류 교차검증 | 진행 중 | `subject-type-cross-verify-report.md` | 미분류 HIGH finding 해소, 남은 source_quality/keyword conflict 검토 |
| 3 | 출제기준 및 참고문서 카탈로그 작성 | 완료 | `exam-criteria-and-reference-catalog.md` | KCA 출제기준, 법령/고시/가이드 후보 상태 분리 |
| 3-0 | 참고문서 패칭 범위 확정 | 완료 | `reference-source-index.md` | 필수 1차 문서 중 KCA/PIPC/ISMS-P/기반시설/시큐어코딩 패칭 완료 |
| 3-1 | 참고문서 원문 URL/파일 확보 | 완료 | `reference-source-index.md` | 각 문서별 공식 URL, 버전, 발행기관, 적용일 기록 |
| 3-2 | 참고문서 텍스트 추출 | 완료 | raw asset + extraction status | 패칭 완료 PDF는 `pdftotext` 성공 |
| 3-3 | 보조 원천 raw/source 선별 원칙 확정 | 완료 | `reference-source-index.md` | `official page confirmed` 보조 원천은 대량 패칭하지 않고, 직접 1차 원천·핵심 반복 근거·외부 삭제 위험이 확인된 경우에만 선별 패칭 |
| 4 | 문항-출제기준-참고문서 연결 | 진행 중 | `item-reference-map.md` | 23~30회 144개 문항 1차 매핑 완료, OWASP/CVE/CWE/CVSS/MITRE/모바일 공식 페이지와 IETF/NIST/GNU/법령 보조 원천, 기존 PIPC 원천 재검토 반영 후 medium 27개 → 4개 |
| 4-1 | 직접 연결 문항 식별 | 진행 중 | direct-reference table | 23~30회에서 ISMS-P, 시큐어코딩, 기반시설 상세가이드 등 직접 연결 후보 반영 |
| 4-2 | 개념 연결 문항 식별 | 진행 중 | conceptual-reference table | 23~30회 키워드/개념 기준 연결, confidence high/medium 표시 |
| 5 | 기출 패턴과 유형 검토 | 완료 | `pattern-analysis.md` | 과목별·문항유형별·출제기준 항목별 반복 패턴 정리 |
| 5-1 | 빈도 수 분석 | 완료 | `frequency-analysis.md` | 회차별/연도별/과목별/참고문서별 빈도 표 생성 |
| 5-2 | 재출제/변형출제 분석 | 완료 | `recurrence-analysis.md` | 동일 개념 반복, 변형 패턴, 출제 간격 기록 |
| 5-3 | 유의미성 검토 | 완료 | `significance-review.md`, `analysis-cross-verify-report.md` | 단순 빈도와 최근성, 출제기준 중요도, 법령 개정성을 함께 평가하고 수량 교차검증 |
| 5-4 | 연도·회차 슬롯 패턴 검토 | 완료 | `session-slot-pattern-analysis.md` | 1회/2회/4회 슬롯별 과목·개념·전이 패턴 검토, 강한 법칙과 보조 신호 분리 |
| 6 | 학습 전략 수립 | 완료 | `study-strategy-2026-02.md` | 고득점 우선순위, 단기 암기표, 서술형 템플릿, 실무형 대응 전략 |
| 7 | 예상 기출 문제 생성 | 완료 | `predicted-practical-questions-2026-02.md` | 근거 문서/기출 패턴/출제기준 항목을 붙인 예상문제 작성 |
| 7-1 | 예상문제 정답·채점포인트 작성 | 완료 | `predicted-practical-questions-2026-02.md` | 단답형 키워드, 서술형 채점요소, 실무형 절차 답안 포함 |
| 7-2 | 예상문제 검증 | 완료 | `prediction-validation-report.md` | 근거 없는 문제 제거, 문서 연결 누락 보정 |

## 우선순위

| 우선순위 | 작업 | 이유 |
|---:|---|---|
| 1 | `subject-type-cross-verify-report.md`의 잔여 finding 검토 | 1~12회 source_quality finding은 해소됐고, 남은 항목은 KCA 공식 원문 미주장 범위와 일부 keyword conflict 판단임 |
| 2 | 학습 전략 실천 및 오답 보강 | 3주 압축 전략과 예상문제 산출이 완료되어 실제 풀이·오답 회전 단계 |
| 3 | `item-reference-map.md` 유지보수 | 기출과 공식/준공식 문서 연결의 핵심 산출물 |
| 4 | KCA 공식 원천 또는 추가 독립 원천 보강 | 현재 1~28회는 thodi-lab/blog-source PDF 편집본까지 대조했지만 KCA 공식 원문 문구는 미주장 |
| 5 | 남은 medium confidence 행의 보조 원천 보강 | 현재 로컬 reference와 raw/source만으로는 high 승격하지 않는다. 무선랜 세부 표준, Cyber Kill Chain 전용 원천, DB 마스킹 방식명, EAM/IAM 벤더 용어 차이에 직접 대응하는 신규 공식·표준·공공기관·벤더 1차 원천이 확보될 때 재개한다. |
| 6 | 보조 원천 raw/source 선별 패칭 | 현재는 대량 패칭하지 않는다. 학습전략·예상문제의 핵심 반복 근거 또는 외부 삭제 위험이 확인된 원천만 선별 패칭한다. |
| 7 | 문서 물리 디렉터리 분리 | 현재는 same-directory 링크와 `source_paths` 정합을 우선해 보류한다. 필요 시 별도 마이그레이션 작업으로 수행한다. |

## 현재 리스크

| 리스크 | 영향 | 대응 |
|---|---|---|
| 1~28회 PDF 편집본의 비공식성 | KCA 공식 원문 문구로 단정 불가 | thodi-lab/blog-source PDF 편집본과 웹 복원본 기준으로만 표현하고, KCA 공식 원천 확보 시 별도 대조 |
| 1~12회 KCA 공식 원문 미주장 | Information Security Tistory 직접 복원글과 PDF 편집본으로 문항/답안은 보강됐지만 KCA 공식 원문은 확인되지 않음 | KCA 공식 원천 확보 시 원문 문구와 최종 대조 |
| 일부 복원글의 설명 본문 부재 | 공식 지시문 완전 복원이 불가 | 현재 확인된 prompt-completeness known-limited 항목은 사용자 제공 원천 이미지로 해소. 신규 발견 시 `source prompt ... unavailable`로 표시 |
| 일부 회차 웹 복원 품질 낮음 | 빈도 분석 왜곡 | 회차별 confidence 반영, 저신뢰 회차는 통계에서 별도 가중치 |
| 32회 verified source 부재 | 실제 기출 데이터와 예상문제가 섞일 위험 | 복원 원천 확보 전까지 `*-practical-32.md` 생성 금지 |
| 참고문서가 KCA 공식 참고문헌인지 공개 확인 불가 | `KCA가 참고했다`는 단정 불가 | `출제기준/기출과 연결 가능한 참고문서`로 표현 제한 |
| 법령·고시 개정 | 최신 시험 대비 오류 가능 | 문서별 적용일/시행일 필드 유지 |
| 예상문제 과신 | 학습 범위 왜곡 | 예상문제마다 근거와 확신도 표기 |

## 다음 작업 후보

1. `subject-type-cross-verify-report.md` 잔여 MEDIUM finding 판단 또는 저신뢰 회차 원천 보강.
2. KCA 공식 원천 확보 시 1~28회 원문 문구 최종 대조.
3. 32회는 실제 복원 원천이 확인될 때만 회차 파일을 생성하고, AI 예상문제·대비요약·후기는 past-exam evidence에서 제외한다.
4. 예상문제 풀이 결과를 오답표로 회수해 `study-strategy-2026-02.md`의 priority 1~2를 보강한다.
5. 남은 4개 medium confidence 행은 현재 레퍼런스로 보강하지 않는다. 추후 직접 대응 가능한 신규 공식·표준·공공기관·벤더 1차 원천이 생기면 재개한다.
6. 보조 원천 raw/source는 대량 저장하지 않는다. 핵심 반복 근거 또는 외부 삭제 위험이 확인된 원천만 선별 패칭한다.
