"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 소수 찾기
    유형       : Brute Force / DFS
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42839
    풀이일자   : 2026-09-23
===================================================================================
[문제 요약]
    한 자리 숫자가 적힌 문자열에서 숫자를 조합해 만들 수 있는
    소수의 개수 반환 (중복 숫자 포함, 순열 방식)

    제약 조건
        - numbers 길이: 1 이상 7 이하
        - 원소: 0~9 한 자리 숫자
        - "011"은 0, 1, 1 세 장의 종이 의미
===================================================================================
[입출력 예시]
    numbers | return
    --------|-------
    "17"    | 3      ([1, 7]로 7, 17, 71 생성)
    "011"   | 2      ([0, 1, 1]로 11, 101 생성)
===================================================================================
[핵심 — 순열 + 소수 판별]
    순열: 길이 1~len(numbers)의 모든 순열 생성
    중복 제거: int 변환 후 set으로 동일 숫자 skip
        "011"에서 "11"(0,1 중 1)과 "11"(1,0 중 1) 모두 11로 변환
    소수 판별: is_prime (√N까지 홀수만 순회)

[최대 경우의 수]
    numbers 길이 7: 7! = 5,040개
    완전탐색 가능

[풀이 비교]
    풀이1 (permutations):
        itertools.permutations: C 레벨 구현
        set으로 중복 제거 후 is_prime 확인
        가장 빠름

    풀이2 (dfs_perm):
        순열을 직접 DFS로 구현 (연습용)
        set 중복 제거 후 is_prime 일괄 확인
        Pure Python 재귀로 가장 느림

    풀이3 (통합 DFS):
        순열 생성 + 중복 제거 + 소수 판별을 단일 DFS에서 처리
        백트래킹으로 visited 배열 활용
        arr를 리스트로 유지 (불변 문자열 대비 append/pop O(1))

[리스트 vs 문자열 백트래킹]
    문자열: arr = arr + char 마다 새 객체 생성 O(len) × 호출 수
    리스트: append/pop O(1), 객체 재사용
    → 리스트 방식이 더 효율적

[실측 결과 — numbers=7자리, 2,000회]
    one (permutations): 36.30ms  ← 가장 빠름
    three (통합 dfs):   41.57ms
    two (dfs_perm):     측정 시간 초과 (순수 Python DFS 중복 구현으로 가장 느림)
===================================================================================
[내 초기 풀이]
    solution_mine_one:   permutations + is_prime
    solution_mine_two:   dfs_perm 직접 구현 (연습용)
    solution_mine_three: 통합 DFS (순열+소수 동시)

[개선 포인트]
    solution_mine_one:   개선 필요 없음 - Best
                         C 레벨 permutations으로 가장 빠름
    solution_mine_two:   연습용 구현, 느림
    solution_mine_three: 통합 DFS - Sub
                         백트래킹 구조 명시적
===================================================================================
[복잡도 분석]
    N = len(numbers) (최대 7)
    P = 총 순열 수 = 1! + 2! + ... + N! (최대 5,040)
    M = 최대 수 (최대 N자리 수)

    Mine_one   - 시간: O(P × √M) | 공간: O(P) - set
    Mine_two   - 시간: O(P × √M) | 공간: O(P) - set
    Mine_three - 시간: O(P × √M) | 공간: O(P) - set + visited
    Best       - 시간: O(P × √M) | 공간: O(P) - Mine_one과 동일
    Sub        - 시간: O(P × √M) | 공간: O(P) - Mine_three와 동일

    N ≤ 7 → P ≤ 5,040 → 사실상 O(1)
"""

import math
from itertools import permutations
import time


def _is_prime(x: int) -> bool:
    """소수 판별: 1 예외, 2 특수, 짝수 제외, 3~√x 홀수 순회"""
    if x <= 1: return False
    if x == 2: return True
    if x % 2 == 0: return False
    for i in range(3, math.isqrt(x) + 1, 2):
        if x % i == 0: return False
    return True


# =================================================================================
# Mine solution one - permutations + is_prime
# =================================================================================
def solution_mine_one(numbers: str) -> int:
    """
    itertools.permutations으로 모든 순열을 생성하고 소수를 찾는 초기 풀이

    2중 for문:
        r=1~len(numbers)까지 모든 길이의 순열 생성
        permutations(numbers, r)로 길이 r 순열

    중복 제거:
        int 변환 후 set으로 동일 수 skip
        is_prime 전에 중복 체크로 소수 판별 횟수 절감

    C 레벨 permutations으로 Pure Python DFS보다 빠름
    """
    s = set()
    answer = 0

    for i in range(1, len(numbers) + 1):
        for nums in permutations(numbers, i):
            num = int(''.join(nums))
            if num not in s and _is_prime(num):
                answer += 1
                s.add(num)

    return answer


# =================================================================================
# Mine solution two - DFS 순열 직접 구현 (연습용)
# =================================================================================
def solution_mine_two(numbers: str) -> int:
    """
    DFS 백트래킹으로 순열을 직접 구현하는 연습용 풀이

    dfs_perm(arr, c):
        visited 배열로 사용 여부 추적
        len(path)==c에서 결과 수집

    두 단계 분리:
        1단계: 모든 순열 생성 → set에 수집
        2단계: set의 수에 대해 is_prime 일괄 확인

    Pure Python DFS라 permutations 대비 느림
    """
    def dfs_perm(arr: list | str, c: int) -> list[tuple]:
        result = []
        visited = [False] * len(arr)

        def dfs(path: list) -> None:
            if len(path) == c:
                result.append(tuple(path))
                return
            for i in range(len(arr)):
                if not visited[i]:
                    path.append(arr[i])
                    visited[i] = True
                    dfs(path)
                    path.pop()
                    visited[i] = False

        dfs([])
        return result

    s = set()
    for i in range(1, len(numbers) + 1):
        for nums in dfs_perm(numbers, i):
            s.add(int(''.join(nums)))

    return sum(1 for n in s if _is_prime(n))


# =================================================================================
# Mine solution three - 통합 DFS (순열 + 소수 동시)
# =================================================================================
def solution_mine_three(numbers: str) -> int:
    """
    순열 생성과 소수 판별을 단일 DFS 탐색으로 통합한 풀이

    백트래킹:
        arr: 현재까지 선택된 숫자 (리스트)
        visited: 각 자리 사용 여부

    arr에 원소가 있으면 바로 소수 판별:
        r=1~N 외부 루프 없이 DFS 깊이가 자연스럽게 길이를 증가

    리스트 선택 이유:
        불변 문자열: arr+char마다 새 객체 생성 O(len)
        가변 리스트: append/pop O(1) → 백트래킹에 효율적

    중복 처리:
        int 변환 후 set에 없으면 is_prime 확인
        이미 있는 수는 소수 판별 없이 skip
    """
    visited = [False] * len(numbers)
    s = set()
    answer = 0

    def dfs(arr: list) -> None:
        nonlocal answer

        if arr:
            num = int(''.join(arr))
            if num not in s:
                s.add(num)
                if _is_prime(num):
                    answer += 1

        for i in range(len(numbers)):
            if not visited[i]:
                arr.append(numbers[i])
                visited[i] = True
                dfs(arr)
                arr.pop()
                visited[i] = False

    dfs([])
    return answer


# =================================================================================
# Best solution - permutations + is_prime (mine_one 주석 보강)
# =================================================================================
def solution_best(numbers: str) -> int:
    """
    C 레벨 permutations으로 가장 빠르게 소수 개수를 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        permutations: C 레벨 구현 → Pure Python DFS보다 빠름
        중복 체크 우선 → is_prime 호출 횟수 절감
        실측 7자리: 36.30ms (통합 DFS 41.57ms 대비 우위)
    """
    s = set()
    answer = 0

    for i in range(1, len(numbers) + 1):
        for nums in permutations(numbers, i):
            num = int(''.join(nums))
            if num not in s and _is_prime(num):
                answer += 1
                s.add(num)

    return answer


# =================================================================================
# Sub solution - 통합 DFS (mine_three 주석 보강)
# =================================================================================
def solution_sub(numbers: str) -> int:
    """
    백트래킹 DFS로 순열 생성과 소수 판별을 통합한 서브 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        단일 DFS로 순열 생성 + 중복 제거 + 소수 판별 통합
        백트래킹 구조(visited + append/pop)가 코드에 직관적으로 드러남
        리스트 arr: 불변 문자열 대비 O(1) append/pop
        Best 대비 Pure Python 재귀 오버헤드로 14% 느림
    """
    visited = [False] * len(numbers)
    s = set()
    answer = 0

    def dfs(arr: list) -> None:
        nonlocal answer

        if arr:
            num = int(''.join(arr))
            if num not in s:
                s.add(num)
                if _is_prime(num):
                    answer += 1

        for i in range(len(numbers)):
            if not visited[i]:
                arr.append(numbers[i])
                visited[i] = True
                dfs(arr)
                arr.pop()
                visited[i] = False

    dfs([])
    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int]] = [
        # (numbers, 기댓값)
        # 공식 예시
        ("17",  3),   # 7, 17, 71
        ("011", 2),   # 11, 101
        # 추가 케이스:
        # 단일 숫자
        ("7",   1),   # 7만 소수
        ("0",   0),   # 0은 소수 아님
        # 모두 동일
        # 손 추적: "11" → {1(비소수), 11(소수)} → 1개
        ("11",  1),
    ]

    solutions = [
        ("Mine_one   (permutations)", solution_mine_one),
        ("Mine_two   (dfs_perm)    ", solution_mine_two),
        ("Mine_three (통합 dfs)    ", solution_mine_three),
        ("Best       (permutations)", solution_best),
        ("Sub        (통합 dfs)    ", solution_sub),
    ]

    # 워밍업
    _n, _ = test_cases[0]
    for _, func in solutions:
        func(_n)

    print("=" * 66)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (numbers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(numbers)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
