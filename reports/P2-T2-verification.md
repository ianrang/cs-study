# P2-T2 검증 보고서

## 완료 보고

- scope: clipping Markdown의 Apple·Windows local-user-home prefix를 단일 privacy leaf에서 digest 전에 정규화하고, 8개 append-only revision·16개 live manifest reference·8개 resolution digest·tracked web source를 정합화했다.
- excluded: Linux `/home/**` 예시 정규화, 기존 8개 immutable revision 삭제·수정, terminal journal·candidate 변경, migration apply·restore·recover, git index·commit·push는 제외했다.
- tests run: `uv run --with pytest --with jsonschema --with pyyaml pytest -q` -> 154 passed, 11 skipped; `uvx ruff check --select E,F,I --ignore E501 <P2-T2 Python files>` -> exit 0; `python scripts/wiki_ingest.py check --all --target-root wiki --report jsonl` -> structural PASS, findings 0; `python scripts/lint.py --report jsonl` -> exit 0.
- changed files: tracked=`docs/wiki-ingest-{prd,architecture,business-logic,review}.md`, `tests/test_lint.py`, web source 1개, live wiki 8개, `todo.md`, `.claude/resume_prompt.md`; untracked=`scripts/contracts/privacy.py`, artifact·migration·CLI 구현, privacy·artifact·boundary·architecture tests, resolution, clipping revisions, 본 보고서. 기존 untracked recovery revision 8개는 수정하지 않았다.
- known gaps: none
- observations: P2-T3 runtime evidence ignore guard와 P2-T4 persistent baseline commit은 승인된 별도 후속 작업이며 P2-T2 결함이 아니다.
- SoT sync: todo=`P2-T2 [x]`와 본 검증 보고서 연결; resume=`next_task: P2-T3` 및 privacy 이행 수치 갱신; memory=todo·resume·본 보고서가 상태를 소유하므로 별도 memory 갱신 제외.
- Task Quality Gate: L3
- Task ID: P2-T2
- Intent: persistent repository에서 개인 local-user-home 경로를 제거하면서 raw immutability·digest identity·migration lineage를 보존한다.
- SoT: `docs/wiki-ingest-prd.md` FR-KP-003, `docs/wiki-ingest-architecture.md` §2·§5·§9, `docs/wiki-ingest-business-logic.md` BR-ART-001·002·010 및 BR-MIG-011~013.
- Derived: 8개 신규 clipping revision, live wiki manifest reference, resolution source digest, live wiki tree digest, 검증 보고서.
- Forbidden: 기존 revision overwrite·삭제, generic `/home/**` 치환, 별도 migration sanitizer, active personal path 허용, journal·candidate 변경, stage·commit·push.
- Invariants: source identity·target path·75개 active manifest 집합은 유지되고, normalization은 결정적·멱등이며, active manifest digest·size는 payload bytes와 일치하고, dependency cycle·최대 edge chain은 증가하지 않는다.
- Completion Predicates: active personal path offender 0, active manifests 75/75 검증, resolution manifest set과 active set 동일, physical revisions 83 중 기존 8개 보존, 전체 test·canonical check·lint 성공, 설계 명제와 graph 수치 정합.
- Validation Plan: TDD red→green, 정규화 정상·edge·예외, capture integration, hidden-inclusive persistent scanner, active manifest verification, resolution set equality, AST exact graph, full pytest, lint와 canonical check, diff·SoT review.
- User-required Gates: 2026-08-25 사용자가 privacy-normalized exact-byte 설계와 P2-T2 실행을 승인했다. P2-T4 stage·commit은 별도 승인 gate로 유지한다.
- Promotion Candidates: `tests/test_project_boundaries.py::test_persistent_markdown_does_not_expose_local_user_paths`가 active persistent 경로 guard, `tests/test_privacy_contract.py`가 leaf 결정성·멱등·금지 표면, `tests/test_knowledge_check.py`가 architecture exact graph를 소유한다.

## 설계 명제 커버리지

| ID | source | 구현 근거 | 테스트·실데이터 근거 | 금지 표면 근거 | 판정 |
|---|---|---|---|---|---|
| P2T2-P1 | BR-ART-010 | `scripts/contracts/privacy.py`, `scripts/knowledge/artifacts.py` | privacy unit·capture integration | non-UTF-8 reject | ✅ |
| P2T2-P2 | FR-KP-003 | normalized bytes로 digest·size·payload 생성 | active manifests 75/75 `verify_manifest` | normalization 전 digest 혼용 금지 | ✅ |
| P2T2-P3 | BR-MIG-011~013 | `scripts/knowledge/migration.py`의 공용 normalization leaf 소비 | resolution manifest set 75/75 active set과 동일 | 별도 migration sanitizer 0 | ✅ |
| P2T2-P4 | Append-only raw | content digest별 신규 bundle capture | physical 83 = active 75 + inactive 기존 8 | overwrite·삭제 0 | ✅ |
| P2T2-P5 | privacy persistent gate | active wiki·manifest payload·web scanner | active offender 0, placeholder 40회 | inactive recovery revision은 active scanner·stage 대상 제외 | ✅ |
| P2T2-P6 | NFR-KP-001·002 | `artifacts/migration → privacy` 단방향 leaf | 목표 10/14, 내부 9/14, command 12/18, cycle 0 | 최대 edge chain 3/2/4 불변 | ✅ |

## 결정적 검증 결과

| 게이트 | 결과 |
|---|---|
| TDD 최초 red | `ModuleNotFoundError: contracts.privacy` |
| privacy 범위 red | active persistent offender 11 files 검출 |
| 전체 pytest | 154 passed, 11 skipped |
| Ruff E/F/I | exit 0; E501은 기존 저장소 formatter 비적용 baseline과 분리 |
| canonical check | structural `PASS`, findings 0, semantic review `not-performed` |
| legacy/raw lint | exit 0, 출력 finding 0 |
| active artifact | unique manifest 75, verified 75, payload 75 |
| append-only artifact | physical clipping revision 83, inactive 기존 revision 8 보존 |
| privacy scanner | active offender 0; active placeholder 40회 |
| inactive recovery evidence | 8 files / 34 occurrences; active reference·검사·commit allowlist 제외 |
| reference parity | wiki manifest occurrence 150, unique 75; resolution manifest set과 exact equality |
| live wiki tree | `ef5d0c42f08d1a5841a78633cb3e92adabc322e85eff8aeb5b87cf41bf0c6b21` |

## 5계층 판정

| 계층 | 결과 |
|---|---|
| 1 명제 일관성 | 6/6 명제에 source·구현·test·금지 표면 매핑 |
| 2 정적 분석 | Ruff E/F/I, AST graph, persistent scanner, canonical checker 성공 |
| 3 단위 | privacy 정상·공백 profile·idempotence·Linux 보존·non-UTF-8 예외 성공 |
| 4 mock 통합 | capture·migration·manifest·lint 포함 전체 154 passed; canonical cutover 전용 11 tests는 현재 target 상태라 skip |
| 5 실환경 | 실제 75 active manifests와 live wiki·web source를 자동 검사해 offender 0, digest 75/75, resolution set equality 확인 |

P2-T2에는 GUI·외부 서비스·사용자 주관 판정이 없으므로 사용자 필수 5계층 영역은 0건이다. 의미론적 claim grounding은 P2-T2 privacy·persistence 범위 밖이며 전체 pipeline 완료 판정으로 확대하지 않는다.
