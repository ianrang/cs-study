# ADR-0003: Domain Registry (`_meta/domains.yaml`) 도입

- Status: **Accepted** (사용자 승인 2026-06-05 · raw video -> wiki synthesis 2차 설계)
- Date: 2026-06-05
- 관련: `docs/wiki-ingest-prd.md`, `docs/wiki-ingest-architecture.md`, `docs/wiki-ingest-business-logic.md`

## Context

2차 raw -> wiki synthesis 는 raw source 를 `wiki/domains/<domain>/sources/` 또는 `wiki/staging/domain-review/` 로 분류해야 한다.

기존 vault 에서 domain 판단 기준은 다음 surface 에 흩어져 있다.

- `wiki/overview.md`: 예정 domain 목록
- `wiki/domains/`: 실제 디렉토리 구조
- `_meta/taxonomy.md`: tag/entity/concept vocabulary

이 상태에서 `scripts/wiki_ingest.py` 가 domain 이름을 코드에 하드코딩하면 domain 추가마다 script 수정이 필요하고, taxonomy 와 domain 책임이 섞인다. 이는 단일 진실, 캡슐화, 유지보수성 원칙에 맞지 않는다.

## Decision

`_meta/domains.yaml` 을 domain registry 의 단일 진실로 도입한다.

1. `_meta/domains.yaml` 은 active/inactive domain 목록, 표시 이름, source root hint 를 가진다.
2. `_meta/taxonomy.md` 는 계속 vocabulary 의 단일 진실로만 유지한다.
3. `scripts/wiki_ingest.py` 는 domain 이름을 하드코딩하지 않고 registry loader 로만 domain 을 읽는다.
4. registry 에 없거나 inactive 인 domain 은 active target 으로 쓰지 않는다.
5. registry 에 없는 domain decision 은 low confidence 로 강등되어 `wiki/staging/domain-review/` 로 간다.
6. domain 추가/비활성화는 `_meta/domains.yaml` 변경에서 시작한다. taxonomy 확장이 필요하면 별도 review 로 처리한다.
7. `scripts/wiki_ingest.py --domain <domain>` 수동 override 는 registry 에 존재하고 active 인 domain 에만 허용한다. missing/inactive override 는 reject 한다.

초기 seed:

- `developer-tools`
- `ai-engineering`
- `software-engineering`
- `information-security`
- `network`
- `cryptography`
- `programming-language`
- `algorithms`

## Consequences

- (+) domain 추가 시 코드 수정 없이 `_meta/domains.yaml` 한 곳에서 시작할 수 있다.
- (+) taxonomy 와 domain 책임이 분리된다.
- (+) wiki ingest stage 의 캡슐화와 단방향 의존이 유지된다.
- (+) registry 에 없는 domain 을 staging 으로 보내므로 오분류를 줄인다.
- (+) 수동 override 도 active registry domain 으로 제한되어 domain SoT 를 우회하지 못한다.
- (-) `_meta/` schema surface 가 하나 늘어난다. 대신 ADR 과 registry schema 로 관리한다.

## Rejected alternatives

- `scripts/wiki_ingest.py` 에 domain list 하드코딩: 기각. domain 변경마다 코드 수정이 필요하고 캡슐화가 깨진다.
- `_meta/taxonomy.md` 에 domain list 병합: 기각. taxonomy 는 tag/entity/concept vocabulary SoT 이며 domain registry 와 책임이 다르다.
- `wiki/overview.md` 를 domain SoT 로 사용: 기각. overview 는 사람이 읽는 entry point 이며 machine-readable registry 로 안정적이지 않다.
