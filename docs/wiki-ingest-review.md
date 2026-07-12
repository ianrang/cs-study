# Review: raw video -> LLM wiki synthesis 설계 검토

> 대상 문서: `docs/wiki-ingest-prd.md`, `docs/wiki-ingest-architecture.md`, `docs/wiki-ingest-business-logic.md`.
> 본 검토는 report-only 이며 코드 구현은 수행하지 않았다.

## 1. 현재 구현 상태

1차 추출/적재 파이프라인은 다음 계약으로 구현되어 있다.

```text
scripts/pipeline.py
  -> ytscript CLI subprocess
  -> canonical JSON path
  -> scripts/ingest.py ingest
  -> raw/sources/video/<video_id>.md/.json
```

확인 사항:
- `scripts/pipeline.py` 는 ytscript 를 import 하지 않고 subprocess 로 호출한다.
- `scripts/ingest.py` 는 canonical JSON dict 만 읽고 추출기 모듈을 import 하지 않는다.
- raw 대상 파일이 있으면 기본 skip, `--force` 시 재생성한다.
- `.md` 와 `.json` 은 temp dir + `os.replace` 로 쓰며, 둘째 쓰기 실패 시 `.md` 를 롤백한다.
- `wiki.enabled=true` 는 자동 합성이 아니라 review gate 안내만 한다.

검증:
- `.venv-lint/bin/python tests/test_ingest.py` -> 14 passed
- `.venv-lint/bin/python tests/test_pipeline.py` -> 8 passed

## 2. 인터페이스 연결성 검토

| 연결 | 상태 | 판단 |
|---|---|---|
| ytscript -> pipeline | PASS | CLI stdout 마지막 JSON path 계약. Python import 없음 |
| pipeline -> ingest | PASS | 내부 함수 호출이지만 1차 범위 안에서만 연결 |
| ingest -> raw | PASS | raw path 와 canonical copy 가 deterministic |
| raw -> wiki 2차 | 설계 PASS | 2차는 raw markdown 을 입력으로 읽는 독립 command |
| pipeline -> wiki 2차 | intentionally disconnected | 자동 연결하지 않아 review gate 와 생명주기 분리 |

판단: 현재 연결성은 단방향이다. 2차 설계도 이 방향을 유지한다.

## 3. 멱등성 검토

| 계층 | key | 현재/설계 동작 |
|---|---|---|
| 1차 raw ingest | `video_id` | `raw/sources/video/<video_id>.md` 존재 시 skip |
| 1차 canonical copy | `video_id` | 동일 path 의 `.json` 보관 |
| 2차 source summary | `video_id` | staging/domains 전체에서 같은 video_id source summary 1개만 허용 |
| 2차 staging | `video_id` | low confidence 는 staging path 로 고정 |
| 후보 report | `video_id` | 같은 raw 재실행 시 같은 report path |

주의할 점:
- domain 이 low 에서 high 로 바뀌는 승격은 자동 이동으로 처리하지 않는다.
- 자동 이동을 넣으면 staging cleanup, index/log 재작성, old link 처리 생명주기가 추가된다.
- 따라서 승격은 별도 review operation 으로 분리하는 것이 단순하다.
- MVP 는 승격 명령을 구현하지 않는다. 승격은 다음 단계의 별도 promote stage 로 설계한다.
- 동일 video_id source summary 는 staging/domains 전체에서 전역 유일해야 한다. 다른 domain 에 이미 있으면 새 파일 생성이 아니라 reject 로 처리한다.

## 4. 논리성/정합성 검토

| 항목 | 상태 | 근거 |
|---|---|---|
| raw 불변 | PASS | 2차는 raw 를 읽기만 함 |
| 보수적 claim 저장 | PASS | 기본 status = claimed |
| 검증 상태 구분 | PASS | claimed/corroborated/verified/rejected |
| 검증 상태 중복 제거 | PASS | claim table 이 SoT, frontmatter 는 derived roll-up |
| claim table 최종 형식 | PASS | `id/primary/claim/status/evidence/notes` 고정 pipe table + `\|` escaping + no multiline cells |
| domain ambiguity 처리 | PASS | low confidence -> staging |
| domain seed 캡슐화 | PASS | `_meta/domains.yaml` 을 단일 진실로 사용 |
| 중복 억제 | PASS | concept/entity 자동 생성 금지, 후보 report 로 분리 |
| Obsidian link 정합성 | PASS | 존재 파일 또는 same-plan 파일만 wikilink 허용 |
| lint 정비 | PASS 설계 | templates/system page 를 일반 wiki page 에서 분리 |
| 순환 참조 | PASS | 2차 -> 1차 import 금지, pipeline -> 2차 자동 호출 금지 |

## 5. 복잡성 제거 결정

제거하거나 이연한 항목:
- `scripts/pipeline.py` 에 wiki stage 자동 실행 추가: 제거
- concept/entity 자동 생성: MVP 제외
- 기존 concept/entity 자동 rewrite: MVP 제외
- taxonomy 자동 확장: 사람 review 로 분리
- staging 자동 삭제/이동: 별도 review operation 으로 분리
- 외부 웹 검증 자동화: MVP 제외
- raw frontmatter 보강: 원본 불변 원칙 때문에 제외
- LLM CLI adapter 자동 실행: MVP 제외, prompt-plan + validated SemanticWritePlan input 으로 제한
- wiki/index.md + wiki/log.md 자동 갱신: MVP 제외, promote/index stage 로 분리
- 내부 상태 전이 옵션: 제거. 옵션은 leaf command 입력/실행 모드만 제어

이 결정으로 생명주기는 세 개로 분리된다.

```text
extract/raw ingest lifecycle
wiki source summary lifecycle
domain/taxonomy review lifecycle
```

## 6. lint 정비 반영 상태

전수 lint 는 scaffold/system/template scope 정비 후 HIGH=0 상태로 검증됐다. 2차 구현 전 lint blocker 는 남아 있지 않다.

| 대상 | 이전 문제 | 반영 |
|---|---|---|
| `wiki/templates/` | placeholder link/source_paths 때문에 HIGH | 일반 wiki content required fields/link 검사 제외 |
| `wiki/index.md` | system page 인데 content frontmatter 를 요구 | content frontmatter 검사만 제외하고 내부 link 검사는 유지 |
| `wiki/log.md` | system page 인데 content frontmatter 를 요구 | content frontmatter 검사만 제외하고 내부 link 검사는 유지 |
| `wiki/overview.md` | 예정 link 와 root-relative link 가 혼재 | 예정 대상은 plain path로 두고 실제 내부 link는 root-first resolver로 검사 |
| `_meta/*.md` | 예시 wikilink 가 broken 처리 | fenced code block link 검사 제외 및 예시 link escape |

## 7. 요구사항 충족 검토

| 사용자 요구 | 충족 | 설명 |
|---|---|---|
| 추천 B domain 분류 | PASS | confidence 기반 staging |
| 애매하면 staging | PASS | BR-DOM-2 |
| 보수적 claim | PASS | BR-CLM-1 |
| 검증 완료/미완료 구분 | PASS | VerificationStatus enum |
| lint 예외 정비 포함 | PASS | PRD FR-10, logic BR-LINT-* |
| Obsidian 링크 정확성 | PASS | link resolver 정책 |
| 공식/검증된 기준 비교 | PASS | Obsidian 공식 link/graph, LLM Wiki raw/wiki/schema 분리 기준 반영 |
| 규칙/원칙 준수 | PASS | raw 불변, source_paths, review gate, taxonomy review |
| 중복/복잡성 제거 | PASS | candidate report, 자동 rewrite 제외 |
| 순환/양방향 참조 제거 | PASS | import/call 금지 방향 명시 |
| domain 확장성 | PASS | domain seed 는 `_meta/domains.yaml` 단일 수정 지점 |
| 검증 상태 정합성 | PASS | claim table 과 roll-up 불일치 시 reject |
| source summary 전역 유일성 | PASS | 동일 video_id 는 staging/domains 전체에서 1개만 허용 |
| SemanticWritePlan 캡슐화 | PASS | LLM/사람 plan 은 파일 쓰기 계획이 아니라 `_meta/wiki-ingest-write-plan.schema.json` 기반 semantic JSON 검증 대상 |
| 옵션 경계 | PASS | `--apply/--force/--now/--write-plan/--domain/--format` 만 허용하고 규칙 우회 불가 |
| index/log 분리 | PASS | MVP 는 index/log 를 쓰지 않고 promote/index stage 로 이연 |

## 8. 구현 전 체크리스트

완료된 기반 작업:
1. `scripts/lint.py` 에 template/system page scope 분리.
2. root-relative wikilink resolver 보강.
3. `_meta/domains.yaml` 을 추가하고 seed domains 를 등록한다.
4. claim table schema validator 를 구현한다. Literal pipe 는 `\|` 로 escape 하고 multiline cell 은 reject 한다.

남은 2차 wiki ingest 구현 작업:
1. `scripts/wiki_ingest.py` 는 plan-only 기본으로 구현.
2. `tests/test_wiki_ingest.py` 에 raw fixture, low confidence fixture, duplicate candidate fixture 추가.
3. source summary frontmatter 에 `verification_status` 와 `claim_status_counts` 를 derived field 로 반영한다.
4. taxonomy 확장은 자동화하지 않고 candidate report 로만 제안.
5. verified 는 공식 문서, 원문 논문, canonical repo, maintainer/저자 문서 evidence 가 있을 때만 허용한다.
6. 동일 video_id source summary 전역 유일성 검사를 구현한다.
7. `--write-plan` 입력은 `_meta/wiki-ingest-write-plan.schema.json` strict schema 와 path/target/claim/link/lint 검증을 통과해야 apply 가능하게 한다.
8. `--domain` override 는 active registry domain 만 허용하고 missing/inactive 는 reject 한다.
9. MVP write plan 에 `wiki/index.md` 또는 `wiki/log.md` write 가 있으면 reject 한다.

## 9. 결론

설계는 현재 1차 추출/적재 파이프라인의 인터페이스와 멱등성을 깨지 않는다.

가장 중요한 구조적 결정은 2차를 `pipeline.py` 에 붙이지 않는 것이다. 이렇게 해야 raw 생성, wiki 합성, domain/taxonomy review 의 생명주기가 섞이지 않고, 재실행과 review gate 가 명확하다.

MVP 는 source summary + candidate report + lint 정비 + domain registry + derived verification roll-up + validated SemanticWritePlan input 으로 제한하는 것이 맞다. 이 범위는 사용자의 요구사항을 만족하면서도 중복 문서, 검증되지 않은 지식 승격, 순환 의존, 불필요한 관리 포인트를 최소화한다.
