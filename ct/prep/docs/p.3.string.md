# p.3 String & StringBuilder

> 랭크: Silver 진행 중 (prep 3/3) | 리뷰 미션 포함

---

## 리뷰 미션 (p.2 배열)

**R1.** `int[][] grid = new int[4][3];`에서 `grid.length`와 `grid[0].length`는?

<details>
<summary>정답</summary>
grid.length = 4 (행 수), grid[0].length = 3 (열 수).
</details>

**R2.** 다음 코드의 문제점은?

```java
int[] a = {1, 2, 3};
int[] b = a;
b[0] = 99;
System.out.println(a[0]);
```

<details>
<summary>정답</summary>
a[0]이 99가 된다. b = a는 같은 배열을 참조하는 참조 복사이므로, b를 수정하면 a도 바뀐다. 독립 복사하려면 a.clone() 또는 Arrays.copyOf()를 사용해야 한다.
</details>

---

## 1. 설명

### String 주요 메서드

`String`은 불변(immutable) 객체다. 메서드 호출 시 원본은 변하지 않고 새 String이 반환된다.

| 메서드 | 동작 | 예 |
|--------|------|-----|
| `length()` | 문자열 길이 | `"hello".length()` → 5 |
| `charAt(i)` | i번째 문자 반환 | `"hello".charAt(0)` → 'h' |
| `substring(s, e)` | s부터 e 직전까지 부분 문자열 | `"hello".substring(1, 3)` → "el" |
| `substring(s)` | s부터 끝까지 | `"hello".substring(2)` → "llo" |
| `indexOf(s)` | 문자열 위치 (-1이면 없음) | `"hello".indexOf("ll")` → 2 |
| `contains(s)` | 포함 여부 | `"hello".contains("ell")` → true |
| `equals(s)` | 값 비교 | `"abc".equals("abc")` → true |
| `compareTo(s)` | 사전순 비교 | `"a".compareTo("b")` → 음수 |
| `toCharArray()` | char 배열로 변환 | `"abc".toCharArray()` → {'a','b','c'} |
| `split(regex)` | 구분자로 분리 | `"a,b,c".split(",")` → {"a","b","c"} |
| `trim()` | 양쪽 공백 제거 | `" hi ".trim()` → "hi" |
| `toUpperCase()` | 대문자 변환 | `"abc".toUpperCase()` → "ABC" |
| `toLowerCase()` | 소문자 변환 | `"ABC".toLowerCase()` → "abc" |
| `replace(a, b)` | 문자열 치환 | `"aabb".replace("a","x")` → "xxbb" |

### 문자열 불변성 (Immutability)

String 객체는 한 번 생성되면 내용을 바꿀 수 없다.

```java
String s = "hello";
s.toUpperCase();           // s는 바뀌지 않음!
System.out.println(s);     // "hello" 그대로

s = s.toUpperCase();       // 새 String을 s에 재대입
System.out.println(s);     // "HELLO"
```

**문자열 + 연산의 문제:**

```java
String result = "";
for (int i = 0; i < 10000; i++) {
    result += i;  // 매번 새 String 객체 생성 → O(n²)
}
```

매 반복마다 새 String 객체가 생성되고 이전 내용이 복사된다.
10,000번 반복하면 약 10,000개의 임시 객체가 생성되어 **매우 느리다**.

### StringBuilder

가변(mutable) 문자열. 내부 버퍼에 문자를 추가하므로 효율적이다.

```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10000; i++) {
    sb.append(i);          // 내부 버퍼에 추가 → O(1) 평균
}
String result = sb.toString();  // 최종 변환
```

**주요 메서드:**

| 메서드 | 동작 |
|--------|------|
| `append(x)` | 끝에 추가 (int, char, String 등) |
| `insert(i, x)` | i 위치에 삽입 |
| `delete(s, e)` | s~e-1 구간 삭제 |
| `reverse()` | 뒤집기 |
| `toString()` | String으로 변환 |
| `length()` | 현재 길이 |

### 코테에서의 출력 패턴

반복 출력 시 `System.out.println`을 매번 호출하지 말고, StringBuilder로 모아서 한 번에 출력한다.

```java
StringBuilder sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    sb.append(i).append('\n');
}
System.out.print(sb);
```

> 참조: [java/part1/docs/1.7.string_encoding.md](../../../java/part1/docs/1.7.string_encoding.md)

---

## 2. 예제

### 예제 1: String 메서드 활용

```java
public class Main {
    public static void main(String[] args) {
        String s = "Hello, World!";

        System.out.println(s.length());           // 13
        System.out.println(s.charAt(0));           // 'H'
        System.out.println(s.substring(7, 12));    // "World"
        System.out.println(s.indexOf("World"));    // 7
        System.out.println(s.contains("Hello"));   // true
        System.out.println(s.toLowerCase());       // "hello, world!"
        System.out.println(s.replace("World", "Java")); // "Hello, Java!"
    }
}
```

### 예제 2: toCharArray로 문자 빈도수 세기

```java
public class Main {
    public static void main(String[] args) {
        String s = "banana";
        int[] count = new int[26];  // a~z 각 문자의 빈도

        for (char c : s.toCharArray()) {
            count[c - 'a']++;
        }

        // 출력
        for (int i = 0; i < 26; i++) {
            if (count[i] > 0) {
                System.out.println((char)('a' + i) + ": " + count[i]);
            }
        }
        // a: 3, b: 1, n: 2
    }
}
```

### 예제 3: StringBuilder로 효율적 출력

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            sb.append(i).append('\n');
        }
        System.out.print(sb);  // 한 번에 출력
    }
}
```

---

## 3. 직접 작성

### 과제 1: 문자열 뒤집기

문자열을 입력받아 뒤집어 출력하라. 두 가지 방법으로 작성:
1. `toCharArray()` + 반복문
2. `StringBuilder.reverse()`

### 과제 2: 단어 분리

공백으로 구분된 문장을 입력받아 각 단어를 한 줄씩 출력하라. (`split` 사용)

```
입력: "Java is fun"
출력:
Java
is
fun
```

---

## 4. 이론 퀴즈

**Q1.** String이 불변(immutable)이라는 것은 무엇을 의미하는가?

<details>
<summary>정답</summary>
한 번 생성된 String 객체의 내용은 변경할 수 없다. 문자열을 수정하는 것처럼 보이는 메서드(toUpperCase, replace 등)는 실제로 새 String 객체를 생성하여 반환한다.
</details>

**Q2.** 반복문에서 `String +=` 대신 `StringBuilder`를 사용해야 하는 이유는?

<details>
<summary>정답</summary>
String +=는 매번 새 String 객체를 생성하고 이전 내용을 복사하여 O(n²) 시간이 든다. StringBuilder는 내부 버퍼에 추가하므로 O(n)이다.
</details>

**Q3.** `"hello".substring(1, 3)`의 결과는?

<details>
<summary>정답</summary>
"el". 인덱스 1부터 3 직전(2)까지의 부분 문자열.
</details>

**Q4.** `charAt()`과 `toCharArray()`의 차이는?

<details>
<summary>정답</summary>
charAt(i)는 특정 인덱스의 문자 하나를 반환한다. toCharArray()는 문자열 전체를 char 배열로 변환하여 반환한다.
</details>

---

## 5. 함정 노트

### 1. String 비교에 == 사용

```java
String a = new String("hello");
String b = new String("hello");
System.out.println(a == b);       // false (참조 비교)
System.out.println(a.equals(b));  // true  (값 비교)
```

문자열 비교는 항상 `.equals()` 사용.

### 2. String 메서드 결과를 받지 않음

```java
String s = "hello";
s.toUpperCase();           // 반환값 무시! s는 여전히 "hello"
s = s.toUpperCase();       // 올바름: s에 재대입
```

불변이므로 반환값을 반드시 받아야 한다.

### 3. split의 인자는 정규식

```java
"a.b.c".split(".");     // 빈 배열! '.'은 정규식에서 "모든 문자"
"a.b.c".split("\\.");   // {"a", "b", "c"} 올바름
```

`.`, `|`, `*`, `+` 등 정규식 특수문자는 `\\`로 이스케이프해야 한다.

### 4. StringBuilder를 println에 직접 전달

```java
StringBuilder sb = new StringBuilder();
sb.append("hello");
System.out.println(sb);         // OK: toString() 자동 호출
// 하지만 명시적으로 toString() 호출하는 것이 명확
System.out.println(sb.toString());
```

### 5. 빈 문자열과 null 혼동

```java
String empty = "";      // 빈 문자열 (길이 0, 객체 존재)
String nil = null;      // null (객체 없음)

empty.length();         // 0 (정상)
nil.length();           // NullPointerException!
```

---

## 6. 코딩 문제

### 문제 1: [백준 2438 - 별 찍기 - 1](https://www.acmicpc.net/problem/2438)

- **난이도**: Bronze V
- **핵심**: 반복문 + StringBuilder로 별 패턴 출력
- **힌트**: i번째 줄에 별 i개. StringBuilder로 모아서 출력

### 문제 2: [백준 2439 - 별 찍기 - 2](https://www.acmicpc.net/problem/2439)

- **난이도**: Bronze V
- **핵심**: 오른쪽 정렬 별 패턴
- **힌트**: 공백 (N-i)개 + 별 i개

### 문제 3: [백준 11718 - 그대로 출력하기](https://www.acmicpc.net/problem/11718)

- **난이도**: Bronze V
- **핵심**: 입력 끝까지 읽기, 그대로 출력
- **힌트**: `readLine()`이 null을 반환할 때까지 반복

---

## 7. 보스 문제

### [백준 1152 - 단어의 개수](https://www.acmicpc.net/problem/1152)

- **난이도**: Bronze II
- **핵심**: 문자열 처리 종합. `trim()` + `split()` 활용
- **포인트**: 앞뒤 공백 처리, 빈 문자열 예외 처리, split 결과 배열 활용
- **힌트**: `trim()` 후 `split(" ")`으로 분리. 빈 문자열이면 0 출력

### 회고 체크리스트

1. 이 문제의 시간/공간 복잡도는?
2. `trim()`을 쓰지 않았다면 어떤 문제가 발생했을 것인가?
3. 빈 입력(" ")에 대한 예외 처리를 했는가?

---

## prep 완료 체크포인트

prep 3개 단원을 모두 클리어했으면 stage2(OOP)로 진행.
stage2까지 완료하면 **Silver** 랭크 획득!

다음 단계: [stage2 — OOP 기초](../../stage2/docs/2.1.class.md)
