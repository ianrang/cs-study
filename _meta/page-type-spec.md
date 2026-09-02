# Page Type Spec

본 문서는 page type 계약의 소유 경계만 정의한다. enum과 section 목록을 복제하지 않는다.

## Current contract

- `_meta/knowledge.schema.json`의 `PageType`과 조건부 `allOf`가 page type·필수 section의 단일 진실이다.
- `scripts/knowledge/schema.py`가 schema에서 page type·section contract를 읽어 검증한다.
- `scripts/knowledge/materialize.py`가 같은 contract로 `wiki/templates/`를 생성한다.
- `wiki/domains/`·`wiki/collections/`의 active page와 `wiki/staging/`·`wiki/archive/` page는 모두 같은 schema contract를 사용한다.
- `cs/`, `development/`, `coding-test/`, `lang/`, `tools/`의 authored 문서에는 이 계약을 적용하지 않는다.

## Historical contract

순서 6b 이전의 6개 page type·수동 section matrix·`provenance`·`evergreen` 규칙은 historical non-normative이며 현재 validator 입력이 아니다. 이전 상세는 Git history가 보존한다.
