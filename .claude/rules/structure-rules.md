# 프로젝트 구조 규칙

이 문서는 cs-study의 authored 5개 tree와 `projects/`의 폴더 구조, 파일 배치, 네이밍을 정의한다. `raw/`, `wiki/`, `_meta/`, `scripts/`에는 각 계층의 schema와 architecture 규칙을 적용한다.

---

## 1. 최상위 분류 (Depth 1)

모든 authored 학습 콘텐츠는 다음 5개 카테고리 중 하나에 속한다. 실행 코드·테스트·프로젝트 문서는 이 분류와 분리해 `projects/<project>/`에 둔다.

| 카테고리 | 폴더 | 정의 | 판별 기준 |
|----------|------|------|-----------|
| CS 이론 | `cs/` | 컴퓨터 과학의 이론과 지식 | "이것은 CS 이론/원리인가?" |
| 프로그래밍 언어 | `lang/` | 특정 프로그래밍 언어의 문법, 특성, 내부 동작 | "특정 언어를 학습하는 것인가?" |
| 코딩 테스트 | `coding-test/` | 코딩 테스트 준비를 위한 커리큘럼과 실습 | "코딩 테스트 준비 목적인가?" |
| 개발 도구 | `tools/` | 개발 과정에서 사용하는 도구의 사용법 | "개발할 때 쓰는 도구인가?" |
| 개발 실무 | `development/` | 소프트웨어를 설계하고 만드는 방법론과 실무 지식 | "소프트웨어를 어떻게 만드는가?" |

`projects/`는 여섯 번째 학습 카테고리가 아니다. 각 하위 디렉터리는 독립 실행·테스트 가능한 프로젝트 경계이며 `wiki/`의 knowledge migration 입력에서 제외한다. 프로젝트가 지식 원본을 참조할 때는 repo-relative 단방향 경로를 사용하고 canonical 지식을 프로젝트 문서에 복제하지 않는다.

프로젝트 Markdown은 일반 문서로 유지하고 `tier`, `page_type`, `source_paths` 등 `wiki/` 전용 frontmatter를 두지 않는다. 프로젝트 계약은 본문과 프로젝트별 실행 테스트가 검증한다.

### 분류 판별 순서

하나의 주제가 여러 카테고리에 해당할 수 있을 때, 다음 순서로 판별한다:

1. 코딩 테스트 목적이면 → `coding-test/`
2. 특정 도구의 사용법이면 → `tools/`
3. 특정 언어에 종속된 내용이면 → `lang/`
4. 개발 방법론/설계/실무이면 → `development/`
5. 위 어디에도 해당하지 않는 이론이면 → `cs/`

### 배치 예시

| 주제 | 카테고리 | 이유 |
|------|----------|------|
| 운영체제 이론 | `cs/os/` | CS 이론 |
| 데이터베이스 이론 | `cs/database/` | CS 이론 |
| 네트워크 원리 | `cs/network/` | CS 이론 |
| Python 문법 | `lang/python/` | 언어 학습 |
| Java 컬렉션 | `lang/java/part3-collections/` | 언어 학습 |
| Docker 사용법 | `tools/docker/` | 개발 도구 |
| Git 명령어 | `tools/git/` | 개발 도구 |
| 디자인 패턴 | `development/design-patterns/` | 개발 실무/설계 |
| 클린 아키텍처 | `development/clean-architecture/` | 개발 실무/설계 |
| AI 이론 | `cs/ai/` | CS 이론 |

---

## 2. 주제 폴더 (Depth 2)

각 카테고리 안에 주제별 폴더를 생성한다.

### 규칙

- 폴더명은 **kebab-case**를 사용한다: `network/`, `clean-architecture/`
- 약어를 사용하지 않는다: `ct/` (X) → `coding-test/` (O), `cws/` (X) → `network/` (O)
- 주제 폴더는 해당 주제의 **일반적인 영어 명칭**을 사용한다
- 향후 사용 예정인 빈 폴더는 허용한다 — 내용이 추가될 때 네이밍 규칙에 맞게 리네임한다

### 다중 소스 규칙

같은 주제에 여러 학습 소스(강의, 책, 자체 정리 등)가 존재할 수 있다.

- **단일 소스**인 동안은 플랫 구조를 유지한다
- **두 번째 소스가 추가되는 시점**에 소스별 서브폴더로 분리한다
- 소스 폴더명은 소스의 식별 가능한 이름을 kebab-case로 사용한다

```
# 단일 소스 (현재)
cs/network/
├── 01.computer-structure.md
└── ...

# 두 번째 소스 추가 시
cs/network/
├── infra-youtube/           ← 기존 소스를 서브폴더로 이동
│   ├── 01.computer-structure.md
│   └── ...
├── tcp-ip-book/             ← 새 소스
│   ├── 01.xxx.md
│   └── ...
└── README.md                ← (선택) 소스 목록과 설명
```

이 규칙은 `cs/`, `development/`, `tools/` 모든 카테고리에 동일하게 적용된다.

### 카테고리별 내부 구조

**`cs/`** — 주제별 플랫 구조:
```
cs/{주제}/
├── 01.{주제}.md
├── 02.{주제}.md
└── ...
```

**`lang/`** — 언어 > 파트 > docs+practice:
```
lang/{언어}/
├── {part번호}-{주제}/
│   ├── docs/
│   └── practice/
```

**`coding-test/`** — 독자적 커리큘럼 구조:
```
coding-test/
├── CURRICULUM.md
├── PROGRESS.md
├── {stage 또는 prep}/
│   ├── docs/
│   └── practice/
│       ├── ex/       ← 연습 문제
│       ├── prob/     ← 플랫폼 문제
│       └── quiz/     ← 이론 퀴즈
```

**`tools/`** — 도구별 플랫 구조:
```
tools/{도구명}/
├── {kebab-case}.md
└── ...
```

**`development/`** — 주제별 플랫 구조:
```
development/{주제}/
├── {번호}.{kebab-case}.md
└── ...
```

---

## 3. 학습 콘텐츠 폴더 (Depth 3)

학습 자료와 실습 코드가 공존하는 주제는 `docs/`와 `practice/`로 분리한다.

### 규칙

- 학습 문서는 `docs/`에 위치한다 (복수형 `docs/`, 단수형 `doc/` 사용하지 않음)
- 실습 코드는 `practice/`에 위치한다
- `docs/`는 읽기 전용이다 — 학습 중 수정하지 않는다
- 학습 결과물(풀이, 회고)은 `practice/`에 작성한다
- 문서만 존재하는 주제(예: `cs/network/`)는 `docs/` 없이 플랫 구조를 사용한다
- `coding-test/`의 `practice/`는 `ex/`, `prob/`, `quiz/` 서브폴더로 유형을 구분한다

### 적용 기준

| 조건 | 구조 |
|------|------|
| 문서 + 실습 코드가 모두 존재하거나 예정 | `docs/` + `practice/` 분리 |
| 문서만 존재 (코드 실습 없음) | 플랫 구조 (폴더 안에 .md 파일 직접 배치) |

---

## 4. 파일 (Depth 4)

### 번호 인덱싱 기준

학습 순서가 존재하는 콘텐츠에만 번호를 부여한다. 순서 의존성이 없는 독립 토픽은 번호 없이 kebab-case만 사용한다.

| 콘텐츠 성격 | 번호 부여 | 예시 |
|------------|----------|------|
| 순차 학습 (커리큘럼, 이론 시리즈) | 부여한다 | `01.checksum-hash.md`, `1.3.variable.md` |
| 독립 토픽 (도구 레퍼런스, 팁) | 부여하지 않는다 | `rebase.md`, `workflow.md` |

### 문서 파일 네이밍

```
순차 학습:  {번호}.{kebab-case}.md    (예: 01.checksum-hash.md)
독립 토픽:  {kebab-case}.md           (예: rebase.md)
```

- 번호와 주제 사이는 점(`.`)으로 구분한다
- 주제는 kebab-case를 사용한다
- 모든 문서는 한국어로 작성한다

### 코드 파일 네이밍

```
Java:  PascalCase.java     (예: GenericMain.java, IoScanner.java)
```

- Java 파일명 = 클래스명이므로 PascalCase만 허용한다
- 파일명에 단원 번호 접두사를 포함하지 않는다 — 단원 정보는 폴더 경로가 담당한다

### 메타 문서

프로젝트 또는 카테고리 수준의 관리 문서는 다음 네이밍을 사용한다:

| 파일 | 위치 | 역할 |
|------|------|------|
| `README.md` | 각 주제 폴더 루트 | 해당 폴더의 개요와 학습 가이드 |
| `CURRICULUM.md` | `coding-test/` 루트 | 커리큘럼 전체 구조와 랭크 체계 |
| `PROGRESS.md` | `coding-test/` 루트 | 학습 진행 상황 추적 |
| `CLAUDE.md` | 각 `docs/` 폴더 | AI 도구(claude-mem)가 자동 생성하는 컨텍스트 파일 — 수동 편집하지 않는다 |
| `.claude/rules/structure-rules.md` | 저장소 규칙 디렉터리 | 이 문서. authored·project 구조 규칙 정의 |

메타 문서는 대문자로 작성하여 일반 학습 문서와 구분한다.

### 금지 사항

- snake_case 파일명 사용 금지: `checksum_hash.md` (X) → `checksum-hash.md` (O)
- 폴더명과 중복되는 접두사 사용 금지: `tools/git/git-rebase.md` (X) → `tools/git/rebase.md` (O)
- 확장자 누락 금지: 모든 문서는 `.md` 확장자를 포함한다
- Java 파일에 인덱스 접두사 금지: `EX02_IoScanner.java` (X) → `IoScanner.java` (O)
- 빈 파일 커밋 금지: 내용 없는 파일은 생성하지 않는다 (빈 폴더는 허용)

---

## 5. Obsidian 연동

이 프로젝트는 Obsidian vault로 사용할 수 있다.

### 규칙

- `.obsidian/` 폴더는 git에서 제외한다 (`.gitignore`에 포함)
- 문서 간 참조는 Obsidian 위키링크를 사용할 수 있다: `[[파일명]]`
- 위키링크는 최단 경로(Shortest path) 설정을 사용한다
- 동일 파일명이 여러 위치에 존재할 경우 상대 경로를 포함한다: `[[cs/network/05.tcp-connection]]`
- authored 학습 문서의 선택 태그는 문서 상단 frontmatter에 작성한다:
  ```yaml
  ---
  tags: [network, tcp, protocol]
  ---
  ```
- authored frontmatter 태그는 선택 사항이다 — 폴더 구조가 1차 분류 체계이며, 태그는 교차 참조 보조 수단이다. `projects/**/*.md`에는 frontmatter를 두지 않는다.

---

## 요약: 전체 경로 패턴

```
cs-study/
├── cs/{주제}/{번호}.{kebab-case}.md
├── lang/{언어}/{partN-주제}/docs/{번호}.{kebab-case}.md
├── lang/{언어}/{partN-주제}/practice/{PascalCase}.java
├── coding-test/{stage}/docs/{번호}.{kebab-case}.md
├── coding-test/{stage}/practice/{ex,prob,quiz}/{PascalCase}.java
├── tools/{도구명}/{kebab-case}.md
└── development/{주제}/{번호}.{kebab-case}.md
```

위 authored 경로의 최대 깊이는 4이다. `projects/`와 이 문서 적용 범위 밖의 `wiki/`에는 이 상한을 적용하지 않는다.
단, `coding-test/stage4/week{N}/docs/`는 커리큘럼 특수 구조로 예외를 허용한다.
