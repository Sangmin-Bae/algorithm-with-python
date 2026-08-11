"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 귤 고르기
    유형       : Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/138476
    풀이일자   : 2026-08-11
================================================================================
[문제 요약]
    귤 k개를 고를 때 크기가 서로 다른 종류의 수의 최솟값 반환

    제약 조건
        - 1 <= k <= len(tangerine) <= 100,000
        - 1 <= tangerine 원소 <= 10,000,000
================================================================================
[입출력 예시]
    k | tangerine                  | result
    --|----------------------------|-------
    6 | [1,3,2,5,4,5,2,3]          | 3
    4 | [1,3,2,5,4,5,2,3]          | 2
    2 | [1,1,1,1,2,2,2,3]          | 1
================================================================================
[그리디 핵심 — 개수가 많은 크기부터 선택]
    종류를 최소화하려면 같은 크기가 많은 것부터 담아야 함

    교환 논증:
        최적 해에서 count 작은 크기 A를 선택하고
        count 큰 크기 B를 선택하지 않은 경우,
        A를 B로 교체하면 같은 k를 채우면서 종류가 줄거나 같아짐
        → 많은 것부터 선택이 항상 최적

    k <= 0 조건:
        담는 크기의 개수가 k를 초과해도 됨
        예) k=3, counts=[2,2,1]: 2→1→ k=-1 → 2종류로 3개 이상 충족
        같은 크기를 전부 담지 않아도 됨 → k가 정확히 0이 될 필요 없음

[most_common() vs sorted(values()) 성능 비교]
    실측 (N=100,000 귤, 1,000회 반복):
        풀이1 (직접dict+sorted): 17.756ms
        풀이2 (Counter+sorted):  15.321ms  ← 가장 빠름
        풀이3 (most_common):     34.699ms  ← 가장 느림

    most_common()이 느린 이유:
        (key, value) 쌍 전체를 정렬 → 비교 대상이 튜플
        sorted(values()): 단순 정수만 정렬 → 비교 비용 작음
        언패킹(_, count)으로 key를 버리는 연산도 추가
================================================================================
[내 초기 풀이]
    solution_mine_one  : 직접 dict 구성 + sorted(values())
    solution_mine_two  : Counter + sorted(values())
    solution_mine_three: Counter.most_common()

[개선 포인트]
    solution_mine_one  : Counter로 교체하면 집계 비용 감소 - Sub
                         직접 순회로 동작 원리 명시적
    solution_mine_two  : 개선 필요 없음 - Best
                         Counter C 레벨 집계 + 단순 정수 정렬
    solution_mine_three: most_common()이 sorted(values())보다 느림
                         (key, value) 튜플 정렬 > 정수 정렬
================================================================================
[복잡도 분석]
    N = len(tangerine) (최대 100,000)
    M = 고유 크기 수 (최대 min(N, 10,000,000))

    Mine_one   - 시간: O(N + M log M) | 공간: O(M) - 직접 dict + sorted
    Mine_two   - 시간: O(N + M log M) | 공간: O(M) - Counter(C레벨) + sorted
    Mine_three - 시간: O(N + M log M) | 공간: O(M) - Counter + most_common
    Best       - 시간: O(N + M log M) | 공간: O(M) - Mine_two와 동일
    Sub        - 시간: O(N + M log M) | 공간: O(M) - Mine_one과 동일
"""

from collections import Counter
import time


# ================================================================================
# Mine solution one - 직접 dict 구성 + sorted(values())
# ================================================================================
def solution_mine_one(k: int, tangerine: list[int]) -> int:
    """
    직접 순회해 귤 크기별 개수를 dict에 담고 내림차순 정렬 후 k를 차감하는 풀이

    dict 구성:
        tangerine 순회하며 각 크기의 개수 집계
        Counter 없이 직접 구현 → 동작 원리 명시적

    sorted(counts.values(), reverse=True):
        개수 내림차순 → 많은 크기부터 선택

    k <= 0 조건:
        정확히 k개를 맞출 필요 없음
        k가 음수가 되어도 k개 이상 선택된 것 → 조건 충족
    """
    counts = dict()
    for size in tangerine:
        if size in counts:
            counts[size] += 1
        else:
            counts[size] = 1

    answer = 0
    for count in sorted(counts.values(), reverse=True):
        k -= count
        answer += 1
        if k <= 0:
            break

    return answer


# ================================================================================
# Mine solution two - Counter + sorted(values())
# ================================================================================
def solution_mine_two(k: int, tangerine: list[int]) -> int:
    """
    Counter로 집계 후 values만 정렬해 k를 차감하는 풀이

    Counter(tangerine):
        C 레벨 구현으로 직접 dict 구성보다 빠름
        {크기: 개수} 딕셔너리 반환

    sorted(Counter(tangerine).values(), reverse=True):
        value(개수)만 정렬 → 단순 정수 비교
        most_common()의 튜플 정렬보다 빠름
    """
    answer = 0
    counts = sorted(Counter(tangerine).values(), reverse=True)

    for count in counts:
        k -= count
        answer += 1
        if k <= 0:
            break

    return answer


# ================================================================================
# Mine solution three - Counter.most_common()
# ================================================================================
def solution_mine_three(k: int, tangerine: list[int]) -> int:
    """
    Counter.most_common()으로 정렬된 (크기, 개수) 쌍을 순회하는 풀이

    most_common():
        (key, value) 튜플 쌍을 value 기준 내림차순 정렬 후 반환
        내부적으로 heapq 기반 정렬
        직접 sorted() 불필요하나 튜플 정렬이라 mine_two보다 느림

    _, count 언패킹:
        key(크기)는 이 문제에서 불필요 → _ 로 무시
    """
    answer = 0
    for _, count in Counter(tangerine).most_common():
        k -= count
        answer += 1
        if k <= 0:
            break

    return answer


# ================================================================================
# Best solution - Counter + sorted(values()) (mine_two 주석 보강)
# ================================================================================
def solution_best(k: int, tangerine: list[int]) -> int:
    """
    Counter C 레벨 집계 + 단순 정수 정렬로 최적 처리하는 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        Counter: C 레벨로 직접 dict보다 빠른 집계
        sorted(values()): 단순 정수 정렬 → most_common() 튜플 정렬보다 빠름
        실측 N=100,000: 15.321ms (mine_one 17.756ms, mine_three 34.699ms 대비 우위)
        그리디: 개수 많은 크기부터 선택이 최솟값 종류 보장
    """
    answer = 0
    counts = sorted(Counter(tangerine).values(), reverse=True)

    for count in counts:
        k -= count
        answer += 1
        if k <= 0:
            break

    return answer


# ================================================================================
# Sub solution - 직접 dict 구성 (mine_one 주석 보강)
# ================================================================================
def solution_sub(k: int, tangerine: list[int]) -> int:
    """
    직접 dict로 집계해 그리디 동작 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        Counter 없이 직접 순회로 집계 → 동작 과정 가시적
        sorted(counts.values()): Best와 동일한 단순 정수 정렬
        실측 Best 대비 약 16% 느림 (직접 dict 집계 오버헤드)

    counts.get(size, 0) + 1:
        mine_one의 if/else 분기 → 한 줄로 표현
        key 없으면 기본값 0 반환 후 +1 → 더 간결
    """
    counts = dict()
    for size in tangerine:
        counts[size] = counts.get(size, 0) + 1

    answer = 0
    for count in sorted(counts.values(), reverse=True):
        k -= count
        answer += 1
        if k <= 0:
            break

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[int], int]] = [
        # (k, tangerine, 기댓값)
        # 공식 예시
        # 손 추적:
        # [1,3,2,5,4,5,2,3] → counts={5:2, 3:2, 2:2, 1:1, 4:1}
        # 내림차순: [2,2,2,1,1]
        # k=6: 6-2=4, 6-2=2, 6-2=0 → answer=3
        (6, [1, 3, 2, 5, 4, 5, 2, 3], 3),
        # k=4: 4-2=2, 4-2=0 → answer=2
        (4, [1, 3, 2, 5, 4, 5, 2, 3], 2),
        # k=2: 2-4=-2 → answer=1
        (2, [1, 1, 1, 1, 2, 2, 2, 3], 1),
        # 추가 케이스:
        # 단일 크기
        (3, [1, 1, 1], 1),
        # k == len(tangerine)
        (5, [1, 2, 3, 4, 5], 5),
    ]

    solutions = [
        ("Mine_one   (직접dict) ", solution_mine_one),
        ("Mine_two   (Counter)  ", solution_mine_two),
        ("Mine_three (most_com) ", solution_mine_three),
        ("Best       (Counter)  ", solution_best),
        ("Sub        (직접dict) ", solution_sub),
    ]

    # 워밍업 스텝
    _k, _t, _ = test_cases[0]
    for _, func in solutions:
        func(_k, _t[:])

    print("=" * 66)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (k, tangerine, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(k, tangerine[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
