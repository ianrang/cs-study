# Architecture: raw video -> LLM wiki synthesis (2차)

> 대상 PRD: `docs/wiki-ingest-prd.md`.
> 본 설계는 1차 결정적 importer 뒤에 붙는 독립 2차 stage 만 정의한다.

## 1. 기술 스택

| 분류 | 기술 | 근거 |
|---|---|---|
| 언어 | Python | 기존 `scripts/*.py` 와 테스트 구조 정합 |
| frontmatter 파싱 | PyYAML | `scripts/lint.py`, `scripts/ingest.py` 와 동일 |
| CLI | argparse | 기존 `scripts/lint.py`, `scripts/pipeline.py` 패턴 |
| 파일 처리 | pathlib | 기존 scripts 정합 |
| LLM | CLI 세션 / profile alias | `_meta/llm-config.yaml` 의 `ingest` profile 사용. API 직접 호출 금지 |

## 2. 레이어 구조

```text
CLI
  -> orchestrator
      -> parser/raw reader
      -> classifier
      -> planner/renderer (prompt/write-plan boundary 포함)
      -> validator
      -> commit
```

의존 방향:

```text
scripts/wiki_ingest.py
  reads -> raw/sources/video/<id>.md
  reads -> wiki/, _meta/domains.yaml, _meta/taxonomy.md, _meta/frontmatter-spec.md
  writes -> wiki/domains/<domain>/sources/<id>.md
         -> wiki/staging/domain-review/<id>.md
         -> wiki/staging/domain-review/<id>-candidates.md
```

금지 방향:

```text
scripts/wiki_ingest.py -> scripts/pipeline.py import 금지
scripts/wiki_ingest.py -> scripts/ingest.py import 금지
scripts/wiki_ingest.py -> raw 수정 금지
scripts/pipeline.py -> scripts/wiki_ingest.py 자동 호출 금지
```

이 분리는 생명주기를 단순하게 유지한다. 1차는 "원문 적재", 2차는 "지식 합성"이다.

## 3. 디자인 패턴

| 패턴 | 적용 위치 | 선택 이유 | 기각한 대안 |
|---|---|---|---|
| Anti-Corruption Boundary | raw reader | raw page 를 SourceInput 으로만 변환하고 raw 파일 자체는 수정하지 않음 | raw frontmatter 를 2차에서 보강: 원본 불변 위반 |
| Plan-then-Apply | planner/commit | dry-run 에서 생성/skip/staging 결정을 검토 가능 | 즉시 apply: review gate 와 멱등 판단이 불명확 |
| Idempotent Target Key | target path 계산 | source summary key 는 `video_id`; 같은 raw 는 같은 path | 날짜/제목 기반 파일명: rename drift, 중복 위험 |
| Candidate Report | concept/entity 후보 | MVP 에서 기존 지식 페이지 rewrite 를 막고 review 가능성 확보 | concept/entity 자동 생성: taxonomy drift, 중복 증가 |
| Link Resolver | validator | Obsidian link 가 실제 파일에 연결되는지 사전 검증 | lint 사후 실패만 의존: broken graph 누적 |
| Semantic WritePlan Boundary | prompt/write-plan boundary | LLM/사람 산출물을 파일 쓰기 계획이 아닌 semantic JSON 검증 대상 입력으로만 취급 | LLM 직접 write: 캡슐화·검증 경계 붕괴 |

## 4. 데이터 모델

### SourceInput

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `raw_path` | Path | raw/sources/video 하위 | 입력 raw markdown |
| `video_id` | str | 파일 stem | target key |
| `title` | str | non-empty | raw frontmatter title |
| `source_url` | str | required key, empty 허용 | YouTube URL |
| `source_date` | str | required key, empty 허용 | 영상 게시일 |
| `last_verified` | str | non-empty | raw 추출 확인일 |
| `body` | str | non-empty required | raw script body |

### DomainDecision

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `domain` | str | kebab-case | target domain |
| `confidence` | high/medium/low | required | low 는 staging |
| `rationale` | str | required | 분류 근거 |
| `source` | classifier/write_plan/override | required | 자동 분류, SemanticWritePlan, active domain override |

### DomainRegistry

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `version` | int | required | registry schema version |
| `domains` | dict | required | domain SoT |
| `status` | active/inactive | required | active 만 domain target 허용 |
| `source_roots` | list[str] | optional | 분류 힌트. write scope 허용 목록이 아님 |

### Claim

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `text` | str | required | 보수적 claim 문장 |
| `status` | claimed/corroborated/verified/rejected | required | 검증 상태 |
| `evidence` | str | required | raw path 또는 verified source |
| `notes` | str | required key, empty 허용 | 검증 필요/반례 |

Claim table 이 검증 상태의 SoT 이다. Source summary frontmatter 의 `verification_status` 와 `claim_status_counts` 는 claim table 에서 계산되는 파생값이다.

### SourceSummaryMeta

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `verification_status` | claimed/corroborated/verified/rejected | derived | claim table roll-up |
| `claim_status_counts` | dict | derived | claim table status counts |

### Candidate

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `kind` | concept/entity | required | MVP 후보 page type |
| `slug` | str | kebab-case | target 후보 |
| `label` | str | non-empty | 사람이 읽는 후보 이름 |
| `status` | existing/review-needed/duplicate | required | 처리 상태 |
| `matched_path` | Path \| null | required | 기존 페이지가 없으면 null |
| `reason` | str | required | 판단 근거 |

### SemanticWritePlan

SoT: `_meta/wiki-ingest-write-plan.schema.json`.

SemanticWritePlan 은 LLM/사람이 제공할 수 있는 구조화 입력이다. 파일 경로, frontmatter, rendered markdown, write operation 은 plan 에서 받지 않고 Python validator 가 재계산한다.

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `schema_version` | str | const `wiki-ingest-plan.v1` | schema version |
| `raw_path` | Path | required | 입력 raw source |
| `video_id` | str | required | source summary key |
| `domain_decision` | DomainDecision | required | target 분류 |
| `source_summary` | object | required | title, summary, main_claims |
| `claims` | list[ClaimRow] | min 1 | claim table 원천 |
| `candidates` | list[Candidate] | empty 허용 | candidate report 원천 |

금지 필드:
- `writes`, `skips`
- `source_summary_path`, `candidate_report_path`
- `frontmatter`
- `verification_status`, `claim_status_counts`
- rendered markdown body

예시:

```json
{
  "schema_version": "wiki-ingest-plan.v1",
  "raw_path": "raw/sources/video/abc123.md",
  "video_id": "abc123",
  "domain_decision": {
    "domain": "developer-tools",
    "confidence": "high",
    "rationale": "영상 주제가 CLI 기반 개발 도구 사용법이다.",
    "source": "write_plan"
  },
  "source_summary": {
    "title": "영상 제목 기반 source summary",
    "summary": "영상은 개발 도구 사용 흐름을 설명한다.",
    "main_claims": ["영상은 X라고 주장한다."]
  },
  "claims": [
    {
      "id": "C1",
      "primary": true,
      "claim": "영상은 X라고 주장한다.",
      "status": "claimed",
      "evidence": "raw/sources/video/abc123.md",
      "notes": "추가 검증 필요"
    }
  ],
  "candidates": [
    {
      "kind": "concept",
      "slug": "model-context-protocol",
      "label": "Model Context Protocol",
      "status": "existing",
      "matched_path": "wiki/domains/developer-tools/concepts/model-context-protocol.md",
      "reason": "기존 wiki page 와 slug 일치"
    }
  ]
}
```

SemanticWritePlan 은 신뢰 입력이 아니다. `--write-plan` 으로 들어온 JSON 은 Python validator 가 `_meta/wiki-ingest-write-plan.schema.json`, 현재 raw, domain registry, wiki filesystem, frontmatter spec, claim table rules 를 기준으로 다시 검증한다.

### ClaimTable

Claim table 은 source summary 본문 `## Claims` 아래의 고정 pipe table 이다. SemanticWritePlan 의 `claims[]` 는 이 table 을 렌더링하기 위한 원천 데이터이며, markdown table 자체는 Python renderer 가 생성한다.

| column | type | required | rule |
|---|---|---|---|
| `id` | str | yes | `C1`, `C2` 형식. 문서 내 unique |
| `primary` | bool | yes | `true \| false` |
| `claim` | str | yes | 보수적 주장 문장 |
| `status` | enum | yes | claimed/corroborated/verified/rejected |
| `evidence` | str | yes | raw path 또는 verified evidence |
| `notes` | str | yes, empty 허용 | 검증 필요/반례/보충 |

Parsing rules:
- `## Claims` 아래 header row 와 delimiter row 가 바로 온다. 중간 blank line 은 header 전까지만 허용한다.
- column 순서와 이름은 고정이며 누락·추가·순서 변경은 reject 한다.
- cell 안의 literal pipe 는 `\|` 로 escape 한다.
- cell 안의 newline 은 허용하지 않는다.
- `claim_status_counts` 는 전체 rows count, `verification_status` 는 `primary=true` rows roll-up 이다.
- `primary=true` row가 없으면 `verification_status` 는 `claimed` 이다.

설계 근거:
- Obsidian properties 는 small atomic metadata 에 적합하고 Markdown in properties 를 지원하지 않는다.
- Claim 상세는 사람이 읽고 validator 가 파싱해야 하므로 본문 table SoT 로 둔다.
- Frontmatter 의 `verification_status`, `claim_status_counts` 는 ClaimTable 에서 계산한다.

## 5. CLI 설계

```bash
scripts/wiki_ingest.py raw/sources/video/<id>.md [--apply] [--force] [--now YYYY-MM-DD] [--write-plan plan.json] [--domain <active-domain>] [--format text|json]
```

기본은 plan-only 이다.

| 옵션 | 의미 |
|---|---|
| 기본 | 변경하지 않고 write plan 만 출력 |
| `--apply` | 검증 통과 시 파일 생성 |
| `--force` | same target source summary 덮어쓰기. 다른 domain/staging 중복은 여전히 reject |
| `--now` | 테스트 결정성을 위한 date 주입 |
| `--write-plan` | 사람/외부 CLI 세션이 만든 SemanticWritePlan JSON 입력. 검증 통과 시에만 apply 가능 |
| `--domain` | active registry domain 으로 수동 override. missing/inactive 는 reject |
| `--format` | plan 출력 형식. `text` 또는 `json` |

옵션 설계 원칙:
- 옵션은 leaf command 의 입력과 실행 모드만 제어한다.
- 옵션은 claim 상태 전이, domain registry, source summary uniqueness, lint, roll-up 규칙을 우회하지 못한다.
- 내부 상태 처리 옵션은 추가하지 않는다.

exit code:
- `0`: plan 또는 apply 성공
- `1`: 입력/검증 실패
- `2`: review 필요로 staging plan 생성. 파일 생성 자체는 실패가 아님이므로 CLI 정책에서 선택 가능

## 6. 저장 규칙

high/medium confidence:

```text
wiki/domains/<domain>/sources/<video_id>.md
```

low confidence:

```text
wiki/staging/domain-review/<video_id>.md
wiki/staging/domain-review/<video_id>-candidates.md
```

MVP 에서는 concept/entity page 를 쓰지 않는다. source summary 에서 실제 존재하는 wiki page 는 wikilink 로 연결하고, 존재하지 않는 후보는 plain text 또는 candidate table 로 둔다.

## 7. Obsidian link 정책

허용 예시는 다음 형태다. 아래는 lint 가 설계 문서 예시를 실제 link 로 오인하지 않도록 괄호를 띄어 쓴 표기다.

```markdown
[ [wiki/domains/developer-tools/sources/abc123|영상 source summary] ]
[ [wiki/domains/developer-tools/concepts/model-context-protocol] ]
```

조건부 허용:
- 같은 apply plan 에서 생성되는 파일로의 link

금지:
- 존재하지 않는 미래 page wikilink
- 디렉토리 link
- placeholder `[ [wikilink] ]`, `[ [source path] ]`
- root-relative 인지 file-relative 인지 불명확한 markdown link

lint 정비 시 link resolver 는 다음을 지원해야 한다.
- wikilink target 을 repo root 기준으로 먼저 해석
- 실패 시 현재 파일 기준으로 해석
- `.md` 확장자 보강
- 디렉토리는 `overview.md` 또는 `index.md` 가 있을 때만 허용
- `wiki/templates/` placeholder 는 일반 link 검사에서 제외

## 8. LLM 호출 경계

MVP 구현은 prompt-plan + validated SemanticWritePlan input 으로 고정한다. CLI-assisted 방식은 다음 단계에서 adapter 설계가 필요할 때 재검토한다.

| 방식 | 설명 | 장점 | 단점 |
|---|---|---|---|
| prompt-plan + SemanticWritePlan | script 가 raw/context bundle 과 prompt 를 만들고, 사람이 CLI 세션에서 생성한 `write-plan.json` 을 `--write-plan` 으로 검증 입력 | API/모델 결합 최소, 검증 경계 명확 | 외부 CLI 실행은 수동 |
| CLI-assisted | script 가 `LLMResolver.resolve("ingest")` 로 profile 을 확인하고 외부 CLI 세션에 넘길 command/prompt 를 생성 | profile 규약 명확 | 실제 CLI adapter 설계 필요. MVP 제외 |

LLM 출력은 apply 전 구조화 검증을 거쳐야 하며, raw/wiki write 는 Python validator 가 담당한다. LLM 이 직접 파일을 쓰지 않는다.

SemanticWritePlan 검증은 다음을 포함한다.
- `_meta/wiki-ingest-write-plan.schema.json` strict schema 확인
- unknown/additional field reject
- `raw_path`, `video_id` 가 실제 raw 파일과 일치하는지 확인
- target path 를 raw video_id 와 domain decision 으로 재계산
- same target force 외 동일 video_id 중복 reject
- claim rows schema 와 derived roll-up 검증
- wikilink target 검증
- 생성 파일 lint HIGH=0 검증
- `writes`, `skips`, `frontmatter`, derived fields, rendered markdown 이 plan 에 있으면 reject

## 9. 멱등성

멱등 key:

```text
source_summary_path = wiki/domains/<domain>/sources/<video_id>.md
staging_path = wiki/staging/domain-review/<video_id>.md
```

규칙:
- 대상 파일이 있고 `--force` 가 없으면 skip.
- 동일 raw 재실행 시 후보 report 는 같은 target path 로 계산.
- 동일 `video_id` source summary 는 `wiki/domains/*/sources/` 와 `wiki/staging/domain-review/` 전체에서 하나만 존재할 수 있다.
- 다른 domain 에 동일 `video_id` source summary 가 이미 있으면 reject 하고 existing path 를 출력한다.
- domain 이 low 에서 high 로 승격되면 staging 파일을 자동 삭제하지 않는다. 승격은 별도 review command 또는 사람 작업으로 처리한다.
- MVP 는 `wiki/index.md` 와 `wiki/log.md` 를 갱신하지 않는다. index/log 는 다음 promote/index stage 에서 처리한다.

## 10. Domain registry

Domain 목록은 `_meta/domains.yaml` 이 단일 진실이다.

초기 seed:

```text
developer-tools
ai-engineering
software-engineering
information-security
network
cryptography
programming-language
algorithms
```

구현 규칙:
- `wiki_ingest.py` 는 registry loader 를 통해 domain 목록을 읽는다.
- domain 이름을 코드 상수로 하드코딩하지 않는다.
- registry 에 없는 domain decision 은 `confidence=low`, `registry_status=missing` 으로 staging 처리한다.
- inactive domain 은 target 으로 쓰지 않는다.
- `--domain` override 는 active registry domain 에만 허용한다. missing/inactive override 는 reject 한다.
- taxonomy 는 vocab SoT 이고 domain registry 가 아니다.

## 11. 프로젝트 구조

```text
_meta/
  domains.yaml               # domain registry SoT
scripts/
  wiki_ingest.py              # 2차 orchestrator
tests/
  test_wiki_ingest.py         # raw fixture -> plan/render/validate
docs/
  wiki-ingest-prd.md
  wiki-ingest-architecture.md
  wiki-ingest-business-logic.md
  wiki-ingest-review.md
wiki/
  staging/domain-review/
  domains/<domain>/sources/
```

## 12. 요구사항 추적성

| PRD ID | 아키텍처 surface | 비즈니스 로직·검증 surface |
|---|---|---|
| D-5 | §7 Obsidian link 정책 | BR-LINT-1~4 |
| D-6 | §7 Link Resolver | BR-LNK-1~4 |
| D-7 | §2 금지 방향, §3 Candidate Report, §6 저장 규칙 | BR-CAN-4~5 |
| FR-5 | §4 Claim·SourceSummaryMeta·ClaimTable | BR-CLM-1~7, BR-ROLL-1~7·14 |
| FR-12 | §2 금지 방향 | 1차 pipeline import·수정 금지 |
| FR-14 | §10 Domain registry | ADR-0003, BR-DOM-3~6, VR-11 |
| FR-15 | §9 source summary 전역 유일성 | BR-IDEM-7~8, VR-13 |
| FR-16 | §4 ClaimTable 고정 형식 | BR-ROLL-8~13, VR-14 |
| FR-17 | §4 SemanticWritePlan 검증 경계 | BR-LLM-7~9, VR-15 |
| FR-18 | §5 `--domain`, §10 registry override | BR-DOM-7, VR-17 |
| FR-19 | §5 CLI 옵션 경계 | BR-OPT-1~3, VR-16 |
| NFR-1 | §2 단방향 의존 | importer import·수정 금지 |
| NFR-3 | §2 orchestrator 5-stage 구조 | parse/classify/plan-render/validate/commit 경계 |
| NFR-4 | §2 raw 수정 금지, §3 Anti-Corruption Boundary | raw read-only |
| NFR-6 | §7 Obsidian link 정책 | BR-LNK-1~4, VR-7 |
| NFR-8 | §6 staging, §9 별도 승격 생명주기 | BR-DOM-2, BR-IDEM-3·6 |
| NFR-9 | §10 registry loader | BR-DOM-3~6, VR-11 |
| NFR-10 | §4 ClaimTable·derived roll-up | BR-ROLL-1~7·14, VR-12 |
| NFR-11 | §9 `video_id` 전역 유일성 | BR-IDEM-7~8, VR-13 |
| NFR-12 | §5 옵션 최소화 | BR-OPT-1~3, VR-16 |
| NFR-13 | §4 SemanticWritePlan Boundary | BR-LLM-6~9, VR-15 |

## 13. 자체 검증

| 항목 | 상태 | 근거 |
|---|---|---|
| 순환 참조 | PASS | 2차는 1차를 import 하지 않고 raw 산출물만 읽음 |
| 계층 깊이 | PASS | CLI -> orchestrator -> stage 함수 구조. edge 4 이내로 설계 |
| 캡슐화 | PASS | LLM 출력은 직접 write 하지 않고 plan/validator 를 거침. domain 은 registry loader 로만 접근 |
| 요구사항 커버리지 | PASS | PRD FR-1~19 반영 |
| 기술 스택 정합성 | PASS | 기존 Python/PyYAML/argparse 패턴 유지 |
| 복잡성 억제 | PASS | concept/entity 자동 rewrite 와 pipeline 자동 연결 제외 |
| 전역 유일성 | PASS | 동일 video_id source summary 는 staging/domains 전체에서 1개만 허용 |
| 옵션 경계 | PASS | 옵션은 leaf command 입력/실행 모드만 제어하고 비즈니스 규칙 우회 불가 |
| index/log 생명주기 | PASS | MVP 에서 제외하고 promote/index stage 로 분리 |

## 14. 리스크

| 리스크 | 영향 | 대응 |
|---|---|---|
| domain taxonomy 부족 | 많은 문서가 staging 에 쌓임 | 초기에는 정상. review 로 taxonomy 확장 |
| 검증 상태가 frontmatter 와 claim table 에 중복 | 관리 drift | claim table 을 SoT 로 두고 page-level 은 derived roll-up 으로만 허용 |
| index/log 갱신 요구 증가 | source summary lifecycle 과 navigation lifecycle 혼합 | MVP 제외, promote/index stage 로 분리 |
| LLM 출력 품질 불안정 | broken link, 과감한 사실화 | validator 가 claimed 기본값과 existing-link-only 정책 강제 |
