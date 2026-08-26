# Page Type Spec

본 문서는 wiki 페이지 type enum 과 각 type 별 표준 섹션·순서를 정의한다. Panel-debate B (2026-05-20) 합의.

## Enum

| type | 정의 | 예시 |
|---|---|---|
| `concept` | 기술·아이디어·메커니즘·이론 | Mixture of Experts, RLHF, Attention |
| `entity` | 회사·인물·모델·제품 | OpenAI, Mistral AI, GPT-4, Anthropic |
| `comparison` | A vs B / 평가 매트릭스 | MoE vs Dense, RLHF vs DPO vs RLAIF |
| `benchmark` | 벤치마크·데이터셋·평가 도구 | MMLU, HumanEval, MT-Bench |
| `dataset` | 학습·평가용 데이터셋 | The Pile, Common Crawl, LAION |
| `method` | 알고리즘·기법·훈련 방법 | LoRA, QLoRA, Speculative Decoding |

frontmatter `page_type: <enum>` 필수.

## 표준 섹션 매트릭스 — 섹션 순서 고정 (Editor)

### concept

```markdown
[1-2 문장 summary]

## Definition
[개념의 본질 1-2 문단]

## Mechanism
[작동 원리. 다이어그램 권장 (mermaid)]

## Variants
[변형·확장·관련 기법. 표 또는 불릿]

## Trade-offs
[장단점·적용 조건]

## Open Questions
[미해결 모순·후속 조사 주제]

## Sources
[source_paths frontmatter 의 narrative 인용]
```

### entity

```markdown
[1-2 문장 summary]

## Overview
[entity 의 본질·역할 1 문단]

## Products / Outputs
[표 또는 불릿 — 모델·논문·도구 등]

## Timeline
[연혁·주요 마일스톤. 표 권장 (date / event)]

## Relationships
[관련 entity (parent/subsidiary/collaboration). [[wikilink]]]

## Sources
[narrative 인용]
```

### comparison

```markdown
[1-2 문장 summary — 무엇을 비교하는가]

## Comparison Table
[표 — 항목 × 후보 × 결과]

## Trade-offs
[각 후보의 장단점]

## When to Use
[적용 조건·결정 기준]

## Open Questions
[비교 한계·미해결 영역]

## Sources
[narrative 인용]
```

### benchmark

```markdown
[1-2 문장 summary]

## Definition
[benchmark 의 목적·평가 영역]

## Methodology
[측정 방법·데이터·metric]

## Leaderboard
[최신 SOTA 결과. 표 권장]

## Limitations
[benchmark 자체의 한계·비판]

## Sources
[narrative 인용]
```

### dataset

```markdown
[1-2 문장 summary]

## Overview
[데이터셋 출처·규모·라이선스]

## Schema / Composition
[필드·예시·통계]

## Usage
[학습·평가·연구 활용 예]

## Limitations / Biases
[데이터 편향·noise]

## Sources
[narrative 인용]
```

### method

```markdown
[1-2 문장 summary]

## Definition
[기법의 본질 1-2 문단]

## Algorithm
[단계·pseudo-code·수식]

## Implementation
[구현 노트·라이브러리·예시 코드]

## Trade-offs
[장단점·적용 조건]

## Open Questions
[미해결·후속 연구]

## Sources
[narrative 인용]
```

## 검증 (lint.py grep)

각 page_type 별 표준 섹션 (level-2 heading `## `) 전수 존재 확인. 일반 누락은 soft-warn이다. 단, `provenance: ambiguous` 페이지의 `Open Questions` 누락은 충돌 표시 요건 위반이므로 HIGH hard-fail이다.

섹션 *순서* 도 위 매트릭스 순서대로 강제. 순서 위반 시 soft-warn.

## evergreen 플래그

foundational paper (예: Transformer 2017 - "Attention Is All You Need") 는 frontmatter `evergreen: true` 명시 시 재현성·시의성 축 age ≥730일 hard-fail 임계 면제. concept type 한정.

## 비교 — 기존 cs/, development/ 노트

본 spec 은 **승격된 wiki content 페이지**에 적용한다. `wiki/domains/<domain>/drafts/`의 작업 초안은 frontmatter `page_type`을 승격 후보 분류로만 기록하며, 표준 섹션·순서 검사는 승격 시 수행한다. cs/, development/, coding-test/, lang/, tools/ 노트는 본 spec 무시 (사람 자유 작성).

## 참고

- 결정 출처: panel-debate B B2 (page_type enum + 표준 섹션 매트릭스)
- 섹션 순서 고정: Editor 페르소나 권고
