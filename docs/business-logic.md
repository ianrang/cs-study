# Business Logic: video importer (`scripts/ingest.py` — 1차)

> **상태: Superseded.** 2026-08-23 immutable capture 전환으로 본 규칙은 historical non-normative가 됐다. 활성 artifact 규칙은 `docs/wiki-ingest-business-logic.md`가 소유한다.

> 대상: `docs/prd.md` + `docs/architecture.md`. 본 문서는 **규칙 명제·일관성**만 다룬다(구조·패턴은 architecture.md).
>
> **인용 경로 범례**: cs-study 파일은 `~/dev/personal/001_cs-study/` 기준(`lint.py`=`scripts/`, `*-spec.md`·`quality-bar.md`·`taxonomy.md`·`llm-config.yaml`=`_meta/`, `AGENTS.md`=루트). 추출기 파일은 `~/dev/personal/007_youtube-script/` 기준(`domain.py`·`pipeline.py`=`src/ytscript/`, `doc_hook.py`=`src/ytscript/hooks/`, `default.md.j2`=`templates/`).

## 1. 도메인 개념

### 용어 사전
| 용어 | 정의 |
|------|------|
| canonical JSON | 추출기 산출 표준 포맷 v1.0 (`domain.py:85-109 to_canonical`). importer 입력 계약 |
| variant | 한 영상의 한 추출 결과. `<method>.<variant>`(추출기 pipeline.py:45-52). method∈{manual,auto_sub,stt} |
| best variant | 한 영상의 여러 variant 중 importer가 채택할 1개(우선순위 P-SEL-1) |
| raw 페이지 | cs-study `raw/sources/video/<video_id>.md` — verbatim 1차 자료(AGENTS.md:24) |
| verbatim | LLM 교정 없는 원문 그대로(NFR-4, AGENTS.md:31 "본문 무수정") |
| directive | lint.py가 강제하는 AGENTS.md 규약(model_id 인용 금지 등, lint.py:179-204) |

### 엔티티
| 엔티티 | 설명 | 식별자 |
|--------|------|--------|
| RawPage | importer 산출 단위(architecture.md §4) | `video_id` (canonical `video.id`) |

### 값 객체 (VO)
| VO | 속성 | 설명 |
|----|------|------|
| Frontmatter | 순서 고정 dict | raw 메타(P-MAP-*) |
| VariantRef | method, variant, extracted_at, path | 선택 후보(P-SEL-*) |

### 도메인 이벤트
| 이벤트 | 트리거 | 설명 |
|--------|--------|------|
| RawPageCommitted | atomic_commit 성공 | `.md`+`.json` 동시 산출(BR-TXN-1) |
| IngestSkipped | 대상 존재 + ¬force | 멱등 skip(BR-IDEM-1) |
| IngestRejected | schema 불일치 / 경로 부재 | exit 1(VR-*) |

## 2. 비즈니스 규칙

### 입력·선택 (SEL)
| ID | 명제 (IF-THEN) | 예외 (UNLESS) | 출처 |
|----|----------------|---------------|------|
| BR-SEL-1 | IF 입력이 canonical JSON 파일 THEN 그 파일 1개를 대상으로 한다 | — | FR-1 |
| BR-SEL-2 | IF 입력이 `out/<id>/` 디렉토리 THEN 내부 canonical JSON들을 후보로 수집한다 | — | FR-1 |
| BR-SEL-3 | IF 후보 ≥2 THEN method 우선순위 `manual > auto_sub > stt` 로 1개 선택한다 | — | FR-2 |
| BR-SEL-4 | IF 동일 최우선 method 후보 ≥2 (예: stt.medium, stt.large) THEN `extracted_at` 최신 1개 선택한다 | — | FR-2 |
| BR-SEL-5 | IF 후보 = 0 THEN IngestRejected(exit 1) | — | FR-1 |

### 필드 매핑 (MAP) — canonical → raw frontmatter
| ID | 명제 (IF-THEN) | 예외 (UNLESS) | 출처 |
|----|----------------|---------------|------|
| P-MAP-1 | THEN `title = video.title` | UNLESS `video.title` is null THEN `title = video.id` | FR-4, frontmatter-spec.md:33 |
| P-MAP-2 | THEN `source_url = video.url` | — | FR-4, frontmatter-spec.md:34 |
| P-MAP-3 | THEN `source_date = video.upload_date`(YYYY-MM-DD) | UNLESS null THEN `source_date = ""`(빈 값) | FR-4, domain.py:43 |
| P-MAP-4 | THEN `source_type = "video"`(상수) | — | FR-4, domain.py:15, frontmatter-spec.md:36 |
| P-MAP-5 | THEN `last_verified = date(extraction.extracted_at)` (ISO datetime→date) | — | FR-4, domain.py:54, lint.py:159-161 |
| P-MAP-6 | THEN `ingested_date = importer 실행 UTC date` | — | FR-4, frontmatter-spec.md:38 |
| P-MAP-7 | THEN `tier = "raw"`(상수) | — | FR-4, frontmatter-spec.md:40 |
| P-MAP-8 | THEN `extraction_method = extraction.method` | — | FR-4, default.md.j2:9 |
| P-MAP-9 | IF `extraction.method == "stt"` THEN `stt_model = extraction.model` AND `stt_engine = extraction.engine` | UNLESS method≠stt THEN 두 필드 생략 | FR-4, default.md.j2:10-11 |
| P-MAP-10 | THEN `channel/duration_seconds/language = video.*` (provenance 보조) | UNLESS null THEN 빈 값 | FR-4, default.md.j2:6-8 |

### 본문 (BODY)
| ID | 명제 (IF-THEN) | 예외 (UNLESS) | 출처 |
|----|----------------|---------------|------|
| BR-BODY-1 | THEN body = canonical `full_text` + 타임스탬프 segments 를 **문자 그대로** 기록 | — | FR-5, NFR-4 |
| BR-BODY-2 | THEN importer는 body에 LLM 교정·요약·구조화를 **적용하지 않는다** | — | FR-5, NFR-4, AGENTS.md:31 |
| BR-BODY-3 | IF `full_text == ""` AND `segments == []` THEN 본문 비어도 산출(거부 아님) — 추출 결과 그대로 | — | 엣지(빈 전사) |

### 산출·멱등·트랜잭션 (IDEM/TXN)
| ID | 명제 (IF-THEN) | 예외 (UNLESS) | 출처 |
|----|----------------|---------------|------|
| BR-IDEM-1 | IF `raw/sources/video/<video_id>.md` 존재 AND ¬force THEN IngestSkipped(exit 0) | — | FR-7, pipeline.py:111 |
| BR-IDEM-2 | IF force THEN 기존 산출물 재생성(덮어쓰기) | — | FR-7 |
| BR-DUP-1 | THEN 한 `video_id`에 raw 페이지 정확히 1개 | — | FR-3 |
| BR-TXN-1 | THEN `.md` + `.json` 은 한 트랜잭션 — 둘째 실패 시 첫째 롤백(부분 산출물 0) | — | FR-8, pipeline.py:55-81 |
| BR-OUT-1 | THEN 산출 경로 = `<out>/<video_id>.md` AND `<out>/<video_id>.json`. 기본 `out = raw/sources/video/` | — | FR-3, FR-6 |

### 의존·LLM (DEP)
| ID | 명제 (IF-THEN) | 예외 (UNLESS) | 출처 |
|----|----------------|---------------|------|
| BR-DEP-1 | THEN importer는 추출기 모듈(`ytscript.*`)을 import하지 않는다 — canonical을 dict로만 소비 | — | FR-12, NFR-1 |
| BR-DEP-2 | THEN 본 라운드 실행 경로에 LLM 호출 0 | — | FR-13, NFR-3 |
| BR-DEP-3 | IF (2차) LLM 호출 THEN profile alias `ingest`(_meta/llm-config.yaml:11) + Claude Code/Codex CLI 세션. API·model_id 직접 인용 금지 | — | NFR-3, Claude 메모리 `llm-call-cli-not-api` |

### 스키마 directive (ADR)
| ID | 명제 (IF-THEN) | 예외 (UNLESS) | 출처 |
|----|----------------|---------------|------|
| P-ADR-1 | THEN 페이지 본문(raw·wiki 공통)의 model_id·자기추론 grep 규칙은 **폐기** — 본문 모델명은 lint 대상 아님 | — | FR-10, ADR-001, taxonomy.md:118-126 |
| P-ADR-2 | THEN model_id alias 규율은 **LLM 호출 site·프롬프트**에만 유지(코드 규약, 마크다운 grep 무관) | — | FR-10, AGENTS.md:113-118, _meta/llm-config.yaml:11 |
| P-ADR-3 | THEN `raw/sources/video/` 는 유효 raw 폴더 — AGENTS.md:24 목록 + source_type:video 정합 | — | FR-11, ADR-002 |

## 3. 상태 전이

### RawPage (ingest 1회)
| 시작 | → 종료 | 트리거 | 규칙 |
|------|--------|--------|------|
| (입력) | Rejected | 경로 부재 / schema 불일치 / 후보 0 | VR-1,2,3 / BR-SEL-5 |
| (입력) | Skipped | 대상 존재 ∧ ¬force | BR-IDEM-1 |
| (입력) | Selected | 후보 ≥1 ∧ (¬존재 ∨ force) | BR-SEL-3,4 |
| Selected | Mapped | frontmatter 생성 | P-MAP-* |
| Mapped | Rendered | body 결합(verbatim) | BR-BODY-1 |
| Rendered | Committed | atomic 성공 → RawPageCommitted | BR-TXN-1 |
| Rendered | Rejected | atomic 실패 → 롤백 | BR-TXN-1 |

- 종료 상태: {Rejected, Skipped, Committed} — 모두 명확. 데드 상태 없음. 도달 불가 상태 없음.

## 4. 검증 규칙
| ID | 대상 | 조건 | 실패 시 |
|----|------|------|---------|
| VR-1 | 입력 경로 | 존재해야 함 | exit 1, "입력 경로 부재: <path>" |
| VR-2 | `schema_version` | `== "1.0"`(domain.py:12) | exit 1, "지원하지 않는 schema_version" |
| VR-3 | `video.id` | non-empty | exit 1, "video.id 부재 — 파일명 생성 불가" |
| VR-4 | canonical 구조 | `video`·`extraction`·`full_text` 키 존재 | exit 1, "canonical 구조 손상" |
| VR-5 | 출력 결과 | 생성 후 `lint.py --paths <md>` HIGH=0. lint이 raw 필수필드(`RAW_REQUIRED_FIELDS` 6개) 누락을 hard-fail | 필드 누락/HIGH 시 거부(FR-9) |

## 5. 일관성 검증 결과

### 규칙 간 충돌
| 규칙 A | 규칙 B | 충돌 유형 | 해결 |
|--------|--------|----------|------|
| P-ADR-1 (본문 grep 폐기) | P-ADR-2 (alias는 호출 site 유지) | 외견상 "폐기 vs 유지" | **충돌 아님** — 적용 대상 분리(페이지 본문 grep ↔ LLM 호출 코드 규약). 서로 다른 layer |
| BR-BODY-1 (verbatim) | P-MAP-5 (last_verified 변환) | 외견상 "무수정 vs 변환" | **충돌 아님** — frontmatter는 메타(변환 대상), body만 verbatim. 적용 대상 분리 |
| BR-IDEM-1 (skip) | BR-IDEM-2 (force 덮어쓰기) | 동일 대상 상반 결과 | **충돌 아님** — force 플래그로 우선순위 명확 |
| BR-SEL-3 (method 우선) | BR-SEL-4 (extracted_at) | 동률 처리 | **충돌 아님** — SEL-4는 SEL-3 동률 시에만 발동(계층적) |
| BR-DUP-1 (영상당 1개) | BR-SEL-3 (best 1개 선택) | — | **정합** — 1개 선택이 1페이지를 보장 |

→ 충돌 0.

### 완전성
| 검증 항목 | 상태 | 비고 |
|----------|------|------|
| 분기 누락 | PASS | 입력 3분기(파일/디렉토리/부재) + 후보 0/1/N 전부 규칙 존재 |
| 경계값 | PASS | null title/upload_date/channel(P-MAP-1,3,10), 빈 전사(BR-BODY-3), 후보 0(BR-SEL-5) |
| 예외 처리 | PASS | VR-1~4 거부 경로 + BR-TXN-1 롤백 |

### 교차 검증 (architecture.md 대비)
| 검증 항목 | 상태 | 불일치 상세 |
|----------|------|-----------|
| 엔티티 매핑 | PASS | RawPage(arch §4) = 본 문서 §1 엔티티. 속성 일치 |
| API-규칙 매핑 | PASS | CLI ingest(arch §5) ↔ BR-SEL/IDEM/TXN 트리거. `--force`↔BR-IDEM-2, `--now`↔P-MAP-6 |
| 제약조건 일관성 | PASS | arch §4 frontmatter 순서 = §2 P-MAP-* 순서. lint 필수 6필드(lint.py:64)는 importer 산출 7필드(6+ingested_date)의 **부분집합** → importer 산출은 항상 lint 충족 |

### 교차 검증 (prd.md 대비)
| FR | 대응 규칙 | 상태 |
|----|----------|------|
| FR-1 | BR-SEL-1,2,5 / VR-1 | PASS |
| FR-2 | BR-SEL-3,4 | PASS |
| FR-3 | BR-DUP-1, BR-OUT-1 | PASS |
| FR-4 | P-MAP-1~10 | PASS |
| FR-5 | BR-BODY-1,2,3 | PASS |
| FR-6 | BR-OUT-1, BR-TXN-1 | PASS |
| FR-7 | BR-IDEM-1,2 | PASS |
| FR-8 | BR-TXN-1 | PASS |
| FR-9 | VR-5 | PASS |
| FR-10 | P-ADR-1,2 | PASS |
| FR-11 | P-ADR-3 | PASS |
| FR-12 | BR-DEP-1 | PASS |
| FR-13 | BR-DEP-2,3 | PASS |

→ FR 13건 전부 ≥1 규칙 매핑(추적성 PASS).
