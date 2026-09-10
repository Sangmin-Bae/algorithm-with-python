"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 등굣길
    유형       : DP (Dynamic Programming)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42898
    풀이일자   : 2026-09-10
===================================================================================
[문제 요약]
    m×n 격자에서 (1,1)→(m,n)까지 오른쪽/아래로만 이동하는
    최단 경로의 개수를 1,000,000,007로 나눈 나머지 반환
    웅덩이 위치는 통과 불가

    제약 조건
        - m, n: 1 이상 100 이하
        - puddles: 0개 이상 10개 이하
        - (1,1), (m,n)에는 웅덩이 없음
===================================================================================
[입출력 예시]
    m | n | puddles | return
    --|---|---------|-------
    4 | 3 | [[2,2]] | 4
===================================================================================
[왜 DP인가]
    BFS: 최단 경로 길이 → 가능
         최단 경로 개수 → 부적합 (같은 레벨 경로를 세는 구조 없음)

    DFS(완전탐색): 모든 경로 열거 가능
        최악 O(2^(m+n)) → m=n=100이면 불가능

    DP: 중복 계산 제거 → O(m×n)
        오른쪽/아래로만 이동 → (i,j)의 직전 위치는
        반드시 (i-1,j) 또는 (i,j-1) 둘 중 하나
        두 경우 겹치지 않음 → 단순 합산 가능

[DP 점화식]
    dp[i][j] = "(1,1)에서 (i,j)까지 도달하는 최단 경로 수"

    dp[i][j] = dp[i-1][j] + dp[i][j-1]   (웅덩이 아닌 경우)
    dp[i][j] = 0                           (웅덩이인 경우)

[패딩(+1 크기) 방식]
    dp = [[0] * (m+1) for _ in range(n+1)]
    인덱스 1부터 사용, 0행/0열을 경계 0으로 활용
    dp[i-1][j], dp[i][j-1] 범위 밖 → 자동으로 0
    별도의 범위 체크 없이 처리

[puddle 좌표 변환]
    puddles 원소: [x, y] = [열, 행]
    dp 접근: dp[행][열] = dp[i][j]
    → {(y,x) for x,y in puddles}: 행,열 기준으로 변환
    set으로 in 연산 O(1)

[실측 결과 — m=n=100, 10,000회]
    one (Bottom-up): 1163.2μs  ← 4.8배 빠름
    two (Top-down):  5593.9μs

    Bottom-up이 빠른 이유:
        Top-down: 재귀 함수 호출마다 스택 프레임 생성
        Bottom-up: 반복문, 스택 프레임 없음
===================================================================================
[내 초기 풀이]
    solution_mine_one: Bottom-up 타뷸레이션
    solution_mine_two: Top-down 메모이제이션 + 재귀

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       반복문 기반 Bottom-up, 4.8배 빠름
    solution_mine_two: 재귀 오버헤드로 느림 - Sub
                       DP 원리 이해에 유용
===================================================================================
[복잡도 분석]
    M = m (최대 100), N = n (최대 100)

    Mine_one - 시간: O(M×N) | 공간: O(M×N) - dp 2차원 배열
    Mine_two - 시간: O(M×N) | 공간: O(M×N) - memo + 재귀 스택
    Best     - 시간: O(M×N) | 공간: O(M×N) - Mine_one과 동일
    Sub      - 시간: O(M×N) | 공간: O(M×N) - Mine_two와 동일
"""

import sys
import time

sys.setrecursionlimit(20000)

MOD = 1_000_000_007


# =================================================================================
# Mine solution one - Bottom-up 타뷸레이션
# =================================================================================
def solution_mine_one(m: int, n: int, puddles: list[list[int]]) -> int:
    """
    (1,1)부터 (n,m)까지 순서대로 경로 수를 채우는 Bottom-up DP 풀이

    dp[i][j] = "(1,1)에서 (i,j)까지 최단 경로 수"

    패딩(+1 크기):
        0행/0열을 경계 0으로 활용
        dp[i-1][j], dp[i][j-1] 범위 밖 → 자동으로 0

    puddle_set {(y,x)}:
        puddles [x,y] → (행,열) = (y,x)로 변환
        set in 연산 O(1)
    """
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    puddle_set = {(y, x) for x, y in puddles}
    dp[1][1] = 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if i == 1 and j == 1:
                continue
            if (i, j) in puddle_set:
                dp[i][j] = 0
            else:
                dp[i][j] = (dp[i - 1][j] + dp[i][j - 1]) % MOD

    return dp[n][m]


# =================================================================================
# Mine solution two - Top-down 메모이제이션
# =================================================================================
def solution_mine_two(m: int, n: int, puddles: list[list[int]]) -> int:
    """
    (n,m)에서 (1,1)로 재귀하며 경로 수를 구하는 Top-down DP 풀이

    find_path(i, j) = "(1,1)에서 (i,j)까지 최단 경로 수"
    (n,m) 호출 → 재귀로 (1,1)까지 내려감 → 올라오며 합산

    memo[i][j] != -1: 이미 계산된 값 재사용
    i<1 or j<1: 범위 밖 → 0 반환
    (i,j) in puddle_set: 웅덩이 → 0 반환

    한계:
        재귀 호출마다 스택 프레임 생성
        m=n=100이면 최악 10,000번 재귀
        Bottom-up 대비 4.8배 느림
    """
    memo = [[-1] * (m + 1) for _ in range(n + 1)]
    puddle_set = {(y, x) for x, y in puddles}

    def find_path(i: int, j: int) -> int:
        if i == 1 and j == 1:
            return 1
        if i < 1 or j < 1 or (i, j) in puddle_set:
            return 0
        if memo[i][j] != -1:
            return memo[i][j]
        memo[i][j] = (find_path(i - 1, j) + find_path(i, j - 1)) % MOD
        return memo[i][j]

    return find_path(n, m)


# =================================================================================
# Best solution - Bottom-up 타뷸레이션 (mine_one 주석 보강)
# =================================================================================
def solution_best(m: int, n: int, puddles: list[list[int]]) -> int:
    """
    반복문 기반 Bottom-up으로 O(M×N) 시간에 최단 경로 수를 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        재귀 스택 프레임 없음 → Top-down 대비 4.8배 빠름
        패딩으로 경계 처리 간결
        실측 m=n=100: 1163μs (Top-down 5594μs 대비 우위)
    """
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    puddle_set = {(y, x) for x, y in puddles}
    dp[1][1] = 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if i == 1 and j == 1:
                continue
            if (i, j) in puddle_set:
                dp[i][j] = 0
            else:
                dp[i][j] = (dp[i - 1][j] + dp[i][j - 1]) % MOD

    return dp[n][m]


# =================================================================================
# Sub solution - Top-down 메모이제이션 (mine_two 주석 보강)
# =================================================================================
def solution_sub(m: int, n: int, puddles: list[list[int]]) -> int:
    """
    재귀 + 메모이제이션으로 DP 원리를 명시적으로 표현하는 서브 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        (n,m) 질문 → (1,1)까지 재귀 → 올라오며 합산
        Top-down 방향이 점화식 "직전에서 왔다"를 자연스럽게 표현
        Best 대비 재귀 오버헤드로 4.8배 느림
        sys.setrecursionlimit 설정 권장 (m=n=100 → 최대 10,000 재귀)
    """
    memo = [[-1] * (m + 1) for _ in range(n + 1)]
    puddle_set = {(y, x) for x, y in puddles}

    def find_path(i: int, j: int) -> int:
        if i == 1 and j == 1:
            return 1
        if i < 1 or j < 1 or (i, j) in puddle_set:
            return 0
        if memo[i][j] != -1:
            return memo[i][j]
        memo[i][j] = (find_path(i - 1, j) + find_path(i, j - 1)) % MOD
        return memo[i][j]

    return find_path(n, m)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (m, n, puddles, 기댓값)
        # 공식 예시
        (4, 3, [[2, 2]], 4),
        # 추가 케이스:
        # 1행: 오른쪽으로만
        # 손 추적: (1,1)→(2,1)→(3,1)→(4,1): 1가지
        (4, 1, [],       1),
        # 1열: 아래로만
        (1, 3, [],       1),
        # 2×2 격자: (1,1)→(1,2)→(2,2) 또는 (1,1)→(2,1)→(2,2) → 2가지
        (2, 2, [],       2),
        # 3×3, 중앙 웅덩이
        (3, 3, [[2, 2]], 2),
    ]

    solutions = [
        ("Mine_one (Bottom-up)", solution_mine_one),
        ("Mine_two (Top-down) ", solution_mine_two),
        ("Best     (Bottom-up)", solution_best),
        ("Sub      (Top-down) ", solution_sub),
    ]

    # 워밍업 스텝
    _m, _n, _p, _ = test_cases[0]
    for _, func in solutions:
        func(_m, _n, _p)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (m, n, puddles, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(m, n, puddles)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
