# Architecture: 정보보안기사 실기 복습 문제 앱

## 1. 기술 스택

| 분류 | 기술 | 버전 |
|---|---|---|
| UI | HTML5, CSS3, 브라우저 기본 JavaScript | 현대 데스크톱 브라우저 호환 범위 |
| 콘텐츠 원본 | JSON | repository에서 사람이 검토·diff 가능 |
| 콘텐츠 검증/생성 | Python 3 표준 라이브러리 스크립트 | 외부 패키지 없음 |
| 영속성 | Browser LocalStorage | 계정·서버·외부 API 없음 |
| 배포 | 정적 파일 | `file://` 직접 열기와 정적 호스팅 모두 지원 |

브라우저는 `file://`에서 JSON fetch를 안정적으로 수행할 수 없으므로, 검증된 JSON 원본에서 생성한 `practice-data.js`를 일반 script로 로드한다. 따라서 직접 열기와 정적 호스팅 모두 같은 앱 동작을 사용한다.

## 2. 레이어 구조

```text
학습 문서·기출·Lab (read-only source)
                ↓ source_refs
JSON curriculum/question packs
                ↓ validate + generate
practice-data.js ──→ App state / grading engine ──→ HTML renderer
                               ↓                         ↓
                          LocalStorage              학습자 상호작용
```

의존 방향은 source → content → generated data → app → browser storage로 단방향이다. UI는 원본 학습 문서나 JSON을 직접 수정하지 않으며, LocalStorage는 문제 은행과 분리된 사용자 상태만 보관한다.

| 레이어 | 책임 | 허용 의존성 |
|---|---|---|
| Source references | 학습 사실·기출 검증 상태 제공 | 없음 |
| Content source | curriculum 및 문제/정답/rubric 선언 | Source references |
| Validator/build | 구조·근거·답 형식을 확인하고 browser data 생성 | Content source |
| Domain engine | 정규화·자동 채점·진행도 전이 | Generated data |
| UI renderer | 탐색, 문제 입력, 결과·근거 표시 | Domain engine |
| Persistence | 사용자 진행도 저장/복구/초기화 | Domain engine state |

## 3. 디자인 패턴

| 패턴 | 적용 위치 | 선택 이유 | 검토한 대안 |
|---|---|---|---|
| Schema-driven content | JSON question packs와 curriculum | 콘텐츠 추가 시 UI 코드를 수정하지 않고 근거/검증 상태를 강제할 수 있다. | HTML에 문항을 직접 작성: 직접 열기는 쉽지만 확장·검증·추적성이 약하다. |
| Strategy renderer/grader | question type별 render/normalize/grade 함수 | 단답·빈칸·순서·판정·자가채점을 같은 세션 흐름에서 일관되게 처리한다. | 하나의 거대 조건문: 유형 추가 시 결합도가 높다. |
| Pure state transition | 제출·정답 공개·자가평가·초기화 | 재풀이와 LocalStorage 복구가 결정적이며 테스트 가능하다. | DOM을 상태 저장소로 사용: 재렌더·복구 오류 위험이 높다. |
| Build-time validation | Python validator | 앱 실행 전에 ID·근거·정답·선수관계 오류를 차단한다. | 런타임 검증만 수행: 사용자에게 콘텐츠 오류가 노출된다. |

## 4. 데이터 모델

### CurriculumNode

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `id` | string | 전역 unique | 학습 경로/장·절 필터의 안정 식별자 |
| `title` | string | non-empty | 화면 표시명 |
| `sourceChapter` | string | `1`~`5` 또는 shared | 원본 정리 장 |
| `sourceSection` | string | source path와 일치 | 예: `2.3.2` |
| `learningPath` | string | registry enum | 사고 흐름 기반 탐색 그룹 |
| `prerequisites` | string[] | DAG, self-reference 금지 | 선수 학습 노드 |
| `status` | enum | active/future | V1 노출 상태 |

### StageDefinition

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `id` | string | 전역 unique | renderer/grader handler 식별자 |
| `label` | string | non-empty | 단계 필터와 카드 표시명 |
| `handler` | enum | short/cloze/order/essay | 재사용 가능한 입력·채점 상호작용 |
| `grading` | enum | auto/self | 자동 채점 또는 자가 채점 흐름 |

### Question

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `id` | string | 전역 unique, immutable | 진행도와 연결되는 문항 식별자 |
| `curriculumId` | string | 유효한 CurriculumNode | 문항 소속 |
| `stage` | enum | recall/cloze/order/decision/practical/essay | 단계별 학습 방식 |
| `prompt` | block[] | non-empty | 텍스트·코드·표시 단서 |
| `examPrompt` | block[]/optional | non-empty when present | 실전 모드 전용 지문. 주제·정답 후보를 불필요하게 드러내는 학습용 단서를 제거한다. |
| `questionKind` | optional enum | predicted only | 예상 문항임을 명시한다. 생략하면 실제 회차 참조 여부로 기출 기반/학습 문제를 화면에서 분류한다. |
| `answer` | typed object | stage와 호환 | 자동 채점 정답 또는 자가 채점 rubric |
| `explanation` | block[] | non-empty | 정답 근거와 오답 교정 |
| `sourceRefs` | ref[] | 최소 1개, excerpt가 실제 source line에 포함 | path, line, excerpt, verification 상태 |
| `tags` | string[] | controlled topic tags | 필터·복습용 |
| `prerequisites` | string[] | curriculum와 모순 금지 | 문항 수준 선수 개념 |

### Answer contract

- 단답·빈칸·판정은 `matchPolicy`를 반드시 선언한다. `case-insensitive`는 앞뒤 공백·연속 공백·대소문자를 정규화하고, `exact`는 입력값을 그대로 비교한다.
- 순서 문항은 item ID 배열을 비교한다. 드래그 앤 드롭은 배열 순서만 바꾸며, 키보드 대체 조작은 초점이 있는 항목의 `Alt`/`Option`+위·아래 화살표다.
- 서술형은 `keywordGroups`를 단일 기준으로 사용한다. 화면의 퍼센트는 각 그룹에 하나 이상의 용어가 포함됐는지 계산한 **키워드 충족률**이며, 정답·오답 또는 논리적 정확성 판정이 아니다.
- 기존 handler를 재사용하는 새 단계·문항·주제는 JSON만 추가한다. 완전히 새로운 상호작용은 `stageHandlers`의 단일 handler를 추가한 뒤 `StageDefinition.handler`로 연결하며, 여러 조건문을 수정하지 않는다.
- `실전 복합형`은 `cloze` handler를 재사용해 여러 결정적 빈칸을 하나의 설정 시나리오로 묶는다. 따라서 자동 채점 엔진을 복제하지 않으며, 답이 복수일 수 있는 실무 설계는 `essay` handler에 둔다.
- 문항 분류는 UI의 ID 조건문이 아니라 `sourceRefs`와 `questionKind`에서 단방향으로 계산한다. `01-rounds` 참조는 기출 기반, `questionKind: predicted`는 예상 문제, 나머지는 학습 문제다. validator는 예상 문항에 `08-prediction`과 `05-analysis` 근거를 모두 요구한다.

### ProgressRecord

| 속성 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `schemaVersion` | integer | current version | migration/폐기 판단 |
| `questionId` | string | 기존 Question ID | 문항 연결 |
| `attemptCount` | integer | 0 이상 | 재풀이 횟수 |
| `lastResult` | enum | correct/incorrect/self-understood/self-review | 마지막 학습 결과 |
| `masteryStatus` | enum | mastered/review | 이전 정답 완료를 보존하는 학습 상태 |
| `essayKeywordScore` | integer/null | 0~100 또는 null | 가장 최근 서술형 키워드 충족률 |
| `updatedAt` | ISO timestamp | browser generated | 마지막 상태 전이 |

### 관계

- CurriculumNode 1:N Question
- Question 1:0..1 ProgressRecord
- CurriculumNode N:N CurriculumNode via prerequisites, 단 방향 비순환 그래프

## 5. API 설계

외부 API는 없다. 앱 내부 경계는 다음의 순수 함수 계약으로 제한한다.

| 함수군 | 입력 | 출력 | 책임 |
|---|---|---|---|
| `loadData` | generated data | validated in-memory registry | data version과 참조 해석 |
| `grade` | Question, learner response | result, normalized response, feedback key | 결정적 자동 채점 |
| `transitionProgress` | ProgressRecord, action | next ProgressRecord | 제출·자가평가·초기화 상태 전이 |
| `selectQuestions` | filters, progress | Question[] | 장/경로/단계/복습 필요 필터 |
| `render` | app state | DOM update | 화면 갱신 |

## 6. 프로젝트 구조

```text
practice/
├── index.html                    # 직접 열 수 있는 앱 진입점
├── styles.css                    # 디자인 토큰·레이아웃·상태 스타일
├── app.js                        # 상태 조립, 유형별 renderer/grader 호출
├── practice-data.js              # JSON 원본에서 생성; 브라우저 로드용
├── data/
│   ├── curriculum.json           # 장/절·학습 경로·선수관계 registry
│   └── question-packs/
│       ├── network-firewall.json # 2장 네트워크·방화벽 문제 원본
│       └── service-security.json # 3장 서비스 보안설정 문제 원본
├── schemas/
│   └── question-bank.schema.json # 데이터 구조·enum 기준
├── scripts/
│   └── build-practice-data.py    # validate + practice-data.js 생성
└── README.md                     # 열기, 검증, 콘텐츠 추가 방법
```

- `data/`만 새 학습 콘텐츠의 편집 surface다. UI 코드와 생성 파일은 콘텐츠 추가 시 직접 수정하지 않는다.
- `practice-data.js`는 generated artifact다. JSON 원본과 validator의 결과로만 갱신한다.
- `app.js`는 data-driven renderer이며, 원본 문서·Lab을 읽거나 쓰지 않는다.
- 문제 pack 파일명은 lowercase kebab-case, 문항 ID는 `<curriculum-id>-<sequence>`로 고정한다.

### UI 정보 구조

```text
App shell
├── 학습 경로 필터: curriculum의 active learningPath
├── 원본 장/절 필터: curriculum의 sourceChapter/sourceSection
├── 세부 주제 필터: CurriculumNode
├── 단계 필터: curriculum의 stage registry
├── 문항 상태 탐색: 현재 필터의 1..n 번호 상자·미풀이/풀이함/정답 완료/복습 필요
├── 문제 카드: 단서, 코드, 입력, 제출
├── 결과 카드: 정오답 또는 키워드 충족률/모범답/감점 위험/해설/근거·검증 상태
└── 진행도: 완료·복습 필요·현재 문항/선택 범위/전체 초기화
```

자동 채점 문제는 결과 카드가 즉시 열리고, 서술형은 키워드 충족률과 누락 항목을 본 뒤 자가 채점 버튼으로 `이해함/복습 필요` 중 하나를 기록한다. 정답 완료와 최근 복습 필요 상태는 분리해 표시하며, 상단 번호 상자의 색은 동일한 `ProgressRecord`에서 계산한다. 근거 path·line·excerpt·verification 상태는 결과 카드의 최하단에서 확인한다. LocalStorage가 차단되면 비영속 풀이를 유지하되 화면에 경고한다.

## 7. 검증 결과

| 항목 | 상태 | 비고 |
|---|---|---|
| 순환 참조 | PASS | Source → Content → Build → App → Storage의 단방향 구조다. |
| 계층 깊이 | PASS | UI는 renderer/grader/state helper를 직접 호출하며 직렬 호출 깊이를 4단계 미만으로 유지한다. |
| 캡슐화 | PASS | ProgressRecord는 LocalStorage adapter만 접근하고, UI는 원본 콘텐츠를 변경하지 않는다. |
| 요구사항 커버리지 | PASS | PRD FR-1~8은 curriculum, question schema, grader, self-review, persistence, validator, Lab reference로 매핑된다. |
| 기술 스택 정합성 | PASS | 외부 라이브러리·fetch 없이 script-loaded generated data를 사용해 직접 열기와 정적 배포를 모두 지원한다. |

## 8. 리스크

- 복원 기출의 문구·답이 공식 원문과 다를 수 있다. 대응: source-derived 상태를 노출하고, 자동 채점 정답은 검증된 문법/명령과 분리해 source refs를 강제한다.
- 정답 변형이 많은 서술형을 자동 채점하면 오판할 수 있다. 대응: V1은 서술형 자동 채점을 금지하고 rubric 자가 채점으로 제한한다.
- LocalStorage 삭제/차단 시 진행도가 사라질 수 있다. 대응: 문제 풀이 자체는 무상태로 유지하고, 저장 불가 상태를 UI에 알린다.
- JSON 원본과 generated data가 어긋날 수 있다. 대응: validator가 생성까지 맡고 README에 단일 갱신 명령을 제공한다.
- 단일 화면에 정보가 많으면 코드/해설 가독성이 떨어질 수 있다. 대응: 문제·정답·근거를 단계적으로 공개하고, 코드 블록과 키보드 포커스 상태를 명확히 구분한다.
