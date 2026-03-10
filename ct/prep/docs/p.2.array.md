# p.2 배열

> 랭크: Silver 진행 중 (prep 2/3) | 리뷰 미션 포함

---

## 리뷰 미션 (p.1 제어문)

**R1.** `break`와 `continue`의 차이를 한 줄로 설명하라.

<details>
<summary>정답</summary>
break는 반복문을 완전히 종료하고, continue는 현재 반복만 건너뛰고 다음 반복을 계속한다.
</details>

**R2.** 다음 코드의 출력은?

```java
for (int i = 0; i < 5; i++) {
    if (i == 3) continue;
    System.out.print(i + " ");
}
```

<details>
<summary>정답</summary>
0 1 2 4
</details>

---

## 1. 설명

### 1차원 배열

같은 타입의 데이터를 연속된 메모리에 저장하는 자료구조다.

```java
// 선언과 생성
int[] arr = new int[5];         // 크기 5, 기본값 0으로 초기화
int[] arr2 = {1, 2, 3, 4, 5};  // 선언과 동시에 초기화
```

**핵심 특성:**
- 인덱스는 0부터 시작
- 크기는 생성 시 고정 (변경 불가)
- `arr.length`로 크기 확인

### 배열 순회

```java
int[] arr = {10, 20, 30, 40, 50};

// 일반 for문 (인덱스 필요할 때)
for (int i = 0; i < arr.length; i++) {
    System.out.println("arr[" + i + "] = " + arr[i]);
}

// for-each (값만 필요할 때)
for (int num : arr) {
    System.out.println(num);
}
```

### 배열과 메모리

- 배열 변수(`arr`)는 스택에 저장 (참조)
- 배열 객체(실제 데이터)는 힙에 저장
- `int[] arr = null;` → 아직 배열 객체가 없음

### 2차원 배열

행(row)과 열(column)로 구성된 표 형태의 배열이다.

```java
// 선언과 생성
int[][] grid = new int[3][4];     // 3행 4열, 기본값 0

// 선언과 동시에 초기화
int[][] grid2 = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};
```

### 2차원 배열 순회

```java
int[][] grid = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// 이중 for문 순회
for (int i = 0; i < grid.length; i++) {           // 행
    for (int j = 0; j < grid[i].length; j++) {    // 열
        System.out.print(grid[i][j] + " ");
    }
    System.out.println();
}
```

**크기 확인:**
- `grid.length` → 행의 수
- `grid[i].length` → i번째 행의 열 수

### 배열의 활용 패턴

```java
// 최대값 찾기
int max = arr[0];
for (int i = 1; i < arr.length; i++) {
    max = Math.max(max, arr[i]);
}

// 합계
int sum = 0;
for (int num : arr) {
    sum += num;
}

// 특정 값 개수 세기
int count = 0;
for (int num : arr) {
    if (num == target) count++;
}
```

---

## 2. 예제

### 예제 1: 1차원 배열 기본

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int[] arr = new int[n];

        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }

        // 합계, 최대, 최소
        int sum = 0, max = arr[0], min = arr[0];
        for (int num : arr) {
            sum += num;
            max = Math.max(max, num);
            min = Math.min(min, num);
        }

        System.out.println("합: " + sum);
        System.out.println("최대: " + max);
        System.out.println("최소: " + min);
    }
}
```

### 예제 2: 2차원 배열 입력과 출력

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int rows = Integer.parseInt(st.nextToken());
        int cols = Integer.parseInt(st.nextToken());

        int[][] grid = new int[rows][cols];

        // 입력
        for (int i = 0; i < rows; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < cols; j++) {
                grid[i][j] = Integer.parseInt(st.nextToken());
            }
        }

        // 출력 (전체 합 포함)
        int total = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print(grid[i][j] + " ");
                total += grid[i][j];
            }
            System.out.println();
        }
        System.out.println("전체 합: " + total);
    }
}
```

### 예제 3: 배열 뒤집기

```java
public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};

        // 양쪽 끝에서 교환
        int left = 0, right = arr.length - 1;
        while (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }

        // 출력: 5 4 3 2 1
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
}
```

---

## 3. 직접 작성

### 과제 1: 배열 입력과 출력

정수 N개를 입력받아 역순으로 출력하는 프로그램을 작성하라.

```
입력:
5
1 2 3 4 5

출력:
5 4 3 2 1
```

### 과제 2: 2차원 배열 대각선 합

3x3 2차원 배열을 입력받아 주 대각선(좌상→우하) 요소의 합을 출력하라.

```
입력:
1 2 3
4 5 6
7 8 9

출력: 15  (1 + 5 + 9)
```

---

## 4. 이론 퀴즈

**Q1.** 배열의 인덱스는 몇부터 시작하는가?

<details>
<summary>정답</summary>
0.
</details>

**Q2.** `int[] arr = new int[5];`에서 `arr[3]`의 초기값은?

<details>
<summary>정답</summary>
0. int 배열은 기본값 0으로 초기화된다.
</details>

**Q3.** 2차원 배열 `int[][] grid = new int[3][4];`에서 `grid.length`와 `grid[0].length`는 각각?

<details>
<summary>정답</summary>
grid.length = 3 (행 수), grid[0].length = 4 (열 수).
</details>

**Q4.** 배열은 생성 후 크기를 변경할 수 있는가?

<details>
<summary>정답</summary>
없다. 배열 크기는 생성 시 고정된다. 동적 크기가 필요하면 ArrayList를 사용한다.
</details>

---

## 5. 함정 노트

### 1. ArrayIndexOutOfBoundsException

```java
int[] arr = new int[5];
arr[5] = 10;  // 예외! 인덱스는 0~4까지

// 흔한 실수: <= 사용
for (int i = 0; i <= arr.length; i++) { }  // 마지막에 예외
for (int i = 0; i < arr.length; i++) { }   // 올바름
```

### 2. 배열 비교에 == 사용

```java
int[] a = {1, 2, 3};
int[] b = {1, 2, 3};
System.out.println(a == b);                    // false (참조 비교)
System.out.println(java.util.Arrays.equals(a, b)); // true (값 비교)
```

### 3. 배열 크기 0

```java
int[] arr = new int[0];  // 합법적. 빈 배열
// arr[0] = 1;           // ArrayIndexOutOfBoundsException
System.out.println(arr.length);  // 0
```

### 4. 2차원 배열에서 행과 열 혼동

```java
int[][] grid = new int[3][5];  // 3행 5열
// grid[행][열] 순서
// grid[0].length = 5 (열 수)
// grid.length = 3 (행 수)
```

### 5. 배열 복사 시 참조 복사

```java
int[] a = {1, 2, 3};
int[] b = a;       // 같은 배열을 참조!
b[0] = 99;
System.out.println(a[0]);  // 99! a도 바뀜

// 올바른 복사
int[] c = a.clone();
// 또는
int[] d = java.util.Arrays.copyOf(a, a.length);
```

---

## 6. 코딩 문제

### 문제 1: [백준 10818 - 최소, 최대](https://www.acmicpc.net/problem/10818)

- **난이도**: Bronze III
- **핵심**: 배열 입력 후 최소, 최대 탐색
- **힌트**: `Math.max`, `Math.min` 활용

### 문제 2: [백준 2562 - 최댓값](https://www.acmicpc.net/problem/2562)

- **난이도**: Bronze III
- **핵심**: 최댓값과 그 **위치(인덱스)** 찾기
- **힌트**: 인덱스가 필요하므로 일반 for문 사용 (for-each 불가)

### 문제 3: [백준 2738 - 행렬 덧셈](https://www.acmicpc.net/problem/2738)

- **난이도**: Bronze V
- **핵심**: 2차원 배열 입력, 덧셈, 출력
- **힌트**: 두 행렬을 각각 입력받아 같은 위치끼리 더하기

---

## 7. 보스 문제

### [백준 2563 - 색종이](https://www.acmicpc.net/problem/2563)

- **난이도**: Silver V
- **핵심**: 2차원 배열을 좌표 평면처럼 활용
- **포인트**: 100x100 boolean 배열에 색종이 영역을 표시하고, true인 칸 수를 세기
- **힌트**: 색종이의 좌하단 좌표 (x, y)가 주어지면 `grid[i][j] = true`로 10x10 영역 표시

### 회고 체크리스트

1. 이 문제의 시간/공간 복잡도는?
2. 2차원 배열을 좌표계로 활용하는 패턴이 이해되었는가?
3. 겹치는 영역을 어떻게 중복 없이 처리했는가?
