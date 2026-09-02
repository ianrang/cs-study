# P2-T6 검증 보고서

## 완료 보고

- scope: 순서 8 deterministic materializer의 schema-derived index·overview·PageType template·단일 Obsidian Base 생성, Obsidian-canonical Base serialization·in-band formula ownership, independent semantic validation, repository checker 연결, directory-FD-bound atomic leaf apply와 exact replay 구현·검증.
- excluded: authored canonical page·raw content 수정, 순서 9–12, migration apply·restore·recover, commit·push.
- tests run: 전체 `pytest -q` 270 passed·11 skipped; Base ownership focused 7 passed, materializer·checker 관련 71 passed, requirement traceability focused 11 passed; canonical `check --all` structural PASS·findings 0; project lint HIGH 0·MEDIUM 0; `git diff --check` exit 0.
- real data: canonical active page 75, index link 75/75 unique, missing 0·extra 0, generated manifest 11. 두 render의 input SHA-256 `97b874e061ab6b4ad20aa0be8f7217b9774613034ec64d058c87760ee7db39c6`, output tree SHA-256 `609bda25526a99ac31fff267bb20834aab1523a4035ba39e3f1f0d82937f0659`가 동일했다. Base expected·actual SHA-256은 `5aeb21544ba998b14ba63a777968699dac9472acdbdf5134c1694c29ba65c89f`로 같고 Obsidian 1.13.7 open·save 뒤 SHA·mtime·size가 모두 불변이었다.
- changed files: tracked modified 25, P2-T6 관련 untracked 6, 사용자 소유 raw untracked 16. raw 16은 수정·stage·삭제·ignore하지 않았다.
- known gaps: none
- SoT sync: todo=P2-T6 `[x]`·verified report 연결; resume=`next_task: P2-T7`과 P2-T6 검증 증거·commit 승인을 갱신; memory=cleanup 범위가 아니므로 제외.
- Task Quality Gate: L3
- Task ID: P2-T6
- Intent: canonical schema·domain registry·active pages에서 정확히 한 generated view tree를 결정적으로 만들고 drift·경쟁·부분 적용을 탐지하거나 exact replay로 수렴시킨다.
- SoT: `docs/wiki-ingest-prd.md`, `docs/wiki-ingest-architecture.md` §4·§9·§10·§14, `docs/wiki-ingest-business-logic.md` BR-GEN·BR-CHK·VR-KP-017~019, `_meta/knowledge.schema.json`, `_meta/domains.yaml`, `_meta/knowledge-requirements.json`.
- Derived: `scripts/knowledge/materialize.py`, `scripts/knowledge/{schema,fs,check}.py`, `scripts/wiki_ingest.py`, 11 generated files, P2-T6 tests·review·본 보고서.
- Forbidden: authored canonical page·raw 수정, markerless leaf adoption/overwrite, unknown generated deletion, renderer-validator common-mode universe, duplicate registry, runtime wall clock·filesystem order, partial canonical write, unapproved commit·push.
- Invariants: exact `3 + |PageType|` manifest, active page coverage 100%, one runtime generator identity, strict UTF-8·finite JSON·display-safe input, pure deterministic render, independent validation before compare/write, shared lock, directory and leaf identity binding, temp bytes digest binding, atomic exchange/no-replace, own-leaf-only rollback/recovery, same-input exact replay.
- Completion Predicates: normal·edge·exception·race TDD, 명제·금지 surface mapping, generated parity, active coverage, DAG/call-depth ratchet, full regression, automated real-data two-run, review finding reconcile, raw 비접촉.
- Validation Plan: focused RED→GREEN, schema/registry mutation, renderer/validator mutation, parent/leaf/temp race injection, cleanup failure replay, CLI/check rule routing, exact manifest and Base parse, full suite, lint/static/diff, canonical check, two-run digest, external spec·standards·Claude recheck.
- User-required Gates: 구현·리뷰·교차검증 승인을 수신했고, 사용자는 Base 렌더링에 문제가 없다고 확인했다. 독립 commit은 별도 gate다.
- Promotion Candidates: marker ownership, strict schema/display 문자열, temp digest/inode/mode, managed-temp recovery, exact manifest, independent validator, CLI rule routing, call graph, requirement traceability owner boundary를 executable tests·checker registry로 승격했다. 추가 구현 결함용 후속 task는 없다.

## 계층별 필드 IO·영속성 판정

| 계층 | 입력 | 출력·영속 상태 | 일관성·원자성 근거 | 판정 |
|---|---|---|---|---|
| Canonical schema | `_meta/knowledge.schema.json`의 `Properties`·`PageType` | `schema.py`의 property·section·table·Base order contract | schema digest와 strict loader, schema-derived manifest | PASS |
| Domain registry | `_meta/domains.yaml`의 key·label·status | domain view name/filter와 overview count | unique YAML·정렬·active 상태 검증 | PASS |
| Domain parser | canonical Markdown frontmatter·tables | validated `DocumentInstance.properties`와 graph records | 같은 schema validator와 exact table contract | PASS |
| Materializer | validated records·registry·schema contract | 11개 expected in-memory bytes | pure render, exact manifest, independent semantic validation | PASS |
| Filesystem persistence | expected bytes·current generated leaf observation | `wiki/index.md`, `overview.md`, templates, 단일 Base | shared repository lock, directory/leaf/temp identity, atomic no-replace/exchange, own-leaf rollback·replay | PASS |
| Obsidian Base | Base YAML의 `filters`·`views`·bare property ID·`formulas._generated_by` | UI table columns와 view selection; Markdown canonical content는 변경하지 않음 | open·save SHA·mtime·size 불변, formula는 view `order` 밖 | PASS |
| DB·ERD·HTTP API·DTO | 해당 계층 없음 | 해당 계층 없음 | P2-T6 구현 surface는 filesystem CLI와 Obsidian derived view이며 product DB/API/UI form을 추가하지 않음 | N/A |

필드 흐름은 `title/page_type/summary/date_updated` 한 표기를 schema property → parsed `DocumentInstance.properties` → `BASE_TABLE_ORDER` → Base `views[].order` → Obsidian columns로 단방향 전달한다. `file.name`만 Obsidian file intrinsic field다. Base 내부 소유권 formula는 persistence metadata이며 `views[].order`로 전달하지 않는다. 별도 DTO·mapping table·sidecar·registry를 만들지 않아 변환 관리 지점은 `schema.py`의 generated contract 한 곳이다.

## Requirement Proposition Matrix

| ID | 검증 명제 | Source | 구현 근거 | 테스트·검증 근거 | 금지 surface 근거 | 판정 |
|---|---|---|---|---|---|---|
| P2T6-P1 | generated manifest는 index·overview·Base와 schema PageType별 template의 exact set이다 | `docs/wiki-ingest-architecture.md:91-110` | `scripts/knowledge/materialize.py:335-344`, `scripts/knowledge/materialize.py:511-544` | `tests/test_materialize.py:83-123`, `tests/test_materialize.py:316-345` | 별도 template registry·고정 page type list·extra marker leaf reject | PASS |
| P2T6-P2 | index는 active canonical page 100%를 한 번씩 열거하고 overview는 registry count만 소유한다 | `docs/wiki-ingest-business-logic.md:159-160` | `scripts/knowledge/materialize.py:162-215`, `scripts/knowledge/materialize.py:363-417` | `tests/test_materialize.py:126-146`; real 75/75 unique·missing 0·extra 0 | staging/archive/inactive/unregistered page 포함과 overview 목록 중복 reject | PASS |
| P2T6-P3 | template·Base 구조는 schema/registry contract에서만 파생한다 | `docs/wiki-ingest-architecture.md:104-110` | `scripts/knowledge/schema.py:25-31`, `scripts/knowledge/schema.py:350-380`, `scripts/knowledge/materialize.py:243-274` | `tests/test_materialize.py:126-190`, `tests/test_materialize.py:241-251`, `tests/test_materialize.py:316-345` | duplicate registry, custom domain Base, relocated marker reject | PASS |
| P2T6-P4 | 입력·출력 identity와 serialization은 결정적이고 연속 replay는 byte no-op다 | `docs/wiki-ingest-architecture.md:409-418` | `scripts/knowledge/materialize.py:45-68`, `scripts/knowledge/materialize.py:233-274`, `scripts/knowledge/materialize.py:493-508`, `scripts/knowledge/materialize.py:555-591` | `tests/test_materialize.py:83-123`, `tests/test_materialize.py:126-190`; real two-run tree digest와 Obsidian open·save SHA·mtime 동일 | wall clock·mtime·locale·filesystem enumeration order·YAML alias 배제 | PASS |
| P2T6-P5 | write는 parent/leaf/temp identity와 temp content를 결속하고 경쟁·중단 뒤 외부 bytes를 덮지 않는다 | `docs/wiki-ingest-business-logic.md:163` | `scripts/knowledge/fs.py:258-399`, `scripts/knowledge/materialize.py:633-718` | `tests/test_materialize.py:400-546` | markerless target/temp 삭제, symlink 추종, bytes-only rollback ownership reject | PASS |
| P2T6-P6 | checker와 CLI는 실제 generated parity·index coverage를 실행하고 candidate는 base→canonical overlay→candidate coverage 순서다 | `docs/wiki-ingest-business-logic.md:229-230` | `scripts/wiki_ingest.py:282-295`, `scripts/knowledge/check.py:281-301` | `tests/test_knowledge_check.py:33-39`, `tests/test_materialize.py:922-941`, `tests/test_materialize.py:944-1001` | 선언-only rule, candidate bytes와 current repository 직접 비교 reject | PASS |
| P2T6-P7 | malformed/non-finite/invalid UTF-8 schema, unsafe display 문자열, inactive domain은 public boundary에서 fail closed다 | `docs/wiki-ingest-business-logic.md:153`, `docs/wiki-ingest-business-logic.md:163` | `_meta/knowledge.schema.json:75`, `_meta/knowledge.schema.json:87`, `scripts/knowledge/schema.py:238-349` | `tests/test_materialize.py:726-832` | NaN/Infinity, multiline index entry, table-breaking label reject | PASS |
| P2T6-P8 | 신규 양방향·순환 의존은 없고 승인된 graph/call-depth를 증가시키지 않는다 | `docs/wiki-ingest-business-logic.md:231` | `scripts/wiki_ingest.py:40-45`, `scripts/knowledge/materialize.py:13-35`의 one-way imports | `tests/test_materialize.py:847-911`, `tests/test_knowledge_check.py:370-650` | reverse import·추가 edge/depth는 graph tests, duplicate AST checker loop는 `scripts/knowledge/check.py:152-190`의 단일 helper owner로 reject | PASS |
| P2T6-P9 | Base 소유권은 공식 YAML 내부에 정확히 한 번 존재하고 화면 열로 노출되지 않으며 markerless·malformed leaf는 채택하지 않는다 | `docs/wiki-ingest-business-logic.md:154-165` | `scripts/knowledge/materialize.py:53-68`, `scripts/knowledge/materialize.py:85-86`, `scripts/knowledge/materialize.py:264-274`, `scripts/knowledge/materialize.py:467-508`, `scripts/knowledge/materialize.py:633-662` | `tests/test_materialize.py:108-120`, `tests/test_materialize.py:156-190`, `tests/test_materialize.py:241-313`, `tests/test_materialize.py:581-597`; Obsidian 화면·open/save SHA 실측 | sidecar·registry·formula view order·pseudo marker overwrite/delete 금지 | PASS |
| P2T6-P10 | 문서 section·logic mapping과 FR/NFR step·implementation·verification mapping은 분리된 owner를 가지며 ID 누락·중복·열 역유입을 거부한다 | `docs/wiki-ingest-prd.md:165`, `docs/wiki-ingest-architecture.md:510-550`, `docs/wiki-ingest-business-logic.md:149` | `_meta/knowledge-requirements.json:1-42`, `tests/test_knowledge_schema.py:24-101` | `tests/test_knowledge_schema.py:441-648`의 정상·누락·중복·malformed·mapping 역유입·semantic-empty 11개 계약 | PRD·architecture 비정규/빈 의미 행과 manifest top-level·entry mapping 중복 owner 금지 | PASS |

## 리뷰 finding reconcile

- spec round 1~3: parent/leaf TOCTOU, independent validator, 실제 VR 실행, temp content binding, managed-temp replay, JSON Schema trailing newline anchor, stale temporary-tree 문구를 모두 코드·테스트·문서로 수정했다.
- standards round 1~3: inactive domain, strict schema, generator identity, actual call-depth, cleanup/rollback ownership, invalid UTF-8 registry, neutral fs vocabulary, AST contract 검사 중복을 모두 수정했다.
- Claude 최종 제한 재검사는 위 finding의 동일 반례만 대상으로 PASS를 반환했다. 추가 LOW였던 overview finding path 오귀속은 `tests/test_knowledge_check.py:33-39` RED 뒤 `scripts/knowledge/check.py:281-301`에서 실제 navigation path로 수정했다. call-depth의 두 CLI target이 현재 두 core root와 같은 점은 관찰이며, 실제 main 호출 대상 유도·두 호출 존재·core/CLI 최대 edge를 각각 강제하므로 결함으로 분류하지 않았다.
- 최초 실환경 Base 확인 뒤 Obsidian이 YAML 주석을 제거하고 alias를 전개하며 `note.*` order를 bare property ID로 저장해 generated parity가 깨지는 결함을 재현했다. Base ownership을 `formulas._generated_by` constant formula로 이동하고, alias-free sequence-indented serializer와 bare property ID를 TDD로 적용했다. markerless Base의 steady-state adoption은 추가하지 않았고 승인된 repository data transition으로만 현재 파일을 교체했다.
- 최종 ownership 적대 리뷰에서 unquoted·relocated pseudo formula를 generated ownership으로 오인해 existing Base를 덮어쓰고 managed temp를 삭제하는 HIGH를 재현했다. ownership 인식을 파일 시작의 exact canonical formula block으로 제한하고 current/temp 4개 보존 반례와 canonical stale-digest 교체를 회귀 테스트로 고정했다.
- 최종 spec 적대 리뷰에서 requirement manifest 소유권 문구는 정합했지만 validator가 architecture mapping과 분리된 열을 실행 검증하지 않는 MEDIUM을 재현했다. PRD·architecture·manifest의 header/body/top-level/entry/ID/semantic-empty 경계를 TDD mutation 10개와 정상 계약 1개로 고정했고, 반복 sibling 리뷰의 omission·duplicate·malformed·mapping 역유입·빈 의미 cell 반례를 모두 거부한다.

## 5계층 검증 판정

| 계층 | 실행 증거 | 판정 |
|---|---|---|
| 1 명제 | P2T6-P1~P10 source·implementation·test·forbidden surface mapping | PASS |
| 2 정적 | canonical findings 0, project lint HIGH 0·MEDIUM 0, 변경 production Python Ruff 통과, diff check, exact DAG/call graph | 오류 0 |
| 3 단위 | renderer, validator, schema/registry, requirement traceability, filesystem identity·rollback·recovery | 전체 270 passed에 포함 |
| 4 mock 통합 | CLI check/apply, candidate overlay, shared lock, partial apply/replay, failure injection | 전체 270 passed에 포함 |
| 5 자동화 실환경 | live canonical 75, exact generated 11, two-run digest, actual filesystem atomic exchange, Obsidian 1.13.7 open·save 뒤 Base SHA·mtime·size 불변과 generated parity 0 | 자동화 가능 영역 모두 시도·OK |
| 5 사용자 필수 | Obsidian vault Base 렌더링 | 사용자가 문제없음을 확인; 후속 자동화 screenshot에서 All active 75개와 canonical columns·formula 비노출 확인 |

## 완료 판정

- P2-T6 구현과 자동화 가능한 5계층 영역은 모두 시도했고 미시도 0건이다. generated data는 filesystem 파생 자산이며 DB·ERD·HTTP API·DTO·화면 입력 계층은 이 task에 존재하지 않는다. 영속성 transaction은 schema/registry/canonical Markdown read와 generated leaf filesystem write 경계로 검증했다.
- 사용자 소유 untracked raw는 현재 16 files이며 `sorted relative path + NUL + exact bytes` 지문은 `d8a2f9801babf1a08cfefe495159b3dd71a6ad168633d35610b6cbe801b0af6b`다. active session의 구현 전 snapshot과 같은 값이지만, 저장소 내부에는 별도 pre-work snapshot 파일을 만들지 않았다.
- 구현·실환경·spec·standards·grounding 교차검증과 독립 commit 승인을 충족해 P2-T6를 `[x]`로 전이했다. 전체 pipeline은 순서 9–12가 남아 있으므로 완료를 선언하지 않는다.
