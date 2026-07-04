# Algorithm with Python

Python으로 알고리즘 문제를 풀고 학습하는 저장소입니다.
단순 정답 코드가 아닌, 스스로 고민한 풀이 과정과 이를 개선한 최적 풀이까지 기록합니다.

---

## 개발 환경

| 항목              | 내용 |
|-----------------|-----|
| Language        | Python 3.12.11 |
| Version Manager | pyenv |
| IDE | Pycharm |
| Virtual Env | `.venv` (프로젝트 루트) |

---

## 디렉토리 구조 

```
algorithm-with-python/
├── programmers/
│   ├── level1/
│   ├── level2/
│   └── level3/
├── baekjoon/
│   ├── greedy/
│   ├── dp/
│   ├── bfs/
│   └── ...
├── leetcode/
│   ├── easy/
│   ├── medium/
│   └── hard/
└── codewars/
    ├── kyu6/
    └── kyu5/
```

---

## 파일명 규칙

```
{알고리즘유형}_{문제명}.py
```
 
| Prefix         | 알고리즘 유형  |
|----------------|----------|
| `greedy_`      | 탐욕법      |
| `dp_`          | 동적 프로그래밍 |
| `bfs_`         | 너비 우선 탐색 |
| `dfs_`         | 깊이 우선 탐색 |
| `sort_`        | 정렬       |
| `hash_`        | 해시       |
| `stack_`       | 스택       |
| `heap_`        | 힙        |
| `binary_`      | 이분 탐색    |
| `graph_`       | 그래프      |
| `two_pointer_` | 투 포인터    |
| `sliding_`     | 슬라이딩 윈도우 |
| `math_`        | 수학       |
| `simulation_`  | 시뮬레이션    |

---

## 풀이 파일 구조
 
각 풀이 파일은 아래 구조를 따릅니다.
 
```python
"""
[문제 정보]   사이트 / 카테고리 / 문제명
[문제 요약]   핵심 조건 요약
[입출력 예시] 주요 예시
[풀이 전략]   접근 방식 설명
[복잡도 분석] 시간 O(?), 공간 O(?)
"""
 
# 내가 직접 고민한 풀이 (1개 이상, 시도한 순서대로)
def solution_mine_one():
    pass
 
def solution_mine_two():
    pass
 
# 위 풀이를 바탕으로 개선한 최적 풀이
def solution_best():
    pass
 
# 다른 접근 방식의 대안 풀이
def solution_sub():
    pass
 
# 풀이 간 전략 및 복잡도 비교
def solution_comparison():
    pass
 
if __name__ == "__main__":
    pass
```
 
---
 
## 진행 현황
 
| 사이트      | 풀이 수 |
|-------------|:----:|
| Programmers |  52  |
| Baekjoon    |  -   |
| LeetCode    |  -   |
| Codewars    |  -   |
 
---
 
## Reference
 
- [Programmers](https://programmers.co.kr/)
- [Baekjoon Online Judge](https://www.acmicpc.net/)
- [LeetCode](https://leetcode.com/)
- [Codewars](https://www.codewars.com/)