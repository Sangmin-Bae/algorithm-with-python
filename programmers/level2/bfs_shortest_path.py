"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 게임 맵 최단거리
    유형       : BFS (너비 우선 탐색)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/1844
    풀이일자   : 2026-07-16
================================================================================
[문제 요약]
    N×M 격자에서 (0,0)에서 (N-1,M-1)까지 최단 거리 반환
    0=벽, 1=길, 도달 불가 시 -1 반환
    상하좌우 1칸씩 이동

    제약 조건
        - N, M: 1 이상 100 이하
        - maps: 0과 1로만 구성
        - N과 M이 모두 1인 경우 없음
================================================================================
[입출력 예시]
    maps                                         | answer
    ---------------------------------------------|-------
    [[1,0,1,1,1],[1,0,1,0,1],                   | 11
     [1,0,1,1,1],[1,1,1,0,1],[0,0,0,0,1]]       |
    [[1,0,1,1,1],[1,0,1,0,1],                   | -1
     [1,0,1,1,1],[1,1,1,0,0],[0,0,0,0,1]]       |
================================================================================
[왜 BFS인가 — DFS vs BFS]
    DFS: 경로를 끝까지 탐색 후 다른 경로로 이동
         → 처음 도달하는 경로가 최단이 아닐 수 있음 → 최단 거리 보장 불가

    BFS: 레벨 단위로 탐색 (거리 1인 모든 노드 → 거리 2인 모든 노드 → ...)
         → 처음 목표에 도달하는 순간이 항상 최단 거리 → 최단 거리 보장

[BFS 거리 추적 방식 비교]
    solution_one: distance 2D 배열 별도 관리
        visited, distance 두 배열 → 공간 O(N×M) × 2

    solution_two: 레벨 BFS + 외부 정수 distance
        for _ in range(len(queue)): 현재 레벨 전부 처리 후 distance += 1
        BFS의 레벨 구조를 코드에 명시적으로 표현

    solution_three: (y, x, dist) 튜플로 큐 내부 관리
        dist + 1을 다음 노드에 전달 → distance 배열 불필요
        가장 간결하고 정확

    solution_four: maps 자체에 거리 기록
        maps[ny][nx] == 1 조건이 visited 역할 (방문 즉시 1 초과로 갱신)
        → 재진입 조건 미충족 → 중복 삽입 원천 차단
        (0,0)은 maps[0][0]=1 유지 → 인접 셀 처리 시 재방문 위험
        → if ny==0 and nx==0: continue로 예외 처리
        (0,0)은 좌측 상단 코너라 돌아오는 경로가 물리적으로 없음
        continue는 (0,0) 인접 셀 처리 시 사실상 2회만 실행

    solution_five: maps를 -1로 방문 표시 + 큐 내부 dist
        maps[0][0] = -1로 즉시 방문 표시 → (0,0) 재방문 원천 차단
        0=벽, 1=미방문 길, -1=방문 완료로 재정의
        solution_four의 continue 예외 처리 불필요

    solution_six: maps[0][0]=2로 시작 + maps에 거리 기록
        maps[0][0] = 2로 초기화 → maps==1 조건에 걸리지 않아 재방문 차단
        solution_four 아이디어(maps에 거리 기록)에 continue 예외 처리 불필요
        최종 도달 시 maps[N-1][M-1] - 1로 거리 보정 (시작값 2이므로)

    maps 오염 방식 세 가지 비교:
        four: maps[0][0]=1 유지 + continue 예외 처리 (코너 구조 의존)
        five: maps[0][0]=-1 + 큐 내부 dist (구조 무관, 가장 견고)
        six:  maps[0][0]=2 + maps 거리 기록 + 최종 -1 보정 (four 완성형)
================================================================================
[내 초기 풀이]
    solution_mine_one  : 정석 BFS (visited + distance 2D 배열)
    solution_mine_two  : 레벨 BFS (for _ in range(len(queue)) + 외부 distance)
    solution_mine_three: 큐 내부 dist 튜플 (y, x, dist)
    solution_mine_four : maps에 거리 기록 + continue 예외 처리
    solution_mine_five : maps -1 방문 표시 + 큐 내부 dist
    solution_mine_six  : maps[0][0]=2 시작 + maps에 거리 기록

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         정석 BFS, 동작 원리 명시적, visited/distance 분리
    solution_mine_two  : 개선 필요 없음
                         레벨 BFS 구조 명시적 표현
    solution_mine_three: 개선 필요 없음 - Best
                         추가 자료구조 최소화, 간결하고 정확
    solution_mine_four : 개선 필요 없음 (학습 목적)
                         maps==1 조건이 visited 역할 → 중복 삽입 차단
                         (0,0) 예외만 continue로 처리 → 정상 동작
                         코너 구조에 의존 → six로 continue 제거 가능
    solution_mine_five : 개선 필요 없음 (학습 목적)
                         maps 오염 방식 중 가장 견고한 구현
    solution_mine_six  : 개선 필요 없음 (학습 목적)
                         four의 continue 예외를 시작값 변경으로 제거
================================================================================
[복잡도 분석]
    N = 행 수, M = 열 수 (최대 100×100 = 10,000)

    Mine_one   - 시간: O(N×M) | 공간: O(N×M) - visited + distance 2D 배열 × 2
    Mine_two   - 시간: O(N×M) | 공간: O(N×M) - visited 2D 배열
    Mine_three - 시간: O(N×M) | 공간: O(N×M) - visited 2D 배열, dist는 튜플
    Mine_four  - 시간: O(N×M) | 공간: O(1)   - maps 오염, maps==1이 visited 역할
    Mine_five  - 시간: O(N×M) | 공간: O(1)   - maps 오염, -1로 방문 표시
    Mine_six   - 시간: O(N×M) | 공간: O(1)   - maps 오염, 시작값 2로 초기화
    Best       - 시간: O(N×M) | 공간: O(N×M) - Mine_three와 동일
    Sub        - 시간: O(N×M) | 공간: O(N×M) - Mine_one과 동일

    모든 풀이 시간복잡도 O(N×M): 각 셀 최대 1번 방문
"""

import time
from collections import deque


# ================================================================================
# Mine solution one - 정석 BFS (visited + distance 2D 배열)
# ================================================================================
def solution_mine_one(maps: list[list[int]]) -> int:
    """
    visited와 distance 2차원 배열로 BFS를 수행하는 정석 풀이

    핵심:
        visited[y][x]: 방문 여부 추적 → 중복 방문 방지
        distance[y][x]: (0,0)에서 해당 좌표까지 거리 기록
        distance[0][0] = 1: 시작칸 포함 계산

    dy, dx 방향 배열:
        상(-1,0), 하(1,0), 좌(0,-1), 우(0,1)
        for i in range(4)로 4방향 순회

    도달 즉시 반환:
        BFS 특성상 처음 (N-1,M-1)에 도달하는 순간이 최단 거리
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0)])

    visited = [[False] * M for _ in range(N)]
    distance = [[0] * M for _ in range(N)]
    visited[0][0] = True
    distance[0][0] = 1

    dy = [-1, 1, 0, 0]
    dx = [0, 0, -1, 1]

    while queue:
        y, x = queue.popleft()

        if y == N - 1 and x == M - 1:
            return distance[y][x]

        for i in range(4):
            ny = y + dy[i]
            nx = x + dx[i]

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    distance[ny][nx] = distance[y][x] + 1
                    queue.append((ny, nx))

    return -1


# ================================================================================
# Mine solution two - 레벨 BFS (for _ in range(len(queue)) + 외부 distance)
# ================================================================================
def solution_mine_two(maps: list[list[int]]) -> int:
    """
    레벨 단위로 BFS를 수행하고 외부 정수 distance로 거리를 추적하는 풀이

    레벨 BFS 구조:
        for _ in range(len(queue)): 현재 레벨의 모든 노드 처리
        현재 레벨 완료 후 distance += 1
        → BFS의 레벨 구조를 코드에 명시적으로 표현

    mine_one 대비:
        distance 2D 배열 → 외부 정수 1개로 대체
        directions 리스트[튜플]: for i in range(4) 대신 직관적 표현
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0)])

    visited = [[False] * M for _ in range(N)]
    visited[0][0] = True

    distance = 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        for _ in range(len(queue)):
            y, x = queue.popleft()

            if y == N - 1 and x == M - 1:
                return distance

            for dy, dx in directions:
                ny = y + dy
                nx = x + dx

                if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                    if not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((ny, nx))

        distance += 1

    return -1


# ================================================================================
# Mine solution three - 큐 내부 dist 튜플 (y, x, dist)
# ================================================================================
def solution_mine_three(maps: list[list[int]]) -> int:
    """
    (y, x, dist) 튜플로 거리를 큐 내부에서 관리하는 풀이

    mine_one 대비:
        distance 2D 배열 없이 dist를 튜플에 담아 전달
        dist + 1을 다음 노드에 바로 전달 → 별도 배열 불필요

    visited 배열은 여전히 필요:
        dist가 큐 내부에 있어도 중복 방문 방지는 별도 필요
        visited 없으면 같은 셀이 여러 번 큐에 삽입될 수 있음
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0, 1)])

    visited = [[False] * M for _ in range(N)]
    visited[0][0] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        y, x, dist = queue.popleft()

        if y == N - 1 and x == M - 1:
            return dist

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((ny, nx, dist + 1))

    return -1


# ================================================================================
# Mine solution four - maps에 거리 기록 + continue 예외 처리
# ================================================================================
def solution_mine_four(maps: list[list[int]]) -> int:
    """
    maps 자체에 거리를 기록해 visited/distance 배열을 사용하지 않는 풀이

    아이디어:
        maps[ny][nx] == 1: 길이면서 미방문 → 방문 가능
        maps[ny][nx] = maps[y][x] + 1: 방문 즉시 거리로 갱신 (1 초과)
        → 재진입 조건 미충족 → 중복 삽입 원천 차단

    if ny == 0 and nx == 0: continue 필요 이유:
        (0,0)은 maps[0][0] = 1로 초기값 유지 (거리 기록 안 됨)
        (1,0) 또는 (0,1) 처리 시 4방향 탐색에 (0,0)이 포함
        → maps[0][0]이 잘못된 거리 값으로 오염될 위험 → continue로 방지
        (0,0)은 좌측 상단 코너 → 돌아오는 경로가 물리적으로 없음
        continue는 (0,0) 인접 셀 처리 시 사실상 2회만 실행

    solution_six로 개선:
        maps[0][0] = 2로 초기화하면 continue 예외 처리 불필요
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0)])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        y, x = queue.popleft()

        if y == N - 1 and x == M - 1:
            return maps[y][x]

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                if ny == 0 and nx == 0:
                    continue

                maps[ny][nx] = maps[y][x] + 1
                queue.append((ny, nx))

    return -1


# ================================================================================
# Mine solution five - maps -1 방문 표시 + 큐 내부 dist
# ================================================================================
def solution_mine_five(maps: list[list[int]]) -> int:
    """
    maps에 -1로 방문 표시해 구조에 무관하게 견고하게 동작하는 풀이

    mine_four 대비:
        maps[ny][nx] = -1: 즉시 방문 표시
        0=벽, 1=미방문 길, -1=방문 완료로 재정의
        maps[0][0] = -1로 시작점 표시 → continue 예외 처리 불필요
        dist는 큐 내부 튜플로 관리 → distance 배열 불필요

    실무 적합성:
        원본 maps가 변경됨 → 함수 호출 후 maps 재사용 불가
        코딩테스트에서는 허용되나 실무에서는 지양
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0, 1)])

    maps[0][0] = -1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        y, x, dist = queue.popleft()

        if y == N - 1 and x == M - 1:
            return dist

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                maps[ny][nx] = -1
                queue.append((ny, nx, dist + 1))

    return -1


# ================================================================================
# Mine solution six - maps[0][0]=2 시작 + maps에 거리 기록 (four 개선)
# ================================================================================
def solution_mine_six(maps: list[list[int]]) -> int:
    """
    시작점을 2로 초기화해 solution_four의 continue 예외 처리를 제거한 풀이

    mine_four 대비 개선:
        maps[0][0] = 1 유지 → (0,0) 재방문 시 maps==1 조건 통과 위험
        → if ny==0 and nx==0: continue 예외 처리 필요

        maps[0][0] = 2로 초기화:
        → (0,0) 재방문 시 maps[0][0]=2 → maps==1 조건 미충족 → 자동 차단
        → continue 예외 처리 불필요

    거리 보정:
        시작값이 2이므로 최종 도달 시 실제거리 = maps[N-1][M-1] - 1

    maps 오염 방식 세 가지 비교:
        four: maps[0][0]=1 유지 + continue (코너 구조 의존)
        five: maps[0][0]=-1 + 큐 내부 dist (구조 무관, 가장 견고)
        six:  maps[0][0]=2 + maps 거리 기록 + 최종 -1 보정 (four 완성형)
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0)])

    maps[0][0] = 2

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        y, x = queue.popleft()

        if y == N - 1 and x == M - 1:
            return maps[y][x] - 1

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                maps[ny][nx] = maps[y][x] + 1
                queue.append((ny, nx))

    return -1


# ================================================================================
# Best solution - 큐 내부 dist 튜플 (mine_three 주석 보강)
# ================================================================================
def solution_best(maps: list[list[int]]) -> int:
    """
    (y, x, dist) 튜플로 거리를 큐 내부에서 관리하는 최적 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        distance 2D 배열 불필요 → 메모리 절약
        dist + 1을 다음 노드에 직접 전달 → 코드 간결
        visited 배열로 중복 삽입 정확하게 방지
        BFS 동작 원리: 처음 (N-1,M-1)에 도달하는 dist가 최단 거리 보장
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0, 1)])

    visited = [[False] * M for _ in range(N)]
    visited[0][0] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        y, x, dist = queue.popleft()

        if y == N - 1 and x == M - 1:
            return dist

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((ny, nx, dist + 1))

    return -1


# ================================================================================
# Sub solution - 정석 BFS (mine_one 주석 보강)
# ================================================================================
def solution_sub(maps: list[list[int]]) -> int:
    """
    visited와 distance 2D 배열로 BFS를 수행하는 서브 풀이

    Best 대비 특징:
        visited, distance를 분리된 배열로 관리
        각 좌표의 거리가 distance 배열에 명시적으로 보존
        BFS의 동작 원리(레벨 탐색, 거리 갱신)가 코드에 직접 드러남
        O(N×M) 추가 공간 사용 (distance 배열)
    """
    N, M = len(maps), len(maps[0])
    queue = deque([(0, 0)])

    visited = [[False] * M for _ in range(N)]
    distance = [[0] * M for _ in range(N)]
    visited[0][0] = True
    distance[0][0] = 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        y, x = queue.popleft()

        if y == N - 1 and x == M - 1:
            return distance[y][x]

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx

            if 0 <= ny < N and 0 <= nx < M and maps[ny][nx] == 1:
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    distance[ny][nx] = distance[y][x] + 1
                    queue.append((ny, nx))

    return -1


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증한다"""

    test_cases: list[tuple[list[list[int]], int]] = [
        # (maps, 기댓값)
        # 프로그래머스 공식 예시:
        # 최단 경로: 11칸
        ([[1,0,1,1,1],[1,0,1,0,1],[1,0,1,1,1],[1,1,1,0,1],[0,0,0,0,1]], 11),
        # 도달 불가 → -1
        ([[1,0,1,1,1],[1,0,1,0,1],[1,0,1,1,1],[1,1,1,0,0],[0,0,0,0,1]], -1),
        # 추가 케이스:
        # 1×2: (0,0)→(0,1) → 거리 2
        ([[1, 1]], 2),
        # 2×2: (0,0)→(0,1)→(1,1) 또는 (0,0)→(1,0)→(1,1) → 거리 3
        ([[1, 1], [1, 1]], 3),
        # 벽으로 막힌 경우 → -1
        ([[1, 0], [0, 1]], -1),
    ]

    solutions = [
        ("Mine_one   (visited+dist2D)  ", solution_mine_one),
        ("Mine_two   (레벨BFS+int)     ", solution_mine_two),
        ("Mine_three (큐내부dist)      ", solution_mine_three),
        ("Mine_four  (maps거리+continue)", solution_mine_four),
        ("Mine_five  (maps-1+dist)     ", solution_mine_five),
        ("Mine_six   (maps[0][0]=2)    ", solution_mine_six),
        ("Best       (큐내부dist)      ", solution_best),
        ("Sub        (visited+dist2D)  ", solution_sub),
    ]

    # 워밍업 스텝
    _maps, _ = test_cases[0]
    for _, func in solutions:
        func([row[:] for row in _maps])

    print("=" * 70)
    print(f"{'풀이':<32} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (maps, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func([row[:] for row in maps])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<32} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
