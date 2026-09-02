# Business Logic: 지속 가능한 지식 파이프라인

## 1. 용어와 상태

| 용어 | 정의 |
|---|---|
| Source identity | provider object 또는 canonical locator를 식별하는 논리 key |
| ArtifactBundle | capture-contract payload와 descriptor를 함께 보존하는 immutable directory |
| SemanticPlan | LLM/사람이 제안한 지식 의미 입력. path·frontmatter·derived field·rendered Markdown·write operation은 포함하지 않음 |
| PageWritePlan | Python이 SemanticPlan 또는 명시적 lifecycle command를 single-page write-set·base/target digest·rendered bytes로 resolve한 strict transaction instance |
| DraftPage | `wiki/staging/` 아래의 schema-valid 검토 대상 Markdown |
| ActivePage | `wiki/domains/` 또는 `wiki/collections/` 아래의 canonical Markdown |
| ArchivedPage | `wiki/archive/` 아래의 보존 page |
| Page ID | 전역 유일한 filename stem |
| Collection | Members 행 순서로 grouping과 sequence를 소유하는 page |
| Claim | status와 evidence를 가진 검증 단위 |
| Relation | subject page가 소유하는 typed outgoing edge |
| Generated surface | canonical data에서 byte-identical하게 재생성되는 navigation/template/view |

Lifecycle 상태는 frontmatter에 중복 저장하지 않고 path로 결정한다.

```text
staging -> active -> archive
   ^                    |
   +--------------------+  explicit restore review only
```

Claim 상태는 `claimed`, `corroborated`, `verified`, `rejected`다. exact enum owner는 `_meta/knowledge.schema.json`이다.

## 2. 불변 원문과 source evidence 규칙

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-ART-001 | capture 입력이 file이면 | file bytes에 source type·media type별 capture contract를 적용해 primary payload로 사용한다 | directory implicit scan 금지 |
| BR-ART-002 | primary capture-contract bytes가 결정되면 | SHA-256과 byte size를 계산한다 | normalization 전 bytes digest와 혼용 금지 |
| BR-ART-003 | 같은 source ID와 digest bundle이 완전하게 존재하면 | no-op exit 0이다 | bytes·manifest 불일치면 corruption reject |
| BR-ART-004 | 같은 source ID에 다른 digest가 들어오면 | 새 revision bundle을 만든다 | 기존 revision overwrite 금지 |
| BR-ART-005 | artifact bundle을 commit하면 | temp sibling directory 전체를 검증 후 rename한다 | final path 존재 시 replace 금지 |
| BR-ART-006 | manifest digest 또는 size가 실제 payload와 다르면 | artifact를 거부한다 | 없음 |
| BR-ART-007 | extractor contract version이 미지원이면 | capture를 거부한다 | silent coercion 금지 |
| BR-ART-008 | normalized content 또는 asset을 bundle에 넣으면 | 각각 exact digest descriptor를 기록한다 | primary payload digest와 혼용 금지 |
| BR-ART-009 | page가 source를 인용하면 | `source_paths`는 artifact manifest path를 가리킨다 | raw payload 직접 경로·외부 URL만의 evidence 금지 |
| BR-ART-010 | clipping Markdown을 capture하면 | UTF-8 payload의 Apple `/Users/<profile>/`·Windows `<drive>:\\Users\\<profile>\\` prefix를 `<local-user-home>`으로 결정적·멱등 치환한 뒤 digest·size·payload를 생성한다 | generic `/home/**`·`/tmp/**`·`/var/**` 치환, non-UTF-8 수용, 기존 revision overwrite 금지 |
| BR-ART-011 | 저장된 artifact·asset manifest 또는 descriptor leaf를 읽으면 | schema가 dot·backslash component를 먼저 거부하고 `fs.py`가 호출자가 명시한 `raw` trust anchor 아래 bundle을 descriptor-relative로 한 번 열어 검증 종료까지 identity를 유지하며, 모든 leaf와 file inventory를 같은 descriptor에서 읽고 정상 종료 직전에 path identity를 재검증한다 | trust anchor 아래에서 resolve 후 외부 read, bundle별 trust boundary 축소, multi-read 사이 path 재개방, path 기반 inventory, consumer별 path regex·symlink 추종 금지 |
| BR-ASSET-001 | 동일 asset bytes가 다시 제공되면 | 기존 digest asset을 재사용한다 | 없음 |
| BR-ASSET-002 | asset bytes가 바뀌면 | 새 digest asset을 만든다 | 기존 asset overwrite 금지 |

## 3. 지식 합성·검토·승격 규칙

### 합성

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-SYN-001 | synthesize가 실행되면 | CLI `--source`와 SemanticPlan `source_paths`의 exact-match manifest 목록만 source universe로 사용한다 | wiki/는 collision·graph 검증 context로만 읽고 source로 ingest하지 않는다 |
| BR-SYN-002 | SemanticPlan이 제공되면 | strict schema와 current artifact/vault 상태로 재검증한다 | unknown field reject |
| BR-SYN-003 | SemanticPlan이 path·frontmatter·derived field·rendered Markdown·write operation을 포함하면 | 거부한다 | 없음 |
| BR-SYN-004 | 동일 주제를 여러 manifest가 설명하면 | 한 DraftPage의 `source_paths`와 Claims에 함께 반영할 수 있다 | source별 별도 summary가 요구되면 separate page |
| BR-SYN-005 | 기존 stable ID 또는 의미 중복 후보가 있으면 | 새 active page를 만들지 않고 draft에 merge/review finding을 남긴다 | 자동 merge 금지 |
| BR-SYN-006 | SemanticPlan을 resolve하면 | Python renderer가 staging candidate bytes와 logical write-set 최대 1개를 가진 PageWritePlan을 no-write로 게시한다 | LLM direct write·plan mode knowledge page write 금지 |
| BR-SYN-007 | synthesize PageWritePlan을 apply하면 | plan SHA·schema·base tree·target 부재·candidate full check를 재검증한 뒤 staging Markdown 한 개만 atomic create한다 | apply mode의 semantic 재결정 금지 |

### Page와 claim

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-PAGE-001 | 새 page ID를 만들면 | 전역 basename과 충돌하지 않는 deterministic kebab-case key를 사용한다 | 충돌 시 자동 suffix 금지, 사용자 결정 |
| BR-PAGE-002 | page title·domain·path가 바뀌면 | filename stem ID는 보존한다 | page의 본질적 identity 변경은 새 page+supersede 결정 |
| BR-PAGE-003 | page가 active이면 | schema·graph·evidence hard rule을 모두 통과해야 한다 | 의미 review 결과는 별도 gate |
| BR-CLM-001 | BR-CLM-004, BR-CLM-003, BR-CLM-002를 순서대로 평가해 모두 충족하지 못하면 | status는 claimed다 | 미해결 mixed evidence도 claimed 유지 |
| BR-CLM-002 | review가 material rebuttal 없음과 독립 source 둘 이상의 같은 의미 지지를 확정하고 BR-CLM-003은 충족하지 않으면 | status는 corroborated다 | source 독립성이 없으면 불가 |
| BR-CLM-003 | review가 material rebuttal 없음과 보존된 primary/official source artifact의 직접 지지를 확정하면 | status는 verified다 | URL만 있거나 artifact 미보존이면 불가 |
| BR-CLM-004 | review가 보존된 반례 evidence로 claim이 반박됐다고 확정하면 | status는 rejected이고 반례 evidence를 기록한다 | page에서 조용히 삭제 금지 |
| BR-CLM-005 | Claim row가 있으면 | ID, primary, claim, status, evidence, notes 구조를 만족한다 | exact columns는 schema 소유 |
| BR-CLM-006 | Claim row가 있으면 | 해당 claim을 위한 최소 evidence 하나가 실재해야 한다 | primary claim은 BR-CHK-006 semantic review도 요구 |

### 승격과 변경

BR-LIFE-003·BR-LIFE-004는 archive·restore의 목표 상태 규칙이다. 두 전이의 executable command와 PageWritePlan operation은 P2-T5 범위가 아니며, 별도 schema version·task 승인 전에는 unsupported로 거부한다. P2-T5의 `move`는 같은 lifecycle root 안의 경로 변경만 소유한다.

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-LIFE-001 | draft를 active로 승격하면 | full check와 명시적 review approval을 요구한다 | 자동 승격 금지 |
| BR-LIFE-002 | promote가 성공하면 | content bytes를 바꾸지 않고 page를 active path로 rename한다 | target collision reject |
| BR-LIFE-005 | promote plan을 만들면 | strict review JSON의 모든 primary claim ID에 claim-level evidence verdict를 exact 1개 결속하고 status와 verdict 정합을 검증한다 | `claimed` primary·`insufficient` 승격, 누락·중복·비-primary verdict, boolean-only approval 금지 |
| BR-LIFE-003 | active page를 archive하면 | filename ID와 content를 보존해 archive path로 이동한다 | 삭제 금지 |
| BR-LIFE-004 | archived page의 explicit restore review를 시작하면 | 즉시 staging Draft로 이동하고 BR-LIFE-001을 다시 적용한다 | archive→active 직접 이동 금지 |
| BR-APPLY-001 | 기존 page update plan을 만들면 | base SHA-256을 기록한다 | 없음 |
| BR-APPLY-002 | current tree가 base와 일치하는 최초 apply에서 current page SHA-256이 plan의 page base SHA-256과 다르면 | stale plan으로 거부한다 | BR-APPLY-007의 exact target-state confirmed replay에는 적용하지 않고 force overwrite는 금지 |
| BR-APPLY-003 | page bytes를 갱신하면 | temp file 검증·fsync 후 atomic replace한다 | validation 후속 실행에 의존 금지 |
| BR-APPLY-004 | command write-set에 knowledge page가 둘 이상이면 | 거부한다 | generated-only write는 materialize가 별도 소유 |
| BR-APPLY-005 | ordinary page plan을 게시하면 | canonical JSON plan bytes의 SHA-256, schema SHA-256, base/target tree SHA-256, normalized input SHA-256, generator version을 결속한다 | 기존 plan overwrite 금지 |
| BR-APPLY-006 | ordinary page plan을 apply하면 | 사용자가 확인한 plan SHA-256과 exact plan bytes digest가 일치해야 한다 | confirmation 생략·prefix match 금지 |
| BR-APPLY-007 | apply 시 current tree가 base와 다르면 | current tree·target page bytes·mode·move source 부재가 plan target state와 모두 정확히 같고 plan에 결속된 base bytes로 operation-specific delta를 재검증한 confirmed replay만 idempotent no-op으로 허용하고, 나머지는 write 0 stale/collision reject한다 | force·부분 target match·replay semantic gate 우회 금지 |
| BR-APPLY-008 | candidate page operation을 apply하면 | write 전에 in-memory overlay full check를 통과해야 한다 | checker repair·검증 후 수정 금지 |
| BR-APPLY-009 | replace를 commit하면 | sibling temp에 target bytes를 쓰고 검증·fsync한 뒤 atomic replace한다 | delete+create gap 금지 |
| BR-APPLY-010 | create 또는 move를 commit하면 | target no-replace primitive를 사용하고 move는 source bytes와 ID를 보존한다 | competing target overwrite 금지 |
| BR-APPLY-011 | ordinary apply를 실행하면 | `fs.py`의 non-blocking repository-root directory descriptor lock을 materializer apply와 공유하고 invoked command·exact plan operation·operation input digest, candidate check 직후 tree·source bytes·mode를 재검증한다. commit·post-tree 실패 시 planned target 상태로 관찰된 own leaf만 이전 상태로 rollback한다 | 관찰된 외부 same-leaf bytes overwrite, lock 획득 실패 후 write, rollback conflict/failure를 단순 stale로 축소 금지; 관찰과 syscall 사이 non-cooperative race는 보장 범위 밖 |
| BR-APPLY-012 | Markdown leaf를 create·replace·move하면 | create mode는 `0644`, replace·move mode는 source mode를 보존한다 | 기존 vault의 mode를 일괄 정규화하지 않는다 |
| BR-APPLY-013 | namespace commit 뒤 process가 종료되면 | atomic leaf는 base 또는 target exact state이며 다음 confirmed plan replay가 상태를 재판별한다 | partial content·임의 자동 overwrite 금지 |
| BR-MOVE-001 | page를 이동하면 | ID와 lifecycle root를 보존하고 target collision을 사전 검사한다 | staging→active·active→archive·archive→staging lifecycle 전이를 move로 우회하거나 inbound backlink를 수동 수정 금지 |

다음 BR-MIG 규칙은 순서 6 전역 schema migration의 historical non-normative 실행 계약이다. 순서 9 이후 runtime command는 제공하지 않으며 향후 전역 migration은 별도 설계·승인을 요구한다. 보존된 journal digest와 결속되는 exact plan·backup bytes를 회수하지 못한 사실은 historical limitation으로 유지하되 현재 runtime 완료 술어나 P2-T7 적용 입력으로 사용하지 않는다.

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-MIG-001 | migration inventory를 만들면 | explicit `wiki/` root의 canonical universe와 generated/template exclusion을 분리한다 | project root 포함 금지 |
| BR-MIG-002 | canonical ID를 검사하면 | canonical collision과 generated/template reserved-name conflict를 별도 보고한다 | 자동 suffix 금지 |
| BR-MIG-003 | resolved plan을 승인 후보로 만들면 | source·target universe, source digest, rendered target bytes·mode, base·target tree digest를 모두 고정하고 sibling temp+fsync+atomic no-replace로 게시한다 | semantic field 자동 추론·기존 승인 산출물 overwrite 금지 |
| BR-MIG-004 | unresolved decision이 1개 이상이거나 universe coverage가 불완전하면 | backup·apply를 write 0으로 거부한다 | partial migration 금지 |
| BR-MIG-005 | backup을 만들면 | root를 포함한 path·type·POSIX mode·size·bytes manifest와 exact plan bytes를 exclusive content-bound tar에 기록하고 다시 검증한다 | symlink·special file·path traversal 금지 |
| BR-MIG-006 | apply 직전 current tree·plan·backup 중 하나의 digest가 다르면 | stale 또는 corruption으로 거부한다 | force 금지 |
| BR-MIG-007 | candidate full tree와 결합 external-reference target이 checker·generator·expected digest를 통과하면 | preservation manifest binding이 있는 plan은 self-declared mode와 무관하게 preservation으로만 허용하고 payload lineage audit를 다시 수행한 뒤, active external reference가 있는 migration은 cascade target과 wiki directory exchange를 journal v2의 `PREPARED→EXTERNAL_WRITTEN→SWAPPED→COMMITTED` 단일 transaction으로만 적용한다 | 독립 cascade apply·mode downgrade·audit 생략·copy/delete wiki fallback·`EXDEV` 금지 |
| BR-MIG-008 | 결합 apply·restore가 중단되면 | journal의 operation과 requested `repo/wiki`, resolved plan, cascade plan binding 및 current/candidate tree·external digest 조합으로 rollback 여부만 결정한다. non-committed apply는 wiki base+external base, non-committed restore는 restore 시작 상태인 wiki target+external target으로 수렴시키며 candidate는 모든 terminal state에서 보존한다. 이후 cascade는 canonical terminal journal의 knowledge root·operation·state·candidate path와 state별 tree digest가 결속된 candidate만 reserved rollback artifact로 제외한다 | `CONFLICT`·미지 digest·임의 root 자동 수정·candidate 자동 삭제·prefix-only/nonterminal/digest-mismatched candidate 제외·reserved root symlink/special 허용·wiki-only 또는 external-only terminal state 금지 |
| BR-MIG-009 | path 또는 stable ID가 바뀌는 apply를 검사하면 | checker 전·후 repository snapshot에서 active 이전 path·이전 stable ID 참조를 모두 거부하고 checker impact에는 이전·목표 canonical universe를 함께 넣는다 | append-only historical log와 immutable artifact는 active dependency가 아니며, 미래 동시 writer까지 잠금 없이 배제했다고 주장 금지 |
| BR-MIG-010 | preservation resolution을 로드하면 | current 75-page universe와 source order·digest·base tree, target ID uniqueness, collection 1개·Members 정확히 52개와 legacy index link exact-order를 검증한다 | partial/default 보완·51/53/reorder 금지 |
| BR-MIG-011 | legacy page를 clipping으로 capture하면 | BR-ART-010의 동일 leaf가 만든 payload digest가 승인 source digest와 일치하는지 write 전에 확인하고 logical locator source identity를 보존한다 | digest 불일치 orphan revision write·별도 migration sanitizer·clipping의 사실성·최신성 확대 해석 금지 |
| BR-MIG-012 | preservation target을 render하면 | BR-ART-010 정규화 뒤의 legacy body를 보존하고 H2·path만 구조적으로 변환하며 Claims·Relations row는 0으로 둔다 | 개인 홈 prefix 복원·claim·typed relation 자동 추론 금지 |
| BR-MIG-013 | no-apply preservation preview를 실행하면 | temp sibling에서 target tree·checker·75-page privacy-normalized payload parity를 의무 검증하고 active external reference를 apply blocker로 보고한 뒤 final preview를 atomic no-replace 게시한다 | audit 선택화·partial final·immutable `raw/**` artifact의 live dependency 판정 금지 |
| BR-MIG-014 | resolved plan target frontmatter가 content-addressed preservation manifest를 선언하면 | operation payload에서 manifest binding을 독립 판별하고 `resolution_mode=generic`을 preview·backup·apply 전에 거부한다 | self-declared discriminator만 신뢰한 lineage audit 우회 금지 |
| BR-MIG-015 | external-reference cascade plan을 만들면 | active owner를 고정 owner 집합으로 전수 분류하고 canonical question-pack은 `sourceRefs.path` 외 필드를 보존하며 generated JS는 target tree에서 기존 generator로 재생성하고 각 operation의 path·owner·action·base/target bytes·mode를 resolved plan과 결속한다 | 독립 cascade apply·미분류 owner·직접 generated 편집·append-only `log.md` 과거 경로 rewrite 금지 |

## 4. 컬렉션과 관계 규칙

### Collection

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-COL-001 | page들이 강의 시리즈·학습 경로·주제 묶음을 이루면 | CollectionPage 하나가 membership을 소유한다 | 별도 YAML registry 금지 |
| BR-COL-002 | collection member를 추가하면 | BR-COL-005가 결정한 초기 행 위치에 `[[page-id]]`를 한 번 기록한다 | page에 collection backlink 저장 금지 |
| BR-COL-003 | Members row 순서가 바뀌면 | 변경된 행 순서가 새 canonical sequence다 | 숫자 position 이중 저장 금지 |
| BR-COL-004 | collection에 같은 member가 둘 이상 있으면 | reject한다 | 없음 |
| BR-COL-005 | collection member의 초기 행 위치를 결정하면 | ordered lecture/learning path는 review된 `before` 또는 `after` 위치를, 단순 topic group은 명시적으로 선택한 deterministic ID sort를 사용한다 | 세 정책 중 정확히 하나를 선택해야 하며 이후 명시적 reorder는 BR-COL-003 적용 |
| BR-COL-006 | provider playlist 순서와 논리 학습 순서가 다르면 | 별도 CollectionPage로 표현한다 | 한 collection에 두 sequence 저장 금지 |
| BR-COL-007 | member target이 없거나 ambiguous하면 | collection update를 거부한다 | 미래 placeholder link 금지 |

### Relation

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-REL-001 | A의 더 넓은 개념이 B이면 | A에 `broader -> [[B]]` 직접 edge 하나를 저장한다 | B의 narrower inverse 저장 금지 |
| BR-REL-002 | A와 B가 대칭 관련이면 | `min(A.id,B.id)` page에 `related` edge 하나만 저장한다 | self edge 금지 |
| BR-REL-003 | A를 먼저 알아야 B를 학습할 수 있으면 | A에 `prerequisite-of -> [[B]]` edge를 저장한다 | 반대 edge 중복 금지 |
| BR-REL-004 | B가 A 다음 강의·단계를 직접 잇는다면 | A에 `followed-by -> [[B]]` edge를 저장한다 | collection 전체 transitive edge 저장 금지 |
| BR-REL-005 | broader, prerequisite-of, followed-by edge를 추가하면 | 해당 relation graph cycle 검사를 통과해야 한다 | related는 cycle 검사 대상 아님 |
| BR-REL-006 | relation target이 없거나 ambiguous하면 | update를 거부한다 | same apply로 다른 canonical page 생성 금지 |
| BR-REL-007 | inverse·transitive closure 또는 backlink 검사가 필요하면 | checker는 outgoing edge에서 graph를 계산하고 Obsidian은 outgoing link에서 backlink view를 계산한다 | persistent cache와 materialized backlink 파일 금지 |

## 5. 생성물과 검증 규칙

아래 규칙은 최종 목표 rule-set이다. 전환 중 validator rule의 활성 상태는 `scripts/knowledge/check.py`의 `RULE_REGISTRY`가 소유하고, `_meta/knowledge-requirements.json`은 FR/NFR의 requirement-to-step·implementation/verification surface coverage를 소유한다. `inactive-until-*` rule은 명시된 순서에서 구현·검증 surface와 함께 `active`로 전환되기 전까지 BR-CHK-001의 “현재 활성 normative” 집합에 포함하지 않는다.

| ID | IF | THEN | 예외 |
|---|---|---|---|
| BR-GEN-001 | schema·registry·canonical page가 주어지면 | strict UTF-8·finite JSON schema와 validated registry를 입력으로 deterministic sort·serialization generated surface를 만든다. title·summary는 CR/LF 없는 단일 행이고 domain label은 CR/LF/`|` 없는 table-safe 문자열이며, `domains/`의 canonical page는 registry `active` domain에만 존재해야 한다 | wall clock 직접 사용, malformed/non-finite schema, display control 입력 수용, inactive·unregistered domain page 포함 금지 |
| BR-GEN-002 | generated 파일을 commit하면 | Markdown은 comment marker, Base는 공식 `formulas._generated_by` constant formula에 generator identity와 schema digest를 정확히 한 번 포함한다 | marker 없는 기존 파일은 migration gate; Base formula는 view `order`에 포함 금지 |
| BR-GEN-003 | `materialize --check`가 실행되면 | 독립 검증된 expected in-memory map과 repository bytes를 비교하고 차이가 있으면 non-zero다 | 자동 수정 금지 |
| BR-GEN-004 | materialize를 같은 입력으로 두 번 실행하면 | 두 tree hash가 같아야 한다 | 다르면 nondeterminism HIGH |
| BR-GEN-005 | active page가 추가·이동·archive되면 | 다음 materialize에서 index와 overview가 반영한다 | canonical page가 index를 직접 수정 금지 |
| BR-GEN-006 | generated manifest를 만들면 | index 1, overview 1, schema PageType exact set의 각 값별 template 1, `knowledge-pages.base` 1로 `3 + |PageType|` path를 만든다 | 고정 template 수·enum 복제·domain별 Base 파일·별도 template registry 금지 |
| BR-GEN-007 | index를 render하면 | registry domain key, page type, stable ID 순으로 active page를 100% 열거하고 collection을 별도 열거한다 | staging·archive 포함, overview의 page 목록 중복 금지 |
| BR-GEN-008 | overview를 render하면 | registry의 모든 domain label·status·active count와 active collection count를 출력한다 | canonical count 저장·active page 재열거 금지 |
| BR-GEN-009 | template을 render하면 | `schema.py`가 공개한 schema property·PageType·section/table contract에서만 파생한다 | legacy property·schema 밖 section·table header 복제·canonical page validation 금지 |
| BR-GEN-010 | Bases를 render하면 | 단일 Base의 global `filters.or`에 active canonical root 두 개만 두고 All active, active domain key 순서의 domain view, Collections view를 공식 `file.inFolder`·`order` syntax로 만든다. `order`의 note property는 Obsidian UI canonical identifier를 사용하고 sequence indentation·alias-free serialization을 고정한다 | persistent backlink·domain별 Base·SQL/Dataview식 source·Obsidian 저장 시 bytes drift 금지 |
| BR-GEN-011 | generated write mode를 실행하면 | renderer와 분리된 validator가 독립 canonical universe에서 expected path·ownership marker 위치·YAML·index/overview coverage·template/Base 구조를 먼저 검증한다. shared lock 안에서 regular parent directory descriptor의 device/inode, preflight leaf bytes·device·inode·mode, temp bytes digest·device·inode·mode를 결속하고 atomic exchange 뒤 target bytes와 displaced identity를 확인해 path 순서로 missing leaf create와 ownership-bearing leaf replace만 수행한다. 중단 잔여 managed-name temp는 Markdown comment 또는 Base formula generator marker가 있는 own leaf만 다음 preflight에서 제거한다 | marker 없는 leaf overwrite·parent symlink 교체 추종·preflight 뒤 다른 leaf overwrite·bytes만 같은 경쟁 inode rollback·markerless temp 삭제·unknown generated leaf 삭제·canonical full-tree exchange 금지 |
| BR-GEN-012 | generated leaf 적용 중 실패하면 | canonical page 변경은 0이고 `--check`가 partial derived drift를 실패로 보고하며 같은 입력 재실행이 target bytes로 수렴한다 | generated 전체 원자성을 canonical transaction으로 확대하거나 drift를 성공 처리 금지 |
| BR-GEN-013 | generated marker를 render·validate하면 | generator identity `cs-study-materializer/1.0`과 current schema SHA-256을 Markdown exact comment grammar 또는 Base의 exact `formulas._generated_by` constant formula grammar로 한 번 기록한다 | marker 생략·중복·다른 generator·stale schema digest·Base marker formula의 화면 열 노출 허용 금지 |
| BR-GEN-014 | 순서 8 최초 전환 commit을 만들면 | 기존 markerless generated 8개는 검증된 expected bytes로 교체하고 missing 3개를 생성한 뒤 정상 materialize 계약만 남긴다 | runtime adoption option·영구 migration branch·markerless steady-state replace 금지 |
| BR-CHK-001 | 현재 활성 normative schema/문서에 hard rule이 선언되면 | rule registry에 구현 rule ID가 있어야 한다 | historical·superseded 절과 구현·검증 surface가 아직 활성화되지 않은 `inactive-until-*` rule은 제외하고, active rule ID가 없으면 `UNSUPPORTED_RULE` HIGH |
| BR-CHK-002 | `check --changed`가 실행되면 | changed page와 graph상 직접 영향 surface를 동일 rule implementation으로 검사한다 | 별도 축소 rule 정의 금지 |
| BR-CHK-003 | CLI `check --all` 또는 `lint.py` 검사가 실행되면 | read-only dispatcher가 explicit·changed·default input inventory를 한 번만 수행하고 path·Git·필수 root inventory 실패를 HIGH로 수렴한 뒤, hidden 포함 canonical scope의 checker 결과와 materializer의 실제 generated parity 결과를 단방향 조립한다. changed inventory는 repository root에 결속한 모든 Git NUL-delimited path bytes를 Markdown suffix 판정 전에 strict UTF-8로 해석하고 explicit path도 같은 UTF-8 경계를 사용한다. Git status를 보존해 wiki 삭제·이동은 현재 `WIKI_DIR` canonical 검사로 수렴한다. non-wiki 삭제는 current leaf가 부재할 때만 skip하고 재등장한 leaf는 current inventory로 검사하며 malformed status·빈/비정규 path record는 HIGH로 거부한다. 사람용 report의 path·message는 제어문자를 한 물리 행 escape로 출력하고 Markdown delimiter를 escape한다. CLI는 합성 structural verdict·findings·exclusions를 보고하고 lint는 동등한 HIGH findings·exit semantics를 반환한다 | `.git`, declared cache·venv 제외; 호출자 working directory Git 사용, 줄바꿈 기준 path 분리, non-Markdown path decode 생략, surrogateescape·raw control·Markdown delimiter 출력 누출, AST surface 존재를 VR-KP-017·018 실행으로 치환, 두 번째 inventory, wiki rule 복제·legacy validator·canonical 실패 fallback 금지 |
| BR-CHK-004 | HIGH finding이 하나 이상이면 | promote·CI는 실패한다 | 사용자 위험 수용으로 CI PASS 치환 금지 |
| BR-CHK-005 | 구조 check가 성공하면 | structural verdict만 PASS로 보고한다 | 사실성·완전성 PASS로 확대 금지 |
| BR-CHK-006 | semantic review가 수행되면 | review 대상 claim마다 `support`, `contradiction`, `insufficient` 중 하나의 evidence verdict를 기록한다 | page-level 감상 판정 금지 |
| BR-CHK-007 | 사람이 generated 파일을 수정하면 | regeneration diff로 실패한다 | generated 내용에서 정책 수정 금지 |
| BR-CHK-008 | local hook이 실행되면 | extractor는 index와 다른 unstaged·untracked file 0을 확인한 뒤 source tree Ruff와 contract·architecture 빠른 test를 실행한다. cs-study는 dependency-free system Python 표준 라이브러리 bootstrap으로 `--name-status -z --no-renames` inventory 실패와 staged Markdown의 index·worktree 직접 불일치를 거부한다. 전체 Git index의 임시 격리 tree가 소유한 Python patch·lint dependency에서 non-delete 후보 전체를 `scripts/lint.py --repository-paths`로 전달하고, repository lint owner가 dot-segment와 symlink ancestor를 해소한 canonical parent로 scope를 filter하면서 원래 leaf identity를 inventory에 전달한다. Markdown 삭제가 하나라도 있으면 mixed write-set 전체를 default repository lint로 수렴시킨 뒤 contract·project-boundary 빠른 test를 실행한다. 선행 하이픈 path는 `./`로 명시하고 snapshot 생성·회수 실패는 non-zero이며 두 hook은 feedback만 제공한다 | hook의 repository scope 복제·lexical path를 통한 scope 우회·leaf symlink 타입 소실·bootstrap의 worktree dependency·working tree의 untracked target·unstaged sibling·test repair로 staged 결함 은폐·repository default scope 밖 문서를 legacy lint로 확대·mixed write-set 덮어쓰기·rename의 source 삭제 누락·branch 전체 diff를 staged 입력으로 오인·선행 하이픈의 option 해석·공백·개행 경로 분해·Git inventory·snapshot 실패 은폐·required CI authority 대체 금지 |
| BR-CHK-011 | required CI가 실행되면 | 각 저장소가 상대 저장소 없이 독립 실행되고, architecture §10의 canonical CI profile을 사용한다. cs-study는 schema 포함 전체 test·full check·materialize parity·repository lint를 모두 통과해야 merge-eligible이다 | local hook 성공·canonical profile 이탈·상대 저장소 checkout·검증 일부 생략으로 성공 처리 금지 |
| BR-CHK-012 | persistent privacy boundary가 project·wiki·raw web Markdown과 active artifact를 검사하면 | 각 Markdown tree의 directory·`.md` entry를 non-symlink inventory로 먼저 검증하고 content를 해당 trust anchor의 공용 reader로 읽으며, artifact manifest·payload는 하나의 bundle descriptor context에서 읽는다 | `rglob` 결과의 direct `read_text`, symlink·FIFO content read, checker·lint 선행 성공 의존 금지 |
| BR-CHK-009 | canonical page candidate full check를 실행하면 | current canonical base의 generated repository parity, candidate overlay의 canonical rule, candidate expected index·overview coverage를 순서대로 검증한다 | 선행 generated drift 허용·candidate expected bytes와 pre-materialize repository bytes의 동일성 요구·generated 암묵 write 금지 |
| BR-CHK-010 | canonical page 또는 taxonomy를 검사하면 | taxonomy canonical·alias 정의의 중복·충돌을 먼저 거부하고 tag와 entity page·경로형 entity wikilink를 같은 `VR-KP-023` 구현으로 검사한다 | 일반 concept wikilink를 entity로 분류하거나 alias를 자동 치환 금지 |

## 6. 상태 전이

### ArtifactBundle

| 시작 | 종료 | 조건 |
|---|---|---|
| Input | Rejected | path, contract, digest, media type 검증 실패 |
| Input | Existing | 동일 source ID와 digest bundle이 완전하게 존재 |
| Input | Staged | 신규 digest를 temp directory에 완전 작성 |
| Staged | Committed | bundle schema·digest 검증 후 atomic rename |
| Staged | Rejected | 검증 또는 rename 실패, temp 회수 |

### KnowledgePage

| 시작 | 종료 | 조건 |
|---|---|---|
| SemanticPlan | Rejected | schema, source, collision, evidence 검증 실패 |
| SemanticPlan | PageWritePlan | strict schema·source exact match·domain·ID·candidate 검증 성공 |
| PageWritePlan | Rejected | plan/schema/base tree/source digest/target precondition/candidate check 불일치 |
| PageWritePlan | Draft | confirmed synthesize plan이 staging Markdown 한 개 atomic create |
| Draft | Active | full check + BR-LIFE-005 claim verdict exact/status gate + review approval + atomic rename |
| Draft | Draft | review 수정 후 base digest 일치 atomic replace |
| Active | Active | base digest 일치 update |
| Active | Archived | P2-T5 이후 별도 승인된 explicit archive transition |
| Archived | Draft | explicit restore review 시작 |

Draft·Active·Archived는 경로에서 배타적으로 결정된다. 파일 하나가 두 lifecycle 상태를 동시에 가질 수 없다.

### Claim

매 review는 BR-CLM-004 → BR-CLM-003 → BR-CLM-002 → BR-CLM-001 순서로 목표 상태를 한 번 계산한다. 최초 상태는 그 결과이며, 기존 상태와 목표 상태가 다르면 evidence set 또는 review verdict가 변경된 경우에만 전이한다. 따라서 `claimed → verified` 직접 전이와 evidence 변경에 따른 강등을 모두 허용한다. `rejected`에서 다른 상태로 복구할 때는 새 evidence와 review를 모두 요구한다.

## 7. 검증 규칙

| ID | 대상 | 결정 조건 | 실패 |
|---|---|---|---|
| VR-KP-001 | contract | supported `$id`와 version | reject |
| VR-KP-002 | payload | digest·size·media type 일치 | corruption reject |
| VR-KP-003 | artifact path | source type/source ID/digest scope | reject |
| VR-KP-004 | DocumentInstance | JSON Schema 2020-12 assertions 전부 충족 | reject |
| VR-KP-005 | property | unknown·type·enum·conditional field 없음 | reject |
| VR-KP-006 | section | page type별 exact order와 cardinality | reject |
| VR-KP-007 | page ID | filename stem 규칙·전역 유일 | reject |
| VR-KP-008 | wikilink | target 정확히 1개 | reject |
| VR-KP-009 | source_paths | manifest 실재·중복 0 | reject |
| VR-KP-010 | claim | local ID unique·status·evidence 유효 | reject |
| VR-KP-011 | collection | member 실재·중복 0·ordered rule | reject |
| VR-KP-012 | related | canonical owner page에만 1 edge | reject |
| VR-KP-013 | directed relation | broader/prerequisite-of/followed-by cycle 0 | reject |
| VR-KP-014 | lifecycle | path와 허용 operation 일치; `domains/<key>/` page는 registry에 등록된 active domain만 허용 | reject |
| VR-KP-015 | update/replay | 최초 apply는 invoked operation·operation input digest·current bytes/mode와 plan base 일치; replay는 exact target tree·page bytes/mode·move source 부재 및 plan base bytes 기반 operation delta 일치 | 그 밖의 상태는 stale reject |
| VR-KP-016 | 일반 lifecycle·page command write-set | shared repository lock 안에서 logical knowledge page 최대 1, plan·base/target tree digest와 operation-specific delta 일치 | reject; future global migration은 현재 runtime 예외가 아니며 별도 설계·승인 필요 |
| VR-KP-017 | generated repository parity | current canonical base에서 render·validate한 exact manifest·Markdown comment/Base formula generator-schema marker·valid YAML·expected in-memory bytes가 current repository generated bytes와 일치하고, Base bytes가 Obsidian UI canonical serialization과 일치 | `materialize --check`·순서 10 CI·page candidate base precondition에서 drift reject; candidate expected bytes와 repository 비교 금지 |
| VR-KP-018 | generated index·overview | 검증 대상 canonical tree에서 render한 expected map이 active page coverage 100%, archived/staging 0%, domain·collection count 일치를 만족 | current tree는 `materialize --check`·CI, candidate tree는 page candidate full check에서 reject; repository parity와 독립 |
| VR-KP-019 | architecture | 최종 core+contract edge set exact(10 modules·16 edges)·command-inclusive 12 modules·18 edges·cycle 0·최대 dependency edge chain 3 | runtime checker는 core+contract exact set·cycle·depth reject; project boundary AST test는 command-inclusive exact set·cycle·depth reject |
| VR-KP-020 | rule coverage | 현재 활성 normative hard rule마다 executable rule ID 존재. historical·superseded 규칙과 구현·검증 surface가 아직 활성화되지 않은 `inactive-until-*` rule은 실행 대상에서 제외 | unsupported reject |
| VR-KP-021 | replay | 동일 input tuple의 output tree hash 동일 | nondeterminism reject |
| VR-KP-022 | semantic gate | primary claim ID exact set·verdict enum·status matrix 일치, `claimed`·`insufficient` 0건 | active promotion reject |
| VR-KP-023 | taxonomy | canonical·alias 정의 중복·충돌 0; tag와 entity page·경로형 entity wikilink는 canonical vocabulary만 사용 | unknown HIGH reject; alias MEDIUM canonical 안내 |

## 8. 완료 술어

| 명제군 | 입력 | 기대 결과 | 확인 surface |
|---|---|---|---|
| Artifact immutability | 같은 source의 같은/different bytes | same=no-op, different=new bundle, old bytes 동일 | artifact integration test |
| Atomic capture | bundle write 단계별 injected failure | final partial bundle 0, 기존 bundle 동일 | failure-injection test |
| Page atomicity | create·replace·move pre/post-commit failure와 cooperative/non-cooperative race | pre-commit·safe rollback은 own leaf bytes·mode가 base, rollback 전에 관찰된 same-leaf conflict는 외부 bytes를 보존한 indeterminate, 관찰 이후 새 경합은 보장 범위 밖, crash는 base 또는 target, 성공은 target tree 일치 | filesystem integration test |
| Stable identity | active page move | filename stem 동일, resolved link 단일 | move integration test |
| Collection sequence | member add/reorder | collection 한 파일만 canonical diff | write-set assertion |
| Relation integrity | cycle/inverse/symmetric duplicate fixture | 각 invalid fixture non-zero | graph parameterized test |
| Schema ownership | 파생물·fixture 미갱신 비호환 required field/section enum mutation | parser·renderer·materializer(template 포함)·checker contract test 동시 실패 | mutation test |
| Generated idempotence | materialize 2회 | tree hash 동일 | materialize integration test |
| Index completeness | active/staging/archive fixture | active 100%, 나머지 0% 등재 | index test |
| Boundary independence | 각 저장소 clean environment | 상대 source import 없이 독립 test success | CI job |
| Semantic grounding | primary claim과 evidence artifact | support/contradiction/insufficient 중 명시 verdict | grounding review |

제거된 global migration safety 완료 술어와 failure-injection test는 전환 실행 보고서가 보존하는 historical evidence이며 현재 완료 술어가 아니다.

## 9. 논리 일관성 검증

| 규칙 | 잠재 충돌 | 해소 |
|---|---|---|
| BR-ART-003 vs BR-ART-004 | 동일 source의 skip과 revision 생성 | payload digest 조건이 배타적이다 |
| BR-SYN-004 vs BR-APPLY-004 | 여러 source와 one-page write | 여러 source는 한 page의 evidence이며 write page는 하나다 |
| BR-PAGE-002 vs page rename | title 변경과 stable ID | filename stem은 title slug가 아니라 생성 후 immutable ID다 |
| BR-LIFE-002 vs lifecycle metadata | promote 시 status 변경 필요 | status를 저장하지 않고 path에서 파생해 content rename만 수행한다 |
| BR-COL-003 vs numeric position | row order와 position drift | position field를 저장하지 않는다 |
| BR-REL-002 vs outgoing-only | symmetric relation의 양 endpoint 필요 | canonical smaller-ID owner 한 곳만 저장한다 |
| BR-GEN-005 vs one-page apply | index도 함께 갱신해야 함 | apply와 materialize를 별도 command/commit 단계로 분리한다 |
| BR-CHK-005 vs NFR 의미 안전성 | 구조 성공을 전체 성공으로 오인 | structural·semantic verdict를 별도 필드로 보고한다 |
| BR-APPLY-004·VR-KP-016 vs historical BR-MIG-007 | 일반 lifecycle·page command는 one-page이나 완료된 schema migration은 multi-page였다 | historical migration은 exact universe·별도 schema·backup·사용자 승인·atomic full-tree exchange를 적용했고 현재 runtime에서 제거했다 |

분기 커버리지:

- artifact: invalid, same digest, new digest, corruption을 모두 정의했다.
- page lifecycle: draft, active, archive, restore와 invalid direct transition을 정의했다.
- relation: directed, symmetric, missing target, self/duplicate, cycle을 정의했다.
- collection: ordered, unordered deterministic sort, duplicate, missing member를 정의했다.
- apply: create, update, stale, collision, injected failure를 정의했다.
- generated: clean parity, missing path, marker/schema mismatch, unexpected marker-bearing path, unmarked collision, partial leaf failure, exact replay를 정의했다.

설계 명제 사이의 candidate base parity→canonical overlay→candidate coverage 충돌과 FR-KP-017 추적 누락을 수정했고, 2026-08-28 logic proposition repeat 2 재검증에서 finding 0건이었다. 이 판정은 P2-T6 설계 명제 범위이며 구현·실환경 검증 PASS로 확대하지 않는다.

## 10. 변경 이력

- 2026-08-21: immutable artifact, one-page apply, path-derived lifecycle, collection row-order, outgoing-only relation, fail-closed checker 규칙으로 `archives/design/docs/wiki-ingest-business-logic-v1.md`를 대체했다.
- 2026-08-28: P2-T6 generated marker, official Bases filter/order, schema/table contract 단일 소유, 최초 전환과 steady-state write 분리, candidate base parity→canonical overlay→candidate coverage 검증 순서를 BR-GEN-009–014·BR-CHK-009와 VR-KP-017–019에 고정했다. Obsidian 1.13.7 실환경 저장이 Base 주석·YAML alias·`note.*` 식별자를 정규화하는 결함을 재현해, marker ownership을 보존되는 constant formula로 이동하고 UI canonical serializer·property identifier를 같은 규칙에 추가했다.
- 2026-09-02: 회수되지 않은 순서 6 exact plan·backup bytes를 historical limitation으로 고정하고 현재 runtime·P2-T7 완료 조건과 분리했다.
