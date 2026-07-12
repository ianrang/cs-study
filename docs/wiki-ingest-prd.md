# PRD: raw video -> LLM wiki synthesis (2차)

> 범위: 본 문서는 `raw/sources/video/<video_id>.md` 를 입력으로 받아 LLM wiki source summary 와 review 후보를 생성하는 2차 라운드를 정의한다.
> 1차 추출/적재(`scripts/pipeline.py`, `scripts/ingest.py`)는 변경하지 않는다. 2차는 1차 산출물을 읽는 독립 stage 이다.

## 1. 목적

유튜브 스크립트 raw 원문을 그대로 wiki 에 복사하지 않고, raw 를 근거로 삼아 Obsidian 에서 탐색 가능한 지식 페이지로 정리한다.

핵심 목표:
- raw 원문은 불변으로 보존한다.
- wiki 에는 근거 경로, 분류, 검증 상태, 내부 링크를 갖춘 source summary 를 생성한다.
- domain 이 불확실하거나 검증이 부족한 내용은 `wiki/staging/domain-review/` 에 둔다.
- 기존 wiki/taxonomy 와 중복되는 concept/entity 는 새 페이지로 만들지 않고 후보로 보고한다.
- lint 예외/정비를 포함해 생성 산출물이 broken link 와 frontmatter drift 를 만들지 않게 한다.

## 2. 현재 1차 파이프라인 계약

현재 구현은 1차 범위에서 완료되어 있다.

```text
scripts/pipeline.py <URL>
  -> ytscript CLI subprocess 호출
  -> canonical JSON 경로 회수
  -> scripts/ingest.py 내부 ingest 호출
  -> raw/sources/video/<video_id>.md
  -> raw/sources/video/<video_id>.json
  -> wiki.enabled=true 여도 review gate 메시지 후 정지
```

2차는 이 계약 뒤에 연결된다.

```text
raw/sources/video/<video_id>.md
  -> scripts/wiki_ingest.py <raw-path>
  -> wiki/domains/<domain>/sources/<video_id>.md
  -> 또는 wiki/staging/domain-review/<video_id>.md
```

2차는 `scripts/pipeline.py` 안에 자동 연결하지 않는다. 자동 연결하면 extract, raw ingest, wiki synthesis 생명주기가 한 명령에 섞여 재실행 의미와 review gate 가 불명확해진다.

## 3. 사용자 결정

| ID | 결정 | 반영 |
|---|---|---|
| D-1 | domain 분류는 confidence 기반 staging 정책을 쓴다 | high/medium 은 domains, low 는 staging |
| D-2 | domain 이 애매하면 staging 에 둔다 | 자동 승격 금지 |
| D-3 | 영상 주장은 보수적으로 저장한다 | claim 은 기본 `claimed` |
| D-4 | 검증 완료/미완료를 구분한다 | claim table 이 검증 상태 SoT, page-level `verification_status` 는 roll-up 파생값 |
| D-5 | lint 예외 정비를 같이 한다 | templates/system page 를 일반 wiki page 와 분리 |
| D-6 | Obsidian 링크는 실제 존재 문서로 정확히 연결한다 | broken link hard-fail 유지 |
| D-7 | 순환/양방향 참조와 중복 복잡성을 제거한다 | 2차는 1차를 읽기만 하고 기존 concept/entity 자동 rewrite 금지 |
| D-8 | 승격 명령은 다음 단계로 분리한다 | MVP 는 staging 생성까지만 수행 |
| D-9 | domain seed 는 registry 로 관리한다 | `_meta/domains.yaml` 을 domain SoT 로 사용하고 code hardcode 금지 |
| D-10 | LLM 실행은 초기에는 prompt-plan + validated SemanticWritePlan input 으로 제한한다 | CLI adapter 자동 실행은 MVP 제외 |
| D-11 | source summary 는 video_id 기준 전역 유일해야 한다 | staging/domains 전체에 동일 video_id source summary 1개만 허용 |
| D-12 | claim table 형식은 고정한다 | `id/primary/claim/status/evidence/notes` markdown table 을 SoT 로 사용 |
| D-13 | LLM prompt-plan 결과는 검증된 SemanticWritePlan 으로만 apply 한다 | LLM 은 파일을 직접 쓰지 않고 `_meta/wiki-ingest-write-plan.schema.json` 에 맞는 semantic JSON 만 제공한다 |
| D-14 | index/log 갱신은 MVP 에서 제외한다 | source summary/candidate 생성과 promotion/index lifecycle 을 분리한다 |
| D-15 | 옵션은 leaf 실행 모드와 입력만 제어한다 | 내부 상태 전이, 검증 기준, roll-up 규칙은 옵션화하지 않는다 |
| D-16 | domain 수동 override 는 active registry domain 만 허용한다 | missing/inactive domain override 는 reject 하고 classifier 결과의 missing/inactive 는 staging 으로 간다 |

## 4. 기능 요구사항

| ID | 요구사항 | 수용 기준 | 우선순위 |
|---|---|---|---|
| FR-1 | 2차 입력은 명시적 raw video markdown 파일 1개다 | `scripts/wiki_ingest.py raw/sources/video/<id>.md` 형태. 디렉토리 전체 자동 스캔 금지 | Must |
| FR-2 | raw page frontmatter 와 body 를 파싱한다 | raw 필수 필드 누락 시 거부. raw body 는 수정하지 않음 | Must |
| FR-3 | domain 을 분류하고 confidence 를 기록한다 | `_meta/domains.yaml` 에 등재된 domain 만 active target 으로 사용. low 는 staging 저장 | Must |
| FR-4 | source summary page 를 생성한다 | wiki content 15필드 + source summary 추가 필드 충족 | Must |
| FR-5 | claim 을 보수적으로 저장한다 | 영상 기반 claim row 는 기본 `claimed`. page-level `verification_status` 는 claim table 에서 파생 | Must |
| FR-6 | 검증 상태를 구분한다 | `claimed \| corroborated \| verified \| rejected` enum 사용 | Must |
| FR-7 | concept/entity 후보를 추출하되 자동 승격하지 않는다 | 후보 report 에 existing/duplicate/review-needed 로 표시 | Must |
| FR-8 | 기존 wiki/taxonomy 중복을 검사한다 | 같은 slug, alias, 기존 wikilink 후보 발견 시 새 페이지 생성 금지 | Must |
| FR-9 | Obsidian 내부 링크는 실제 파일에만 연결한다 | 존재하지 않는 link 는 후보 텍스트로 두거나 staging review 로 보낸다 | Must |
| FR-10 | lint 정비를 포함한다 | `wiki/templates/`, `wiki/index.md`, `wiki/log.md`, `wiki/overview.md` 는 별도 규칙으로 처리 | Must |
| FR-11 | MVP 는 index/log 를 갱신하지 않는다 | source summary/candidate 생성만 수행하고 index/log 는 다음 promote/index stage 로 이연 | Must |
| FR-12 | 1차 추출/적재 파이프라인을 변경하지 않는다 | `scripts/pipeline.py`, `scripts/ingest.py` 의 호출 계약 유지 | Must |
| FR-13 | LLM 호출 규약을 준수한다 | profile alias `ingest` 만 사용. API 호출 금지. model_id 하드코딩 금지 | Must |
| FR-14 | domain registry 를 단일 진실로 사용한다 | domain 추가/비활성화는 `_meta/domains.yaml` 한 곳에서 시작. taxonomy 는 vocab SoT 로 분리 | Must |
| FR-15 | source summary 전역 유일성을 보장한다 | 동일 `video_id` 는 `wiki/domains/*/sources/` 와 `wiki/staging/domain-review/` 전체에서 하나만 존재 가능 | Must |
| FR-16 | claim table 표준 형식을 검증한다 | `## Claims` 아래 `id/primary/claim/status/evidence/notes` table 이 없거나 schema 가 다르면 reject | Must |
| FR-17 | LLM 결과는 SemanticWritePlan 입력으로만 적용한다 | `--write-plan <json>` 은 `_meta/wiki-ingest-write-plan.schema.json`, path scope, claim rows, roll-up, lint 검증 통과 시에만 `--apply` 가능 | Must |
| FR-18 | domain override 를 제한적으로 허용한다 | `--domain <domain>` 은 `_meta/domains.yaml` 의 active domain 에만 허용. invalid override 는 reject | Should |
| FR-19 | CLI 옵션은 실행 경계만 제어한다 | 허용 옵션은 `--apply`, `--force`, `--now`, `--write-plan`, `--domain`, `--format` 으로 제한 | Should |

## 5. 비기능 요구사항

| ID | 요구사항 | 기준 |
|---|---|---|
| NFR-1 | 단방향 의존 | 2차는 raw/wiki/_meta 를 읽고 wiki 만 쓴다. 1차 importer 를 import 하거나 수정하지 않는다 |
| NFR-2 | 멱등성 | 같은 raw 를 재실행하면 같은 target path 를 계산하고, 기존 산출이 있으면 기본 skip 또는 plan-only diff 를 출력한다 |
| NFR-3 | 낮은 복잡도 | 신규 script 는 parse, classify, plan/render, validate, commit 의 5개 major stage 를 넘지 않는다. SemanticWritePlan 경계는 plan/validate 내부 책임으로 둔다 |
| NFR-4 | 원본 불변 | raw body/frontmatter 는 2차에서 수정하지 않는다 |
| NFR-5 | 검증 가능성 | 생성/변경 파일 단위 lint 가 HIGH=0 이어야 한다 |
| NFR-6 | Obsidian 정합성 | wikilink 는 실제 존재 파일 또는 같은 작업에서 생성되는 파일만 허용한다 |
| NFR-7 | 중복 억제 | 새 concept/entity page 는 MVP 범위에서 생성하지 않고 후보로만 둔다 |
| NFR-8 | review gate | low confidence, ambiguous claim, taxonomy 확장은 사람 review 없이는 domains 로 승격하지 않는다 |
| NFR-9 | domain 캡슐화 | wiki ingest 코드는 domain 이름을 하드코딩하지 않고 registry loader 를 통해서만 접근한다 |
| NFR-10 | 검증 상태 정합성 | claim table 과 page-level roll-up 이 불일치하면 reject 한다 |
| NFR-11 | source summary 유일성 | video_id 중복 source summary 를 생성하지 않는다 |
| NFR-12 | 옵션 최소화 | 옵션은 leaf command 입출력/실행 모드만 제어하고 비즈니스 규칙을 우회하지 못한다 |
| NFR-13 | SemanticWritePlan 캡슐화 | LLM output 은 신뢰하지 않고 Python validator 가 SourceInput/registry/wiki state 로 target path, frontmatter, markdown, roll-up, write operation 을 재계산한다 |

## 6. MVP 범위

포함:
- raw video 1개 입력
- source summary 생성
- domain confidence 산출
- low confidence staging
- claim 검증 상태 구분
- concept/entity 후보 report
- existing wiki/taxonomy 중복 검사
- lint 예외 정비 설계 및 구현
- `_meta/domains.yaml` domain seed registry 도입
- video_id source summary 전역 유일성 검사
- prompt/context bundle 생성
- `_meta/wiki-ingest-write-plan.schema.json` 기반 `--write-plan` schema 검증과 적용
- 제한적 active domain override

제외:
- 기존 concept/entity 본문 자동 rewrite
- raw 수정
- taxonomy 자동 확장
- 외부 웹 검증 자동화
- `scripts/pipeline.py` 에 wiki stage 자동 연결
- wiki commit 자동 수행
- staging 승격 명령
- LLM CLI adapter 자동 실행
- wiki/index.md + wiki/log.md 자동 갱신
- business rule 을 우회하는 내부 상태 옵션

## 7. 산출물 형식

확실한 domain:

```text
wiki/domains/<domain>/sources/<video_id>.md
```

불확실한 domain:

```text
wiki/staging/domain-review/<video_id>.md
```

후보 report:

```text
wiki/staging/domain-review/<video_id>-candidates.md
```

## 8. 검증 상태 의미

| 상태 | 의미 | wiki 본문 표현 |
|---|---|---|
| `claimed` | raw 영상이 주장했지만 추가 검증 전 | "영상은 X 라고 주장한다" |
| `corroborated` | 다른 raw 또는 사용자 노트가 같은 취지로 지지 | "복수 source 에서 X 가 반복된다" |
| `verified` | 공식 문서, 원문 논문, 신뢰 가능한 repo 등으로 확인 | 지식 문장으로 승격 가능 |
| `rejected` | 검증 결과 틀림 | source summary 에 반례와 함께 남기고 concept/entity 에 반영 금지 |

### 검증 상태 SoT 와 roll-up

검증 상태의 source of truth 는 claim table 이다. Frontmatter 의 `verification_status` 는 사람이 독립적으로 판단하는 값이 아니라 claim table 에서 계산되는 page-level roll-up 이다.

```yaml
verification_status: claimed
claim_status_counts:
  claimed: 4
  corroborated: 1
  verified: 0
  rejected: 0
```

규칙:
- claim table 이 SoT 이다.
- `verification_status` 는 검색, 필터링, review queue 용 파생값이다.
- `claim_status_counts` 는 claim table 에서 계산한 통계다.
- claim table 과 frontmatter roll-up 이 불일치하면 validator 가 reject 한다.
- 영상 하나만 근거인 claim 은 `verified` 가 될 수 없다.
- claim table 은 `id/primary/claim/status/evidence/notes` pipe table 로 고정한다.
- claim table cell 안의 literal pipe 는 `\|` 로 escape 하고, multiline cell 은 허용하지 않는다.
- `claim_status_counts` 는 전체 claim row count 이며, `verification_status` 는 `primary=true` claim 으로 계산한다.
- Obsidian properties 는 small atomic metadata 에 적합하고 Markdown in properties 를 지원하지 않으므로, claim 상세는 frontmatter 에 넣지 않는다.

Page-level roll-up:
- `primary=true` claim이 하나도 없으면 `verification_status: claimed`.
- 핵심 claim 전체가 verified이고 전체 claim row의 rejected가 0개면 `verification_status: verified`.
- 핵심 claim 전체가 최소 corroborated 이상이고 전체 claim row의 rejected가 0개면 `verification_status: corroborated`.
- 그 외 대부분은 `verification_status: claimed`.
- 핵심 claim 전체가 반박되면 `verification_status: rejected`.

## 9. Domain seed registry

Domain 은 `_meta/domains.yaml` 이 단일 진실이다. `_meta/taxonomy.md` 는 tag/entity/concept vocabulary 의 단일 진실이며 domain 목록의 SoT 가 아니다.

초기 seed:

```yaml
version: 1
domains:
  developer-tools:
    status: active
    label: Developer Tools
    source_roots: [tools/, development/claud-code/]
  ai-engineering:
    status: active
    label: AI Engineering
    source_roots: [development/ai-industry/, development/harness/]
  software-engineering:
    status: active
    label: Software Engineering
    source_roots: [development/software-engineering/, development/architecture/]
  information-security:
    status: active
    label: Information Security
    source_roots: [cs/information-security/, cs/security/]
  network:
    status: active
    label: Network
    source_roots: [cs/network/]
  cryptography:
    status: active
    label: Cryptography
    source_roots: [cs/cryptography/]
  programming-language:
    status: active
    label: Programming Language
    source_roots: [lang/]
  algorithms:
    status: active
    label: Algorithms
    source_roots: [coding-test/]
```

규칙:
- domain 추가/비활성화는 `_meta/domains.yaml` 에서 시작한다.
- `scripts/wiki_ingest.py` 는 registry loader 로만 domain 을 읽는다.
- script 에 domain 이름을 하드코딩하지 않는다.
- `wiki/overview.md`, `wiki/index.md`, domain directory 는 registry 와 정합 검증 대상이다.
- registry 에 없는 domain 은 low confidence 로 강등되어 staging 으로 간다.
- 사용자가 `--domain` 으로 수동 지정한 domain 은 registry 에 있고 active 여야 한다. missing/inactive override 는 reject 한다.

## 10. CLI 옵션과 SemanticWritePlan 경계

MVP CLI 옵션은 leaf command 의 입력과 실행 모드만 제어한다. claim 상태 전이, domain registry 규칙, source summary 전역 유일성, lint 기준, roll-up 계산은 옵션으로 우회할 수 없다.

허용 옵션:

| 옵션 | 의미 | 규칙 |
|---|---|---|
| `--apply` | 검증 통과 시 파일 생성 | 없으면 파일 변경 0 |
| `--force` | same target source summary 덮어쓰기 | 다른 domain/staging 에 존재하는 동일 video_id 는 여전히 reject |
| `--now YYYY-MM-DD` | 테스트 결정성을 위한 날짜 주입 | 렌더링 날짜에만 영향 |
| `--write-plan <json>` | 외부 LLM/사람이 만든 SemanticWritePlan 입력 | schema/path/lint/claim 검증 통과 시에만 사용 |
| `--domain <domain>` | active registry domain 으로 수동 override | missing/inactive domain 은 reject |
| `--format text\|json` | plan 출력 형식 | 산출 semantics 에 영향 없음 |

SemanticWritePlan 규칙:
- LLM 은 파일을 직접 쓰지 않는다.
- script 는 raw/context bundle 과 prompt 를 만들 수 있다.
- 사람 또는 외부 CLI 세션이 생성한 `write-plan.json` 은 신뢰 입력이 아니라 검증 대상이다.
- `write-plan.json` 은 `_meta/wiki-ingest-write-plan.schema.json` 을 따라야 한다.
- `write-plan.json` 은 semantic fields 만 담는다: `schema_version`, `raw_path`, `video_id`, `domain_decision`, `source_summary`, `claims`, `candidates`.
- `writes`, `skips`, `source_summary_path`, `candidate_report_path`, `frontmatter`, `verification_status`, `claim_status_counts`, rendered markdown 은 금지한다.
- Python validator 는 path scope, source summary uniqueness, claim rows, derived roll-up, wikilink, frontmatter, lint 를 모두 재검증한다.
- validator 는 target path, frontmatter, claim table markdown, candidate report markdown, write operation 을 재계산한다.

## 11. Source summary 전역 유일성

동일 `video_id` 의 source summary 는 wiki 전체에서 하나만 존재할 수 있다.

검사 범위:

```text
wiki/domains/*/sources/<video_id>.md
wiki/staging/domain-review/<video_id>.md
```

동작:
- 같은 target 에 이미 있으면 skip 또는 `--force`.
- 다른 domain source 에 이미 있으면 reject 하고 existing path 를 출력한다.
- staging 에 이미 있으면 skip 또는 review 필요로 보고한다.
- domains 에 이미 있는데 staging 생성 시도하면 reject 한다.
- domain 재분류나 이동은 MVP 가 아니라 다음 promote/move stage 에서 처리한다.

## 12. Index/log 정책

MVP 는 source summary 와 candidate report 만 생성한다. `wiki/index.md` 와 `wiki/log.md` 갱신은 source promotion/index stage 로 분리한다.

이유:
- source summary 생성과 wiki navigation/index lifecycle 을 분리해 재실행 의미를 단순하게 유지한다.
- staging 승격, index/log, old link cleanup 을 같은 command 에 묶으면 관리해야 할 상태가 증가한다.
- AGENTS.md 의 일반 ingest sequence 는 최종 wiki 반영 lifecycle 이며, YouTube MVP source-summary stage 는 그 전 단계다.

## 13. 수용 기준

2차 MVP 는 다음을 만족해야 완료로 본다.

- 1차 테스트(`tests/test_ingest.py`, `tests/test_pipeline.py`)가 계속 통과한다.
- raw video fixture 1개로 source summary 와 후보 report 를 생성한다.
- low confidence fixture 는 `wiki/staging/domain-review/` 로 간다.
- 재실행 시 중복 파일을 만들지 않는다.
- 생성 파일에 broken link 가 없다.
- templates/system page 때문에 전수 lint 가 실패하지 않는다.
- 기존 concept/entity 자동 rewrite 가 없다.
- `verification_status` 와 `claim_status_counts` 가 claim table 과 동기화된다.
- domain seed 는 `_meta/domains.yaml` 한 곳에서 관리된다.
- 동일 `video_id` source summary 가 staging/domains 전체에서 중복 생성되지 않는다.
- claim table schema 가 고정 형식으로 검증된다.
- `--write-plan` 입력은 schema 또는 validator 검증 실패 시 파일을 쓰지 않는다.
- `--domain` override 는 active registry domain 에만 성공한다.
- MVP 실행은 `wiki/index.md` 와 `wiki/log.md` 를 변경하지 않는다.

## 14. 외부 기준과 정합성

- Obsidian 공식 문서는 wikilink, markdown internal link, heading/block link 를 지원한다. 본 프로젝트는 Obsidian graph 정합성을 위해 wikilink 를 주 형식으로 쓰되, 존재하지 않는 내부 링크는 만들지 않는다.
- Obsidian graph view 는 internal link 를 note 관계로 시각화한다. 따라서 source summary 에서 concept/entity 후보를 링크할 때는 실제 파일 존재 여부가 중요하다.
- Obsidian properties 는 YAML frontmatter 에 저장되고 Markdown in properties 를 지원하지 않는다. 따라서 claim 상세는 본문 table 로 두고 frontmatter 에는 derived metadata 만 둔다.
- Obsidian/GFM table syntax 는 header row, delimiter row, data row 의 pipe table 형식을 지원한다. Claim table 은 이 형식을 validator 가 읽을 수 있도록 고정한다.
- LLM Wiki 패턴은 raw sources, wiki, schema file 을 분리하고 ingest/query/lint 루프를 둔다. 본 PRD 는 raw 불변, wiki 합성, AGENTS.md schema, lint gate 를 유지한다.

참고:
- Obsidian Internal links: https://obsidian.md/help/links
- Obsidian Graph view: https://obsidian.md/help/Plugins/Graph%2Bview
- Obsidian Properties: https://help.obsidian.md/properties
- Obsidian Advanced syntax tables: https://help.obsidian.md/advanced-syntax
- GitHub Flavored Markdown tables: https://github.github.com/gfm/#tables-extension-
- Karpathy LLM Wiki gist listing: https://gist.github.com/karpathy
