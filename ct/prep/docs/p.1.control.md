# p.1 제어문

> 랭크: Silver 진행 중 (prep 1/3) | 리뷰 미션 포함

---

## 리뷰 미션 (stage1.5 메서드)

**R1.** `main`에서 호출하는 메서드가 `static`이어야 하는 이유를 설명하라.

<details>
<summary>정답</summary>
main이 static이므로 인스턴스 없이 실행된다. static 컨텍스트에서는 인스턴스 멤버에 접근할 수 없으므로, 호출하는 메서드도 static이어야 한다.
</details>

**R2.** `Math.max(Math.min(10, 20), 15)`의 결과는?

<details>
<summary>정답</summary>
15. Math.min(10, 20) = 10, Math.max(10, 15) = 15.
</details>

---

## 1. 설명

### if / else if / else

조건에 따라 실행 흐름을 분기한다.

```java
if (조건1) {
    // 조건1이 true일 때
} else if (조건2) {
    // 조건1이 false이고 조건2가 true일 때
} else {
    // 모든 조건이 false일 때
}
```

### switch

하나의 값을 여러 경우와 비교할 때 사용한다.

```java
switch (변수) {
    case 값1:
        // 실행
        break;
    case 값2:
        // 실행
        break;
    default:
        // 어떤 case에도 해당하지 않을 때
}
```

- `break`가 없으면 다음 case로 **관통(fall-through)** 된다
- `int`, `char`, `String`, `enum` 타입 사용 가능

### for 반복문

횟수가 정해진 반복에 적합하다.

```java
for (초기화; 조건; 증감) {
    // 반복할 코드
}

// 예: 0부터 4까지 출력
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}
```

### while 반복문

조건이 true인 동안 반복한다. 반복 횟수가 미정일 때 적합하다.

```java
while (조건) {
    // 반복할 코드
}

// 예: 1부터 합이 100을 넘을 때까지
int sum = 0, n = 1;
while (sum <= 100) {
    sum += n;
    n++;
}
```

### do-while 반복문

최소 1번은 실행 후 조건을 검사한다.

```java
do {
    // 최소 1번 실행
} while (조건);
```

### break와 continue

- `break`: 반복문을 즉시 종료
- `continue`: 현재 반복을 건너뛰고 다음 반복으로

```java
for (int i = 0; i < 10; i++) {
    if (i == 5) break;      // 5에서 반복 종료
    if (i % 2 == 0) continue; // 짝수는 건너뜀
    System.out.println(i);   // 1, 3 출력
}
```

### for-each (향상된 for문)

배열이나 컬렉션의 모든 요소를 순회할 때 사용한다.
인덱스가 필요 없을 때 for-each가 더 간결하다.

```java
int[] arr = {10, 20, 30};

// 일반 for
for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}

// for-each (같은 동작, 더 간결)
for (int num : arr) {
    System.out.println(num);
}
```

- `for (타입 변수 : 배열/컬렉션)` 형식
- 읽기 전용: 순회 중 요소를 수정할 수 없다
- 인덱스 접근이 필요하면 일반 for문 사용

---

## 2. 예제

### 예제 1: 조건 분기

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int score = Integer.parseInt(br.readLine().trim());

        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else if (score >= 70) {
            System.out.println("C");
        } else {
            System.out.println("F");
        }
    }
}
```

### 예제 2: 반복문 패턴

```java
public class Main {
    public static void main(String[] args) {
        // 1부터 N까지의 합
        int n = 100;
        int sum = 0;
        for (int i = 1; i <= n; i++) {
            sum += i;
        }
        System.out.println("합: " + sum);  // 5050

        // 구구단 2단
        for (int i = 1; i <= 9; i++) {
            System.out.println("2 * " + i + " = " + (2 * i));
        }
    }
}
```

### 예제 3: 중첩 반복문

```java
public class Main {
    public static void main(String[] args) {
        // 구구단 전체 (2단~9단)
        for (int dan = 2; dan <= 9; dan++) {
            for (int i = 1; i <= 9; i++) {
                System.out.println(dan + " * " + i + " = " + (dan * i));
            }
            System.out.println(); // 단 사이 빈 줄
        }
    }
}
```

---

## 3. 직접 작성

### 과제 1: 조건문 연습

정수를 입력받아 양수/음수/0을 판별하여 출력하라.

### 과제 2: 반복문 연습

1부터 100까지 정수 중 3의 배수이면서 5의 배수가 아닌 수를 모두 출력하라.
(for, if, continue 사용)

---

## 4. 이론 퀴즈

**Q1.** switch문에서 `break`를 생략하면 어떻게 되는가?

<details>
<summary>정답</summary>
다음 case로 관통(fall-through)된다. 해당 case뿐 아니라 이후 모든 case의 코드가 break를 만나거나 switch가 끝날 때까지 실행된다.
</details>

**Q2.** `for (int x : arr)`에서 `x`의 값을 바꾸면 원본 배열이 바뀌는가?

<details>
<summary>정답</summary>
아니다. x는 배열 요소의 복사본이므로 x를 바꿔도 원본 배열은 변하지 않는다. (원시 타입 배열의 경우)
</details>

**Q3.** `while(true)`는 어떻게 종료하는가?

<details>
<summary>정답</summary>
반복문 내부에서 break를 사용하거나, return으로 메서드를 종료한다.
</details>

**Q4.** `continue`와 `break`의 차이는?

<details>
<summary>정답</summary>
continue는 현재 반복만 건너뛰고 다음 반복을 계속한다. break는 반복문 전체를 종료한다.
</details>

---

## 5. 함정 노트

### 1. if 조건에 = 대신 == 사용

```java
if (a = 5) { }   // 컴파일 에러 (Java는 대입을 boolean으로 안 봄)
if (a == 5) { }   // 올바른 비교
```

Java에서는 C와 달리 대입문이 boolean이 아니므로 컴파일 에러가 나지만, 혼동하지 않도록 주의.

### 2. switch fall-through

```java
switch (grade) {
    case 'A':
        System.out.println("우수");
        // break 빠짐!
    case 'B':
        System.out.println("양호");  // A일 때도 이것이 실행됨
        break;
}
```

### 3. 무한 루프에서 break 누락

```java
while (true) {
    // break 조건을 잊으면 프로그램이 멈추지 않는다
}
```

### 4. for문 변수 스코프

```java
for (int i = 0; i < 5; i++) {
    // i 사용 가능
}
// System.out.println(i);  // 컴파일 에러! i는 for문 밖에서 접근 불가
```

### 5. off-by-one 오류

```java
// 0부터 시작하는데 <= 사용 → 요소가 하나 더 처리됨
for (int i = 0; i <= arr.length; i++) { }  // ArrayIndexOutOfBoundsException
for (int i = 0; i < arr.length; i++) { }   // 올바름
```

---

## 6. 코딩 문제

### 문제 1: [백준 1330 - 두 수 비교하기](https://www.acmicpc.net/problem/1330)

- **난이도**: Bronze V
- **핵심**: if / else if / else
- **힌트**: 두 수의 대소 비교 후 `>`, `<`, `==` 출력

### 문제 2: [백준 9498 - 시험 성적](https://www.acmicpc.net/problem/9498)

- **난이도**: Bronze V
- **핵심**: 범위 조건 분기
- **힌트**: 90 이상 A, 80 이상 B, 70 이상 C, 60 이상 D, 나머지 F

### 문제 3: [백준 2739 - 구구단](https://www.acmicpc.net/problem/2739)

- **난이도**: Bronze V
- **핵심**: for 반복문
- **힌트**: `N * i` 형식 출력

---

## 7. 보스 문제

### [백준 2884 - 알람 시계](https://www.acmicpc.net/problem/2884)

- **난이도**: Bronze III
- **핵심**: 조건 분기 + 경계값 처리 (시간이 0 미만이 될 때)
- **포인트**: 45분 전으로 설정할 때 시간이 바뀌는 경우와 분만 바뀌는 경우를 분리
- **힌트**: 분이 45 미만이면 시간에서 1 빼고 분에 60 더한 뒤 45 빼기. 시간이 0 미만이면 23으로.

### 회고 체크리스트

1. 이 문제의 시간/공간 복잡도는?
2. 경계값(0시 0분, 0시 44분 등)을 모두 테스트했는가?
3. if-else 구조가 깔끔하게 정리되었는가?
