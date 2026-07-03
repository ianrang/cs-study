# cs-study 다음 세션 진입 — 정보보안기사 실기 참고문서 패칭 및 28~30회 매핑 후속

> 작성: 2026-07-03
> 직전 세션 작업: 소프트웨어 개발보안 가이드 공식 원천을 KISA 첨부로 검증·패칭하고, 최근 28~30회 문항-출제기준-참고문서 1차 매핑을 생성했다.
> 작업 위치: `/Users/ian/dev/personal/001_cs-study` (`docs/infosec-exam-reorg` 브랜치)
> 다음 세션 첫 동작 의무: 본 파일과 `reference-source-index.md`, `item-reference-map.md`, `analysis-roadmap-todo.md`, `subject-type-cross-verify-report.md`를 먼저 읽고 추측 없이 진행.
> commit: 본 handoff는 이번 세션 dev-commit 대상에 포함된다. 재개 시 `git log -1 --oneline`으로 최종 SHA를 확인한다.

---

## 1. 본 세션 한정 정책

- 공식 URL이 확인된 문서만 `patched`로 승격한다.
- 검색에 노출되는 직접 첨부 URL이라도 문서 동일성, 페이지 수, 해시가 맞지 않으면 raw asset으로 사용하지 않는다.
- 원문 PDF 본문은 wiki 문서에 장문 복제하지 않고, raw asset + raw source metadata + source index로 분리한다.
- 문항-참고문서 연결은 `KCA가 특정 문서를 참고했다`고 단정하지 않고, 공개 출제기준·공공 가이드·기출 주제 간 연결성으로만 표현한다.

---

## 2. 잔여 task

### 2-1. MAP-23-27 — 23~27회 문항-근거 매핑 확장
- 근거: `analysis-roadmap-todo.md` 단계 4, `item-reference-map.md` Follow-Up.
- 진입 전 확인: `subject-type-cross-verify-report.md`의 23~27회 MEDIUM/HIGH finding 중 매핑에 영향을 주는 분류 충돌을 먼저 확인한다.
- 작업 범위: 23~27회 문항을 `item-reference-map.md` 스키마로 확장하되, 분류가 흔들리는 문항은 notes에 보수적으로 표시한다.

### 2-2. CLASS-FINDINGS — 과목/유형 분류 finding 보정
- 근거: `subject-type-cross-verify-report.md` HIGH 12건, MEDIUM 14건.
- 진입 전 확인: 회차별 복원 문서와 `subject-type-classification-detail.md`를 함께 읽는다.
- 작업 범위: 명백한 오분류/미분류만 정정하고, source quality low 회차는 복원 원천 보강 task로 분리한다.

### 2-3. REF-OWASP-CWE — OWASP/CVE/CWE 계열 참고문서 패칭 필요성 결정
- 근거: `reference-source-index.md` Next Patch Targets, `analysis-roadmap-todo.md` 우선순위.
- 진입 전 확인: 23~30회 중 OWASP, CVE, CWE, CVSS 직접 언급 또는 고확신 개념 연결 문항을 집계한다.
- 작업 범위: 공식 원천 후보를 확정한 뒤 필요 시 별도 raw asset/source metadata로 패칭한다.

### 2-4. LOW-CONFIDENCE-ROUNDS — 저신뢰 회차 보강
- 근거: `subject-type-cross-verify-report.md` source_quality_low finding.
- 진입 전 확인: 11회, 15회, 19~22회 원천 품질과 암호화 PDF 접근 가능성을 확인한다.
- 작업 범위: 대체 원천 확보 또는 confidence 유지 정책을 명시한다.

---

## 3. 본 세션 변경 핵심

### 3-1. 신규 raw 자산

| 파일 | 역할 |
|---|---|
| `raw/assets/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.pdf` | KISA 소프트웨어 개발보안 가이드 공식 첨부 PDF |

### 3-2. 신규 raw source metadata

| 파일 | 역할 |
|---|---|
| `raw/sources/web/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.md` | KISA 공식 URL, 다운로드 패턴, 해시, 텍스트 추출 상태, 행안부 첨부 혼동 주의사항 |

### 3-3. 신규 wiki 문서

| 파일 | 역할 |
|---|---|
| `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/item-reference-map.md` | 28~30회 54개 문항의 KCA 실기 세부항목 + 참고문서 ref_id 1차 매핑 |

### 3-4. 갱신된 wiki 문서

| 파일 | 변경 의미 |
|---|---|
| `reference-source-index.md` | `REF-SECURE-CODING-GUIDE`를 `patched`로 승격하고 KISA URL/asset/source를 등록 |
| `reference-patching-review.md` | 소프트웨어 개발보안 가이드 검증 항목 추가, 기존 HIGH finding 해소 |
| `analysis-roadmap-todo.md` | 참고문서 패칭 단계 3-0/3-1/3-2 완료, 문항-근거 연결 단계 진행 중으로 갱신 |
| `exam-criteria-and-reference-catalog.md` | 소프트웨어 개발보안 가이드 상태를 원문 패칭 완료로 갱신 |
| `wiki/log.md` | 시큐어코딩 패칭 및 28~30회 매핑 로그 append |

### 3-5. 검증 증거

| 계층 | 상태 | 근거 |
|---|---|---|
| 1. 명제 일관성 | OK | source index, review, roadmap, catalog의 `REF-SECURE-CODING-GUIDE` 상태 대조 |
| 2. 정적 분석 | OK | `python3 ../../../scripts/lint.py` → `HIGH=0, MEDIUM=0` |
| 3. 단위 | N/A | 문서/raw asset 작업, 단위 테스트 없음 |
| 4. mock 통합 | N/A | 문서/raw asset 작업 |
| 5a. 자동화 영역 | OK | `curl`, `pdfinfo`, `shasum -a 256`, `cmp -s`, `pdftotext`, `rg`, lint 수행 |
| 5b. 사용자 필수 영역 | N/A | 주관 UI/인터랙티브 검증 없음 |

검증한 해시:
- KISA 소프트웨어 개발보안 가이드: `fcd8c4343f5f3ec0d7a1beda7ba4a6f86b67f5d6267664241fb66f6710ca0407`
- 동일 해시 확인 대상: KISA 다운로드본, `/Users/ian/Downloads/소프트웨어_개발보안_가이드(2021.12.29) (1).pdf`, repo raw asset.

---

## 4. 진입 전 필수 read

| 우선순위 | 파일 | 역할 |
|---:|---|---|
| 1 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/reference-source-index.md` | 참고문서 원천 SSOT |
| 2 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/item-reference-map.md` | 28~30회 문항-근거 매핑 SSOT |
| 3 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/analysis-roadmap-todo.md` | 단계별 TODO |
| 4 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-cross-verify-report.md` | 분류/원천 품질 finding |
| 5 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/document-architecture.md` | 문서 구조와 참조 방향 규칙 |

---

## 5. 잔존 함정·회귀

### 5-1. 표준 프로젝트 todo 부재
- 발생 사례: `todo.md`, `.manage/todo/todo.md`, `docs/TODO.md`가 없어 `dev-todo-update`는 표준 todo 갱신을 수행할 수 없다.
- 회피 방법: 이 작업 흐름에서는 `analysis-roadmap-todo.md`를 도메인 로드맵 TODO로 사용하되, 일반 harness todo처럼 DAG row가 파싱된다고 가정하지 않는다.

### 5-2. 무관한 dirty worktree
- 발생 사례: 세션 시작 전부터 대량 삭제/수정 및 untracked 파일이 존재했다.
- 회피 방법: 이번 커밋에는 본 세션 변경 파일만 staging한다. 기존 `AGENTS.md`, `_meta`, `scripts/lint.py`, `wiki/index.md`, `round-1/`, `tests/`, 대량 삭제 파일은 포함하지 않는다.

### 5-3. 행안부 직접 첨부 URL 혼동
- 발생 사례: 검색 결과의 `https://www.mois.go.kr/cmm/fms/FileDown.do?atchFileId=FILE_000000000046958&fileSn=0`은 다운로드 가능하지만 8쪽짜리 2013 PDF이며, 이번 2021.12.29 KISA PDF와 다르다.
- 회피 방법: 소프트웨어 개발보안 가이드 raw asset은 KISA `postSeq=5`, `attachSeq=1` 다운로드 패턴만 사용한다.

### 5-4. 매핑 confidence 과신 금지
- 발생 사례: 28~30회 매핑은 고신뢰 복원본 기반이나 공식 실기 원문이 공개된 것은 아니다.
- 회피 방법: `item-reference-map.md`의 confidence와 notes를 유지하고, medium 행은 OWASP/CWE/CVE/모바일/법령 원천 보강 후 승격한다.

---

## 6. 본 세션에 미진입한 안건

- 23~27회 문항-근거 매핑 확장.
- `subject-type-cross-verify-report.md` HIGH/MEDIUM finding 정정.
- OWASP/CVE/CWE 계열 공식 원천 패칭 여부 결정.
- 저신뢰 회차 보강.
- 빈도·재출제 분석 및 2026년 2회 대비 학습전략 작성.
