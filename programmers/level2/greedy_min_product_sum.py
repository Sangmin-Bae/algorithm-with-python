"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 최솟값 만들기
    유형       : Greedy / Sort
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12941
    풀이일자   : 2026-08-03
================================================================================
[문제 요약]
    길이가 같은 자연수 배열 A, B에서 각 원소를 하나씩 뽑아 곱하고
    모든 곱을 누적합했을 때 최솟값 반환 (각 원소는 한 번만 사용)

    제약 조건
        - A, B 크기: 1,000 이하 자연수
        - A, B 원소: 1,000 이하 자연수 (음수 없음)
================================================================================
[입출력 예시]
    A         | B         | answer
    ----------|-----------|-------
    [1, 4, 2] | [5, 4, 4] | 29
    [1, 2]    | [3, 4]    | 10
================================================================================
[수학적 증명 — 재배열 부등식(Rearrangement Inequality)]
    오름차순 A × 내림차순 B가 최솟값인 이유:

    교환 논증 (2개 원소 기준):
        A = [a_s, a_l] (a_s <= a_l)
        B = [b_l, b_s] (오름차순×내림차순)과 [b_s, b_l] (오름차순×오름차순)의 차:

        (a_s×b_l + a_l×b_s) - (a_s×b_s + a_l×b_l)
        = (a_s - a_l)(b_l - b_s)
        a_s <= a_l → (a_s - a_l) <= 0
        b_l >= b_s → (b_l - b_s) >= 0
        → 차이 <= 0 → 오름차순×내림차순이 항상 작거나 같음

    N개 원소로 확장: 재배열 부등식
        오름차순 × 내림차순 배열이 모든 순열 중 내적(dot product) 최솟값 보장

    자연수 조건의 중요성:
        음수 포함 시 음수×음수=양수가 되어 이 그리디가 성립하지 않음
        이 문제의 "자연수" 제약이 그리디 적용 가능 조건

[실측 결과 — N=1000, 5,000회 반복]
    풀이2 (sort+제너레이터):      0.210ms  ← 가장 빠름
    풀이4 (sorted+[::-1]):        0.242ms
    풀이4v2(sorted+reverse=True): 0.271ms
    풀이3 (sort+map+mul):         0.279ms

    sort() in-place가 sorted() 새 리스트보다 빠름
    [::-1] 슬라이싱이 reverse=True 정렬보다 빠른 케이스
    map+mul이 제너레이터 x*y보다 느린 이유:
        mul 함수 객체를 인수로 전달하는 오버헤드 > 인라인 x*y
================================================================================
[내 초기 풀이]
    solution_mine_one  : permutations 완전 탐색 (효율성 실패 O(N!))
    solution_mine_two  : sort() + 제너레이터
    solution_mine_three: sort() + map + mul
    solution_mine_four : sorted() + [::-1] 한 줄

[개선 포인트]
    solution_mine_one  : O(N!) → 효율성 실패, 학습 목적
    solution_mine_two  : 개선 필요 없음 - Best
                         sort() in-place + 제너레이터로 실측 가장 빠름
                         A, B 원본 수정 (sort() in-place)
    solution_mine_three: map+mul이 제너레이터보다 느림
    solution_mine_four : 개선 필요 없음 - Sub
                         한 줄 표현, A, B 원본 불변 유지 (sorted() 새 리스트)
================================================================================
[복잡도 분석]
    N = len(A) = len(B) (최대 1,000)

    Mine_one   - 시간: O(N! × N) | 공간: O(N!) - permutations 완전 탐색
    Mine_two   - 시간: O(N log N) | 공간: O(1)  - sort() in-place
    Mine_three - 시간: O(N log N) | 공간: O(1)  - sort() in-place
    Mine_four  - 시간: O(N log N) | 공간: O(N)  - sorted() 새 리스트 2개
    Best       - 시간: O(N log N) | 공간: O(1)  - Mine_two와 동일
    Sub        - 시간: O(N log N) | 공간: O(N)  - Mine_four와 동일
"""

import timeit
from itertools import permutations
from operator import mul
import time


# ================================================================================
# Mine solution one - permutations 완전 탐색 (효율성 실패)
# ================================================================================
def solution_mine_one(A: list[int], B: list[int]) -> int:
    """
    B의 모든 순열에 대해 A와 내적을 계산하는 완전 탐색 풀이 (효율성 실패)

    permutations(B):
        B 원소의 모든 순서 배열 생성 → N! 가지
        각 순열에 대해 A와 곱셈 합산 → N회

    효율성 실패 이유:
        O(N! × N): N=1000이면 천문학적 연산량
        그리디로 O(N log N)에 해결 가능

    min_total = float('inf'):
        시스템 상의 최댓값으로 초기화
        어떤 값과 비교해도 첫 케이스가 갱신됨
    """
    min_total = float('inf')

    for perm_B in permutations(B):
        current_sum = sum(x * y for x, y in zip(A, perm_B))
        if current_sum < min_total:
            min_total = current_sum

    return min_total


# ================================================================================
# Mine solution two - sort() + 제너레이터
# ================================================================================
def solution_mine_two(A: list[int], B: list[int]) -> int:
    """
    오름차순 A × 내림차순 B로 최솟값을 구하는 풀이

    재배열 부등식 적용:
        A.sort(): 오름차순 (작은 값이 앞)
        B.sort(reverse=True): 내림차순 (큰 값이 앞)
        작은 값 × 큰 값 쌍으로 합산 → 최솟값 보장

    sort() in-place:
        원본 A, B 수정
        새 리스트 생성 없음 → sorted() 대비 빠름
    """
    A.sort()
    B.sort(reverse=True)
    return sum(x * y for x, y in zip(A, B))


# ================================================================================
# Mine solution three - sort() + map + mul
# ================================================================================
def solution_mine_three(A: list[int], B: list[int]) -> int:
    """
    map + operator.mul로 곱셈을 처리하는 풀이

    mine_two 대비:
        sum(x * y for x, y in zip(A, B)) → sum(map(mul, A, B))
        map + mul: 함수 객체 전달 오버헤드
        → 실측에서 제너레이터 x*y보다 느림

    mul = operator.mul: 곱셈 연산을 함수로 표현
    """
    A.sort()
    B.sort(reverse=True)
    return sum(map(mul, A, B))


# ================================================================================
# Mine solution four - sorted() + [::-1] 한 줄
# ================================================================================
def solution_mine_four(A: list[int], B: list[int]) -> int:
    """
    sorted()와 [::-1] 슬라이싱으로 한 줄에 표현하는 풀이

    sorted():
        원본 A, B 불변 유지 → mine_two의 sort() in-place와 차이
        새 리스트 생성 → 공간 O(N)

    sorted(B)[::-1]:
        sorted(B): 오름차순 새 리스트 생성
        [::-1]: 역순 새 리스트 생성
        → sorted(B, reverse=True)보다 빠른 케이스 (실측 확인)
    """
    return sum(x * y for x, y in zip(sorted(A), sorted(B)[::-1]))


# ================================================================================
# Best solution - sort() + 제너레이터 (mine_two 주석 보강)
# ================================================================================
def solution_best(A: list[int], B: list[int]) -> int:
    """
    sort() in-place + 제너레이터로 최솟값을 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        sort() in-place: sorted() 새 리스트 생성 없음 → 메모리 효율
        제너레이터 x*y: map+mul 함수 객체 오버헤드 없음
        실측 N=1000: 0.210ms (풀이3 0.279ms, 풀이4 0.242ms 대비 우위)
        재배열 부등식: 자연수 원소에서 오름차순×내림차순이 최솟값 보장
    """
    A.sort()
    B.sort(reverse=True)
    return sum(x * y for x, y in zip(A, B))


# ================================================================================
# Sub solution - sorted() + [::-1] 한 줄 (mine_four 주석 보강)
# ================================================================================
def solution_sub(A: list[int], B: list[int]) -> int:
    """
    sorted()와 [::-1]로 원본 불변을 유지하면서 한 줄에 표현하는 서브 풀이

    Best 대비 특징:
        sorted(): 원본 A, B 불변 유지 (sort() in-place와 달리)
        한 줄 표현 → 코드 간결
        공간 O(N): sorted() 새 리스트 2개 생성
        성능은 Best보다 약간 느림 (새 리스트 생성 비용)
    """
    return sum(x * y for x, y in zip(sorted(A), sorted(B)[::-1]))


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], list[int], int]] = [
        # (A, B, 기댓값)
        # 손 추적:
        # A=[1,4,2], B=[5,4,4]
        # 정렬 후: A=[1,2,4], B=[5,4,4]
        # 1×5 + 2×4 + 4×4 = 5+8+16 = 29 ✓
        ([1, 4, 2], [5, 4, 4], 29),
        # A=[1,2], B=[3,4]
        # 정렬 후: A=[1,2], B=[4,3]
        # 1×4 + 2×3 = 4+6 = 10 ✓
        ([1, 2],    [3, 4],    10),
        # 추가 케이스:
        # 동일 원소
        ([3, 3], [3, 3], 18),
        # 단일 원소
        ([5], [7], 35),
    ]

    # mine_one은 소규모 입력에서만 검증
    small_cases = test_cases[:2]
    solutions_all = [
        ("Mine_one   (permutations)", solution_mine_one),
        ("Mine_two   (sort+gen)    ", solution_mine_two),
        ("Mine_three (sort+map+mul)", solution_mine_three),
        ("Mine_four  (sorted+[::-1])", solution_mine_four),
        ("Best       (sort+gen)    ", solution_best),
        ("Sub        (sorted+[::-1])", solution_sub),
    ]
    solutions_fast = solutions_all[1:]

    # 워밍업 스텝
    _A, _B, _ = test_cases[0]
    for _, func in solutions_fast:
        func(_A[:], _B[:])

    print("=" * 68)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    print("--- Mine_one (소규모 입력만) ---")
    for idx, (A, B, expected) in enumerate(small_cases, 1):
        start = time.perf_counter()
        output = solution_mine_one(A[:], B[:])
        elapsed = time.perf_counter() - start
        status = "PASS" if output == expected else "FAIL"
        print(f"{'Mine_one   (permutations)':<30} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
    print("-" * 68)

    for name, func in solutions_fast:
        for idx, (A, B, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(A[:], B[:])
            elapsed = time.perf_counter() - start
            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
