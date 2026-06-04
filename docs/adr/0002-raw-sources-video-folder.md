# ADR-0002: `raw/sources/video/` 폴더 신설

- Status: **Proposed** (사용자 승인 대기 — 스키마 공진화 게이트, AGENTS.md:27 / PRD NFR-6)
- Date: 2026-06-04
- 관련: PRD FR-11, business-logic P-ADR-3

## Context

`frontmatter-spec.md:36` 은 raw `source_type` enum 에 `video` 를 포함한다. 그러나 실측 raw 디렉토리는 `raw/sources/{papers,web,conversations,urls}/` 4종뿐(AGENTS.md:24)이며 **video 전용 폴더가 없다**. importer 가 video raw 페이지를 적재할 표준 위치가 미정의.

## Decision

**`raw/sources/video/` 폴더를 신설**하고 video importer 출력의 기본 위치로 한다.

1. 디렉토리: `raw/sources/video/<video_id>.md` (verbatim raw) + `raw/sources/video/<video_id>.json` (canonical 원본 복사, FR-6).
2. `AGENTS.md:24` raw 폴더 목록을 `{papers,web,conversations,urls,video}` 로 갱신.
3. `frontmatter-spec.md`: `source_type: video` 페이지의 표준 위치를 `raw/sources/video/` 로 명시(enum↔폴더 정합).

## Consequences

- (+) source_type:video ↔ 폴더명 일치 → 탐색성·일관성(축3) 향상.
- (+) YouTube=URL 출처라는 이유로 `urls/` 재사용하는 모호성 제거(source_type 불일치 회피).
- (중립) 폴더 1개 추가 — 기존 4종과 동일 계층, 스키마 영향 최소.

## 대안 (기각)
- `raw/sources/urls/` 재사용 — 기각: source_type(video)↔폴더명(urls) 불일치로 탐색성 저하.
- `raw/sources/papers/` 등 기존 폴더 전용화 — 기각: 의미 불일치.
