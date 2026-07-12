# cs-study 다음 세션 진입 — 정보보안 실기 문서·wiki-ingest 기반 교차검증 완료

> 작성: 2026-07-12
> 직전 세션 작업: 정보보안기사 실기 1~5장·네트워크 질의 문서를 검토하고, raw video → wiki synthesis 기반의 PRD·아키텍처·비즈니스 규칙·domain registry·SemanticWritePlan schema·lint를 교차검증해 enum·roll-up·추적성 경계 충돌을 정정했다.
> 작업 위치: `/Users/ian/dev/personal/001_cs-study` (`docs/infosec-exam-reorg` 브랜치)
> 다음 세션 첫 동작 의무: 본 파일과 `docs/wiki-ingest-prd.md`, `docs/wiki-ingest-architecture.md`, `docs/wiki-ingest-business-logic.md`, `docs/wiki-ingest-review.md`, `wiki/domains/information-security/drafts/study/1장 정리.md`~`5장 정리.md`, `wiki/domains/information-security/queries/network-path-functions-and-placement.md`를 먼저 읽고 추측 없이 진행.
> commit: 본 handoff는 이번 세션 dev-commit 대상에 포함된다. 재개 시 `git log -1 --oneline`으로 최종 SHA를 확인한다.

---

## 1. 본 세션 한정 정책

- `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` authored SoT는 수정하지 않는다.
- 이번 변경은 정보보안 실기 1~5장·네트워크 질의 문서와 raw video → wiki synthesis의 설계·schema·lint 기반 작업에 한정한다.
- 예상문제는 기출 기반 학습용 예측이며 실제 출제를 보장하지 않는다.
- 연도·회차 슬롯 패턴은 보조 가중치로만 사용한다. 회차만으로 결정적 예측 규칙을 만들지 않는다.
- 현재 근거만으로 high 승격하지 않기로 한 medium confidence 항목은 추후 직접 대응 가능한 공식·표준·공공기관·벤더 1차 원천이 생길 때 재개한다.
- 보조 원천 raw/source는 대량 저장하지 않는다. 핵심 반복 근거 또는 외부 삭제 위험이 확인된 원천만 선별 패칭한다.
- 문서 물리 디렉터리 분리는 현재 보류한다. same-directory 링크와 `source_paths` 정합을 우선하고, 필요 시 별도 마이그레이션 작업으로 수행한다.
- worktree에는 사용자/이전 작업으로 보이는 대량 `cs/` 삭제와 별도 dataset·`wiki/index.md` 변경이 섞여 있으므로 커밋 시 아래 allowlist만 선별한다.
- 이번 마무리의 commit allowlist는 정보보안 `drafts/study/` 1~5장과 네트워크 질의, `wiki/overview.md`, `AGENTS.md`, `_meta/{frontmatter-spec.md,page-type-spec.md,domains.yaml,wiki-ingest-write-plan.schema.json}`, `docs/{prd.md,wiki-ingest-*.md,adr/0003-domain-registry.md}`, `scripts/lint.py`, `requirements-lint.txt`, `tests/{test_lint.py,test_wiki_ingest_schema.py}`, 본 handoff 파일이다. 나머지 dirty worktree는 staging하지 않는다.
- 정보보안기사 실기 답안은 상위 분류보다 기출의 채점 단위를 우선한다. Slow HTTP Header(Slowloris), Slow HTTP POST(RUDY), Slow HTTP Read를 패킷 단서와 대응별로 구분한다.
- 법규 수치는 2026-07-18 시험 적용일을 기준으로 하며, 이후 시행 법령·고시는 현행 답안으로 섞지 않는다.

---

## 2. 잔여 task

### 2-1. OFFICIAL-PDF-GATE — 공식 PDF 원문 대조
- 근거: 회차 파일 공통 note와 `subject-type-cross-verify-report.md`의 official PDF scope limit.
- 진입 전 확인: 현재 공식 PDF는 비밀번호를 알 수 없어 대조하지 않았다.
- 작업 범위: 비밀번호 또는 독립 원천 확보 시 1~28회 원문 문구를 최종 대조한다.

### 2-2. REMAINING-MEDIUM-REFS — 남은 4개 medium confidence 문항 보조 원천 보강
- 근거: `item-reference-map.md` coverage가 144개 중 high 140개, medium 4개로 닫힌다.
- 남은 항목: `R24-Q4` 무선랜 보안 표준, `R28-Q6` Cyber Kill Chain, `R30-Q11` DB 마스킹 방식명, `R30-Q15` EAM/IAM 비교.
- 진입 전 확인: 기존 패칭 원천만으로는 직접 근거가 부족하므로, 새 원천이 공식·표준·공공기관·벤더 1차 문서인지 먼저 판정한다.

### 2-3. RAW-SOURCE-PATCH-GATE — official page confirmed 원천 raw/source 저장 여부 결정
- 근거: `reference-source-index.md`의 selective raw/source policy.
- 진입 전 확인: 보조 원천은 대량 저장하지 않기로 결정했다.
- 작업 범위: 학습전략·예상문제의 핵심 반복 근거 또는 외부 삭제 위험이 확인된 원천만 선별 패칭한다.

### 2-4. STUDY-FEEDBACK-LOOP — 예상문제 풀이 결과 오답표 회수
- 근거: `analysis-roadmap-todo.md` 다음 작업 후보.
- 진입 전 확인: 사용자가 예상문제를 실제로 푼 뒤 오답·모르는 개념을 제공해야 한다.
- 작업 범위: 오답을 `study-strategy-2026-02.md`의 priority 1~2 보강과 예상문제 보정으로 회수한다.

### 2-5. DOCUMENT-MIGRATION-GATE — 물리 디렉터리 분리 여부
- 근거: `document-management-scaffold.md` 물리 스캐폴딩 정책.
- 진입 전 확인: 현재는 same-directory 링크와 `source_paths` 정합 때문에 보류한다.
- 작업 범위: 실제 디렉터리 분리가 필요해지면 링크·frontmatter·인덱스 마이그레이션을 별도 작업으로 수행한다.

### 2-6. WIKI-INGEST-MVP — raw video → wiki 실행기 구현
- 근거: `docs/wiki-ingest-review.md` §8 구현 전 체크리스트.
- 진입 전 확인: domain registry, strict SemanticWritePlan schema, claim-table lint와 설계 교차검증까지만 완료됐다.
- 작업 범위: `scripts/wiki_ingest.py` plan-only 기본, `tests/test_wiki_ingest.py` fixture, 전역 유일성·active override·apply 검증을 구현한다.

### 2-7. PAGE-TYPE-MIGRATION — 복합 dataset/lab 표준 섹션 정합화
- 근거: `_meta/page-type-spec.md`의 승격 content 표준 섹션과 현재 복합 dataset/lab 89개 문서 구조가 다르다.
- 진입 전 확인: 이번 PR에서는 `wiki/domains/<domain>/drafts/`를 승격 전 초안으로 명시해 study draft의 섹션 강제를 제외했다.
- 작업 범위: dataset/lab 복합 산출물의 page type 모델을 별도 결정한 뒤 표준 섹션 마이그레이션과 lint soft-warn 활성화를 함께 수행한다.

---

## 3. 본 세션 변경 핵심

### 3-1. 신규 자산

| 파일 | 역할 |
|---|---|
| `wiki/domains/information-security/queries/network-path-functions-and-placement.md` | 라우팅·NAT/PAT·방화벽·로드밸런싱·IDS·IPS의 논리 기능, 통합·분리 구성, 패킷 흐름과 오해 교정 정리 |
| `_meta/domains.yaml` | active/inactive domain과 source root hint를 관리하는 registry SoT |
| `_meta/wiki-ingest-write-plan.schema.json` | 외부 입력을 semantic field로 제한하는 strict SemanticWritePlan schema |
| `docs/wiki-ingest-prd.md` | raw video → wiki synthesis 2차 요구사항 |
| `docs/wiki-ingest-architecture.md` | 5-stage 구조·데이터 모델·CLI·저장·요구사항 추적성 설계 |
| `docs/wiki-ingest-business-logic.md` | BR/VR·상태 전이·경계 조건 명제 |
| `docs/wiki-ingest-review.md` | 구현 전 범위·복잡성·연결성 review |
| `docs/adr/0003-domain-registry.md` | domain registry 분리 결정 |
| `requirements-lint.txt` | lint·schema 검증 의존성 pin |
| `tests/test_lint.py` | claim count type/key/value/roll-up 회귀 테스트 |
| `tests/test_wiki_ingest_schema.py` | SemanticWritePlan strict schema 회귀 테스트 |

### 3-2. 변경 자산

| 파일 | 변경 의미 |
|---|---|
| `drafts/study/1장 정리.md` | 시스템 보안 기출형 설정·로그·Windows 구성요소·답안 체크리스트 확장; IIS 경로와 P1/P2 분류 정합화 |
| `drafts/study/2장 정리.md` | 라우팅·NAT·DoS 계열 답안 확장; Slow HTTP Header/POST/Read를 패킷 단서·영향·대응별로 분리 |
| `drafts/study/3장 정리.md` | 응용 보안 설명 보강 및 IIS/HTTPERR 로그 경로 기준 유지 |
| `drafts/study/4장 정리.md` | 암호·인증·PKI 학습 본문과 답안 템플릿 확장 |
| `drafts/study/5장 정리.md` | 관리·위험·사고·인증·개인정보보호 법규를 2026-07-18 시험 적용일 기준으로 확장 |
| `AGENTS.md` | domain registry·SemanticWritePlan SoT와 video ingest MVP lifecycle 반영 |
| `_meta/frontmatter-spec.md` | wiki 15필드, source-summary claim table·derived roll-up 규칙 정합화 |
| `scripts/lint.py` | system/template scope, link resolver, claim table와 안전한 count validation 구현 |
| `docs/prd.md` | 기존 raw importer와 6개 필수 field 기준 정합화 |

### 3-3. cascade 갱신 사이트

- 1장의 IIS site log를 3장과 같은 `%SystemDrive%\inetpub\logs\LogFiles\W3SVC*` 기준으로 통일했다.
- 1장의 Windows 구성요소 P2 분류를 즉답 체크리스트·회독 질문·완료 기준까지 일관되게 갱신했다.
- 2장의 Slow HTTP 분리를 빠른 식별표·상세 모범답안·복습 체크리스트에 함께 반영했다.

### 3-4. 작업 중 발견·수정한 결함

- IIS site log가 1장에서는 `C:\Windows\inetpub...`, 3장에서는 `%SystemDrive%\inetpub...`로 충돌하던 문제를 수정했다.
- LSA/LSASS·SAM·SRM·SID 본문은 P2인데 P1 즉답·회독 질문에 포함되던 우선순위 충돌을 수정했다.
- Slow HTTP 상위 분류 하나로 Header·POST·Read를 묶어 기출 채점 단위를 흐리던 문제를 분리했다.
- Slowloris의 정상 CRLF 줄 구분과 CRLF Injection/HTTP Response Splitting을 구분해 서술했다.
- Candidate status를 `existing/review-needed/duplicate`, kind를 MVP의 `concept/entity`로 단일화했다.
- `matched_path`·claim `notes`를 required nullable/empty key로 명확히 하고 schema 회귀 테스트로 고정했다.
- 비핵심 rejected row와 핵심 claim 0개 roll-up 경계를 명시하고 `claimed` fallback을 테스트했다.
- domain seed 비활성화와 충돌하던 VR-11을 selected active target 검증으로 좁혔다.
- PRD 21개 요구사항의 아키텍처·BR/VR 추적성 표를 추가하고 5-stage 경계를 정합화했다.
- system page 내부 link 검사를 복원하고 root-first·heading suffix·directory index/overview 조건을 회귀 테스트로 고정했다.
- verified evidence를 존재하는 repo-local `raw/sources/{papers,web,urls}/...md`로 제한하고 URL·부재·path traversal 우회를 차단했다.
- wiki metadata enum·배열·boolean·ISO date 타입을 검증하고 `draft` 상태를 정식 enum으로 반영했다.
- 정보보안 문서의 source_paths를 clean checkout에 존재하는 authored/raw 근거로 정정하고 wiki-only 파생 경로를 제거했다.
- domain registry에 inactive LLM domain 6개를 등록하고 overview의 planned link·software domain 명칭을 registry와 정합화했다.

### 3-5. 검증 증거

| 계층 | 상태 | 근거 |
|---|---|---|
| 1. 명제 일관성 | OK | 초기 design-cross finding을 원인별 재분류·수정 후 독립 `logic-reverify` → `findings=0`, `scanned=7`; coverage 21개 → `findings=0`; grounding 301개 → `findings=0` |
| 2. 정적 분석 | OK | 전체 `scripts/lint.py` → `HIGH=0, MEDIUM=0`; `git diff --check`; `check-ai-contract-leak.sh --all` 통과 |
| 3. 단위 | OK | `test_lint.py` 17/17, `test_wiki_ingest_schema.py` 8/8 |
| 4. mock 통합 | OK | 기존 `test_ingest.py` 14/14, `test_pipeline.py` 8/8; 전체 47/47 |
| 5a. 자동화 영역 | OK | schema·lint·문서 명제·요구사항 ID·BR/VR 참조·정보보안 공식 근거를 결정적으로 검증 |
| 5b. 사용자 필수 영역 | N/A | UI/디바이스/주관 판단 없음 |

외부 `run-parallel.sh` 재검은 최초 finding 산출 후 주간 모델 한도 HTTP 429로 실행 불가했다. 이를 성공으로 간주하지 않고 동일 범위를 현재 세션의 독립 논리·coverage·grounding 검사자 3개로 대체해 최종 0건을 확인했다.

### 3-6. dev-todo-update 결과

- `.work-management.json`, `todo.md`, `.manage/todo/todo.md`가 없어 harness todo SoT는 없음.
- 이번 세션의 미해결 review finding은 없으며 todo 파일을 새로 만들지 않았다.

---

## 4. 진입 전 필수 read

| 우선순위 | 파일 | 역할 |
|---:|---|---|
| 1 | `wiki/domains/information-security/drafts/study/1장 정리.md` | 시스템 보안 통합 학습 문서 |
| 2 | `wiki/domains/information-security/drafts/study/2장 정리.md` | 네트워크 보안 및 Slow HTTP·DoS 답안 기준 |
| 3 | `wiki/domains/information-security/drafts/study/3장 정리.md` | 응용 보안 통합 학습 문서 |
| 4 | `wiki/domains/information-security/drafts/study/4장 정리.md` | 암호·인증·PKI 통합 학습 문서 |
| 5 | `wiki/domains/information-security/drafts/study/5장 정리.md` | 관리·법규 및 2026 시험일 현행 기준 |
| 6 | `wiki/domains/information-security/queries/network-path-functions-and-placement.md` | 네트워크 장비 기능·배치·패킷 흐름 질의 정리 |
| 7 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/00-management/analysis-roadmap-todo.md` | 후속 작업과 리스크 상태 |
| 8 | `docs/wiki-ingest-prd.md` | 2차 wiki synthesis 요구사항 SoT |
| 9 | `docs/wiki-ingest-architecture.md` | 구조·모델·추적성 설계 |
| 10 | `docs/wiki-ingest-business-logic.md` | BR/VR와 상태 전이 SoT |
| 11 | `docs/wiki-ingest-review.md` | 구현 전 완료 기반과 잔여 구현 목록 |

---

## 5. 잔존 함정·회귀

### 5-1. 회차 슬롯 패턴 과신 금지
- 발생 사례: 사용자가 1회차/2회차/3회차 간 강한 패턴 여부를 질문했다.
- 회피 방법: `session-slot-pattern-analysis.md` 결론처럼 슬롯은 보조 가중치로만 쓰고, 결정적 출제 예측 규칙으로 승격하지 않는다.

### 5-2. 예상문제 과신 금지
- 발생 사례: 2026년 2회 예상문제 36문항을 작성했다.
- 회피 방법: 실제 출제 보장이 아니라 학습용 고확률 세트로 유지하고, confidence가 medium인 문항은 보수적으로 다룬다.

### 5-3. 물리 디렉터리 분리 보류
- 발생 사례: 문서 관리 스캐폴딩 중 디렉터리 분리 여부를 검토했다.
- 회피 방법: 현재는 same-directory 링크와 `source_paths` 정합을 유지한다. 이동은 별도 마이그레이션으로만 수행한다.

### 5-4. 무관한 dirty worktree
- 발생 사례: 세션 시작 전부터 대량 `cs/` 삭제, `_meta`, `docs`, `scripts`, `tests`, `wiki/index.md` 변경이 존재했다.
- 회피 방법: 이번 세션의 명시된 allowlist만 staging하고, authored `cs/` 삭제·별도 dataset·`wiki/index.md`·digital-forensics·DS_Store 변경은 절대 함께 커밋하지 않는다.

### 5-5. 장비와 네트워크 기능의 일대일 대응 금지
- 발생 사례: 라우터와 NAT 장비가 반드시 하나인지, 포트 매핑을 어느 장비에서 수행하는지 혼동했다.
- 회피 방법: 라우팅·NAT/PAT·방화벽·로드밸런싱·IDS·IPS를 먼저 논리 기능으로 구분한다. 실제 배치는 통합형 또는 분리형일 수 있으며, 포트 매핑은 NAT/PAT 기능을 수행하는 장비에서 설정한다.

### 5-6. Slow HTTP와 CRLF 공격 혼동 금지
- 발생 사례: Slow HTTP Header가 CRLF를 삽입·조작하는 공격인지 혼동했다.
- 회피 방법: Slowloris는 요청 헤더의 종료를 뜻하는 빈 줄을 보내지 않고 헤더 조각을 천천히 추가해 연결을 유지한다. CRLF Injection과 HTTP Response Splitting은 개행 문자를 입력값에 주입해 헤더·응답 구조를 변조하는 별도 공격이다.

### 5-7. Windows 로그 경로 하드코딩 금지
- 발생 사례: IIS site log 경로를 `C:\Windows\inetpub...`로 잘못 고정해 3장과 충돌했다.
- 회피 방법: IIS site log는 `%SystemDrive%\inetpub\logs\LogFiles\W3SVC*`, HTTPERR는 `%SystemRoot%\System32\LogFiles\HTTPERR`, DHCP는 `%SystemRoot%\System32\DHCP` 기준을 유지하고 설치 환경에 따른 변수 경로임을 함께 적는다.

### 5-8. 요구사항 coverage finding을 구현 누락으로 단정 금지
- 발생 사례: requirements checker가 접두사형 `docs/wiki-ingest-business-logic.md`를 선언 범위대로 읽지 않아 실제 존재하는 FR-5 매핑까지 uncovered로 보고했다.
- 회피 방법: exact ID grep 결과와 의미 매핑을 분리해 검증한다. 현재 canonical traceability는 `docs/wiki-ingest-architecture.md` §12이다.

### 5-9. Candidate와 roll-up 경계 재확장 금지
- 발생 사례: generic page type 6종과 중복되는 `new` 상태가 MVP schema에 들어가고, 핵심 claim 0개·비핵심 rejected row의 roll-up이 모호했다.
- 회피 방법: MVP candidate kind는 `concept/entity`, status는 `existing/review-needed/duplicate`로 유지한다. `matched_path`와 `notes`는 key 필수·null/empty 허용이며, 핵심 claim 0개는 `claimed`다.

### 5-10. system page·verified evidence 예외 확대 금지
- 발생 사례: system page 링크 검사를 통째로 제외하고 verified evidence를 문자열 패턴만으로 허용해 broken link·부재 파일·path traversal이 통과했다.
- 회피 방법: system page는 content frontmatter만 면제하고 내부 link는 검사한다. verified evidence는 resolve 후 repo 내부 허용 raw root의 실제 Markdown 파일인지 확인한다.

---

## 6. 본 세션에 미진입한 안건

- 공식 PDF 비밀번호 확보 시 1~28회 원문 문구 최종 대조.
- 예상문제 풀이 결과를 오답표로 회수해 학습 전략과 예상문제를 보정.
- 남은 4개 medium confidence 문항의 전용 공식 원천 보강 또는 medium 유지 결정.
- 보조 원천 raw/source 선별 패칭 여부 결정.
- 문서 물리 디렉터리 분리가 필요해질 경우 별도 마이그레이션 수행.
- 이번 dev-finish allowlist 밖의 기존 dirty worktree는 검토·수정·커밋하지 않았으므로 별도 작업에서 소유권과 상태를 확인한다.
- `scripts/wiki_ingest.py`와 `tests/test_wiki_ingest.py` 구현은 아직 시작하지 않았다. 현재 완료 범위는 설계·registry·strict schema·lint 기반이며, 구현은 `docs/wiki-ingest-review.md` §8 체크리스트에서 재개한다.
