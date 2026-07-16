# 정보보안기사 실기 복습 문제 앱

현재 학습한 1장 P1 시스템 보안, 2장 네트워크·방화벽, 3장 P1 서비스 보안설정, 5장 P1 관리체계·위험관리·업무연속성·침해사고·포렌식·개인정보 기초 범위를 반복하기 위한 정적 브라우저 앱이다. 회차별 기출 복원은 원본 MD를 읽기 전용으로 변환해 별도 필터에서 반복 풀이한다. 실제 방화벽·네트워크 장비를 조작하지 않으며, 기존 `../labs/`의 offline 실습과 별도로 동작한다.

## 열기

`index.html`을 브라우저로 직접 연다. 외부 API·서버는 필요 없다.

## 디자인 시스템과 테마

- 화면 스타일의 진입점은 `styles.css`이며, `styles/tokens.css → styles/base.css → styles/components.css → styles/layout.css` 순서로만 적용된다.
- 색상·spacing·typography·radius·shadow의 값은 `styles/tokens.css`가 단일 진실이다. 컴포넌트와 레이아웃에는 raw color 또는 고정 dimension을 직접 추가하지 않는다.
- 기본 테마는 운영체제 설정을 따른다. 헤더의 테마 버튼은 `시스템 → 다크 → 라이트 → 시스템`을 순환하며 명시 선택을 이 브라우저에 저장한다.
- 상세 계약은 `DESIGN.md`, 구조 근거는 `docs/architecture.md`를 따른다.

```bash
python3 scripts/check-design-system.py
python3 scripts/test-practice-contract.py
node --test scripts/practice-core.test.js
```

첫 명령은 CSS 계층·script 의존 순서, 필수 토큰·테마·컴포넌트, token 파일 밖의 raw color/dimension, inline style과 JavaScript style mutation을 검사한다. 두 번째는 UI가 요구하는 curriculum·question metadata 계약의 결함을, 세 번째는 테마·진행 상태 머신을 검사한다. `scripts/browser-contract-check.html`을 직접 열면 테마 순환, feedback·순서 항목 포커스 복원, attempted 상태, future topic label, Surface 합성을 실제 DOM에서 검사해 `PASS` 또는 `FAIL`을 표시한다.

## 학습 흐름

1. 좌측에서 `학습 문항` 또는 `기출 복원`을 고른다. 학습 문항은 학습 경로·원본 장/절·세부 주제·단계를, 기출 복원은 연도·회차·문항 유형을 필터링한다. 전체·주제 기준 기본 순서는 선수 문항을 의존 문항보다 먼저 보이게 하며, 단계 필터를 선택하면 해당 단계만 본다.
2. 좌측 필터는 현재 선택 범위를 요약해 보여 주며 `필터 해제`로 한 번에 되돌릴 수 있다. 문제 상단의 번호 상자로 문항을 이동한다. 미풀이·풀이함·정답 완료·복습 필요 상태가 색으로 표시된다. 단답은 `Enter`로 정답을 확인하고, 빈칸형은 `Enter`로 다음 빈칸으로 이동한 뒤 마지막 빈칸에서 정답을 확인한다. 순서 문제는 드래그 앤 드롭으로 정렬하며, 키보드에서는 항목에 초점을 둔 뒤 `Alt`(macOS는 `Option`)+위·아래 화살표를 사용한다. 서술형은 줄바꿈을 보존하므로 `Enter`로 제출하지 않는다.
3. `학습` 모드는 입력 의미·문항 분류·근거 상태를 보조로 표시한다. `실전` 모드는 주제·단계·분류·상세 입력 라벨을 숨긴다. 기출 복원은 답안을 직접 작성한 뒤 복원 답안·검증 문구를 공개하고, `정답 완료` 또는 `복습 필요`로 자기 채점한다.
4. `실전 복합형`은 여러 빈칸을 하나의 설정/판독 시나리오로 묶되, 각 빈칸의 답이 결정적인 경우에만 자동 채점한다. 여러 정상 답이 가능한 설계 문제는 서술형 자가 채점으로 유지한다.
5. 서술형은 키워드 충족률·누락 항목·모범 답안·감점 위험을 보고 `이해함` 또는 `복습 필요`를 기록한다. 모범 답안을 열고 아직 자가 판정을 고르지 않은 문항은 `풀이함`으로 표시된다. 키워드 충족률은 정오답 판정이 아니다.
6. 진행도는 현재 브라우저의 LocalStorage에 저장된다. `풀이함`, `정답 완료`, `복습 필요`는 서로 다른 의미이며 현재 문항·현재 선택 범위·전체 단위 초기화가 가능하다. 초기화는 해당 범위의 진행도와 미제출 서술형 초안을 함께 지우고 집계를 즉시 다시 계산한다. 정답·해설 뒤의 `근거와 검증 상태`에서 출처를 확인한다. 저장소가 차단된 환경에서는 경고를 표시하고 비영속 풀이로 계속한다.

## 문제 콘텐츠 갱신

문제 원본은 `data/` 아래 JSON 파일이다. `practice-data.js`를 직접 수정하지 않는다.

```bash
python3 scripts/build-practice-data.py
python3 scripts/build-practice-data.py --check
```

- 첫 번째 명령은 JSON schema 필수 필드·선수 문항 관계·source path/line/excerpt·정답 형식을 검증하고, 원본 회차 MD를 `data/generated/past-exams.json`으로 파생한 뒤 브라우저용 `practice-data.js`를 생성한다.
- 두 번째 명령은 검증뿐 아니라 생성 파일이 최신 원본과 일치하는지 확인한다.

## 콘텐츠 작성 규칙

- 모든 문항에는 고유 `id`, `curriculumId`, 단계, `prerequisites`, 해설, `sourceRefs`, tags가 필요하다. 단계는 `data/curriculum.json`의 stage registry에서 정의하며 `short`, `cloze`, `order`, `essay` handler 중 하나를 재사용한다.
- 자동 채점은 단답·빈칸·순서·판정처럼 답이 결정적인 문항에만 사용하며, 단답·빈칸·판정에는 `matchPolicy`를 명시한다. 현재 기본값은 `case-insensitive`; 비밀번호·해시처럼 대소문자가 의미 있는 값은 `exact`를 사용한다.
- 서술형은 `modelAnswer`, `keywordGroups`, `deductionRisks`를 제공하고 자동 채점하지 않는다. `keywordGroups`는 키워드 충족률과 누락 항목을 표시하는 단일 기준이다.
- 각 `sourceRefs`에는 실제 근거 줄에 포함된 `excerpt`와 검증 상태를 쓴다. locator가 빈 줄·코드 펜스·무관한 줄을 가리키면 build가 실패한다.
- 실제 회차 데이터셋(`../datasets/info-sec-engineer-practical-past-exams/01-rounds/`) 근거와 복원한 실전 지문(`examPrompt`)을 함께 가진 문항만 `기출 기반 · 복원 문항`으로 표시한다. 회차 자료를 근거로만 인용한 문항은 `학습 문제`로 표시한다. 어느 경우든 공식 원문 보장을 뜻하지 않으므로 `source-derived` 상태를 함께 확인한다.
- `questionKind: predicted` 문항은 `예상 문제 · 분석 근거`로만 표시한다. validator는 예상 문항에 예측 목록(`08-prediction`)과 패턴 분석(`05-analysis`) 근거를 모두 요구한다. 예상 문항을 기출 기반으로 표기하면 안 된다.
- 그 밖의 문항은 학습 문제다. 이 분류는 근거 검증 상태(`official`/`source-derived`/`inferred`)와 별개다.
- 원본 학습 노트·기출 데이터·Lab은 read-only source다.
- 기출 복원 MD(`../datasets/info-sec-engineer-practical-past-exams/01-rounds/`)는 `scripts/past_exam_converter.py`가 읽기 전용으로 변환한다. `data/generated/past-exams.json`과 `practice-data.js`는 생성물이므로 직접 수정하지 않는다.
