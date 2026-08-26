# P2-T3 검증 보고서

## 완료 보고

- scope: terminal migration journal 3개와 journal-bound candidate root 3개를 디스크에 보존하면서 Git untracked·stage surface에서 제외하는 repository ignore guard를 TDD로 추가했다.
- excluded: runtime evidence 삭제·이동·내용 변경, raw recovery revision ignore, persistent snapshot stage, commit·push, migration apply·restore·recover는 제외했다.
- tests run: `uv run --with pytest pytest -q tests/test_project_boundaries.py -k terminal_migration_evidence` -> red 1 failed 뒤 green 1 passed; `uv run --with pytest --with jsonschema --with pyyaml pytest -q` -> 155 passed, 11 skipped; `uvx ruff check --select E,F,I --ignore E501 tests/test_project_boundaries.py` -> exit 0; `git diff --check` -> exit 0.
- changed files: tracked=`.gitignore`, `todo.md`, `.claude/resume_prompt.md`; untracked=`tests/test_project_boundaries.py`, `reports/P2-T3-verification.md`. journal 3개와 candidate 255 files는 ignored local evidence이며 내용 변경 없음.
- known gaps: none
- observations: P2-T4 persistent baseline staging·전체 검증·commit은 별도 사용자 승인 gate이며 P2-T3 결함이 아니다.
- SoT sync: todo=`P2-T3 [x]`와 본 검증 보고서 연결, `P2-T4 [ ]` 유지; resume=`next_task: P2-T4`와 runtime ignore 검증 수치 갱신; memory=todo·resume·본 보고서가 상태를 소유하므로 별도 memory 갱신 제외.
- Task Quality Gate: L2
- Task ID: P2-T3
- Intent: 복구 증거를 삭제하지 않고 우발적 stage·commit surface에서 결정적으로 격리한다.
- SoT: `todo.md` P2-T3, `.gitignore`, terminal journal 3개, journal-bound candidate root 3개, 현재 Git index·worktree.
- Derived: 세 ignore pattern, preservation·ignore·tracked-zero·staged-zero 회귀 테스트, 검증 보고서.
- Forbidden: runtime evidence 삭제·변경, broad `.wiki*` 또는 JSON 전체 ignore, raw artifact ignore, index 변경, stage·commit·push.
- Invariants: journal SHA-256 3개와 candidate file count 255는 P2-T1 기준과 동일하고, runtime root는 3 journal+3 candidate이며, Git tracked·staged runtime path는 0이다.
- Completion Predicates: six runtime roots exist, exact three patterns이 각 root를 match, normal porcelain runtime record 0, tracked·staged runtime path 0, journal digests와 candidate count 불변, full tests와 static checks 성공.
- Validation Plan: ignore 전 red, 최소 pattern 반영 후 green, `git check-ignore -v`, hidden-inclusive status, `git ls-files`, cached diff, digest·file count, full pytest, Ruff, diff check, todo DAG.
- User-required Gates: 사용자가 P2-T1 분류 뒤 P2-T2·P2-T3을 순서대로 수행하도록 승인했다. P2-T4의 stage·commit은 별도 승인 gate다.
- Promotion Candidates: `tests/test_project_boundaries.py::test_terminal_migration_evidence_is_preserved_and_git_ignored`가 runtime evidence 보존·ignore·tracked/staged-zero guard를 소유한다.

## 결정적 검증 결과

| 게이트 | 결과 |
|---|---|
| TDD red | ignore 전 `git check-ignore` exit 1, test 1 failed |
| TDD green | ignore 후 test 1 passed |
| ignore owner | `.gitignore` 17–19행의 journal·migration candidate·restore candidate 3 patterns |
| runtime roots | journal 3 + candidate 3 = 6 |
| candidate files | 255, P2-T1 기준과 동일 |
| journal SHA-256 | apply `97240f44…`, reapply `1e76f7bd…`, restore `15cd21f2…`; P2-T1과 동일 |
| `git check-ignore -v` | 6/6 matched |
| normal porcelain | runtime root match 0; 검색 범위는 hidden-inclusive 전체 status, 제외 없음 |
| tracked·staged | runtime path 각각 0 |
| 전체 pytest | 155 passed, 11 skipped |
| Ruff·diff | 둘 다 exit 0 |

## 판정

P2-T3의 자동화 가능한 정적·단위·실 repository 영역은 모두 시도했다. GUI·외부 서비스·사용자 주관 판정은 없으며, runtime evidence bytes와 복구 가능성은 보존된 상태다. 이 판정은 P2-T4 stage·commit 승인을 포함하지 않는다.
