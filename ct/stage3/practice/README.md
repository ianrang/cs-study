# stage3 practice — 컬렉션 (Gold)

## 폴더 구조

```
practice/
├── ex/                  직접 작성 과제
├── prob/                코딩 문제 (BOJ / 직접 설계)
└── boss/                보스 문제
```

---

## 3.1 제너릭

### ex/
- `Ex01_GenericStack.java` — GenericStack<T> (push, pop, peek, isEmpty, size)
- `Ex02_CountMethod.java` — count<T> 메서드 (배열에서 특정 값 개수)

### prob/
- `Pair.java` — Pair<K, V> 클래스 (이름-나이 쌍)
- `FindMax.java` — findMax<T extends Comparable<T>> (배열 최댓값)

### boss/
- `SimpleList.java` — SimpleList<T> 직접 구현 (add, get, size, remove)

---

## 3.2 List (ArrayList)

### ex/
- `Ex05_ReverseList.java` — N개 정수 ArrayList 역순 출력 (Collections.reverse)
- `Ex06_WordFreq.java` — 단어 빈도 세기 (Collections.frequency)

### prob/
- `Boj10807.java` — 개수 세기 (Bronze V)
- `Boj10810.java` — 공 넣기 (Bronze III)

### boss/
- `Boj1158.java` — 요세푸스 문제 (Silver IV)

---

## 3.3 Set (HashSet)

### ex/
- `Ex07_UniqueCount.java` — 정수 배열 고유 요소 개수
- `Ex08_SetOps.java` — 합집합, 교집합, 차집합 출력

### prob/
- `Boj3052.java` — 나머지 (Bronze II)
- `Boj11478.java` — 서로 다른 부분 문자열 (Silver III)

### boss/
- `Boj1764.java` — 듣보잡 (Silver IV)

---

## 3.4 Map (HashMap)

### ex/
- `Ex09_CharFreq.java` — 문자 출현 횟수 (빈도 분석)
- `Ex10_PhoneBook.java` — 이름-전화번호 전화번호부 (getOrDefault)

### prob/
- `Boj10816.java` — 숫자 카드 2 (Silver IV)
- `Boj1620.java` — 나는야 포켓몬 마스터 (Silver IV)

### boss/
- `Boj1157.java` — 단어 공부 (Bronze I)
