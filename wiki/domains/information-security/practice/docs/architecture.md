# Architecture: 정보보안기사 실기 복습 앱 UI 시스템

## 1. 기술 스택

| 분류 | 기술 | 역할 |
|---|---|---|
| Markup | HTML5 | 정적 shell과 접근 가능한 기본 구조 |
| Styling | CSS custom properties + cascade layers | token/theme/component/layout 분리 |
| Behavior | browser JavaScript IIFE + pure core | 필터, 문항 렌더링, LocalStorage, theme preference |
| Content | learning JSON + round MD → generated browser data | 학습 문항·커리큘럼·기출 복원 source of truth |

번들러·외부 API·데이터베이스는 사용하지 않는다. `file://`로 직접 열 수 있어야 한다.

## 2. 레이어 구조

```
learning JSON ─┐
round MD ──────┼─> build-practice-data.py -> generated JSON + practice-data.js -> app.js -> DOM state/classes
               └─> past_exam_converter.py (read-only)
practice-core.js --------------------------------------------------^  (theme·문항 분류·선수 순서 순수 로직)
styles/tokens.css -> styles/base.css -> styles/components.css -> styles/layout.css -> rendered style
```

- 학습 JSON과 회차 MD는 presentation을 모른다. 회차 MD는 문항·답안의 읽기 전용 SSOT이고, 기출 JSON은 생성물이다.
- app.js는 theme preference와 semantic class를 선택하지만 색상값을 소유하지 않는다. `practice-core.js`는 theme state machine, 복원 기출 판정, 선수 문항 정렬을 소유하며 Node 기본 테스트로 검증한다.
- token layer만 raw visual value를 소유한다.
- component layer는 semantic token을 소비한다.
- layout layer는 화면 배치와 breakpoint만 소유한다.

각 화살표는 단방향이며, CSS/JS가 콘텐츠 원본을 수정하지 않는다.

## 3. 디자인 패턴

| 패턴 | 적용 위치 | 선택 이유 | 기각한 대안 |
|---|---|---|---|
| three-tier design tokens | tokens → semantic → component | 테마를 한 곳에서 바꾸고 의미를 보존 | 컴포넌트별 직접 색상 |
| CSS cascade layers | style entrypoint | import 순서와 override 소유권 고정 | 단일 대형 stylesheet |
| class-based state | app.js + component CSS | inline style 없이 상태 표시 | DOM style mutation |
| registry strategy | stageHandlers | 문항 handler 확장 시 분기 집중 방지 | stage별 거대 조건문 |

## 4. 데이터 모델

브라우저는 세 종류의 LocalStorage만 사용한다.

| 키 | 소유자 | 내용 | 제약 |
|---|---|---|---|
| `info-security-practice-progress-v1` | app.js | 학습 문항 풀이 기록 | `attempted`/`mastered`/`review`, schemaVersion 1 유지 |
| `info-security-past-exam-progress-v1` | app.js | 기출 복원 풀이 기록 | 학습 문항 진행도와 분리, schemaVersion 1 유지 |
| `info-security-practice-theme-v1` | app.js | `light` 또는 `dark` | 값이 다르면 OS preference 사용 |

학습 문항 JSON 계약은 유지한다. 기출 복원은 `schemas/past-exam-bank.schema.json`과 `data/generated/past-exams.json`의 파생 계약을 따르며, 원본 MD에 역기록하지 않는다.

## 5. API 설계

해당 없음. 앱은 외부 네트워크 API를 호출하지 않는다.

## 6. 프로젝트 구조

```
practice/
├── index.html              # semantic shell, CSS/JS entrypoint
├── app.js                  # interaction and rendering state
├── practice-core.js         # testable theme·문항 분류·선수 순서 순수 로직
├── styles.css              # ordered CSS entrypoint
├── styles/
│   ├── tokens.css          # raw + semantic + component tokens, themes
│   ├── base.css            # reset and element defaults
│   ├── components.css      # reusable UI component contracts
│   └── layout.css          # shell, responsive layout, page composition
├── scripts/
│   ├── build-practice-data.py
│   ├── past_exam_converter.py
│   ├── check-design-system.py
│   ├── test-practice-contract.py
│   └── browser-contract-check.html
├── data/                   # editable content source
│   └── generated/           # round MD에서 생성된 기출 JSON (직접 수정 금지)
└── practice-data.js        # generated browser data
```

## 7. 검증 결과

구현 뒤 design-system guard, JavaScript syntax check, generated data freshness check, content contract unit test, theme/progress state-machine unit test, browser contract check(기출 필터·자가 채점·분리 저장소 포함), 그리고 source-level architecture review를 실행한다. 실제 브라우저의 시각적 품질은 별도 사용자 확인 영역이다.

## 8. 리스크

- CSS custom property를 지원하지 않는 구형 브라우저는 지원 범위가 아니다.
- raw `file://` 환경에서 module script를 쓰면 브라우저 제약을 받을 수 있으므로 IIFE script를 유지한다.
- CSS만으로 breakpoint 값을 재사용할 수 없으므로 breakpoint는 `styles/tokens.css` 주석과 `styles/layout.css`에만 둔다.
