# Frontmatter Spec

본 문서는 frontmatter 계약의 소유 경계만 정의한다. 필드 목록을 다른 문서에 복제하지 않는다.

## Current wiki content

- `_meta/knowledge.schema.json`의 `DocumentInstance.properties`가 허용 필드·필수 필드·타입의 단일 진실이다.
- `scripts/knowledge/schema.py`가 Markdown을 instance로 변환하고 schema와 page-type section contract를 검증한다.
- `scripts/knowledge/check.py`가 artifact·graph·lifecycle·taxonomy 규칙을 같은 instance에 적용한다.
- domain과 lifecycle은 path에서 파생하며 frontmatter에 중복 저장하지 않는다.
- Claims·Relations·Members는 frontmatter가 아니라 schema가 정의한 본문 table이다.

## Raw source

- content-addressed `raw/sources/<source_type>/<source_id>/<digest>/` bundle은 `_meta/knowledge.schema.json`의 `ArtifactManifest`와 `scripts/knowledge/artifacts.py`가 소유한다.
- legacy curated raw Markdown의 최소 필드와 recency는 `scripts/lint.py`의 `RAW_REQUIRED_FIELDS`와 raw 전용 검사만 적용한다.
- raw `last_verified` 누락과 age 730일 이상의 HIGH는 `evergreen`으로 면제하지 않는다. non-raw authored concept가 명시적으로 `evergreen: true`와 `last_verified`를 함께 가지면 age 730일 이상의 HIGH만 면제하고 180일 이상의 MEDIUM은 유지한다.

## Authored source

`cs/`, `development/`, `coding-test/`, `lang/`, `tools/`는 사람 작성 원문이며 frontmatter를 강제하지 않는다. `_meta/defaults.yaml`은 ingest 시 해석 기본값이고 canonical wiki frontmatter로 복사하는 필드 목록이 아니다.

## Historical contract

순서 6b 이전의 wiki 15-field·source-summary derived frontmatter 계약은 historical non-normative이며 현재 validator 입력이 아니다. 이전 상세는 Git history가 보존한다.
