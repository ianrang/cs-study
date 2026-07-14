# 정보보안기사 실기 복습 앱 디자인 시스템

## 목적

이 문서는 화면의 시각적 단일 진실과 변경 규칙이다. 이 앱은 서버·번들러 없이 `index.html`을 직접 열어 동작해야 하므로, 프레임워크 컴포넌트 대신 표준 CSS 계층과 안정된 클래스 계약을 사용한다.

- 모든 화면 색상·간격·글꼴·반경·그림자는 토큰에서 파생한다.
- 라이트/다크 모드는 같은 semantic token 이름을 유지하며 값만 바꾼다.
- 콘텐츠 데이터는 화면 스타일을 갖지 않으며, `app.js`는 상태와 클래스 선택만 맡는다.

## 토큰 계층

`styles/tokens.css`가 시각 값의 단일 진실이다.

1. **기반 토큰**: spacing scale, type scale, radius, shadow, control size와 라이트/다크 원시 색상쌍을 `styles/tokens.css`에만 둔다.
2. **의미 토큰**: `--color-text-*`, `--color-surface-*`, `--color-border-*`, `--color-status-*`처럼 용도를 표현한다. 컴포넌트는 원시 색을 직접 참조하지 않는다.
3. **컴포넌트 토큰**: 버튼·입력·배지·패널이 자체 크기와 상태 값을 의미 토큰에서 조합한다.

토큰 파일 밖에서 새 hex/rgb/hsl 색상, 고정 spacing/typography/radius 값을 추가하지 않는다. CSS custom property를 쓸 수 없는 media query breakpoint만 예외이며, 그 값은 `styles/tokens.css`에 문서화한다.

## 테마와 다크 모드

- 기본값은 OS의 `prefers-color-scheme`이다.
- 헤더의 테마 버튼은 OS 상태와 무관하게 `시스템 → 다크 → 라이트 → 시스템`을 순환하며, 명시 선택만 `localStorage`에 저장하고 `html[data-theme]`만 변경한다.
- 저장된 선택값은 CSS가 로드되기 전에 적용되어 테마 전환 깜박임을 피한다.
- 각 테마는 foreground/background/border/status 조합을 semantic token 단위로 재정의한다. 컴포넌트 CSS나 JavaScript에 별도 dark-mode 분기가 없어야 한다.

## 컴포넌트 계약

| 컴포넌트 | 기본 계약 | 상태/변형 |
|---|---|---|
| Button | 동일한 높이, focus ring, disabled 처리 | primary, quiet, danger |
| Surface | 패널 배경·border·shadow 제공 | sidebar, practice panel, statistic(`surface-stat`) |
| Field | label·입력·focus ring 일관성 | short, cloze, essay |
| Badge | 상태 정보를 색과 텍스트로 함께 전달 | source, origin, progress, mode |
| Question step | 문항 이동과 진행 상태 제공 | unseen, attempted, mastered, review |
| Feedback | 채점 결과·모범 답안의 시각적 컨테이너 | correct, incorrect, self |

통계 카드는 `stat surface surface-stat`을 함께 사용한다. 따라서 panel 배경·border는 `surface`가 한 번만 소유하고 statistic의 radius/shadow 차이만 variant가 소유한다.

`app.js`는 위 컴포넌트의 class 이름을 선택할 수 있지만 색상·크기·레이아웃을 계산하거나 inline style을 설정하지 않는다. 전체 재렌더 뒤에는 feedback 또는 이동한 순서 항목으로 포커스를 복원한다.

## 파일 경계와 의존 방향

```
data/*.json ─┐
             ├─> practice-data.js ─┐
practice-core.js ───────────────────┼─> app.js ─> HTML class/state
index.html ─────────────────────────┘                 │
styles/tokens.css ─> styles/base.css ─> styles/components.css ┴─> styles/layout.css
                           (styles.css가 순서 고정)
```

CSS는 왼쪽에서 오른쪽으로만 의존한다. `styles/layout.css`는 컴포넌트의 색상값을 재정의하지 않고, `styles/components.css`는 페이지 배치를 소유하지 않는다.

## 유지보수 규칙

- 테마 변경은 `styles/tokens.css`의 semantic token만 수정한다.
- 공통 UI 변경은 `styles/components.css`의 해당 컴포넌트 계약만 수정한다.
- 페이지 배치 변경은 `styles/layout.css`에 한정한다.
- 새 상태는 HTML 텍스트·ARIA 상태·컴포넌트 variant·토큰을 함께 추가한다. `attempted`는 서술형의 모범 답안·채점 기준을 열었지만 자가 판정을 아직 선택하지 않은 상태다.
- 데이터 JSON, 생성된 `practice-data.js`, 문항 validator는 화면 리팩터링 범위가 아니다.

## 검증 규칙

`python3 scripts/check-design-system.py`는 CSS import·script 의존 순서, 필수 토큰/테마/컴포넌트, 통계 Surface 합성, 토큰 파일 밖의 raw color, inline style·JavaScript 스타일 조작을 검사한다. 콘텐츠 정합성은 `python3 scripts/build-practice-data.py --check`, 계약 회귀는 `python3 scripts/test-practice-contract.py`, 순수 상태 머신은 `node --test scripts/practice-core.test.js`, 실제 DOM 흐름은 `scripts/browser-contract-check.html`이 담당한다.
