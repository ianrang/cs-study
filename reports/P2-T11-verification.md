# P2-T11 검증 보고서

## Task Quality Gate Capsule

- Task Quality Gate: L3
- Task ID: P2-T11
- Intent: 순서 1–11이 반영된 현재 저장소의 full vault, 설계 명제, 코드 구조, 영속 artifact/page field, 작업 상태와 자동화 가능한 5계층 영역을 전수 감사해 최종 pipeline의 정합성을 판정한다.
- SoT: `todo.md:47`, `docs/wiki-ingest-architecture.md:499-517`, `docs/wiki-ingest-business-logic.md:213-257`, `docs/wiki-ingest-prd.md:24-44`.
- Derived: repository inventory·명제 coverage·DAG·field flow·vault·CI 실측, 최소 결함 정정, 본 최종 보고서, todo·resume closure.
- Forbidden: 사용자 소유 `raw/sources/clipping/` 8 bundle/16 files의 수정·stage·삭제·ignore, extractor 저장소 수정, 새 기능·schema·도메인·관리 원장 추가, historical evidence 재작성, 구조 검증을 의미 사실성 판정으로 확대, 미실행 영역의 PASS 처리.
- Invariants: 추출기와 wiki runtime import 독립, content-addressed no-overwrite artifact, strict plan→single-page apply, path-derived lifecycle, outgoing-only relation, generated 11-file 단일 owner, exact rule registry와 DAG, todo 단방향 선행, 동일 입력 replay 결정성.
- Completion Predicates: persistent inventory와 제외 조건 명시, 활성 PRD/architecture/BR·VR 명제 coverage GAP 0, schema→artifact→plan→page→generated field·digest 정합, canonical checker HIGH 0, repository lint HIGH/MEDIUM 0, generated drift 0, import cycle 0·설계 edge/depth exact, 전체 tests 성공, 실제 source·active page·GitHub CI 검증, 자동화 가능 5계층 미시도 0, spec·standards·grounding 적대 검토 findings 0, P2-T11 독립 commit·remote CI.
- Validation Plan: hidden 포함 Git·파일 inventory, schema·문서 ID·rule·module AST 정적 대조, 전체/집중/경계 테스트, full checker·materialize·lint·compile·Ruff, artifact와 active page 실데이터 검사, replay·hash 검사, GitHub run·branch status 확인, 독립 교차검증.
- User-required Gates: 사용자가 P2-T10 이후 P2-T11까지 전수 조사→분석→설계 검증→구현 필요 시 TDD→리뷰·교차검증→마무리를 연속 승인했다. 새 의미 정책 결정이나 사용자 환경 전용 검증이 발견되면 별도 gate로 올린다.
- Promotion Candidates: P2-T11에서 재현되는 L3 결함은 기존 owner의 last-leaf test·script·CI guard로 승격하거나 실제 owning task를 둔다. 단순 관찰을 형식용 후속 task로 만들지 않는다.

## Scope Contract

- Request boundary: 현재 cs-study 지식 파이프라인 전체의 데이터·코드·비즈니스 규칙·표현 surface와 작업 추적을 검증한다. GUI 제품 화면·DB·HTTP API는 저장소에 존재할 때만 검증하며 부재를 추론하지 않고 inventory로 판정한다.
- Symptom path: P2-T11은 보고된 단일 장애가 아니라 `docs/wiki-ingest-architecture.md:515`의 최종 검증 gate다. 진입 기준 commit `c60446c`의 `docs/wiki-ingest-review.md:136-173`에는 순서 10–12 상태가 과거 값으로 남아 있었다.
- Last-leaf candidate: 감사 보고서와 실제 stale 상태 문구. 코드·schema 변경은 재현 가능한 구현 결함이 있을 때만 별도 TDD로 허용한다.
- Allowlist draft: `reports/P2-T11-verification.md`, 실제 finding이 확인된 normative/review/todo/resume 문서와 그 명제를 고정하는 기존 테스트.
- Denylist draft: `raw/sources/clipping/**`, `raw/sources/video/**`, active wiki content, extractor 저장소, runtime code·schema·generated files는 실제 결함과 TDD RED 없이 수정 금지. clipping은 semantic inspection·mutation을 금지하고 integrity digest 산출을 위한 byte read만 허용한다.
- Entry unknowns: 진입 시 finding 수와 사용자 필수 영역 수는 미확인이었고, 아래 감사와 5계층 분류에서 해소했다.

## Requirement Proposition Matrix

| ID | 검증 명제 | Source | 구현·데이터 surface | 테스트·검증 surface | 금지 surface | 상태 |
|---|---|---|---|---|---|---|
| P2T11-P1 | 저장소 inventory와 사용자 소유 제외 경계가 완전하게 분류된다. | `todo.md:47`; 본 Capsule | Git status·tracked tree·runtime evidence | hidden/NUL-safe inventory·denylist digest | clipping semantic inspection·mutation·조용한 제외 | PASS |
| P2T11-P2 | schema→artifact→plan→page→generated field와 digest가 단일 계약으로 이어진다. | `docs/wiki-ingest-prd.md:35-44`; `docs/wiki-ingest-business-logic.md:183-207` | schema·artifact·page·manifest·renderer | schema mutation·artifact·lifecycle·materializer tests와 실데이터 | DB/API/UI 존재 추론·이중 schema | PASS |
| P2T11-P3 | module dependency는 설계 edge·depth와 일치하고 cycle·reverse coupling이 없다. | `docs/wiki-ingest-business-logic.md:235`; `docs/wiki-ingest-architecture.md:45-48,76` | `scripts/knowledge/`, CLI | AST graph·project boundary·import scan | extractor import·consumer별 guard 복제 | PASS |
| P2T11-P4 | 활성 FR/NFR/BR/VR은 구현 rule·test·금지 surface 근거를 가지며 모순·누락이 없다. | `docs/wiki-ingest-architecture.md:519-580`; `docs/wiki-ingest-business-logic.md:213-257` | normative docs·rule registry·tests | ID set·coverage·logic/spec/grounding review | historical rule의 활성 오인 | PASS |
| P2T11-P5 | full vault의 schema·graph·evidence·taxonomy·generated coverage가 HIGH 0이다. | `docs/wiki-ingest-prd.md:30-31`; `docs/wiki-ingest-business-logic.md:217-239` | canonical wiki·raw manifest·generated 11 files | checker all·repository lint·materialize check | 구조 PASS를 의미 PASS로 확대 | PASS |
| P2T11-P6 | capture·page operation·materializer replay가 동일 입력에서 결정적이고 멱등이다. | `docs/wiki-ingest-business-logic.md:231,237,243-255` | artifact bundle·PageWritePlan·generated tree | replay·tree hash·stale/failure tests | overwrite·암묵 write·multi-page command | PASS |
| P2T11-P7 | local·remote 검증 gate와 자동화 가능한 실환경 영역을 모두 시도한다. | `docs/wiki-ingest-architecture.md:513-515`; `docs/wiki-ingest-business-logic.md:175-176` | hook·workflow·GitHub required run | local commands·clean remote CI·branch status | local 결과로 remote 대체 | PASS |
| P2T11-P8 | todo·resume·review의 현재 단계와 완료 증거가 같은 단방향 상태를 표현한다. | `todo.md:46-47`; `docs/wiki-ingest-architecture.md:514-517` | todo·resume·review·reports | 상태/참조 grep·completion gate·SoT drift | 조기 완료·과거 상태의 현재화 | PASS |

## 감사 결과

### 저장소·데이터 경계

- 감사 시작 snapshot에서 `git ls-files -z` 기준 tracked 713개였고 `git ls-files --others --exclude-standard -z` 기준 untracked 17개 중 16개는 사용자 소유 clipping 8 bundle, 1개는 본 보고서였다. 감사 commit `0075659` 뒤 현재 종결 snapshot은 tracked 714개·untracked clipping 16개다.
- clipping 16개는 semantic content를 해석하지 않고 integrity 확인을 위해 bytes만 읽어 경로 정렬 뒤 파일별 SHA-256으로 다시 해시했다. denylist digest는 `fe2316435d1694c2c539ddad520f6739024910337af72af4d5a5f519c3a26e10`이며 감사 전후 동일하다.
- canonical Markdown은 76개다. 지정 영상은 2 bundle·6 files이며 두 payload SHA-256이 revision 디렉터리명과 일치한다. active page 1개가 두 manifest 경로를 `source_paths`로 가진다.
- 현재 canonical wiki tree SHA-256은 `8a13c8d752c09d6627b3d4b135ccad542cb1635498acf3405023345185f97041`이다. P2-T2 직후 해시를 현재 값으로 서술하던 문구는 historical 시점으로 한정했다.
- pipeline 실행 범위 `scripts/knowledge/`, `scripts/wiki_ingest.py`에서 SQL/DB 관련 파일 0개, HTTP/UI framework import 0개, extractor import 0개다. 이 검색은 `.git`만 제외하고 hidden을 포함했으며 저장소의 학습용 비pipeline 코드는 범위에서 제외했다.

### 아키텍처·규칙·작업 관리

- canonical architecture guard는 core+contract 10 modules·16 edges·cycle 0·최대 dependency edge 3, command-inclusive 12 modules·18 edges·cycle 0·최대 dependency edge 3을 검사한다.
- `RULE_REGISTRY`는 `VR-KP-001`~`VR-KP-023` 23개를 소유한다. PRD의 고유 ID는 FR 22개·NFR 15개·AC 14개로 합계 51개이며 외부 requirements checker 두 반복은 findings 0이었다. checker의 `requirements=52`는 고유 ID 분모로 해석하지 않는다.
- local `todo.md`는 14 task·직접 선행 edge 13·unknown/self dependency 0·cycle 0이고, `check-local-todo-dag.py`도 14 rows를 승인했다. 14개 중 10개 작업명이 60자를 넘지만 모두 기존 상세 실행 문장이라 현재 완료 이력을 축약하지 않는 LOW 관찰로 종결하며 신규 관리 task를 만들지 않는다.
- 현재 pipeline task P2-T1~P2-T11은 모두 완료됐고 열린 task는 0개다. P2-T11은 독립 감사 commit과 그 push·PR `verify` 성공 뒤에만 완료 상태로 전이했다.

### 발견·수정한 결함

| ID | 심각도 | 재현 | 수정·재발 방지 |
|---|---|---|---|
| P2T11-DOC-001 | HIGH | review·architecture가 순서 10–12를 미실행/GAP으로 두면서 P2-T11은 순서 1–11 반영을 전제했다. | 순서 10·11을 해소, 12를 진행 중으로 정합화하고 기존 normative-surface test에 stale 문구 부재·현재 문구 존재 assertion을 추가했다. |
| P2T11-DOC-002 | HIGH | P2-T2 직후 tree digest를 순서 11 이후에도 `현재 live wiki tree`라고 서술했다. | 문구를 `P2-T2 privacy 이행 직후` historical 관찰값으로 한정하고 현재화 금지 assertion을 추가했다. |
| P2T11-DOC-003 | HIGH | 순서 12를 진행 중이라면서 같은 문서가 `다음 진입 gate`로 표시했다. | `현재 완료 gate`로 단일화하고 진입/진행 시제 회귀 assertion을 추가했다. |
| P2T11-DOC-004 | HIGH | §10의 개념적 검증 계층 목록을 `CI 순서`라고 표시해 canonical CI profile의 실제 명령 순서와 충돌했다. | 목록을 실행 순서가 아닌 검증 계층으로 명명하고 실제 순서는 workflow·canonical CI profile만 소유하도록 회귀 assertion을 추가했다. |
| P2T11-DOC-005 | HIGH | P2-T11 완료 전이 뒤에도 resume 하단이 순서 12를 `다음 범위`로 지목해 상단 terminal 상태와 충돌했다. | 하단을 순서 1–12·P2-T11 완료와 명시적 신규 작업 원칙으로 정합화하고 stale 문구 부재 assertion을 추가했다. |
| P2T11-DOC-006 | HIGH | resume의 pipeline 첫 동작은 P2-T11 보고서를 요구하지만 중간 진입 절은 P2-T9 보고서를 우선 대상으로 남겼다. | pipeline 진입 read의 단일 소유자를 문서 상단으로 고정하고 중간 절은 정보보안 작업용 목록으로 한정했다. |
| P2T11-DOC-007 | HIGH | 감사 시작 당시 본 보고서가 untracked였던 17개 inventory와 종결 시점의 untracked 16개를 시점 구분 없이 함께 기록했다. | 시작 snapshot과 `0075659` 이후 종결 snapshot을 분리하고 tracked 713→714·untracked 17→16 전이를 명시했다. |
| P2T11-DOC-008 | HIGH | review의 현재 위험표가 P2-T6 당시 75-page universe를 현행 collision 분모로 유지했다. | 현재 canonical 76 files·basename duplicate 0 실측으로 갱신하고 75-page 문구 회귀 assertion을 추가했다. |
| P2T11-DOC-009 | HIGH | `P2-T6 historical 5계층 snapshot` 표의 결과 열을 `현재 결과`로 표시했다. | 열 이름을 `P2-T6 관찰 결과`로 한정해 historical/current 시점을 분리했다. |
| P2T11-DOC-010 | HIGH | resume의 보존 목록이 review 문서를 `구현 전 완료 기반과 잔여 구현 목록`으로 설명해 최종 판정 역할과 충돌했다. | 역할을 `구현 이력·해소 상태·최종 판정`으로 현재화하고 stale 역할 회귀 assertion을 추가했다. |
| P2T11-DOC-011 | HIGH | resume가 완료된 P2-T1~P2-T11을 `현재·후속 작업` 소유자로 남겨 열린 task 0 상태와 충돌했다. | 해당 그룹의 역할을 완료 이력·직접 선행·완료 증거로 한정하고 current/follow-up 소유 문구 회귀 assertion을 추가했다. |
| P2T11-DOC-012 | HIGH | resume의 PAGE-TYPE-MIGRATION 후보가 현행 schema 단일 계약과 무관한 89개 문서·legacy draft 경로를 후속 관리 대상으로 남겼다. | `_meta/page-type-spec.md`가 이미 현행 schema owner와 authored-source 제외를 선언하므로 obsolete 후속 후보 전체를 제거하고 부재 assertion을 추가했다. |
| P2T11-DOC-013 | HIGH | resume가 3-1~3-6을 2026-07-12 과거 이력으로 묶으면서 3-6의 현행 todo terminal 결과와 시점이 충돌했다. | historical 범위를 3-1~3-5로 축소하고 exact 범위 assertion을 추가했다. |
| P2T11-DOC-014 | HIGH | review 서두가 §7~§9를 최신 상태 owner로 선언하지만 §7은 P2-T6 historical snapshot이었다. | §7 historical·§8~§9 current로 owner 범위를 분리하고 회귀 assertion을 추가했다. |
| P2T11-DOC-015 | HIGH | P2-T10 구현 commit과 closure commit의 서로 다른 성공 run을 commit 표지 없이 비교하면 동일 증거 충돌로 해석됐다. | 구현 `cefc60a`의 두 run과 closure `c60446c`의 두 run을 commit별로 명시했다. |
| P2T11-DOC-016 | MEDIUM | resume가 P2-T10 구현 `cefc60a`를 `closure`로 표시해 실제 closure `c60446c`의 identity를 누락했다. | 구현·closure evidence를 별도 행으로 분리하고 두 commit·네 run identity를 회귀 assertion으로 고정했다. |
| P2T11-DOC-017 | MEDIUM | resume의 `본 세션에 미진입한 안건`에 P2-T4·P2-T11 완료 이력이 섞여 section 의미와 완료 이력 owner를 중복했다. | 완료 두 행을 제거하고 미진입 목록을 실제 외부-trigger 후보만 남기며 부재 assertion을 추가했다. |
| P2T11-TEST-018 | MEDIUM | DOC-016 회귀 검사가 두 commit만 확인해 네 GitHub run ID 변조를 탐지하지 못했다. | 구현·closure별 commit과 두 run을 각각 완전한 문장 assertion으로 고정했다. |

문서 결함 17건은 같은 `test_post_migration_normative_surfaces_use_current_contract_only`에 RED를 먼저 확인한 뒤 문서를 수정했고, 테스트 계약 결함 1건은 정확한 원격 identity assertion으로 보강했다. historical report·patch는 당시 증거이므로 수정하지 않았다.

## 결정적 검증 결과

| 게이트 | 결과 |
|---|---|
| cs-study 전체 | `uv run --with-requirements requirements-lint.txt python -m pytest -q` → 428 passed |
| full vault | `python scripts/wiki_ingest.py check --all --target-root wiki --report jsonl` → structural PASS, findings 0; semantic review는 별도 grounding으로 수행 |
| generated parity | `python scripts/wiki_ingest.py materialize --check` → exit 0; actual replay 2회 모두 created 0·replaced 0·unchanged 11, input `d0b660...b85`, output `c76bec...e9f`; 관찰 tree digest 3회 동일 `41f406...eb42` |
| repository static | `python scripts/lint.py --report jsonl`, `compileall`, Ruff `E9,F63,F7,F82`, `git diff --check` → exit 0 |
| extractor clean snapshot | `git archive 1891e0c...` 격리본에서 `uv sync --locked`, Ruff, `pytest -m 'not network'`, `uv build` → 194 passed·build 성공; Python 3.12.13 wheel install과 `ytscript --help` 성공 |
| remote gate | 두 main protection 모두 `strict=true`, `verify/app_id=15368`, `enforce_admins=true`; extractor `33600648908`·`33600652635`, P2-T10 구현 `cefc60a`의 push·PR `33624656646`·`33624661153`, P2-T10 closure `c60446c`의 push·PR `33625135719`·`33625140180`, P2-T11 commit `0075659`의 push `33631360562`·PR `33631364222` success |
| Obsidian | Obsidian 1.13.7에서 active page의 frontmatter·두 source path·Definition·timestamp links 렌더링을 자동 관찰했다. Base 내용은 이번 diff에서 변경하지 않았고 P2-T6 open/save bytes 및 사용자 시각 확인 증거를 재사용한다. |

## 5계층 판정

| 계층 | 상태 | 근거 |
|---|---|---|
| 1 명제 일관성 | PASS | P2T11-P1~P8 source→구현→테스트→금지 surface 매핑, 문서 모순 17건·테스트 계약 1건 정정 |
| 2 정적 분석 | PASS | checker·lint·Ruff·compile·diff·DAG·import inventory |
| 3 단위(mock) | PASS | 정상·edge·예외·mutation을 포함한 전체 428 tests |
| 4 mock 통합 | PASS | artifact→plan→page→materializer와 clean extractor 194 tests·wheel smoke |
| 5a 자동화 영역 | PASS | local Git·filesystem·CLI·Obsidian GUI·GitHub Actions/protection을 모두 시도; 미시도 K=0 |
| 5b 사용자 필수 영역 | 완료 | 이번 diff는 UI 디자인을 바꾸지 않으며 새 주관적 시각 판정 M=0; 기존 Base는 P2-T6 사용자 확인 완료 |

## 교차 검증 상태

- Claude full 4관점 2회에서 spec drift findings 0, grounding findings 0, requirements coverage findings 0을 받았다. logic 관점과 종결 교차검증은 stale 단계·진입 read·snapshot 시점·canonical 분모·문서 역할·historical owner·remote evidence 식별·section membership 충돌과 identity test gap을 검출했고 문서 17건·테스트 1건 정정으로 연결했다.
- 감사 commit `0075659` snapshot에서 Claude logic 2회는 fingerprint dedup 뒤 findings 0, Codex Spec은 P2T11-P1~P8 GAP 0/findings 0, Standards findings 0, Grounding citations 20/20·findings 0으로 수렴했다. 이후 closure delta는 같은 관점을 수정 뒤 재실행해 별도 종결 증거로 분리한다.
- 문서 17건·테스트 1건 정정 뒤 고정 closure working tree에서 Claude logic repeat 2는 findings 0, Codex Spec은 P2T11-P1~P8 GAP 0/findings 0, Standards는 findings 0이었다. exact closure commit의 원격 CI와 Grounding 재검은 자기 commit payload 밖 종결 gate로 분리한다.
- 최초 외부 실행 원본은 `$HOME/.claude/logs/agents/claude-agents.8iYfnn`, 중간 logic 재검증 원본은 `$HOME/.claude/logs/agents/claude-agents.XNSXAL`·`$HOME/.claude/logs/agents/claude-agents.4zgz4N`·`$HOME/.claude/logs/agents/claude-agents.mk6suX`·`$HOME/.claude/logs/agents/claude-agents.A7Vfuc`·`$HOME/.claude/logs/agents/claude-agents.xdzwnG`, `0075659` 최종 원본은 `$HOME/.claude/logs/agents/claude-agents.jkx4n1`, closure 최종 원본은 `$HOME/.claude/logs/agents/claude-agents.V6fBO5`에 보존된다.

Closure working tree 최종 Claude logic 원본 반환:

{"agent":"logic-proposition-checker","findings":0,"scanned":5,"abstain":false}

## 완료 보고

- scope: P2-T11 full vault·설계·코드·데이터·작업 상태·자동화 가능 5계층 최종 감사.
- excluded: 사용자 소유 clipping 8 bundle/16 files의 semantic inspection·수정·stage·삭제·ignore(무결성 digest용 byte read만 포함), extractor 변경, 저장소에 존재하지 않는 UI·DB·HTTP API의 구현.
- tests run: `uv run --with-requirements requirements-lint.txt python -m pytest -q` → 428 passed; full checker findings 0; materialize actual replay 2회 unchanged 11; lint·compile·Ruff·diff exit 0; extractor `1891e0c` clean archive에서 Ruff·194 tests·build·Python 3.12 wheel smoke 성공.
- changed files: task 전체 tracked=6개(`.claude/resume_prompt.md`, `docs/wiki-ingest-architecture.md`, `docs/wiki-ingest-review.md`, `reports/P2-T11-verification.md`, `tests/test_knowledge_check.py`, `todo.md`); task 밖 untracked=사용자 소유 clipping 16개.
- known gaps: none
- observations: extractor의 현재 `feat/screen-extraction` worktree는 사용자 변경으로 dirty라 수정·검증 기준에서 제외했고, P2-T9의 clean commit `1891e0c`를 격리 검증했다. 첫 wheel smoke가 시스템 Python 3.9.6으로 실패한 뒤 package의 Python ≥3.12 계약에 맞춘 3.12.13 환경에서 성공했다. 삭제 없는 정책 때문에 `/tmp/p2t11-extractor.9rXH1Q`, `/tmp/p2t11-wheel.VRKdW3`, `/tmp/p2t11-wheel312.A47wzt`를 자동 삭제하지 않았다.
- SoT sync: todo=P2-T11 completed; resume=열린 task 0·pipeline 완료로 갱신; memory=변경 제외.
