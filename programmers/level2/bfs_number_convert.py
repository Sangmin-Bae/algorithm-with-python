"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 숫자 변환하기
    유형       : BFS / DP
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/154538
    풀이일자   : 2026-09-04
===================================================================================
[문제 요약]
    x를 y로 변환하는 최소 연산 횟수 반환
    가능한 연산: +n, ×2, ×3
    변환 불가능하면 -1

    제약 조건
        - 1 ≤ x ≤ y ≤ 1,000,000
        - 1 ≤ n < y
===================================================================================
[입출력 예시]
    x  | y  | n  | result
    ---|----|----|-------
    10 | 40 | 5  | 2      (×2 × 2)
    10 | 40 | 30 | 1      (+30)
    2  | 5  | 4  | -1
===================================================================================
[BFS가 최솟값을 보장하는 이유]
    각 연산을 간선 가중치 1인 그래프 탐색으로 모델링
    BFS는 너비 우선 → 처음 y에 도달하는 순간 = 최소 연산 횟수

[정방향 vs 역방향 BFS]
    정방향 (mine):
        x → +n, ×2, ×3 → 다음 후보 (3개 항상 추가)
        x=1, y=100000, n=3: queue에 수많은 숫자 축적

    역방향 (ref_one):
        y → -n 항상, ÷2는 짝수일 때만, ÷3은 3의 배수일 때만
        조건부 후보로 queue 크기 자연히 감소
        실측 x=1,y=100000,n=3: 정방향 22ms → 역방향 0.05ms (440배 차이)

[역방향 아이디어를 캐치하는 신호]
    정방향 연산이 "항상 가능"
    역방향 연산은 "조건부" (나머지가 0일 때만)
    → 역방향이 탐색 공간을 자연스럽게 제한
    → 역방향 BFS가 유리한 신호

[ref_two — Bottom-up DP (상향식 타뷸레이션)]
    dp[i] = "x에서 i까지 도달하는 최소 연산 횟수"
    dp[x] = 0 (출발점)
    x → y 방향으로 순서대로 채움

    점화식:
        dp[i+n] = min(dp[i+n], dp[i]+1)
        dp[i×2] = min(dp[i×2], dp[i]+1)
        dp[i×3] = min(dp[i×3], dp[i]+1)

    "벽돌 쌓기": 작은 dp 값이 완성된 후 큰 dp 값에 업데이트

[ref_three — Top-down DP (하향식 메모이제이션)]
    dp(curr_y) = "curr_y에서 x로 역방향으로 가는 최소 횟수"
               = "x에서 curr_y까지 최소 횟수"
    dp(y) 구하기 위해 dp(y-n), dp(y÷2), dp(y÷3) 재귀 요청

    점화식:
        dp(i) = min(dp(i-n), dp(i÷2), dp(i÷3)) + 1

    "질문하기": 큰 값이 작은 값에게 재귀로 요청
    sys.setrecursionlimit 필요 (y 최대 1,000,000 → 재귀 깊이 위험)

[상향식 vs 하향식 직관적 구분]
    상향식 (Bottom-up):
        x에서 출발해 y 방향으로 올라가며 채움 (정방향)
        반복문 사용

    하향식 (Top-down):
        y에서 출발해 x 방향으로 내려가며 계산 (역방향)
        재귀 + 메모이제이션 사용

[실측 결과 — x=1, y=100,000, n=3, 500회]
    ref_one (역방향BFS): 0.05ms  ← 440배 빠름
    mine    (정방향BFS): 22.25ms
    ref_two (DP 상향식): 43.70ms
    ref_thr (DP 하향식): 메모리 과다로 측정 생략
===================================================================================
[내 초기 풀이]
    solution_mine: 정방향 BFS

[개선 포인트]
    solution_mine:    정방향 BFS O(y-x) - Sub
                      직관적이나 queue 크기가 큰 케이스에서 불리
    solution_ref_one: 역방향 BFS - Best
                      조건부 후보로 queue 크기 대폭 감소
    solution_ref_two: Bottom-up DP
                      O(y-x) 순회, BFS보다 느림
    solution_ref_three: Top-down DP + 메모이제이션
                        setrecursionlimit 필요, 메모리 주의
===================================================================================
[복잡도 분석]
    N = y - x (최대 999,999)

    Mine     - 시간: O(N) 최악 | 공간: O(N) - queue + visited
    Ref_one  - 시간: O(N) 최악 | 공간: O(N) - 역방향, 실제 훨씬 빠름
    Ref_two  - 시간: O(N)      | 공간: O(y) - dp 배열
    Ref_three- 시간: O(N)      | 공간: O(N) - memo dict + 재귀 스택
    Best     - 시간: O(N) 최악 | 공간: O(N) - Ref_one과 동일
    Sub      - 시간: O(N) 최악 | 공간: O(N) - Mine과 동일
"""

import sys
from collections import deque
import time

sys.setrecursionlimit(10000000)


# =================================================================================
# Mine solution - 정방향 BFS
# =================================================================================
def solution_mine(x: int, y: int, n: int) -> int:
    """
    x에서 y 방향으로 BFS로 최소 연산 횟수를 구하는 초기 풀이

    visited 추가 시점:
        큐에 넣을 때 visited.add → "이미 최솟값으로 등록됨" 보장
        꺼낼 때 추가하면 같은 노드가 큐에 중복으로 들어갈 수 있음

    next_num <= y 가지치기:
        y를 초과하는 값은 절대 y에 도달 불가 → 탐색 공간 감소

    한계:
        +n, ×2, ×3 세 가지 항상 후보 → queue 크기 빠르게 증가
        x가 작고 y가 클 때 느림
    """
    if x == y:
        return 0

    queue = deque([(x, 0)])
    visited = set([x])

    while queue:
        curr_num, count = queue.popleft()

        for next_num in [curr_num + n, curr_num * 2, curr_num * 3]:
            if next_num == y:
                return count + 1

            if next_num <= y and next_num not in visited:
                visited.add(next_num)
                queue.append((next_num, count + 1))

    return -1


# =================================================================================
# Ref solution one - 역방향 BFS
# =================================================================================
def solution_ref_one(x: int, y: int, n: int) -> int:
    """
    y에서 x 방향으로 역방향 BFS로 최소 연산 횟수를 구하는 최적 풀이

    역방향 연산:
        -n: 항상 가능
        ÷2: curr_num % 2 == 0일 때만 (정방향 ×2의 역)
        ÷3: curr_num % 3 == 0일 때만 (정방향 ×3의 역)

    역방향이 빠른 이유:
        조건부 후보 → queue에 추가되는 숫자 수 자연히 감소
        대부분의 수에서 후보가 1~2개
        실측 y=100,000에서 정방향 대비 440배 빠름

    역방향 아이디어 캐치 신호:
        정방향: 항상 3가지 후보
        역방향: 조건부 1~3가지 후보
        → 역방향이 탐색 공간을 제한하는 조건을 만들 때 역방향 우위
    """
    if x == y:
        return 0

    queue = deque([(y, 0)])
    visited = set([y])

    while queue:
        curr_num, count = queue.popleft()

        next_candidates = [curr_num - n]
        if curr_num % 2 == 0:
            next_candidates.append(curr_num // 2)
        if curr_num % 3 == 0:
            next_candidates.append(curr_num // 3)

        for next_num in next_candidates:
            if next_num == x:
                return count + 1

            if next_num >= x and next_num not in visited:
                visited.add(next_num)
                queue.append((next_num, count + 1))

    return -1


# =================================================================================
# Ref solution two - Bottom-up DP (상향식 타뷸레이션)
# =================================================================================
def solution_ref_two(x: int, y: int, n: int) -> int:
    """
    x에서 y 방향으로 dp 배열을 채우는 Bottom-up DP 풀이

    dp[i] = "x에서 i까지 도달하는 최소 연산 횟수"
    dp[x] = 0, 나머지 inf 초기화

    점화식 (push 방식):
        dp[i]가 확정되면 dp[i+n], dp[i×2], dp[i×3]을 업데이트
        min으로 더 작은 값만 반영

    상향식 특성:
        x → y 방향으로 순서대로 채움 (작은 것부터)
        dp[i] = inf이면 도달 불가능 → skip
    """
    if x == y:
        return 0

    dp = [float('inf')] * (y + 1)
    dp[x] = 0

    for i in range(x, y + 1):
        if dp[i] == float('inf'):
            continue

        next_count = dp[i] + 1

        if i + n <= y:
            dp[i + n] = min(dp[i + n], next_count)

        if i * 2 <= y:
            dp[i * 2] = min(dp[i * 2], next_count)

        if i * 3 <= y:
            dp[i * 3] = min(dp[i * 3], next_count)

    return dp[y] if dp[y] != float('inf') else -1


# =================================================================================
# Ref solution three - Top-down DP (하향식 메모이제이션)
# =================================================================================
def solution_ref_three(x: int, y: int, n: int) -> int:
    """
    y에서 x 방향으로 재귀하며 메모이제이션으로 최소 횟수를 구하는 Top-down DP

    dp(curr_y) = "curr_y에서 x로 역방향으로 가는 최소 횟수"
               = "x에서 curr_y까지 최소 횟수"

    점화식 (pull 방식):
        dp(i) = min(dp(i-n), dp(i÷2), dp(i÷3)) + 1

    하향식 특성:
        dp(y)를 구하기 위해 dp(y-n), dp(y÷2), dp(y÷3) 재귀 요청
        y → x 방향으로 내려감 (큰 것이 작은 것에게 요청)
        memo로 중복 계산 방지

    sys.setrecursionlimit 필요:
        y 최대 1,000,000 → 재귀 깊이가 y-x에 비례
    """
    if x == y:
        return 0

    memo = {}

    def dp(curr_y: int) -> float:
        if curr_y == x:
            return 0
        if curr_y < x:
            return float('inf')
        if curr_y in memo:
            return memo[curr_y]

        res = dp(curr_y - n) + 1

        if curr_y % 2 == 0:
            res = min(res, dp(curr_y // 2) + 1)

        if curr_y % 3 == 0:
            res = min(res, dp(curr_y // 3) + 1)

        memo[curr_y] = res
        return res

    answer = dp(y)
    return answer if answer != float('inf') else -1


# =================================================================================
# Best solution - 역방향 BFS (ref_one 주석 보강)
# =================================================================================
def solution_best(x: int, y: int, n: int) -> int:
    """
    역방향 BFS로 조건부 후보 탐색으로 가장 빠르게 최소 횟수를 구하는 최적 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        역방향 조건부 후보 → queue 크기 대폭 감소
        실측 y=100,000: 정방향 22ms → 0.05ms (440배 우위)
        역방향 ÷2, ÷3 조건이 탐색 공간을 자연스럽게 제한
    """
    if x == y:
        return 0

    queue = deque([(y, 0)])
    visited = set([y])

    while queue:
        curr_num, count = queue.popleft()

        next_candidates = [curr_num - n]
        if curr_num % 2 == 0:
            next_candidates.append(curr_num // 2)
        if curr_num % 3 == 0:
            next_candidates.append(curr_num // 3)

        for next_num in next_candidates:
            if next_num == x:
                return count + 1

            if next_num >= x and next_num not in visited:
                visited.add(next_num)
                queue.append((next_num, count + 1))

    return -1


# =================================================================================
# Sub solution - 정방향 BFS (mine 주석 보강)
# =================================================================================
def solution_sub(x: int, y: int, n: int) -> int:
    """
    정방향 BFS로 최소 연산 횟수를 구하는 서브 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        BFS의 직관적 구조 → x에서 y로 가는 과정이 코드에 명확
        visited 큐 삽입 시점 추가 → 최솟값 보장
        next_num <= y 가지치기 → y 초과 탐색 차단
        Best 대비 정방향이라 queue 크기가 더 커질 수 있음
    """
    if x == y:
        return 0

    queue = deque([(x, 0)])
    visited = set([x])

    while queue:
        curr_num, count = queue.popleft()

        for next_num in [curr_num + n, curr_num * 2, curr_num * 3]:
            if next_num == y:
                return count + 1

            if next_num <= y and next_num not in visited:
                visited.add(next_num)
                queue.append((next_num, count + 1))

    return -1


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (x, y, n, 기댓값)
        # 공식 예시
        # 손 추적: 10×2=20×2=40 → 2회
        (10, 40, 5,  2),
        # 손 추적: 10+30=40 → 1회
        (10, 40, 30, 1),
        # 변환 불가
        (2,  5,  4,  -1),
        # 추가 케이스:
        # x == y
        (5,  5,  3,  0),
        # 단일 연산
        (1,  3,  2,  1),
    ]

    solutions = [
        ("Mine    (정방향BFS)  ", solution_mine),
        ("Ref_one (역방향BFS)  ", solution_ref_one),
        ("Ref_two (DP 상향식)  ", solution_ref_two),
        ("Ref_thr (DP 하향식)  ", solution_ref_three),
        ("Best    (역방향BFS)  ", solution_best),
        ("Sub     (정방향BFS)  ", solution_sub),
    ]

    # 워밍업 스텝
    _x, _y, _n, _ = test_cases[0]
    for _, func in solutions:
        func(_x, _y, _n)

    print("=" * 66)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (x, y, n, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(x, y, n)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
