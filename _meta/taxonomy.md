# Taxonomy — Controlled Vocabulary

본 문서는 tag 와 entity·concept 명칭의 controlled vocabulary 를 정의한다. wiki/ 페이지의 모든 tag·entity 명칭은 본 목록에서만 선택.

## 갱신 워크플로우 (Panel B B7)

| 변경 | 절차 |
|---|---|
| 신규 vocab 추가 | PR 1개 — taxonomy.md 수정 + 사람 review |
| vocab supersede (예: foundation → frontier) | ADR + `alias:` 필드 추가 (frontmatter + taxonomy.md 양쪽, taxonomy.md canonical). 자동 일괄 치환 금지 |
| vocab 삭제 | ADR + 1주 deprecation window + alias redirect |

## Tag 목록 — LLM/AI 도메인

### 아키텍처 (architecture)

- `transformer`
- `attention` (alias: `self-attention`)
- `mixture-of-experts` (alias: `moe`)
- `sparse-models`
- `dense-models`
- `state-space-models` (alias: `ssm`, `mamba`)
- `diffusion-models`
- `autoregressive`
- `encoder-decoder`
- `decoder-only`

### 훈련 (training)

- `pretraining`
- `post-training`
- `instruction-tuning` (alias: `sft`, `supervised-fine-tuning`)
- `rlhf`
- `dpo`
- `rlaif`
- `lora`
- `qlora`
- `continual-learning`
- `curriculum-learning`

### 추론 (inference)

- `speculative-decoding`
- `kv-cache`
- `quantization`
- `pruning`
- `distillation`

### Scaling

- `scaling-laws`
- `chinchilla-scaling`
- `emergent-abilities`
- `compute-optimal`

### Evaluation

- `benchmark`
- `mmlu`
- `humaneval`
- `mt-bench`
- `lm-eval-harness`
- `holistic-evaluation` (alias: `helm`)

### Safety / Alignment

- `alignment`
- `constitutional-ai` (alias: `cai`)
- `red-teaming`
- `jailbreak`
- `prompt-injection`
- `hallucination`
- `refusal`

### Infrastructure

- `vllm`
- `sglang`
- `tgi` (alias: `text-generation-inference`)
- `tensorrt-llm`
- `ollama`
- `transformers-library`

### Agents

- `agent`
- `tool-use`
- `function-calling`
- `mcp` (alias: `model-context-protocol`)
- `react-pattern`
- `chain-of-thought` (alias: `cot`)

### Concepts (general)

- `in-context-learning` (alias: `icl`)
- `few-shot`
- `zero-shot`
- `chain-of-thought`
- `prompt-engineering`

## Entity 목록 (LLM/AI 영역)

(초기 시드 — 최소 핵심. 신규 entity 추가 PR 로 확장)

### Organizations

- `openai`
- `anthropic`
- `google-deepmind` (alias: `deepmind`, `google-ai`)
- `meta-ai` (alias: `fair`)
- `mistral-ai`
- `cohere`
- `hugging-face`
- `vercel`

### Models (frontier — 2026-05 기준)

- `gpt-5` (alias: `gpt-5.1`, `gpt-5.2`, `gpt-5.5`)
- `claude-opus-4-7`
- `claude-sonnet-4-6`
- `claude-haiku-4-5`
- `gemini-2`
- `llama-4`
- `mixtral-8x7b`
- `mixtral-8x22b`
- `qwen-2.5`

### Foundational papers (evergreen)

- `attention-is-all-you-need` (Vaswani et al. 2017)
- `bert` (Devlin et al. 2018)
- `gpt-2` (Radford et al. 2019)
- `gpt-3` (Brown et al. 2020)
- `chinchilla` (Hoffmann et al. 2022)
- `instructgpt` (Ouyang et al. 2022)
- `lora-paper` (Hu et al. 2021)

## CS 도메인 별 vocabulary (보안 / 암호 / 네트워크 등)

cs/ 영역은 wiki/ 합성 진입 후 본 taxonomy 에 별도 섹션 추가. 현재 wiki/domains/ 가 llm-* 6개만 있으므로 다음 PR 에서 확장:
- `wiki/domains/information-security/` 진입 시 보안 vocab 신설
- `wiki/domains/cryptography/` 진입 시 암호 vocab 신설
- `wiki/domains/network/` 진입 시 네트워크 vocab 신설

## Alias 메커니즘

alias 는 같은 개념의 다른 표기를 동일 entity 로 redirect. taxonomy.md canonical, frontmatter `tags:` 는 canonical 만 사용.

예: `tags: [self-attention]` 금지. `tags: [attention]` 만 허용 (canonical).

LLM 이 alias 어휘 사용 시 lint.py 가 자동 변환 또는 warn.

## 검증

`scripts/lint.py` 가 wiki/ 페이지의 tags · entity 인용 전수 check. taxonomy 미등재 vocab 사용 시 hard-fail.

## 참고

- 결정 출처: panel-debate B B7 (vocabulary 갱신 워크플로우)
- 초기 시드는 2026-05-20 기준. dogfood 후 확장.
