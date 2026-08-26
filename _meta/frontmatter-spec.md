# Frontmatter Spec

본 문서는 등급 별 frontmatter 필수·선택 필드를 정의한다.

규칙 수명: raw video pair·field 절은 2026-08-23 immutable ArtifactBundle capture 전환으로 superseded된 historical non-normative다. wiki content 절은 순서 6b 전까지 current legacy contract다. 순서 5의 target checker는 fixture·no-write dry-run에만 적용하고 legacy wiki에는 적용하지 않는다. 승인된 순서 6b migration 성공과 같은 변경에서 wiki content의 frontmatter lifecycle·claim/evidence·content-page `provenance` field 규칙을 `_meta/knowledge.schema.json`과 `docs/wiki-ingest-business-logic.md` 규칙으로 supersede한다. 외부 `wiki/_meta/provenance.json` 선언은 순서 9 migration apply 성공과 같은 변경에서 supersede한다. 각 surface의 전환 전에는 legacy 규칙만 active normative이고 전환 후에는 target 규칙만 active normative다. superseded 절은 historical non-normative로 남으며 active hard-rule registry 대상에서 제외하고, 같은 surface에 legacy와 target validator를 동시에 적용하지 않는다.

## wiki/ content 페이지 (synthesis 등급) — 15 필드

```yaml
---
title: "Mixture of Experts (MoE)"            # 필수
tier: llm-synthesis                            # 필수 enum: raw | human-note | llm-synthesis
page_type: concept                             # 필수 enum: concept | entity | comparison | benchmark | dataset | method
domain: llm-foundations                        # 필수 — wiki/domains/<domain>/
domain_confidence: high                        # 필수 enum: high | medium | low (low → staging/domain-review)
shared_scope: domain                           # enum: domain | global (global 은 2 도메인 이상 reuse 만)
tags: [architecture, sparse-models, scaling]   # taxonomy.md controlled vocabulary 만
status: active                                 # enum: draft | active | staged | archived
date_created: 2026-05-20                       # ISO 8601
date_updated: 2026-05-20                       # ISO 8601
source_paths:                                  # 필수 — 인용 path 배열
  - raw/sources/papers/2401.04088.md
  - cs/information-security/.../crypto-aes.md
source_count: 2
provenance: extracted                          # enum: extracted | inferred | ambiguous
summary: "Sparse architecture routing tokens to a subset of expert FFNs per layer; reduces active params while keeping total capacity."
evergreen: false                               # foundational paper 면제 시 true (concept type 한정)
---
```

## raw/sources/ (raw 등급) — 최소 6 필드

```yaml
---
title: "Mixtral of Experts (Jiang et al., 2024)"
source_url: "https://arxiv.org/abs/2401.04088"   # 외부 url 또는 local path
source_date: 2024-01-08                            # 출처 발행일
source_type: paper                                  # enum: paper | blog | video | podcast | conversation | clipping
last_verified: 2026-05-20                           # 최종 확인 timestamp (재현성·시의성)
ingested_date: 2026-05-20                              # video importer 추가 필드; 전역 raw 최소 6에는 미포함
tier: raw
---
```

`source_type: video` 페이지는 `raw/sources/video/<video_id>.md` 에 저장하고 canonical 원본을 `<video_id>.json` 으로 동반 보관한다 (ADR-0002, video importer).

선택 필드 (자동 채워짐 — Paper Importer 등):
- `authors`, `abstract`, `doi`, `arxiv_id`, `isbn`, `pages`

## raw/sources/conversations/ (Claude Code 세션) — 추가 필드

```yaml
---
title: "Session 2026-05-20 — LLM wiki panel-debate"
source_type: conversation
session_id: "20260520-132625"
session_path: "~/.claude/projects/.../sessions/20260520-132625.jsonl"
participants: ["swan", "claude-opus-4-7"]    # 실제 model_id 는 ingest 시점의 lookup. 메타로만 기록 (lint 통과 위해 별도 처리).
last_verified: 2026-05-20
tier: raw
---
```

## cs/, development/, coding-test/, lang/, tools/ (authored 등급) — lazy fallback

frontmatter 없어도 동작. ingest 시점에 `_meta/defaults.yaml` default 추정:

```yaml
# defaults.yaml 가 제공하는 추정 값
tier: human-note
human_authored: true
inferred: true        # default 추정값임을 표시
source_paths: []      # 사람 노트는 자체 source
provenance: extracted # 사람 작성 원문에 직접 존재하는 내용
```

사용자가 의도적으로 frontmatter 추가 시 lazy 추정값을 override.

`wiki/overview.md`, `wiki/index.md`, `wiki/log.md`, `wiki/templates/` 는 system/template scope 이므로 위 content page 필수 필드 검사 대상이 아니다.

## Source 페이지 — source summary 페이지 추가 필드

wiki/domains/<domain>/sources/ 에 생성되는 source summary 페이지는 위 15 필드 + 다음 추가:

```yaml
source_path: raw/sources/papers/2401.04088.md   # source 원본
main_claims:
  - "Mixtral 8x7B uses 8 experts, top-2 routing"
  - "Outperforms Llama 2 70B with ~5x less inference cost"
entities_touched:
  - "[[wiki/domains/llm-foundations/entities/mistral-ai]]"
concepts_touched:
  - "[[wiki/domains/llm-foundations/concepts/top-k-routing]]"
pages_updated:                                  # 본 source 가 ingest 시 갱신한 wiki 페이지
  - "[[wiki/domains/llm-foundations/concepts/mixture-of-experts]]"
```

`source_type: video` 의 source summary 는 추가로 다음 derived field 를 가진다.

```yaml
verification_status: claimed                    # derived: claim table roll-up
claim_status_counts:                            # derived: claim table count
  claimed: 4
  corroborated: 1
  verified: 0
  rejected: 0
```

검증 상태의 source of truth 는 본문 `## Claims` table 이다. Frontmatter 의 `verification_status` 와 `claim_status_counts` 는 검색·필터링·review queue 용 파생값이며, claim table 과 불일치하면 ingest 를 거부한다.

Claim table 표준 형식:

```markdown
## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|
| C1 | true | 영상은 X라고 주장한다. | claimed | raw/sources/video/abc123.md | 추가 검증 필요 |
```

Claim table 규칙:
- `id`: 문서 내 claim 식별자. `C1`, `C2` 형식.
- `primary`: `true | false`. page-level 등급 threshold는 `primary=true` claim으로 계산하고, 전체 claim row의 `rejected` 존재 여부는 verified/corroborated 승격 veto로 사용한다.
- `claim`: 보수적 주장 문장. 영상 하나만 근거면 "영상은 ... 주장한다" 형태를 유지한다.
- `status`: `claimed | corroborated | verified | rejected`.
- `evidence`: 기본적으로 raw path를 기록한다. `verified` 상태는 검토·보존된 `raw/sources/papers/`, `raw/sources/web/`, `raw/sources/urls/` 아래 Markdown 근거만 허용하며 외부 URL은 먼저 raw source로 ingest한다.
- `notes`: key는 필수이며 내용은 비어 있을 수 있다. 값이 있으면 추가 검증 필요, 반례, 보충 설명을 기록한다.

Claim table escaping/parsing 규칙:
- `## Claims` heading 아래 첫 non-empty line 은 header row 여야 한다.
- header columns 는 정확히 `id | primary | claim | status | evidence | notes` 순서여야 하며 누락·추가·순서 변경을 허용하지 않는다.
- 두 번째 non-empty line 은 delimiter row 여야 하며 각 cell 은 `---`, `:---`, `---:`, `:---:` 형식만 허용한다.
- data row 는 pipe table row 만 허용한다. 빈 줄 또는 pipe 로 시작하지 않는 줄에서 claim table 이 종료된다.
- cell 안의 literal pipe 는 반드시 `\|` 로 escape 한다. unescaped pipe 는 column separator 로 파싱한다.
- cell 안의 newline 은 허용하지 않는다. 긴 문장은 한 줄 문장으로 정리한다.
- `id` 는 정규식 `C[1-9][0-9]*` 를 따른다.
- `id` 는 문서 내 unique 여야 한다.
- `primary` 는 소문자 `true` 또는 `false` 만 허용한다.
- `status` 는 소문자 `claimed`, `corroborated`, `verified`, `rejected` 만 허용한다.
- `claim` 과 `evidence` 는 non-empty 여야 한다.
- `claim_status_counts` 는 전체 claim row 의 status count 이다.
- `verification_status` roll-up의 등급 threshold는 `primary=true` claim으로 계산하되, 전체 claim row의 `rejected` count가 1 이상이면 verified/corroborated가 될 수 없다.

Roll-up 규칙:
- 아래 순서를 위에서부터 평가해 처음 충족한 결과 하나만 사용한다.
- `primary=true` claim이 하나도 없으면 `verification_status: claimed`.
- 핵심 claim 전체가 `rejected` 이면 `verification_status: rejected`.
- 핵심 claim 전체가 `verified` 이고 전체 claim row의 `rejected` count가 0이면 `verification_status: verified`.
- 핵심 claim 전체가 최소 `corroborated` 이상이고 전체 claim row의 `rejected` count가 0이면 `verification_status: corroborated`.
- 그 외는 `verification_status: claimed`.
- 영상 하나만 근거인 claim 은 `verified` 가 될 수 없다.
- 자동 lint에서 `verified` evidence는 검토·보존된 `raw/sources/{papers,web,urls}/...md` 경로만 허용한다.

참고 기준:
- Obsidian Properties 는 YAML frontmatter 에 저장되며, Markdown in properties 는 지원하지 않는다. 따라서 claim 상세는 frontmatter 가 아니라 본문 table 로 둔다.
- Obsidian table syntax 와 GitHub Flavored Markdown table spec 은 header row, delimiter row, data row 의 pipe table 형식을 지원한다.

## human_authored 추적 (Panel A C3 — 외부 인덱스)

cs/, development/ 노트의 `human_authored` 메타는 **frontmatter 가 아닌 `wiki/_meta/provenance.json`** 외부 인덱스에 기록. 본문 무변경 보장.

```json
{
  "cs/information-security/.../aes.md": {
    "human_authored": true,
    "inferred": true
  },
  "cs/information-security/.../some-llm-paste.md": {
    "human_authored": "partial",
    "llm_assisted_sections": ["## 응용 사례"],
    "source": "ChatGPT 답변 2026-05-15"
  }
}
```

`partial` 시 source URL/도서/AI 모델 명시 의무. 사용자가 lazy 적용 시 본 파일에 직접 entry 추가.

## 검증 (lint.py)

- wiki/ content 페이지: 15 필드 hard-fail
- wiki/ system/template 페이지: content page 필수 필드 검사 제외. system page 내부 링크는 검사하고 template의 예시·placeholder 링크만 제외
- raw/ 페이지: 최소 6 필드(lint.py `RAW_REQUIRED_FIELDS`) hard-fail
- source summary claim table: fixed columns, escaping/parsing, derived field 누락·roll-up 불일치 hard-fail
- cs/, dev/ 노트: lazy fallback 적용, wiki content 15필드 검사는 면제
- source/raw 페이지의 `last_verified` 누락은 `evergreen`과 무관하게 hard-fail한다. 값이 있으면 모든 페이지에 age ≥180일 warning을 적용하고, concept의 `evergreen: true`만 age ≥730일 hard-fail을 면제한다. 현행 `lint.py`의 evergreen early return은 이 범위를 초과하는 알려진 spec drift이며 target checker 전환에서 제거한다.

## 참고

- 결정 출처: panel-debate A C3 (provenance 외부 인덱스) + B B1 (재현성·시의성 축) + B B6 (lint pass 0/1)
