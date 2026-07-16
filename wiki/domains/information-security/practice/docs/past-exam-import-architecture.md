# Architecture: 기출 복원 MD Practice 바인딩

## 1. 목적과 경계

`datasets/info-sec-engineer-practical-past-exams/01-rounds/*.md`의 회차별 복원 문항을 수정하지 않고, 결정적으로 파생한 JSON으로 Practice에서 풀이한다.

- 회차 MD는 문항·답·복원 근거의 SSOT이며 읽기 전용이다.
- `practice/data/question-packs/*.json`은 학습용 구조화 문항의 SSOT로 유지한다.
- 변환 결과인 `data/generated/past-exams.json`을 감사 가능한 파생물로 남기고, 이를 포함한 `practice-data.js`만 브라우저에 전달한다.
- 변환기와 UI는 회차 MD에 링크·메타데이터·학습 결과를 역기록하지 않는다.

## 2. 현재 근거

- 회차 문서 아키텍처는 회차별 문항·답의 SSOT를 `*-practical-*.md`에 두고, 역방향 참조와 본문 복제를 금지한다 (`../../datasets/info-sec-engineer-practical-past-exams/00-management/document-architecture.md:72-93`).
- 31개 회차 파일은 모두 `## Reconstruction`과 동일한 5열 표 헤더(`no`, `type`, `reconstructed prompt`, `answer`, `verification`)를 사용한다.
- 전수 검사 결과는 31개 파일·513개 문항이며, 번호는 각 회차에서 1부터 연속이고 빈 셀·열 수 오류는 없다. 유형 분포는 short 310개, essay 171개, practical 32개다. 이 집계는 빈도 분석의 513문항 기준과 일치한다 (`../../datasets/info-sec-engineer-practical-past-exams/05-analysis/frequency-analysis.md:23-45`).
- 표 셀에 escape된 파이프(`\|`)를 포함한 행이 9개 있으므로, 단순 `split("|")` 구현은 금지한다.
- 현재 Practice는 JSON pack을 검증한 뒤 하나의 생성 파일로 합치며, 브라우저는 그 생성 파일만 읽는다 (`../scripts/build-practice-data.py`).

## 3. 레이어와 의존 방향

```text
round MD (read-only SSOT) ─> past_exam_converter.py ─> past-exams.json ─┐
                                                                         ├─> build-practice-data.py ─> practice-data.js ─> app.js
question-pack JSON (SSOT) ──────────────────────────────────────────────┘                                      ↕
                                                                                                  localStorage (progress only)
```

- `past_exam_converter.py`는 회차 파일의 frontmatter·표를 읽어 파생 레코드를 만든다.
- `build-practice-data.py`가 기존 학습 문항과 파싱된 기출 레코드를 한 번에 생성한다.
- `app.js`는 데이터 종류별 렌더러를 선택할 뿐, 원문·정답을 재구성하거나 저장하지 않는다.
- LocalStorage의 `info-security-past-exam-progress-v1` 키에 `R31-Q01` 같은 item ID별 진행 상태만 저장한다. 기존 학습 진행도 키와 회차 MD 모두와 독립된다.

## 4. 파생 데이터 모델

```text
PastExamRound
  roundId: "R31"
  year: "2026"
  session: "01"
  title: string
  documentProvenance: string
  status: "source-derived"
  sourcePath: string
  sourceDigest: SHA-256 string
  items: PastExamItem[]

PastExamItem
  id: "R31-Q01"
  number: 1
  type: "short" | "essay" | "practical"
  prompt: string
  answer: string
  verification: string
  sourcePath: string
  sourceLine: integer
  sourceRef: { path, line, excerpt, status: "source-derived" }
  contentDigest: SHA-256 string
```

`answer`는 자동 채점용 accepted 목록으로 변환하지 않는다. 회차 MD의 답안은 서술·복수 답·복원 설명을 포함하므로, 화면에는 자유 답안 입력 후 정답 공개와 자기 채점(정답/복습 필요)만 제공한다.

## 5. 변환 계약

1. 파일 탐색 범위는 `01-rounds/*-practical-*.md`로 고정한다.
2. frontmatter의 `title`, `provenance`와 `## Reconstruction`의 고정 헤더를 확인한다.
3. 표 행은 번호, 유형, 복원 지문, 답안, 검증 문구가 모두 비어 있지 않아야 한다.
4. 회차 ID는 파일명의 마지막 회차 번호, item ID는 표의 번호로 결정한다.
5. 표의 escape된 파이프(`\|`)는 셀 안의 문자 `|`로 복원한다. 열 수가 맞지 않거나 번호가 중복·비연속이면 빌드를 실패시킨다.
6. 모든 기출 레코드는 `source-derived`로 표시한다. 변환기는 공식 원문 여부를 승격하지 않는다.
7. 회차 MD 변경으로 `past-exams.json` 또는 `practice-data.js`가 달라지면 `--check`가 stale 상태로 실패해야 한다.

## 6. UI와 학습 흐름

- 상단 학습 종류에서 `학습 문항`과 `기출 복원`을 분리한다.
- 기출 복원은 회차·연도·유형(short/essay/practical) 필터와 회차 내 문항 이동을 제공한다.
- 실전 모드에서는 답안·검증 문구를 숨기고, 사용자가 공개를 선택한 뒤 자기 채점한다.
- 화면에는 `기출 복원·파생 근거`와 원본 `sourcePath:line`을 표시한다. `공식 기출`이라는 표현은 사용하지 않는다.
- 대화형 학습은 서술 답안의 논리·누락·표현 교정에 계속 사용한다. Practice는 시간 제한 회차 풀이와 오답 누적에 사용한다.

## 7. 검증

| 범주 | 검증 |
|---|---|
| MD 파싱 | 31개 회차 전체 파싱, ID 유일성, 번호 연속성, 필수 셀·frontmatter 검증 |
| 회귀 | escape 파이프, 코드 인라인, short/essay/practical 행을 포함한 fixture 검증 |
| 생성 | 기존 question-pack 계약, 기출 변환 계약, `practice-data.js --check` |
| UI | 학습/기출 필터 분리, 정답 비공개·공개, 자기 채점 진행도, 새로고침 후 진행도 복원 |
| 출처 | 모든 기출 item의 `sourcePath`, `sourceLine`, `source-derived` 상태 검증 |
| 전수 무결성 | 입력 31개 파일·513개 행과 파생 31개 회차·513개 item의 수, ID, 지문·답안·검증 문구를 대조 |

## 8. 제외 범위

- 회차 MD 자동 수정·보강
- 기출 답안을 자동으로 short/cloze/essay 정답 JSON으로 추론하는 기능
- 회차 MD에서 학습 문항으로의 역링크 생성
- 기출 문항을 기존 학습 question pack에 복제하는 기능
- 외부 네트워크·LLM 호출 또는 하드코딩 회차 목록
