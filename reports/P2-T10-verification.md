# P2-T10 검증 보고서

## Task Quality Gate Capsule

- Task Quality Gate: L3
- Task ID: P2-T10
- Intent: 보존된 두 YouTube canonical transcript를 새 pipeline의 immutable artifact로 capture하고, 중복을 제거한 하나의 concept draft를 검토·승격해 active wiki에 배치한다.
- SoT: `docs/wiki-ingest-architecture.md:501-517`, `docs/wiki-ingest-business-logic.md:53-73`, `_meta/knowledge.schema.json:30-40,152-167`.
- Derived: video ArtifactBundle 2개, SemanticPlan 1개의 결정적 PageWritePlan, active concept page 1개, generated navigation, 검증 보고서.
- Forbidden: 원본 extractor worktree 수정, `git ls-files --others --exclude-standard -- raw/sources/clipping` 기준 사용자 소유 8 bundle/16 files 접촉, LLM의 direct Markdown write, 영상별 중복 page, 자동 merge, 미보존 URL만으로 verified 판정, 도메인 registry 변경, path guard를 consumer별로 복제, symlink·dot-component를 read 후 거부. 이 denylist의 sorted `sha256  path` 16행 집합 digest는 `fe2316435d1694c2c539ddad520f6739024910337af72af4d5a5f519c3a26e10`이다.
- Invariants: CLI·SemanticPlan source exact match, source ID·transcript video ID 일치, content-addressed no-overwrite, one semantic topic→one page, claim→declared manifest, review verdict→primary claim exact coverage, plan SHA·base tree·candidate revalidation, active path에서만 domain·lifecycle 파생.
- Completion Predicates: 두 source capture/replay 결과 일치, primary claim 1개 이상, 전 핵심 주장의 claim→manifest→timestamp→verdict coverage, manifest·payload를 읽기 전에 dot-component·raw trust anchor escape·그 아래 ancestor/leaf symlink·non-regular file 거부, multi-read·inventory를 하나의 bundle descriptor identity에 결속, draft plan/apply, draft bytes·verdict·promote SHA 제시 후 사용자의 명시적 승격 승인, promote apply/replay, active page·navigation 재생성, full checker findings 0, 전체 test·lint, 독립 commit·remote CI.
- Validation Plan: 명제 matrix, schema·hash·identity 정적 검증, capture/synthesize/promote 실환경 실행, replay·tree hash 멱등성, full test/check/materialize/lint, spec·standards·grounding 교차 검증.
- User-required Gates: 2026-09-02 사용자가 전수 조사부터 draft 생성·교차 검증까지 연속 실행을 승인했다. `promote --review-approved` apply는 실제 draft bytes·claim verdict·plan SHA를 제시한 뒤 별도 명시 승인을 받기 전에는 실행하지 않는다.
- Promotion Candidates: 실데이터 운영 리뷰에서 발견한 artifact path pre-read·FIFO blocking·bundle/ancestor identity·privacy inventory 결함을 `_meta/knowledge.schema.json`의 lexical contract, `knowledge.fs`의 descriptor-held context, fail-closed Markdown inventory, schema/fs/artifact/check/project-boundary 회귀 테스트로 실제 승격한다. 별도 follow-up task는 만들지 않는다.

## 경로 안전성 수정 계약

- Pre-edit Scope Contract: 수정 허용은 `_meta/knowledge.schema.json`, `scripts/knowledge/fs.py`, `scripts/knowledge/artifacts.py`, `scripts/knowledge/check.py`, `tests/test_knowledge_schema.py`, `tests/test_fs.py`, `tests/test_artifacts.py`, `tests/test_knowledge_check.py`, `tests/test_project_boundaries.py`, `docs/wiki-ingest-architecture.md`, `docs/wiki-ingest-business-logic.md`, 본 보고서다. schema digest 변경에 따라 `materialize`가 단독 소유하는 generated exact 11 files는 derived cascade로만 허용한다. 두 설계 문서는 새 path-safety invariant의 normative source를 한 번씩 보유한다. 사용자 clipping 16 files, video artifact 6 files, staging candidate, extractor 원본과 architecture module edge는 수정 금지다.
- Dirty 분류: P2-T10 관련은 video·active page·report·schema·설계·코드·테스트·schema-derived generated 11 files이고, 사용자 clipping 16 files는 unrelated/denylist다. staging candidate는 승격으로 제거됐으며 index·overview는 active page를 포함해 재물질화됐다.
- 외부 영향: ManifestPath·Descriptor·ArtifactManifest·AssetManifest의 영속 path component schema는 기존 안전 경로를 보존하면서 dot-component·backslash component만 추가 거부한다. schema digest marker 때문에 generated exact 11 files가 결정적으로 재생성된다. DB·API·DTO·화면 필드는 존재하지 않아 영향 0이며 production module edge는 추가하지 않는다.

| ID | 명제 | Source | 구현 surface | 테스트·검증 계획 | 금지 surface | 상태 |
|---|---|---|---|---|---|---|
| PATH-P1 | ManifestPath·descriptor·source ID component는 `.`·`..`·backslash를 허용하지 않는다. | `docs/wiki-ingest-business-logic.md:44`; `_meta/knowledge.schema.json:9-12,71,125,143` | `_meta/knowledge.schema.json:9-12,71,125,143` | schema 정상·dot·backslash 6 cases | consumer regex 복제 | PASS |
| PATH-P2 | manifest는 명시적 `raw` trust anchor 아래 regular non-symlink path임을 확인한 뒤에만 읽는다. | `docs/wiki-ingest-business-logic.md:44`; `docs/wiki-ingest-architecture.md:138` | `scripts/knowledge/fs.py:410-516`; `scripts/knowledge/check.py:505-520` | anchor escape·manifest/ancestor symlink·directory leaf·FIFO | resolve 후 외부 read·bundle별 anchor | PASS |
| PATH-P3 | payload·content·asset은 같은 `raw` trust anchor 아래 regular non-symlink leaf임을 확인한 뒤에만 읽는다. | `docs/wiki-ingest-business-logic.md:44`; `docs/wiki-ingest-architecture.md:133,138` | `scripts/knowledge/artifacts.py:132-180,199-204,340-356`; `scripts/knowledge/check.py:532-550` | traversal·bundle ancestor/payload/asset symlink·valid bundle | raw `Path.read_bytes()`·bundle별 anchor | PASS |
| PATH-P4 | artifact verifier·privacy inventory·canonical checker는 같은 path primitive와 `raw` trust boundary를 재사용한다. | `docs/wiki-ingest-architecture.md:76,138,140,320,333` | `scripts/knowledge/artifacts.py:14-22,132-180,340-356`; `scripts/knowledge/check.py:16-20,511-550`; `tests/test_project_boundaries.py:15-28,50-58,145-179` | sibling grep·architecture edge exactness | 별도 confinement 구현·축소된 anchor | PASS |
| PATH-P5 | 한 bundle의 manifest·descriptor leaf·inventory는 하나의 열린 directory chain identity에서 검증한다. | `docs/wiki-ingest-business-logic.md:44`; `docs/wiki-ingest-architecture.md:138` | `scripts/knowledge/fs.py:431-507`; `scripts/knowledge/artifacts.py:137-180,342-356`; `scripts/knowledge/check.py:511-550`; `tests/test_project_boundaries.py:151-166` | `tests/test_fs.py:82-109`; `tests/test_artifacts.py:275-309,549-597`; `tests/test_knowledge_check.py:1869-1901` | multi-read 사이 path 재개방·중간 ancestor 교체·consumer 예외 오역·production path `iterdir()` | PASS |
| PATH-P6 | privacy guard는 project·wiki·raw web Markdown을 non-symlink inventory 후 trust-anchor reader로만 읽는다. | `docs/wiki-ingest-business-logic.md:177`; `docs/wiki-ingest-architecture.md:140` | `tests/test_project_boundaries.py:50-58,112-129,145-179` | `tests/test_project_boundaries.py:80-109`; standalone 9/9 | `rglob` 결과의 direct `read_text`·symlink/FIFO read | PASS |

## 설계 고정

| 항목 | 결정 | 근거 |
|---|---|---|
| source universe | `tBRz9JonUUw` (`/Users/ian/dev/personal/007_youtube-script/out/tBRz9JonUUw/auto_sub.ko.json`, 75,856 bytes, 478 segments, `9ccab2007ecc554464250fb3b78f40f5daf5e68d6cf1dc423945cfef59be8577`) · `fsou1Butd6U` (`/Users/ian/dev/personal/007_youtube-script/out/fsou1Butd6U/auto_sub.ko.json`, 383,861 bytes, 2,414 segments, `2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045`) | 사용자 지정 URL·BR-SYN-001 exact match·capture payload byte equality |
| identity | provider-native video ID | ArtifactManifest `source_id`와 transcript `video.id` 동일성 guard |
| domain | `ai-engineering` | `_meta/domains.yaml`의 `development/harness/` hint와 강의의 agent runtime·harness 중심 주제 |
| page | `coding-agent-design-and-architecture`, `concept` | 두 영상이 연속 강의이고 동일 주제를 설명하므로 BR-SYN-004의 one-page 통합 |
| tags | `agent`, `architecture`, `tool-use` | `_meta/taxonomy.md`의 canonical vocabulary |
| assets | 추가 생성 안 함 | 핵심 명제와 근거가 transcript에 있고 시각 자료 없이 완전하게 표현 가능 |
| review status | 보존된 primary-source transcript artifact가 직접 지지하는 “강의자의 설명”만 `verified` | BR-CLM-003; 채널 메타데이터로 official 여부를 추론하거나 외부 보편 사실로 확장하지 않음 |
| promote scaffold | `wiki/domains/ai-engineering/` 부재·상위 일반 directory·non-symlink를 확인한 뒤 promote 직전에 하나의 directory만 생성 | `build_promote_plan` target-dir precondition; 최종 active page의 부모로만 소유 |
| transient lifecycle | SemanticPlan·synthesize plan·review verdict·promote plan은 격리된 `/tmp/P2-T10-run/`에만 두고 최종 보고서에 digest만 보존 | 저장소 추가 관리 표면 제거; 영속 산출물은 video bundle·active page·generated navigation·report로 제한 |

## Claim Grounding Matrix

| Claim | 핵심 주장 | Manifest | Transcript 구간 | Review |
|---|---|---|---|---|
| C1 | workflow·agent 제어 경계 | tBRz9JonUUw | 00:16:45–00:21:46 | support |
| C2 | request·iteration·turn·session | fsou1Butd6U | 00:14:05–00:19:37 | support |
| C3 | subagent의 별도 session 성격 | fsou1Butd6U | 00:32:13–00:38:37 | support |
| C4 | goal의 다음 turn 생성 | fsou1Butd6U | 00:49:08–00:51:49 | support |
| C5 | 통합 대기열 | fsou1Butd6U | 00:56:37–00:57:18 | support |
| C6 | tool·skill 책임 분리 | fsou1Butd6U | 01:08:45–01:12:55 | support |
| C7 | 외부 tool process protocol | fsou1Butd6U | 01:13:51–01:19:51 | support |
| C8 | 변경 영향 격리 | fsou1Butd6U | 00:39:51–00:45:38 | support |
| C9 | hook에 정책 분리 | fsou1Butd6U | 01:46:55–01:53:40 | support |
| C10 | 승인 피로와 system guardrail | tBRz9JonUUw | 00:10:24–00:16:34 | support |
| C11 | 4시·7시 context heuristic | fsou1Butd6U | 00:25:21–00:31:35 | support; 강의자 경험칙으로 한정 |
| C12 | 200B·Q5 경험 하한 | fsou1Butd6U | 01:40:17–01:45:03 | support; 보편 기준이 아님 |

편집 설계 질문은 `Open Questions`에서 영상 직접 발언이 아님을 명시하고 claim으로 승격하지 않는다.

## Requirement Proposition Matrix

| ID | 명제 | Source | 구현 근거 | 테스트·검증 근거 | 금지 surface 근거 | 상태 |
|---|---|---|---|---|---|---|
| P2T10-P1 | 두 지정 source만 immutable artifact로 보존한다. | `docs/wiki-ingest-architecture.md:507,514`; `docs/wiki-ingest-business-logic.md:53` | video ArtifactBundle 2개·6 files | 원본→payload `cmp` 2건 exit 0, manifest identity·digest 일치, capture replay 2건 `existing` | implicit latest·wiki re-ingest 0 | PASS |
| P2T10-P2 | 동일 연속 주제는 source trace 2개를 가진 page 1개로 통합한다. | `docs/wiki-ingest-business-logic.md:56`; `docs/wiki-ingest-architecture.md:514` | active concept page 1개·source path 2개 | full checker findings 0; source별 page inventory 1개; active 승격 완료 | source별 duplicate page 0 | PASS |
| P2T10-P3 | SemanticPlan은 쓰기 권한 없이 strict PageWritePlan으로 resolve된다. | `docs/wiki-ingest-business-logic.md:54-59`; `_meta/knowledge.schema.json:152-167` | 교정 SemanticPlan `abf1acaa91c5c0ac314a3ba60c82d71188337ce2ad98b75a080e553d9d62f459`; synthesize plan `99dfc4957b4c764a71c688b21e8f2d27eb305566bd09d9531a0d3ed6d6a48727`; staging output `f9d33e2ce2a79b1098767036b2aba5bf164c7d5219dd2c06929e6a7a3a1b36ef` | 동일 current state의 독립 plan 2개 byte `cmp` exit 0; strict apply·candidate checker exit 0 | direct active write·semantic path·frontmatter·operation 0 | PASS |
| P2T10-P4 | primary claim은 보존된 영상의 직접 지지와 exact review verdict를 갖는다. | `docs/wiki-ingest-business-logic.md:68-73,81-83` | C1–C12 `verified`; verdict file `f19efe9bb5cd32015a4c053865a245133e74d16f83b9c98a604a3f520dde1763` | transcript grounding 12/12 support, contradiction·insufficient 0 | URL-only·insufficient primary 0 | PASS |
| P2T10-P5 | 승격 후 active page와 파생 navigation은 full checker와 재실행 멱등성을 만족한다. | `docs/wiki-ingest-architecture.md:399-418,511,514`; `docs/wiki-ingest-business-logic.md:92-96,155-157` | schema-bound promote plan `a1e2dca4513533d8460c4ec6e30eca8cd0189851d93970b1b3da257f557b8c9f`; active candidate `f9d33e2ce2a79b1098767036b2aba5bf164c7d5219dd2c06929e6a7a3a1b36ef` | 승인 후 apply `applied`; materialize `replaced=2, unchanged=9`; check exit 0; exact replay `unchanged` | staging 잔존 0·generated drift 0 | PASS |

## 완료 보고

- scope: P2-T10 두 YouTube source의 artifact→draft→active integrated wiki 운영 처리와 evidence trace.
- excluded: 사용자 raw clipping 8 bundle/16 files, P2-T11 저장소 전체 최종 감사, UI·DB·API, extractor 원본 수정.
- tests run: `uv run --with-requirements requirements-lint.txt python -m pytest -q` → 428 passed; path-focused 5 files → 235 passed; `... python tests/test_project_boundaries.py` → 9 passed; `... wiki_ingest.py check --all ...` → findings 0; `... materialize --check`, `... scripts/lint.py --report jsonl`, `git diff --check`, `py_compile`, Ruff hard-error subset → exit 0.
- changed files: tracked=기존 추적 schema 1개·설계 2개·fs/artifacts/check 3개·tests 5개·schema-derived generated 11개·todo·resume; untracked=P2-T10 video ArtifactBundle 2개·6 files, active concept 1개, 본 보고서 1개. 사용자 raw clipping 8 bundle/16 files는 제외한다.
- known gaps: none
- observations: P2-T10 독립 commit·remote CI는 closure 절차로 이어지며 구현 결함이나 후속 task가 아니다.
- SoT sync: todo=P2-T10 in-progress·P2-T11 pending; resume=next_task P2-T10 closure; memory=todo·resume·본 보고서가 상태를 소유하므로 별도 갱신 제외.

## 검증 결과

- P2-T9 prerequisite repair: commit `585ce5e`; GitHub push run `33602403175`·PR run `33602408410` success.
- capture: source 2개를 bundle 2개·6 files로 생성; 원본→payload `cmp` 2건 exit 0; 동일 capture replay 2건 `existing`.
- synthesize: SemanticPlan `9bedb6ed44bb73d044035e62ce5d209d7a1b531526442f9cd9eebb6c6c89f563`; PageWritePlan 독립 2회 `74c9305cc0810ff381c3e0c7922c17ad1f40034da0e560a08304d4dfb1b283e5`, byte `cmp` exit 0; staging page SHA-256 `61c7c25808214809c318e73d5b2cb98aca2b84e3b2b0c89e742be2e1ca01ff37`.
- semantic review: C1–C12 12/12 support, contradiction·insufficient 0. 대기 전략의 정확한 시작은 transcript `01:22:50`이므로 SemanticPlan을 교정했고, strict synthesize plan/apply로 동일 SHA-256의 staging candidate를 다시 생성했다.
- promote plan: review verdict `f19efe9bb5cd32015a4c053865a245133e74d16f83b9c98a604a3f520dde1763`; plan `460fe723cf157d49c8458abc71f7e230d0daa28dd272663f93bcbaeab0c526ea`; one move, base=target content SHA-256 `61c7c25808214809c318e73d5b2cb98aca2b84e3b2b0c89e742be2e1ca01ff37`; `requires_review_approval=true`.
- initial promote: 사용자가 후보 `61c7c25808214809c318e73d5b2cb98aca2b84e3b2b0c89e742be2e1ca01ff37`와 plan `460fe723cf157d49c8458abc71f7e230d0daa28dd272663f93bcbaeab0c526ea`을 명시 승인했고 apply·materialize 후 replay는 `unchanged`였다.
- correction: grounding review에서 대기 전략 링크가 직접 발언보다 50초 앞선 것을 발견했다. transcript `raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/content.md:1794-1803`에 맞춰 `01:22:50`/`t=4970`으로 교정했다. 최초 active/generated delta를 pre-promotion 상태로 복구한 뒤 교정 SemanticPlan에서 strict synthesize plan 2개를 독립 생성해 bytes 동일성을 확인하고 plan `99dfc4957b4c764a71c688b21e8f2d27eb305566bd09d9531a0d3ed6d6a48727`을 apply했다. staging candidate SHA-256은 `f9d33e2ce2a79b1098767036b2aba5bf164c7d5219dd2c06929e6a7a3a1b36ef`이다.
- path-safety review: schema-valid dot component, symlink pre-read, FIFO blocking, bundle별 trust-boundary 축소, multi-read 사이 directory·중간 ancestor swap, consumer 예외 오역, privacy Markdown direct read를 TDD RED로 재현했다. schema 4 field, nonblocking descriptor-held directory chain context 1개, 명시적 trust anchor, fail-closed Markdown inventory, artifact·checker·privacy consumer를 정합화했다. trust anchor 상위의 운영체제 경로는 호출자 소유 범위이며, 그 아래 모든 열린 ancestor·bundle identity를 종료 시 재확인한다. production path 기반 bundle inventory와 project-boundary direct `read_text` sibling은 각각 0건(검색 범위 `scripts/`, `tests/test_project_boundaries.py`)이며, path-focused 235 passed·전체 428 passed다.
- promotion closure: schema-bound promote plan SHA-256 `a1e2dca4513533d8460c4ec6e30eca8cd0189851d93970b1b3da257f557b8c9f`, candidate SHA-256 `f9d33e2ce2a79b1098767036b2aba5bf164c7d5219dd2c06929e6a7a3a1b36ef`을 사용자가 명시 승인했다. apply는 `applied`; 활성화 직후 materialize 전 replay는 generated drift 2건을 write 없이 거부했고, 설계 순서대로 materialize(`replaced=2, unchanged=9`)·check 후 exact replay는 `unchanged`였다.
