# P2-T1 검증 보고서

## 완료 보고

- scope: hidden·untracked를 포함한 Git status universe를 전수 분류하고 unsafe index, persistent 절대경로, runtime recovery evidence, todo/resume drift를 식별해 순서 1–6b atomic baseline의 선행 작업과 직접 선행 DAG를 고정했다.
- excluded: source·wiki·raw·project content 수정, migration apply·restore·recover, git index 변경, commit·push는 P2-T2·P2-T3·P2-T4 소관이라 제외했다.
- tests run: `python3 ~/dev/dotfiles/scripts/check-local-todo-dag.py todo.md` -> exit 0, 14 rows OK; `bash ~/dev/dotfiles/scripts/check-completion-gate.sh reports/P2-T1-verification.md` -> exit 0; `bash ~/dev/dotfiles/scripts/check-sot-drift.sh --project-root "$PWD" --mode preflight` -> exit 1, C2 19개만 WARN; `bash ~/dev/dotfiles/scripts/check-ai-contract-leak.sh --all` -> exit 0; `git diff --check` -> exit 0.
- changed files: tracked=`todo.md`, `.claude/resume_prompt.md`; untracked=`reports/P2-T1-verification.md`; 기존 source·wiki·raw·project 변경은 수정하지 않았다.
- known gaps:
  - persistent repository 11 files의 로컬 사용자 절대경로 40회 remediation 미수행 -> 엔진 결함·parity / P2-T2
  - terminal journal·candidate의 repository ignore guard 미구현 -> 계획된 갭 / P2-T3
  - 순서 1–6b final persistent index 검증·atomic commit 미수행 -> 계획된 갭 / P2-T4
- SoT sync: todo=`지속 가능한 지식 파이프라인` P2-T1~P2-T11 등록; resume=`next_task: P2-T2`, `focus_group: 지속 가능한 지식 파이프라인` 및 현재 상태 갱신; memory=이번 상태는 todo·resume·본 보고서가 소유하므로 별도 memory 갱신 제외.
- Task Quality Gate: L2
- Task ID: P2-T1
- Intent: 변경 626건을 누락 없이 분류하고 안전한 commit 경계의 선행 결함과 owner를 결정적으로 고정한다.
- SoT: `todo.md`, `.claude/resume_prompt.md`, `docs/wiki-ingest-architecture.md` §13, `docs/wiki-ingest-review.md` §9, 현재 Git index/worktree.
- Derived: 변경 inventory TSV·JSON, atomic allowlist·denylist, P2-T2~P2-T11 직접 선행 DAG.
- Forbidden: source/runtime code·wiki·raw·project content 수정, existing staging 변경, journal·candidate 삭제·변경, migration apply·restore·recover, git add·commit·push.
- Invariants: Git status 626 records는 정확히 한 family에 속하고, staged 77 records와 journal 3개·candidate 255 files는 P2-T1 수행 전후 불변이며, todo와 resume의 next task·focus group이 일치한다.
- Completion Predicates: inventory 합계 626/626, task DAG cycle·unknown dependency·transitive edge 0, todo/resume stale 현재 상태 제거, P2-T1 known gap마다 직접 owner 존재, index와 비-SoT source bytes 불변.
- Validation Plan: porcelain-v2 hidden-inclusive inventory, todo DAG checker, completion report gate, SoT drift, stale·privacy grep, before/after index·source digest 비교, 독립 변경·SoT·commit-boundary 교차검토.
- User-required Gates: 2026-08-25 사용자가 todo/resume 정합화와 재검증을 승인했다. actual source remediation·staging·commit은 본 승인 범위에 포함하지 않는다.
- Promotion Candidates: persistent 절대경로 재발 방지 검사는 P2-T2, runtime evidence stage 방지 guard는 P2-T3이 소유한다.

## 결정적 검증 결과

| 게이트 | 결과 |
|---|---|
| local todo DAG checker | exit 0, task 14개, cycle·unknown dependency·transitive edge·warning 0 |
| completion report gate | exit 0 |
| SoT drift preflight | exit 1, C2 untracked implementation 19개 WARN; C3·C4·C5·C6 finding 0 |
| SoT drift completion | exit 2, 동일 C2 19개 BLOCK; P2-T4 baseline commit 전에는 repository completion 금지 |
| AI contract leak | exit 0 |
| stale resume 문구 grep | 0건; 검색 범위는 `todo.md`, `.claude/resume_prompt.md`, 본 보고서 전체이며 제외 없음 |
| persistent absolute path inventory | `raw/`, `wiki/` 전체 11 files / 40 matches; P2-T2 owner |
| runtime absolute path inventory | terminal journal·candidate 21 files / 79 matches; P2-T3 owner |
| index digest | `1e9cbfabf868cc4acf943456b49a48a30ab21d8d841b5dcb15d22b2cf4bff242`, pre-edit와 동일 |
| 비-SoT tracked diff digest | `aff71515d042bc2ae3b5717198bfcb2929d63385983d9afc53c597bb32d408f2`, pre-edit와 동일 |
| terminal journal digest | apply `97240f44…`, reapply `1e76f7bd…`, restore `15cd21f2…`; pre-edit와 동일 |
| confirmed defects entry check | exit 0, registry 부재로 skip |

`check-confirmed-defects.sh --mode preflight`은 지원하지 않는 mode라 exit 2였고, 사용법을 확인해 `--mode entry`로 정정 실행했다. 최초 오호출은 성공 증거로 사용하지 않는다.

## 교차 검증 결과

- 변경 전수 검토: 626/626 분류, runtime evidence 258개 denylist, staged rename 77개 중 RM 52개 확인.
- SoT 검토: 순서 7–12 owning task 누락, resume의 worktree·branch·구현 상태 drift 확인.
- commit 경계 검토: staged-only commit 거부, persistent 절대경로와 runtime ignore guard를 선행 gate로 확정.

## 판정

P2-T1의 분류·SoT 정합화·commit-boundary preflight 자동화 영역은 모두 시도했다. 확인된 구현·운영 gap은 P2-T2·P2-T3·P2-T4가 각각 소유하며 순서 7 진입은 P2-T4 뒤로 고정한다. P2-T1에는 사용자 실환경·주관 검증 영역이 없다.
