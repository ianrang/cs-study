# stage2 practice — OOP 기초 (Silver)

## 폴더 구조

```
practice/
├── ex/                  직접 작성 과제
├── prob/                코딩 문제 (직접 설계 문제)
└── boss/                보스 문제
```

> stage2는 BOJ 대신 직접 설계 문제를 풀기 때문에 prob/ 파일명이 클래스명 기반

---

## 2.1 클래스·객체

### ex/
- `Ex01_Book.java` — Book 클래스 (title, price, 생성자, getter, toString)
- `Ex02_BookChain.java` — 기본 생성자 + title만 받는 생성자 (this() 체이닝)

### prob/
- `Point.java` — Point 클래스 (x, y, 거리 계산 메서드)
- `Student.java` — Student 클래스 (국/영/수 총점·평균)

### boss/
- `BankAccount.java` — BankAccount (deposit, withdraw, getBalance, 출금 검증)

---

## 2.2 상속·다형성

### ex/
- `Ex05_Vehicle.java` — Vehicle → Car, Bicycle (move() 재정의)
- `Ex06_ItemCounter.java` — Item 클래스 (static count 증가)

### prob/
- `Shape.java` — Shape → Triangle, Circle (area() 구현)
- `Intersection.java` — 두 배열의 교집합 (static 메서드)

### boss/
- `Employee.java` — Employee → FullTime, PartTime (다형성 급여 계산)

---

## 2.3 인터페이스·추상

### ex/
- `Ex09_Animal.java` — Animal 추상 클래스 → Dog, Cat, Bird
- `Ex10_Calculable.java` — Calculable 인터페이스 → Adder, Multiplier

### prob/
- `Measurable.java` — Measurable 인터페이스 (BankAccount, Country)
- `Converter.java` — Converter 추상 → KmToMile, CelsiusToFahrenheit

### boss/
- `Payment.java` — Payable 인터페이스 + Employee 추상 + Invoice
