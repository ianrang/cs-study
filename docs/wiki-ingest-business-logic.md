# Business Logic: raw video -> LLM wiki synthesis (2차)

> 대상: `docs/wiki-ingest-prd.md`, `docs/wiki-ingest-architecture.md`.
> 본 문서는 2차 raw video -> wiki source summary 합성의 규칙과 검증을 명제화한다.

## 1. 도메인 개념

### 용어 사전

| 용어 | 정의 |
|---|---|
| RawVideo | `raw/sources/video/<video_id>.md` 에 저장된 원문 보존 페이지 |
| SourceSummary | raw source 1개를 wiki 에서 요약한 page |
| DomainDecision | source 를 어느 wiki domain 에 둘지에 대한 결정 |
| DomainRegistry | `_meta/domains.yaml` 에 저장된 domain 단일 진실 |
| Staging | confidence 가 낮거나 review 가 필요한 source 를 임시 보관하는 영역 |
| Claim | source 에서 추출한 주장 |
| VerificationStatus | claim 을 지식으로 받아들일 수 있는 정도 |
| VerificationRollup | claim table 에서 계산한 page-level 검증 상태 |
| Candidate | concept/entity page 생성 또는 갱신 후보 |
| SourceSummaryUniqueness | 동일 video_id source summary 전역 유일성 |

### 엔티티

| 엔티티 | 설명 | 식별자 |
|---|---|---|
| RawVideo | 2차 입력 | raw path, video_id |
| SourceSummary | wiki source page | source_summary_path |
| CandidateReport | 후보 검토 문서 | raw video_id |
| DomainRegistry | domain 목록 | `_meta/domains.yaml` |

### 값 객체

| VO | 속성 | 설명 |
|---|---|---|
| DomainDecision | domain, confidence, rationale | 분류 결과 |
| Claim | text, status, evidence, notes | 보수적 주장 단위 |
| VerificationRollup | verification_status, claim_status_counts | claim table 에서 파생된 page-level 요약 |
| ClaimTable | id, primary, claim, status, evidence, notes | 검증 상태 SoT |
| Candidate | kind, slug, label, status, matched_path, reason | 중복/신규 후보 |
| SemanticWritePlan | raw_path, video_id, domain_decision, source_summary, claims, candidates | LLM/사람이 제공하는 semantic JSON. 파일 write 계획이 아님 |
| CommandOptions | apply, force, now, write_plan, domain, format | leaf command 입력/실행 모드 |

### 도메인 이벤트

| 이벤트 | 트리거 | 설명 |
|---|---|---|
| WikiIngestPlanned | raw 입력 검증 후 | 파일 변경 없이 plan 생성 |
| WritePlanValidated | `--write-plan` 입력 검증 후 | 외부 semantic plan 이 `_meta/wiki-ingest-write-plan.schema.json` 과 현재 raw/wiki/schema 상태에 정합 |
| SourceSummaryCommitted | source summary apply 성공 | wiki source page 생성 |
| SourceSummarySkipped | target 존재 + not force | 멱등 skip |
| DomainReviewQueued | confidence low | staging 에 review 대상 생성 |
| WikiIngestRejected | 입력/링크/lint 검증 실패 | 파일 write 금지 |

## 2. 비즈니스 규칙

### 입력

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-IN-1 | IF 입력 path 가 raw/sources/video 하위 markdown 이면 THEN RawVideo 후보로 읽는다 | UNLESS frontmatter 없음 THEN reject | FR-1, FR-2 |
| BR-IN-2 | IF 입력 path 가 디렉토리이면 THEN reject | - | FR-1 |
| BR-IN-3 | IF raw 필수 필드가 누락되면 THEN reject | - | FR-2 |
| BR-IN-4 | IF raw body 가 비어 있거나 claim 을 1개 이상 만들 수 없으면 THEN wiki ingest 를 reject 한다 | raw 는 그대로 보존 | SemanticWritePlan schema |

### 분류

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-DOM-1 | IF domain_confidence in {high, medium} AND domain.status = active in `_meta/domains.yaml` THEN target = wiki/domains/<domain>/sources/<video_id>.md | - | FR-3 |
| BR-DOM-2 | IF domain_confidence = low THEN target = wiki/staging/domain-review/<video_id>.md | - | FR-3 |
| BR-DOM-3 | IF domain 이 `_meta/domains.yaml` 에 없으면 THEN confidence 는 low 로 강등한다 | UNLESS 사용자가 같은 작업에서 domain registry 수정을 승인 | D-1, D-2 |
| BR-DOM-4 | IF 복수 domain 후보가 동률이면 THEN staging 으로 보낸다 | - | D-2 |
| BR-DOM-5 | IF domain.status != active THEN target domain 으로 사용하지 않는다 | - | D-9 |
| BR-DOM-6 | IF 새 domain 이 필요하면 THEN `_meta/domains.yaml` 후보 변경으로만 제안한다 | - | D-9 |
| BR-DOM-7 | IF `--domain` override 가 주어지면 THEN domain 은 `_meta/domains.yaml` 에 존재하고 active 여야 한다 | UNLESS missing/inactive THEN reject | D-16 |
| BR-DOM-8 | IF classifier decision domain 이 missing/inactive 이면 THEN staging 으로 보낸다 | - | D-16 |

### Claim 검증

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-CLM-1 | IF claim 이 raw video 에만 근거하면 THEN status = claimed | - | D-3, D-4 |
| BR-CLM-2 | IF claim 이 다른 raw/human note 에서도 반복되면 THEN status = corroborated | UNLESS source 간 의미가 다르면 ambiguous note 로 남김 | D-4 |
| BR-CLM-3 | IF claim 이 공식 문서/원문 논문/신뢰 가능한 repo 로 확인되고 해당 근거가 `raw/sources/{papers,web,urls}/`에 보존되면 THEN status = verified | - | D-4 |
| BR-CLM-4 | IF claim 이 검증 중 반례로 틀렸음이 확인되면 THEN status = rejected | - | D-4 |
| BR-CLM-5 | IF status != verified THEN concept/entity page 에 확정 사실 문장으로 반영하지 않는다 | - | D-3 |
| BR-CLM-6 | IF claim 이 영상 하나만 근거로 가진다면 THEN status 는 verified 가 될 수 없다 | - | D-4 |
| BR-CLM-7 | IF status = verified THEN evidence 는 검토·보존된 `raw/sources/{papers,web,urls}/...md` 경로여야 한다 | 외부 URL은 raw source로 먼저 ingest | D-4 |

### 검증 roll-up

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-ROLL-1 | IF claim table 이 존재하면 THEN claim table 이 검증 상태 SoT 이다 | - | D-4 |
| BR-ROLL-2 | IF claim table 이 존재하면 THEN frontmatter `verification_status` 가 존재하고 claim table 에서 계산된 roll-up 과 같아야 한다 | - | D-4 |
| BR-ROLL-3 | IF claim table 이 존재하면 THEN frontmatter `claim_status_counts` 가 존재하고 claim table count 와 같아야 한다 | - | D-4 |
| BR-ROLL-4 | IF 핵심 claim 전체가 verified AND 전체 claim row의 rejected count = 0 THEN page verification_status = verified | - | D-4 |
| BR-ROLL-5 | IF 핵심 claim 전체가 at least corroborated AND 전체 claim row의 rejected count = 0 THEN page verification_status = corroborated | UNLESS BR-ROLL-4 applies | D-4 |
| BR-ROLL-6 | IF 핵심 claim 전체가 rejected THEN page verification_status = rejected | - | D-4 |
| BR-ROLL-7 | IF BR-ROLL-4/5/6 이 적용되지 않으면 THEN page verification_status = claimed | - | D-4 |
| BR-ROLL-8 | IF `## Claims` table 이 없거나 columns 가 `id/primary/claim/status/evidence/notes` 와 다르면 THEN reject | - | D-12 |
| BR-ROLL-9 | IF `primary` 가 `true` 또는 `false` 가 아니면 THEN reject | - | D-12 |
| BR-ROLL-10 | IF claim id 가 문서 내 중복이면 THEN reject | - | D-12 |
| BR-ROLL-11 | IF claim table cell 에 literal pipe 가 필요하면 THEN `\|` 로 escape 한다 | - | D-12 |
| BR-ROLL-12 | IF claim table cell 에 newline 이 있으면 THEN reject 한다 | - | D-12 |
| BR-ROLL-13 | IF header row 이후 delimiter row 가 없거나 delimiter 형식이 아니면 THEN reject 한다 | - | D-12 |
| BR-ROLL-14 | IF `primary=true` claim 이 하나도 없으면 THEN page verification_status = claimed | - | D-4 |

### 후보와 중복

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-CAN-1 | IF extracted concept/entity slug 가 기존 wiki page 와 일치하면 THEN candidate.status = existing | - | FR-7, FR-8 |
| BR-CAN-2 | IF slug 가 taxonomy alias 와 일치하면 THEN canonical slug 로 매핑하고 duplicate 로 표시한다 | - | FR-8 |
| BR-CAN-3 | IF 기존 page 가 없으면 THEN candidate.status = review-needed 로 둔다 | - | FR-7 |
| BR-CAN-4 | IF candidate.status != existing THEN source summary 본문에 wikilink 를 만들지 않는다 | - | FR-9 |
| BR-CAN-5 | IF 새 concept/entity 생성이 필요하면 THEN 별도 review/PR 대상으로 분리한다 | - | NFR-7 |

### 링크

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-LNK-1 | IF wiki 본문에 wikilink 가 있으면 THEN target file 이 존재해야 한다 | UNLESS validator 가 같은 apply operation 에서 생성한다고 재계산함 | FR-9 |
| BR-LNK-2 | IF target 이 디렉토리이면 THEN overview.md 또는 index.md 로 명시해야 한다 | - | FR-9 |
| BR-LNK-3 | IF link 가 placeholder 이면 THEN reject | - | FR-10 |
| BR-LNK-4 | IF link target 에 Obsidian invalid character 가 있으면 THEN reject | - | Obsidian link policy |

### 멱등과 생명주기

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-IDEM-1 | IF target source summary exists AND not force THEN SourceSummarySkipped | - | NFR-2 |
| BR-IDEM-2 | IF force THEN same target path 를 덮어쓴다 | - | NFR-2 |
| BR-IDEM-3 | IF low confidence source 가 나중에 승격되어도 THEN staging 파일 자동 삭제는 하지 않는다 | UNLESS 별도 review command 가 승인됨 | review gate |
| BR-IDEM-4 | IF apply 가 실패하면 THEN 부분 산출물을 남기지 않는다 | - | 정합성 |
| BR-IDEM-5 | IF MVP command runs THEN `wiki/index.md` 와 `wiki/log.md` 를 갱신하지 않는다 | - | FR-11, D-14 |
| BR-IDEM-6 | IF staging source 를 domains 로 승격해야 하면 THEN MVP command 가 아니라 별도 promote stage 에서 처리한다 | - | D-8 |
| BR-IDEM-7 | IF 동일 video_id source summary 가 staging/domains 전체에 이미 있으면 THEN 새 source summary 생성을 reject 또는 skip 한다 | same target 이면 skip 가능 | D-11 |
| BR-IDEM-8 | IF 동일 video_id 가 다른 active domain source 에 있으면 THEN reject 하고 existing path 를 출력한다 | - | D-11 |
| BR-IDEM-9 | IF `--force` 가 주어지면 THEN same target path 만 덮어쓴다 | 다른 domain/staging 중복은 여전히 reject | D-15 |

### LLM 호출

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-LLM-1 | IF LLM 을 사용하면 THEN profile alias `ingest` 를 사용한다 | - | FR-13 |
| BR-LLM-2 | IF LLM 출력이 `_meta/wiki-ingest-write-plan.schema.json` 을 만족하지 않으면 THEN reject | - | NFR-5 |
| BR-LLM-3 | IF LLM 이 verified status 를 부여하려면 THEN 검토·보존된 `raw/sources/{papers,web,urls}/...md` evidence가 있어야 한다 | 외부 URL 직접 사용 금지 | D-4 |
| BR-LLM-4 | IF LLM 이 새 taxonomy vocab 을 제안하면 THEN candidate report 에만 기록한다 | - | taxonomy review gate |
| BR-LLM-5 | IF MVP implementation runs THEN LLM execution mode = prompt-plan + validated SemanticWritePlan input | - | D-10, D-13 |
| BR-LLM-6 | IF LLM output proposes direct file writes THEN reject | - | 캡슐화 |
| BR-LLM-7 | IF `--write-plan` is provided THEN strict schema, semantic fields, target recomputation, claim rows, roll-up, links, lint must pass before apply | - | D-13 |
| BR-LLM-8 | IF `--write-plan` includes writes/skips/target paths/frontmatter/derived fields/rendered markdown THEN reject | - | D-13 |
| BR-LLM-9 | IF validator recomputes target path/frontmatter/markdown/write operation THEN it must ignore any external generated equivalent | - | D-13 |

### 옵션

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-OPT-1 | IF option is one of apply/force/now/write_plan/domain/format THEN it may affect only command input, output format, or apply mode | - | D-15 |
| BR-OPT-2 | IF option attempts to bypass claim status, roll-up, domain registry, uniqueness, link, lint, or raw immutability rules THEN reject | - | D-15 |
| BR-OPT-3 | IF `--format` changes THEN only plan/report representation changes | semantics unchanged | D-15 |

### Lint 정비

| ID | 명제 | 예외 | 출처 |
|---|---|---|---|
| BR-LINT-1 | IF path in wiki/templates THEN 일반 wiki required fields/link 검사에서 제외하고 template 규칙을 적용한다 | - | FR-10 |
| BR-LINT-2 | IF path in {wiki/index.md, wiki/log.md, wiki/overview.md} THEN content frontmatter 검사는 제외하되 내부 link는 검증한다 | - | FR-10 |
| BR-LINT-3 | IF generated source summary has missing wiki required field THEN reject | - | FR-4 |
| BR-LINT-4 | IF generated page has HIGH lint finding THEN reject | - | NFR-5 |

## 3. 상태 전이

### WikiIngest

| 시작 | 종료 | 트리거 | 규칙 |
|---|---|---|---|
| Input | Rejected | raw path invalid/frontmatter invalid | BR-IN-1..3 |
| Input | Parsed | raw valid | BR-IN-* |
| Parsed | Classified | domain decision produced | BR-DOM-* |
| Classified | Rejected | invalid `--domain` override | BR-DOM-7 |
| Classified | PlannedDomain | confidence high/medium | BR-DOM-1 |
| Classified | PlannedStaging | confidence low | BR-DOM-2 |
| Planned* | Rejected | invalid `--write-plan` | BR-LLM-7..9 |
| PlannedDomain | Skipped | target exists and not force | BR-IDEM-1 |
| PlannedStaging | Skipped | target exists and not force | BR-IDEM-1 |
| PlannedDomain | Committed | apply + lint pass | BR-LINT-3..4 |
| PlannedStaging | Queued | apply + lint pass | BR-DOM-2 |
| Planned* | Rejected | broken link/lint/schema failure | BR-LNK-*, BR-LINT-* |

종료 상태:
- Rejected
- Skipped
- Committed
- Queued
- Planned only

데드 상태 없음. `Queued` 는 사람 review 로만 `Committed` 승격 가능하다.

## 4. 검증 규칙

| ID | 대상 | 조건 | 실패 시 |
|---|---|---|---|
| VR-1 | raw path | file exists and suffix .md | reject |
| VR-2 | raw path | under raw/sources/video | reject |
| VR-3 | raw frontmatter | raw required fields present | reject |
| VR-4 | domain_confidence | high/medium/low | reject |
| VR-5 | verification status | claimed/corroborated/verified/rejected | reject |
| VR-6 | source summary frontmatter | wiki required fields + source summary fields | reject |
| VR-7 | wikilinks | targets exist or same plan creates them | reject |
| VR-8 | candidate slugs | kebab-case and no path separator | reject |
| VR-9 | write plan | no write outside wiki/ | reject |
| VR-10 | generated files | lint HIGH=0 | reject |
| VR-11 | domain registry | `_meta/domains.yaml` exists, registry schema가 유효하고 domain target으로 선택된 domain이 active | reject |
| VR-12 | verification roll-up | frontmatter roll-up equals claim table derived state/counts | reject |
| VR-13 | source summary uniqueness | same video_id appears at most once across domains/staging | reject |
| VR-14 | claim table schema | fixed columns, delimiter row, escaped pipes, no multiline cells, valid field values | reject |
| VR-15 | semantic write-plan input | strict schema/semantic fields/path/target/claim/link/lint checks pass | reject |
| VR-16 | command options | no option bypasses business rules | reject |
| VR-17 | domain override | override domain exists and status=active | reject |
| VR-18 | index/log | MVP write plan contains no `wiki/index.md` or `wiki/log.md` writes | reject |

## 5. 일관성 검증 결과

### 규칙 간 충돌

| 규칙 A | 규칙 B | 충돌 유형 | 해결 |
|---|---|---|---|
| BR-DOM-1 | BR-DOM-2 | target 분기 | confidence enum 으로 배타적 |
| BR-CLM-1 | BR-CLM-3 | claimed vs verified | evidence 수준에 따라 verified 가 더 강한 상태 |
| BR-CLM-3 | BR-CLM-6 | verified 기준 | 영상 하나만 근거면 verified 불가. 권위 evidence 필요 |
| BR-ROLL-1 | frontmatter verification_status | 중복 가능성 | claim table 이 SoT, frontmatter 는 derived 로만 허용 |
| BR-CAN-3 | BR-CAN-4 | 새 후보와 link 생성 | 새 후보는 plain text/candidate table 로만 기록 |
| BR-IDEM-3 | source 승격 | staging 보존 vs domain 생성 | 별도 review command 로 생명주기 분리 |
| BR-IDEM-7 | BR-IDEM-2 | 중복과 force | force 는 same target 에만 적용. 다른 domain 중복은 reject |
| BR-LINT-1 | BR-LINT-3 | template 예외 vs generated page 검증 | path scope 분리 |
| BR-LLM-5 | BR-LLM-6 | LLM plan 사용 vs LLM write 금지 | plan 은 검증 대상 입력일 뿐이며 write 는 Python validator 만 수행 |
| BR-DOM-7 | BR-DOM-8 | domain override reject vs classifier staging | 수동 override 는 active 만 허용, 자동 classifier missing/inactive 는 staging 으로 분리 |
| BR-IDEM-5 | AGENTS 일반 ingest index/log | MVP source-summary stage vs 최종 wiki ingest lifecycle | index/log 는 promote/index stage 로 이연 |

충돌 없음.

### 완전성

| 검증 항목 | 상태 | 비고 |
|---|---|---|
| 입력 분기 | PASS | file/dir/missing/frontmatter invalid |
| domain 분기 | PASS | high/medium/low |
| claim 상태 | PASS | claimed/corroborated/verified/rejected |
| claim roll-up | PASS | claim table SoT + derived frontmatter |
| claim table schema | PASS | 고정 columns + validator 검증 |
| 중복 처리 | PASS | existing/duplicate/review-needed |
| source summary 전역 유일성 | PASS | same video_id one summary across staging/domains |
| link 처리 | PASS | existing/same-plan/invalid |
| 생명주기 | PASS | planned/skipped/committed/queued/rejected |
| 옵션 경계 | PASS | options do not bypass business rules |
| write-plan 경계 | PASS | external plan is validated input, not trusted state |
| index/log 분리 | PASS | MVP write plan rejects index/log writes |

### 교차 검증

| 항목 | 상태 | 근거 |
|---|---|---|
| 1차 pipeline 정합성 | PASS | 2차는 raw 산출물을 읽기만 하므로 1차 멱등/트랜잭션 계약을 변경하지 않음 |
| Obsidian link 정합성 | PASS | 존재 파일 또는 same-plan file 만 wikilink 허용 |
| LLM Wiki 원칙 | PASS | raw/wiki/schema 분리 + ingest/lint gate 유지 |
| domain 확장성 | PASS | `_meta/domains.yaml` 단일 수정 지점, code hardcode 금지 |
| 복잡성 억제 | PASS | 자동 concept/entity rewrite, pipeline 자동 연결, taxonomy 자동 확장, staging promote 자동화 제외 |
