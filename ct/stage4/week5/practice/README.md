# week5 practice — DP (Diamond 2/2)

## 폴더 구조

```
practice/
├── ex/                  직접 작성 과제
├── prob/                코딩 문제 (BOJ)
└── boss/                보스 문제
```

---

## 5-1 DP 개념

### ex/
- `Ex01_CallCount.java` — 순수 재귀 피보나치 호출 횟수 (n=10,20,30)
- `Ex02_DpJudge.java` — DP 적용 가능 여부 판단 (합, 피보나치, 정렬)

### prob/
- `Boj2748.java` — 피보나치 수 2 (Bronze I)
- `Boj24416.java` — 알고리즘 수업 - 피보나치 수 1 (Bronze I)

### boss/
- `Boj1003.java` — 피보나치 함수 (Silver III)

---

## 5-2 탑다운

### ex/
- `Ex03_Memoization.java` — 순수 재귀에 메모이제이션 추가 (f(n)=f(n-1)+f(n-3))
- `Ex04_StairTopDown.java` — 계단 오르기 변형 (1,2,3칸)

### prob/
- `Boj1904.java` — 01타일 (Silver III)
- `Boj9184.java` — 신나는 함수 실행 (Silver II)

### boss/
- `Boj1932.java` — 정수 삼각형 (Silver I)

---

## 5-3 바텀업

### ex/
- `Ex05_StairBottomUp.java` — 5-2 계단 오르기를 바텀업으로 변환
- `Ex06_SpaceOpt.java` — 배열 대신 변수 3개만 사용 (공간 최적화)

### prob/
- `Boj2747.java` — 피보나치 수 (Bronze II)
- `Boj11726.java` — 2xn 타일링 (Silver III)

### boss/
- `Boj11727.java` — 2xn 타일링 2 (Silver III)

---

## 5-4 1차원 DP

### ex/
- `Ex07_Recurrence.java` — "1,2,3 합으로 n 나타내기" 점화식 세우기
- `Ex08_BottomUp1D.java` — 위 점화식 바텀업 구현

### prob/
- `Boj2579.java` — 계단 오르기 (Silver III)
- `Boj1463.java` — 1로 만들기 (Silver III)

### boss/
- `Boj9095.java` — 1, 2, 3 더하기 (Silver III)

---

## 5-5 2차원 DP

### ex/
- `Ex09_GridPath.java` — 3x4 격자 경로 수 (종이 → 코드 검증)
- `Ex10_KnapsackTrace.java` — 배낭 문제 역추적 (선택 물건 출력)

### prob/
- `Boj1149.java` — RGB거리 (Silver I)
- `Boj11053.java` — 가장 긴 증가하는 부분 수열 (Silver II)

### boss/
- `Boj12865.java` — 평범한 배낭 (Gold V)
