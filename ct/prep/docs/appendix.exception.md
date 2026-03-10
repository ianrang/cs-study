# 부록: 예외 처리

> 참고용 문서. 필수 학습 대상이 아니다.

---

## 1. try-catch

예외가 발생할 수 있는 코드를 감싸서 프로그램 비정상 종료를 방지한다.

```java
try {
    int result = 10 / 0;  // ArithmeticException 발생
} catch (ArithmeticException e) {
    System.out.println("0으로 나눌 수 없습니다: " + e.getMessage());
} finally {
    System.out.println("항상 실행되는 블록");
}
```

### 구조

```java
try {
    // 예외가 발생할 수 있는 코드
} catch (예외타입 변수) {
    // 예외 발생 시 처리
} finally {
    // 예외 여부와 관계없이 항상 실행 (선택)
}
```

## 2. 자주 마주치는 예외

| 예외 | 원인 |
|------|------|
| `NullPointerException` | null 참조에서 메서드 호출 |
| `ArrayIndexOutOfBoundsException` | 배열 범위 밖 인덱스 접근 |
| `NumberFormatException` | 숫자로 변환할 수 없는 문자열 |
| `ArithmeticException` | 정수를 0으로 나누기 |
| `StackOverflowError` | 재귀 호출이 너무 깊음 |

## 3. 코테에서의 예외 처리

코딩 테스트에서는 입력이 보장된 환경이므로 **예외 처리가 거의 필요 없다**.

- `BufferedReader` 사용 시 `throws Exception`을 main에 추가하면 충분
- 입력 검증이나 try-catch는 불필요
- 예외가 발생한다면 로직 자체의 오류이므로, 예외를 잡는 것보다 로직을 수정해야 한다
