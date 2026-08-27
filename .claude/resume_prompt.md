# cs-study 다음 세션 진입 — P2-T6 순서 8 deterministic materializer

> 작성: 2026-08-26
> 직전 작업: P2-T5 순서 7 leaf command를 TDD로 구현하고 전체 회귀·설계·코드·live no-write 교차검증을 완료했다.
> 작업 위치: 현재 cs-study linked worktree (`feat/knowledge-pipeline` 브랜치)
> 다음 세션 첫 동작 의무: 본 파일, `todo.md`, `reports/P2-T5-verification.md`, `docs/wiki-ingest-architecture.md` §13, `docs/wiki-ingest-business-logic.md`의 generated-view 규칙을 먼저 읽고 P2-T6 materializer 범위를 고정한다.
> commit: P2-T5 변경은 구현·검증했지만 아직 commit하지 않았다. 사용자의 별도 commit 승인 전에 P2-T6를 시작하지 않는다.

---

## 1. 현재 작업 정책

- `cs/`, `development/`, `coding-test/`, `lang/`, `tools/` authored SoT는 현재 status 변경 0건이며 baseline 범위 밖이다.
- P2-T2는 privacy-normalized clipping contract와 persistent 경로 guard, 8개 append-only revision 이행까지 검증했다.
- terminal journal 3개와 journal-bound candidate 3개(255 files)는 삭제하지 않고 로컬 rollback evidence로 보존하며 commit에서 제외한다.
- P2-T4 final restage에서 staged ACMR 363개 index/worktree byte mismatch 0과 tracked unstaged 0을 확인했다.
- active persistent snapshot의 Apple·Windows local-user-home 경로는 P2-T2에서 TDD로 제거·재생성·cascade 검증했다.
- runtime evidence를 제외한 순서 1–6b snapshot은 P2-T4에서 전체 검증과 사용자 commit 승인을 마쳤다.
- 순서 7은 P2-T5에서 구현·검증했고, 순서 8–12는 각각의 설계 gate와 독립 commit 후보를 유지한다.

---

## 2. 다음 진입 작업과 외부 trigger

- next_task: P2-T6
- focus_group: 지속 가능한 지식 파이프라인

### P2-T2. persistent 절대경로 비식별화
- 완료: Apple·Windows user-home prefix를 단일 privacy leaf로 정규화하고 active persistent offender 0을 확인했다.
- 완료: 8개 immutable clipping revision을 append-only로 추가하고 active manifest reference 16개·resolution digest 8개·live target을 정합화했다.
- 증거: `reports/P2-T2-verification.md`; 전체 154 passed, 11 skipped, active manifest 75/75 검증.

### P2-T3. runtime evidence ignore guard
- 완료: terminal journal 3개·candidate root 3개/255 files를 보존하고 exact ignore pattern 3개로 격리했다.
- 완료: runtime path tracked·staged·normal porcelain 각 0, journal digest와 candidate count 불변을 확인했다.
- 증거: `reports/P2-T3-verification.md`; 전체 155 passed, 11 skipped.

### P2-T4. 순서 1–6b atomic baseline commit
- 완료: persistent allowlist 385개만 stage하고 index/worktree 일치·전체 검증·별도 사용자 commit 승인을 확인했다.
- 증거: `reports/P2-T4-verification.md`; root 156 passed, 11 skipped, project contract 27 tests OK, 자동화 가능한 5계층 영역 미시도 0건.

### P2-T5. 순서 7 leaf command TDD
- 완료: synthesize·promote·collection·move command, strict PageWritePlan, shared writer lock, validate-before-write, atomic rollback·exact replay를 TDD로 구현·검증했다.
- 증거: `reports/P2-T5-verification.md`; root 212 passed, 11 skipped, live structural findings 0, lint exit 0.
- P2-T6~P2-T11의 세부 작업·직접 선행·완료 증거의 canonical은 `todo.md`다.

### P2-T6. 순서 8 deterministic materializer
- 다음 작업: canonical page·registry·schema와 순서 7 leaf command를 입력으로 index·overview·template·Bases generated view를 TDD로 구현한다.
- 완료 gate: 연속 2회 materialize tree hash 동일, active coverage 100%, authored source 무변경, 별도 commit 승인.

### 2-1. OFFICIAL-PRIMARY-SOURCE-GATE — KCA 공식 원문 대조
- 근거: 회차 파일 공통 note와 `subject-type-cross-verify-report.md`의 official PDF scope limit.
- 진입 전 확인: 사용자 제공 편집본 PDF 4개는 해제·대조했지만 KCA 공식 원문은 확보하지 못했다.
- 작업 범위: KCA 공식 원문 또는 독립 1차 원천 확보 시 1~28회 문구를 최종 대조한다.

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

### 2-6. WIKI-INGEST-REMAINDER — 구현 순서 8–12
- 근거: `docs/wiki-ingest-architecture.md` §13, `docs/wiki-ingest-review.md` §9.
- 진입 전 확인: 순서 1–6b engine·canonical cutover·privacy/runtime guard와 P2-T4 baseline 검증·승인이 완료됐다.
- 작업 범위: P2-T6부터 P2-T11까지 직접 선행 DAG대로 수행한다.

### 2-7. PAGE-TYPE-MIGRATION — 복합 dataset/lab 표준 섹션 정합화
- 근거: `_meta/page-type-spec.md`의 승격 content 표준 섹션과 현재 복합 dataset/lab 89개 문서 구조가 다르다.
- 진입 전 확인: `wiki/domains/<domain>/drafts/`는 canonical cutover 전 legacy authored draft 경로이며, 목표 DraftPage 경로 `wiki/staging/`로의 lifecycle 전환은 P2-T5 이후 별도 작업이다.
- 작업 범위: dataset/lab 복합 산출물의 page type 모델을 별도 결정한 뒤 표준 섹션 마이그레이션과 lint soft-warn 활성화를 함께 수행한다.

---

## 3. 현재 상태와 과거 변경 이력

### 3-0. 2026-08-25 commit-boundary preflight

- P2-T1 SoT 적용 전 historical Git status baseline은 ignored 39개 제외 626 records, 분류 626/626이었다.
- P2-T3 이후 P2-T4 restage 전 normal porcelain-v1 logical record는 391개였으며 terminal journal 3개·candidate root 3개/255 files는 ignore됐다.
- P2-T4 restage 전 index는 rename 77개이며 destination 52개의 index bytes가 worktree와 달라 commit을 금지한 상태였다.
- active persistent local-user-home offender는 0이고, active reference가 없는 기존 clipping revision 8개/34 occurrences는 P2-T4 denylist다.
- 이 preflight 시점에는 순서 7–12가 미구현이었고 다음 진입은 별도 승인 gate인 P2-T4였다.

아래 3-1~3-6은 2026-07-12 handoff의 과거 변경 이력이다.

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
| `wiki/domains/information-security/drafts/study/info-sec-engineer-system-security-study.md` | 시스템 보안 기출형 설정·로그·Windows 구성요소·답안 체크리스트 확장; IIS 경로와 P1/P2 분류 정합화 |
| `wiki/domains/information-security/drafts/study/info-sec-engineer-network-security-study.md` | 라우팅·NAT·DoS 계열 답안 확장; Slow HTTP Header/POST/Read를 패킷 단서·영향·대응별로 분리 |
| `wiki/domains/information-security/drafts/study/info-sec-engineer-application-security-study.md` | 응용 보안 설명 보강 및 IIS/HTTPERR 로그 경로 기준 유지 |
| `wiki/domains/information-security/drafts/study/info-sec-engineer-security-general-study.md` | 암호·인증·PKI 학습 본문과 답안 템플릿 확장 |
| `wiki/domains/information-security/drafts/study/info-sec-engineer-management-and-law-study.md` | 관리·위험·사고·인증·개인정보보호 법규를 2026-07-18 시험 적용일 기준으로 확장 |
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
| 4. mock 통합 | historical | 2026-07-12 기록값은 당시 importer 14/14·pipeline 8/8·전체 47/47이며, 두 legacy test 파일은 현재 전환에서 삭제됐다 |
| 5a. 자동화 영역 | OK | schema·lint·문서 명제·요구사항 ID·BR/VR 참조·정보보안 공식 근거를 결정적으로 검증 |
| 5b. 사용자 필수 영역 | N/A | UI/디바이스/주관 판단 없음 |

외부 `run-parallel.sh` 재검은 최초 finding 산출 후 주간 모델 한도 HTTP 429로 실행 불가했다. 이를 성공으로 간주하지 않고 동일 범위를 현재 세션의 독립 논리·coverage·grounding 검사자 3개로 대체해 최종 0건을 확인했다.

### 3-6. dev-todo-update 현재 결과

- local mode canonical은 `todo.md`이며 `.work-management.json`과 `.manage/todo/todo.md`는 없다.
- `지속 가능한 지식 파이프라인` 그룹의 P2-T1~P2-T11이 현재·후속 작업을 소유한다.

---

## 4. 진입 전 필수 read

우선 `todo.md`, `reports/P2-T1-verification.md`, `docs/wiki-ingest-architecture.md` §13, `docs/wiki-ingest-review.md` §9를 읽는다. 아래 표는 정보보안 학습 문서 작업을 재개할 때의 보존된 목록이다.

| 우선순위 | 파일 | 역할 |
|---:|---|---|
| 1 | `wiki/domains/information-security/drafts/study/info-sec-engineer-system-security-study.md` | 시스템 보안 통합 학습 문서 |
| 2 | `wiki/domains/information-security/drafts/study/info-sec-engineer-network-security-study.md` | 네트워크 보안 및 Slow HTTP·DoS 답안 기준 |
| 3 | `wiki/domains/information-security/drafts/study/info-sec-engineer-application-security-study.md` | 응용 보안 통합 학습 문서 |
| 4 | `wiki/domains/information-security/drafts/study/info-sec-engineer-security-general-study.md` | 암호·인증·PKI 통합 학습 문서 |
| 5 | `wiki/domains/information-security/drafts/study/info-sec-engineer-management-and-law-study.md` | 관리·법규 및 2026 시험일 현행 기준 |
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

### 5-4. 대량 dirty worktree 임의 분할 금지
- 발생 사례: 626 records가 pipeline·canonical migration·project relocation·task handoff·runtime evidence에 결속돼 있고 authored SoT 5개 영역의 변경은 0건이다.
- 회피 방법: P2-T2·P2-T3 이후 inventory를 다시 만들고 persistent snapshot의 중간 tree 검증 근거가 없으면 기능군별로 소급 분할하지 않는다.

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
- 회피 방법: exact ID grep 결과와 의미 매핑을 분리해 검증한다. 현재 canonical traceability는 `docs/wiki-ingest-architecture.md` §14이다.

### 5-9. Candidate와 roll-up 경계 재확장 금지
- 발생 사례: generic page type 6종과 중복되는 `new` 상태가 MVP schema에 들어가고, 핵심 claim 0개·비핵심 rejected row의 roll-up이 모호했다.
- 회피 방법: MVP candidate kind는 `concept/entity`, status는 `existing/review-needed/duplicate`로 유지한다. `matched_path`와 `notes`는 key 필수·null/empty 허용이며, 핵심 claim 0개는 `claimed`다.

### 5-10. system page·verified evidence 예외 확대 금지
- 발생 사례: system page 링크 검사를 통째로 제외하고 verified evidence를 문자열 패턴만으로 허용해 broken link·부재 파일·path traversal이 통과했다.
- 회피 방법: system page는 content frontmatter만 면제하고 내부 link는 검사한다. verified evidence는 resolve 후 repo 내부 허용 raw root의 실제 Markdown 파일인지 확인한다.

### 5-11. staged rename-only commit 금지
- 발생 당시 77개 rename 중 52개 destination의 후속 수정이 index에 없어 중간 상태였다. P2-T4 final allowlist restage로 mismatch 0을 확인하기 전까지 commit하지 않았다.

### 5-12. immutable clipping 제자리 수정 금지
- P2-T2는 payload를 덮어쓰지 않고 새 content digest revision을 만든 뒤 manifest reference와 target digest를 함께 cascade한다.

### 5-13. terminal rollback evidence 삭제·commit 금지
- journal 3개와 candidate 255 files는 복구 증거로 보존하되 P2-T3 ignore guard로 stage를 차단한다.

---

## 6. 본 세션에 미진입한 안건

- KCA 공식 원문 또는 독립 1차 원천 확보 시 1~28회 문구 최종 대조.
- 예상문제 풀이 결과를 오답표로 회수해 학습 전략과 예상문제를 보정.
- 남은 4개 medium confidence 문항의 전용 공식 원천 보강 또는 medium 유지 결정.
- 보조 원천 raw/source 선별 패칭 여부 결정.
- 문서 물리 디렉터리 분리가 필요해질 경우 별도 마이그레이션 수행.
- 순서 1–6b persistent baseline은 P2-T4에서 final verification과 별도 commit 승인을 마쳤다.
- `scripts/wiki_ingest.py` 기반 순서 1–7은 구현·검증했다. 순서 8 deterministic materializer를 P2-T6에서 재개한다.
