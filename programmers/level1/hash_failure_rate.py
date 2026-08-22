"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 실패율
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42889
    풀이일자   : 2026-08-22
===================================================================================
[문제 요약]
    stages 배열(각 플레이어가 멈춘 스테이지)과 전체 스테이지 수 N이 주어질 때
    실패율 내림차순으로 정렬한 스테이지 번호 배열 반환
    실패율 = 클리어 못한 플레이어 수 / 도달한 플레이어 수
    실패율 같으면 스테이지 번호 오름차순

    제약 조건
        - N: 1 이상 500 이하
        - stages 길이: 1 이상 200,000 이하
        - stages 원소: 1 이상 N+1 이하 (N+1 = 마지막 스테이지 클리어)
===================================================================================
[입출력 예시]
    N | stages                    | result
    --|---------------------------|----------
    5 | [2,1,2,6,2,4,3,3]         | [3,4,2,1,5]
    4 | [4,4,4,4,4]               | [4,1,2,3]
===================================================================================
[핵심 — player 누적 차감]
    스테이지 n에 도달한 플레이어 수:
        전체 플레이어 수 - (스테이지 1~n-1에 머문 플레이어 수)

    구현:
        player = 전체 플레이어 수로 초기화
        n=1부터 N까지 순회:
            count[n] = n에 머문 플레이어 수
            실패율 = count[n] / player
            player -= count[n]  ← 누적 차감

    player == 0 예외처리:
        모든 플레이어가 이전 스테이지에 머물면 분모 0 발생
        → 실패율 0으로 처리

[안정 정렬(Stable Sort) 덕에 실패율 같으면 번호 오름차순 자동 보장]
    rate를 스테이지 1→N 순서로 추가
    Python sort는 안정 정렬 → 실패율 같으면 먼저 추가된 것(작은 번호)이 앞

[ref_two의 -stage 정렬 트릭]
    (실패율, -stage) 튜플로 저장 후 reverse=True 정렬
    실패율 내림차순: reverse=True
    실패율 같을 때 -stage 내림차순 = stage 오름차순
    → 별도 key 없이 한 번의 sorted로 두 조건 동시 처리

[실측 결과 — N=500, stages=200,000, 1,000회]
    풀이2 (Counter):  11.81ms  ← 가장 빠름
    풀이1 (dict):     16.03ms
    ref2  (bisect):   29.05ms
    ref1  (포인터):   41.75ms  ← 가장 느림

    ref1이 느린 이유:
        "dict 없이 메모리 절약" 의도였으나
        stages.sort() O(M log M)이 dict 구성 O(M)보다 비쌈

    ref2가 ref1보다 빠른 이유:
        bisect O(log M)이 while 포인터 O(M)보다 빠름
        단 정렬 비용은 동일
===================================================================================
[내 초기 풀이]
    solution_mine_one: 직접 dict + 누적 차감
    solution_mine_two: Counter + 누적 차감

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Sub
                       직접 dict로 hash 집계, 동작 원리 명시적
    solution_mine_two: 개선 필요 없음 - Best
                       Counter로 간결하게 집계, 실측 가장 빠름
    solution_ref_one:  정렬+포인터, 추가 자료구조 없음
                       단 sort() 비용으로 실측 가장 느림
    solution_ref_two:  bisect 이진탐색, -stage 정렬 트릭
                       정렬 비용 동일, bisect 활용법 참고용
===================================================================================
[복잡도 분석]
    N = 스테이지 수 (최대 500), M = len(stages) (최대 200,000)

    Mine_one - 시간: O(M+N) | 공간: O(N) - dict 집계 O(M) + N 순회
    Mine_two - 시간: O(M+N) | 공간: O(N) - Counter 집계 O(M) + N 순회
    Ref_one  - 시간: O(M log M + N) | 공간: O(N) - sort + 포인터
    Ref_two  - 시간: O(M log M + N log M) | 공간: O(N) - sort + bisect N회
    Best     - 시간: O(M+N) | 공간: O(N) - Mine_two와 동일
    Sub      - 시간: O(M+N) | 공간: O(N) - Mine_one과 동일
"""

from bisect import bisect_left, bisect_right
from collections import Counter
import time


# =================================================================================
# Mine solution one - 직접 dict + 누적 차감
# =================================================================================
def solution_mine_one(N: int, stages: list[int]) -> list[int]:
    """
    직접 dict로 각 스테이지 플레이어 수를 집계하고 누적 차감으로 실패율을 구하는 풀이

    player 누적 차감:
        전체 플레이어에서 스테이지별 머문 수를 순서대로 빼면
        해당 스테이지에 도달한 플레이어 수가 됨

    안정 정렬 활용:
        rate를 1→N 순서로 추가 → 실패율 같으면 번호 오름차순 자동 보장
    """
    count = {}
    player = len(stages)
    rate = []

    for s in stages:
        count[s] = count.get(s, 0) + 1

    for n in range(1, N + 1):
        if player == 0:
            rate.append((n, 0))
            continue

        c = count.get(n, 0)
        rate.append((n, c / player))
        player -= c

    return [n for n, r in sorted(rate, key=lambda x: x[1], reverse=True)]


# =================================================================================
# Mine solution two - Counter + 누적 차감
# =================================================================================
def solution_mine_two(N: int, stages: list[int]) -> list[int]:
    """
    Counter로 집계 후 누적 차감으로 실패율을 구하는 파이써닉한 풀이

    Counter[n]: 없는 키에 0 반환 (KeyError 없음)
        Counter.__missing__ 메서드가 0을 반환하도록 구현
        count.get(n, 0)과 동일 효과

    rate.sort(key=...) vs sorted(rate, key=...):
        sort(): in-place, 반환값 None
        sorted(): 새 리스트 반환
        이미 리스트인 rate에 sort()가 더 효율적
    """
    count = Counter(stages)
    player = len(stages)
    rate = []

    for n in range(1, N + 1):
        if player == 0:
            rate.append((n, 0))
            continue

        c = count[n]
        rate.append((n, c / player))
        player -= c

    rate.sort(key=lambda x: x[1], reverse=True)

    return [n for n, r in rate]


# =================================================================================
# Ref solution one - 정렬 + while 포인터
# =================================================================================
def solution_ref_one(N: int, stages: list[int]) -> list[int]:
    """
    정렬된 stages를 포인터로 순회해 각 스테이지 플레이어 수를 세는 참고 풀이

    추가 자료구조 없이 포인터만으로 처리:
        stages.sort() → 같은 스테이지 번호가 연속으로 배치
        while 루프로 현재 스테이지 번호를 가진 원소 수를 직접 셈
        idx 포인터가 앞으로 이동하며 O(M) 전체 순회

    실측 가장 느린 이유:
        stages.sort() O(M log M) 비용이
        dict 구성 O(M)보다 비쌈
    """
    stages.sort()
    heads = len(stages)
    failure = []
    idx = 0

    for i in range(1, N + 1):
        if heads == 0:
            failure.append((i, 0))
            continue

        count = 0
        while idx < len(stages) and stages[idx] == i:
            count += 1
            idx += 1

        failure.append((i, count / heads))
        heads -= count

    return [stage for stage, rate in sorted(failure, key=lambda x: x[1], reverse=True)]


# =================================================================================
# Ref solution two - bisect 이진탐색 + -stage 정렬 트릭
# =================================================================================
def solution_ref_two(N: int, stages: list[int]) -> list[int]:
    """
    bisect로 각 스테이지 플레이어 수를 O(log M)에 찾는 참고 풀이

    bisect_left(stages, stage):  stage보다 작은 원소 수 = 이미 넘어간 플레이어
    bisect_right(stages, stage): stage 이하인 원소 수

    도달한 플레이어 수 = total - bisect_left  (앞의 원소들 = 이전 스테이지)
    머문 플레이어 수   = bisect_right - bisect_left

    -stage 정렬 트릭:
        (실패율, -stage) 저장 후 reverse=True 단일 정렬
        실패율 내림차순 + 실패율 같으면 -stage 내림차순 = stage 오름차순
        → 두 정렬 조건을 한 번에 처리
    """
    stages.sort()
    total_players = len(stages)
    failure_rate = []

    for stage in range(1, N + 1):
        left_idx = bisect_left(stages, stage)
        right_idx = bisect_right(stages, stage)

        player = total_players - left_idx
        count = right_idx - left_idx

        if player == 0:
            failure_rate.append((0, -stage))
        else:
            failure_rate.append((count / player, -stage))

    return [-stage for _, stage in sorted(failure_rate, reverse=True)]


# =================================================================================
# Best solution - Counter + 누적 차감 (mine_two 주석 보강)
# =================================================================================
def solution_best(N: int, stages: list[int]) -> list[int]:
    """
    Counter 집계 + 누적 차감으로 O(M+N) 시간에 실패율을 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        정렬 없음 → sort() O(M log M) 비용 없음
        Counter C 레벨 집계 → dict 직접 구성보다 빠름
        실측 N=500, M=200,000: 11.81ms (ref_one 41.75ms 대비 3.5배 우위)
    """
    count = Counter(stages)
    player = len(stages)
    rate = []

    for n in range(1, N + 1):
        if player == 0:
            rate.append((n, 0))
            continue

        c = count[n]
        rate.append((n, c / player))
        player -= c

    rate.sort(key=lambda x: x[1], reverse=True)

    return [n for n, r in rate]


# =================================================================================
# Sub solution - 직접 dict + 누적 차감 (mine_one 주석 보강)
# =================================================================================
def solution_sub(N: int, stages: list[int]) -> list[int]:
    """
    직접 dict로 hash 집계 후 누적 차감으로 처리하는 서브 풀이

    Best 대비 특징:
        Counter 없이 직접 dict 구성 → 동작 원리 명시적
        count.get(n, 0): 없는 스테이지는 0으로 처리
        안정 정렬로 실패율 같은 경우 번호 오름차순 자동 보장
    """
    count = {}
    player = len(stages)
    rate = []

    for s in stages:
        count[s] = count.get(s, 0) + 1

    for n in range(1, N + 1):
        if player == 0:
            rate.append((n, 0))
            continue

        c = count.get(n, 0)
        rate.append((n, c / player))
        player -= c

    return [n for n, r in sorted(rate, key=lambda x: x[1], reverse=True)]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[int], list[int]]] = [
        # (N, stages, 기댓값)
        # 공식 예시
        (5, [2, 1, 2, 6, 2, 4, 3, 3], [3, 4, 2, 1, 5]),
        (4, [4, 4, 4, 4, 4],           [4, 1, 2, 3]),
        # 추가 케이스:
        # 모든 스테이지 실패율 0 (N+1만 존재)
        (3, [4, 4, 4],                  [1, 2, 3]),
        # 단일 플레이어
        (2, [1],                        [1, 2]),
    ]

    solutions = [
        ("Mine_one (dict)     ", solution_mine_one),
        ("Mine_two (Counter)  ", solution_mine_two),
        ("Ref_one  (포인터)   ", solution_ref_one),
        ("Ref_two  (bisect)   ", solution_ref_two),
        ("Best     (Counter)  ", solution_best),
        ("Sub      (dict)     ", solution_sub),
    ]

    # 워밍업 스텝
    _N, _s, _ = test_cases[0]
    for _, func in solutions:
        func(_N, _s[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (N, stages, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(N, stages[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
