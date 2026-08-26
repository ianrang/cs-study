# Architecture: 기출 복원 보기·코드 블록 렌더링

## 1. 목적과 비목적

기출 복원 지문의 코드·명령·설정·패킷 흐름을 본문과 시각적으로 분리해 읽기 쉽게 한다. 회차 MD를 검증·보완 가능한 콘텐츠 SSOT로 유지하고, 513개 문항의 ID·출처 연결과 `source-derived` 상태는 바꾸지 않는다.

다음은 범위 밖이다.

- 문항별 HTML·CSS·JavaScript 하드코딩
- Markdown 전체 문법 또는 임의 HTML 해석
- 기출 답안의 자동 채점 전환
- 회차 MD의 문장·정답을 UI 편의를 위해 추론·보충하는 작업

## 2. 현재 구조와 변경 지점

```text
round MD (content SSOT)
  -> past_exam_converter.py (문법 검증·문자열 보존)
  -> past-exams.json (generated)
  -> practice-data.js (generated)
  -> app.js formatPastExamText (escape 후 안전한 블록 렌더링)
  -> components.css (semantic block style)
```

의존 방향은 기존과 동일하게 단방향이다. MD는 문항별 HTML·CSS·JavaScript가 아니라 제한 marker로 보기 의미만 선언하고, UI는 생성 데이터나 MD를 수정하지 않는다.

## 3. 제안 마커 계약

표 셀 한 줄 안에서 사용할 수 있고, 기존 `<br>` 계약과 충돌하지 않는 제한 마커를 사용한다.

```text
{{code:bash}}iptables -A INPUT -p tcp --dport 22 -j ACCEPT{{/code}}
{{reference}}Client -> SYN -> Server\nServer -> SYN/ACK -> Client{{/reference}}
```

| marker | 용도 | 렌더링 |
|---|---|---|
| `{{code}}...{{/code}}` | 언어 미지정 명령·설정 | `pre > code` |
| `{{code:bash}}...{{/code}}` | bash, shell, config 등 언어 힌트가 있는 명령·설정 | `pre > code` + `data-language` |
| `{{reference}}...{{/reference}}` | 패킷 흐름, 설정값 표, 보기 묶음 | 의미 있는 reference block |

- 허용 언어 이름은 `bash`, `shell`, `config`, `http`, `snort`, `sql`, `text`처럼 소문자 영숫자·하이픈만 허용한다.
- 내용은 마커 내부에서 다시 파싱하지 않는다. `<br>`은 줄바꿈으로, `\n`은 블록 안의 줄바꿈으로만 변환한다.
- 중첩 마커, 빈 블록, 닫히지 않은 마커, 지원하지 않는 언어는 변환 단계에서 실패한다.
- 기존 inline backtick은 짧은 토큰·옵션명에 계속 사용한다. 한 줄 이상의 명령·설정·패킷 교환만 block marker를 사용한다.

## 4. 렌더링 패턴과 안전성

`formatPastExamText`의 순서는 다음으로 고정한다.

1. 전체 원문을 HTML escape한다.
2. 변환기가 검증한 제한 마커만 placeholder로 인식한다.
3. marker 내부의 escape된 텍스트를 `pre > code` 또는 reference block으로 복원한다.
4. 기존 리터럴 `<br>`과 legacy label만 현재 규칙대로 줄바꿈으로 복원한다.

따라서 회차 MD의 `<script>`, 임의 태그, 속성은 항상 텍스트로 남는다. `innerHTML`에 원문 HTML을 직접 전달하거나 문항 ID별 예외 분기를 두지 않는다.

## 5. 스타일 및 접근성

| 요소 | 요구사항 |
|---|---|
| 코드 블록 | `pre > code`, 가로 overflow, 읽기 쉬운 고정폭 글꼴, 색상은 semantic token만 사용 |
| reference block | `aside` 또는 `section`과 `aria-label="보기"`, 본문과 구분되는 surface·border token 사용 |
| 모바일 | 긴 명령은 줄바꿈을 훼손하지 않고 가로 스크롤 가능 |
| 복사 | 브라우저 기본 텍스트 선택·복사가 가능하며 별도 버튼은 추가하지 않음 |
| 실전 모드 | 지문 블록은 그대로 표시하고 답안·검증 문구만 기존 정책대로 숨김 |

새 CSS는 `styles/components.css`에 semantic class만 추가한다. raw color, inline style, 문항별 selector는 금지한다.

## 6. 데이터 모델과 호환성

`PastExamItem`의 `prompt`, `answer`, `verification`은 모두 기존 `string` 타입을 유지한다. JSON schema·converter 출력 형식·ID·digest **계산 규칙**은 변경하지 않는다. 새 marker는 문자열 내부의 제한된 작성 규칙일 뿐 별도 AST·양방향 참조·새 API가 아니다. converter는 `prompt`·`answer`의 marker만 검증하고, UI는 같은 두 필드만 block renderer에 전달한다.

marker가 없는 문항은 기존 inline·줄바꿈 렌더링을 유지한다. 근거 확인으로 문항을 보완하거나 marker를 추가하면 현재 MD digest가 갱신되며, 생성물을 반드시 재빌드한다.

## 7. 구현 및 검증

1. converter에 marker 형식·중첩·빈 블록 검증을 추가했다.
2. `formatPastExamText`를 pure block renderer로 분리하고 HTML escape 우선 순서를 테스트한다.
3. `components.css`에 generic `exam-code-block`, `exam-reference-block`만 추가했다.
4. 실제 R07~R13 기출의 18개 문항에서 명령·Snort 룰·서버 설정·TCP 흐름을 20개 marker로 보강했다.
5. 아래 검증을 통과한 뒤에만 다른 회차의 원문에 확장한다.

| 검증 | 기대 결과 |
|---|---|
| converter fixture | 유효 marker 보존, 잘못된 marker build 실패 |
| content contract | 31회차·513문항·ID·`source-derived` 상태 유지, 현재 MD와 source/content digest 일치 |
| renderer unit | HTML escape, code/reference block, `<br>`, legacy label 공존 |
| browser contract | 실전/학습 모드 모두 block 가독성·정답 공개 흐름 유지 |
| design-system check | token·cascade·inline style 규칙 준수 |

## 8. 선택과 기각한 대안

| 대안 | 결정 | 이유 |
|---|---|---|
| 제한 marker + generic renderer | 선택 | 원본·생성물·UI 경계를 유지하며 필요한 표현력만 제공 |
| 문항별 HTML 저장 | 기각 | XSS·하드코딩·표현 불일치 위험 |
| 전체 Markdown parser 도입 | 기각 | 정적 앱의 요구보다 범위가 크고 표 셀 파싱 복잡성을 늘림 |
| JSON에 별도 보기 배열 추가 | 기각 | MD SSOT를 깨고 source/derived 이중 관리 발생 |

## 9. 자체 검증

| 항목 | 결과 |
|---|---|
| 순환 참조 | 없음. MD → converter → generated data → UI 단방향 유지 |
| 계층 깊이 | 기존 converter·renderer 경계 안의 검증/표현 확장으로 4단계 이하 |
| 캡슐화 | marker 문법은 converter, 표현은 renderer, 색상은 CSS token 계층이 각각 소유 |
| 하드코딩 방지 | 문항 ID가 아닌 generic marker와 generic CSS class만 사용 |
| 기존 계약 호환 | 문자열 schema·513문항 파생·`source-derived` 상태 유지 |
