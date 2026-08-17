"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 정수 삼각형
    유형       : DP (Dynamic Programming)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/43105
    풀이일자   : 2026-08-17
================================================================================
[문제 요약]
    삼각형 꼭대기에서 바닥까지 경로를 따라 내려갈 때
    거쳐간 숫자의 합의 최댓값 반환

    제약 조건
        - 삼각형 높이: 1 이상 500 이하
        - 각 숫자: 0 이상 9999 이하
================================================================================
[입출력 예시]
    triangle                               | result
    ---------------------------------------|-------
    [[7],[3,8],[8,1,0],[2,7,4,4],[4,5,2,6,5]] | 30
================================================================================
[왜 Greedy가 아닌 DP인가]
    Greedy 실패 반례:
            7
           3 8       ← 8이 더 크므로 Greedy 선택
          8 1 0      ← 8 선택 후 선택지: 1, 0
    최대: 7+8+1 = 16

    최적 경로:
            7
           3          ← Greedy 기준으론 3이 나쁨
          8           ← 3 선택 후 선택지: 8, 1
    최대: 7+3+8 = 18

    "현재 선택(8)이 이후 선택지를 바꾼다" → Greedy 불가 → DP 필요

[DP 핵심 발상]
    dp[i][j] = triangle[i][j]에서 출발해 바닥까지의 최댓값

    점화식:
        dp[i][j] = triangle[i][j] + max(dp[i+1][j], dp[i+1][j+1])

    기저 조건:
        dp[n-1][j] = triangle[n-1][j]  (바닥행은 그 자체)

[Bottom-up vs Top-down]
    Bottom-up (ref_three):
        바닥행부터 위로 순서대로 채움
        "작은 문제를 먼저 전부 해결하고 쌓아올림"
        반복문이 직접 아래에서 위로 처리

    Top-down (ref_one, ref_two):
        꼭대기에서 출발, 필요할 때 재귀로 내려가서 구함
        "큰 문제가 작은 문제를 필요할 때 요청"
        실제 값 확정 순서는 Bottom-up과 같음 (바닥부터)
        차이: "어떤 부분 문제를 계산할지 결정하는 방식"

    두 방식의 공통점:
        값이 실제로 확정되는 순서: 바닥 → 꼭대기
        점화식: dp[i][j] = triangle[i][j] + max(dp[i+1][j], dp[i+1][j+1])

[Bottom-up 손 추적]
    초기:
        [4, 5, 2, 6, 5]  ← 바닥행, dp값 = 자기 자신

    i=3: 바닥 바로 위
        j=0: 2+max(4,5)=7  j=1: 7+max(5,2)=12
        j=2: 4+max(2,6)=10 j=3: 4+max(6,5)=10
        → [7, 12, 10, 10]

    i=2:
        j=0: 8+max(7,12)=20 j=1: 1+max(12,10)=13 j=2: 0+max(10,10)=10
        → [20, 13, 10]

    i=1:
        j=0: 3+max(20,13)=23 j=1: 8+max(13,10)=21
        → [23, 21]

    i=0:
        j=0: 7+max(23,21)=30
        → [30]

    return 30 ✓

[실측 결과 — N=20, 1,000회]
    ref_one (Top-down+memo): 0.409ms
    ref_three (Bottom-up):   0.123ms

    ref_three가 빠른 이유:
        재귀 함수 호출 오버헤드 없음
        반복문 + 단순 인덱스 접근만 수행
================================================================================
[내 초기 풀이]
    solution_mine: DFS 완전탐색 → O(2^N) → 시간 초과

[개선 포인트]
    solution_mine:   O(2^N) → 시간 초과
                     N=500이면 2^500 연산 불가능
                     메모이제이션으로 O(N²)으로 개선 가능

    solution_ref_one: Top-down + 수동 memo - Sub
                      재귀 구조로 DP 발상 명시적
    solution_ref_two: Top-down + @cache
                      ref_one과 동일, Python이 memo 자동 관리
    solution_ref_three: Bottom-up + in-place - Best
                        재귀 없이 가장 빠름, triangle 원본 수정
================================================================================
[복잡도 분석]
    N = 삼각형 높이 (최대 500)
    총 원소 수 = N(N+1)/2

    Mine      - 시간: O(2^N)  | 공간: O(N)    - DFS, 시간 초과
    Ref_one   - 시간: O(N²)   | 공간: O(N²)   - Top-down + memo 배열
    Ref_two   - 시간: O(N²)   | 공간: O(N²)   - Top-down + @cache dict
    Ref_three - 시간: O(N²)   | 공간: O(1)    - Bottom-up, triangle 제자리 수정
    Best      - 시간: O(N²)   | 공간: O(1)    - Ref_three와 동일
    Sub       - 시간: O(N²)   | 공간: O(N²)   - Ref_one과 동일
"""

from functools import cache
import time


# ================================================================================
# Mine solution - DFS 완전탐색 (시간 초과)
# ================================================================================
def solution_mine(triangle: list[list[int]]) -> int:
    """
    모든 경로를 DFS로 탐색해 최댓값을 구하는 초기 풀이 (시간 초과)

    시간 초과 이유:
        각 위치에서 좌/우 두 방향으로 분기 → O(2^N)
        N=500이면 2^500 연산 → 불가능
        dp(i,j)가 여러 경로에서 중복 호출 → 메모이제이션으로 해결 가능

    DP와의 구조적 차이:
        curr_sum을 위에서 아래로 누적
        같은 (i,j)에 다른 경로로 도달해도 별도로 계산
    """
    answer = 0
    n = len(triangle)

    def dfs(i: int, j: int, curr_sum: int) -> None:
        nonlocal answer
        if i == n - 1:
            answer = max(answer, curr_sum)
            return
        dfs(i + 1, j,     curr_sum + triangle[i + 1][j])
        dfs(i + 1, j + 1, curr_sum + triangle[i + 1][j + 1])

    dfs(0, 0, triangle[0][0])
    return answer


# ================================================================================
# Ref solution one - Top-down + 수동 memo
# ================================================================================
def solution_ref_one(triangle: list[list[int]]) -> int:
    """
    재귀 Top-down DP로 메모이제이션을 수동 관리하는 풀이

    dp(i,j) 의미:
        triangle[i][j]에서 출발해 바닥까지의 최댓값

    메모이제이션:
        memo[i][j] != -1이면 이미 계산된 값 → 즉시 반환
        중복 계산 제거로 O(2^N) → O(N²)

    Top-down 특성:
        꼭대기에서 출발, 필요한 부분 문제만 재귀로 요청
        실제 값 확정 순서는 바닥 → 꼭대기 (Bottom-up과 동일)
    """
    n = len(triangle)
    memo = [[-1] * len(row) for row in triangle]

    def dp(i: int, j: int) -> int:
        if i == n - 1:
            return triangle[i][j]
        if memo[i][j] != -1:
            return memo[i][j]
        memo[i][j] = triangle[i][j] + max(dp(i + 1, j), dp(i + 1, j + 1))
        return memo[i][j]

    return dp(0, 0)


# ================================================================================
# Ref solution two - Top-down + @cache
# ================================================================================
def solution_ref_two(triangle: list[list[int]]) -> int:
    """
    @cache 데코레이터로 메모이제이션을 자동 관리하는 풀이

    ref_one과 동일한 로직:
        @cache: functools.lru_cache(maxsize=None)와 동일
                호출 인수를 key로 결과를 dict에 자동 저장

    주의:
        triangle이 리스트라 @cache 내부에서 직접 접근 가능
        triangle 자체는 cache key에 포함되지 않음
    """
    n = len(triangle)

    @cache
    def dp(i: int, j: int) -> int:
        if i == n - 1:
            return triangle[i][j]
        return triangle[i][j] + max(dp(i + 1, j), dp(i + 1, j + 1))

    return dp(0, 0)


# ================================================================================
# Ref solution three - Bottom-up + in-place (Best)
# ================================================================================
def solution_ref_three(triangle: list[list[int]]) -> int:
    """
    바닥부터 위로 순서대로 채우는 Bottom-up DP (triangle 원본 수정)

    Bottom-up 특성:
        바닥행(dp 기저값 = 자기 자신)부터 위로 채움
        위 행을 계산할 때 아래 행의 dp값이 항상 완성된 상태

    in-place 수정:
        triangle[i][j] += max(triangle[i+1][j], triangle[i+1][j+1])
        "이 위치에서 바닥까지의 최댓값"으로 값 업데이트
        추가 공간 없이 O(1) 공간

    실측 ref_one 대비 3배 빠름:
        재귀 함수 호출 오버헤드 없음
        단순 반복문 + 인덱스 접근만 수행
    """
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(len(triangle[i])):
            triangle[i][j] += max(triangle[i + 1][j], triangle[i + 1][j + 1])

    return triangle[0][0]


# ================================================================================
# Best solution - Bottom-up + in-place (ref_three 주석 보강)
# ================================================================================
def solution_best(triangle: list[list[int]]) -> int:
    """
    Bottom-up DP로 O(N²) 시간, O(1) 공간에 최댓값을 구하는 최적 풀이

    ref_three와 동일한 로직, 선정 근거 주석 보강:
        재귀 없이 반복문만 사용 → 함수 호출 오버헤드 없음
        O(1) 공간: triangle 제자리 수정
        실측 N=20: 0.123ms (ref_one 0.409ms 대비 3배 빠름)
        바닥부터 올라오므로 항상 완성된 하위 dp값을 참조
    """
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(len(triangle[i])):
            triangle[i][j] += max(triangle[i + 1][j], triangle[i + 1][j + 1])

    return triangle[0][0]


# ================================================================================
# Sub solution - Top-down + 수동 memo (ref_one 주석 보강)
# ================================================================================
def solution_sub(triangle: list[list[int]]) -> int:
    """
    Top-down 재귀 DP로 점화식과 메모이제이션 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        dp(i,j) 재귀 구조로 점화식이 코드에 직접 드러남
        memo[i][j]: "이 위치는 이미 계산됨"이 가시적
        "위에서 내려가며 필요한 것만 계산" 동작 원리 명확
        재귀 오버헤드로 Best보다 느림
    """
    n = len(triangle)
    memo = [[-1] * len(row) for row in triangle]

    def dp(i: int, j: int) -> int:
        if i == n - 1:
            return triangle[i][j]
        if memo[i][j] != -1:
            return memo[i][j]
        memo[i][j] = triangle[i][j] + max(dp(i + 1, j), dp(i + 1, j + 1))
        return memo[i][j]

    return dp(0, 0)


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""
    import copy

    test_cases: list[tuple[list[list[int]], int]] = [
        # (triangle, 기댓값)
        # 공식 예시 — 손 추적: 7→3→8→7→5=30
        ([[7],[3,8],[8,1,0],[2,7,4,4],[4,5,2,6,5]], 30),
        # 단일 원소
        ([[5]], 5),
        # 2행
        ([[1],[2,3]], 4),
        # 모든 값 동일
        ([[1],[1,1],[1,1,1]], 3),
    ]

    # mine은 소규모에서만 검증
    print("--- Mine (소규모만, 시간 초과 풀이) ---")
    for idx, (triangle, expected) in enumerate(test_cases, 1):
        start = time.perf_counter()
        output = solution_mine(copy.deepcopy(triangle))
        elapsed = time.perf_counter() - start
        status = "PASS" if output == expected else "FAIL"
        print(f"  TC{idx}: {status} ({elapsed*1000:.4f}ms)")

    solutions = [
        ("Ref_one  (Top-down+memo) ", solution_ref_one),
        ("Ref_two  (Top-down+cache)", solution_ref_two),
        ("Ref_three(Bottom-up)     ", solution_ref_three),
        ("Best     (Bottom-up)     ", solution_best),
        ("Sub      (Top-down+memo) ", solution_sub),
    ]

    # 워밍업 스텝
    _t, _ = test_cases[0]
    for _, func in solutions:
        func(copy.deepcopy(_t))

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (triangle, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(copy.deepcopy(triangle))
            elapsed = time.perf_counter() - start
            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
