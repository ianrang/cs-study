# P2-T4 검증 보고서

## 완료 보고

- scope: 순서 1–6b persistent snapshot 재분류·restage, validation-only Ruff/generated reconcile, 1~5계층 자동 검증, 구조·설계 교차검증, 별도 commit 승인 자료 작성.
- excluded: 순서 7–12 구현(P2-T5~P2-T11), inactive clipping revision 8개/16 files, terminal migration journal·candidate, authored 5개 tree, commit·push.
- tests run: `uv run --with coverage --with pytest --with jsonschema --with pyyaml coverage run -m pytest -q` -> 156 passed, 11 skipped; `uv run --with coverage coverage run projects/info-sec-engineer-practice/scripts/test-practice-contract.py` -> 27 tests OK; project Node·rendering·design-system·labs·generator·Chrome contract commands -> exit 0.
- changed files: tracked=385 staged paths; untracked=inactive clipping revision 16 files를 보존하고 stage·수정·삭제·ignore하지 않음.
- known gaps: none
- SoT sync: todo=P2-T4 `[x]` 및 verified report 연결; resume=P2-T5 next task로 갱신; memory=별도 세션 정리 작업이 아니므로 갱신 제외.
- Task Quality Gate: L2
- Task ID: P2-T4
- Intent: 순서 1–6b의 검증된 persistent snapshot만 정확히 stage하고 별도 사용자 commit 승인에 필요한 결정적 증거를 만든다.
- SoT: `todo.md:40`, `docs/wiki-ingest-architecture.md:424-442`, `.claude/resume_prompt.md:38-39`.
- Derived: persistent allowlist·inactive revision denylist, staged tree, 본 검증 보고서, commit 승인 자료.
- Forbidden: authored 5개 tree 변경, runtime journal·candidate stage·수정, inactive revision stage·삭제·수정·ignore, 순서 7–12 구현, migration apply·restore·recover, 승인 전 commit·push.
- Invariants: staging 전후 persistent worktree bytes 동일, runtime evidence 불변, active manifest 75개와 live wiki target 유지, inactive revision 8개/16 files 보존.
- Completion Predicates: persistent stage와 inactive denylist의 완전 분할, tracked unstaged·index/worktree mismatch·runtime stage·active personal path 각각 0, 자동화 가능한 5계층 전수 시도, 미해소 blocking finding 0, 별도 commit 승인 요청.
- Validation Plan: hidden-inclusive status parser, manifest set equality, index/worktree blob 비교, runtime digest·count, full pytest·coverage, Ruff, canonical/legacy lint, todo·SoT guards, browser contract, 구조·설계 교차검증.
- User-required Gates: P2-T4 restage·전체 검증·리뷰 실행 승인과 최종 staged snapshot의 commit 승인을 모두 수신했다.
- Promotion Candidates: 기존 privacy/runtime guard와 exact architecture graph test가 반복 결함을 기계 차단하므로 신규 관리 surface 없음.

## 구현 전 Task Quality Gate Capsule

- Task ID: P2-T4
- Task class: L2
- Intent: 순서 1–6b의 검증된 persistent snapshot만 정확히 stage하고 별도 사용자 commit 승인에 필요한 결정적 증거를 만든다.
- SoT: `todo.md` P2-T4, `docs/wiki-ingest-architecture.md` §13, `.claude/resume_prompt.md` P2-T4, 현재 Git index/worktree.
- Derived: persistent allowlist·inactive revision denylist, staged tree, 본 검증 보고서, commit 승인 자료.
- Forbidden: authored 5개 tree 변경, terminal migration journal·candidate 변경 또는 stage, inactive clipping revision 8개 stage·삭제·수정·ignore, 순서 7–12 구현, migration apply·restore·recover, 승인 전 commit·push.
- Invariants: worktree bytes는 staging 전후 동일하고, runtime journal SHA-256 3개와 candidate 255 files는 불변이며, active manifest 75개와 live wiki tree는 현재 target 상태를 유지하고, inactive revision 8개/16 files는 local untracked evidence로 보존된다.
- Completion Predicates: hidden-inclusive logical status를 persistent stage 집합과 inactive denylist로 완전 분할하고, tracked unstaged 0, staged/worktree byte mismatch 0, runtime tracked·staged·normal status 0, active personal-path offender 0, 전체 테스트·정적·실데이터·교차검증의 미해소 blocking finding 0을 확인한 뒤 별도 commit 승인을 요청한다.
- Validation Plan: porcelain-v1 `-z -uall` parser, active manifest reference 기반 set equality, index/worktree blob 비교, runtime digest·count, full pytest, Ruff E/F/I, canonical checker, legacy lint, todo DAG, completion·SoT drift preflight, architecture·design cross verification.
- User-required Gates: 사용자가 persistent 재스테이징·전체 검증·리뷰를 승인했고 staged diff와 메시지를 확인한 뒤 실제 commit도 별도로 승인했다.
- Promotion Candidates: 기존 `tests/test_project_boundaries.py`의 privacy/runtime guards와 `tests/test_knowledge_check.py`의 exact architecture graph guard가 반복 결함을 기계 차단하므로 신규 관리 surface를 만들지 않는다.

## Pre-edit Scope Contract

- 요청 요약: 기존 불완전 index를 폐기하고 검증된 순서 1–6b persistent snapshot으로 교체한다.
- 확인 코드 경로: `scripts/contracts/`, `scripts/knowledge/`, `scripts/wiki_ingest.py`, `tests/`, `_meta/`, `raw/`, `wiki/`, `projects/`, P2-T1~T3 보고서와 SoT.
- allowlist: 현재 hidden-inclusive status 중 P2-T1~T3 persistent snapshot으로 분류되고 inactive clipping revision denylist에 속하지 않는 경로, 본 보고서.
- denylist: `cs/`, `development/`, `coding-test/`, `lang/`, `tools/`, terminal migration journal 3개, journal-bound candidate root 3개, inactive clipping revision 8개/16 files, 순서 7–12 surface.
- dirty 분류: persistent pipeline·canonical migration·project relocation·SoT는 request-relevant; runtime evidence와 inactive revision은 unrelated local evidence; uncertain 0.
- 외부 영향: Git index와 검증 보고서를 새로 변경한다. 검증 중 발견된 Ruff E/F/I 8개 파일은 의미 변경 없이 정렬·미사용 변수만 정리하고, stale generated pair는 기존 generator로 재생성한다. schema·비즈니스 규칙·UI 로직은 변경하지 않는다.

## Requirement Proposition Matrix

| ID | 명제 | Source | 구현 surface | 검증 계획 | 금지 surface | 상태 |
|---|---|---|---|---|---|---|
| P2T4-P1 | P2-T2·P2-T3 뒤 persistent snapshot만 stage한다 | `todo.md:40` | Git index | status set partition·cached diff | runtime·inactive revision | PASS |
| P2T4-P2 | 기존 불완전 index를 commit하지 않는다 | `.claude/resume_prompt.md:87` | Git index | 기존 77 rename/52 mismatch 제거 후 mismatch 0 | 기존 index 재사용 | PASS |
| P2T4-P3 | 순서 1–6b 기준선 뒤에만 순서 7을 연다 | `docs/wiki-ingest-architecture.md:424-442` | todo·resume | P2-T4 `[x]`, P2-T5 next task | 순서 7–12 구현 | PASS |
| P2T4-P4 | raw bundle과 runtime recovery evidence의 보존성을 유지한다 | `AGENTS.md:24-35` | raw·ignored runtime | manifest verify·journal digest·candidate count | overwrite·삭제·stage | PASS |
| P2T4-P5 | 실제 commit은 별도 사용자 승인을 요구한다 | `.claude/resume_prompt.md:38-40` | commit gate | 메시지 self-grep·사용자 승인 | 승인 전 commit·push | PASS |

## Persistent stage 경계

- 기준 HEAD: `c7c1d919aad0fa1f9ef7713f0577161ab0a1a595`, branch `feat/knowledge-pipeline`.
- restage 입력 universe: active manifest 75개, physical clipping revision 83개, inactive revision 8개/16 files.
- 최종 persistent stage: 385 paths (`A 207`, `D 22`, `M 88`, `R 68`), staged path-set SHA-256 `7abe3e9324211cd8226740190e8006e29e89d68a556100035e1c807ce5e3dc33`.
- inactive denylist: 16 untracked files, path-set SHA-256 `ae3707b497945e550c42e6a9cd09c6e4b81108c69ac4ed828fedce33eb6b806a`; stage·삭제·ignore 0.
- index reset·restage 전후 기존 persistent worktree 379개 SHA-256 변경 0. 최종 staged ACMR 363개 index/worktree byte mismatch 0, staged delete 22개 worktree 잔존 0, tracked unstaged 0.
- staged authored tree(`cs/`, `development/`, `coding-test/`, `lang/`, `tools/`) 0, runtime path 0, inactive revision 0, symlink 0.

## 수정 및 TDD 증거

- 최초 Ruff 실행은 8개 Python 파일에서 import order·unused variable을 검출했다. 해당 위치만 정리한 뒤 staged Python E/F/I(`E501` 제외)가 0으로 종료했다.
- `test-practice-contract.py` 최초 실행은 회차 R10·R30의 stale `sourceDigest`로 1건 실패했다. 기존 `build-practice-data.py`를 실행해 `data/generated/past-exams.json`과 `practice-data.js`를 함께 재생성한 뒤 27 tests가 통과했고 `--check`도 0으로 종료했다.
- 두 생성물은 회차 MD·question pack의 파생물이며 직접 수정 금지다(`projects/info-sec-engineer-practice/README.md:35-43,55`, `projects/info-sec-engineer-practice/docs/past-exam-import-architecture.md:24-31,76`). 생성 도중 부분 drift는 canonical 손상이 아니며 기존 `--check`가 탐지하고 동일 generator 재실행으로 복구한다(`docs/wiki-ingest-architecture.md:347-352`). 별도 journal을 추가하지 않았다.

## 검증 결과

| 계층 | 실행 증거 | 결과 |
|---|---|---|
| 1 명제 | 위 P2T4-P1~P5의 source·구현·검증·금지 surface 대조 | P1~P5 PASS |
| 2 정적 | `git diff --cached --check`, Ruff E/F/I, canonical check, legacy lint, todo DAG, AI contract leak, SoT drift preflight | 오류 0; canonical structural findings 0; semantic review는 도구 계약상 not-performed |
| 3 단위 | root full pytest | 156 passed, 11 skipped |
| 4 mock 통합 | project contract 27, practice-core 6, rendering, design-system, labs syntax, generator `--check` | 모두 exit 0 |
| 5 자동화 실환경 | active manifest 75/75, resolution digest 75/75, active privacy offender 0, Chrome headless DOM contract | 모두 OK |
| 5 사용자 필수 | 사람 의미 grounding review | P2-T4 commit 경계의 자동 판정 대상이 아니며 순서 12(P2-T11)의 명시 입력으로 대기 |

- 현재 live wiki tree SHA-256: `ef5d0c42f08d1a5841a78633cb3e92adabc322e85eff8aeb5b87cf41bf0c6b21`.
- terminal journal 3개 SHA-256은 apply `97240f...`, reapply `1e76f7...`, restore `15cd21...`로 재검사 전후 동일했다. 결합 candidate는 3 roots/255 files이며 normal·tracked·staged status가 모두 0이다.
- 활성 clipping manifest는 75/75 검증됐고 active local-user-home offender는 0이다. 물리 revision 83개는 active 75개와 보존된 inactive 8개로 정확히 분할된다.

## 구조·설계 교차검증 reconcile

- design cross verification의 logic, spec drift, design token finding은 0이었다. 첫 requirements 실행은 `docs/prd.md:3`의 `Superseded` 표지를 무시해 historical FR/NFR을 current requirement로 판정했다. current SoT가 historical 문서를 non-normative로 지정한다(`docs/wiki-ingest-prd.md:12`). scope를 바로잡은 재실행은 requirements 37/surfaces 37/findings 0이었다.
- grounding verifier는 최종 보고서와 resume의 인용 18개를 검사해 findings 0을 반환했다.
- cycle detector는 실제 `scripts/` Python graph findings 0이었다. hyphenated 실행 파일 3개는 pydeps가 module name으로 처리하지 못해 별도 module-safe 이름의 byte-identical 임시 복제에서 project graph를 재실행했고 findings 0이었다. 원본 저장소 변경은 0이다.
- layer-depth 15개 경고 중 `knowledge_format_checker → is_canonical_datetime`는 callback 등록, `rule_coverage_findings → _artifact_findings`는 함수 레지스트리 참조라 실제 self-code 호출 edge가 아니다. 나머지 경고 경로는 command orchestration, inventory, 검증, parsing, digest처럼 서로 다른 경계를 소유하며 단순 pass-through가 아니다. project의 함수 5개 직렬(= edge 4)은 설계에 명시된 ratchet과 정확히 일치한다(`projects/info-sec-engineer-practice/docs/past-exam-import-architecture.md:34`, `docs/wiki-ingest-architecture.md:74`). 신규 경로가 이 값을 늘린 증거는 0이다.
- transaction finding 4개 중 OCR 2개는 staged diff 밖의 기존 임시-workdir 도구다. generated pair는 위 파생·재실행 계약으로 복구된다. preservation capture batch는 각 content-addressed bundle이 sibling temp에서 검증 후 atomic no-replace로 독립 게시되고 same digest replay가 no-op이다(`docs/wiki-ingest-architecture.md:331-337`); 여러 독립 revision의 all-or-nothing batch 계약은 없다. 미해소 transaction defect로 채택한 항목은 0이다.
- test-coverage-delta의 73개 direct-name finding은 private helper의 간접 실행을 테스트 부재로 간주했다. 실제 coverage 대조에서 unique function 72개 모두 실행됐고 30개는 executable lines 전부, 42개는 정상·엣지·예외 분기에 따라 부분 실행, 0-execution function은 0이었다. root 전체 line coverage는 80.26%, project contract coverage는 84.81%다. generator `main`은 별도 실명령 `--check`와 regeneration으로 실행했다.
- commit 전 신규 Python 식별자 감사 범위는 staged ACMR Python 28개 전부다. 함수·클래스 456개/unique 427개를 추출했고 non-test 동명이름 12종은 module-local helper(`_finding`, `_sha256`, `to_dict`, `validate`, `visit`), 실행 진입점 `main`, test-local failure injector로 분류됐다. 동일 클래스의 `*FilePath`/`*FileName` 병존은 0건이며 path 계열 변수 61개의 정의를 AST로 읽어 file·directory 역할을 대조했다. 프로젝트 용어집 검색은 `AGENTS.md`, `docs/`, `_meta/`, `projects/` 전체에서 0 match였으므로 설계 문서와 기존 다수 표기를 canonical로 사용했다.
- commit 직전 무의식적 추측 pattern은 staged ACMR 전 파일을 대상으로 155 matches(`재사용` 82, `추정` 48, `placeholder` 17, `같은 그룹` 6, `미확정` 2)를 전수 분류했다. immutable raw 인용과 그 generated mirror, HTML `placeholder` attribute, schema가 금지·검사하는 placeholder 용어, 위험분석·통계·프로토콜의 행위명, 불확실성을 명시하고 승격을 금지한 verification 기록이었다. 미확정 값을 확정 사실로 승격하거나 임시 label을 canonical 식별자로 사용한 항목은 0이었다. generated mirror는 generator `--check`, raw는 active manifest 75/75 digest, authored·설계 surface는 canonical checker·전체 테스트·grounding 검증으로 대조했다.

## 완료 판정

- 자동화 도구 inventory: Git, pytest/coverage, Ruff, canonical checker, legacy lint, todo/SoT guards, browser Chrome, manifest verifier, 9-agent review harness를 사용했다.
- 자동화 가능한 5계층 영역 미시도: 0건.
- 사용자 필수 영역: 의미 grounding review 1건은 P2-T11 소유이며 P2-T4 완료 술어가 아니다. P2-T4의 baseline commit 승인 gate는 충족됐다.
- 잔여 결함: 없음. 순서 7–12는 결함이 아니라 `todo.md:41-47`의 승인된 후속 범위다.
- commit·push: commit 승인은 수신했다. 본 보고서를 포함한 staged tree를 P2-T4 baseline commit으로 생성하며 자기 SHA는 commit object 메타데이터이므로 commit 직후 외부 결과로 보고한다. push는 범위 밖이다.
