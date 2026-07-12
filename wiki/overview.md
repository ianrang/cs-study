# Overview

본 페이지는 wiki/ 의 도메인 지도이자 최상위 entry point. AI 에이전트와 사람 모두 본 페이지를 먼저 read.

## 도메인 카탈로그

### LLM / AI

- `wiki/domains/llm-foundations/` — 트랜스포머·MoE·scaling laws (inactive, 예정)
- `wiki/domains/llm-prompting/` — 프롬프트 엔지니어링·few-shot·CoT (inactive, 예정)
- `wiki/domains/llm-agents/` — 에이전트 아키텍처·MCP·tool use (inactive, 예정)
- `wiki/domains/llm-evaluation/` — 벤치마크·HELM·MT-Bench (inactive, 예정)
- `wiki/domains/llm-infrastructure/` — vLLM·SGLang·TGI·Ollama (inactive, 예정)
- `wiki/domains/llm-safety/` — alignment·red-teaming·jailbreak (inactive, 예정)

### CS / 보안 / 개발 (cs/, development/ 의 wiki 합성 영역 — 진입 시 신설)

- 정보보안 (`wiki/domains/information-security/` — active. `cs/information-security/` 인용)
- 암호 (`wiki/domains/cryptography/` — 예정)
- 네트워크 (`wiki/domains/network/` — 예정)
- 소프트웨어 엔지니어링 (`wiki/domains/software-engineering/` — 예정. `development/software-engineering/`, `development/architecture/` 인용)
- AI 산업·하네스 (`wiki/domains/ai-engineering/` — 예정. development/ai-industry/, development/harness/ 인용)

## 도메인 추가 절차

1. `_meta/domains.yaml`에 domain과 active/inactive 상태 등록
2. `wiki/domains/<domain>/` 디렉토리 생성
3. `wiki/domains/<domain>/overview.md` 작성 (concept page 형식)
4. 실제 overview가 생성된 뒤 본 페이지에 link 추가
5. controlled vocabulary가 필요하면 `_meta/taxonomy.md`에 domain-specific vocab 섹션 추가

## Global

도메인 2개 이상에서 reuse 되는 entity / concept 만:

- `wiki/global/entities/` (현재 비어 있음)
- `wiki/global/concepts/` (현재 비어 있음)

## 카테고리

- [[wiki/index]] — 모든 active 페이지 카탈로그
- [[wiki/log]] — 모든 변경 시간순 로그
- `wiki/staging/domain-review/` — 도메인 분류 미정 staging
- `wiki/archive/` — merged / demoted 페이지

## 운영 규약

- [[AGENTS.md]] — LLM 운영 schema
- [[_meta/quality-bar]] — 6축 명제
- [[_meta/page-type-spec]] — page_type 표준 섹션
- [[_meta/frontmatter-spec]] — wiki content frontmatter 15 필드
- [[_meta/taxonomy]] — controlled vocabulary

## 진행 현황

- vault scaffold 완료: 2026-05-20
- 첫 ingest: (대기 중)
- dogfood 시작: (대기 중)

자세한 변경 이력: [[wiki/log]]
