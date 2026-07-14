# Architecture: 정보보안기사 실기 복습 앱 UI 시스템

## 1. 기술 스택

| 분류 | 기술 | 역할 |
|---|---|---|
| Markup | HTML5 | 정적 shell과 접근 가능한 기본 구조 |
| Styling | CSS custom properties + cascade layers | token/theme/component/layout 분리 |
| Behavior | browser JavaScript IIFE + pure core | 필터, 문항 렌더링, LocalStorage, theme preference |
| Content | JSON → generated browser data | 문항과 커리큘럼 source of truth |

번들러·외부 API·데이터베이스는 사용하지 않는다. `file://`로 직접 열 수 있어야 한다.

## 2. 레이어 구조

```
content data -> practice-data.js -> app.js -> DOM state/classes
practice-core.js ------------------^  (theme state machine)
styles/tokens.css -> styles/base.css -> styles/components.css -> styles/layout.css -> rendered style
```

- content data는 presentation을 모른다.
- app.js는 theme preference와 semantic class를 선택하지만 색상값을 소유하지 않는다. 순수 상태 전이(`practice-core.js`)는 Node 기본 테스트로 검증한다.
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

브라우저는 두 종류의 LocalStorage만 사용한다.

| 키 | 소유자 | 내용 | 제약 |
|---|---|---|---|
| `info-security-practice-progress-v1` | app.js | 문항별 풀이 기록 | `attempted`/`mastered`/`review`, schemaVersion 1 유지 |
| `info-security-practice-theme-v1` | app.js | `light` 또는 `dark` | 값이 다르면 OS preference 사용 |

문항 JSON·schema·생성 데이터의 계약은 변경하지 않는다.

## 5. API 설계

해당 없음. 앱은 외부 네트워크 API를 호출하지 않는다.

## 6. 프로젝트 구조

```
practice/
├── index.html              # semantic shell, CSS/JS entrypoint
├── app.js                  # interaction and rendering state
├── practice-core.js         # testable theme state machine
├── styles.css              # ordered CSS entrypoint
├── styles/
│   ├── tokens.css          # raw + semantic + component tokens, themes
│   ├── base.css            # reset and element defaults
│   ├── components.css      # reusable UI component contracts
│   └── layout.css          # shell, responsive layout, page composition
├── scripts/
│   ├── build-practice-data.py
│   ├── check-design-system.py
│   ├── test-practice-contract.py
│   └── browser-contract-check.html
├── data/                   # editable content source
└── practice-data.js        # generated browser data
```

## 7. 검증 결과

구현 뒤 design-system guard, JavaScript syntax check, generated data freshness check, content contract unit test, theme/progress state-machine unit test, browser contract check, 그리고 source-level architecture review를 실행한다. 실제 브라우저의 시각적 품질은 별도 사용자 확인 영역이다.

## 8. 리스크

- CSS custom property를 지원하지 않는 구형 브라우저는 지원 범위가 아니다.
- raw `file://` 환경에서 module script를 쓰면 브라우저 제약을 받을 수 있으므로 IIFE script를 유지한다.
- CSS만으로 breakpoint 값을 재사용할 수 없으므로 breakpoint는 `styles/tokens.css` 주석과 `styles/layout.css`에만 둔다.
