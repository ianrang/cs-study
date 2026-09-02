# PRD: cs-study raw→wiki ingest 후처리 (1차 — video 결정적 importer)

> **상태: Superseded.** 2026-08-23 immutable ArtifactBundle capture가 `scripts/wiki_ingest.py` 단일 진입점으로 전환되면서 본 v1 pair/force 계약은 historical non-normative가 됐다. 현재 계약은 `docs/wiki-ingest-prd.md`가 소유한다.

> 범위 한정: 본 PRD는 **1차 라운드 = canonical JSON → cs-study `raw/sources/video/` 결정적 importer** 만 다룬다.
> LLM 교정·구조화·wiki 합성(synthesis)은 **2차 라운드로 이연**한다(§5, §9). 본 라운드 실행 경로에 LLM 없음.
>
> **인용 경로 범례**: cs-study 파일은 `~/dev/personal/001_cs-study/` 기준 — `lint.py`·`llm_config.py`=`scripts/`, `frontmatter-spec.md`·`quality-bar.md`·`taxonomy.md`·`defaults.yaml`·`llm-config.yaml`=`_meta/`, `AGENTS.md`=루트. 추출기 파일은 `~/dev/personal/007_youtube-script/` 기준 — `domain.py`·`pipeline.py`=`src/ytscript/`, `doc_hook.py`=`src/ytscript/hooks/`, `default.md.j2`=`templates/`.

> **기준선 수명**: 본문의 “현재/현행/실측”은 이 v1 설계 작성 당시 기준선이며 2026-08-21 current inventory가 아니다. 당시 `scripts/ingest.py`는 존재하고 실행 기준선으로 사용됐다. current evidence baseline은 `docs/wiki-ingest-review.md` §2, aggregate verdict는 같은 문서 §9가 소유하며, 이 문서에서 날짜와 근거를 명시한 구현 상태는 그 verdict의 evidence snapshot일 뿐 별도 판정 owner가 아니다. 본 문서의 v1 요구는 2026-08-23 `docs/wiki-ingest-prd.md`에 의해 superseded됐다.

## 1. 개요

### 문제 정의
- v1 설계 작성 당시 YouTube 추출기(`~/dev/personal/007_youtube-script`)는 영상 → 자막/STT → **canonical JSON + MD** 를 산출했지만(`domain.py:85-109` 당시 위치), cs-study 위키로 합류시키는 **ingest 실행 계층이 부재**했다(`scripts/ingest.py` 당시 실측 0건; 당시 `AGENTS.md:46-57`은 ingest 순서만 규정). 이 line citation은 current 줄 의미를 주장하지 않는다.
- 추출기 MD frontmatter(`templates/default.md.j2`)는 cs-study raw 필수 필드와 **불일치**: `tier`·`last_verified`·`ingested_date` 누락, `extracted_at`↔`last_verified` 이름 상이. → 누군가 필드 변환을 담당해야 함.
- raw `source_type: video`(frontmatter-spec.md:36) enum 은 존재하나 디스크 위치(`raw/sources/video/`)가 미생성(실측 폴더 `papers/web/conversations/urls` 4종뿐).
- raw verbatim 본문이 model명("GPT-5" 등)을 합법 인용하면 `lint.py` model_id directive(lint.py:44-48,233)가 hard-fail → ingest 차단(이연 충돌, memory:21).

### 대상 사용자
- 주: 사용자(swan) — 학습 영상을 cs-study 위키 raw 자료로 적재.
- 보조: cs-study의 LLM 에이전트(2차 synthesis 라운드에서 본 raw를 source로 소비).

### 핵심 가치
- 추출기 산출물을 **규칙·원칙을 모두 만족하는 cs-study raw 페이지**로, **중복·순환의존 없이**, **원본 충실도(verbatim) 보존**하며 결정적으로 적재.

### 프로젝트 유형
- brownfield (기존 cs-study 스키마 + 기존 추출기 위에 신규 importer 추가).

## 2. 기능 요구사항

| ID | 요구사항 | 수용 기준 | 우선순위 |
|----|---------|----------|---------|
| FR-1 | importer는 **명시적 입력 경로**(canonical JSON 파일 또는 `out/<id>/` 디렉토리)를 인자로 받아 ingest한다. out_dir 전체 스캔 금지. | `ingest.py <path>` 형태로 단일 대상 처리. 경로 미존재 시 명확한 오류. | Must |
| FR-2 | 동일 `out/<id>/`에 여러 variant가 존재하면 **best variant 1개**만 선택한다. 우선순위 `manual > auto_sub > stt`, 동률 시 `extracted_at` 최신. | variant 2개 이상 입력 시 우선순위표대로 정확히 1개 선택. 결정적(동일 입력→동일 선택). | Must |
| FR-3 | 영상당 cs-study raw 페이지는 **정확히 1개** 생성한다. 파일명 = `raw/sources/video/<video_id>.md`. | 동일 `video_id` 재실행 시 페이지 수 1 유지(변형 파일 미생성). | Must |
| FR-4 | canonical JSON → raw frontmatter **필드 매핑**을 결정적으로 수행한다(§매핑표). | `title/source_url/source_date/source_type/last_verified/ingested_date/tier` 7개 키가 모두 존재한다. upload_date가 null일 때만 `source_date: ""`를 허용한다. `tier: raw`, `source_type: video`. | Must |
| FR-5 | 본문은 **verbatim 보존**한다 — `full_text` + 타임스탬프 segments 를 LLM 교정 없이 그대로 기록. | 산출 본문이 canonical `full_text`/`segments` 와 문자 단위 일치. | Must |
| FR-6 | canonical JSON 원본을 cs-study 내로 **복사 보관**한다(`raw/sources/video/<video_id>.json`). | raw .md 와 동일 디렉토리에 canonical 원본 존재. 교차 repo 경로 참조 0. | Must |
| FR-7 | 멱등성: 대상 raw 페이지가 이미 존재하면 **skip**, `--force` 에만 재생성. | 재실행 시 기본 skip(덮어쓰기 0). `--force` 시에만 갱신. 추출기 pipeline.py:111 과 동일 의미. | Must |
| FR-8 | 트랜잭션 경계: raw `.md` + `.json` 두 산출물은 **부분 산출물 0** 으로 커밋된다. | 둘째 쓰기 실패 시 첫째 롤백 → `.md` 만/`.json` 만 남는 상태 불가. 추출기 pipeline.py:55-81 패턴 정합. | Must |
| FR-9 | 산출 raw가 **`scripts/lint.py` 통과**(HIGH 0)하고, lint.py가 **raw 필수필드를 실제 강제**하도록 `RAW_REQUIRED_FIELDS`(6개, lint.py:64) 체크를 구현한다(frontmatter-spec.md:115 spec 완성). | `python3 scripts/lint.py --paths raw/sources/video/<id>.md` → HIGH=0. 필수필드 누락 raw는 hard-fail. | Must |
| FR-10 | **ADR-001** — 페이지 본문 model_id/자기추론 grep 규칙 **폐기**(raw·wiki 공통). model_id alias 규율은 LLM 호출 site·프롬프트에만 유지. | 페이지 본문(raw·wiki)의 모델명이 lint HIGH를 유발하지 않음. taxonomy 모델 entity(taxonomy.md:118-126)와 정합. 나머지 lint(last_verified/broken link 등)는 유지. | Must |
| FR-11 | **ADR-002** — `raw/sources/video/` 폴더 신설 + AGENTS.md:24 폴더 목록·frontmatter-spec 정합. | AGENTS.md raw 폴더 목록에 `video` 등재. source_type:video ↔ 폴더 일치. | Must |
| FR-12 | importer는 **단방향**: cs-study가 추출기 canonical 포맷을 읽는다. 추출기는 cs-study를 모른다(doc_hook no-op 유지). | importer 코드가 추출기 모듈을 import하지 않음. 추출기 무변경. | Must |
| FR-13 | **LLM seam 정의**(실행 아님): 2차 synthesis 라운드가 본 raw를 입력으로 plug-in 할 핸드오프 지점을 문서화. | arch 문서에 seam 명시. 본 라운드 실행 경로에 LLM 호출 0. | Should |

### canonical JSON → raw frontmatter 매핑표 (FR-4)

| raw 필드 | 출처 (canonical) | 변환 | 근거 |
|---|---|---|---|
| `title` | `video.title` | 그대로(null→`video.id`) | frontmatter-spec.md:33 |
| `source_url` | `video.url` | 그대로 | frontmatter-spec.md:34 |
| `source_date` | `video.upload_date` | `YYYY-MM-DD` 그대로 | domain.py:43 주석 |
| `source_type` | 상수 `video` | `domain.py:15 MEDIA_TYPE` | frontmatter-spec.md:36 |
| `last_verified` | `extraction.extracted_at` | ISO datetime → date | domain.py:54 주석, lint.py:159-161 |
| `ingested_date` | importer 실행일 | UTC date | frontmatter-spec.md:38 |
| `tier` | 상수 `raw` | — | frontmatter-spec.md:40 |
| `extraction_method` | `extraction.method` | provenance 보조 | default.md.j2:9 |
| `stt_model`/`stt_engine` | `extraction.model`/`engine` | method=stt 시만 | default.md.j2:10-11 |
| `channel`/`duration_seconds`/`language` | `video.*` | provenance 보조 | default.md.j2:6-8 |

## 3. 비기능 요구사항

| ID | 요구사항 | 기준 |
|----|---------|------|
| NFR-1 | **단방향 의존**: 순환·양방향 참조 0. importer→추출기 canonical 포맷 단방향. | arch-cycle-detector 0건. importer가 추출기 import 0. |
| NFR-2 | **결정성**: 동일 입력 → 동일 산출(파일명·필드·본문). LLM·시계·랜덤 비결정 요소 격리. | `ingested_date`/`last_verified` 외 모든 산출 결정적. |
| NFR-3 | **LLM 호출 규약**: API 금지, Claude Code/Codex CLI 세션만. model_id 직접 인용 금지(profile alias). | 본 라운드 LLM 0. 2차 라운드는 `ingest` alias(_meta/llm-config.yaml:11) + CLI 세션. (Claude 메모리 `llm-call-cli-not-api`) |
| NFR-4 | **원본 충실도**: raw 본문 무수정(verbatim). 교정본은 raw에 쓰지 않음. | AGENTS.md:24/31 "원본 불변" 위반 0. |
| NFR-5 | **자기 코드 호출 깊이**: 신규 importer 직렬 체인 함수 5개 미만(= edge 4 미만), edge 4 이상은 설계 경고. | arch-layer-depth 임계 내. |
| NFR-6 | **스키마 변경 게이트**: `_meta/`·`scripts/`·AGENTS.md 변경은 ADR + 사용자 승인. | ADR-001/002 승인 후에만 스키마 edit. |
| NFR-7 | **사람 review 게이트**: raw→wiki 승격은 사람 필수(본 라운드는 raw까지라 승격 미발생). | AGENTS.md:85-91 정합. |

## 4. 에픽

### Epic 1: 스키마 공진화 (ADR)
- 의존성: 없음 (다른 에픽의 선행 — lint/폴더가 importer 산출의 통과 조건)
- 스토리:
  - 1.1 ADR-001 작성·승인 — 페이지 본문 model_id/자기추론 grep 폐기(raw·wiki) + lint.py 정정 + taxonomy 모순 해소
  - 1.2 ADR-002 작성·승인 — `raw/sources/video/` 신설 + AGENTS.md/frontmatter-spec 정합

### Epic 2: 결정적 video importer
- 의존성: Epic 1 (산출물이 lint 통과하려면 ADR-001 필요)
- 스토리:
  - 2.1 입력 해석 + best-variant 선택 (FR-1, FR-2)
  - 2.2 canonical→frontmatter 매핑 + verbatim 본문 렌더 (FR-4, FR-5)
  - 2.3 atomic 산출(.md + .json 복사) + 멱등 (FR-3, FR-6, FR-7, FR-8)
  - 2.4 lint raw-필수필드 강제 체크 구현 + 산출물 lint 통과 + 단방향 의존 보장 (FR-9, FR-12)

### Epic 3: LLM synthesis seam (이연 — 문서만)
- 의존성: Epic 2
- 스토리:
  - 3.1 2차 라운드 핸드오프 지점 문서화 (FR-13) — 실행 없음

## 5. MVP 범위
- **포함**: Epic 1 (ADR 2건), Epic 2 (결정적 importer 전체), Epic 3.1 (seam 문서).
- **제외 (2차 라운드 이연)**:
  - LLM 교정(구두점·용어·문단·소제목) 및 corrected 레이어 산출.
  - domain 분류(low confidence → staging) — raw는 domain 불요(lint.py:64 raw 필드에 domain 없음).
  - wiki/domains 합성 페이지(concept/entity/source summary) 생성.
  - software-engineering 등 video 대응 wiki 도메인 신설(v1 설계 작성 당시 inventory는 llm-* 6개; current inventory 아님).
  - raw→wiki 승격 사람 review 게이트(승격이 본 라운드에 미발생).

## 6. 기술 제약
- 입력: 추출기 canonical JSON v`1.0`(`SCHEMA_VERSION`, domain.py:12).
- 출력: cs-study `raw/sources/video/<video_id>.{md,json}`. Python(uv) 단일 스크립트(`scripts/ingest.py`).
- v1 구현 evidence snapshot(2026-08-21, current aggregate verdict 입력): `scripts/lint.py`가 raw 필수필드(`RAW_REQUIRED_FIELDS` 6개)를 강제한다. 작성 당시 premortem의 미호출 skeleton은 구현으로 해소됐고, frontmatter spec과 lint의 필수필드 6개 집합만 동일하다. raw enum을 포함한 다른 규칙의 완전성은 주장하지 않는다.
- 스키마 변경(ADR-001/002)은 사용자 승인 후.
- LLM: 본 라운드 0. 향후 Claude Code/Codex CLI 세션만(API 금지).

## 7. 검증 결과 (자체)

| 항목 | 상태 |
|------|------|
| 완전성 (모든 FR 수용기준 보유) | PASS |
| 일관성 (FR 간 모순) | PASS |
| 추적성 (FR→에픽 매핑) | PASS (FR-1~9,12→E2 / FR-10,11→E1 / FR-13→E3) |
| 범위 (MVP 외 기능 미포함) | PASS (LLM·wiki 합성 명시 제외) |
| 의존성 (에픽 순서) | PASS (E1→E2→E3) |

## 8. Premortem 결과 (Phase 2.5)

| 차원 | 발견 허점 | 사용자 결정 | FR/NFR 갱신 |
|------|----------|-----------|-------------|
| 암묵 가정 | importer 입력 발견 방식 미정 / canonical 원본 보관 위치 | 명시적 경로 인자 + canonical JSON cs-study 내 복사 보관 | FR-1, FR-6 |
| 암묵 가정 | lint.py가 raw 필드를 실제 강제한다고 가정 | 정정: 현재 lint.py:64 RAW_REQUIRED_FIELDS 미호출(skeleton). **본 작업에서 강제 체크 구현** + spec wording 4→6 정합 | FR-9, §6 |
| 엣지 케이스 | 동일 영상 다중 variant 누적 | 영상당 1개 + best-variant(manual>auto_sub>stt, 동률 extracted_at 최신) | FR-2, FR-3 |
| 엣지 케이스 | `.md`/`.json` 부분 산출물 | atomic 트랜잭션(둘째 실패 시 롤백) | FR-8 |
| 엣지 케이스 | `video.title`/`upload_date`/`channel` null | title null→video.id fallback. `source_date` 키는 항상 존재하되 upload_date null이면 값 `""`; channel 등 선택 보조 필드는 null이면 빈 값 | FR-4 매핑표 |
| 모호성 | "ingest"가 wiki 합성까지 포함하는지 | 1차=raw까지만, LLM 교정·합성 이연 | §1 범위, §5 |
| 모호성 | 파일명에 식별자/날짜 인코딩 | `<video_id>.md`(전역 고유·불변). 추출 메타는 frontmatter 단일진실 | FR-3 |
| 충돌 | model_id directive(본문 grep) ↔ verbatim 원본보존(축3) **및 taxonomy 모델 entity(taxonomy.md:118-126)** | ADR-001 본문 grep 규칙 폐기(raw·wiki). alias 규율은 LLM 호출 site 유지 | FR-10, NFR-6 |
| 충돌 | 추출기 1파일 강제 ↔ 단방향 의존 | 추출기 범용 유지, 선택은 importer 소유 | FR-2, FR-12, NFR-1 |
| 충돌 | LLM 교정 ↔ raw 원본 불변 | 교정본은 raw에 미기록(2차 wiki synthesis 영역) | NFR-4, §5 |

## 9. 이연 항목 (2차 라운드 — 별도 PRD)
- LLM 교정·구조화(Claude Code/Codex CLI 세션, `ingest` profile) → corrected/wiki 산출.
- domain 분류 → `wiki/staging/domain-review/` low-confidence 경로(AGENTS.md:52).
- wiki/domains 합성(7단계 ingest 순서, AGENTS.md:50-57) + 6축 quality-bar 전수 + 사람 승격 게이트.
- video 대응 wiki 도메인(software-engineering 등) 신설 + taxonomy 확장(taxonomy.md:140-143).

## 참고
- 분석 근거: AGENTS.md, `_meta/{frontmatter-spec,page-type-spec,quality-bar,taxonomy,defaults}`, `scripts/lint.py`, 추출기 `domain.py`/`pipeline.py`/`templates/default.md.j2`.
- 결정 출처: 사용자 게이트(2026-06-04) — 교정정책·산출타깃·연결방향·ADR방향·variant선택·파일명.
