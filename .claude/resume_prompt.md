# cs-study 다음 세션 진입 — 정보보안기사 실기 참고문서 패칭 후속

> 작성: 2026-07-03
> 직전 세션 작업: 정보보안기사 실기 기출 분석 로드맵에 필요한 공식 참고문서 원문을 raw/source index 구조로 패칭하고 검증했다.
> 작업 위치: `/Users/ian/dev/personal/001_cs-study` (`docs/infosec-exam-reorg` 브랜치)
> 다음 세션 첫 동작 의무: 본 파일과 `reference-source-index.md`, `analysis-roadmap-todo.md`를 먼저 읽고 추측 없이 진행.
> commit: this handoff is included in the latest commit for this session; check `git log -1 --oneline`

---

## 1. 본 세션 한정 정책

- 공식 URL이 확인된 문서만 `patched`로 승격했다.
- 공식 원천이 확정되지 않은 문서는 `pending`으로 남기고 raw asset을 저장하지 않았다.
- 원문 PDF 본문은 wiki 문서에 장문 복제하지 않고, raw asset + raw source metadata + source index로 분리했다.

---

## 2. 잔여 task

### 2-1. REF-SECURE-CODING-GUIDE — 소프트웨어 개발보안 가이드 공식 원천 확인
- 근거: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/reference-source-index.md`
- 현재 상태: `pending official URL`
- 진입 전 확인: KISA/행정안전부 등 공식 게시글과 첨부 다운로드 경로를 먼저 확정한다.
- 작업 범위: 공식 URL 확인 → raw asset 저장 → raw source metadata 작성 → `reference-source-index.md`와 `reference-patching-review.md` 갱신 → lint.

### 2-2. 기출 문항과 참고문서 연결
- 근거: `analysis-roadmap-todo.md` 단계 4, 4-1, 4-2
- 진입 전 확인: source index의 `patched` 문서만 high-confidence 연결에 사용한다.
- 작업 범위: 각 문항에 KCA 출제기준 항목과 공식 참고문서 ref_id를 연결한다.

---

## 3. 본 세션 변경 핵심

### 3-1. 신규 raw 자산

| 파일 | 역할 |
|---|---|
| `raw/assets/information-security-exam-references/kisa-ciip-technical-vulnerability-assessment-guide-2026.pdf` | KISA 주요정보통신기반시설 기술적 취약점 상세가이드 원문 |
| `raw/assets/information-security-exam-references/kisa-ismsp-criteria-guide-2023-11.pdf` | KISA ISMS-P 인증기준 안내서 원문 |

### 3-2. 신규 raw source metadata

| 파일 | 역할 |
|---|---|
| `raw/sources/web/information-security-exam-references/kisa-ciip-technical-vulnerability-assessment-guide-2026.md` | 기반시설 상세가이드 공식 URL, 다운로드 패턴, 해시, 추출 상태 |
| `raw/sources/web/information-security-exam-references/kisa-ismsp-criteria-guide-2023-11.md` | ISMS-P 안내서 공식 URL, 다운로드 패턴, 해시, 추출 상태 |

### 3-3. 갱신된 wiki 문서

| 파일 | 변경 의미 |
|---|---|
| `reference-source-index.md` | KCA/PIPC/ISMS-P/기반시설 원천 패칭 상태를 SSOT로 정리하고 시큐어코딩만 pending으로 남김 |
| `reference-patching-review.md` | 공식성, 해시, 텍스트 추출, fail-closed 판단을 교차검증 결과로 기록 |
| `exam-criteria-and-reference-catalog.md` | 파생 카탈로그의 문서 상태를 패칭 결과와 맞춤 |
| `analysis-roadmap-todo.md` | 단계 3-0/3-1/3-2를 진행 중으로 갱신하고 남은 조건을 명시 |

### 3-4. 검증 증거

| 계층 | 상태 | 근거 |
|---|---|---|
| 1. 명제 일관성 | OK | `reference-source-index.md`와 `reference-patching-review.md`의 patched/pending 상태 대조 |
| 2. 정적 분석 | OK | `python3 ../../../scripts/lint.py` → `HIGH=0, MEDIUM=0` |
| 3. 단위 | N/A | 문서/raw asset 작업, 단위 테스트 없음 |
| 4. mock 통합 | N/A | 문서/raw asset 작업 |
| 5a. 자동화 영역 | OK | `curl`, `file`, `shasum -a 256`, `pdftotext`, `rg`, lint 수행 |
| 5b. 사용자 필수 영역 | N/A | 주관 UI/인터랙티브 검증 없음 |

검증한 해시:
- KISA 기반시설 상세가이드: `44fe393981b244147be6af7423d99dc15633c089fad0bcb296cbe2371dde812d`
- KISA ISMS-P 안내서: `6df06f8ddf007094952ec714341bc466266a4fc5459470b1744495725049e599`
- PIPC 개인정보 영향평가 안내서: `5e4746fa960ffa305cd112881c6282e3bd7ca00eb831627d384b8ed87a261c42`
- PIPC 안전성 확보조치 안내서: `dcc29db0bc847049175933e08ea537b1dfed22b39d0bc97164b9ddb6fb90413c`

---

## 4. 진입 전 필수 read

| 우선순위 | 파일 | 역할 |
|---:|---|---|
| 1 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/reference-source-index.md` | 참고문서 원천 SSOT |
| 2 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/reference-patching-review.md` | 패칭 교차검증 결과 |
| 3 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/analysis-roadmap-todo.md` | 단계별 TODO |
| 4 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/document-architecture.md` | 문서 구조와 참조 방향 규칙 |

---

## 5. 잔존 함정·회귀

### 5-1. 표준 프로젝트 todo 부재
- 발생 사례: `todo.md`, `.manage/todo/todo.md`, `docs/TODO.md`가 없어 `check-sot-drift`가 todo SoT를 찾지 못했다.
- 회피 방법: 이 작업 흐름에서는 `analysis-roadmap-todo.md`를 도메인 로드맵 TODO로 사용하되, 일반 harness todo처럼 DAG row가 파싱된다고 가정하지 않는다.

### 5-2. 무관한 dirty worktree
- 발생 사례: `check-sot-drift --mode completion`이 기존 untracked `tests/test_wiki_ingest_schema.py` 때문에 C2 BLOCK을 냈다.
- 회피 방법: 이번 참고문서 패칭 커밋에는 해당 파일과 기존 대량 삭제/수정 상태를 포함하지 않는다.

### 5-3. ISMS-P 전용 도메인 DNS
- 발생 사례: `isms.kisa.or.kr` DNS resolution 실패가 있었지만, KISA 공식 사이트의 안내서 첨부로 동일 계열 공식 원문을 패칭했다.
- 회피 방법: 전용 도메인 복구 시 첨부 PDF 동일성 비교를 후속으로 수행한다.

---

## 6. 본 세션에 미진입한 안건

- 소프트웨어 개발보안 가이드 공식 원천 패칭.
- 문항-출제기준-참고문서 연결 테이블 작성.
- 참고문서별 기출 빈도/재출제 분석.
