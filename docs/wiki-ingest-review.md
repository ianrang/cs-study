# Review: 지속 가능한 지식 파이프라인 설계 검증

## 1. 검증 범위와 방법

- 대상: `docs/wiki-ingest-{prd,architecture,business-logic,review}.md`, 두 저장소의 관련 코드·schema·wiki scaffold·tests·CI
- 모드: 검증 기록. 설계 단계의 report-only 결과와 이후 별도 승인된 구현·apply·restore 실행 증거를 함께 기록함
- 설계 시작 기준 시각: 2026-08-22. §2–§6의 수치·판정·외부 기준은 당시 historical design baseline이며 현재 구현 판정으로 재사용하지 않는다. 최신 구현·검증 상태는 §7–§9와 변경 이력이 소유한다.
- 검색: hidden 포함 `rg --files -uu`; `.git`, declared virtualenv/cache/vendor만 제외
- 정적 차원: ownership, import/document DAG, schema drift, ID/link/collection/relation, raw immutability, atomicity, idempotence, generated coverage
- 동적 차원: 기존 unit/mock tests, current lint, fixture replay 가능 여부
- 의미 차원: claim-evidence support는 정적 구조와 별도 판정

Task Quality Gate Capsule:

| Field | Value |
|---|---|
| Task ID | KNOWLEDGE-ARCH-DESIGN-003 |
| Task class | L2 design + cross-repository validation |
| Intent | 두 저장소의 extraction→immutable raw→synthesis→review→Obsidian wiki 파이프라인을 단일 ownership과 검증 가능한 규칙으로 설계 |
| SoT | 사용자 요구, 실제 코드, canonical 설계 3문서 |
| Derived | 본 review, traceability, 구현 순서 |
| Forbidden | dirty code/wiki 수정, 검증 전 구현, 중복 schema owner, extractor→cs-study 역의존, canonical↔derived 양방향 쓰기 |
| Invariants | extractor는 wiki를 모름; canonical owner는 concern당 1개; raw revision overwrite 0; generated surface 수동 편집 0; typed directed relation cycle 0; ordinary page apply canonical write 0 또는 1, 승인된 전역 schema migration은 exact full-tree transaction 예외 |
| Completion Predicates | FR/NFR 전수 downstream mapping; logic·grounding finding 0; 구현 drift는 owning implementation step에 전수 매핑; 사용자 최종 설계 승인 |
| Validation Plan | ID·heading·traceability 정적 검사; finding별 단건 재검증; 최종 logic·grounding·requirements 검증; 현행 코드 spec drift 재측정 |
| User-required Gates | 교차 검증 비용·조합 승인; 최종 설계 승인; 기준 worktree·migration dry-run 승인 |
| Promotion Candidates | `_meta/knowledge.schema.json` checker; materialize byte-diff; import-boundary AST test; artifact immutability integration test; required CI |

## 2. 설계 시작 당시 기준선

| 항목 | 실측 |
|---|---:|
| extractor Python modules / import edges / cycles | 20 / 40 / 0 |
| cs-study scripts modules / local import edges / cycles | 8 / 1 / 0 |
| extractor tests | non-network 118 passed(coverage 91.14%); 사용자 제공 영상 실 network frame capture 1 passed |
| cs-study 관련 tests | 47/47 passed |
| current lint | HIGH 0, MEDIUM 0 |
| wiki Markdown / content / active | 138 / 129 / 126 |
| active index exact coverage | 0/126 |
| stable page·series·collection·relation fields | 0/129 |
| duplicate basenames | 6 groups, 31 files |
| cs-study required CI·pre-commit | 0 |

현재 테스트 성공은 구현된 검사 차원만 증명한다. orphan과 logic은 `scripts/lint.py`에 TODO이며 template section/order·evergreen restriction·raw enum은 false-negative가 확인됐다.

설계 시작 당시 Critical/High 기준선:

1. raw `--force` 기존 pair 교체 중 JSON rename 실패 경로는 새 Markdown을 삭제하고 이전 JSON만 남겨 FR-8과 원본 불변을 위반한다.
2. extractor `DocHook`은 cs-study push 연결을 의도하는 불필요한 reverse seam이다.
3. extractor/consumer contract version이 코드 문자열 두 곳에 독립적으로 존재한다.
4. field·section·template 규칙이 다중 SoT이며 6 templates 중 5개가 required field와 drift했다.
5. index·overview·log가 실제 vault와 동기화되지 않는다.
6. 당시 2차 wiki ingest executable과 integration test는 존재하지 않았다.
7. structure rules의 top-level 5종 “예외 없음”과 실제 raw/wiki/schema layer가 충돌한다.

## 3. 요구 명제 커버리지

| 구분 | 선언 | architecture mapping | logic/validation mapping | 판정 |
|---|---:|---:|---:|---|
| FR-KP | 22 | 22 | 22 | ✅ 설계 mapping 존재 |
| NFR-KP | 15 | 15 | 15 | ✅ 설계 mapping 존재 |
| AC-KP | 14 | 14 | 14 | ✅ 구현 순서·관찰 증거 mapping 존재 |
| executable implementation | 37 | 0 | 0 | ❌ 당시 구현 전 GAP |

`docs/wiki-ingest-architecture.md` §14가 각 requirement ID의 architecture와 logic surface를 소유한다. `_meta/knowledge-requirements.json`은 구현·검증 파일 mapping만 소유하며, validator는 두 surface의 ID 집합과 분리된 열을 대조해 누락·중복을 거부한다.

## 4. 의존성·복잡성·관리 지점 판정

| 항목 | 2026-08-22 당시 | 목표 설계 | 당시 판정 |
|---|---|---|---|
| runtime import cycle | 0 | 0 | ✅ 현행 cycle 없음 |
| reverse extension edge | extractor hook 2 edges | 0 | ❌ 제거 구현 필요 |
| schema rule owner | 4개 이상 surface | 1 machine schema | ❌ migration 필요 |
| collection membership owner | 없음 | CollectionPage 1 | ⚠️ 설계됨, 미구현 |
| backlink/inverse owner | external index 선언 | 계산 | ❌ legacy 선언 제거 필요 |
| generated navigation | 수동/LLM 혼합 | materializer 단독 | ❌ 미구현 |
| raw revision | video ID overwrite | content digest append-only | ❌ migration 필요 |
| canonical apply width | 명시 계약 없음 | page 1 | ⚠️ 설계됨, 미구현 |
| target dependency graph | 미구현 | 8 modules, 11 edges, cycles 0, max chain 2 | ⚠️ 당시 설계 모델; 현재 10-module·14-edge 계약으로 superseded |

관리 지점은 파일 개수가 아니라 사람이 독립적으로 동일 사실을 수정해야 하는 canonical owner 수로 계산한다. generated index·template·Bases는 파일이지만 수동 관리 지점이 아니다.

## 5. 정적 검증 결과

| 검증 | 결과 | 설명 |
|---|---|---|
| 문서 section cardinality | ✅ PRD 10·architecture 15·logic 10·review 10 | `^## ` 전수 계수 |
| requirement·acceptance ID uniqueness | ✅ 51/51 unique | 정의 구간 FR 22·NFR 15·AC 14, architecture missing 0 |
| rule ID uniqueness | ✅ BR 62·VR 22 unique | 정의 구간 중복 0 |
| logic finding reconcile | ✅ 최종 문서 검증 0 | 전체 4문서를 section-complete 5개 파티션으로 전수 검사: 5/5 findings 0, abstain 0. 수정 finding별 단건 재검증도 0 |
| grounding finding reconcile | ✅ 최종 review 검증 0 | citations 7/7 checked, abstain false, errors 0 |
| requirement coverage | ✅ 설계 ID mapping 51/51 | 로컬 ID diff missing·extra·duplicate 각 0; checker 2/2 findings 0, requirements 51, surfaces 16; 당시 구현 manifest·tests는 GAP |
| architecture cycle | ✅ 설계 cycle 0 | command sibling import 금지와 leaf dependencies만 허용 |
| module dependency depth | ✅ 당시 설계 dependency edge chain 2 | historical baseline이며 현재 목표 core+contract 10 modules·14 edges·최대 edge 3과 전환 command-inclusive 12 modules·18 edges·최대 edge 4 ratchet으로 superseded |
| 자기 코드 호출 깊이 | ✅ 함수 5개 미만 직렬(= 호출 edge 4 미만) 기준 | 당시 구현 call graph는 GAP |
| last-leaf scenarios | ✅ 설계 충족 | 전역 schema migration은 명시적 예외 |
| idempotence definition | ✅ input digest+schema digest+generator version+normalized command options tuple | 당시 file-exists skip은 FAIL |
| raw atomicity | ✅ directory rename 설계 | 당시 pair overwrite는 FAIL |
| page atomicity | ✅ one-page replace/rename 설계 | 구현 GAP |
| semantic completeness | 정적 보장 불가 | evidence coverage와 사람 review로 분리 |

requirements checker의 `surfaces`는 requirement ID cardinality가 아니라 에이전트가 인식한 downstream 인용 record 수다. 최종 두 반복은 모두 16이었지만 coverage 분모나 완료 판정에는 사용하지 않는다.

정적 검증은 “주장이 현실에서 참인가” 또는 “입력에서 중요한 의미가 하나도 누락되지 않았는가”를 증명하지 않는다. 이 범위를 구조 PASS에 포함하지 않는다.

## 6. 외부 기준 교차 검증

| 기준 | 채택 | 설계 반영 |
|---|---|---|
| [Obsidian Properties](https://obsidian.md/help/properties) | ✅ | flat YAML만 사용하고 복합 claim/relation은 본문 table로 둔다 |
| [Obsidian Templates](https://obsidian.md/help/Plugins/Templates) | ⚠️ | schema-derived authoring 편의로만 사용한다 |
| [Obsidian Bases](https://obsidian.md/help/bases) | ✅ | Markdown을 canonical로 유지하는 generated view다 |
| [Obsidian Internal links](https://obsidian.md/help/links)·[Backlinks](https://obsidian.md/help/backlinks) | ✅ | outgoing link만 저장하고 backlink는 계산한다 |
| [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12) | ✅ | parsed DocumentInstance의 표준 assertion owner다 |
| [JSON Schema Core](https://json-schema.org/draft/2020-12/draft-bhutton-json-schema-01) | ✅ | 미인식 `x-*`를 assertion으로 간주하지 않는다 |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | ⚠️ | Entity/Activity/used/derived-from 의미만 manifest에 매핑한다 |
| [W3C SKOS](https://www.w3.org/TR/skos-reference/) | ⚠️ | direct broader, related, ordered collection 의미만 차용한다 |
| [W3C SHACL](https://www.w3.org/TR/2017/REC-shacl-20170720/) | ❌ | RDF graph가 canonical이 아니므로 이중 validator stack을 만들지 않는다 |
| [Git diff](https://git-scm.com/docs/git-diff)·[GitHub status checks](https://docs.github.com/en/pull-requests/reference/status-checks) | ✅ | regeneration diff와 required CI를 권위 gate로 사용한다 |
| [OCI content descriptor](https://github.com/opencontainers/image-spec/blob/main/descriptor.md?plain=1) | ⚠️ | digest·size·media type 최소 descriptor만 차용한다 |

공식 기준은 현재 최소 설계를 지지한다. 전체 PROV/SKOS/RDF 모델이나 OCI registry를 도입하는 것은 요구 범위를 넘어 관리 surface를 증가시키므로 기각했다.

## 7. 현재 5계층 검증 상태

| 계층 | 현재 결과 | 판정 |
|---|---|---|
| 1 명제 일관성 | FR/NFR/AC 51개 mapping과 10-module·14-edge 목표 core+contract DAG | ✅ 전환 command-inclusive 12 modules·18 edges·cycle 0·최대 dependency edge 4 ratchet |
| 2 정적 분석 | live target lint HIGH 0·canonical findings 0; text report exclusions 9개; affected migration/check/test Ruff E/F 0; AST guard가 목표 수치와 현재 비전환 edge coverage 검증 | ✅ base/target validator 소유권과 목표 DAG edge contract 정합 |
| 3 단위 | current live target 156 passed·legacy-base 전용 11 skipped. P2-T2·P2-T3 단계 증거는 각각 154·155 passed였고, 최종 1개 증가는 preservation resolved-plan privacy digest 회귀다 | ✅ canonical target lifecycle과 privacy·runtime guard 결함 재현·회귀 테스트 통과 |
| 4 mock 통합 | live target의 156 passed에 capture·asset·schema·graph·check·migration fixture 통합 시나리오 포함 | ⚠️ 순서 7–8 command와 materializer는 미구현 |
| 5 실환경 | 승인된 결합 plan을 `.knowledge-migration-6b-reapply.json`으로 재적용해 `COMMITTED`, live wiki target hash, 당시 external 15/15 target, active stale 0을 확인했다. 후속 승인된 architecture evidence 수정 뒤 historical cascade vector는 비문서 14/14 exact이고 architecture 1개만 새 digest `7377a1e2…c00f5`다. canonical check findings 0, lint HIGH 0, generator current이며 동일 plan 재적용은 write 0으로 거부됐다 | ⚠️ 자동화 가능한 local target 전환 검증은 모두 수행; Chrome DOM 계약은 자동 focus 권한 부재로 사용자 확인 영역 |

이번 문서 정합 범위에서 자동화 가능한 로컬 정적·단위·mock 통합·실데이터 no-write 영역은 모두 시도했다. Obsidian Bases rendering은 materializer 미구현으로 자동화 조건을 충족하지 않고, 원격 branch protection은 접근권 미확인이다. 전체 pipeline 검증 완료나 release 가능 판정으로 확대하지 않는다.

## 8. 잔여 위험과 구현 게이트

남은 spec drift와 미구현 surface는 다음 결정·구현 순서가 소유한다.

| Drift family | 구현 소유 순서 |
|---|---:|
| SemanticPlan·synthesize·promote·collection·move command | 7 |
| generated marker·navigation·template | 8 |
| structure-rule scope/depth·wiki path·log·backlink·provenance legacy surface | 9 |
| 독립 CI·required check | 10 |
| 두 영상 재처리·full vault review | 11, 12 |

| 위험 | 상태 | 차단 게이트 |
|---|---|---|
| current dirty branches와 migration 충돌 | HIGH | 기준 commit·전용 worktree 사용자 승인 |
| post-apply validator·test lifecycle cutover | 해소 | terminal journal-bound candidate exclusion, unbound/nonterminal/digest-mismatch inclusion, target-state test lifecycle, exact-base legacy lint→canonical checker 단독 위임과 text exclusions 보고를 live target에서 재검증함 |
| canonical basename collision | 확인 | 75-page universe에서 collision group 0 |
| generated/template reserved ID conflict | 해소 | `index` 1건은 승인 A에 따라 collection page ID `info-sec-engineer-practical-past-exams`로 이동했고 external reference cascade와 함께 적용됨 |
| 75개 canonical page schema migration | 해소 | 75/75 resolution·exact-tree backup·full diff 승인 후 결합 transaction으로 적용하고 live target을 재검증함 |
| JSON Schema validator dialect 지원 | 확인 | 2020-12·format contract tests 통과 |
| YAML date normalization | 확인 | parser fixture·mutation tests 통과 |
| source digest 대상 bytes | 결정 | 기본은 exact bytes, clipping Markdown preservation은 privacy-normalized exact bytes로 고정 |
| logical collection ordering | 사용자 의미 판단 | provider order와 별도 review |
| claim 사실성·누락 | 자동 증명 불가 | claim-level grounding review |
| remote required check | 미확인 | GitHub branch setting 확인 |

남은 단계별 진입 gate:

- 순서 7: 6b live target과 설계된 leaf write-set·stale base digest 계약을 기준으로 구현 범위를 고정한다
- 순서 9 apply: no-write removal plan과 derived parity plan의 사용자 승인 전 migration apply 금지

## 9. 최종 판정

2026-08-25 기준 구현 순서 1–5, 6a no-write inventory와 6b fail-closed 결합 migration engine은 구현됐다. `check.py → fs.py`, neutral canonical timestamp leaf, clipping privacy leaf를 포함하는 목표 core+contract DAG는 10 modules·14 edges·cycle 0·최대 dependency edge 3이며, 전환 command-inclusive DAG는 12 modules·18 edges·cycle 0·최대 dependency edge 4 ratchet으로 AST guard에 연결됐다. post-apply validation lifecycle을 보완한 뒤 승인된 결합 plan을 재적용했으며 `.knowledge-migration-6b-reapply.json`은 `COMMITTED`, live wiki와 external reference는 모두 target 상태다. 순서 7–12는 실행되지 않았다.

- 설계 문서 gate: 승인된 목표 DAG와 AST regression guard 정합
- 현재 범위 판정: 순서 1–6b engine과 승인된 canonical cutover를 정적·단위·mock 통합·실데이터 apply·refusal로 검증
- 전체 시스템 판정: 6b canonical cutover는 완료됐지만 순서 7–12 GAP 때문에 PASS 선언 불가
- 다음 진입 gate: 순서 7 SemanticPlan·synthesize·promote·collection·move leaf command 설계 범위 확인

75-page preservation resolution은 source/target 75/75, 이동 8, collection 1, `Members` 52 unique, unresolved 0으로 고정됐다. `Members` 순서는 legacy index의 Markdown link 52개와 exact-order로 대조했다. 활성 clipping manifest/payload는 75/75이며 P2-T2에서 개인 홈 prefix가 있던 8개 revision을 append-only로 추가하고 active manifest reference 16개와 resolution digest 8개를 새 digest로 전환했다. 당시 no-apply preview는 structural PASS, payload parity 75/75, Claims 0, Relations 0, Members 52를 확인했고 project question-pack의 전체 sourceRef 410/410이 target preview의 동일 line·excerpt를 가리켰다. 외부 참조 관찰값 676회는 active question-pack 329회, generated `practice-data.js` 329회, project docs 5회, `.claude/resume_prompt.md` 11회, architecture 1회와 append-only `log.md`의 historical 1회로 분해된다. historical 기록은 수정하지 않는다. 이전 actual apply에 사용한 cascade plan SHA-256은 `1004572e3966031923f0b1f168b15a7f1140e8b8de0c54622d75df4548105d28`였다. lifecycle remediation 후 승인·적용한 resolved plan은 `ef15632778e1490c281dd63224939ac20f56b1e99689e1ba694f00764dd0299c`, cascade plan은 `b0a8e366fb76fce6b7a3dddb3f5c266a9b3eece779df36ec2b728bd5e80f11b0`, full diff는 `636255b5ac3988c1c8ff0354844cd6376337055ce3641ced3a9b99c11336495a`, backup은 `3553e4ed6ef96a9069d46103e73f3e5335018f10862a6e78562e74540133d885`이며 두 번의 생성 결과가 byte-identical이었다. 당시 journal target wiki tree는 `23c8e82e54af6f6f5331435df64dcc0357601577e1f8282f45243eafec9e0d4a`였고, P2-T2 privacy 이행 뒤 현재 live wiki tree는 `ef5d0c42f08d1a5841a78633cb3e92adabc322e85eff8aeb5b87cf41bf0c6b21`이다. apply 시점의 external target 15/15 중 비문서 14개는 그대로이며, architecture는 승인된 후속 evidence 수정으로 SHA-256 `7377a1e206d0b405e1a0904be2bbf07dbcb5b551251fa23bae9c7ee9744c00f5`가 됐다. apply·restore·reapply journal과 journal-bound 세 candidate는 historical execution·recovery evidence로 보존한다.

## 10. 변경 이력

- 2026-08-21: 전수 baseline, 공식 기준, 5계층 상태, 구현 차단 게이트를 포함하는 검증 문서로 `archives/design/docs/wiki-ingest-review-v1.md`를 대체했다.
- 2026-08-21: logic·grounding·requirements finding을 순차 reconcile하고 현행 spec drift를 구현 순서 2–10에 귀속했다.
- 2026-08-22: 규칙 수명·심각도·provenance·recency 경계를 수정하고, logic 전수 파티션·requirements 2회·두 저장소 테스트·실 network 검증 결과를 반영했다.
- 2026-08-23: 구현 순서 1–6a 증거, 114 content migration inventory, 6b 별도 승인 gate를 반영했다.
- 2026-08-24: 사용자 승인 A의 75-page canonical universe, project boundary, 6b fail-closed engine과 94-test·실데이터 no-write 증거로 현재 상태를 갱신했다. 직전 114-page·31-collision 수치는 historical baseline으로만 보존한다.
- 2026-08-24: historical baseline과 현재 검증 상태를 분리하고, CLI·모듈 수명 및 목표 DAG 잔여 결정을 반영했다.
- 2026-08-24: `check.py → fs.py` 목표 edge를 승인 반영하고 8 modules·12 edges AST regression guard로 잔여 결정을 해소했다.
- 2026-08-25: timestamp validator를 neutral dependency-free leaf로 단일화하고 목표 core+contract 9 modules·13 edges·최대 edge 3, 전환 command-inclusive 11 modules·16 edges·cycle 0·최대 edge 4 ratchet exact guard로 갱신했다.
- 2026-08-24: 75-page preservation resolution·immutable clipping·결정적 preview·plan-bound backup과 123-test, full canonical check, project sourceRef 410/410 보존 증거를 반영했다.
- 2026-08-24: collection 52 exact-order, capture expected digest, plan·preview atomic no-replace, preservation preview·apply mandatory lineage audit와 전환 graph exact guard를 회귀 게이트로 승격했다.
- 2026-08-24: operation payload의 content-addressed manifest binding으로 preservation을 독립 판별해 `resolution_mode=generic` downgrade를 preview·backup·apply 전에 거부하는 적대적 회귀 게이트를 추가했다.
- 2026-08-25: clipping Markdown의 Apple·Windows local-user-home prefix를 digest 전에 단일 privacy leaf로 치환하고, 활성 wiki·manifest payload·web source의 개인 경로 정적 거부와 8개 revision·16개 active manifest reference·8개 resolution digest 이행을 반영했다. 이전 immutable revision은 recovery evidence로 유지한다.
- 2026-08-25: lifecycle remediation 후 승인된 결합 plan을 재적용하고 live target hash, external target 15/15, active stale 0, canonical findings 0, 전체 target 테스트와 멱등 refusal 결과를 반영했다.
- 2026-08-25: 후속 교차검증의 prefix-only candidate exclusion, checker text exclusions 누락, architecture live-state drift를 TDD로 보강하고 historical cascade vector와 후속 architecture digest를 분리 기록했다.
