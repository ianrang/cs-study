# cs-study 다음 세션 진입 — 정보보안기사 실기 과목 분류 보정 후 23~27회 매핑 확장

> 작성: 2026-07-03
> 직전 세션 작업: 정보보안기사 실기 과목/유형 교차검증 finding을 논리적으로 재검토하고, 명백한 미분류·과목 충돌을 `subject-type-classification-detail.md`와 `subject-type-matrix.md`에 반영했다.
> 작업 위치: `/Users/ian/dev/personal/001_cs-study` (`docs/infosec-exam-reorg` 브랜치)
> 다음 세션 첫 동작 의무: 본 파일과 `analysis-roadmap-todo.md`, `subject-type-cross-verify-report.md`, `subject-type-classification-detail.md`, `subject-type-matrix.md`, `item-reference-map.md`를 먼저 읽고 추측 없이 진행.
> commit: 본 handoff는 이번 세션 dev-commit 대상에 포함된다. 재개 시 `git log -1 --oneline`으로 최종 SHA를 확인한다.

---

## 1. 본 세션 한정 정책

- 분류 보정은 회차별 복원 문항의 visible evidence와 기존 cross-verify finding에 근거한 명백한 항목만 반영한다.
- 원천 품질 문제(`source_quality_low`)와 암호화 PDF 직접 대조 불가(`official_pdf_unverified`)는 분류 표기만으로 해소하지 않는다.
- `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` authored SoT는 수정하지 않는다.
- 문항-참고문서 연결은 `KCA가 특정 문서를 참고했다`고 단정하지 않고, 공개 출제기준·공공 가이드·기출 주제 간 연결성으로만 표현한다.

---

## 2. 잔여 task

### 2-1. MAP-23-27 — 23~27회 문항-근거 매핑 확장
- 근거: `analysis-roadmap-todo.md` 단계 4, `item-reference-map.md` Follow-Up.
- 진입 전 확인: 이번 세션에서 23회 #1/#16, 26회 #4/#16, 27회 #7 분류가 보정됐으므로 해당 subject 기준으로 매핑한다.
- 작업 범위: 23~27회 문항을 `item-reference-map.md` 스키마로 확장하고, 남은 MEDIUM finding이 있는 24회 #4/#8 등은 notes에 보수적으로 표시한다.

### 2-2. CLASS-RESIDUAL — 잔여 과목/유형 finding 판단
- 근거: `subject-type-cross-verify-report.md` active finding은 HIGH 7건, MEDIUM 6건으로 축소됐다.
- 진입 전 확인: HIGH 7건은 대부분 source quality 또는 official PDF verification 한계라 원천 보강 없이는 완료 처리하지 않는다.
- 작업 범위: 12회 #3, 18회 #15/#16, 21회 #2, 24회 #4/#8의 MEDIUM finding을 회차별 복원 문서와 대조해 유지/정정/원천 보강으로 분리한다.

### 2-3. REF-OWASP-CWE — OWASP/CVE/CWE 계열 참고문서 패칭 필요성 결정
- 근거: `reference-source-index.md` Next Patch Targets, `item-reference-map.md` medium confidence 행.
- 진입 전 확인: 23~30회 중 OWASP, CVE, CWE, CVSS 직접 언급 또는 고확신 개념 연결 문항을 집계한다.
- 작업 범위: 공식 원천 후보를 확정한 뒤 필요 시 별도 raw asset/source metadata로 패칭한다.

### 2-4. LOW-CONFIDENCE-ROUNDS — 저신뢰 회차 보강
- 근거: `subject-type-cross-verify-report.md` source_quality_low finding.
- 진입 전 확인: 11회, 15회, 19~22회 원천 품질과 암호화 PDF 접근 가능성을 확인한다.
- 작업 범위: 대체 원천 확보 또는 confidence 유지 정책을 명시한다.

---

## 3. 본 세션 변경 핵심

### 3-1. 갱신된 wiki 문서

| 파일 | 변경 의미 |
|---|---|
| `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md` | 미분류 HIGH 5건과 23~28회 명백한 과목 충돌 일부를 보정 |
| `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md` | 상세 분류 변경에 맞춰 영향 회차 집계 갱신 |
| `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-cross-verify-report.md` | active finding을 HIGH 7건, MEDIUM 6건으로 축소하고 resolved 섹션 추가 |
| `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/analysis-roadmap-todo.md` | 다음 후보를 잔여 finding 판단 및 23~27회 매핑 확장으로 재정렬 |
| `wiki/log.md` | 분류 finding 보정 로그 append |

### 3-2. 주요 보정

| 범위 | 처리 |
|---|---|
| 1회 #2 | 미분류 → 네트워크 보안 |
| 8회 #16/#17 | 미분류 → 정보보안 일반 |
| 9회 #13/#14/#15 | xinetd 설정 연속 행 → 시스템 보안 |
| 14회 #14/#16 | 네트워크 보안으로 정리 |
| 23회 #1/#16 | 시스템 보안, 어플리케이션 보안으로 보정 |
| 26회 #4/#16 | 어플리케이션 보안으로 보정 |
| 27회 #7 | 어플리케이션 보안으로 보정 |
| 28회 #4/#18 | 어플리케이션 보안, 네트워크 보안으로 보정 |

### 3-3. 검증 증거

| 계층 | 상태 | 근거 |
|---|---|---|
| 1. 명제 일관성 | OK | `subject-type-classification-detail.md` 변경과 `subject-type-matrix.md` 영향 회차 재계산 일치 |
| 2. 정적 분석 | OK | `python3 ../../../scripts/lint.py` → `HIGH=0, MEDIUM=0` |
| 3. 단위 | N/A | 문서 분류/집계 작업, 단위 테스트 없음 |
| 4. mock 통합 | N/A | 문서 분류/집계 작업 |
| 5a. 자동화 영역 | OK | 상세표 기반 영향 회차 집계 재계산 스크립트 → `matrix/detail affected-round consistency: OK` |
| 5b. 사용자 필수 영역 | N/A | 주관 UI/인터랙티브 검증 없음 |

---

## 4. 진입 전 필수 read

| 우선순위 | 파일 | 역할 |
|---:|---|---|
| 1 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/analysis-roadmap-todo.md` | 단계별 TODO와 다음 후보 |
| 2 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-cross-verify-report.md` | 잔여 finding과 resolved 목록 |
| 3 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md` | 과목/유형 분류 SSOT |
| 4 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md` | 회차별 파생 집계 |
| 5 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/item-reference-map.md` | 28~30회 문항-근거 매핑 SSOT, 23~27회 확장 대상 |
| 6 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/document-architecture.md` | 문서 구조와 참조 방향 규칙 |

---

## 5. 잔존 함정·회귀

### 5-1. 표준 프로젝트 todo 부재
- 발생 사례: `todo.md`, `.manage/todo/todo.md`, `docs/TODO.md`가 없어 `dev-todo-update`는 표준 todo 갱신을 수행할 수 없다.
- 회피 방법: 이 작업 흐름에서는 `analysis-roadmap-todo.md`를 도메인 로드맵 TODO로 사용하되, 일반 harness todo처럼 DAG row가 파싱된다고 가정하지 않는다.

### 5-2. 무관한 dirty worktree
- 발생 사례: 세션 시작 전부터 대량 삭제/수정 및 untracked 파일이 존재했다.
- 회피 방법: 이번 커밋에는 본 세션 변경 파일만 staging한다. 기존 `AGENTS.md`, `_meta`, `scripts/lint.py`, `wiki/index.md`, `round-1/`, `tests/`, 대량 삭제 파일은 포함하지 않는다.

### 5-3. `source_quality_low`는 분류 보정으로 닫지 않음
- 발생 사례: 11회, 15회, 19~22회는 미분류/제외 비율이 높아 실제 회차 분포 신뢰도가 낮다.
- 회피 방법: source quality finding은 대체 원천 확보 또는 confidence 정책으로 별도 처리한다.

### 5-4. 매핑 confidence 과신 금지
- 발생 사례: 최근 회차 매핑은 고신뢰 복원본 기반이나 공식 실기 원문이 공개된 것은 아니다.
- 회피 방법: `item-reference-map.md`의 confidence와 notes를 유지하고, medium 행은 OWASP/CWE/CVE/모바일/법령 원천 보강 후 승격한다.

---

## 6. 본 세션에 미진입한 안건

- 23~27회 문항-근거 매핑 확장.
- 잔여 MEDIUM finding의 유지/정정/원천 보강 분리.
- OWASP/CVE/CWE 계열 공식 원천 패칭 여부 결정.
- 저신뢰 회차 보강.
- 빈도·재출제 분석 및 2026년 2회 대비 학습전략 작성.
