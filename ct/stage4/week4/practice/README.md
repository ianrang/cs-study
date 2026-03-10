# week4 practice — 트리·힙, 그래프, DFS·BFS (Diamond 1/2)

## 폴더 구조

```
practice/
├── ex/                  직접 작성 과제
├── prob/                코딩 문제 (BOJ / 직접 설계)
└── boss/                보스 문제
```

---

## 4-1 트리

### ex/
- `Ex01_TraversalTrace.java` — 전위/중위/후위 순회 결과 종이 → 코드 검증
- `Ex02_TreeBuild.java` — Node 클래스, 트리 생성, 세 가지 순회 출력
- `Ex03_LevelOrder.java` — Queue 사용 레벨 순회 구현

### prob/
- `Boj1991.java` — 트리 순회 (Silver I)

### boss/
- `TraversalRestore.java` — 순회 복원 (전위+중위 → 후위)

---

## 4-2 힙

### ex/
- `Ex04_MinHeap.java` — PriorityQueue N개 정수 오름차순 poll
- `Ex05_MaxHeap.java` — 내림차순 출력 (Comparator.reverseOrder)
- `Ex06_HeapSimulation.java` — 삽입 과정 시뮬레이션 (종이 → 검증)

### prob/
- `Boj1927.java` — 최소 힙 (Silver IV)
- `Boj11279.java` — 최대 힙 (Silver IV)

### boss/
- `Boj11286.java` — 절댓값 힙 (Silver II)

---

## 4-3 그래프

### ex/
- `Ex07_AdjList.java` — 인접 리스트 구성, 각 정점 인접 정점 출력
- `Ex08_AdjMatrix.java` — 인접 행렬 구성, 메모리 비교
- `Ex09_DirectedGraph.java` — 방향 그래프 입력 처리

### prob/
- `Degree.java` — 그래프 입력 템플릿, 각 정점 차수 출력

### boss/
- `GraphConvert.java` — 인접 행렬 ↔ 인접 리스트 변환

---

## 4-4 DFS

### ex/
- `Ex10_DfsRecursive.java` — DFS 재귀 구현, 방문 순서 출력
- `Ex11_DfsStack.java` — 스택 기반 DFS, 재귀 결과와 비교
- `Ex12_ConnectedComp.java` — 연결 요소 개수 구하기

### prob/
- `Boj1260_Dfs.java` — DFS와 BFS (Silver II, DFS 부분)
- `Boj2606.java` — 바이러스 (Silver III)

### boss/
- `Boj11724.java` — 연결 요소의 개수 (Silver II)

---

## 4-5 BFS

### ex/
- `Ex13_BfsOrder.java` — BFS 방문 순서 (종이 → 코드 검증)
- `Ex14_BfsDist.java` — 정점 1에서 각 정점까지 최단 거리
- `Ex15_GridBfs.java` — 5x5 격자 (0,0)→(4,4) 최단 거리

### prob/
- `Boj1260_Bfs.java` — DFS와 BFS (Silver II, BFS 부분)
- `Boj2178.java` — 미로 탐색 (Silver I)

### boss/
- `Boj7576.java` — 토마토 (Gold V)
- `Boj1697.java` — 숨바꼭질 (Silver I)
