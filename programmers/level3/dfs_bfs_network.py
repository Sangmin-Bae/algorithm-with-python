"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 네트워크
    유형       : DFS / BFS
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/43162
    풀이일자   : 2026-07-22
================================================================================
[문제 요약]
    n개 컴퓨터와 연결 정보(인접 행렬)가 주어질 때
    연결된 컴포넌트(네트워크)의 수 반환

    제약 조건
        - n: 1 이상 200 이하
        - computers[i][i] = 1 (자기 자신과 항상 연결)
        - computers[i][j] == computers[j][i] (무방향 그래프)
================================================================================
[입출력 예시]
    n | computers                          | return
    --|------------------------------------|---------
    3 | [[1,1,0],[1,1,0],[0,0,1]]          | 2
    3 | [[1,1,0],[1,1,1],[0,1,1]]          | 1
================================================================================
[핵심 아이디어 - 연결 컴포넌트 수 세기]
    방문하지 않은 노드를 발견할 때마다 새 네트워크 시작
    해당 노드에서 탐색 가능한 모든 노드를 방문 처리
    -> 다음 for 순회에서 이미 방문된 노드는 건너뜀

    DFS vs BFS 선택:
        최단 거리 -> BFS 필요
        특정 경로 탐색 -> DFS 유리
        연결 컴포넌트 수 -> DFS / BFS 모두 동일하게 사용 가능
            탐색 순서만 다를 뿐 같은 컴포넌트의 모든 노드를 방문하므로 결과 동일

[computers[i][i] = 1 처리]
    자기 자신과 항상 연결되어 있으므로 dfs(node) 호출 시
    neighbor = node인 경우 computers[node][node] = 1 조건 충족
    -> visited[node] = True를 재귀 호출 전에 먼저 처리해야 무한 루프 방지
    solution_one에서 visited[node] = True가 for 루프보다 앞에 있어 안전

[재귀 깊이 주의]
    n <= 200 -> 최악 재귀 깊이 200
    Python 기본 재귀 한도 1000이므로 이 문제에서 안전
    n이 더 컸다면 sys.setrecursionlimit 또는 BFS 방식 필요

[yield + 제너레이터 방식 미적용 이유]
    DFS에서 반환값이 필요 없고 visited 갱신(side effect)만 필요
    제너레이터는 지연 평가나 값을 전달할 때 유용
    반환값 없는 side effect 전용 함수에서 yield는 불필요한 복잡도 추가
================================================================================
[내 초기 풀이]
    solution_mine_one: 재귀 DFS + 외부 for 루프로 시작점 탐색
    solution_mine_two: deque BFS + 외부 for 루프로 시작점 탐색

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       재귀 DFS로 코드 간결, DFS 컴포넌트 탐색 표준 패턴
    solution_mine_two: 개선 필요 없음 - Sub
                       재귀 없이 명시적 큐로 동작 원리 명시적
================================================================================
[복잡도 분석]
    N = n (최대 200)

    Mine_one - 시간: O(N²) | 공간: O(N) - visited O(N) + 재귀 스택 O(N)
                             인접 행렬 전체 순회: N개 노드 × N개 이웃 = O(N²)
    Mine_two - 시간: O(N²) | 공간: O(N) - visited O(N) + deque O(N)
                             인접 행렬 전체 순회: O(N²)
    Best     - 시간: O(N²) | 공간: O(N) - Mine_one과 동일
    Sub      - 시간: O(N²) | 공간: O(N) - Mine_two와 동일

    N=200: 최대 40,000 연산 -> 충분히 빠름
"""

from collections import deque
import time


# ================================================================================
# Mine solution one - 재귀 DFS
# ================================================================================
def solution_mine_one(n: int, computers: list[list[int]]) -> int:
    """
    재귀 DFS로 연결 컴포넌트를 탐색하고 개수를 세는 풀이

    핵심:
        visited[node] = True를 for 루프 전에 처리
            -> computers[node][node]=1이므로 방문 전 처리 없으면 무한 루프
        dfs(i) 호출 완료 = 하나의 네트워크 전체 탐색 완료 -> network_cnt += 1
        if not visited[i]: 이미 다른 네트워크 탐색 중 방문된 노드는 시작점으로 불필요

    재귀 구조:
        모든 이웃을 탐색하는 for 루프
        -> 방문 가능한 이웃마다 재귀 호출
        -> 재귀 완료 시 해당 컴포넌트의 모든 노드 방문 완료
    """
    visited = [False] * n
    network_cnt = 0

    def dfs(node: int) -> None:
        visited[node] = True                        # 방문 처리 (for 루프 전 필수)

        for neighbor in range(n):
            if computers[node][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:
            dfs(i)
            network_cnt += 1                        # dfs 완료 = 한 네트워크 탐색 완료

    return network_cnt


# ================================================================================
# Mine solution two - deque BFS
# ================================================================================
def solution_mine_two(n: int, computers: list[list[int]]) -> int:
    """
    deque BFS로 연결 컴포넌트를 탐색하고 개수를 세는 풀이

    핵심:
        queue에 시작 노드를 넣고 visited 처리를 동시에 수행
            -> 큐에 넣는 시점에 visited 처리해야 중복 삽입 방지
        while queue: 현재 컴포넌트의 모든 노드 탐색 완료까지 반복
        for 루프의 if not visited[i]: DFS와 동일하게 중복 시작점 방지

    DFS 대비:
        재귀 없이 명시적 큐로 탐색
        레벨 단위 탐색 (이 문제에서 레벨 구분 불필요)
        재귀 깊이 제한 없음 -> n이 클 때 안전
    """
    visited = [False] * n
    network_cnt = 0

    for i in range(n):
        if not visited[i]:
            network_cnt += 1

            queue = deque([i])
            visited[i] = True                       # 큐 삽입 시점에 방문 처리

            while queue:
                node = queue.popleft()
                for neighbor in range(n):
                    if computers[node][neighbor] == 1 and not visited[neighbor]:
                        visited[neighbor] = True    # 삽입 시점에 방문 처리
                        queue.append(neighbor)

    return network_cnt


# ================================================================================
# Best solution - 재귀 DFS (mine_one 주석 보강)
# ================================================================================
def solution_best(n: int, computers: list[list[int]]) -> int:
    """
    재귀 DFS로 연결 컴포넌트 수를 세는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        재귀 DFS: 컴포넌트 탐색 표준 패턴, 코드 간결
        visited[node] = True 선행: computers[i][i]=1 자기참조 무한 루프 방지
        dfs() 완료 시점에 network_cnt += 1: 컴포넌트 경계 명확
        n <= 200 -> 재귀 깊이 최대 200, Python 기본 한도(1000) 이내 안전
    """
    visited = [False] * n
    network_cnt = 0

    def dfs(node: int) -> None:
        visited[node] = True

        for neighbor in range(n):
            if computers[node][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:
            dfs(i)
            network_cnt += 1

    return network_cnt


# ================================================================================
# Sub solution - deque BFS (mine_two 주석 보강)
# ================================================================================
def solution_sub(n: int, computers: list[list[int]]) -> int:
    """
    deque BFS로 연결 컴포넌트 수를 세는 서브 풀이

    Best 대비 특징:
        재귀 없이 명시적 큐로 탐색 -> 재귀 깊이 제한 없음
        n이 매우 클 때 (n >> 1000) 더 안전
        visited를 큐 삽입 시점에 처리 -> 중복 삽입 방지
        탐색 순서는 다르나 컴포넌트 내 모든 노드 방문 결과 동일
    """
    visited = [False] * n
    network_cnt = 0

    for i in range(n):
        if not visited[i]:
            network_cnt += 1
            queue = deque([i])
            visited[i] = True

            while queue:
                node = queue.popleft()
                for neighbor in range(n):
                    if computers[node][neighbor] == 1 and not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

    return network_cnt


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[list[int]], int]] = [
        # (n, computers, 기댓값)
        # 손 추적:
        # n=3, [[1,1,0],[1,1,0],[0,0,1]]
        # 0 시작: dfs(0) -> visited[0]=True
        #   neighbor=0: visited -> skip
        #   neighbor=1: computers[0][1]=1, 미방문 -> dfs(1)
        #     neighbor=0: visited -> skip
        #     neighbor=1: visited -> skip
        #     neighbor=2: computers[1][2]=0 -> skip
        #   neighbor=2: computers[0][2]=0 -> skip
        # dfs(0) 완료 -> network_cnt=1
        # 1: visited -> skip
        # 2: 미방문 -> dfs(2) -> visited[2]=True -> network_cnt=2
        (3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2),
        # n=3, [[1,1,0],[1,1,1],[0,1,1]]
        # 모두 연결 -> 1개
        (3, [[1, 1, 0], [1, 1, 1], [0, 1, 1]], 1),
        # 추가 케이스:
        # n=1: 컴퓨터 1개 -> 네트워크 1개
        (1, [[1]], 1),
        # n=4: 2+2 분리
        # 0-1 연결, 2-3 연결, 0-2 미연결
        (4, [[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]], 2),
        # n=4: 모두 분리 -> 4개
        (4, [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], 4),
    ]

    solutions = [
        ("Mine_one (재귀DFS) ", solution_mine_one),
        ("Mine_two (deque BFS)", solution_mine_two),
        ("Best     (재귀DFS) ", solution_best),
        ("Sub      (deque BFS)", solution_sub),
    ]

    # 워밍업 스텝
    _n, _c, _ = test_cases[0]
    for _, func in solutions:
        func(_n, [row[:] for row in _c])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (n, computers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, [row[:] for row in computers])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
