# Java 기초 문법 & 코딩 테스트 커리큘럼

## 목표

- AI/IDE 자동완성 없이 맨땅에서 코딩하는 능력 회복
- 단순 코테 통과가 아닌 정확한 이해와 실무 활용
- 프로그래머스 LV3 / 백준 실버~골드 수준 도달

---

## 학습 구조

### 단원 구성 (7단계)

```
[리뷰 미션 2~3문제]         ← 이전 단원 복습
         |
1. 설명                     ← 개념 이해
2. 예제 (2~3개)             ← 코드로 확인
3. 직접 작성 (변형 1~2개)    ← 손으로 체득
4. 이론 퀴즈 (3~5문제)       ← 개념 점검
5. 함정 노트 (3~5개)         ← 실수 방지
6. 코딩 문제 (2~3문제)       ← 실전 적용
7. 보스 문제 (1문제 + 회고)   ← 종합 도전
         |
[체크포인트 통과 → 다음 단원 해금]
```

### 스킵 클리어 규칙

이미 아는 단원은 빠르게 넘길 수 있다:

- 이론 퀴즈 전부 정답 시 → 직접 작성 생략 → 코딩 문제만 풀기
- 보스 문제는 반드시 풀어야 클리어

### 보스 문제 회고 체크리스트

풀이 후 반드시 답하는 3가지:

1. 이 문제의 시간/공간 복잡도는?
2. 처음 접근이 틀렸다면, 어디서 방향을 잘못 잡았는가?
3. 같은 유형이 나오면 어떤 패턴으로 접근할 것인가?

### 리뷰 미션

각 단원 시작 시 이전 단원 복습:

| 구성 | 내용 |
|------|------|
| 이론 1문제 | 이전 단원 핵심 개념 OX 또는 빈칸 |
| 코드 1문제 | 이전 단원 코드 출력 예측 또는 빈칸 채우기 |
| 응용 1문제 | 이전 + 현재 단원 연결 문제 (선택) |

---

## 랭크 체계

| 랭크 | 조건 | 구간 |
|------|------|------|
| Bronze | stage1 완료 | 기초 문법 |
| Silver | prep + stage2 완료 | 알고리즘 준비 + OOP |
| Gold | stage3 완료 | 컬렉션 |
| Platinum | stage4 week1~3 완료 | 알고리즘 기초 |
| Diamond | stage4 week4~5 완료 | 심화 알고리즘 |
| Master | stage4 week6 완료 | 기출 정복 |

---

## 커리큘럼 흐름

```
stage1 (기초 문법)
    |
  prep (알고리즘 준비)
    |
stage2 (OOP 기초)
    |
stage3 (컬렉션)
    |
stage4 week1 (복잡도)
    |
stage4 week2 (배열·링크드리스트·이진탐색·재귀)
    |
stage4 week3 (정렬·스택·큐·해시)
    |
stage4 week4 (트리·힙·그래프·DFS·BFS)
    |
stage4 week5 (DP)
    |
stage4 week6 (기출)
```

---

## stage1: 기초 문법 → Bronze

| 순서 | 주제 | 핵심 내용 | 문서 | 참조 |
|------|------|-----------|------|------|
| 1.1 | 환경·실행 | javac/java 명령줄, main 구조 | [docs/1.1.env.md](stage1/docs/1.1.env.md) | part1: 1.4, 1.5 |
| 1.2 | 입출력 | Scanner + BufferedReader/StringTokenizer | [docs/1.2.io.md](stage1/docs/1.2.io.md) | part1: 1.9 |
| 1.3 | 변수·타입 | 원시/참조, Wrapper 클래스, 오토박싱/언박싱 | [docs/1.3.variable.md](stage1/docs/1.3.variable.md) | part1: 1.7, 1.8 |
| 1.4 | 연산자 | 산술, 비교, 논리, 형승격, 단락평가 | [docs/1.4.operator.md](stage1/docs/1.4.operator.md) | part1: 1.11 |
| 1.5 | 메서드 | 시그니처, 매개변수, 반환, 오버로딩, static 도입, Math 클래스 | [docs/1.5.method.md](stage1/docs/1.5.method.md) | part1: 1.12 |

### 의존 관계

```
1.1 → 1.2 → 1.3 → 1.4 → 1.5
```

---

## prep: 알고리즘 준비 → Silver (1/2)

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| p.1 | 제어문 | if/else, switch, for, while, break/continue, for-each | [docs/p.1.control.md](prep/docs/p.1.control.md) |
| p.2 | 배열 | 1차원 + 2차원 (선언, 초기화, 이중 for 순회) | [docs/p.2.array.md](prep/docs/p.2.array.md) |
| p.3 | String & StringBuilder | String 메서드(charAt, substring, length, split, toCharArray) + 불변성 → StringBuilder → append | [docs/p.3.string.md](prep/docs/p.3.string.md) |
| 부록 | 예외 처리 | try-catch, NumberFormatException (참고용) | [docs/appendix.exception.md](prep/docs/appendix.exception.md) |

### 의존 관계

```
stage1 완료 → p.1 → p.2 → p.3
```

---

## stage2: OOP 기초 → Silver (2/2)

| 순서 | 주제 | 핵심 내용 | 문서 | 참조 |
|------|------|-----------|------|------|
| 2.1 | 클래스·객체 | 필드, 생성자, this, getter/setter | [docs/2.1.class.md](stage2/docs/2.1.class.md) | part2: 2.2, 2.3 |
| 2.2 | 상속·다형성 | extends, override, 캐스팅(간단 언급), 인스턴스 vs static 심화 | [docs/2.2.inheritance.md](stage2/docs/2.2.inheritance.md) | part2: 2.4, 2.6 |
| 2.3 | 인터페이스·추상 | interface, abstract class | [docs/2.3.interface.md](stage2/docs/2.3.interface.md) | part2: 2.6 |

### 의존 관계

```
prep 완료 → 2.1 → 2.2 → 2.3
stage1.5 static ──→ 2.2 인스턴스 vs static 심화
```

---

## stage3: 컬렉션 → Gold

| 순서 | 주제 | 핵심 내용 | 문서 | 참조 |
|------|------|-----------|------|------|
| 3.1 | 제너릭 | `List<T>`, 타입 파라미터, 제너릭 이론과 사용법 | [docs/3.1.generic.md](stage3/docs/3.1.generic.md) | part3a: 8.1 |
| 3.2 | List | ArrayList, add/get/size/remove, Collections 유틸(sort, reverse, max, min, frequency) | [docs/3.2.list.md](stage3/docs/3.2.list.md) | part3a: 8.2 |
| 3.3 | Set | HashSet, 중복 제거, 순회 | [docs/3.3.set.md](stage3/docs/3.3.set.md) | part3a: 8.2, 9.1 |
| 3.4 | Map | HashMap, get/put/containsKey, 순회 | [docs/3.4.map.md](stage3/docs/3.4.map.md) | part3a: 8.2 |

### 의존 관계

```
stage2 완료 → 3.1 → 3.2 → 3.3 → 3.4
stage1.3 Wrapper/오토박싱 ──→ 3.1 List<Integer>
prep p.1 for-each ──→ 3.2~3.4 컬렉션 순회
```

---

## stage4: 알고리즘 (6주)

사전 요건: stage1 + prep + stage2 + stage3 모두 완료

---

### week1: 시간·공간 복잡도 → Platinum (1/3)

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| 1-1 | 알고리즘 기초 | 알고리즘이란, 입력·출력·제약 | [docs/1-1.intro.md](stage4/week1/docs/1-1.intro.md) |
| 1-2 | 시간 복잡도 | O(1), O(n), O(n²), 반복문 수 분석 | [docs/1-2.time.md](stage4/week1/docs/1-2.time.md) |
| 1-3 | 공간 복잡도 | 변수·배열·재귀에 따른 메모리 | [docs/1-3.space.md](stage4/week1/docs/1-3.space.md) |
| 1-4 | 점근 표기법 | Big-O, Omega, Theta | [docs/1-4.asymptotic.md](stage4/week1/docs/1-4.asymptotic.md) |

---

### week2: 배열·링크드리스트, 이진탐색, 재귀 → Platinum (2/3)

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| 2-1 | 배열 vs 링크드리스트 | 접근·삽입·삭제 특성 비교 | [docs/2-1.array_vs_list.md](stage4/week2/docs/2-1.array_vs_list.md) |
| 2-2 | 링크드리스트 구현 | Node 클래스, head/tail, add/remove | [docs/2-2.linkedlist.md](stage4/week2/docs/2-2.linkedlist.md) |
| 2-3 | 이진 탐색 | 정렬 전제, mid 계산, Arrays.binarySearch | [docs/2-3.binary_search.md](stage4/week2/docs/2-3.binary_search.md) |
| 2-4 | 재귀 함수 | base case, recursive case, 스택 프레임 | [docs/2-4.recursion.md](stage4/week2/docs/2-4.recursion.md) |

---

### week3: 정렬, 스택·큐, 해시 → Platinum (3/3)

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| 3-1 | 정렬 | 버블·선택·삽입, Arrays.sort, Comparable/Comparator (람다 중심, 익명 클래스 참고) | [docs/3-1.sort.md](stage4/week3/docs/3-1.sort.md) |
| 3-2 | 스택 | LIFO, push/pop, ArrayDeque | [docs/3-2.stack.md](stage4/week3/docs/3-2.stack.md) |
| 3-3 | 큐 | FIFO, offer/poll, ArrayDeque | [docs/3-3.queue.md](stage4/week3/docs/3-3.queue.md) |
| 3-4 | 해시 | 해시 원리, 충돌, O(1) 조회, 빈도수 패턴, Two-Sum | [docs/3-4.hash.md](stage4/week3/docs/3-4.hash.md) |

---

### week4: 트리·힙, 그래프, DFS·BFS → Diamond (1/2)

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| 4-1 | 트리 | 노드·엣지·루트·리프, 이진트리, 순회(전위·중위·후위) | [docs/4-1.tree.md](stage4/week4/docs/4-1.tree.md) |
| 4-2 | 힙 | 완전이진트리, 최대/최소 힙, PriorityQueue | [docs/4-2.heap.md](stage4/week4/docs/4-2.heap.md) |
| 4-3 | 그래프 | 정점·간선, 인접리스트·인접행렬 | [docs/4-3.graph.md](stage4/week4/docs/4-3.graph.md) |
| 4-4 | DFS | 깊이 우선, 스택/재귀 활용 | [docs/4-4.dfs.md](stage4/week4/docs/4-4.dfs.md) |
| 4-5 | BFS | 너비 우선, 큐 활용 | [docs/4-5.bfs.md](stage4/week4/docs/4-5.bfs.md) |

---

### week5: DP → Diamond (2/2)

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| 5-1 | DP 개념 | 최적 부분 구조, 중복 부분 문제 | [docs/5-1.dp_intro.md](stage4/week5/docs/5-1.dp_intro.md) |
| 5-2 | 탑다운 | 재귀 + 메모이제이션 | [docs/5-2.top_down.md](stage4/week5/docs/5-2.top_down.md) |
| 5-3 | 바텀업 | 반복문 + 테이블 | [docs/5-3.bottom_up.md](stage4/week5/docs/5-3.bottom_up.md) |
| 5-4 | 1차원 DP | 피보나치, 계단 오르기 | [docs/5-4.dp_1d.md](stage4/week5/docs/5-4.dp_1d.md) |
| 5-5 | 2차원 DP | 격자 경로, 배낭 문제 입문 | [docs/5-5.dp_2d.md](stage4/week5/docs/5-5.dp_2d.md) |

---

### week6: 기출 → Master

| 순서 | 주제 | 핵심 내용 | 문서 |
|------|------|-----------|------|
| 6-1 | LINE 인턴 | 기출 유형 분석·풀이 | [docs/6-1.line.md](stage4/week6/docs/6-1.line.md) |
| 6-2 | 카카오 신입 | 기출 유형 분석·풀이 | [docs/6-2.kakao.md](stage4/week6/docs/6-2.kakao.md) |
| 6-3 | 삼성 역량 | 기출 유형 분석·풀이 | [docs/6-3.samsung.md](stage4/week6/docs/6-3.samsung.md) |
| 6-4 | 종합 실전 | 시간 제한 모의고사 | [docs/6-4.mock.md](stage4/week6/docs/6-4.mock.md) |

> 문제 선정은 week5 완료 후 실력에 맞춰 결정

---

## 의존 관계 전체 맵

```
stage1.3 Wrapper/오토박싱 ──→ stage3.1 제너릭 List<Integer>
stage1.5 static + Math ────→ stage2.2 인스턴스 vs static 심화
prep p.1 for-each ─────────→ stage3.2~3.4 컬렉션 순회
prep p.2 2차원 배열 ────────→ week4 인접행렬
prep p.3 String 메서드 ────→ week3 해시(문자열 처리)
stage2.3 interface ────────→ week3 Comparable/Comparator
stage3 컬렉션 API ─────────→ week3 해시 원리·활용
week2 재귀 ────────────────→ week4 DFS ──→ week5 메모이제이션
week3 스택·큐 ─────────────→ week4 DFS·BFS
```

---

## 학습 관리

### 진행 추적

- [PROGRESS.md](PROGRESS.md) — 체크박스로 학습 진행 현황 관리
- 각 항목 완료 시 `[ ]` → `[x]`, 퀴즈는 `Q1:O Q2:X` 형식으로 기록
- 스킵 클리어 시 `[-] 직접 작성 (스킵)`으로 변경

### practice 폴더 사용법

- `docs/` — **읽기 전용** (커리큘럼 원본, 수정 금지)
- `practice/` — **개인 학습** (코드 작성, 회고 기록)
- 각 practice 폴더의 `README.md`에 해당 단원의 파일 목록과 네이밍 가이드가 있음

#### 폴더 구조

```
practice/
├── ex/                  직접 작성 과제 (Ex01_Name.java)
├── prob/                코딩 문제 (Boj2557.java / Point.java)
├── boss/                보스 문제 (Boj10172.java / BankAccount.java)
├── review.md            보스 회고
└── review_template.md   회고 양식 원본 (stage1에만 존재)
```

> 폴더별 분류로 유형이 명확하고, 파일명은 Java 클래스명 규칙을 준수

#### 보스 회고 작성

`stage1/practice/review_template.md`를 복사하여 각 단원의 `review.md`로 사용

---

## 파일 구조

```
01-ct/
├── CURRICULUM.md              # 이 문서 (커리큘럼 설계)
├── PROGRESS.md                # 진행 현황 추적
├── stage1/
│   ├── docs/                  # 1.1~1.5 설명 문서 (읽기 전용)
│   └── practice/              # README.md + 4_review_template.md
├── prep/
│   ├── docs/                  # p.1~p.3 + 부록 (읽기 전용)
│   └── practice/              # README.md
├── stage2/
│   ├── docs/                  # 2.1~2.3 (읽기 전용)
│   └── practice/              # README.md
├── stage3/
│   ├── docs/                  # 3.1~3.4 (읽기 전용)
│   └── practice/              # README.md
└── stage4/
    ├── week1/
    │   ├── docs/              # 1-1~1-4 (읽기 전용)
    │   └── practice/          # README.md
    ├── week2/
    │   ├── docs/              # 2-1~2-4 (읽기 전용)
    │   └── practice/          # README.md
    ├── week3/
    │   ├── docs/              # 3-1~3-4 (읽기 전용)
    │   └── practice/          # README.md
    ├── week4/
    │   ├── docs/              # 4-1~4-5 (읽기 전용)
    │   └── practice/          # README.md
    ├── week5/
    │   ├── docs/              # 5-1~5-5 (읽기 전용)
    │   └── practice/          # README.md
    └── week6/
        ├── docs/              # 6-1~6-4 (읽기 전용)
        └── practice/          # README.md
```
