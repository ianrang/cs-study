# Architecture: 지속 가능한 지식 파이프라인

## 1. 설계 범위와 전제

본 문서는 `docs/wiki-ingest-prd.md`의 전체 지식 파이프라인 구조를 정의한다. 1차 video importer의 v1 요구 계약과 실행 경로는 2026-08-23 순서 4 전환으로 superseded됐으며 digest revision 계약만 normative다. 두 저장 모델의 동시 쓰기는 금지한다.

설계 시작 기준선(2026-08-21, historical non-normative):

- extractor는 canonical JSON과 Markdown을 산출한다.
- cs-study는 extractor CLI를 subprocess로 호출하고 canonical JSON을 pull한다.
- 당시 2차 wiki ingest 실행 파일과 통합 테스트는 존재하지 않았다.
- 당시 wiki에는 안정 page ID, collection, relation의 machine contract가 없었다.
- 당시 dirty code/wiki 변경은 설계 작성 범위가 아니었다.

현재 실행 범위는 immutable capture, target schema/parser/checker, strict PageWritePlan 기반 synthesize·promote·collection·move command와 deterministic materializer다. 순서 6 전환 engine과 순서 9 legacy surface는 target runtime에서 제거했다. 당시 순서 6에서 현재 확인 가능한 digest·journal·rollback candidate·검증 보고는 historical evidence로 보존하고 exact plan·backup bytes 미회수는 limitation으로 기록한다. 시점별 검증 evidence는 `docs/wiki-ingest-review.md`가 기록한다.

## 2. 아키텍처 원칙

1. **Ownership before automation**: 동일 규칙의 canonical owner는 한 곳이다.
2. **Canonical before derived**: 수동 입력과 재생성 가능한 결과를 구분한다.
3. **Pull boundary**: downstream consumer만 upstream artifact contract를 안다.
4. **Append-only raw**: raw identity는 capture-contract bytes digest이며 overwrite하지 않는다. clipping Markdown은 개인 로컬 홈 prefix를 결정적으로 치환한 bytes가 capture contract다.
5. **At most one knowledge page per ordinary apply**: 현재 lifecycle·page command는 no-op 또는 knowledge page 1개만 변경한다. 향후 전역 schema migration은 현재 runtime의 예외가 아니며 별도 설계·승인 전에는 실행할 수 없다.
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
wiki_ingest.py -> fs.py
artifacts.py -> schema.py
artifacts.py -> fs.py
artifacts.py -> privacy.py
documents.py -> schema.py
documents.py -> fs.py
materialize.py -> schema.py
materialize.py -> fs.py
check.py -> schema.py
check.py -> fs.py
check.py -> graph.py
schema.py -> timestamps.py
graph.py: validated DocumentInstance만 소비하며 project module import 없음
```

CLI entrypoint module끼리 import하지 않는다. 최종 core+neutral-contract 그래프는 10 modules, 16 directed edges, cycle 0, 최대 dependency edge chain 3이다. `wiki_ingest.py → fs.py`는 승인 plan의 atomic no-replace 게시를 위한 직접 leaf edge이며 이를 숨기기 위한 pass-through wrapper를 추가하지 않는다. `fs.py`는 path confinement, repository lock, atomic leaf primitive의 canonical owner이므로 checker와 materializer도 직접 의존한다. dependency-free `scripts/contracts/timestamps.py`와 `scripts/contracts/privacy.py`는 각각 canonical date-time과 clipping privacy normalization을 소유한다. runtime checker는 `knowledge`·`contracts` 실제 Python module inventory와 CLI entrypoint를 hidden-inclusive로 열거해 10-module exact set과 16-edge exact set을 비교하고, package 깊이 안의 absolute·relative `ImportFrom` alias를 포함한 cycle·최대 depth를 검사한다. package 깊이를 초과하거나 package가 없는 CLI가 사용하는 relative import는 `VR-KP-019`로 거부한다. canonical import namespace는 `knowledge.*`·`contracts.*` 하나씩이며 동일 파일을 별도 module object로 로드하는 `scripts.knowledge.*`·`scripts.contracts.*` alternate import는 거부한다. repository root·`scripts`·두 module root는 regular non-symlink directory여야 하며 invalid ancestor는 하위 source bytes를 읽지 않고 fail-closed한다. 모든 architecture source는 regular non-symlink UTF-8 Python file이어야 하고 두 package `__init__.py`는 import-free여야 한다. core·contract·CLI에서 `projects.*`와 declared DAG 밖의 identifier-named top-level `scripts` file·package import는 금지한다. module identity는 path 정렬 순서로 만들고 같은 identity에 둘 이상의 path가 대응하면 duplicate finding으로 거부한다. source·inventory·stat의 unreadable UTF-8·syntax·I/O 오류는 `VR-KP-019` finding으로 거부한다. project generator chain은 knowledge runtime에 결합하지 않고 project boundary AST test가 `ImportFrom` alias를 포함한 command-inclusive 12 modules, 18 edges, cycle 0, 최대 dependency edge chain 3을 검증한다.

## 4. Canonical·Derived 소유권

| Concern | Canonical owner | Derived consumer |
|---|---|---|
| extractor output contract | `007_youtube-script/schemas/canonical-transcript-v1.schema.json` | cs-study의 pinned vendored copy와 contract fixture |
| artifact·draft·page structure | `_meta/knowledge.schema.json` | `schema.py`의 schema loader·digest·section/table contract를 통한 parser, renderer, materializer, checker |
| domain names·status | `_meta/domains.yaml` | index, overview, Bases, domain validation |
| controlled vocabulary | `_meta/taxonomy.md` | tag/alias checker |
| raw payload identity | artifact `manifest.json`의 capture-contract byte digest | capture no-op와 evidence resolver |
| knowledge content | Markdown page | index, overview, Bases, Obsidian backlink view, checker graph |
| ordinary page transaction | `_meta/knowledge.schema.json`의 `PageWritePlan` | CLI plan SHA confirmation, checker candidate overlay, atomic leaf apply |
| collection membership | CollectionPage의 `Members` table | collection navigation view |
| relation | subject page의 `Relations` table | checker inverse/closure, Obsidian backlink view |

최종 목표에서 generated-only manifest는 `3 + |schema PageType exact set|` 파일이다. 파일 수와 template 이름은 schema에서 매번 파생하며 문서가 별도 enum·고정 cardinality를 소유하지 않는다.

- `wiki/index.md`
- `wiki/overview.md`
- schema `PageType`의 각 값에 대응하는 `wiki/templates/<page-type>.md`
- `wiki/views/knowledge-pages.base`

`schema.py`의 `CANONICAL_ROOT_EXCLUSIONS`는 canonical parser 입력에서 generated root인 `index.md`·`overview.md`만 제외한다. materializer expected path set은 schema `PageType`에서 별도로 계산하므로 이 exclusion을 generated manifest로 해석하지 않는다.

`index.md`는 active page의 완전 카탈로그다. domain registry의 모든 domain heading을 key 오름차순으로 출력하고, 각 domain의 active page를 `page_type`, stable ID 오름차순으로 열거한다. `collections/`의 active page는 별도 Collections heading에서 같은 순서로 열거한다. 각 entry는 repository-vault-relative wikilink, title, summary를 가지며 `domains/`와 `collections/` 밖의 staging·archive page는 0개다.

index 한 행을 보존하도록 canonical `title`·`summary`는 CR·LF가 없는 단일 행 문자열이다. overview Markdown table의 단일 cell을 보존하도록 domain registry `label`은 CR·LF·`|`를 허용하지 않는다. renderer별 escaping 규칙을 추가하지 않고 schema와 registry 입력 경계가 display-safe 계약을 단독 소유한다.

`overview.md`는 domain 지도다. domain registry의 모든 domain을 key 오름차순으로 한 번씩 출력하고 label, status, active page count를 보여준다. active page를 다시 열거하지 않으며 해당 domain의 `index.md` heading으로 연결한다. 별도 Collections 행에는 active collection count를 기록한다. 따라서 page 추가·이동·archive는 index entry와 overview count에 각각 반영되지만 같은 page 목록을 두 파일에서 중복 소유하지 않는다.

template은 schema `PageType` enum의 exact set과 `DocumentInstance` section contract에서 생성한다. required property를 schema 선언 순서로, optional property를 뒤이어 schema 선언 순서로 출력하고 별도 template registry·legacy property·schema 밖 section을 두지 않는다. `Claims`, `Relations`, collection의 `Members`는 parser가 요구하는 exact table header와 빈 row set을 제공한다. template placeholder는 authoring 입력이며 canonical `DocumentInstance`가 아니므로 template 자체를 content validator에 넣지 않는다.

`knowledge-pages.base`는 [공식 Obsidian Bases syntax](https://obsidian.md/help/bases/syntax)의 valid YAML로 한 파일만 생성한다. global `filters.or`는 `file.inFolder("wiki/domains")`, `file.inFolder("wiki/collections")` 두 식만 가진다. 첫 view는 `type: table`, `name: All active`, 이어서 active domain key 오름차순의 `file.inFolder("wiki/domains/<key>")` domain view, 마지막은 `file.inFolder("wiki/collections")`인 `Collections` view다. 모든 table view의 `order`는 Obsidian UI가 저장하는 canonical property 식별자인 `file.name`, `title`, `page_type`, `summary`, `date_updated`로 같다. serializer는 sequence indentation을 보존하고 YAML alias를 만들지 않아 Obsidian 1.13.7에서 열고 다시 저장해도 bytes가 바뀌지 않아야 한다. domain별 Base 파일과 persistent backlink view는 만들지 않는다.

generated 파일의 generator identity는 `cs-study-materializer/1.0`이다. Markdown marker의 exact grammar는 `<!-- generated-by: cs-study-materializer/1.0; schema-sha256: <64 lowercase hex> -->`다. Base는 Obsidian이 YAML 주석을 저장 시 제거하므로 공식 `formulas` 영역의 `_generated_by` constant formula에 같은 generator identity와 schema digest를 정확히 한 번 기록한다. 이 formula는 어떤 view의 `order`에도 넣지 않아 화면 열로 노출하지 않는다. root Markdown은 첫 heading 앞, template Markdown은 frontmatter closing delimiter 직후에 marker를 둔다. checker는 독립 검증된 expected in-memory bytes와 committed exact manifest를 byte 비교한다. expected path의 ownership marker 누락·중복·문법 불일치, schema digest 불일치, expected path 누락, generated namespace의 예상 밖 ownership-bearing 파일은 drift다. marker 없는 파일을 steady-state command가 덮어쓰거나 삭제하지 않는다. backlink와 inverse relation은 outgoing edge에서 계산하고 persistent external index를 만들지 않는다.

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

2026-08-24 사용자 승인 A에 따라 `wiki/collections/info-sec-engineer-practical-past-exams.md`를 포함한 75-page migration을 수행했다. 당시 machine-readable resolution은 target path·page type·source digest와 legacy index link 순서에서 승인된 52개 `Members` ID를 소유했고 role·rationale를 빈 문자열로 보존했다. 순서 9 이후 resolution 파일은 runtime에서 제거했으며 승인 결과와 검증 증거는 Git history와 P2-T4 보고가 소유한다.

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

repository validation system이 소유하는 검증이다. `check.py`는 canonical page·graph 검증을, `materialize.py`는 generated expected-map·repository parity 검증을 소유하며 서로 import하지 않는다.

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

순서 9 전환 이전 CLI(historical non-normative):

| Command | 상태 | persistent write 범위 | 역할·수명 |
|---|---|---:|---|
| `capture <artifact>` | 구현 | artifact bundle 1 | 최종 목표에도 유지 |
| `capture-asset <asset>` | 구현 | asset bundle 1 | 최종 목표에도 유지 |
| `check --all\|--changed` | 구현 | 0 | 선택한 target root 전체에 동일 rule-set 적용; 순서 6b 전에는 target fixture와 no-write migration tree만 입력하며 legacy wiki root를 호출하지 않음 |
| `synthesize` plan/apply | 구현 | staging page 0 또는 1 | strict SemanticPlan을 PageWritePlan으로 resolve하고 confirmed plan으로 draft 한 개를 생성; 최종 목표에도 유지 |
| `promote` plan/apply | 구현 | page 0 또는 1 move | claim verdict와 명시적 review 승인을 결속해 draft 한 개를 active path로 이동; 최종 목표에도 유지 |
| `collection add-member\|reorder` plan/apply | 구현 | collection page 0 또는 1 | collection 한 페이지의 Members 순서만 변경; 최종 목표에도 유지 |
| `move` plan/apply | 구현 | page 0 또는 1 move | 같은 lifecycle root에서 stable ID를 보존해 이동; 최종 목표에도 유지 |
| `materialize` / `materialize --check` | 구현 | generated leaf 0~11 / 0 | schema·registry·canonical page에서 exact generated manifest를 적용하거나 repository parity를 검사; 최종 목표에도 유지 |
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

순서 9 target tree 통합 뒤의 CLI 목표 상태:

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

순서 9 원자 통합을 마친 현재 모듈:

| Module | 상태·수명 |
|---|---|
| `wiki_ingest.py` | 현재 argparse routing과 exit code |
| `knowledge/schema.py` | 구현된 target schema load·parse·instance validation |
| `knowledge/fs.py` | 구현된 path confinement·repository lock·atomic leaf exchange·no-replace path rename |
| `knowledge/artifacts.py` | 구현된 capture·asset capture·digest 검증 |
| `knowledge/documents.py` | 일반 lifecycle plan/apply 구현·검증 완료 |
| `knowledge/materialize.py` | deterministic generated render·digest·drift·shared-lock leaf apply와 candidate coverage 구현·검증 완료 |
| `knowledge/graph.py` | 구현된 link·relation·collection graph 계산 |
| `knowledge/check.py` | 구현된 target fixture·no-write tree checker |

최종 목표 모듈 책임:

| Module | 단일 책임 |
|---|---|
| `wiki_ingest.py` | argparse routing과 exit code |
| `knowledge/schema.py` | schema·domain registry load, schema digest, Markdown→DocumentInstance parse, section/table contract, instance validation |
| `knowledge/fs.py` | path confinement와 atomic leaf replace |
| `knowledge/artifacts.py` | capture와 digest 검증 |
| `knowledge/documents.py` | synthesize, promote, collection, move |
| `knowledge/graph.py` | link/relation/collection graph 계산 |
| `knowledge/materialize.py` | generated view render·validation·drift check·leaf apply |
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

`.claude/rules/structure-rules.md`의 authored tree 규칙은 `cs/`, `lang/`, `coding-test/`, `tools/`, `development/`에만 적용한다. raw/wiki/schema tree에는 본 문서의 구조를 적용한다.

## 9. 트랜잭션·멱등성·동시성

### Artifact

- primary capture-contract bytes에서 digest를 계산한다. clipping Markdown은 §5의 privacy normalization을 먼저 적용한다.
- temporary sibling directory에 bundle 전체를 작성하고 검증 후 final digest directory로 atomic rename한다.
- final directory가 있고 모든 bytes가 같으면 no-op다.
- final directory가 있는데 bytes가 다르면 corruption으로 거부한다.
- 같은 source의 새 digest는 새 directory다. overwrite와 `--force`는 없다.

### Ordinary knowledge page command

- 일반 lifecycle·page command는 page 한 개만 수정한다. 향후 전역 schema migration은 NFR-KP-015에 따라 별도 설계·backup·사용자 승인을 먼저 요구한다.
- 모든 ordinary apply router는 invoked command와 exact `PageWritePlan.operation`을 결속한다. collection은 `add-member`와 `reorder`도 서로 교차 적용할 수 없다.
- plan은 knowledge page 전체 base tree SHA-256과 operation별 page precondition을 함께 요구한다. replace는 source base SHA-256·bytes를, create는 target 부재를, move는 source base SHA-256·bytes와 target 부재를 모두 기록하며 no-op은 page precondition이 없다.
- ordinary apply와 materializer apply는 `fs.py`가 repository-root directory descriptor에 제공하는 POSIX `flock(LOCK_EX|LOCK_NB)`를 공유하며, lock 획득 실패·미지원 플랫폼은 write 0으로 거부한다. OS descriptor close/process 종료가 lock을 자동 해제하므로 lock file·stale lock cleanup을 만들지 않는다. ordinary apply는 plan load부터 candidate check·commit·rollback/reconcile 종료까지 lock을 보유한다.
- lock 안에서 plan SHA-256·schema SHA-256을 확인하고 candidate check 직후 current tree와 source bytes·mode를 다시 확인한다. current tree·target page bytes·mode·move source 부재가 plan target state와 정확히 일치하는 replay는 idempotent no-op이고, base·target 어느 쪽도 아닌 tree는 stale-plan으로 write 0 거부한다.
- create는 canonical mode `0644`로 게시하고 replace·move는 plan에 결속된 기존 mode를 보존한다. namespace commit 뒤 directory fsync 또는 post-tree 검증이 실패하면 planned target bytes·mode가 그대로 관찰된 own leaf만 이전 상태로 복구한다. rollback 전에 관찰된 same-leaf 외부 변경은 덮지 않고 indeterminate로 중단하지만 관찰과 syscall 사이의 새 non-cooperative 경합은 POSIX content CAS 부재로 무손실 보장 범위 밖이다. in-process rollback 실패도 observed state를 포함한 indeterminate error다. process crash는 atomic namespace operation의 base 또는 target 중 하나로 남고 다음 exact replay가 판별한다.
- promote는 content를 변경하지 않고 staging page를 target으로 rename한다. lifecycle은 path에서 파생한다.
- create·replace·move candidate의 full check는 실제 write 전에 세 입력을 순서대로 검증한다. 첫째 current canonical base에서 render한 expected map과 current repository generated bytes의 VR-KP-017 parity가 일치해야 하므로 선행 수동 drift는 write 0으로 거부한다. 둘째 checker의 in-memory candidate overlay가 canonical page·graph·lifecycle rule을 통과해야 한다. 셋째 candidate overlay에서 render한 expected index·overview가 VR-KP-018 coverage·count를 만족해야 한다. candidate expected bytes는 아직 materialize 전이므로 current repository bytes와 비교하지 않는다. checker와 materializer는 repair나 page apply를 수행하지 않는다.
- collection add-member는 `operation_input`과 plan의 `base_content`를 대조해 Members에 빈 role·rationale의 정확히 한 행만 지정 위치에 추가하고 reorder는 동일한 member row 객체 집합의 순서만 바꾼다. 최초 apply와 target-state replay 모두 같은 delta validator를 통과해야 한다. Members table 바깥 raw bytes와 기존 member row field를 exact 보존하며 invalid·duplicate-member base를 repair하지 않고 거부한다.
- promote plan은 `--review-verdicts` strict JSON에서 draft의 모든 primary claim ID에 verdict 하나를 요구한다. `support`는 claim status `corroborated`·`verified`, `contradiction`은 `rejected`와만 결속하고 `claimed` primary 또는 `insufficient` verdict는 apply를 거부한다. verdict는 promotion-time authorization evidence이고 active page에는 persistent claim status가 남는다. 장기 audit는 Git review와 P2-T5/P2-T11 검증 보고가 소유하며 별도 ReviewRecord·중복 wiki field를 만들지 않는다.
- P2-T5 move는 같은 lifecycle root 안에서만 허용한다. staging→active는 review-approved promote가 소유하고, active→archive와 archive→staging은 P2-T5에서 unsupported이므로 move로 우회하지 않는다.

### Generated surface

- `materialize.py`의 pure render 함수는 strict UTF-8·finite JSON schema, validated registry, schema-valid canonical page를 받아 §4의 exact repository-relative path→bytes map을 만든다. renderer와 독립된 validator가 canonical record·schema contract에서 index·overview·template·Base의 기대 의미를 다시 계산한다. Base renderer는 같은 모듈의 Obsidian-compatible YAML serializer와 in-band formula ownership marker를 사용하며 별도 sidecar·registry를 만들지 않는다. 같은 모듈의 check/apply 함수가 validation·repository 비교·generated leaf 적용을 소유하고 CLI parsing은 소유하지 않는다. renderer와 validator는 `schema.py`가 한 번 로드해 공개하는 property·PageType·section/table·placeholder·Base order contract snapshot을 단방향 소비한다.
- renderer는 key·page type·stable ID의 명시 순서, UTF-8, LF newline, file-final newline, `allow_unicode=true` YAML block serialization을 사용한다. locale·filesystem enumeration order·wall clock을 읽지 않는다.
- `wiki_ingest.py materialize --check`는 materializer가 current canonical tree의 expected in-memory map을 YAML·marker 위치·exact path set·active index coverage까지 독립 검증한 뒤 repository bytes와 비교하도록 호출한다. 별도 temporary tree를 만들지 않으므로 write와 cleanup surface는 0이며 drift가 하나라도 있으면 non-zero다. page candidate full check는 동일 renderer로 current base parity를 먼저 검증하고 candidate expected map의 coverage를 별도로 검증해, 선행 drift와 정상적인 post-candidate 차이를 혼동하지 않는다.
- `wiki_ingest.py materialize`는 materializer가 expected map 전체를 먼저 render·독립 validate하고 `fs.py`의 repository shared lock과 directory-FD-bound atomic leaf primitive로 expected leaf를 repository-relative path 오름차순 적용하도록 호출한다. `wiki/`, `wiki/templates/`, `wiki/views/`의 regular directory descriptor를 preflight부터 commit까지 유지하고 path의 device/inode identity를 재검증한다. Markdown comment marker 또는 Base formula marker를 가진 existing leaf는 preflight bytes·device·inode·mode observation을 결속하고 새 temp의 bytes digest·device·inode·mode를 commit 직전과 직후 검증한 뒤 기존 leaf와 atomic exchange한다. 밀려난 leaf identity까지 일치한 경우만 commit하고, 불일치하면 own target inode를 확인해 exchange-back하여 경쟁 leaf를 복원한다. missing leaf는 같은 temp identity 검증을 거친 atomic no-replace create다. 중단 뒤 남은 managed-name temp 중 해당 형식의 generator marker가 있는 own leaf만 다음 lock preflight에서 identity-bound 삭제하고 markerless leaf는 보존한다. marker 없는 existing leaf, parent/leaf symlink·special file, preflight 뒤 parent/leaf 교체, 예상 밖 ownership-bearing generated leaf가 있으면 외부 경로를 쓰지 않고 거부한다.
- generated surface는 root Markdown과 두 하위 directory에 분산되므로 전체를 canonical full-tree exchange하지 않는다. leaf 적용 도중 실패하면 canonical knowledge page는 0개 변경되고 generated surface는 base 또는 부분 target일 수 있다. 이 상태는 `materialize --check`가 exact drift로 탐지하고 같은 입력의 재실행이 target으로 수렴시킨다. generated 파일은 파생 가능하므로 이 경계를 canonical page의 all-or-nothing transaction으로 확대하지 않는다.
- 순서 8의 최초 전환은 승인 commit에서 기존 marker 없는 8개 파일을 expected bytes로 교체하고 누락 3개를 생성한다. 이 전환 뒤 steady-state command에는 marker 없는 파일 adoption 분기가 없다.

### Replay identity

materialize input digest는 exact schema bytes digest, exact domain registry bytes digest, canonical document tree의 sorted path+bytes digest, generator name/version, normalized command options의 canonical JSON tuple이다. materialize의 normalized option set은 현재 빈 map이며 URL·filename 존재·mtime·wall clock을 넣지 않는다. output tree digest는 expected path와 bytes SHA-256을 path 오름차순 canonical JSON으로 직렬화해 계산한다. 같은 input digest의 연속 두 render와 적용 후 재실행은 output tree digest와 exit semantics가 같아야 한다.

## 10. 검증 아키텍처

`check`는 현재 활성 normative rule-set의 모든 hard rule을 보고한다. active normative 문서에 hard rule이 선언됐지만 구현 rule ID가 없으면 `UNSUPPORTED_RULE` HIGH finding으로 실패한다. historical·superseded 절과 구현·검증 surface가 아직 활성화되지 않은 `inactive-until-*` rule은 registry의 active 대상이 아니다.

`scripts/lint.py`는 별도 wiki rule을 복제하지 않는 read-only dispatcher다. wiki 요청은 tree 상태와 무관하게 canonical checker와 materializer의 generated repository parity를 단방향 조립하며 canonical failure를 legacy fallback으로 바꾸지 않는다. CLI `check --all`은 합성 structural verdict·findings·exclusions를, lint는 동등한 HIGH findings·exit semantics를 제공한다. raw·authored recency·필수 필드·directive·broken-link 검사는 wiki 계약과 독립적으로 계속 실행한다.

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

local pre-commit은 아래 저장소별 staged validation과 빠른 test만 실행한다. merge authority는 우회 불가능한 required CI status check가 가진다.

순서 10의 검증 명령은 저장소별로 독립 실행한다. 공용 wrapper나 상대 저장소 경로를 두지 않으며, tracked hook과 CI workflow가 각 저장소의 기존 명령을 직접 조립한다.

| 저장소 | local pre-commit feedback | required CI command set |
|---|---|---|
| extractor | source tree Ruff와 contract·architecture 빠른 test | locked dependency sync, Ruff, non-network 전체 test, package build |
| cs-study | 격리 Git index snapshot에서 repository lint canonical scope의 status-aware staged Markdown과 contract·project-boundary 빠른 test | schema를 포함한 전체 test, `check --all`, `materialize --check`, repository lint |

cs-study의 local hook은 dependency-free system Python 표준 라이브러리 bootstrap으로 `--name-status -z --no-renames` staged Markdown 상태와 경로를 읽고, 전체 Git index를 임시 격리 tree로 materialize한다. 실제 lint 입력·링크·canonical sibling lookup·빠른 test·lint dependency·Python patch는 같은 index snapshot에 결속한다. hook은 non-delete 후보 전체를 `scripts/lint.py --repository-paths`에 전달하고, `lint.py`의 `default_repository_paths`·`repository_lint_paths`가 canonical default scope와 후보 filtering을 단독 소유한다. 후보 parent와 scope root는 dot-segment와 symlink ancestor를 해소한 canonical path로 비교해 lexical scope 우회를 허용하지 않되, 원래 leaf identity를 보존해 inventory의 symlink·파일 타입 검사를 우회하지 않는다. Markdown 삭제가 하나라도 있으면 mixed write-set 누락을 막기 위해 snapshot의 default repository lint로 수렴시키며, scope 밖 Markdown은 그 owner가 제외하고 빠른 test 대상으로만 남긴다. 전달 경로의 선행 하이픈은 `./`로 명시하고, staged 삭제 경로가 worktree에 다시 존재하거나 나머지 staged 경로에 unstaged 변경이 겹치면 index와 worktree 불일치로 거부하며, snapshot 생성·회수 실패도 non-zero다. branch 전체 diff를 `--changed`의 입력으로 사용하지 않으며, 파일명이 공백·개행을 포함해도 하나의 경로로 보존한다. terminal migration journal·rollback candidate의 local 존재 여부는 clean checkout의 source contract가 아니다. CI는 ignore pattern과 tracked·staged 부재를 검증하고, 실제 local recovery evidence 보존은 작업 검증 보고가 소유한다.

hook은 Git inventory 실패를 별도 non-zero로 전파한다. extractor는 index와 다른 unstaged·untracked file이 하나라도 있으면 전체 빠른 검사를 시작하지 않고 거부한다. cs-study는 staged Markdown의 index·worktree 직접 불일치를 거부하고, lint와 빠른 test는 untracked target이나 unstaged sibling·test repair가 관찰되지 않는 격리 index snapshot에서 실행한다. Markdown 삭제가 하나라도 있으면 snapshot의 default repository lint로 수렴시키고, 삭제가 없는 후보는 repository scope owner가 filter하며, 빈 staged Markdown 집합은 lint 입력 0으로 명시 처리한 뒤 snapshot 빠른 test만 실행한다.

두 저장소의 canonical CI profile은 각 저장소의 workflow 파일 1개와 `verify` job 1개로 고정한다. workflow는 filter 없는 `push`와 `pull_request`에서 실행하고 top-level `contents: read` 외 권한 및 job override를 두지 않는다. `verify`는 `ubuntu-24.04`, timeout 20분, full commit SHA의 checkout·setup-uv action, setup-uv `0.12.9`, 저장소별 `.python-version`의 exact Python patch를 사용한다. 단계 순서는 checkout, setup-uv, 표의 required CI command set 기재 순서이며 조건부 실행·failure 무시·추가 action·추가 job을 허용하지 않는다. 이 profile이 action·tool version·runner·trigger·권한·topology·순서의 정책 SoT다.

finding은 `rule_id`, severity, path, line, subject_id, message, remediation을 가진 machine-readable JSONL과 사람용 text 두 형식으로 출력한다.

## 11. Last-leaf 변경 모델

| 변경 | 수동 관리 SoT 변경 | 파생 재생성·검증 후속 |
|---|---:|---|
| 동일 source 재capture | 0 | 0 |
| source 새 revision | artifact bundle 1 | 0 |
| 지식 draft 추가 | staging page 1 | 0 |
| draft 승격 | page move 1 | navigation 재생성과 derived backlink resolution 검사 |
| collection member 추가 | collection page 1 | collection/index view 재생성 |
| domain 추가 | `domains.yaml` 1 | index/overview/Bases 재생성 |
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
| 9 | legacy structure-rule scope·log/backlink/provenance no-write removal plan, 사용자 승인 후 검증된 Git target tree 통합 | 8 | repository grep와 derived parity report |
| 10 | local hook와 두 저장소 독립 CI 연결 | 2,5,8 | clean checkout required commands 성공 |
| 11 | 두 대상 YouTube source를 새 pipeline로 재처리 | 7, 8, 9, 10 | artifact·draft·통합 wiki evidence trace |
| 12 | full vault 검증과 Claude/code review | 11 | HIGH 0, 자동화 가능한 5계층 영역 전부 시도 |

각 순서는 독립 commit 후보이며 표의 선행 게이트만 의존성을 정의한다. 같은 의존 경로의 선행 게이트가 실패하면 그 후속 작업은 진행하지 않되, 번호만 앞선 독립 작업의 차단을 전역 차단으로 확대하지 않는다. 6a와 순서 9의 no-write plan은 변경 없이 실행하고, 6b actual apply와 순서 9의 승인된 Git target tree 통합은 각 plan의 별도 사용자 승인 없이는 실행하지 않는다.

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
| FR-KP-017 | §4, §7, §9, §10 | BR-GEN-001~BR-GEN-014, VR-KP-017, VR-KP-018, VR-KP-021 |
| FR-KP-018 | §7, §10 | BR-CHK-002, BR-CHK-003 |
| FR-KP-019 | §4, §6, §10 | BR-CHK-001, BR-CHK-010, VR-KP-020, VR-KP-023 |
| FR-KP-020 | §9, §10 | BR-CHK-004, BR-CHK-009, VR-KP-017, VR-KP-018 |
| FR-KP-021 | §5, §8 | BR-ASSET-001, BR-ASSET-002 |
| FR-KP-022 | §5, §7, §9 | BR-MOVE-001, BR-APPLY-007, BR-APPLY-008, BR-APPLY-010, BR-GEN-005, BR-GEN-007, VR-KP-018 |
| NFR-KP-001 | §2, §3, §10 | VR-KP-019 |
| NFR-KP-002 | §14 | 자체 검증: 자기 코드 함수 직렬 호출 깊이 |
| NFR-KP-003 | §3, §10 | 완료 술어: Boundary independence |
| NFR-KP-004 | §5, §9 | BR-ART-003~BR-ART-006 |
| NFR-KP-005 | §7, §9, §10 | BR-APPLY-005~BR-APPLY-007, BR-APPLY-013, BR-GEN-003~BR-GEN-005, BR-GEN-011~BR-GEN-012, VR-KP-021 |
| NFR-KP-006 | §4, §9 | BR-GEN-001, BR-GEN-006~BR-GEN-010, BR-GEN-013, VR-KP-021 |
| NFR-KP-007 | §5, §10 | BR-ART-009, BR-CLM-006 |
| NFR-KP-008 | §4, §6, §9 | BR-CHK-001, BR-GEN-006, BR-GEN-009, VR-KP-017, VR-KP-018 |
| NFR-KP-009 | §5, §9 | BR-APPLY-001~BR-APPLY-013, BR-GEN-011, BR-GEN-012, BR-CHK-009 |
| NFR-KP-010 | §4, §9, §11 | BR-COL-001, BR-REL-007, BR-GEN-005~BR-GEN-010, BR-GEN-014 |
| NFR-KP-011 | §4, §6 | BR-CLM-005, BR-GEN-009, BR-GEN-010 |
| NFR-KP-012 | §4, §9, §11 | BR-CHK-001, BR-GEN-006, BR-GEN-009, BR-GEN-010 |
| NFR-KP-013 | §10 | BR-CHK-008, BR-CHK-011 |
| NFR-KP-014 | §5, §7, §10 | BR-LIFE-005, BR-CHK-005, BR-CHK-006, VR-KP-022 |
| NFR-KP-015 | §7, §13 | historical BR-MIG-001~BR-MIG-015 evidence; future migration은 별도 설계·승인 |

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
| dependency cycle | 최종 module DAG 10 modules·16 edges·cycle 0 | command-inclusive graph 12 modules·18 edges·cycle 0 exact guard |
| module dependency 깊이 | 목표 dependency edge chain 3 | 현재 command-inclusive graph 최대 dependency edge 3 |
| 자기 코드 호출 깊이 | 함수 5개 미만 직렬(= 호출 edge 4 미만)을 목표로 하고 edge 4 이상은 설계 경고 | P2-T5 CLI apply의 대표 semantic parse 경로는 `main → _apply_page_plan → apply_page_write_plan → _apply_page_write_plan_unlocked → _check_page_candidate callback → check_target → parse_markdown → _parse_table → _split_table_row`의 함수 9개 직렬(= edge 8)이다. 작은 AST contract는 이 경로의 직접 호출 edge 7개와 `candidate_check=_check_page_candidate` binding 및 callback invocation만 검증한다. class method·lambda·varargs 등 Python callable 전체를 재해석하는 별도 분석기는 두지 않으며 이 검사는 전체 repository call graph의 exact maximum을 보장하지 않는다. P2-T6 materializer는 범위가 고정된 세 module의 call graph에서 core 함수 6개 직렬(= edge 5), CLI dispatch 포함 함수 7개 직렬(= edge 6)을 ratchet한다. CLI·apply transaction·render/independent validation·schema parsing의 서로 다른 의미 경계로 경고 깊이를 수용한다. pyan3 정적 그래프 수치는 P2-T5 전환 당시 historical baseline으로만 보존한다 |
| canonical owner | concern별 owner 1개 | payload contract는 extractor, ArtifactManifest·지식 구조는 cs-study가 단독 소유 |
| raw immutability | append-only digest bundle | atomic no-replace capture와 same/new digest·corruption·경쟁 주입 test 구현 |
| page apply atomicity | one-page temp+replace 또는 rename | shared lock 안 candidate 재검증, base bytes·mode 재검증, atomic leaf commit, post-commit rollback·indeterminate 분류를 구현하고 순서 7 회귀·교차검증을 완료 |
| collection sequence | one Members table row order | exact base bytes에서 Members body만 교체하고 add/reorder의 최초 apply·replay delta를 구현·검증 |
| relation inverse duplication | outgoing-only | schema·graph checker와 candidate overlay를 구현하고 순서 7 candidate 검증을 완료 |
| generated drift | regeneration diff | materializer exact 11-file parity·two-run digest 구현; required CI는 순서 10 소유 |
| semantic correctness | evidence review로 분리 | 사용자·review 필수 영역 |
| requirement coverage | PRD FR/NFR 전체 surface 매핑 | 순서 1–9 live 통합과 P2-T7/P2-T8 검증 증거 반영; 순서 10–12 GAP 유지 |

설계 모델은 순환·양방향 canonical dependency를 만들지 않는다. 2026-09-02 target state 기준 순서 1–9를 반영했으며 live 적용 전의 no-write 검증·승인 상태는 payload 밖 P2-T7 검증 보고가 소유한다. 순서 10–12가 남아 있으므로 전체 시스템 PASS를 주장하지 않는다.

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
- 2026-08-28: P2-T6 구현 전 materializer의 generated lifecycle 소유권, `schema.py`·`fs.py` 공용 leaf 의존, exact marker와 공식 Bases YAML 계약, 최초 markerless 전환의 commit-only 경계, candidate base parity→canonical overlay→candidate coverage 검증 순서와 P2-T6 관련 FR/NFR logic surface mapping을 정합화했다. Obsidian 1.13.7 실환경 round-trip에서 YAML 주석 제거·alias 전개·note property canonicalization이 확인되어 Base ownership을 보존되는 `_generated_by` formula로 이동하고 serializer contract를 UI 저장 형식과 일치시켰다.
- 2026-08-29: 순서 9 no-write candidate에서 legacy log·external index 선언과 전환 전용 migration runtime 제거를 검증했으며 Git target tree 통합은 NFR-KP-015 증거 gate로 차단했다. plan 게시의 실제 `wiki_ingest.py → fs.py` edge를 목표 DAG에 반영해 core 10 modules·16 edges, command-inclusive 12 modules·18 edges, cycle 0·최대 edge 3으로 고정했다.
- 2026-09-02: P2-T5 호출 깊이 검증을 대표 semantic path·callback binding으로 한정하고 불완전한 범용 Python 분석기 요구를 제거했다. PageWrite lifecycle path는 JSON Schema `LifecyclePath` 한 곳이 소유하고 `target_path`와 nullable `source_path`의 non-null branch가 이를 참조한다. schema 변경은 현재 `3 + |PageType| = 11`개 generated marker를 materializer로 재생성하고 이후 생성되는 PageWritePlan의 `schema_sha256`에 반영한다. 기존 plan bytes는 수정하지 않으며 이전 digest를 가진 plan은 stale로 거부한다.
