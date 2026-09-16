"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 2 x n 타일링
    유형       : DP (Dynamic Programming)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12900
    풀이일자   : 2026-09-16
===================================================================================
[문제 요약]
    2×n 바닥을 2×1 타일로 채우는 경우의 수를 1,000,000,007로 나눈 나머지 반환
    타일은 가로/세로 배치 가능

    제약 조건
        - n: 1 이상 60,000 이하
===================================================================================
[입출력 예시]
    n | result
    --|-------
    4 | 5
===================================================================================
[왜 DP인가 — DP 캐치 신호]
    n 최대 60,000 → O(N²) 이상 안 됨
    직접 세는 것 불가능 → 점화식 필요
    "경우의 수" → DP의 강한 힌트

    작은 경우 나열:
        n=1: 1가지
        n=2: 2가지
        n=3: 3가지
        n=4: 5가지
        → 1,2,3,5,8,... 피보나치

[점화식 도출 — 가장 오른쪽 열 분석]
    경우 A: 세로 타일 1개 (가로 1칸)
             → 나머지 (n-1)칸 = f(n-1)가지

    경우 B: 가로 타일 2개 위아래 (가로 2칸)
             → 나머지 (n-2)칸 = f(n-2)가지

    두 경우 외에 없음
    → f(n) = f(n-1) + f(n-2)

[내 풀이 — 조합(Combination) 접근]
    k = 가로 방향 타일 묶음 수
    세로 타일: n-2k개, 가로 묶음: k개 → 총 n-k개 중 k를 배치
    → C(n-k, k)의 합

    정확성 통과, 효율성 실패:
        math.comb(n-k, k): 팩토리얼 연산 O(n-k)
        n//2번 반복 → O(N²) 수준 → TLE

[ref_three — 행렬 거듭제곱 O(log N)]
    피보나치의 행렬 표현:
        [f(n+1)]   [1  1] [f(n)  ]
        [f(n)  ] = [1  0] [f(n-1)]

    반복 적용:
        [f(n)  ] = [1  1]^(n-2) × [f(2)] = base^(n-2) × [2]
        [f(n-1)]   [1  0]          [f(1)]               [1]

    반환값:
        matrix[0][0] × 2 + matrix[0][1] × 1

    행렬 거듭제곱 분할정복:
        A^p = (A^(p/2))²  (p 짝수)
        A^p = A × A^(p-1) (p 홀수)
        → O(log N)

    이 문제에서는 n≤60,000이라 O(N) DP로 충분
    n=10^18 같은 초대형 입력에서 필요한 방식

[실측 결과 — N=200회]
    ref_thr (행렬 O(log N)):  0.03ms  ← 압도적
    mine    (comb, n=1000):   3.84ms
    ref_one (DP 상향식 O(N)):  5.95ms
    ref_two (DP 하향식 O(N)): 30.35ms
===================================================================================
[내 초기 풀이]
    solution_mine: 조합(Combination) (정확성 통과, 효율성 실패)

[개선 포인트]
    solution_mine:    O(N²) → 효율성 실패
                      조합적 사고는 창의적이나 DP가 더 효율적
    solution_ref_one: Bottom-up DP O(N) - Best
                      직관적, 빠름, 공간 O(N)
    solution_ref_two: Top-down DP O(N) - Sub
                      재귀 오버헤드로 상향식보다 느림
    solution_ref_three: 행렬 거듭제곱 O(log N)
                        초대형 입력용, 이 문제는 오버킬
===================================================================================
[복잡도 분석]
    N = n (최대 60,000)

    Mine     - 시간: O(N²) 수준 | 공간: O(1) - comb 반복
    Ref_one  - 시간: O(N)       | 공간: O(N) - dp 배열
    Ref_two  - 시간: O(N)       | 공간: O(N) - memo + 재귀 스택
    Ref_three- 시간: O(log N)   | 공간: O(log N) - 재귀 스택
    Best     - 시간: O(N)       | 공간: O(N) - Ref_one과 동일
    Sub      - 시간: O(N)       | 공간: O(N) - Ref_two와 동일
"""

import math
import sys
import time

sys.setrecursionlimit(10000000)

MOD = 1_000_000_007


# =================================================================================
# Mine solution - 조합(Combination) (효율성 실패)
# =================================================================================
def solution_mine(n: int) -> int:
    """
    가로 타일 묶음 수 k를 기준으로 C(n-k, k)의 합을 구하는 초기 풀이

    아이디어:
        세로 타일: n-2k개, 가로 묶음: k개 → 총 n-k개 중 k를 배치
        C(n-k, k) = k를 어느 순서에 두는지의 경우의 수

    효율성 실패 원인:
        math.comb(n-k, k): 팩토리얼 연산 O(n-k)
        n//2번 반복 → O(N²) 수준 → TLE
    """
    answer = 0
    for k in range((n // 2) + 1):
        answer += math.comb(n - k, k)
    return answer % MOD


# =================================================================================
# Ref solution one - Bottom-up DP
# =================================================================================
def solution_ref_one(n: int) -> int:
    """
    f(n) = f(n-1) + f(n-2) 점화식을 Bottom-up으로 구현하는 풀이

    점화식 도출:
        가장 오른쪽 열 분석
        경우 A: 세로 타일 1개 → f(n-1)
        경우 B: 가로 타일 2개 → f(n-2)
        f(n) = f(n-1) + f(n-2) (피보나치)

    dp[1]=1, dp[2]=2 초기값에서 시작
    3~n까지 순서대로 채움
    """
    if n == 1:
        return 1
    if n == 2:
        return 2

    dp = [-1] * (n + 1)
    dp[1], dp[2] = 1, 2

    for i in range(3, n + 1):
        dp[i] = (dp[i - 1] + dp[i - 2]) % MOD

    return dp[n]


# =================================================================================
# Ref solution two - Top-down DP + 메모이제이션
# =================================================================================
def solution_ref_two(n: int) -> int:
    """
    f(n)에서 f(1), f(2)로 재귀하며 메모이제이션으로 중복 계산 방지하는 풀이

    f(n) = f(n-1) + f(n-2)를 재귀로 표현
    memo[x]로 이미 계산된 결과 재사용

    재귀 오버헤드로 Bottom-up 대비 약 5배 느림
    """
    memo = [-1] * (n + 1)

    def dp(x: int) -> int:
        if x == 1: return 1
        if x == 2: return 2
        if memo[x] != -1: return memo[x]
        memo[x] = (dp(x - 1) + dp(x - 2)) % MOD
        return memo[x]

    return dp(n)


# =================================================================================
# Ref solution three - 행렬 거듭제곱 O(log N)
# =================================================================================
def solution_ref_three(n: int) -> int:
    """
    피보나치를 행렬로 표현하고 분할정복 거듭제곱으로 O(log N)에 구하는 풀이

    행렬 표현:
        [f(n+1)]   [1  1]   [f(n)  ]
        [f(n)  ] = [1  0] × [f(n-1)]

    반복 적용:
        [f(n)] = base^(n-2) × [2, 1]의 첫 번째 원소

    분할정복:
        A^p = (A^(p/2))²  (p 짝수) → O(log N)
        A^p = A × A^(p-1) (p 홀수)

    이 문제에서는 n≤60,000이라 O(N) DP로 충분
    n=10^18 초대형 입력에서 O(log N)이 필수
    """
    if n == 1: return 1
    if n == 2: return 2

    def multiply_matrix(A: list, B: list) -> list:
        C = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                total = 0
                for k in range(2):
                    total += A[i][k] * B[k][j]
                C[i][j] = total % MOD
        return C

    def power_matrix(A: list, p: int) -> list:
        if p == 1: return A
        if p % 2 == 0:
            half = power_matrix(A, p // 2)
            return multiply_matrix(half, half)
        else:
            return multiply_matrix(A, power_matrix(A, p - 1))

    base = [[1, 1], [1, 0]]
    matrix = power_matrix(base, n - 2)
    return (matrix[0][0] * 2 + matrix[0][1] * 1) % MOD


# =================================================================================
# Best solution - Bottom-up DP (ref_one 주석 보강)
# =================================================================================
def solution_best(n: int) -> int:
    """
    f(n) = f(n-1) + f(n-2) Bottom-up으로 O(N) 시간에 구하는 최적 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        피보나치 점화식을 반복문으로 구현
        재귀 오버헤드 없음 → Top-down 대비 5배 빠름
        실측 n=60,000: 5.95ms (행렬 0.03ms는 오버킬)
        n≤60,000에서 가장 실용적
    """
    if n == 1:
        return 1
    if n == 2:
        return 2

    dp = [-1] * (n + 1)
    dp[1], dp[2] = 1, 2

    for i in range(3, n + 1):
        dp[i] = (dp[i - 1] + dp[i - 2]) % MOD

    return dp[n]


# =================================================================================
# Sub solution - Top-down DP (ref_two 주석 보강)
# =================================================================================
def solution_sub(n: int) -> int:
    """
    재귀 + 메모이제이션으로 f(n)을 구하는 서브 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        f(n) = f(n-1) + f(n-2) 재귀 구조가 점화식과 1:1 대응
        DP 원리 이해에 유용
        재귀 오버헤드로 Best 대비 5배 느림
    """
    memo = [-1] * (n + 1)

    def dp(x: int) -> int:
        if x == 1: return 1
        if x == 2: return 2
        if memo[x] != -1: return memo[x]
        memo[x] = (dp(x - 1) + dp(x - 2)) % MOD
        return memo[x]

    return dp(n)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int]] = [
        # (n, 기댓값)
        # 공식 예시
        # 손 추적: f(4) = f(3)+f(2) = 3+2 = 5
        (4,     5),
        (1,     1),
        (2,     2),
        # 손 추적: f(5) = f(4)+f(3) = 5+3 = 8
        (5,     8),
        # 큰 입력 (mine은 소규모로 검증)
        (1000,  None),
    ]

    # mine은 효율성 실패 풀이라 큰 입력에서 생략
    print("--- Mine (조합, 소규모 검증) ---")
    for n, exp in test_cases[:4]:
        output = solution_mine(n)
        if exp:
            status = "PASS" if output == exp else "FAIL"
            print(f"  n={n}: {output} {status}")

    solutions = [
        ("Ref_one  (DP 상향식)  ", solution_ref_one),
        ("Ref_two  (DP 하향식)  ", solution_ref_two),
        ("Ref_thr  (행렬 O(logN))", solution_ref_three),
        ("Best     (DP 상향식)  ", solution_best),
        ("Sub      (DP 하향식)  ", solution_sub),
    ]

    # n=1000 기준값 설정
    base = solution_best(1000)
    test_cases[-1] = (1000, base)

    # 워밍업
    for _, func in solutions:
        func(4)

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (n, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
