# Todo

작성일: 2026-07-17
SoT: 로컬 `todo.md`

## Scope Contract

| 항목 | 내용 |
|---|---|
| 갱신 대상 task | 신규 P1-T1, P1-T2 등록 |
| 신규 등록 후보 | 기출 복원 31회차 513문항 전체 검증, Information Security Practice 설계 문서 9개 정합화 |
| 범위 밖 | handoff, commit, push, 원본 기출 MD 수정, Practice 구현, 학습 콘텐츠 추가 |
| 검증 기준 | 상태·분류 enum, 중복 없음, 선행 단방향·순환 없음, P1-T1 완료 전 P1-T2 미착수 |

## 상태 Enum

| 상태 | 의미 |
|---|---|
| `[ ]` | pending |
| `[-]` | in-progress |
| `[x]` | completed |
| `[!]` | blocked |
| `[~]` | discarded |

## 정보보안기사 실기 Practice

| ID | 상태 | 분류 | 작업 | 선행 | 입력 | 산출 |
|---|---|---|---|---|---|---|
| P1-T1 | [x] | [검증] | 기출 복원 31회차 513문항의 문제·답안·출처 경계·독립 풀이 가능성을 회차별로 전수 검증하고, 오류·모호성·복원 한계를 근거와 함께 정정·기록 | 없음 | `wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/01-rounds/`, `06-verification/`, KCA 출제 범위 및 확인 가능한 1차·공식 레퍼런스 | 회차별 검증 보고서, 정정된 원본 MD·파생 JSON의 동기화 증거, 남은 복원 한계 목록 |
| P1-T2 | [x] | [검증] | 기출 전수 검증 완료 후 Information Security Practice 설계 문서 9개의 frontmatter·source_paths·provenance·SSOT 참조를 실제 근거로 정합화하고 vault lint를 재검증 | P1-T1 | `AGENTS.md`, `_meta/frontmatter-spec.md`, `scripts/lint.py`, `wiki/domains/information-security/docs/{prd.md,architecture.md,chapter-2-p1-settings-scope.md,chapter-3-p1-settings-scope.md,business-logic/chapter-2-p1-settings.md}`, `wiki/domains/information-security/practice/{README.md,DESIGN.md,docs/architecture.md,docs/past-exam-import-architecture.md}` | 9개 문서의 유효 frontmatter 및 SSOT 참조 정합화, 해당 9개 문서의 lint HIGH 18건 해소 증거, 문서 간 중복·순환 참조 없음 확인 |
