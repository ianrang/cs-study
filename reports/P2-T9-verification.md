# P2-T9 검증 보고서

## 완료 보고

- scope: 두 저장소에 독립 local pre-commit feedback과 required CI workflow를 추가하고 clean snapshot에서 저장소별 required command를 검증한다.
- excluded: commit·push·PR, GitHub main required status 설정, 사용자 소유 raw clipping 16파일, P2-T10~P2-T11, UI·DB·API 변경.
- tests run: extractor `uv sync --locked && uv run ruff check src tests && uv run pytest -m 'not network' && uv build && .githooks/pre-commit` -> clean snapshot 167 passed, Ruff·build·hook exit 0; cs-study `uv run --with-requirements requirements-lint.txt python -m pytest -q && uv run --with-requirements requirements-lint.txt python scripts/wiki_ingest.py check --all --target-root wiki --report jsonl && uv run --with-requirements requirements-lint.txt python scripts/wiki_ingest.py materialize --check && uv run --with-requirements requirements-lint.txt python scripts/lint.py --report jsonl && .githooks/pre-commit` -> 최종 single-file scope 반례 포함 live·clean snapshot 각 376 passed, structural findings 0, materialize·lint·hook exit 0.
- changed files: extractor 구현 commit `74b3038`; cs-study staged 13개(기존 tracked 수정 8개·신규 5개), tracked unstaged 0개, non-raw untracked 0개, 사용자 소유 raw untracked 16개.
- known gaps:
  - 두 원격 main branch의 required status protection이 없고 workflow actual check context도 아직 생성되지 않았다 -> 정책 변수화 미완 / P2-T9
- SoT sync: todo=P2-T9 pending(commit·원격 gate 전)·P2-T10 pending; resume=next_task P2-T9 유지; memory=변경 없음.
- Task Quality Gate: L2
- Task ID: P2-T9
- Intent: local feedback과 원격 merge authority를 분리하면서 두 저장소의 검증을 상대 저장소 없이 독립 실행한다.
- SoT: `docs/wiki-ingest-prd.md:81,91,148,159`, `docs/wiki-ingest-architecture.md:447-458`, `docs/wiki-ingest-business-logic.md:174-175`.
- Derived: 저장소별 workflow·hook·runtime pin·dependency pin·README·repository-scope lint CLI·contract test·boundary test·requirements trace·검증 보고서.
- Forbidden: 상대 저장소 checkout/import/path, 공용 wrapper·registry, schema·canonical wiki·raw 변경, dirty screen-extraction worktree 변경, local hook을 merge authority로 간주.
- Invariants: workflow와 hook은 repository-local command만 조립하고, cs-study 검증은 staged Git index snapshot에 결속하며, P2-T10은 P2-T9 완료 전 시작하지 않는다.
- Completion Predicates: 두 clean snapshot required command 성공, reverse executable reference 0, hook 정상·edge·exception TDD, CI 명령·runner·action·Python pin 검증, 독립 commit 2개, 원격 actual check context의 required merge gate 설정.
- Validation Plan: 명제 matrix, Ruff·diff·workflow 정적 검사, focused TDD, 전체 단위·통합, 두 독립 clean snapshot, spec·standards·grounding·requirements 교차검증, 원격 API enforcement 확인.
- User-required Gates: 2026-09-02 사용자가 P2-T9 설계 정합화 후 TDD 구현과 전수 재검증을 승인했다. 독립 commit 메시지, push·PR, 원격 branch protection 변경은 별도 승인 대상이다.
- Promotion Candidates: Git index snapshot·path·Git failure 반례를 `tests/test_ci_contract.py`, repository-local 검증을 workflow와 tracked hook, clean-checkout 부재 가정을 `tests/test_project_boundaries.py`로 승격했다.

## 결정적 검증 결과

| 게이트 | 결과 |
|---|---|
| extractor focused | `uv run python -m pytest -q tests/test_ci_contract.py` -> 6 passed; `uv run ruff check src tests` -> exit 0 |
| extractor full·clean | clean candidate `/var/folders/0g/dl33n9cs18b__dhpm4fstj7m0000gn/T/tmp.L57eKJORb5`에서 167 passed, Ruff·build·hook exit 0 |
| cs-study TDD | delete/rename·mixed write-set·index/worktree·untracked target·unstaged sibling/test repair·single-owner lint scope·dot-segment·symlink ancestor·directory/single-file leaf symlink·공백/개행/선행 하이픈·Git malformed/non-UTF-8/non-zero·snapshot failure·bootstrap drift를 RED 확인 후 `tests/test_ci_contract.py` 23 passed, `tests/test_lint.py` scope contract 7 passed |
| cs-study live full | 376 passed; full check structural PASS/findings 0; materialize·repository lint exit 0 |
| cs-study clean full | final implementation candidate `/var/folders/0g/dl33n9cs18b__dhpm4fstj7m0000gn/T/tmp.c2nNoywfqV` status 0건; 376 passed; full check structural PASS/findings 0; materialize·repository lint·hook exit 0 |
| requirements trace | `python -m pytest -q tests/test_knowledge_schema.py -k requirement` -> 12 passed |
| reverse dependency | extractor runtime `cs-study|001_cs-study` 0건(`.git,.venv,dist` 제외); cs-study executable `youtube-script|007_youtube-script` 0건(`.git,.venv` 제외) |
| todo | `check-local-todo-dag.py todo.md` -> 14 rows OK; staged 13개·tracked unstaged 0개·non-raw untracked 0개·사용자 소유 raw untracked 16개 |
| remote enforcement | `gh api`에서 두 main protection HTTP 404, rulesets `[]`; actual check context 생성 전이므로 미충족 |

## Requirement Proposition Matrix

| ID | 명제 | Source | 구현 근거 | 테스트·검증 근거 | 금지 surface 근거 | 상태 |
|---|---|---|---|---|---|---|
| P2T9-P1 | 두 저장소 검증은 상대 저장소 없이 독립 실행한다. | `docs/wiki-ingest-prd.md:81` | repository-local workflow·hook | 두 clean snapshot full command | executable reverse reference 0 | PASS |
| P2T9-P2 | extractor에는 cs-study 전용 hook·runtime dependency가 없다. | `docs/wiki-ingest-prd.md:148` | extractor `.githooks/pre-commit`, `.github/workflows/ci.yml` | architecture·CI contract·reverse grep | cs-study 문자열 runtime 0 | PASS |
| P2T9-P3 | local hook은 feedback이고 merge authority는 required CI가 소유한다. | `docs/wiki-ingest-prd.md:91`, `docs/wiki-ingest-architecture.md:447` | 두 hook·두 workflow | hook TDD·workflow contract | remote protection 미설정 | GAP |
| P2T9-P4 | cs-study CI는 schema test·full check·materialize parity·repository lint를 실행한다. | `docs/wiki-ingest-prd.md:159`, `docs/wiki-ingest-business-logic.md:175` | `.github/workflows/knowledge.yml` | live·clean 명령 exit 0 | command 생략 0 | PASS |
| P2T9-P5 | cs-study hook은 staged 상태와 실제 검증을 동일 Git index snapshot 및 single-owner canonical repository lint scope에 결속한다. | `docs/wiki-ingest-architecture.md:456-458`, `docs/wiki-ingest-business-logic.md:174` | `.githooks/pre-commit`, `scripts/lint.py` | hook 23개·scope owner/canonical/leaf identity 7개 정상·edge·exception contract test | worktree repair·untracked target 관찰·scope 복제·lexical path 우회·directory/single-file leaf symlink 타입 소실·mixed write-set 누락 금지 | PASS |
| P2T9-P6 | CI runtime·runner·action은 결정적으로 pin한다. | `docs/wiki-ingest-architecture.md:458`, `docs/wiki-ingest-business-logic.md:175` | 두 `.python-version`, workflow full action SHA, fixed runner | CI contract·actionlint | mutable action tag 0 | PASS |
| P2T9-P7 | clean checkout은 로컬 terminal migration evidence 존재를 요구하지 않는다. | `docs/wiki-ingest-architecture.md:456` | `tests/test_project_boundaries.py` | live·clean full suite | local evidence를 source contract로 오인 0 | PASS |

## 5계층 검증

| 계층 | 결과 |
|---|---|
| 1. 명제 일관성 | P2T9-P1~P7 중 6 PASS·1 GAP; 설계 교차검증 findings 0. |
| 2. 정적 분석 | Ruff·diff check·workflow contract·requirements trace·reverse dependency·todo DAG 통과. local `actionlint` binary는 미보유. |
| 3. 단위(mock) | extractor CI/hook 6, cs-study CI/hook 23·lint scope owner/canonical path/leaf identity 7 contract test 통과. |
| 4. mock 통합 | extractor 167, cs-study live·clean 376 전체 suite와 checker/materializer/lint 통과. |
| 5a. 실환경 자동화 | local Git index·worktree·uv·Python 3.9 bootstrap/3.12.13 validation·두 clean snapshot을 모두 시도했다. 자동화 가능 local 영역 미시도 0. |
| 5b. 사용자 필수 | commit 메시지 승인, push·PR, 원격 required status 설정과 API 재확인이 대기 중이다. |

## 교차 검증 결과

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

## 판정

로컬 구현·TDD·전체 검증·독립 clean snapshot·standards 교차검증은 통과했다. 원격 required check가 아직 merge authority로 설정되지 않았고 독립 commit 2개도 생성 전이므로 P2-T9은 완료가 아니라 pending 상태를 유지한다.
