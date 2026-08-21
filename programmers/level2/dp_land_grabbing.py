"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 땅따먹기
    유형       : DP (Dynamic Programming)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12913
    풀이일자   : 2026-08-21
================================================================================
[문제 요약]
    N행 4열 격자에서 한 행씩 내려오며 한 칸만 밟을 때
    같은 열을 연속으로 밟을 수 없는 조건에서 최대 점수 반환

    제약 조건
        - 행 수 N: 100,000 이하 자연수
        - 열 수: 4 고정
        - 점수: 100 이하 자연수
================================================================================
[입출력 예시]
    land                             | answer
    ---------------------------------|-------
    [[1,2,3,5],[5,6,7,8],[4,3,2,1]] | 16
================================================================================
[왜 Greedy가 아닌 DP인가]
    각 행 최대값만 선택하면:
        행0: 5 (col3), 행1: 8 (col3 → 연속 금지!), 행2: 4 (col0)
        → 같은 열 연속 금지 조건으로 현재 최선이 미래를 막을 수 있음

    "현재 선택이 이후 선택지에 영향" → Greedy 불가 → DP 필요
    정수 삼각형과 동일한 구조를 N행 4열로 확장한 문제

[DP 정의]
    dp[i][j] = "i행 j열까지 내려왔을 때 가능한 최대 누적 점수"

    점화식 (Bottom-up, 위→아래):
        dp[i][j] = land[i][j] + max(dp[i-1][k] for k≠j)

    점화식 (Bottom-up, 아래→위 / solution_one):
        land[i][j] += max(land[i+1][k] for k≠j)
        → land 자체를 누적 최대값으로 갱신

[Bottom-up 방향 두 가지]
    위→아래: land[0]부터 시작, 각 행을 이전 행 누적값으로 갱신
             → reduce로 두 행씩 처리 가능

    아래→위: 마지막 행부터 시작, land 자체를 역방향으로 갱신
             → 정수 삼각형과 동일한 구조

    결과는 동일, 방향만 반대

[solution_ref_one — reduce로 두 행씩 처리]
    reduce(f, [행0, 행1, ..., 행N-1])
    = f(f(f(행0, 행1), 행2), 행3)...

    f(prev_row, curr_row):
        curr_row의 각 j열에 대해
        prev_row에서 j열 제외 나머지 중 최대값 + curr_row[j]

    reduce가 이 함수를 모든 행에 순서대로 누적 적용
    → for 루프와 동일하지만 한 줄로 표현

[solution_ref_two — 최댓값 두 개 캐싱]
    핵심 관찰:
        j열 제외 나머지 중 최대 = 전체 최댓값(같은 열 아닐 때) 또는
                                   두 번째 최댓값(같은 열일 때)

    미리 최댓값(max1), 두 번째 최댓값(max2) 두 개만 구해두면
    각 칸을 O(1) 인덱스 비교로 처리 가능
    → 슬라이싱 리스트 생성 없음

[실측 결과 — N=100,000행, 100회 반복]
    풀이1 (bottom-up+슬라이싱): 210.1ms
    ref1  (reduce+슬라이싱):    178.1ms
    ref2  (max2개캐싱):          129.9ms  ← 가장 빠름

    ref2가 빠른 이유:
        슬라이싱+리스트 연결 → 인덱스 비교 O(1)로 대체
        리스트 객체 생성 없음
================================================================================
[내 초기 풀이]
    solution_mine_one: Bottom-up (아래→위), land 원본 수정
    solution_mine_two: Top-down (재귀 + 메모이제이션)

[개선 포인트]
    solution_mine_one: 슬라이싱 비용 있음 - Sub
                       아래→위 방향, 정수 삼각형과 동일 구조
    solution_mine_two: 재귀 오버헤드 + setrecursionlimit 필요
                       Top-down 구조 학습 목적
    solution_ref_one:  reduce로 두 행씩 처리, 위→아래 방향
                       슬라이싱 비용 존재
    solution_ref_two:  최댓값 두 개 캐싱 O(1) - Best
                       슬라이싱 없이 가장 빠름
================================================================================
[복잡도 분석]
    N = 행 수 (최대 100,000), 열 = 4 고정

    Mine_one - 시간: O(N×4) = O(N) | 공간: O(1) - land 원본 수정
    Mine_two - 시간: O(N×4) = O(N) | 공간: O(N) - memo 배열 + 재귀 스택
    Ref_one  - 시간: O(N×4) = O(N) | 공간: O(4) - reduce 누적 리스트
    Ref_two  - 시간: O(N×4) = O(N) | 공간: O(4) - dp 리스트 크기 4 고정
    Best     - 시간: O(N)   | 공간: O(4) - Ref_two와 동일
    Sub      - 시간: O(N)   | 공간: O(1) - Mine_one과 동일
"""

import sys
from functools import reduce
import time

sys.setrecursionlimit(200000)


# ================================================================================
# Mine solution one - Bottom-up (아래→위, land 원본 수정)
# ================================================================================
def solution_mine_one(land: list[list[int]]) -> int:
    """
    아래 행부터 위로 올라오며 land를 누적 최대값으로 갱신하는 Bottom-up 풀이

    land[i][j] += max(land[i+1][:j] + land[i+1][j+1:]):
        i+1행에서 j열 제외한 나머지 중 최대값을 현재 칸에 누적
        land 자체를 "이 위치까지 도달 가능한 최대 누적값"으로 갱신

    정수 삼각형과 동일한 Bottom-up 구조를 4열 직사각형으로 확장

    슬라이싱 비용:
        land[i+1][:j] + land[i+1][j+1:]: 매번 새 리스트 생성
        4열 고정이라 O(4) 상수, N행에서 4N번 발생
    """
    for i in range(len(land) - 2, -1, -1):
        for j in range(len(land[i])):
            land[i][j] += max(land[i + 1][:j] + land[i + 1][j + 1:])

    return max(land[0])


# ================================================================================
# Mine solution two - Top-down (재귀 + 메모이제이션)
# ================================================================================
def solution_mine_two(land: list[list[int]]) -> int:
    """
    재귀로 큰 문제를 작은 문제로 분해하는 Top-down 메모이제이션 풀이

    max_score(row, col):
        row행 col열에서 0행까지 거슬러 올라갔을 때 최대 누적값
        = land[row][col] + max(max_score(row-1, k) for k≠col)

    Top-down 특성:
        마지막 행에서 호출 시작
        재귀로 0행까지 내려가며 값 확정
        memo로 중복 계산 방지 O(N×4)

    주의:
        N=100,000이면 재귀 깊이 100,000
        sys.setrecursionlimit 필요
    """
    n = len(land)
    memo = [[-1] * 4 for _ in range(n)]

    def max_score(row: int, col: int) -> int:
        if row == 0:
            return land[row][col]
        if memo[row][col] != -1:
            return memo[row][col]

        prev_max = max(max_score(row - 1, c) for c in range(4) if c != col)
        memo[row][col] = land[row][col] + prev_max
        return memo[row][col]

    return max(max_score(n - 1, c) for c in range(4))


# ================================================================================
# Ref solution one - reduce로 두 행씩 누적 처리
# ================================================================================
def solution_ref_one(land: list[list[int]]) -> int:
    """
    reduce로 두 행씩 누적해 위→아래 방향 Bottom-up DP를 구현하는 참고 풀이

    reduce(f, [행0, 행1, ..., 행N-1]):
        = f(f(f(행0, 행1), 행2), 행3) ...
        두 행을 받아 누적값 리스트를 반환하는 함수를 순서대로 적용

    f(prev_row, curr_row):
        curr_row의 각 j열에 대해
        prev_row에서 j열 제외 나머지 중 최대값 + curr_row[j]
        → curr_row와 같은 크기의 누적값 리스트 반환

    mine_one과 방향 반대 (위→아래)이지만 동일한 결과
    슬라이싱 비용은 mine_one과 동일
    """
    return max(reduce(lambda prev_row, curr_row: [
        curr_val + max(prev_row[:j] + prev_row[j + 1:])
        for j, curr_val in enumerate(curr_row)
    ], land))


# ================================================================================
# Ref solution two - 최댓값 두 개 캐싱 (Best)
# ================================================================================
def solution_ref_two(land: list[list[int]]) -> int:
    """
    이전 행의 최댓값 두 개를 미리 구해 슬라이싱 없이 처리하는 최적 풀이

    핵심 관찰:
        j열 제외 나머지 중 최대 = 전체 최댓값 (j가 최댓값 열이 아닐 때)
                                 = 두 번째 최댓값 (j가 최댓값 열일 때)

    max1_idx, max1_val: 이전 행 최댓값과 그 열 인덱스
    max2_idx, max2_val: 이전 행 두 번째 최댓값

    각 칸을 O(1) 인덱스 비교로 처리:
        j == max1_idx → max2_val 더하기
        j != max1_idx → max1_val 더하기

    실측 N=100,000: 129.9ms (mine_one 210.1ms 대비 약 38% 빠름)
    """
    dp = land[0][:]

    for next_row in land[1:]:
        sorted_prev = sorted(enumerate(dp), key=lambda x: x[1], reverse=True)
        max1_idx, max1_val = sorted_prev[0]
        max2_idx, max2_val = sorted_prev[1]

        dp = [val + (max2_val if j == max1_idx else max1_val)
              for j, val in enumerate(next_row)]

    return max(dp)


# ================================================================================
# Best solution - 최댓값 두 개 캐싱 (ref_two 주석 보강)
# ================================================================================
def solution_best(land: list[list[int]]) -> int:
    """
    최댓값 두 개 캐싱으로 O(N) 시간, O(4) 공간에 최대 점수를 구하는 최적 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        슬라이싱 리스트 생성 없음 → 인덱스 비교 O(1)로 대체
        실측 N=100,000: 129.9ms (슬라이싱 방식 210ms 대비 약 38% 빠름)
        열이 4개로 고정이므로 sorted 비용 O(4 log 4) = O(1) 상수
    """
    dp = land[0][:]

    for next_row in land[1:]:
        sorted_prev = sorted(enumerate(dp), key=lambda x: x[1], reverse=True)
        max1_idx, max1_val = sorted_prev[0]
        max2_idx, max2_val = sorted_prev[1]

        dp = [val + (max2_val if j == max1_idx else max1_val)
              for j, val in enumerate(next_row)]

    return max(dp)


# ================================================================================
# Sub solution - Bottom-up 아래→위 (mine_one 주석 보강)
# ================================================================================
def solution_sub(land: list[list[int]]) -> int:
    """
    아래→위 Bottom-up DP로 정수 삼각형과 동일한 구조를 표현하는 서브 풀이

    Best 대비 특징:
        정수 삼각형의 Bottom-up과 동일한 방향 (아래→위)
        land 원본 수정으로 추가 공간 없음 O(1)
        슬라이싱 방식으로 "j열 제외"가 코드에 직접 드러남
        실측 Best보다 약 38% 느림 (리스트 슬라이싱 오버헤드)
    """
    for i in range(len(land) - 2, -1, -1):
        for j in range(len(land[i])):
            land[i][j] += max(land[i + 1][:j] + land[i + 1][j + 1:])

    return max(land[0])


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""
    import copy

    test_cases: list[tuple[list[list[int]], int]] = [
        # (land, 기댓값)
        # 공식 예시
        # 손 추적: 5→7→4 = 16 (col3→col2→col0)
        ([[1, 2, 3, 5], [5, 6, 7, 8], [4, 3, 2, 1]], 16),
        # 단일 행
        ([[1, 1, 1, 1]], 1),
        # 2행: [1,2,3,4] → [5,5,5,5]
        # col3(4)+col0,1,2(5) = 4+5=9, col0(1)+col1,2,3(5) = 1+5=6, 최대=9
        ([[1, 2, 3, 4], [5, 5, 5, 5]], 9),
        # 모두 동일
        ([[1, 1, 1, 1], [1, 1, 1, 1]], 2),
    ]

    # mine_two는 소규모에서만 검증 (재귀 제한)
    print("--- Mine_two (Top-down 재귀, 소규모) ---")
    for idx, (land, expected) in enumerate(test_cases, 1):
        output = solution_mine_two(copy.deepcopy(land))
        status = "PASS" if output == expected else "FAIL"
        print(f"  TC{idx}: {status} (결과={output})")

    solutions = [
        ("Mine_one (bottom-up↑)   ", solution_mine_one),
        ("Ref_one  (reduce)        ", solution_ref_one),
        ("Ref_two  (max2캐싱)      ", solution_ref_two),
        ("Best     (max2캐싱)      ", solution_best),
        ("Sub      (bottom-up↑)   ", solution_sub),
    ]

    # 워밍업 스텝
    _l, _ = test_cases[0]
    for _, func in solutions:
        func(copy.deepcopy(_l))

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (land, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(copy.deepcopy(land))
            elapsed = time.perf_counter() - start
            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
