# Log

wiki/ 의 모든 변경 시간순 기록. append-only. 각 entry prefix = `## [YYYY-MM-DD] operation | title`. 본 형식은 unix tool parseable.

## [2026-05-20] init | LLM Wiki scaffold v3

- Panel-debate A/B/C (3 안건, R=2, 도메인 특화 페르소나) 종결 후 설계 v3 적용
- 생성 파일:
  - AGENTS.md (LLM 운영 schema, scope 분리 B0 명문화)
  - _meta/llm-config.yaml (profile/model alias, fallback chain, daily_call_cap)
  - _meta/quality-bar.md (6축 + AGENTS.md directive, raw/wiki 차등 적용)
  - _meta/page-type-spec.md (concept/entity/comparison/benchmark/dataset/method enum + 표준 섹션 매트릭스)
  - _meta/frontmatter-spec.md (wiki 14 필드 + raw 4 필드 + lazy fallback)
  - _meta/taxonomy.md (LLM/AI 도메인 controlled vocabulary 초기 시드)
  - _meta/defaults.yaml (cs/, development/ 등 lazy fallback 추정값)
  - scripts/lint.py (6축 자동 검증 skeleton)
  - scripts/llm_config.py (LLMResolver — resolve/fallback_chain/invalidate_cache)
  - scripts/commit_wiki.sh (swan-bot author + [wiki-bot] prefix + read-only 영역 차단)
  - .claude/templates/adr-llm-swap.md (7-step 모델 교체 ADR 템플릿)
  - wiki/templates/ (6 page-type templates)
  - wiki/{overview,index,log}.md (초기 stub)
- 폴더 신설: raw/sources/{papers,web,conversations,urls}/, raw/assets/, wiki/{global,staging/domain-review,archive,templates,domains/llm-*/{sources,entities,concepts,queries}}, _meta/, scripts/, .claude/templates/
- 기존 폴더 (cs/, development/, coding-test/, lang/, tools/) 무변경
- Panel-debate 세션 로그: ~/.claude/panel-debate/20260520-{132625,134649,140056}-llm-wiki-{A,B,C}/

---

**Log 형식 규약**:
- prefix: `## [YYYY-MM-DD] operation | title`
- operation enum: `init | ingest | query | lint | wiki-sync | adr | refactor | archive`
- 본문: 변경 사실만. AI/Claude/도구명 금지 (project CLAUDE.md 따름)
- append-only — 기존 entry 수정 금지
