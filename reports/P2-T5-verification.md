# P2-T5 검증 보고서

## 완료 보고

- scope: 설계 SoT 정합화, 순서 7 synthesize·promote·collection·move strict PageWritePlan과 ordinary apply transaction의 TDD 구현, 설계·코드·실환경 재검증, todo·resume 정합화.
- excluded: 순서 8–12(P2-T6~P2-T11), authored wiki·raw·migration content write, inactive clipping revision 8개/16 files, migration apply·restore·recover, commit·push.
- tests run: `uv run --with coverage --with pytest --with jsonschema --with pyyaml coverage run -m pytest -q` -> 212 passed; legacy-base condition으로 11개 제외. canonical `check --all` -> structural PASS·findings 0; legacy dispatcher lint -> exit 0.
- changed files: tracked/staged=23 paths(resume 1, schema·requirements 2, normative design/review 4, runtime Python 7, tests 6, todo 1, verification evidence 2); untracked=inactive raw baseline 16 paths. inactive raw 16 files는 수정·stage·삭제·ignore하지 않음.
- known gaps: none
- SoT sync: todo=P2-T5 `[x]`·verified report 연결; resume=`next_task: P2-T6`·P2-T5 검증 증거·순서 8–12 재개점 갱신; memory=별도 세션 마무리 작업이 아니므로 갱신 제외.
- Task Quality Gate: L2
- Task ID: P2-T5
- Intent: 외부 semantic input을 단일 knowledge page의 결정적 plan/apply로 제한하고 stale·경쟁·부분 commit·semantic gate 우회를 기계적으로 거부한다.
- SoT: `docs/wiki-ingest-prd.md:55-71,111-121`, `docs/wiki-ingest-architecture.md:139-166,291-306,374-386`, `docs/wiki-ingest-business-logic.md:47-99`, `_meta/knowledge-requirements.json:9-36`.
- Derived: `_meta/knowledge.schema.json`, `scripts/wiki_ingest.py`, `scripts/knowledge/{documents,fs,schema,check,migration,artifacts}.py`, P2-T5 tests·cross-verification·본 보고서.
- Forbidden: live canonical wiki·raw·authored tree·migration content write, multiple-page ordinary write-set, implicit source/order/review decision, plan digest prefix match, force overwrite, non-cooperative writer에 대한 filesystem CAS 보장 주장, 승인 전 commit·push.
- Invariants: exact plan SHA-256·schema·operation/input·review verdict 결속, logical page write-set 0~1, validate-before-write, shared repository lock, base tree·bytes·mode stale refusal, atomic leaf·conflict-aware rollback, stable ID·same-lifecycle move, exact target replay만 no-op.
- Completion Predicates: normal·edge·exception·failure-injection TDD, 명제 surface·금지 surface mapping, 순환 0 exact guard, 자기 코드 경로 ratchet, 전체 회귀, 실제 live target no-write check, process-scoped lock, todo·resume·review drift 0, blocking finding 0.
- Validation Plan: schema·requirement mapping, focused RED→GREEN, full pytest+coverage, Ruff E/F/I, canonical checker, legacy lint, hidden-inclusive status, AST dependency/call-path guard, process lock, design cross-verification, completion·SoT drift gate.
- User-required Gates: 권장안 A 설계 정합화→재검증→TDD 구현 승인은 수신했다. commit·push는 별도 승인 대상으로 남겼다.
- Promotion Candidates: shared lock·plan binding·candidate path·operation delta·rollback·replay를 test/AST guard로 승격했다. 추가 owning follow-up task가 필요한 반복 결함은 없다.

## 구현 전 Task Quality Gate Capsule

- Task ID: P2-T5
- Task class: L2
- Intent: strict single-page plan/apply로 순서 7을 구현하고 설계·코드·실환경 계약을 교차검증한다.
- SoT: P2-T5 todo, wiki ingest PRD·architecture·business logic, knowledge schema·requirements manifest.
- Derived: CLI·documents·filesystem·checker·schema implementation, tests, review·verification evidence.
- Forbidden: live wiki·raw·authored·migration content mutation, page 2개 이상 ordinary transaction, implicit semantic/order/review decision, force write, commit·push.
- Invariants: exact digest/binding, write-set 0~1, lock 안 candidate 재검증, atomic leaf, stable ID, exact replay, rollback conflict 보존.
- Completion Predicates: normal·edge·exception TDD, baseline regression, structural/design/code cross-verification, 자동화 가능 5계층 전수 시도, SoT sync.
- Validation Plan: focused tests, full suite/coverage, static/lint/check, actual filesystem/process-lock tests, cross verification, completion gate.
- User-required Gates: 권장안 A 실행 승인 수신; commit·push 별도 승인 유지.
- Promotion Candidates: 반복 위험은 신규 schema/test/AST guard에 귀속하고 문서 후속 task로 대체하지 않는다.

## Requirement Proposition Matrix

| ID | 검증 명제 | Source | 구현 근거 | 테스트·검증 근거 | 금지 surface 근거 | 판정 |
|---|---|---|---|---|---|---|
| P2T5-P1 | SemanticPlan은 명시적 source만 받고 write 권한을 가지지 않는다 | `docs/wiki-ingest-prd.md:55-56`; BR-SYN-001~003 | schema + synthesize planner | `tests/test_page_commands.py:159-283` | implicit latest, wiki re-ingest, path/frontmatter/write operation 입력 reject | PASS |
| P2T5-P2 | plan/apply는 exact identity와 page 0~1 write-set을 결속한다 | `docs/wiki-ingest-prd.md:65`; BR-APPLY-004~007 | PageWritePlan schema + command router + apply | `tests/test_page_commands.py:286-421` | prefix confirmation, operation/input mismatch, force overwrite reject | PASS |
| P2T5-P3 | promote는 stable ID·content를 보존하고 claim verdict·review 승인을 재검증한다 | `docs/wiki-ingest-prd.md:64`; BR-LIFE-001·BR-LIFE-002·BR-LIFE-005 | promote planner/apply | `tests/test_page_commands.py:424-597` | claimed/insufficient/missing/forged verdict, boolean-only approval reject | PASS |
| P2T5-P4 | collection은 Members 행 순서만 단일 소유하고 명시적 정렬 정책을 요구한다 | `docs/wiki-ingest-prd.md:61`; `docs/wiki-ingest-architecture.md:172-176,384` | add-member/reorder delta validator | `tests/test_page_commands.py:599-1010` | implicit order, duplicate/lost member, Members 외 bytes 변경 reject | PASS |
| P2T5-P5 | move는 ID·bytes·mode·lifecycle root를 보존한다 | `docs/wiki-ingest-prd.md:71`; BR-MOVE-001 | move planner/apply + no-replace rename | `tests/test_page_commands.py:1069-1422` | lifecycle bypass, target collision, content/mode mutation reject | PASS |
| P2T5-P6 | ordinary writer는 migration writer와 lock을 공유하고 write 직전 stale를 재검증한다 | `docs/wiki-ingest-prd.md:87`; BR-APPLY-011~013 | repository-root flock + candidate-in-lock + atomic leaf | `tests/test_fs.py:350-380`; `tests/test_migration_plan.py:53-81`; `tests/test_page_commands.py:1013-1067` | lock 실패 후 write, stale bytes/mode write reject | PASS |
| P2T5-P7 | post-commit 실패는 own leaf만 rollback하고 외부 변경·rollback 실패는 indeterminate로 보존한다 | BR-APPLY-011·BR-APPLY-013 | fs leaf primitives + apply reconcile | `tests/test_fs.py:106-348`; `tests/test_page_commands.py:1133-1275` | 관찰된 same-leaf 외부 bytes overwrite·false stale 축소 reject | PASS |
| P2T5-P8 | 신규 순환은 0이고 승인된 호출 깊이 baseline을 늘리지 않는다 | `docs/wiki-ingest-prd.md:79-80`; `docs/wiki-ingest-architecture.md:550-562` | exact dependency graph + callback path binding | `tests/test_knowledge_check.py:499-674` | new cycle, unbound callback, call edge ratchet increase reject | PASS |

## TDD 구현 증거

- RED→GREEN은 operation/input mismatch, forged page ID·review verdict, collection 순서·raw-byte delta, CRLF base, special/symlink entry, candidate-check 중 stale mutation, post-tree mismatch·exception, move source reappearance, unobservable leaf, rollback conflict/failure, 별도 process lock, migration writer lock 순으로 단일 계약씩 진행했다.
- 후속 coverage 대조에서 claim/relation table escape와 collection explicit `before`·`after`·`order-by-id` policy test를 보강했다. 이 두 test는 미구현 기능 RED가 아니므로 기존 구현의 coverage 보강으로 분류한다.
- 최종 execution coverage 대조에서 독립 리뷰의 direct-name heuristic 29개 대상은 모두 1회 이상 실행됐다. 변경 runtime Python 7개 모듈 합계 77%는 P2-T5가 수정하지 않은 baseline migration branch를 포함한 참고값이며, P2-T5 변경 함수의 zero-execution gap은 0이다.

## 설계·코드 교차검증

- chronological raw JSONL 83행은 `reports/P2-T5-cross-verification.jsonl`에 원문 그대로 보존했다. SHA-256은 `1b31f57d9721ad392a611808a5424ce25431db07d48e68a1241e5612cdc020f0`다.
- 초기 finding과 수정 후 recheck를 시간순으로 함께 보존했으므로 파일 전체를 “finding 0”으로 해석하지 않는다. 최종 logic-proposition-checker 2회, spec-drift, requirements, grounding recheck의 blocking finding은 각각 0이다.
- cycle detector는 Python graph cycle 0을 보고했다. DB transaction reviewer는 DB stack이 없어 `stack_not_detected` abstain했으며, 본 작업의 영속성 경계는 filesystem transaction이므로 fs·page·migration failure-injection test로 별도 검증했다.
- pyan3는 edge 4 이상 경로 16개, P2-T5 ordinary 7개·최대 edge 6, migration 최대 edge 7을 보고했다. 동적 candidate path는 함수 9개 직렬(= edge 8)이며 CLI·lock·transaction·candidate·schema/tree·Markdown parsing의 서로 다른 경계로 분류했고 exact AST guard로 증가를 차단했다. one-line validator pass-through는 제거했다.

## 5계층 검증 판정

| 계층 | 실행 증거 | 판정 |
|---|---|---|
| 1 명제 | P2T5-P1~P8의 source·implementation·test·forbidden surface mapping | PASS |
| 2 정적 | schema/requirements mapping, 변경 Python Ruff E/F/I, diff check, exact dependency/call-path guard, completion report gate | 오류 0; repository 전체 Ruff의 범위 밖 baseline 5건은 분리 보고 |
| 3 단위 | schema, plan binding, renderer, delta validator, fs primitives | full suite에 포함 |
| 4 mock 통합 | CLI plan→apply, candidate overlay, migration shared lock, rollback/replay failure injection | full suite에 포함 |
| 5 자동화 실환경 | live target `check --all`·legacy dispatcher lint, 실제 filesystem mode/fsync/rename, 별도 process flock | 모두 시도·OK |
| 5 사용자 필수 | 실제 콘텐츠 claim grounding·시각 판정 | P2-T10·P2-T11 소유; P2-T5는 live content를 변경하지 않음 |

## 완료 판정

- P2-T5 자동화 가능 영역은 모두 시도했고 미시도 0건이다. 순서 7 구현 범위의 blocking 결함·known gap은 없다.
- 사람의 실제 claim grounding은 P2-T5의 no-content-write 완료 술어가 아니며 P2-T10·P2-T11의 명시적 입력이다. 전체 파이프라인은 순서 8–12가 남아 있어 PASS로 판정하지 않는다.
- exact P2-T5 allowlist 23경로만 stage한 후 `check-sot-drift.sh --mode completion`을 재실행해 C2를 해소했다. inactive raw baseline 16경로는 untracked denylist로 보존했다.
- P2-T6 진입 전 P2-T5 변경을 독립 commit 경계로 고정해야 하며, 실제 commit·push는 별도 사용자 승인 범위다.
