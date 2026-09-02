# Todo

작성일: 2026-08-25
SoT: 로컬 `todo.md`

## Scope Contract

| 항목 | 내용 |
|---|---|
| 갱신 대상 task | 지속 가능한 지식 파이프라인 P2-T1~P2-T11의 완료 증거와 직접 선행 관계 |
| 신규 등록 후보 | 실제 미완 작업만 중복 검사 후 등록 |
| 범위 밖 | source·wiki·raw의 작업 추적 목적 수정, 완료 작업 재개방, 추측 기반 후속 task 생성 |
| 검증 기준 | 상태·분류 enum, 의미 중복 없음, 직접 선행 단방향·cycle 0, 구현·운영 commit의 사용자 승인 유지 |

## 상태 Enum

| 상태 | 의미 |
|---|---|
| `[ ]` | pending |
| `[-]` | in-progress |
| `[x]` | completed |
| `[!]` | blocked |
| `[~]` | discarded |

### 정보보안기사 실기 Practice

| ID | 상태 | 분류 | 작업 | 선행 | 입력 | 산출 |
|---|---|---|---|---|---|---|
| P1-T1 | [x] | [검증] | 기출 복원 31회차 513문항의 문제·답안·출처 경계·독립 풀이 가능성을 회차별로 전수 검증하고, 오류·모호성·복원 한계를 근거와 함께 정정·기록 | 없음 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/01-rounds/`, `06-verification/`, KCA 출제 범위 및 확인 가능한 1차·공식 레퍼런스 | 회차별 검증 보고서, 정정된 원본 MD·파생 JSON의 동기화 증거, 남은 복원 한계 목록 |
| P1-T2 | [x] | [검증] | 기출 전수 검증 완료 후 Information Security Practice 설계 문서 9개의 frontmatter·source_paths·provenance·SSOT 참조를 실제 근거로 정합화하고 vault lint를 재검증 | P1-T1 | `AGENTS.md`, `_meta/frontmatter-spec.md`, `scripts/lint.py`, `projects/info-sec-engineer-practice/docs/product/{prd.md,architecture.md,chapter-2-p1-settings-scope.md,chapter-3-p1-settings-scope.md,business-logic/chapter-2-p1-settings.md}`, `projects/info-sec-engineer-practice/{README.md,DESIGN.md,docs/architecture.md,docs/past-exam-import-architecture.md}` | 9개 문서의 유효 frontmatter 및 SSOT 참조 정합화, 해당 9개 문서의 lint HIGH 18건 해소 증거, 문서 간 중복·순환 참조 없음 확인 |
| P1-T3 | [x] | [검증] | 승인된 wiki 이동 8건이 만드는 관찰 external reference 676회를 owner별로 분류하고 active path만 바꾸는 no-write cascade plan과 전체 diff를 생성해 `sourceRef` line·excerpt·status 보존 및 hidden-inclusive active stale scanner 0건(명시적 제외·historical 별도 보고)을 검증한 뒤 actual apply 승인 자료를 제출한다 | 없음 | `reports/P2-T4-verification.md`, `docs/wiki-ingest-review.md`, `projects/info-sec-engineer-practice/data/question-packs/`, `projects/info-sec-engineer-practice/practice-data.js`, `.claude/resume_prompt.md` | canonical question-pack 329회 path 변경, generated JS 재생성, project docs·system refs cascade, historical plan·backup·journal 검증 증거 |

### 지속 가능한 지식 파이프라인

| ID | 상태 | 분류 | 작업 | 선행 | 입력 | 산출 | 비고 |
|---|---|---|---|---|---|---|---|
| P2-T1 | [x] | [검증] | hidden·untracked를 포함한 Git status 626건을 소유권별로 전수 분류하고 unsafe index·개인 경로·runtime evidence·SoT drift를 식별해 commit allowlist·denylist와 후속 owner를 고정한다 | 없음 | `git status --porcelain=v2 -z --untracked-files=all`, index/worktree, 현행 설계·리뷰, migration journal | `reports/P2-T1-verification.md`, 626건 inventory TSV·JSON, atomic baseline 경계 | verified: [[reports/P2-T1-verification]] |
| P2-T2 | [x] | [구현] | persistent repository의 로컬 사용자 절대경로를 거부하는 회귀 검사를 먼저 추가하고 8개 immutable clipping bundle을 비식별 canonical locator로 새 revision capture한 뒤 tracked raw web·live wiki·manifest reference·resolution·target digest를 cascade 정합화한다 | P2-T1 | persistent 11 files, artifact·migration contracts | 절대경로 0인 새 bundle revisions, 갱신된 manifest reference·resolution·target digest, TDD 증거 | verified: [[reports/P2-T2-verification]] |
| P2-T3 | [x] | [구현] | terminal migration journal·candidate를 보존하면서 Git stage에서 제외하는 repository ignore guard와 staged/tracked 0 검증을 추가한다 | P2-T1 | terminal journal 3개, journal-bound candidate 3개, `.gitignore` | runtime evidence ignore rules, 보존·비추적 검증 증거 | verified: [[reports/P2-T3-verification]] |
| P2-T4 | [x] | [운영] | P2-T2·P2-T3 이후 runtime evidence를 제외한 순서 1–6b persistent snapshot만 stage하고 전체 검증과 별도 사용자 승인을 거쳐 atomic baseline commit을 생성한다 | P2-T2, P2-T3 | 검증된 persistent allowlist·denylist, 완료 보고서, 사용자 commit 승인 | 순서 1–6b baseline commit SHA, 전후 status·index 증거 | verified: [[reports/P2-T4-verification]] |
| P2-T5 | [x] | [구현] | 순서 7 synthesize·promote·collection·move leaf command를 TDD로 구현한다 | P2-T4 | 6b live target, SemanticPlan·PageWritePlan operation/input·verdict·base content·mode, shared repository lock 계약 | strict one-page plan/apply, stale·rollback·replay·process-lock 회귀 검증, `reports/P2-T5-cross-verification.jsonl` | verified: [[reports/P2-T5-verification]] |
| P2-T6 | [x] | [구현] | 순서 8 materializer를 구현하고 index·overview·template·Bases를 generated view로 전환한다 | P2-T5 | canonical pages·registry·schema | two-run tree hash·active coverage 100%와 독립 commit | verified: [[reports/P2-T6-verification]] |
| P2-T7 | [x] | [검증] | 순서 9 legacy structure-rule scope·log/backlink/provenance·전환 runtime 제거를 no-write exact patch와 derived parity로 검증한다 | P2-T6 | legacy rules·log·index 선언·전환 runtime | exact patch SHA-256·target Git tree OID·repository query·derived parity report | verified: [[reports/P2-T7-verification]] |
| P2-T8 | [x] | [운영] | P2-T7 별도 사용자 승인 후 검증된 순서 9 target tree를 Git commit 경계로 통합한다 | P2-T7 | 승인된 patch digest·base commit·target tree OID | 순서 9 독립 commit·post-integration 검증 | verified: [[reports/P2-T8-verification]] |
| P2-T9 | [x] | [구현] | 순서 10 local hook와 extractor·현재 저장소의 독립 CI를 연결한다 | P2-T6 | extractor/current repo CI 계약, required commands | 두 저장소 clean-checkout required commands 성공과 독립 commit | verified: [[reports/P2-T9-verification]] |
| P2-T10 | [-] | [운영] | 순서 11 두 대상 YouTube source를 새 pipeline로 재처리한다 | P2-T8, P2-T9 | 두 URL·artifact·canonical pipeline | artifact→draft→통합 wiki evidence trace와 독립 commit | 구현·검증 완료, 독립 commit·remote CI closure 진행 중 |
| P2-T11 | [ ] | [검증] | 순서 12 full vault·설계·코드 교차검증과 자동화 가능한 5계층 검증을 모두 수행한다 | P2-T10 | 전체 vault·설계 명제·검증 도구 inventory | HIGH 0, 명제 coverage, 5계층 최종 보고 | |
