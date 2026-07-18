---
title: "Business Logic: Chapter 2 P1 설정·정책 문항 보강"
tier: llm-synthesis
page_type: method
domain: information-security
domain_confidence: high
shared_scope: domain
tags: []
status: active
date_created: 2026-07-13
date_updated: 2026-07-17
source_paths:
  - "wiki/domains/information-security/docs/chapter-2-p1-settings-scope.md"
  - "wiki/domains/information-security/docs/prd.md"
  - "wiki/domains/information-security/docs/architecture.md"
  - "wiki/domains/information-security/drafts/study/2장 정리.md"
  - "wiki/domains/information-security/practice/data/question-packs/network-firewall.json"
  - "wiki/domains/information-security/practice/app.js"
  - "wiki/domains/information-security/practice/scripts/build-practice-data.py"
source_count: 7
provenance: inferred
summary: "2장 P1 설정·정책 문항의 분류, 자동·자가 채점 경계, 근거와 검증 규칙을 명제화한다."
evergreen: false
---

# Business Logic: Chapter 2 P1 설정·정책 문항 보강

## 1. 도메인 개념

### 용어 사전

| 용어 | 정의 |
|---|---|
| 설정·정책 문항 | 명령, 룰, 적용 위치, 보안 통제 선택 또는 운영 정책의 결과를 답하는 P1 문항이다. |
| 결정적 답 | 원문·지문으로 하나의 명령, 옵션, 순서 또는 판정으로 수렴하는 답이다. 자동 채점 대상이다. |
| 조건 의존 답 | 플랫폼, 버전, 운영 환경 또는 다수 정상 통제안에 따라 답이 달라지는 답이다. 서술형 자가 채점 대상이다. |
| 기출 기반 | 회차 복원 데이터셋을 직접 참조하는 문항이다. 공식 원문 확정을 뜻하지 않으며 `source-derived` 상태를 함께 표시한다. |
| 예상 문제 | 예측 목록과 패턴 분석 근거를 함께 참조하는 문항이다. 기출 기반으로 표시하지 않는다. |

### 엔티티와 값 객체

| 구분 | 이름 | 설명 |
|---|---|---|
| 엔티티 | Question | `id`, 소속 주제, 단계, 답안 계약, 근거를 갖는 불변 문제 정의다. |
| 값 객체 | SourceRef | 원문 경로·행·확인 문구·검증 상태를 묶는다. |
| 값 객체 | AnswerContract | handler와 호환되는 자동 채점 정답 집합 또는 자가 채점 rubric이다. |
| 도메인 이벤트 | AnswerSubmitted / SelfReviewed | 기존 앱의 자동 채점·자가 평가 진행도 전이를 사용한다. |

## 2. 비즈니스 규칙

| ID | 명제 (IF-THEN) | 예외 | 출처 |
|---|---|---|---|
| BR-P1-001 | IF 원문 P1 항목이 명령·룰·적용 위치·통제 선택·운영 정책을 직접 제시 THEN 해당 항목은 최소 한 문제로 표현한다. | 단순 조회 명령·순수 개념·P2/P3은 제외한다. | 사용자 요청, `2장 정리.md:24, 54` |
| BR-P1-002 | IF 답이 하나의 문자열 또는 배열 순서로 결정 THEN 기존 short/cloze/order handler로 자동 채점한다. | 복수 정상 운영안·제품/버전 의존 답은 essay handler로 둔다. | PRD FR-3·4, `2장 정리.md:578, 635, 683` |
| BR-P1-003 | IF 새 문항이 기존 주제의 세부 통제를 보강 THEN 새 curriculum topic이나 handler를 만들지 않고 해당 주제의 후속 문항으로 추가한다. | 기존 handler로 표현할 수 없는 상호작용은 별도 설계가 필요하다. | Architecture의 schema-driven content 원칙 |
| BR-P1-004 | IF 문항이 기출 기반이라면 THEN `01-rounds` sourceRef를 가진다. IF 예상 문제라면 THEN `questionKind: predicted`와 `08-prediction`, `05-analysis` sourceRef를 모두 가진다. | 학습 문항은 원문 sourceRef만으로 등록할 수 있다. | validator provenance 규칙 |
| BR-P1-005 | IF 실전 모드 THEN 주제·단계·분류·상세 입력 라벨을 노출하지 않고, `examPrompt`가 있으면 그것만 제시한다. | `examPrompt`가 없는 기존 문항은 원래 지문을 사용한다. | PRD FR-10 |
| BR-P1-006 | IF 원문은 하나의 보완책을 다른 보완책과 병행하라고 명시 THEN 단일 명령 암기가 아닌 병행 관계 또는 적용 한계를 해설/rubric에 포함한다. | 결정적 명령 자체를 묻는 빈칸은 유지한다. | `2장 정리.md:215, 225, 511, 617` |

## 3. 상태 전이

Question의 진행도 상태는 기존 모델을 바꾸지 않는다.

| 시작 | → 종료 | 트리거 | 규칙 |
|---|---|---|---|
| 미풀이 | → 정답 완료 | 자동 채점 정답 제출 | BR-P1-002 |
| 미풀이/정답 완료 | → 복습 필요 | 자동 채점 오답 제출 또는 자가 평가 | BR-P1-002 |
| 자가 채점 대기 | → 정답 완료/복습 필요 | 모범답안 확인 뒤 학습자 선택 | PRD FR-4 |
| 모든 상태 | → 미풀이 | 문항·범위·전체 초기화 | 기존 LocalStorage 초기화 규칙 |

## 4. 검증 규칙

| ID | 대상 | 조건 | 실패 시 |
|---|---|---|---|
| VR-P1-001 | 16개 추가 문항 | 각각 기존 active curriculumId, unique ID, sourceRef, explanation, tags, prerequisites를 가진다. | builder 실패 |
| VR-P1-002 | 자동 채점 문항 | stage handler와 answer.type·matchPolicy·accepted 구조가 일치한다. | builder 실패 |
| VR-P1-003 | 예상 문항 | `08-prediction`과 `05-analysis` sourceRef가 모두 존재한다. | builder 실패 |
| VR-P1-004 | 원문 근거 | sourceRef의 행에 excerpt가 실제로 포함된다. | builder 실패 |
| VR-P1-005 | 선수관계 | 같은 주제 또는 curriculum 선행 계보 안에 있고 DAG를 이룬다. | builder 실패 |
| VR-P1-006 | 실전 지문 | `examPrompt`가 있으면 빈 배열이 아니고, 자동 채점 허용 정답 토큰을 그대로 노출하지 않는다. | 정적 누출 검사 실패 |

## 5. 완료 술어

| 명제 ID | 완료 술어 | 확인 surface |
|---|---|---|
| BR-P1-001 | 16개 추가 ID가 지정된 주제에 존재하고, P2/P3만의 항목은 새 답안으로 강제하지 않는다. | question pack, curriculum sourceSection, sourceRefs |
| BR-P1-002 | cloze/short/order는 기존 handler로 결과가 결정되고, 조건 의존 통제는 essay rubric으로 표시된다. | `app.js` stageHandlers, builder |
| BR-P1-003 | 추가 문항으로 새 handler·topic·UI 분기 없이 generated data가 생성된다. | `curriculum.json`, `app.js`, build output |
| BR-P1-004 | 예상 문항에서 예측·분석 sourceRef 하나라도 제거하면 validator가 실패한다. | `build-practice-data.py` provenance 검사 |
| BR-P1-005 | 실전 모드의 카드에는 topic/stage/origin badge가 없고 입력 라벨은 일반화된다. | `app.js:renderQuestion/render*Input` |
| BR-P1-006 | 실전용 지문의 정답 토큰 검사 결과가 빈 목록이다. | Node 정적 검사 |

## 6. 일관성 검증 결과

### 규칙 간 충돌

| 규칙 A | 규칙 B | 충돌 유형 | 해결 |
|---|---|---|---|
| BR-P1-001 | BR-P1-002 | 모든 P1 통제를 자동 채점하려는 충돌 | 조건 의존 통제는 essay handler로 고정한다. |
| BR-P1-003 | BR-P1-005 | 데이터 확장과 실전 단서 제거의 충돌 | `examPrompt`를 선택 메타데이터로 두고 UI는 공통 renderer만 사용한다. |
| BR-P1-004 | BR-P1-006 | 근거 표시와 실전 단서 제거의 충돌 | 근거 분류는 학습 모드에만 표시한다. |

### 완전성 및 아키텍처 교차 검증

| 검증 항목 | 상태 | 비고 |
|---|---|---|
| 활성 주제 연결 | PASS 예정 | 기존 active topic만 사용한다. |
| 자동/자가 채점 경계 | PASS 예정 | handler contract로 검증한다. |
| 진행도 모델 | PASS | 새 상태·저장 필드가 없다. |
| UI 공통성 | PASS 예정 | 데이터 추가만으로 렌더한다. |
| 순환 참조 | PASS 예정 | question prerequisite DAG를 builder가 검사한다. |
