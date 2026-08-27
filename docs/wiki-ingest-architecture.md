# Architecture: 지속 가능한 지식 파이프라인

## 1. 설계 범위와 전제

본 문서는 `docs/wiki-ingest-prd.md`의 전체 지식 파이프라인 구조를 정의한다. 1차 video importer의 v1 요구 계약과 실행 경로는 2026-08-23 순서 4 전환으로 superseded됐으며 digest revision 계약만 normative다. 두 저장 모델의 동시 쓰기는 금지한다.

설계 시작 기준선(2026-08-21, historical non-normative):

- extractor는 canonical JSON과 Markdown을 산출한다.
- cs-study는 extractor CLI를 subprocess로 호출하고 canonical JSON을 pull한다.
- 당시 2차 wiki ingest 실행 파일과 통합 테스트는 존재하지 않았다.
- 당시 wiki에는 안정 page ID, collection, relation의 machine contract가 없었다.
- 당시 dirty code/wiki 변경은 설계 작성 범위가 아니었다.

현재 전환 범위(2026-08-25, 순서 1–6b)는 immutable capture·target schema/parser/checker·migration inventory, 75-page preservation resolution·clipping capture·no-apply preview, external-reference no-write cascade planner와 resolved-plan·cascade-plan 결합 journal v2 apply·restore·recovery engine까지다. 결합 transaction의 실행 여부와 결과는 승인 digest, journal state, live wiki tree와 external digest vector로 판정하며 이 아키텍처 문서의 서술을 운영 상태 SoT로 사용하지 않는다. 현재 실행 surface와 최종 목표 surface는 §7에서 분리하고, 시점별 검증 evidence는 `docs/wiki-ingest-review.md`가 기록한다.

## 2. 아키텍처 원칙

1. **Ownership before automation**: 동일 규칙의 canonical owner는 한 곳이다.
2. **Canonical before derived**: 수동 입력과 재생성 가능한 결과를 구분한다.
3. **Pull boundary**: downstream consumer만 upstream artifact contract를 안다.
4. **Append-only raw**: raw identity는 capture-contract bytes digest이며 overwrite하지 않는다. clipping Markdown은 개인 로컬 홈 prefix를 결정적으로 치환한 bytes가 capture contract다.
5. **At most one knowledge page per ordinary apply**: 일반 lifecycle·page command는 no-op 또는 knowledge page 1개만 변경한다. 사용자 승인 전역 schema migration은 NFR-KP-015와 BR-MIG-001~015의 exact full-tree transaction·active 이전 참조 snapshot만 예외다.
6. **Outgoing-only graph**: inverse, backlink, transitive closure는 계산한다.
7. **Parse then validate**: Markdown을 deterministic instance로 변환한 뒤 표준 JSON Schema로 검증한다.
8. **Fail closed**: checker가 지원하지 않는 hard rule은 PASS가 아니라 unsupported failure다.
9. **Semantic humility**: 구조 검증과 사실성 검토를 분리한다.
10. **RDF export only on demand**: ontology 용어를 적용하되 RDF/SHACL을 canonical stack에 추가하지 않는다.

## 3. 시스템 경계와 의존 방향

```text
external providers
        |
        v
007_youtube-script
  extractor CLI -> canonical contract + payload
        |
        | versioned files only
        v
001_cs-study
  capture -> synthesize -> promote -> materialize -> check
```

금지 edge:

- extractor source code → cs-study package, path, schema, callback
- cs-study runtime → extractor Python module import
- promote → synthesize command 호출
- materialize → canonical wiki 수정
- checker → 자동 repair
- canonical page → backlink/inverse registry

목표 module DAG:

```text
wiki_ingest.py -> artifacts.py
wiki_ingest.py -> documents.py
wiki_ingest.py -> materialize.py
wiki_ingest.py -> check.py
artifacts.py -> schema.py
artifacts.py -> fs.py
artifacts.py -> privacy.py
documents.py -> schema.py
documents.py -> fs.py
materialize.py -> schema.py
check.py -> schema.py
check.py -> fs.py
check.py -> graph.py
schema.py -> timestamps.py
graph.py: validated DocumentInstance만 소비하며 project module import 없음
```

CLI entrypoint module끼리 import하지 않는다. 목표 core+neutral-contract 그래프는 10 modules, 14 directed edges, cycle 0, 최대 dependency edge chain 3이다. `fs.py`는 path confinement와 atomic leaf primitive의 canonical owner이므로 `check.py`가 confinement 검증을 위해 직접 의존한다. dependency-free `scripts/contracts/timestamps.py`는 canonical date-time predicate의 단일 owner이며 knowledge와 project가 단방향 소비한다. dependency-free `scripts/contracts/privacy.py`는 clipping Markdown의 local-user-home 정규화 단일 owner이며 artifact capture와 preservation migration이 단방향 소비한다. P2-T5 구현 뒤 내부 Python 전환 그래프는 9 modules, 17 directed edges, cycle 0, 최대 edge chain 3이다. 목표 edge인 `wiki_ingest.py → documents.py`, `documents.py → fs.py`, `documents.py → schema.py`가 활성화됐고 전환 전용 `migration.py → documents.py`가 아직 함께 존재한다. cascade planner의 실제 command edge와 project imports를 포함한 전환 command-inclusive 그래프는 12 modules, 21 directed edges, cycle 0, 최대 dependency edge chain 4다. edge 4는 NFR-KP-002 경고선의 승인된 transition ratchet이며 더 늘리지 않는다. AST architecture test는 목표 graph, 내부 전환 graph, subprocess target과 project import를 합친 command-inclusive graph를 각각 계산한다. 실제 수치가 다르면 문서를 임의 갱신하지 않고 설계 변경 게이트를 연다.

## 4. Canonical·Derived 소유권

| Concern | Canonical owner | Derived consumer |
|---|---|---|
| extractor output contract | `007_youtube-script/schemas/canonical-transcript-v1.schema.json` | cs-study의 pinned vendored copy와 contract fixture |
| artifact·draft·page structure | `_meta/knowledge.schema.json` | parser, renderer, materializer, checker |
| domain names·status | `_meta/domains.yaml` | index, overview, templates, Bases, domain validation |
| controlled vocabulary | `_meta/taxonomy.md` | tag/alias checker |
| raw payload identity | artifact `manifest.json`의 capture-contract byte digest | capture no-op와 evidence resolver |
| knowledge content | Markdown page | index, overview, Bases, Obsidian backlink view, checker graph |
| ordinary page transaction | `_meta/knowledge.schema.json`의 `PageWritePlan` | CLI plan SHA confirmation, checker candidate overlay, atomic leaf apply |
| collection membership | CollectionPage의 `Members` table | collection navigation view |
| relation | subject page의 `Relations` table | checker inverse/closure, Obsidian backlink view |

최종 목표에서 다음 파일은 generated-only다.

- `wiki/index.md`
- `wiki/overview.md`
- `wiki/templates/*.md`
- `wiki/views/*.base`

generated 파일에는 machine marker와 schema digest를 기록한다. checker는 임시 디렉터리 재생성 결과와 committed 결과를 byte 비교한다. `wiki/log.md`는 현재 legacy system page이며 순서 6a migration inventory에서 content migration 제외 대상으로만 취급한다. `wiki/log.md`, 현행 backlink 외부 인덱스 선언(`AGENTS.md` §Cross-link), 현행 provenance 외부 인덱스 선언(`_meta/frontmatter-spec.md` §human_authored 추적)의 제거는 순서 9 no-write plan과 별도 승인 후 apply가 소유한다. 두 외부 인덱스 파일은 현재 생성되지 않았다.

## 5. 데이터 모델

### Source identity

별도 Source registry를 만들지 않는다. 각 artifact manifest가 다음 source identity를 보유한다.

- provider-native immutable ID가 있으면 `{source_type}:{native_id}`를 사용한다.
- provider ID가 없는 legacy wiki preservation은 `logical_locator = "wiki/" + NFC(repo-relative legacy path)`, `source_id = SHA-256(UTF-8(logical_locator))`, `primary_source = logical_locator`로 고정한다. base tree와 payload revision은 source identity에 혼합하지 않고 resolution·resolved plan의 mapping과 `artifact_digest`가 각각 소유한다.
- source identity는 content identity가 아니다. 한 source는 여러 immutable artifact revision을 가질 수 있다.

### ArtifactBundle

| 속성 | 제약 | 의미 |
|---|---|---|
| `schema_version` | 지원 version | manifest contract |
| `source_type` | schema enum | video, web, paper 등 |
| `source_id` | non-empty | 논리 source identity |
| `artifact_digest` | `sha256:<64 lowercase hex>` | primary capture-contract bytes |
| `media_type` | non-empty | primary payload media type |
| `size` | non-negative integer | primary payload byte size |
| `payload` | bundle-relative safe path | immutable primary bytes |
| `created_at` | canonical date-time; 기본 producer는 UTC `Z` 생성 | capture activity time. preservation fallback은 ASCII 숫자, 대문자 `T`와 `Z` 또는 `±HH:MM`, 유효 달력·시각, 초 `00`–`59` subset을 허용한다 |
| `generator` | name+version | artifact 생성 activity |
| `primary_source` | URI 또는 local locator | provenance origin |

manifest는 generated descriptor이며 payload와 함께 immutable bundle로 commit된다. normalized Markdown이나 screen asset이 포함되면 각각 digest·size·media type descriptor를 가진다.

`source_type=clipping`이면서 `media_type=text/markdown`인 primary payload는 UTF-8이어야 한다. capture와 preservation migration은 digest 계산 전에 Apple `/Users/<profile>/` 및 Windows `<drive>:\\Users\\<profile>\\` prefix만 `<local-user-home>/` 또는 `<local-user-home>\\`로 치환한다. 일반 Linux `/home/**`, `/tmp/**`, `/var/**` 예시는 개인 경로로 단정하지 않고 그대로 보존한다. 이 정규화는 결정적·멱등인 `privacy.py` leaf가 단독 소유하며 기존 revision을 overwrite하지 않는다. 그 밖의 source type·media type은 입력 exact bytes가 capture-contract bytes다.

### KnowledgePage

- stable page ID는 전역 유일한 filename stem이다.
- ID는 kebab-case이며 생성 후 title·domain·path 변경과 무관하게 유지한다.
- 외부 source summary ID는 source identity를 정규화한 deterministic key를 사용한다.
- canonical properties는 title, page type, tags, created/updated dates, source manifest paths, summary의 최소 집합이다.
- domain과 lifecycle은 path에서 파생한다. `tier`, `shared_scope`, `source_count`, `provenance`, `domain_confidence`, `evergreen`을 공통 수동 필드로 두지 않는다.
- exact property 이름·타입·조건은 `_meta/knowledge.schema.json`만 소유한다.

초기 page 역할은 concept, entity, method, comparison, benchmark, dataset, source summary, collection이다. 구현 시 이 목록은 schema enum으로 이동하고 본 문서는 역할 설명만 유지한다.

### PageWritePlan

`PageWritePlan`은 SemanticPlan 또는 명시적 lifecycle command를 Python이 결정적 single-page transaction으로 resolve한 내부 strict schema instance다. 외부 LLM/사람이 write operation이나 rendered Markdown을 SemanticPlan에 주입하는 통로가 아니며, plan은 canonical JSON bytes의 SHA-256으로 승인과 apply를 결속한다. promote review verdict는 별도 canonical ReviewRecord page를 만들지 않고 exact plan에만 결속하며 Git review evidence와 함께 승인 경계를 이룬다.

| 필드 | 제약 | 의미 |
|---|---|---|
| `schema_version` | `1.0` | single-page transaction contract version |
| `operation` | P2-T5는 `synthesize`, `promote`, `collection-add-member`, `collection-reorder`, `move` | normalized command |
| `knowledge_root` | repo-relative knowledge root | plan을 다른 root에 적용하지 못하게 결속 |
| `schema_sha256` | lowercase SHA-256 | plan 생성 시 knowledge schema bytes |
| `base_tree_sha256` | knowledge page tree SHA-256 | plan 이후 다른 page 변경을 stale로 거부 |
| `target_tree_sha256` | candidate knowledge page tree SHA-256 | apply 결과의 결정적 tree identity |
| `input_sha256` | lowercase SHA-256 | SemanticPlan 또는 normalized command input identity |
| `generator` | name+version | replay identity |
| `requires_review_approval` | boolean | promote에만 true |
| `review_verdicts` | claim ID별 `support`, `contradiction`, `insufficient` | promote는 draft의 모든 primary claim과 exact match하고 다른 operation은 빈 배열 |
| `operation_input` | operation별 strict normalized object | apply가 invoked command와 semantic delta를 다시 검증하는 canonical input preimage |
| `write_set` | logical page operation 0 또는 1개 | source/target path·base/target digest·base/target UTF-8 Markdown bytes |

`operation_input`은 synthesize의 SemanticPlan digest·source_paths·page ID·date, promote의 source/target path·top-level verdict 배열의 canonical SHA-256, collection-add-member의 collection path·member ID·exclusive order policy, collection-reorder의 collection path·exact member sequence, move의 source/target path를 operation별 `additionalProperties=false` object로 보존한다. `input_sha256`은 이 object의 canonical JSON SHA-256이며 apply가 preimage와 digest를 다시 대조한다. promote는 top-level `review_verdicts` canonical bytes와 `review_verdicts_sha256`도 재대조해 서로 다른 review evidence가 같은 normalized input identity를 공유하지 못하게 한다.

`review_verdicts`는 `claim_id`와 `verdict`만 가진 `additionalProperties=false` object 배열이며 claim ID 오름차순으로 직렬화한다. primary claim ID마다 정확히 한 행, 비-primary claim은 0행이어야 하고 primary claim이 0개면 빈 배열이다. 중복·누락·입력 순서 drift는 plan 생성에서 거부한다.

write-set entry는 `action`, nullable `source_path`, `target_path`, nullable `base_sha256`, `target_sha256`, nullable `base_mode`, `target_mode`, nullable `base_content`, `content`만 가진다. path는 `knowledge_root` 기준 POSIX 상대 Markdown 경로이고 absolute·`..`·backslash를 허용하지 않는다. digest는 lowercase 64자리 SHA-256이고 mode는 `0..4095`(`0o7777`) POSIX permission integer다. create는 source·base digest·base mode·base content가 없고 target mode가 `420`(`0644`)이며 target이 계속 부재해야 한다. replace는 `base_content`의 SHA-256이 `base_sha256`과 같고 source와 target path가 같아야 한다. move는 중복 bytes를 저장하지 않고 `base_content=null`, `base_sha256=target_sha256`, target `content`를 base preimage로 재사용하며 source와 target의 filename stem이 같고 target이 계속 부재해야 한다. replace·move 모두 current source bytes·mode가 base와 같고 target mode가 base mode와 같다. replace base bytes를 plan에 결속하므로 collection replay도 operation-specific delta를 재검증할 수 있다. no-op plan은 빈 write-set만 허용한다.

knowledge page tree SHA-256은 `schema.py`가 소유하는 lexical document path 판별을 사용한다. knowledge root와 traversal 중간 directory는 `lstat` 기준 실제 directory여야 하며 symlink directory를 거부한다. 모든 `.md` directory entry는 generated/template 분류보다 먼저 `lstat`해 symlink·broken symlink·FIFO 등 non-regular entry를 fail-closed로 거부하고 tree digest 계산도 성공으로 반환하지 않는다. 이후 generated root page와 templates를 제외하고 path 오름차순 `{path, sha256}` 배열을 UTF-8 canonical JSON(`sort_keys=true`, separator `,`와 `:`, trailing newline 없음)으로 직렬화한다. 정상 page는 staging·domains·collections·archive 아래에 있어야 하지만, 다른 root나 hidden path의 Markdown도 digest와 checker universe에 포함해 invalid lifecycle path가 stale·검증을 우회하지 못하게 한다. plan 생성은 base tree에 write-set overlay를 적용한 target tree를 같은 함수로 계산한다. generated navigation·template·view, immutable artifact, migration rollback tree는 이 digest universe 밖이다. 이는 migration의 path·type·mode·bytes full-tree digest와 별도 계약이다.

BR-LIFE-003·BR-LIFE-004는 archive·restore의 목표 상태 규칙만 정의한다. 두 전이의 executable command와 PageWritePlan operation은 P2-T5 범위가 아니며, 별도 schema version·task 승인이 있기 전에는 `move`로 요청해도 거부한다. 따라서 P2-T5의 five-member operation enum은 archive·restore 전이를 구현했다고 의미하지 않는다.

### Claim

Claim은 page의 `Claims` table 한 행이다. ID는 page 내부에서 유일하다. `primary`, claim text, verification status, evidence manifest path, notes를 가진다. 상세 claim을 flat YAML property로 중첩하지 않는다.

### CollectionPage

CollectionPage는 일반 Markdown page이며 별도 collection registry를 갖지 않는다. `Members` table의 행 순서 자체가 canonical sequence다. 행은 member wikilink와 역할·순서 근거만 가진다. 숫자 position을 행 순서와 중복 저장하지 않는다.

2026-08-24 사용자 승인 A에 따라 현재 `wiki/collections/info-sec-engineer-practical-past-exams.md`는 migration에서 제외하지 않고 canonical universe에 포함한다. 목표 stable ID와 경로는 `wiki/collections/info-sec-engineer-practical-past-exams.md`, 목표 `page_type`은 `collection`이며 전체 canonical universe는 75개다. `_meta/knowledge-migration-resolution.json`이 target path·page type·source digest와 현재 index link 순서에서 승인된 52개 `Members` ID를 단일 machine-readable resolution으로 소유한다. role·rationale는 의미 추론을 하지 않고 빈 문자열로 보존한다.

### Relation

Relation은 subject page의 `Relations` table 한 행이다. 최소 관계는 broader, related, prerequisite-of, followed-by다.

- broader, prerequisite-of, followed-by는 directed edge다.
- related는 symmetric 의미지만 두 endpoint 중 ID가 사전식으로 작은 page만 저장한다.
- narrower, inverse, backlink, transitive closure는 저장하지 않는다.
- broader, prerequisite-of, followed-by는 relation type별로 각각 DAG를 강제한다.

### Asset

Asset은 content digest로 식별되는 파일이며 별도 entity page나 registry를 만들지 않는다. page가 asset path를 outgoing reference로 소유한다.

## 6. 문서 모델과 Obsidian 표현

```text
Markdown/YAML
  -> deterministic parser
  -> DocumentInstance
     {properties, ordered_sections, claims, relations, members, links}
  -> JSON Schema 2020-12
  -> cross-document graph checker
```

JSON Schema 표준 keyword가 소유하는 검증:

- property type, enum, required, conditional required
- page type별 ordered section array
- Claim, Relation, Member row structure
- local unique arrays와 ID/digest pattern
- unknown property/field rejection

cross-document checker가 소유하는 검증:

- page ID·basename 전역 유일성
- artifact manifest 존재·digest·size
- broken 또는 ambiguous wikilink
- duplicate inverse·symmetric ownership
- typed DAG cycle
- collection duplicate member
- active index coverage
- generated drift와 replay identity

임의 `x-*` keyword를 일반 JSON Schema validator가 검증한다고 가정하지 않는다. Markdown section order도 parser가 표준 JSON instance의 ordered array로 변환한 뒤 schema `prefixItems`, `const`, 길이 제약으로 검사한다.

Obsidian 표현 규칙:

- Properties는 flat scalar 또는 scalar list만 사용한다.
- stable ID와 filename stem을 같게 하여 `[[id]]`가 이동 후에도 유효하게 한다.
- basename 전역 유일성을 hard rule로 강제한다.
- backlink는 Obsidian의 계산 view로, Bases는 generated view로만 사용한다.
- template은 authoring 편의이며 validator가 아니다.

## 7. CLI와 모듈 구조

cs-study knowledge pipeline의 persistent write·plan·apply 단일 진입점은 `python scripts/wiki_ingest.py`다. read-only lifecycle validation dispatcher인 `scripts/lint.py`는 write 진입점이 아니다. legacy `scripts/pipeline.py`와 `scripts/ingest.py`는 2026-08-23 제거됐다. 독립 저장소의 ytscript extractor CLI와 cs-study의 무관한 도구 CLI는 이 단일 write 진입점 범위 밖이다.

현재 전환 CLI(순서 1–6b engine):

| Command | 상태 | persistent write 범위 | 역할·수명 |
|---|---|---:|---|
| `capture <artifact>` | 구현 | artifact bundle 1 | 최종 목표에도 유지 |
| `capture-asset <asset>` | 구현 | asset bundle 1 | 최종 목표에도 유지 |
| `check --all\|--changed` | 구현 | 0 | 선택한 target root 전체에 동일 rule-set 적용; 순서 6b 전에는 target fixture와 no-write migration tree만 입력하며 legacy wiki root를 호출하지 않음 |
| `migrate-plan --knowledge-root wiki` | 전환 전용 | 0 | canonical universe·exclusion·collision·reserved conflict와 exact tree manifest inventory |
| `migrate-capture-preservation` | 전환 전용 | immutable clipping bundle 최대 75 | 승인 resolution이 명시한 75개 경로에 one-artifact capture primitive를 각각 1회 적용한다. 암묵 scan은 없고 기존 digest는 no-op이다 |
| `migrate-resolve` | 전환 전용 | 0 | 75-page resolution·manifest를 target privacy-normalized bytes와 resolved plan으로 결정적 render |
| `migrate-preview` | 전환 전용 | 0 | operation payload의 content-addressed manifest binding을 독립 판별해 mode downgrade를 거부하고, preservation plan은 외부 temp tree에서 full checker·tree digest·payload parity·external reference blocker를 의무 검증한 뒤 preview를 atomic no-replace 게시 |
| `migrate-cascade-plan` | 전환 전용 | 0 | external reference를 고정 owner 정책으로 분류하고 question-pack은 `sourceRefs.path`만 변경하며 generated JS·past-exams JSON은 격리된 target tree에서 기존 generator로 함께 재생성한다. operation의 base/target bytes·mode와 `diff_sha256`을 결합한 plan·full diff를 sibling temp directory에서 완성한 뒤 하나의 approval bundle로 atomic no-replace 게시한다. plan은 독립 write 명령의 입력이 아니라 결합 migration transaction 입력이다 |
| `migrate-backup` / `migrate-verify-backup` | 전환 전용 | 0 | resolved plan과 exact tree path·type·mode·bytes를 묶은 exclusive backup 생성·검증 |
| `migrate-apply` | 구현·실행 결과는 journal 판정 | full `wiki/` exchange + cascade plan exact files | resolved plan·backup·cascade plan confirmation, preservation lineage, 결합 staged checker·generator·stale-zero 검증 후 journal v2가 external target과 wiki exchange를 함께 commit한다. active reference가 있는 migration의 cascade 없는 apply는 거부한다 |
| `migrate-restore` | 구현·실데이터 복제 검증 | full `wiki/` exchange + cascade plan exact files | post-apply tree·external target digest와 사용자 confirmation이 일치할 때 external base와 exact backup tree를 하나의 journal v2 transaction으로 복원한다 |
| `migrate-recover` | 구현·failure injection 검증 | full `wiki/` + cascade rollback 판정 | journal v1은 기존 두 tree digest로 복구한다. v2는 두 tree와 external digest vector가 유일하게 판별되는 경우에만 non-committed apply를 base로, non-committed restore를 restore 시작 상태인 target으로 복구하며 candidate는 자동 삭제하지 않는다 |

결합 transaction v2에서 자동 복구 가능한 non-conflict 상태와 허용 조합은 다음 표가 단일 기준이다. 여기서 base는 migration 전 wiki·external 조합, target은 migration 후 조합이다. 표에 없는 미지 조합은 아래 규칙에 따라 `CONFLICT`로 기록하며 자동 복구하지 않는다.

| operation | journal state | live wiki | live external | candidate wiki | 다음 동작 |
|---|---|---|---|---|---|
| apply | `PREPARED` | base | base | target | external target 기록 |
| apply | `EXTERNAL_WRITTEN` | base | target | target | wiki exchange |
| apply | `SWAPPED` | target | target | base | 결합 검증 후 commit |
| apply | `COMMITTED` | target | target | base 또는 보존됨 | terminal |
| apply | `ABORTED` | base | base | target 또는 보존됨 | terminal |
| restore | `PREPARED` | target | target | base | external base 기록 |
| restore | `EXTERNAL_WRITTEN` | target | base | base | wiki exchange |
| restore | `SWAPPED` | base | base | target | 결합 검증 후 commit |
| restore | `COMMITTED` | base | base | target 또는 보존됨 | terminal |
| restore | `ABORTED` | target | target | base 또는 보존됨 | terminal |

`PREPARED`, `EXTERNAL_WRITTEN`, `SWAPPED`에서 중단되면 recover는 operation의 시작 조합으로만 rollback한다. 각 external 파일이 plan의 base·target 중 하나로 식별되는 mixed vector는 부분 기록으로 판정해 operation 시작 상태로 rollback한다. 개별 external 파일이 base·target 어느 쪽에도 해당하지 않거나 wiki tree 조합이 표로 유일하게 판별되지 않으면 `CONFLICT`로 전이하고 자동 overwrite하지 않는다.

terminal state가 보존한 repository-top-level `.<knowledge-root>.migration.*`와 `.<knowledge-root>.restore.*` regular tree는 rollback artifact이며 active reference owner가 아니다. exact journal shape·canonical bytes·terminal state·knowledge root·candidate path와 state별 candidate tree digest가 결속된 root만 cascade scan과 staging에서 제외하고, prefix만 같은 unbound·nonterminal·digest-mismatched regular tree는 다른 hidden active owner와 동일하게 포함한다. current in-flight candidate는 호출자가 명시한 excluded root로만 제외한다. reserved root 자체가 symlink·special file이거나 내부 regular-tree 검증에 실패하면 제외로 우회하지 않고 거부한다.

최종 목표 CLI(순서 7–9 완료 후):

| Command | persistent write 범위 | 역할 |
|---|---:|---|
| `capture <artifact>` | artifact bundle 1 | capture-contract payload를 immutable bundle로 적재 |
| `capture-asset <asset>` | asset bundle 1 | content-addressed asset을 불변 적재 |
| `synthesize --semantic-plan <json> --source <manifest>... --page-id <id> --now <date> --output <plan>` | 0 | CLI source 목록과 SemanticPlan source_paths exact match, active domain registry, explicit stable ID를 검증하고 staging candidate PageWritePlan을 atomic no-replace 게시 |
| `synthesize --apply-plan <plan> --confirm-plan-sha256 <digest>` | staging page 0 또는 1 | plan·schema·base tree·target 부재와 candidate check를 재검증하고 draft 한 개를 atomic create |
| `promote <draft> --target-dir <dir> --review-verdicts <json> --output <plan>` | 0 | staging draft의 primary claim별 verdict를 결속한 content-preserving active-path move plan 게시 |
| `promote --apply-plan <plan> --confirm-plan-sha256 <digest> --review-approved` | page 0 또는 1의 path move | 검토 승인·stale·collision·candidate full check 뒤 draft를 active path로 이동 |
| `collection add-member <collection> <member> (--before <id>\|--after <id>\|--order-by-id) --output <plan>` | 0 | member 실재·중복·명시 순서 정책을 검증한 collection replace plan 게시 |
| `collection reorder <collection> --member <id>... --output <plan>` | 0 | 기존 member exact set을 완전 순서로 재배치하는 collection replace plan 게시 |
| `collection add-member\|reorder --apply-plan <plan> --confirm-plan-sha256 <digest>` | collection page 0 또는 1 | stale·candidate graph 검증 뒤 collection 한 페이지만 atomic replace |
| `move <page> <target-dir> --output <plan>` | 0 | 같은 lifecycle root 안에서 ID를 보존하는 move plan 게시 |
| `move --apply-plan <plan> --confirm-plan-sha256 <digest>` | page 0 또는 1 move | stale·collision·candidate graph 검증 뒤 ID 보존 이동 |
| `materialize` | generated-only | index, overview, templates, Bases 생성 |
| `materialize --check` | 0 | 임시 생성 결과와 repository 비교 |
| `check --all` | 0 | 전체 deterministic validation |
| `check --changed` | 0 | 변경 surface와 영향 graph validation |

`synthesize`의 외부 LLM/사람 입력은 SemanticPlan schema instance와 별도 CLI source·page ID·date다. SemanticPlan은 path, frontmatter, derived field, rendered Markdown, write operation을 포함할 수 없다. Python이 명시적 manifest와 current vault validation context에서 PageWritePlan을 재계산한다. `domain`은 SemanticPlan이 제안하는 배치 후보이고 active domain registry로 검증되며, 저장된 KnowledgePage의 domain·lifecycle은 최종 path에서만 파생된다.

모든 P2-T5 command는 plan mode와 apply mode를 배타적으로 제공한다. plan mode만 semantic·path·order 옵션을 받고 promote plan mode는 claim별 verdict JSON을 추가로 받는다. apply mode는 PageWritePlan과 confirmation만 받고 promote만 별도 `--review-approved`를 요구한다. apply는 plan을 다시 해석해 새 결정을 만들지 않고 invoked command·plan operation·plan bytes·schema digest·base tree·source/target precondition·candidate check를 재검증한다. 별도 ReviewRecord entity는 만들지 않는다.

현재 전환 모듈(순서 1–7 구현·재검증 완료):

| Module | 상태·수명 |
|---|---|
| `wiki_ingest.py` | 현재 argparse routing과 exit code |
| `knowledge/schema.py` | 구현된 target schema load·parse·instance validation |
| `knowledge/fs.py` | 구현된 path confinement·atomic no-replace·Darwin/Linux directory exchange primitive |
| `knowledge/artifacts.py` | 구현된 capture·asset capture·digest 검증 |
| `knowledge/documents.py` | preservation target serializer와 P2-T5 일반 lifecycle plan/apply 구현·검증 완료 |
| `knowledge/graph.py` | 구현된 link·relation·collection graph 계산 |
| `knowledge/check.py` | 구현된 target fixture·no-write tree checker |
| `knowledge/migration.py` | 전환 전용 resolution·capture request·preview, inventory, resolved-plan validation, external-reference no-write cascade plan, exact backup, full-tree candidate, apply·restore·recovery transaction owner; artifact capture·검증은 CLI가 sibling `artifacts.py`로 조합하며 승인된 순서 9 apply 뒤 제거 |

최종 목표 모듈 책임:

| Module | 단일 책임 |
|---|---|
| `wiki_ingest.py` | argparse routing과 exit code |
| `knowledge/schema.py` | schema load, Markdown→DocumentInstance parse, instance validation |
| `knowledge/fs.py` | path confinement와 atomic leaf replace |
| `knowledge/artifacts.py` | capture와 digest 검증 |
| `knowledge/documents.py` | synthesize, promote, collection, move |
| `knowledge/graph.py` | link/relation/collection graph 계산 |
| `knowledge/materialize.py` | generated view 렌더링 |
| `knowledge/check.py` | rule registry 실행과 finding 출력 |

단순 pass-through wrapper를 추가하지 않는다. command 함수는 shared schema/fs/graph leaf를 직접 호출한다.

## 8. 저장 구조

```text
007_youtube-script/
├── schemas/
│   └── canonical-transcript-v1.schema.json
├── src/ytscript/
└── tests/fixtures/contracts/

001_cs-study/
├── _meta/
│   ├── knowledge.schema.json
│   ├── domains.yaml
│   ├── taxonomy.md
│   └── contracts/
│       └── canonical-transcript-v1.schema.json
├── raw/
│   ├── sources/<source-type>/<source-id>/<sha256>/
│   │   ├── manifest.json
│   │   ├── payload.<ext>
│   │   └── content.md
│   └── assets/<source-id>/<sha256>/
├── wiki/
│   ├── domains/<domain>/**/<page-id>.md
│   ├── collections/<collection-id>.md
│   ├── staging/**/<page-id>.md
│   ├── archive/**/<page-id>.md
│   ├── index.md
│   ├── overview.md
│   ├── templates/
│   └── views/
├── scripts/
│   ├── wiki_ingest.py
│   └── knowledge/
└── tests/
```

vendored extractor contract는 downstream이 편집하는 SoT가 아니다. upstream `$id`, version, SHA-256을 기록한 pinned dependency이며 update command와 contract test로만 교체한다.

기존 `.claude/rules/structure-rules.md`의 authored tree 규칙은 `cs/`, `lang/`, `coding-test/`, `tools/`, `development/`에만 적용하도록 scope를 정정해야 한다. raw/wiki/schema tree에는 본 문서의 구조가 적용된다.

## 9. 트랜잭션·멱등성·동시성

### Artifact

- primary capture-contract bytes에서 digest를 계산한다. clipping Markdown은 §5의 privacy normalization을 먼저 적용한다.
- temporary sibling directory에 bundle 전체를 작성하고 검증 후 final digest directory로 atomic rename한다.
- final directory가 있고 모든 bytes가 같으면 no-op다.
- final directory가 있는데 bytes가 다르면 corruption으로 거부한다.
- 같은 source의 새 digest는 새 directory다. overwrite와 `--force`는 없다.

### Ordinary knowledge page command

- 일반 lifecycle·page command는 page 한 개만 수정한다. NFR-KP-015의 승인된 전역 schema migration은 §7의 full-tree transaction을 따른다.
- 모든 ordinary apply router는 invoked command와 exact `PageWritePlan.operation`을 결속한다. collection은 `add-member`와 `reorder`도 서로 교차 적용할 수 없다.
- plan은 knowledge page 전체 base tree SHA-256과 operation별 page precondition을 함께 요구한다. replace는 source base SHA-256·bytes를, create는 target 부재를, move는 source base SHA-256·bytes와 target 부재를 모두 기록하며 no-op은 page precondition이 없다.
- apply·migration apply/restore/recover는 `fs.py`가 교체되지 않는 repository-root directory descriptor에 제공하는 POSIX `flock(LOCK_EX|LOCK_NB)`를 공유하며, lock 획득 실패·미지원 플랫폼은 write 0으로 거부한다. knowledge-root directory exchange 전후에도 같은 repository-root inode가 lock authority다. OS descriptor close/process 종료가 lock을 자동 해제하므로 lock file·stale lock cleanup을 만들지 않는다. ordinary apply는 plan load부터 candidate check·commit·rollback/reconcile 종료까지 lock을 보유한다.
- lock 안에서 plan SHA-256·schema SHA-256을 확인하고 candidate check 직후 current tree와 source bytes·mode를 다시 확인한다. current tree·target page bytes·mode·move source 부재가 plan target state와 정확히 일치하는 replay는 idempotent no-op이고, base·target 어느 쪽도 아닌 tree는 stale-plan으로 write 0 거부한다.
- create는 canonical mode `0644`로 게시하고 replace·move는 plan에 결속된 기존 mode를 보존한다. namespace commit 뒤 directory fsync 또는 post-tree 검증이 실패하면 planned target bytes·mode가 그대로 관찰된 own leaf만 이전 상태로 복구한다. rollback 전에 관찰된 same-leaf 외부 변경은 덮지 않고 indeterminate로 중단하지만 관찰과 syscall 사이의 새 non-cooperative 경합은 POSIX content CAS 부재로 무손실 보장 범위 밖이다. in-process rollback 실패도 observed state를 포함한 indeterminate error다. process crash는 atomic namespace operation의 base 또는 target 중 하나로 남고 다음 exact replay가 판별한다.
- promote는 content를 변경하지 않고 staging page를 target으로 rename한다. lifecycle은 path에서 파생한다.
- create·replace·move candidate는 실제 write 전에 checker의 in-memory overlay로 full rule-set을 통과해야 한다. checker는 repair나 apply를 수행하지 않는다.
- collection add-member는 `operation_input`과 plan의 `base_content`를 대조해 Members에 빈 role·rationale의 정확히 한 행만 지정 위치에 추가하고 reorder는 동일한 member row 객체 집합의 순서만 바꾼다. 최초 apply와 target-state replay 모두 같은 delta validator를 통과해야 한다. Members table 바깥 raw bytes와 기존 member row field를 exact 보존하며 invalid·duplicate-member base를 repair하지 않고 거부한다.
- promote plan은 `--review-verdicts` strict JSON에서 draft의 모든 primary claim ID에 verdict 하나를 요구한다. `support`는 claim status `corroborated`·`verified`, `contradiction`은 `rejected`와만 결속하고 `claimed` primary 또는 `insufficient` verdict는 apply를 거부한다. verdict는 promotion-time authorization evidence이고 active page에는 persistent claim status가 남는다. 장기 audit는 Git review와 P2-T5/P2-T11 검증 보고가 소유하며 별도 ReviewRecord·중복 wiki field를 만들지 않는다.
- P2-T5 move는 같은 lifecycle root 안에서만 허용한다. staging→active는 review-approved promote가 소유하고, active→archive와 archive→staging은 P2-T5에서 unsupported이므로 move로 우회하지 않는다.

### Generated surface

- materializer는 deterministic sort와 normalized newline·YAML serialization을 사용한다.
- 전체 결과를 temporary tree에 생성하고 validation한 후 generated 파일만 교체한다.
- 중간 실패는 knowledge page를 변경하지 않는다.
- 부분 generated drift는 `materialize --check`가 탐지하고 재실행으로 복구한다.

### Replay identity

멱등성 key는 URL·filename 존재가 아니라 입력 digest, schema digest, generator version, normalized command options의 tuple이다. wall clock은 `--now`로 주입하며 content가 변하지 않으면 `date_updated`를 바꾸지 않는다.

## 10. 검증 아키텍처

`check`는 현재 활성 normative rule-set의 모든 hard rule을 보고한다. active normative 문서에 hard rule이 선언됐지만 구현 rule ID가 없으면 `UNSUPPORTED_RULE` HIGH finding으로 실패한다. historical·superseded 절과 구현·검증 surface가 아직 활성화되지 않은 `inactive-until-*` rule은 registry의 active 대상이 아니다.

전환 중 `scripts/lint.py`는 별도 wiki rule을 복제하지 않는 lifecycle dispatcher다. live wiki tree digest가 preservation resolution의 `base_tree_sha256`과 정확히 같을 때만 legacy 15-field wiki lint를 실행한다. 그 외 tree는 `check --all`과 같은 canonical checker가 단독 소유하며, canonical failure를 legacy fallback으로 바꾸지 않는다. raw·authored directive 검사는 이 wiki contract 선택과 독립적으로 계속 실행한다.

| Validator | 입력 | 보장 |
|---|---|---|
| contract | upstream schema·fixture·vendored digest | cross-repo artifact shape drift 탐지 |
| schema | DocumentInstance·ArtifactManifest | local shape·enum·section order |
| graph | all parsed pages | ID, link, relation, collection, cycle |
| evidence | claims·manifest | evidence 실재·digest·허용 source class |
| materialize | schema·registry·pages | generated bytes 재현성·coverage |
| architecture | Python AST imports | 금지 edge·cycle·layer depth |
| replay | fixture command twice | byte identity와 no-op semantics |

CI 순서:

```text
static format/lint
  -> unit/property tests
  -> contract + mock integration
  -> full vault check
  -> materialize --check
  -> replay/failure-injection integration
```

local pre-commit은 `check --changed`와 빠른 test만 실행한다. merge authority는 우회 불가능한 required CI status check가 가진다.

finding은 `rule_id`, severity, path, line, subject_id, message, remediation을 가진 machine-readable JSONL과 사람용 text 두 형식으로 출력한다.

## 11. Last-leaf 변경 모델

| 변경 | 수동 관리 SoT 변경 | 파생 재생성·검증 후속 |
|---|---:|---|
| 동일 source 재capture | 0 | 0 |
| source 새 revision | artifact bundle 1 | 0 |
| 지식 draft 추가 | staging page 1 | 0 |
| draft 승격 | page move 1 | navigation 재생성과 derived backlink resolution 검사 |
| collection member 추가 | collection page 1 | collection/index view 재생성 |
| domain 추가 | `domains.yaml` 1 | index/overview/templates/Bases 재생성 |
| page type 추가 | `knowledge.schema.json` 1 | 전체 materialize·parser/renderer/materializer(template 포함)/checker contract test 재실행 |
| relation type 추가 | `knowledge.schema.json` 1 | 전체 materialize·parser/renderer/materializer(template 포함)/checker contract test·graph rule parameterized test 재실행 |
| page 이동 | page path move 1 | navigation 재생성과 derived backlink resolution 검사 |
| 전역 schema 의미 변경 | schema + migration + compatibility test | 전체 materialize |

전역 schema 의미 변경은 시스템 전체 불변식을 바꾸므로 last-leaf 대상이 아니다. 별도 migration과 사용자 승인을 요구한다. 생성 파일 개수는 수동 관리 지점 수에 포함하지 않는다.

## 12. 기각한 대안

| 대안 | 기각 이유 |
|---|---|
| extractor `DocHook`에 cs-study 구현 주입 | reverse coupling과 commit 이후 hook 실패의 이중 성공 경계 |
| raw `<video_id>.md/.json` force overwrite | content identity 부재; 기존 pair 교체 중 JSON rename 실패 시 새 Markdown 삭제·이전 JSON 잔존 |
| `_meta/collections/<id>.yaml` + collection Markdown | membership 이중 SoT |
| 현행 backlink 외부 인덱스 선언(`AGENTS.md` §Cross-link) | outgoing links에서 계산 가능하며 생성 경로도 별도 관리점. 파일은 현재 생성되지 않음 |
| 현행 provenance 외부 인덱스 선언(`_meta/frontmatter-spec.md` §human_authored 추적) | manifest·page source_paths·Git과 중복. 파일은 현재 생성되지 않음 |
| `wiki/log.md` | Git history와 중복되고 실제 상태와 drift |
| ReviewRecord page/entity | Git review evidence와 lifecycle path로 충분 |
| 모든 page의 sequence field | collection별 순서를 page에 중복 저장하고 복수 collection 표현 불가 |
| 양쪽 page에 inverse relation 저장 | rename·edit 시 동기화 지점 증가 |
| RDF/OWL/SHACL canonical stack | Markdown·JSON Schema와 이중 모델·validator stack 발생 |
| JSON Schema `x-sections` 선언만 사용 | 미인식 keyword는 assertion이 아니므로 false PASS |
| local hook만 사용 | `--no-verify`로 우회 가능해 지속 보장 불가 |
| 한 command가 page·collection·index·log 동시 갱신 | transaction과 rollback 범위 확대, last-leaf 위반 |

## 13. 구현 순서

| 순서 | 작업 | 선행 게이트 | 완료 증거 |
|---:|---|---|---|
| 0 | dirty worktree와 기준 commit 확정, 전용 branch/worktree 생성 | 사용자 설계 승인 | 기존 사용자 diff와 작업 diff 분리 |
| 1 | 두 저장소 baseline fixture와 migration inventory 고정 | 0 | counts·exclusions·fixture hash report |
| 2 | extractor canonical JSON Schema·fixture 추가, reverse hook 제거 | 1 | extractor tests·contract tests·AST graph |
| 3 | `knowledge.schema.json`과 deterministic Markdown parser 작성 | 2 | schema mutation·section order·property tests |
| 4 | immutable ArtifactBundle capture와 현 importer migration | 3 | same/different digest·corruption·failure injection |
| 5 | full checker의 schema·graph·evidence rule 구현; target rule은 fixture·no-write dry-run 전용 | 3,4 | target rule coverage manifest, unsupported hard rule 0, legacy vault write/enforcement 0 |
| 6 | 6a stable ID·basename·frontmatter inventory, 6b fail-closed engine, semantic resolved plan 사용자 승인 후 실제 apply | 5 | 75-page exact universe, canonical collision 0·reserved conflict 1, exact-tree backup·failure-injection·migration parity report |
| 7 | synthesize·promote·collection·move leaf command 구현 | 5,6 | one-page write-set·stale base digest tests |
| 8 | materializer 구현 후 index·overview·template·Bases 전환 | 5,7 | two-run tree hash, active coverage 100% |
| 9 | legacy structure-rule scope·log/backlink/provenance no-write removal plan, 사용자 승인 후 migration apply | 8 | repository grep와 derived parity report |
| 10 | local hook와 두 저장소 독립 CI 연결 | 2,5,8 | clean checkout required commands 성공 |
| 11 | 두 대상 YouTube source를 새 pipeline로 재처리 | 7, 8, 9, 10 | artifact·draft·통합 wiki evidence trace |
| 12 | full vault 검증과 Claude/code review | 11 | HIGH 0, 자동화 가능한 5계층 영역 전부 시도 |

각 순서는 독립 commit 후보이며 앞 단계 검증 실패 시 다음 단계로 진행하지 않는다. 6a와 순서 9의 no-write plan은 변경 없이 실행하고, 6b와 순서 9의 migration apply는 각 plan의 별도 사용자 승인 없이는 실행하지 않는다.

## 14. 자체 검증

### 요구사항 추적성

| PRD ID | Architecture surface | Logic surface |
|---|---|---|
| FR-KP-001 | §3, §4, §8 | BR-ART-007 |
| FR-KP-002 | §7, §9 | BR-ART-001 |
| FR-KP-003 | §5, §9 | BR-ART-002, BR-ART-006 |
| FR-KP-004 | §9 | BR-ART-003 |
| FR-KP-005 | §9 | BR-ART-004 |
| FR-KP-006 | §7 | BR-SYN-001 |
| FR-KP-007 | §5, §7, §9 | BR-SYN-002, BR-SYN-003, BR-SYN-006, BR-SYN-007, BR-APPLY-005~BR-APPLY-008 |
| FR-KP-008 | §5, §6 | BR-PAGE-001, BR-PAGE-002 |
| FR-KP-009 | §5, §6 | BR-PAGE-001, VR-KP-007 |
| FR-KP-010 | §5 | BR-SYN-004, BR-ART-009 |
| FR-KP-011 | §5, §6 | BR-CLM-001~BR-CLM-006 |
| FR-KP-012 | §5, §6 | BR-COL-001~BR-COL-007 |
| FR-KP-013 | §5, §6 | BR-REL-001~BR-REL-007 |
| FR-KP-014 | §5, §10 | BR-REL-005, VR-KP-013 |
| FR-KP-015 | §5, §7, §9 | BR-LIFE-001~BR-LIFE-005, BR-APPLY-006~BR-APPLY-008, VR-KP-022 |
| FR-KP-016 | §5, §7, §9 | BR-APPLY-004~BR-APPLY-013, VR-KP-015, VR-KP-016 |
| FR-KP-017 | §4, §7, §10 | BR-GEN-001~BR-GEN-005 |
| FR-KP-018 | §7, §10 | BR-CHK-002, BR-CHK-003 |
| FR-KP-019 | §4, §6, §10 | BR-CHK-001, VR-KP-020 |
| FR-KP-020 | §10 | BR-CHK-004 |
| FR-KP-021 | §5, §8 | BR-ASSET-001, BR-ASSET-002 |
| FR-KP-022 | §5, §7, §9 | BR-MOVE-001, BR-APPLY-007, BR-APPLY-008, BR-APPLY-010 |
| NFR-KP-001 | §2, §3, §10 | VR-KP-019 |
| NFR-KP-002 | §14 | 자체 검증: 자기 코드 함수 직렬 호출 깊이 |
| NFR-KP-003 | §3, §10 | 완료 술어: Boundary independence |
| NFR-KP-004 | §5, §9 | BR-ART-003~BR-ART-006 |
| NFR-KP-005 | §7, §9, §10 | BR-APPLY-005~BR-APPLY-007, BR-APPLY-013, BR-GEN-004, VR-KP-021 |
| NFR-KP-006 | §9 | BR-GEN-001 |
| NFR-KP-007 | §5, §10 | BR-ART-009, BR-CLM-006 |
| NFR-KP-008 | §4, §6 | BR-CHK-001 |
| NFR-KP-009 | §5, §9 | BR-APPLY-001~BR-APPLY-013 |
| NFR-KP-010 | §4, §11 | BR-COL-001, BR-REL-007 |
| NFR-KP-011 | §6 | BR-CLM-005 |
| NFR-KP-012 | §4, §11 | BR-CHK-001 |
| NFR-KP-013 | §10 | BR-CHK-008 |
| NFR-KP-014 | §5, §7, §10 | BR-LIFE-005, BR-CHK-005, BR-CHK-006, VR-KP-022 |
| NFR-KP-015 | §7, §13 | BR-MIG-001~BR-MIG-015 |

요구사항 추적성 표의 Logic surface 셀에서 물결표는 동일 rule 접두사의 시작 ID부터 종료 ID까지 양 끝을 포함하는 연속 숫자 범위를 뜻한다. 이 표는 문서 section·logic mapping을 소유하고, `_meta/knowledge-requirements.json`은 FR/NFR의 구현 순서와 구현·검증 파일 mapping을 소유한다. 아래 Acceptance 표는 별도 AC의 구현 순서와 관찰 증거 계획을 소유한다.

| Acceptance ID | 구현 순서 | 계획된 관찰 증거 |
|---|---:|---|
| AC-KP-001 | 2, 10, 12 | 두 저장소 AST import graph와 extractor 전용 hook 검색 |
| AC-KP-002 | 2 | versioned schema fixture contract test |
| AC-KP-003 | 4 | same/different payload capture integration test |
| AC-KP-004 | 4 | overwrite 경로·`--force` 전수 검색과 immutable replay test |
| AC-KP-005 | 3, 5, 8 | schema mutation contract test |
| AC-KP-006 | 5, 6, 12 | full-vault ID·link·relation·cycle checker |
| AC-KP-007 | 8, 12 | active index exact coverage assertion |
| AC-KP-008 | 8 | consecutive materialize tree-hash assertion |
| AC-KP-009 | 7 | page apply failure-injection test |
| AC-KP-010 | 7 | collection add-member write-set assertion |
| AC-KP-011 | 7, 8 | stable ID move·materialized navigation·derived backlink resolution integration test |
| AC-KP-012 | 10 | clean checkout required CI command set |
| AC-KP-013 | 5, 7, 11, 12 | primary claim evidence resolver와 review verdict assertion |
| AC-KP-014 | 5, 12 | structure result와 semantic review result field 분리 assertion |

| 항목 | 설계 판정 | 구현 판정 |
|---|---|---|
| dependency cycle | 목표 module DAG cycle 0 | P2-T5 command-inclusive graph 12 modules·21 edges·cycle 0 exact guard; 순서 8 materialize 모듈은 미구현 |
| module dependency 깊이 | 목표 dependency edge chain 3 | 현재 command-inclusive graph 최대 dependency edge 4 transition ratchet |
| 자기 코드 호출 깊이 | 함수 5개 미만 직렬(= 호출 edge 4 미만)을 목표로 하고 edge 4 이상은 설계 경고 | P2-T5 CLI apply candidate의 동적 callback 포함 exact 경로는 `main → _apply_page_plan → apply_page_write_plan → _apply_page_write_plan_unlocked → _check_page_candidate callback → check_target → parse_markdown → _parse_table → _split_table_row`의 함수 9개 직렬(= edge 8)이다. pyan3 정적 그래프는 전환 전체에서 경고 경로 16개를 보고했으며 최대 migration 경로 edge 7, P2-T5 ordinary 경로 7개·최대 edge 6이다. 각 경계는 CLI·lock·transaction·candidate 검증·schema/tree 검사·Markdown parsing의 서로 다른 책임을 가지므로 경고를 수용한다. 최대 동적 경로는 callback exact binding 정적 guard로 증가를 금지하고, transition 전체는 P2-T5 검증 보고의 pyan3 결과를 ratchet baseline으로 보존한다 |
| canonical owner | concern별 owner 1개 | payload contract는 extractor, ArtifactManifest·지식 구조는 cs-study가 단독 소유 |
| raw immutability | append-only digest bundle | atomic no-replace capture와 same/new digest·corruption·경쟁 주입 test 구현 |
| page apply atomicity | one-page temp+replace 또는 rename | shared lock 안 candidate 재검증, base bytes·mode 재검증, atomic leaf commit, post-commit rollback·indeterminate 분류를 구현하고 순서 7 회귀·교차검증을 완료 |
| collection sequence | one Members table row order | exact base bytes에서 Members body만 교체하고 add/reorder의 최초 apply·replay delta를 구현·검증 |
| relation inverse duplication | outgoing-only | schema·graph checker와 candidate overlay를 구현하고 순서 7 candidate 검증을 완료 |
| generated drift | regeneration diff | FAIL — materializer/CI 부재 |
| semantic correctness | evidence review로 분리 | 사용자·review 필수 영역 |
| requirement coverage | PRD FR/NFR 전체 surface 매핑 | 순서 1–7 surface 구현·검증 완료; 순서 8–12 GAP 유지 |

설계 모델은 순환·양방향 canonical dependency를 만들지 않는다. 2026-08-26 기준 순서 1–7은 구현·검증했다. 순서 8–12가 남아 있으므로 전체 시스템 PASS를 주장하지 않는다.

## 15. 변경 이력

- 2026-08-21: immutable artifact, deterministic parser+JSON Schema, stable filename ID, ordered collection, outgoing-only relation, generated navigation, one-page apply 구조로 `archives/design/docs/wiki-ingest-architecture-v1.md`를 대체했다.
- 2026-08-23: 순서 1–6a 구현·검증 결과와 순서 7–12 잔여 GAP을 정적 판정 표에 반영했다.
- 2026-08-24: `check.py → fs.py` leaf dependency를 승인하고 목표 DAG를 8 modules·12 edges로 정정했으며 AST regression guard를 연결했다.
- 2026-08-25: canonical date-time 규칙을 neutral dependency-free `scripts/contracts/timestamps.py` leaf로 승격하고 목표 core+contract DAG 9 modules·13 edges·최대 edge 3, 전환 command-inclusive DAG 11 modules·16 edges·cycle 0·최대 edge 4 ratchet으로 정합화했다.
- 2026-08-25: clipping Markdown privacy normalization을 dependency-free `scripts/contracts/privacy.py` leaf로 단일화했다. 이 항목의 P2-T5 전 당시 baseline은 목표 core+contract DAG 10 modules·14 edges·최대 edge 3, 내부 전환 DAG 9 modules·14 edges·최대 edge 2, command-inclusive DAG 12 modules·18 edges·최대 edge 4였으며 현재 계약 수치는 §3과 §14가 소유한다.
- 2026-08-24: project 실행 자산 77개를 `projects/`로 분리하고 canonical 75-page inventory, 별도 resolved-plan schema, exact backup, atomic exchange·restore·crash recovery engine을 추가했다. 해당 날짜에는 실제 migration apply를 수행하지 않았다.
- 2026-08-25: 승인된 결합 plan으로 apply를 commit했으나 post-apply validation harness 결함을 확인해 exact restore를 commit했고, terminal candidate 격리와 base/target validator lifecycle을 보완했다. 해당 restore 직후 live wiki와 external files는 base 상태였다.
- 2026-08-25: lifecycle remediation 후 승인된 결합 plan을 reapply해 live wiki와 external files를 target으로 전환했다. 후속 교차검증에서 terminal journal binding과 checker text exclusions 보고를 보강했으며, committed journal은 당시 승인 bytes의 실행 증거로 보존한다.
- 2026-08-26: P2-T5 CLI apply candidate 자기 코드 경로를 함수 9개 직렬(= edge 8)로 실측했다. NFR-KP-002는 edge 4 이상의 설계 경고이므로 책임 경계를 제거하지 않고 현재 경로를 수용하되 exact path 정적 guard로 증가를 금지하도록 결정했다.
- 2026-08-26: pyan3 전환 전체 측정에서 edge 4 이상 경로 16개를 확인했고 P2-T5 ordinary 경로 7개·최대 edge 6과 migration 전환 경로를 분리했다. one-line validator pass-through는 제거했으며, 남은 의미 경계는 경고·ratchet baseline으로 검증 보고에 결속했다.
