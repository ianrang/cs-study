# Frontmatter Spec

본 문서는 등급 별 frontmatter 필수·선택 필드를 정의한다.

## wiki/ 페이지 (synthesis 등급) — 14 필드

```yaml
---
title: "Mixture of Experts (MoE)"            # 필수
tier: llm-synthesis                            # 필수 enum: raw | human-note | llm-synthesis
page_type: concept                             # 필수 enum: concept | entity | comparison | benchmark | dataset | method
domain: llm-foundations                        # 필수 — wiki/domains/<domain>/
domain_confidence: high                        # 필수 enum: high | medium | low (low → staging/domain-review)
shared_scope: domain                           # enum: domain | global (global 은 2 도메인 이상 reuse 만)
tags: [architecture, sparse-models, scaling]   # taxonomy.md controlled vocabulary 만
status: active                                 # enum: active | staged | archived
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
ingested_date: 2026-05-20
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
provenance: extracted # 사람 직접 작성
```

사용자가 의도적으로 frontmatter 추가 시 lazy 추정값을 override.

## Source 페이지 — source summary 페이지 추가 필드

wiki/domains/<domain>/sources/ 에 생성되는 source summary 페이지는 위 14 필드 + 다음 추가:

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

- wiki/ 페이지: 14 필드 hard-fail
- raw/ 페이지: 최소 6 필드(lint.py `RAW_REQUIRED_FIELDS`) hard-fail
- cs/, dev/ 노트: lazy fallback 적용 (검증 면제)
- 모든 페이지 `last_verified` 임계 검증 (재현성·시의성 축)

## 참고

- 결정 출처: panel-debate A C3 (provenance 외부 인덱스) + B B1 (재현성·시의성 축) + B B6 (lint pass 0/1)
