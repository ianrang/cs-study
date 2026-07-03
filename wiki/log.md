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

## [2026-07-03] ingest | 정보보안기사 실기 28~30회 복원 데이터셋

- 생성: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/index.md`
- 생성: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/2025-01-practical-28.md`
- 생성: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/2025-02-practical-29.md`
- 생성: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/2025-04-practical-30.md`
- 원천: Jaesung Tistory 정보보안 기사 카테고리 1~8페이지 중 명시적 실기 문제 복원 글 3건
- 검증: KCA/KCQ 2023~2026 출제기준 PDF, round-1 과목별 노트, 외부자료 검증 체크리스트로 개념 단위 교차 확인
- 주의: 공식 실기 원문 미공개로 원문 문장 동일성은 보장하지 않고, 문제 요지와 정답 중심으로 재구성

---

## [2026-07-03] ingest | 소프트웨어 개발보안 가이드 공식 원천 패칭

- 생성: `raw/sources/web/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.md`
- 저장: `raw/assets/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.pdf`
- 갱신: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/reference-source-index.md`
- 갱신: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/reference-patching-review.md`
- 갱신: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/analysis-roadmap-todo.md`
- 갱신: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/exam-criteria-and-reference-catalog.md`
- 검증: KISA 공식 상세 페이지 `postSeq=5`, 다운로드 패턴 `menuSeq=2060204&postSeq=5&attachSeq=1`, SHA-256 `fcd8c4343f5f3ec0d7a1beda7ba4a6f86b67f5d6267664241fb66f6710ca0407`, `pdftotext` 성공
- 주의: 행안부 보조 게시글의 검색 노출 직접 첨부 `FILE_000000000046958`은 8쪽짜리 2013 PDF라 원천 asset으로 사용하지 않음

---

## [2026-07-03] ingest | 정보보안기사 실기 28~30회 문항-근거 매핑

- 생성: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/item-reference-map.md`
- 범위: 28회, 29회, 30회 총 54개 문항
- 갱신: `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/analysis-roadmap-todo.md`
- 연결 기준: KCA 실기 출제기준 세부항목, 패칭 완료 참고문서 ref_id, 회차별 복원 문항의 짧은 evidence
- 주의: 23~27회는 남은 분류 finding 보정 후 같은 스키마로 확장

---

**Log 형식 규약**:
- prefix: `## [YYYY-MM-DD] operation | title`
- operation enum: `init | ingest | query | lint | wiki-sync | adr | refactor | archive`
- 본문: 변경 사실만. AI/Claude/도구명 금지 (project CLAUDE.md 따름)
- append-only — 기존 entry 수정 금지
