# PRD: 지속 가능한 지식 파이프라인

## 1. 문서 상태와 범위

- 상태: `Accepted` — 2026-08-23 사용자 승인; migration apply는 순서 6b와 9에서 각각 별도 승인 필요
- 승인 범위: ADR-0003의 domain registry 결정은 `Accepted`로 유지되며 본 설계의 제약이다. 본 `Accepted` 상태는 그 결정을 포함해 재구성한 end-to-end pipeline 전체에 적용된다.
- 적용 저장소: `007_youtube-script`, `001_cs-study`
- canonical 경로: `docs/wiki-ingest-prd.md`
- 이전 버전: `archives/design/docs/wiki-ingest-prd-v1.md`
- 범위: 외부 콘텐츠 추출 결과의 불변 적재부터 지식 합성, 검토, 승격, Obsidian용 파생 뷰 생성, 지속 검증까지

기존 1차 YouTube importer의 v1 요구 계약과 실행 경로는 2026-08-23 순서 4 immutable ArtifactBundle 전환으로 superseded됐다. `docs/prd.md`, `docs/architecture.md`, `docs/business-logic.md`는 historical non-normative 기록이다. 현재 persistent write·plan·apply 단일 진입점은 `scripts/wiki_ingest.py`이며 exact-file capture·digest revision, `_meta/knowledge.schema.json`, migration plan·resolution schema 계약을 runtime에 활성화한다. `_meta/wiki-ingest-write-plan.schema.json`과 `tests/test_wiki_ingest_schema.py`는 superseded v1 입력의 회귀 기록으로만 보존되며 현재 CLI가 import·호출하지 않는다. 구현 순서 2는 extractor 경계를 supersede했고, 순서 7은 `_meta/knowledge.schema.json`의 `SemanticPlan` synthesis seam을 contract test와 같은 변경에서 활성화한다.

## 2. 문제와 목표

### 문제

- 구조 규칙이 `AGENTS.md`, `_meta/*-spec.md`, template, `scripts/lint.py`에 반복되어 변경 시 drift가 발생한다.
- superseded v1 raw importer의 `--force` 교체 중 JSON rename이 실패하면 새 Markdown을 삭제하고 이전 JSON만 남겨 historical `docs/prd.md`의 `FR-8` pair 원자성과 원본 보존을 위반했다. 이 경로는 현재 runtime에서 제거됐다.
- active wiki 페이지와 index가 동기화되지 않으며 안정 ID, collection, sequence, relation 계약이 없다.
- template은 validator에서 제외되어 schema와 달라도 lint가 성공한다.
- orphan, 논리 충돌, generated drift, idempotent replay를 repository gate가 강제하지 않는다.

### 목표

1. 추출과 지식 관리를 독립시켜 역방향 코드·실행 의존을 0으로 유지한다.
2. 사람이 수정하는 canonical 관리 지점을 최소화하고 파생 산출물은 결정적으로 재생성한다.
3. 원문 artifact를 content digest로 식별하고 overwrite 없이 보존한다.
4. 동일 주제의 복수 source와 강의 sequence를 collection으로 표현한다.
5. 문서 구조, 관계, 근거, 링크, index coverage, DAG, 멱등성을 단일 checker로 검증한다.
6. 의미 정확성은 정적 보장 대상으로 오인하지 않고 evidence review와 승격 게이트로 통제한다.

## 3. 소유권과 범위

| Surface | Owner | Canonical 입력 | 허용 산출 | 금지 |
|---|---|---|---|---|
| 콘텐츠 추출 | `007_youtube-script` | URL·provider 입력 | versioned canonical transcript payload와 screen artifact | `001_cs-study` import·경로·schema 인지 |
| artifact 적재 | `001_cs-study` capture | 명시적 외부 artifact | immutable artifact bundle | 기존 bundle overwrite·무차별 output scan |
| 지식 합성 | `001_cs-study` synthesize | 명시적 artifact manifest 목록과 SemanticPlan | 검증 가능한 single-page resolved plan, 승인된 plan apply 뒤 draft 한 개 | raw 수정·LLM 직접 page path·rendered Markdown·write operation 지정 |
| 지식 승격 | `001_cs-study` promote | 검토된 draft 한 개 | canonical wiki page 한 개 | 다중 page 암묵 갱신 |
| navigation 생성 | materializer | schema·domain registry·canonical wiki | index·overview·templates·Bases | generated 파일 수동 정책 소유 |
| 검증 | checker | schema·registry·artifact·wiki·generated | deterministic findings | 자동 사실성 판정 |

의존 방향은 `001_cs-study → versioned artifact contract ← 007_youtube-script`의 소비 방향으로만 존재한다. 두 저장소의 Python 모듈 import와 callback 주입은 허용하지 않는다.

## 4. 기능 요구사항

| ID | 요구사항 | 관찰 가능한 수용 기준 |
|---|---|---|
| FR-KP-001 | extractor는 provider-agnostic canonical payload를 출력한다 | payload가 versioned contract를 만족하고 cs-study 식별자·경로가 0건이며 exact payload path를 CLI 결과로 반환한다 |
| FR-KP-002 | capture primitive는 명시적 artifact 하나만 적재한다 | 디렉토리 전체 암묵 scan 없이 입력 경로 하나를 처리한다. 전환 batch는 승인 resolution의 명시적 경로마다 이 primitive를 한 번씩 조합한다 |
| FR-KP-003 | artifact bundle은 primary capture-contract bytes의 SHA-256로 식별한다 | clipping Markdown은 Apple·Windows local-user-home prefix를 `<local-user-home>`으로 결정적 치환하고, 그 밖의 입력은 exact bytes를 사용하며 manifest digest·size가 저장 payload와 일치한다 |
| FR-KP-004 | 동일 digest 재적재는 no-op이다 | 두 번 실행 후 파일 목록과 bytes가 동일하다 |
| FR-KP-005 | 동일 source의 다른 digest는 새 revision이다 | 기존 bundle 변경 0, 신규 digest directory 1개 증가 |
| FR-KP-006 | 합성 source universe는 manifest 경로의 명시적 목록이다 | SemanticPlan의 `source_paths`와 CLI `--source` 목록이 exact match하고 implicit latest 선택과 wiki 재-ingest가 거부된다. current vault는 collision·graph 검증 context일 뿐 source universe가 아니다 |
| FR-KP-007 | LLM 결과는 SemanticPlan일 뿐 page write 권한이 없다 | path·frontmatter·derived field·rendered Markdown·write operation 입력이 거부되고 Python이 strict PageWritePlan으로 재계산한다 |
| FR-KP-008 | 지식 페이지는 안정적이고 전역 유일한 ID를 가진다 | `id`가 vault 전역에서 1회 나타나고 이동 후에도 변하지 않는다 |
| FR-KP-009 | wiki basename은 전역 유일하다 | `[[id]]`가 단일 페이지로 결정되며 중복 basename 0건이다 |
| FR-KP-010 | 한 페이지는 여러 source artifact를 근거로 가질 수 있다 | `source_paths`가 존재하는 manifest만 포함하고 중복 값 0건이다 |
| FR-KP-011 | claim은 상태와 evidence를 함께 가진다 | 고정 Claim table의 모든 행이 유효 status와 실재 evidence를 가진다 |
| FR-KP-012 | collection page가 membership와 순서를 단독 소유한다 | `Members` table 행 순서가 sequence이고 동일 member 중복 0건이다 |
| FR-KP-013 | relation은 subject page의 outgoing edge만 저장한다 | inverse edge 수동 저장 0건이며 derived backlink로 조회 가능하다 |
| FR-KP-014 | 계층·선행 관계의 순환을 차단한다 | `broader`, `prerequisite-of`, `followed-by`별 directed cycle 0건이다 |
| FR-KP-015 | draft와 active lifecycle을 분리한다 | promote PageWritePlan은 모든 primary claim의 claim ID별 evidence verdict를 결속하고 명시적 review 승인 없는 draft→active apply가 실패한다. `support`는 `corroborated`·`verified`, `contradiction`은 `rejected`와만 정합하며 `insufficient`가 하나라도 있으면 승격하지 않는다 |
| FR-KP-016 | 일반 lifecycle·page command의 한 apply는 knowledge page를 최대 한 개만 변경한다 | PageWritePlan의 logical page write-set이 0 또는 1이고 plan SHA-256이 일치하며 current tree가 base tree와 일치할 때만 최초 apply한다. replace는 source base bytes·digest·mode 일치를, create는 target 부재를, move는 source base bytes·digest·mode 일치와 target 부재를 모두 추가로 요구한다. current tree·target page bytes·mode·move source 부재와 plan base bytes 기반 operation delta가 target state와 정확히 일치하는 confirmed plan replay만 idempotent no-op이고, 그 밖의 tree는 stale이다. 빈 write-set no-op은 base와 target tree가 같아야 한다. NFR-KP-015의 사용자 승인 전역 schema migration은 별도 resolved-plan·backup·full-tree transaction 규칙을 따른다 |
| FR-KP-017 | generated navigation을 재생성한다 | index, overview, templates, Bases가 schema, domain registry, canonical wiki에서 byte-identical하게 생성된다 |
| FR-KP-018 | checker는 전체 vault와 변경 파일 모드를 제공한다 | `check --all`과 `check --changed`가 동일 rule set을 사용한다 |
| FR-KP-019 | 모든 구조 규칙은 단일 machine-readable owner를 가진다 | required fields·enum·section·relation의 독립 규칙 정의가 schema 밖 코드 상수와 문서 표에 0건이다 |
| FR-KP-020 | 검증 finding은 fail-closed로 처리한다 | HIGH finding 또는 unvalidated generated drift가 있으면 promote와 CI가 non-zero다 |
| FR-KP-021 | image/reference asset은 content-addressed로 보존한다 | 동일 bytes no-op, 변경 bytes 신규 digest, 기존 bytes overwrite 0건이다 |
| FR-KP-022 | 페이지 이동은 ID를 보존한다 | move plan의 source와 target filename stem이 같고 lifecycle root가 유지되며, apply 전 candidate graph의 broken link가 0건이다. staging→active는 move가 아니라 promote만 소유한다 |

요구사항과 설계 문서의 필드·enum·section·relation 열거는 적용 범위를 설명하는 비권위 참조다. 구현 후 checker가 schema와의 drift를 검출하며, 열거 자체는 별도 규칙 owner가 아니다.

## 5. 비기능 요구사항

| ID | 요구사항 | 기준 |
|---|---|---|
| NFR-KP-001 | 단방향 의존 | module·command·document ownership graph cycle 0 |
| NFR-KP-002 | 낮은 호출 깊이 | 신규 자기 코드 함수 5개 미만 직렬(= 호출 edge 4 미만)을 목표로 하고 호출 edge 4 이상이면 설계 경고 |
| NFR-KP-003 | 독립성 | extractor 단독 테스트와 vault checker 단독 테스트가 상대 저장소 없이 실행된다 |
| NFR-KP-004 | 불변성 | committed content-addressed ArtifactBundle payload와 manifest의 in-place mutation 0; legacy flat raw source의 privacy remediation은 별도 승인 변경으로 추적 |
| NFR-KP-005 | 멱등성 | 동일 input digest·schema digest·generator version·normalized command options에서 두 번 실행한 결과 bytes와 exit semantics 동일 |
| NFR-KP-006 | 결정성 | clock·UUID·정렬·locale을 주입 또는 고정하고 출력 순서를 명시한다 |
| NFR-KP-007 | 완전성 | 입력 manifest의 모든 source와 primary claim이 page의 provenance/evidence로 추적된다 |
| NFR-KP-008 | 정합성 | schema→parser instance→cross-document checker→generated materializer가 동일 용어를 사용한다 |
| NFR-KP-009 | 안전성 | validate-before-write를 적용하고 동일 knowledge root를 변경하는 ordinary apply와 migration apply·restore·recover는 repository-root shared advisory lock을 사용한다. raw append-only artifact capture는 이 lock의 참여자가 아니라 독립 atomic capture primitive를 사용한다. ordinary apply는 write 직전 optimistic base bytes·mode 재검증, single-page atomic leaf commit과 실패 rollback을 적용한다. 잠금을 따르지 않는 외부 writer를 filesystem-wide CAS로 배제했다고 주장하지 않는다. rollback 전에 이미 관찰된 same-leaf 외부 변경은 덮지 않고 indeterminate로 보고하지만 관찰과 syscall 사이의 새 non-cooperative 경합은 무손실 보장 범위 밖이다. 내부 failure injection은 own leaf를 이전 bytes·mode로 복구하고 rollback 자체가 실패하면 observed state를 포함한 indeterminate error로 보고한다. process crash 뒤 leaf는 atomic namespace operation의 base 또는 target 상태이며 exact replay로 재판별한다 |
| NFR-KP-010 | 최소 관리 지점 | backlinks, inverse relation, counts, index, log를 canonical로 수동 관리하지 않는다 |
| NFR-KP-011 | Obsidian 호환 | flat YAML property와 standard Markdown table·wikilink만 canonical 표현에 사용한다 |
| NFR-KP-012 | 확장성 | source type, page type, relation type 추가가 각각 소유 schema/registry 한 곳에서 시작한다 |
| NFR-KP-013 | 검증 지속성 | local hook은 feedback, required CI check는 merge authority로 분리한다 |
| NFR-KP-014 | 의미 안전성 | 정적 checker가 사실성 PASS를 주장하지 않고 review evidence를 요구한다 |
| NFR-KP-015 | 보존성 | migration은 root를 포함한 exact path·type·mode·bytes manifest, resolved-plan digest, 검증된 backup, stale refusal, 같은 파일시스템의 atomic directory exchange와 crash recovery를 요구한다. journal에 결합된 rollback candidate는 자동 삭제하지 않으며 기존 사용자 wiki를 암묵 수정하지 않는다 |

## 6. 산출물과 사용자 흐름

```text
external source
  -> extractor / capture adapter
  -> immutable artifact bundle
  -> SemanticPlan
  -> synthesize(plan-only PageWritePlan)
  -> plan SHA 확인
  -> synthesize(plan apply, semantic draft 한 개)
  -> structural + evidence review
  -> promote(one canonical page)
  -> materialize(generated navigation)
  -> check(local + CI)
```

### 정상 흐름

1. 사용자가 source 또는 extractor artifact 경로를 명시한다.
2. capture가 source type·media type별 capture contract를 적용하고 payload digest를 계산해 immutable bundle을 만든다.
3. synthesize가 한 개 이상의 명시적 manifest와 SemanticPlan을 받아 Python-generated PageWritePlan 한 개를 no-write로 게시한다.
4. checker가 PageWritePlan의 candidate page를 schema, IDs, source, claims, relations, link, collision 기준으로 검증한다.
5. 사용자가 plan SHA-256을 확인해 apply하면 staging draft 한 개만 생성된다.
6. 사람이 claim grounding과 collection 순서를 검토한다.
7. promote가 별도 PageWritePlan의 plan SHA-256·base tree digest·draft base digest·target collision·BR-LIFE-005 claim verdict exact/status gate·명시적 review 승인을 확인하고 content bytes를 바꾸지 않은 채 active path로 atomic rename한다.
8. materializer가 navigation과 template을 재생성한다.
9. CI가 full check와 regeneration diff를 실행한다.

### 복수 강의 흐름

- 각 영상은 독립 Source와 하나 이상의 immutable Artifact로 적재한다.
- 여러 영상을 하나의 KnowledgePage 근거로 합성할 수 있다.
- 강의 시리즈 또는 논리적 학습 순서는 CollectionPage의 `Members` 행 순서가 소유한다.
- page는 자신이 어느 collection에 속하는지 역참조를 저장하지 않는다.
- provider playlist 순서와 논리 학습 순서가 다르면 서로 다른 collection으로 표현한다.

## 7. 범위 제외

- RDF triple store, OWL reasoner, SHACL canonical validation
- persistent backlinks 또는 inverse relation registry
- 사람이 병행 관리하는 wiki log와 index
- 자동 taxonomy/domain 생성 및 자동 active 승격
- LLM의 raw 또는 canonical wiki 직접 쓰기
- 모든 자연어 명제의 사실성·완전성 자동 판정
- 한 command에서 여러 canonical page를 암묵 갱신하는 cascade
- 승인된 resolved plan 없는 현재 dirty 정보보안 wiki 콘텐츠의 구조 migration

PROV-O와 SKOS는 용어와 관계 의미만 참고한다. 별도 RDF 표현은 실제 외부 소비 요구가 생기기 전까지 도입하지 않는다.

## 8. 수용 기준

| ID | 완료 조건 |
|---|---|
| AC-KP-001 | 두 저장소의 정적 import cycle 0, extractor의 cs-study 전용 hook 0 |
| AC-KP-002 | canonical artifact schema와 fixture가 versioned contract test를 통과한다 |
| AC-KP-003 | 동일 payload 2회 capture 결과 bundle 1개, 다른 payload 결과 revision 2개다 |
| AC-KP-004 | 기존 artifact bytes를 수정하는 실행 경로와 `--force` overwrite 옵션이 0개다 |
| AC-KP-005 | 파생물과 fixture를 갱신하지 않은 비호환 schema-only mutation을 주입하면 parser·renderer·materializer(template 포함)·checker contract test가 함께 실패한다 |
| AC-KP-006 | full vault에서 duplicate ID·basename·broken link·invalid relation·DAG cycle 0 |
| AC-KP-007 | active page의 generated index coverage가 100%다 |
| AC-KP-008 | materialize를 연속 2회 실행한 두 결과 tree hash가 동일하다 |
| AC-KP-009 | cooperative command의 pre-commit 실패와 rollback 가능한 post-commit failure injection 뒤 own knowledge leaf의 이전 bytes·mode가 보존된다. rollback 전에 관찰된 non-cooperative same-leaf conflict는 외부 bytes를 덮지 않은 indeterminate error이고, 관찰과 syscall 사이 새 경합은 보장 범위 밖이며, process crash는 base 또는 target exact state다 |
| AC-KP-010 | collection member 추가는 collection page 한 파일만 canonical 변경한다 |
| AC-KP-011 | page 이동 후 ID가 보존되고 materialized navigation이 새 경로를 가리키며 derived backlink resolution의 broken link가 0건이다 |
| AC-KP-012 | required CI가 schema, tests, full check, materialize diff를 모두 실행한다 |
| AC-KP-013 | promote 시점의 primary claim마다 실재 evidence와 claim-level review verdict가 있고 active page에는 그 결과인 claim status가 지속된다 |
| AC-KP-014 | 검증 결과가 구조 PASS와 의미 review 결과를 별도 필드로 보고한다 |

## 9. 요구사항 추적성

요구사항별 문서 section·Business Logic 매핑은 `docs/wiki-ingest-architecture.md` §14가 소유하고, FR/NFR의 구현 순서와 구현·검증 파일 매핑은 `_meta/knowledge-requirements.json`이 소유한다. 두 surface는 서로 다른 열을 소유하며 같은 mapping을 중복 저장하지 않는다. 본 PRD는 요구사항 ID와 수용 기준만 소유한다.

## 10. 변경 이력

- 2026-08-21: 원본 불변 revision, single-schema, stable ID, ordered collection, outgoing-only relation, generated navigation, fail-closed validation을 포함하는 완전 설계로 `archives/design/docs/wiki-ingest-prd-v1.md`를 대체했다.
