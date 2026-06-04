# Architecture: cs-study `scripts/ingest.py` — 결정적 video importer (1차)

> 대상 PRD: `docs/prd.md`. 본 문서는 **1차 라운드(결정적 importer)** 의 아키텍처만 정의한다.
> 비즈니스 규칙·명제는 `docs/business-logic.md`(dev-design-logic) 소관.
>
> **인용 경로 범례**: cs-study 파일은 `~/dev/personal/001_cs-study/` 기준(`lint.py`=`scripts/`, `*-spec.md`·`quality-bar.md`=`_meta/`, `AGENTS.md`=루트). 추출기 파일은 `~/dev/personal/007_youtube-script/` 기준(`domain.py`·`pipeline.py`=`src/ytscript/`, `doc_hook.py`=`src/ytscript/hooks/`, `default.md.j2`=`templates/`).

## 1. 기술 스택

| 분류 | 기술 | 버전·근거 |
|------|------|------|
| 언어 | Python | uv 3.12 (cs-study 기존 scripts 정합 — `lint.py`, `llm_config.py`) |
| 입력 파싱 | 표준 `json` | canonical JSON v1.0 (`domain.py:12 SCHEMA_VERSION`) |
| frontmatter 직렬화 | PyYAML `yaml.safe_dump` | lint.py:34 기존 의존. YAML 유효성·이스케이프 보장 |
| CLI | 표준 `argparse` | `llm_config.py:165-179`, `lint.py:252-258` 패턴 정합 |
| 파일 경로 | 표준 `pathlib` | 기존 scripts 정합 |
| LLM | **본 라운드 없음** | seam만 정의(§7). 2차는 `LLMResolver.resolve("ingest")` + CLI 세션 |

추출기 코드(`ytscript.*`)는 **import 하지 않는다**(FR-12, NFR-1). canonical JSON을 일반 dict로 읽어 anti-corruption 경계를 둔다.

## 2. 레이어 구조

단일 스크립트(`scripts/ingest.py`) 내부의 **논리 레이어**. 의존 방향 단방향(↓), 순환 0.

```
 CLI (argparse main)                      ─ 진입·인자 해석·exit code
        │ ↓
 orchestrator: ingest(target, *, force)   ─ 흐름 조립 (유일하게 순서를 안다)
        │ ↓                ↓                ↓                 ↓
 (a) input/select   (b) mapping     (c) render        (d) commit
  locate_canonical   build_raw_page  to_markdown      atomic_commit
  select_variant     (dict→RawPage)  (RawPage→str)    (.md + .json)
        │                 │                                  
        └─────────────────┴──────────────┬───────────────────┘
                                          ↓
                          domain model: RawPage (last leaf)
                          ─ 표준 라이브러리만. 어떤 내부 함수도 호출 안 함
```

**호출 체인 깊이** (NFR-5, 신규 코드 ≤ 함수 5개 / edge ≤4):
- `main → ingest → select_variant`  (edge 2)
- `main → ingest → build_raw_page`  (edge 2)
- `main → ingest → to_markdown`     (edge 2)
- `main → ingest → atomic_commit`   (edge 2)

최대 직렬 체인 = 함수 3개(edge 2). 임계(edge 4) 내. orchestrator는 pass-through가 아니라 "추출 흐름을 아는" 의미 있는 조립 경계 — 추출기 `pipeline.py:84-147 run()` 과 동일 역할.

**anti-corruption (단방향 보장)**: (a)는 canonical JSON을 `dict`로만 읽는다. 추출기 `domain.Transcript` 를 import하지 않으므로 추출기→cs-study 결합이 생기지 않는다. canonical 스키마는 "포맷 계약"일 뿐(memory:16). `schema_version` 불일치 시 명시적 거부.

## 3. 디자인 패턴

| 패턴 | 적용 위치 | 선택 이유 | 검토한 대안 (기각) |
|------|----------|----------|-----------|
| Anti-Corruption Layer | (b) mapping: canonical dict → `RawPage` | 추출기 도메인을 cs-study에 누출 안 함. 단방향(FR-12, NFR-1) | 추출기 `Transcript` 직접 import — **기각**: 양방향 결합·순환 위험 |
| Pure render (template method) | (c) `to_markdown` | 결정성(NFR-2), 부수효과 0. 추출기 `render.py` 와 동형 | Jinja2 템플릿 — 기각: 추출기 템플릿 재사용 시 경로 결합. 단순 string으로 충분 |
| Atomic commit (temp + os.replace + 롤백) | (d) `atomic_commit` | 부분 산출물 0(FR-8). 추출기 `pipeline.py:55-81` 패턴 정합 | 직접 write — 기각: `.md`/`.json` 부분 산출 위험 |
| Idempotent skip-unless-force | orchestrator | 멱등(FR-7). 추출기 `pipeline.py:111` 의미 정합 | 항상 덮어쓰기 — 기각: 사람 frontmatter 보강 손실(AGENTS.md:31) |
| Best-variant selector (우선순위 함수) | (a) `select_variant` | 영상당 1페이지(FR-2,3). 추출기 `language.resolve` 우선순위 동형 | 추출기에 1파일 강제 — 기각: 단방향 위반 |

## 4. 데이터 모델

추출기 `domain.py` 를 미러링하되 **cs-study raw 표현**으로 변환한 last-leaf 모델.

### `RawPage` (frozen dataclass)

| 속성 | 타입 | 제약 | 설명 |
|------|------|------|------|
| `video_id` | `str` | NOT NULL·고유 | 파일명 stem (`<video_id>.md/.json`). canonical `video.id` |
| `frontmatter` | `dict[str, Any]` | 순서 고정 | raw frontmatter (§매핑) |
| `body` | `str` | verbatim | `full_text` + 타임스탬프 segments. 무수정(FR-5, NFR-4) |
| `canonical` | `dict` | 원본 | 복사 보관용 canonical 원본(FR-6) |

### frontmatter 필드 (생성 순서 고정 — 결정성 NFR-2)

`title, source_url, source_date, source_type, last_verified, ingested_date, tier, extraction_method, [stt_model, stt_engine,] channel, duration_seconds, language`

- 필수 **7필드** = `lint.py:64 RAW_REQUIRED_FIELDS` 6개(`title, source_url, source_date, source_type, last_verified, tier`) + `ingested_date`(frontmatter-spec.md:38). PRD FR-4 수용기준(7필드 전부 채워짐)과 동일.
- `stt_model/stt_engine` 은 `method == "stt"` 일 때만(조건부, default.md.j2:10-11 정합).
- 매핑 규칙 상세는 `docs/business-logic.md` 명제 P-MAP-*.

### 관계
- `canonical JSON (입력)` 1:1 `RawPage` 1:1 `raw/sources/video/<id>.{md,json} (출력)`.
- `video_id` 가 동일성 키 — 멱등·중복 회피의 단일 기준.

## 5. API 설계 (CLI)

| Command | 형태 | 설명 |
|--------|------|------|
| ingest | `python3 scripts/ingest.py <path> [--force] [--out raw/sources/video]` | `<path>` = canonical JSON 파일 또는 `out/<id>/` 디렉토리(FR-1). 디렉토리면 best-variant 선택(FR-2) |

- exit code: 성공 `0`, skip `0`(메시지), 오류(경로 부재·schema 불일치·부분 실패) `1`. lint.py:286 / llm_config.py:187 패턴 정합.
- 출력 보고: 생성/skip 경로를 stdout. 비결정 요소(`ingested_date`)는 `--now` 주입 가능(테스트 결정성 — 추출기 `pipeline.py:90 now` 패턴 정합).
- 인증/인가: 해당 없음(로컬 파일 처리).

## 6. 프로젝트 구조

```
001_cs-study/
├── scripts/
│   ├── ingest.py          # [신규] 본 설계. 결정적 video importer
│   ├── lint.py            # [수정] ADR-001 본문 grep 폐기 + raw 필수필드 강제(RAW_REQUIRED_FIELDS 호출, frontmatter-spec.md:115 완성)
│   ├── llm_config.py      # [무변경] 2차 라운드 seam이 resolve("ingest") 인용
│   └── commit_wiki.sh     # [무변경] wiki commit (본 라운드 미사용 — raw까지)
├── _meta/
│   ├── frontmatter-spec.md # [수정] ADR-002 video 폴더 위치 + raw 필드수 표기 4→6 정합(FR-9)
│   └── quality-bar.md      # [수정 — ADR-001] directive 행에서 본문 model_id grep 항목 삭제
├── AGENTS.md               # [수정 — ADR-001] 113-118 model_id 금지 = LLM 호출·프롬프트 한정 명시 / [ADR-002] raw 폴더 목록에 video 등재
├── raw/sources/
│   └── video/             # [신규 — ADR-002]
│       ├── <video_id>.md   # 출력: verbatim raw 페이지
│       └── <video_id>.json # 출력: canonical 원본 복사(FR-6)
└── docs/
    ├── prd.md
    ├── architecture.md     # 본 문서
    ├── business-logic.md
    └── adr/
        ├── 0001-raw-verbatim-directive-advisory.md
        └── 0002-raw-sources-video-folder.md
```

**모듈 의존 방향**: `ingest.py → (stdlib json/pathlib + PyYAML)` 만. cs-study 다른 scripts·추출기 import 0. → arch-cycle-detector 대상 시 순환 0 예상.

**네이밍**: 파일 lowercase(video_id는 YouTube가 부여한 case-sensitive id 그대로 — 고유성 우선). ADR `NNNN-kebab-title.md`.

## 7. 파이프라인 오케스트레이션 + LLM synthesis seam

### 7.1 extract→ingest 오케스트레이터 (구현됨)

한 명령으로 추출(stage 1) + 적재(stage 2). `scripts/pipeline.py` + `_meta/pipeline.yaml`.

```
pipeline.py ──(subprocess: uv run ytscript URL --print-json-path)──► canonical JSON 경로 회수
            ──(import ingest)──────────────────────────────────────► raw/sources/video/<id>.{md,json}
            ──(wiki.enabled 면)────────────────────────────────────► 사람 review 게이트에서 정지(안내만)
```

- **단방향**: ytscript 는 subprocess(CLI 계약), ingest 는 cs-study 내부 모듈. pipeline.py 는 ytscript 를 **python import 하지 않는다**(canonical 포맷·CLI 에만 의존 → 순환 0).
- **추출기 의존**: ytscript `--print-json-path`(007 `feat/emit-json-path`) — 산출 canonical 경로를 stdout 1줄로 emit. 추출기는 여전히 cs-study 무지.
- **wiki(stage 3)** 는 raw→wiki 사람 게이트(AGENTS.md:85-91)라 자동 경계 밖 — `wiki.enabled` 여도 정지하고 안내만.
- 사용: `python3 scripts/pipeline.py <URL> [--config _meta/pipeline.yaml] [--force]`

### 7.2 wiki synthesis seam (FR-13 — 이연)

본 라운드는 raw까지. 2차 라운드(별도 PRD)가 plug-in 할 **핸드오프 경계**:

```
[1차 — 본 설계]                          [2차 — 이연]
ingest.py ──► raw/sources/video/<id>.md  ──►  synthesize (Claude Code/Codex CLI 세션)
              raw/sources/video/<id>.json      · ingest universe 입력 (AGENTS.md:48)
              (verbatim, 무 LLM)                · LLMResolver.resolve("ingest") (llm_config.py)
                                                · 교정·구조화·domain 분류·wiki 합성
                                                · 사람 승격 게이트 (AGENTS.md:85-91, NFR-7)
```

- seam 계약: 2차는 **raw 파일을 입력으로만** 읽는다. 1차 importer는 2차를 모른다(단방향 유지).
- 추출기 `doc_hook`(doc_hook.py:19-23 NoOpHook)은 **no-op 유지** — 연결은 cs-study importer pull(memory:16), push 아님.
- LLM 호출은 API 금지, CLI 세션만(Claude 메모리 `llm-call-cli-not-api`, NFR-3).

## 8. 검증 결과 (자체)

| 항목 | 상태 | 비고 |
|------|------|------|
| 순환 참조 | PASS | ingest.py가 추출기·타 scripts import 0. anti-corruption 경계 |
| 계층 깊이 | PASS | 최대 직렬 함수 3개(edge 2) < 임계 edge 4 (NFR-5) |
| 캡슐화 | PASS | canonical을 dict로만 소비. 추출기 도메인 누출 0 |
| 요구사항 커버리지 | PASS | FR-1~13 전부 레이어/패턴/구조에 매핑 |
| 기술 스택 정합성 | PASS | stdlib + PyYAML(기존 의존). 추출기·cs-study 컨벤션 정합 |

### FR → 설계 매핑
- FR-1,2 → §2(a) input/select, §5 CLI
- FR-3,6,7,8 → §2(d) atomic_commit, §3 패턴, §4 관계
- FR-4,5 → §2(b)(c), §4 frontmatter, business-logic P-MAP-*
- FR-9 → §6 lint 통과 + ADR-001
- FR-10,11 → §6 수정 파일, §9 ADR
- FR-12 → §2 anti-corruption, §6 의존 방향
- FR-13 → §7 seam

## 9. 리스크

| 리스크 | 영향 | 대응 |
|---|---|---|
| ADR-001 본문 grep 폐기가 모델 통제를 약화? | 외견상 model_id 자유화 | **약화 0** — model_id alias 단일 통제는 LLM 호출 코드(`LLMResolver`)에 유지. grep은 taxonomy(taxonomy.md:118-126)와 모순된 skeleton 과잉 적용이라 제거. 표기 일관성은 축3 vocab으로 보장. P-ADR-1/2 |
| `lint.py` raw 필드 강제 미구현(skeleton, lint.py:64 미호출) | 산출 raw가 lint는 통과하나 spec 불완전 가능 | **본 작업에서 해소** — RAW_REQUIRED_FIELDS 강제 체크 구현(FR-9) + spec wording 4→6 정합. importer(FR-4)와 이중 보장 |
| `extracted_at`→`last_verified` 의미 차이(추출시각 ≠ 확인시각) | 재현성 축 해석 모호 | 합리적 proxy(추출이 곧 source 확인). business-logic P-MAP-5에 의미 명시 |
| video 대응 wiki 도메인 부재(software-engineering 등) | 2차 합성 시 분류 불가 | 본 라운드 raw는 domain 불요(lint.py:64). 2차 PRD에서 taxonomy 확장(taxonomy.md:140-143) |
| canonical schema_version drift(추출기 1.0→2.0) | 매핑 깨짐 | importer가 `schema_version` 검사 후 불일치 거부(§2 anti-corruption) |
