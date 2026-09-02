# P2-T9 검증 보고서

## 완료 보고

- scope: 두 저장소에 독립 local pre-commit feedback과 canonical required CI를 추가하고 실제 GitHub check를 main merge authority로 설정한다.
- excluded: 사용자 소유 raw clipping 16파일, P2-T10~P2-T11, UI·DB·API 변경.
- tests run: extractor `uv run ruff check src tests && uv run pytest -m 'not network' && uv build` -> 194 passed, Ruff·build exit 0; cs-study `uv run --with-requirements requirements-lint.txt python -m pytest -q && uv run --with-requirements requirements-lint.txt python scripts/wiki_ingest.py check --all --target-root wiki --report jsonl && uv run --with-requirements requirements-lint.txt python scripts/wiki_ingest.py materialize --check && uv run --with-requirements requirements-lint.txt python scripts/lint.py --report jsonl` -> 403 passed, structural findings 0, materialize·lint exit 0; 실제 GitHub Actions 3건 success.
- changed files: tracked=extractor commits `74b3038`, `1891e0c`; cs-study commits `381d3df`, `b6fe1b1` 및 P2-T9 closure 문서; untracked=사용자 소유 raw clipping 16파일.
- known gaps: none
- SoT sync: todo=P2-T9 completed·P2-T10 pending; resume=next_task P2-T10; memory=변경 없음.
- Task Quality Gate: L2
- Task ID: P2-T9
- Intent: local feedback과 원격 merge authority를 분리하면서 두 저장소의 검증을 상대 저장소 없이 독립 실행한다.
- SoT: `docs/wiki-ingest-prd.md:81,91,148,159`, `docs/wiki-ingest-architecture.md:447-460`, `docs/wiki-ingest-business-logic.md:174-175`.
- Derived: 저장소별 workflow·hook·runtime pin·dependency pin·README·repository-scope lint CLI·contract test·boundary test·requirements trace·검증 보고서.
- Forbidden: 상대 저장소 checkout/import/path, 공용 wrapper·registry, schema·canonical wiki·raw 변경, dirty screen-extraction worktree 변경, local hook을 merge authority로 간주.
- Invariants: workflow와 hook은 repository-local command만 조립하고, cs-study 검증은 staged Git index snapshot에 결속하며, P2-T10은 P2-T9 완료 전 시작하지 않는다.
- Completion Predicates: 두 clean snapshot required command 성공, reverse executable reference 0, hook 정상·edge·exception TDD, CI 명령·runner·action·Python pin 검증, 독립 commit 2개, 원격 actual check context의 required merge gate 설정.
- Validation Plan: 명제 matrix, Ruff·diff·workflow 정적 검사, focused TDD, 전체 단위·통합, 두 독립 clean snapshot, spec·standards·grounding·requirements 교차검증, 원격 API enforcement 확인.
- User-required Gates: 2026-09-02 사용자가 작업 마무리까지 연속 실행을 승인했다. 독립 commit, origin push, PR, 원격 branch protection 변경을 수행했다.
- Promotion Candidates: Git index snapshot·path·Git failure 반례를 `tests/test_ci_contract.py`, repository-local 검증을 workflow와 tracked hook, clean-checkout 부재 가정을 `tests/test_project_boundaries.py`로 승격했다.

## 결정적 검증 결과

| 게이트 | 결과 |
|---|---|
| extractor focused | `uv run pytest -q tests/test_ci_contract.py` -> 33 passed; `uv run ruff check tests/test_ci_contract.py` -> exit 0 |
| extractor full·clean | 194 passed, Ruff·build·hook exit 0 |
| cs-study TDD | 기존 hook 반례에 workflow inventory·trigger·permissions·job shape·runner·timeout·action pin·uv version·명령 순서 mutation RED/GREEN을 추가해 `tests/test_ci_contract.py` 50 passed |
| cs-study live full | 403 passed; full check structural PASS/findings 0; materialize·repository lint exit 0 |
| cs-study prior clean baseline | candidate `/var/folders/0g/dl33n9cs18b__dhpm4fstj7m0000gn/T/tmp.c2nNoywfqV` status 0건; 당시 376 passed; full check structural PASS/findings 0; materialize·repository lint·hook exit 0 |
| requirements trace | `python -m pytest -q tests/test_knowledge_schema.py -k requirement` -> 12 passed |
| reverse dependency | extractor runtime `cs-study|001_cs-study` 0건(`.git,.venv,dist` 제외); cs-study executable `youtube-script|007_youtube-script` 0건(`.git,.venv` 제외) |
| todo | `check-local-todo-dag.py todo.md` -> 14 rows OK; 구현 commit 직전 candidate는 staged 13개·tracked unstaged 0개였고 closure candidate는 문서 3개, 사용자 소유 raw untracked는 16개 |
| remote enforcement | extractor push run `33600648908`·PR run `33600652635`, cs-study push run `33600649200` success; actual `verify` check app ID `15368`; 두 main protection `strict=true`, `verify/app_id=15368`, `enforce_admins=true` 재조회 일치 |

## Requirement Proposition Matrix

| ID | 명제 | Source | 구현 근거 | 테스트·검증 근거 | 금지 surface 근거 | 상태 |
|---|---|---|---|---|---|---|
| P2T9-P1 | 두 저장소 검증은 상대 저장소 없이 독립 실행한다. | `docs/wiki-ingest-prd.md:81` | repository-local workflow·hook | 두 clean snapshot full command | executable reverse reference 0 | PASS |
| P2T9-P2 | extractor에는 cs-study 전용 hook·runtime dependency가 없다. | `docs/wiki-ingest-prd.md:148` | extractor `.githooks/pre-commit`, `.github/workflows/ci.yml` | architecture·CI contract·reverse grep | cs-study 문자열 runtime 0 | PASS |
| P2T9-P3 | local hook은 feedback이고 merge authority는 required CI가 소유한다. | `docs/wiki-ingest-prd.md:91`, `docs/wiki-ingest-architecture.md:447` | 두 hook·두 workflow·main protection | hook TDD·actual GitHub `verify` success·protection API | local hook 성공만으로 merge 허용하는 경로 0 | PASS |
| P2T9-P4 | cs-study CI는 schema test·full check·materialize parity·repository lint를 실행한다. | `docs/wiki-ingest-prd.md:159`, `docs/wiki-ingest-business-logic.md:175` | `.github/workflows/knowledge.yml` | live·clean 명령 exit 0 | command 생략 0 | PASS |
| P2T9-P5 | cs-study hook은 staged 상태와 실제 검증을 동일 Git index snapshot 및 single-owner canonical repository lint scope에 결속한다. | `docs/wiki-ingest-architecture.md:456-458`, `docs/wiki-ingest-business-logic.md:174` | `.githooks/pre-commit`, `scripts/lint.py` | hook 23개·scope owner/canonical/leaf identity 7개 정상·edge·exception contract test | worktree repair·untracked target 관찰·scope 복제·lexical path 우회·directory/single-file leaf symlink 타입 소실·mixed write-set 누락 금지 | PASS |
| P2T9-P6 | CI runtime·runner·action·trigger·권한·topology·순서는 canonical profile로 결정한다. | `docs/wiki-ingest-architecture.md:460`, `docs/wiki-ingest-business-logic.md:175` | 두 `.python-version`, 두 workflow | CI contract focused 83건(그중 required-CI mutation 54건)·actual action log | mutable action·filtered trigger·write permission·추가 job·순서 우회 0 | PASS |
| P2T9-P7 | clean checkout은 로컬 terminal migration evidence 존재를 요구하지 않는다. | `docs/wiki-ingest-architecture.md:456` | `tests/test_project_boundaries.py` | live·clean full suite | local evidence를 source contract로 오인 0 | PASS |

## 5계층 검증

| 계층 | 결과 |
|---|---|
| 1. 명제 일관성 | P2T9-P1~P7 모두 PASS; canonical CI profile source GAP 정정 후 Spec finding 0. |
| 2. 정적 분석 | Ruff·diff check·workflow contract·requirements trace·reverse dependency·todo DAG 통과. local `actionlint` binary는 미보유. |
| 3. 단위(mock) | extractor CI contract 33, cs-study CI contract 50을 포함한 정상·edge·exception contract test 통과. |
| 4. mock 통합 | extractor 194, cs-study 403 전체 suite와 checker/materializer/lint 통과. |
| 5a. 실환경 자동화 | local Git·uv·Python과 GitHub Actions push/PR 3건, check-run API, main protection API를 모두 시도했다. 자동화 가능 영역 미시도 0. |
| 5b. 사용자 필수 | 없음. UI·시각 결과와 사용자 실데이터는 P2-T9 범위가 아니다. |

## 교차 검증 결과

### Historical — required status 설정 전

아래 기록은 원격 merge authority를 설정하기 전의 순차 검증 증거다. `external_user_gate` ABSTAIN은 당시 상태를 보존하며 현재 판정이 아니다.

{"agent":"logic-proposition-checker","findings":0,"scanned":3,"abstain":false}
{"agent":"grounding-verifier","findings":0,"citations_checked":2,"abstain":false}
{"agent":"grounding-verifier","findings":0,"citations_checked":3,"abstain":false}
{"agent":"requirements-coverage-checker","findings":0,"requirements":52,"surfaces":20,"abstain":false}
{"agent":"grounding-verifier","findings":0,"citations_checked":19,"abstain":false}
{"verdict":"PASS","findings":0,"dimensions_checked":["두 worktree 최신 변경·신규 파일 17개","stdlib-only Python 3.9 bootstrap 호환","snapshot .python-version·requirements 단일 소비","lint·pytest·Git context 전체 index snapshot 결속","staged-valid/worktree-invalid requirements·Python 반례","untracked link·unstaged wiki/test repair 격리","leading-hyphen·공백·개행·삭제·rename 경로","Git non-zero·malformed·비 UTF-8·checkout-index 실패","extractor clean-index fail-closed","고정 runner·action SHA·Python patch","cross-repo 의존·순환·호출 깊이·결합","cs-study focused 22 passed·youtube-script focused 21 passed·두 저장소 shell syntax/diff check"],"abstain":false}
{"verdict":"ABSTAIN","findings":0,"propositions_checked":7,"abstain":true,"reason":"external_user_gate","detail":"로컬 P2-T9 명제 7개는 재검증했다: focused hook/CI contract 11 passed, staged 삭제 후 worktree 복원 rc=1, wiki .md→.txt+다른 Markdown rc=1, 공백·개행 경로와 index-only snapshot 반례 통과. 잔여 로컬 finding은 0건이다. 다만 두 GitHub main branch는 아직 protection HTTP 404·rulesets 0이며, workflow commit/push 후 실제 check context가 생성되어야 required status를 설정·검증할 수 있으므로 원격 merge-authority 2건은 미충족 사용자 게이트다."}
{"agent":"logic-proposition-checker","findings":0,"scanned":3,"abstain":false}
{"agent":"requirements-coverage-checker","findings":0,"requirements":52,"surfaces":21,"abstain":false}
{"verdict":"PASS","findings":0,"dimensions_checked":["최신 staged 13개 파일·tracked unstaged 0·사용자 raw 16개 비접촉","canonical_leaf_path의 resolved parent·original leaf identity","directory scope와 single-file AGENTS.md 내부·외부 symlink leaf","dot-segment·symlink ancestor·repository 외부 경계","regular·symlink·special-file inventory lstat","single-owner default_repository_paths·repository_lint_paths","Markdown 삭제 mixed write-set·scope 밖 Markdown filtering","index snapshot·bootstrap·Git context·dependency 결속","순환·양방향 의존·호출 깊이·중복·결합","focused 75 passed·shell syntax·staged/unstaged diff check"],"abstain":false}
{"verdict":"ABSTAIN","findings":[],"propositions_checked":7,"abstain":true,"reason":"external_user_gate","detail":"최신 staged 13개에서 로컬 P2T9-P1·P2·P4·P5·P6·P7의 source→implementation→test→forbidden 근거를 재대조했고 잔여 로컬 finding은 0건이다. tests/test_lint.py+tests/test_ci_contract.py 70 passed(47+23), staged index snapshot hook 6 passed/exit 0, git diff --cached --check 0, tracked unstaged 0이다. canonical_leaf_path는 parent만 resolve해 dot-segment·symlink ancestor를 scope 밖으로 거부하면서 directory/single-file leaf symlink identity를 inventory에 보존한다. 보고서의 staged13/nonraw0/raw16·live/clean376 수치도 현재 상태와 정합하다. P2T9-P3만 외부 사용자 게이트로 남는다: 두 원격 main의 actual workflow check context 생성 후 required status protection을 설정·API 확인해야 하므로 전체 완료 판정은 보류한다."}
{"verdict":"PASS","findings":[],"citations_checked":17,"abstain":false}
{"verdict":"PASS","findings":0,"scope":"standards","focused":{"extractor":33,"cs-study":50},"abstain":false}
{"verdict":"ABSTAIN","findings":[],"propositions_checked":8,"abstain":true,"reason":"external_user_gate","detail":"canonical CI profile source gap resolved; local finding 0. 원격 required status 설정 전 판정."}

### Current — required status 설정 후

- Spec: 실제 run 4건과 두 main protection을 독립 재조회했으며 원격 enforcement finding은 0건이다.
- Standards: action·uv literal은 테스트 파일별 단일 owner이고 workflow와 테스트 외 중복 owner는 0건이다.
- Grounding: 영속 file:line 17건, commit 4건, 지정 run 3건, check app ID와 main protection 값이 실제 상태와 일치한다.

## 판정

설계 명제, TDD, 전체 suite, 실제 GitHub Actions, check context와 main protection API가 일치한다. 두 저장소가 독립 `verify` required check를 merge authority로 사용하므로 P2-T9 완료 조건을 충족한다.
