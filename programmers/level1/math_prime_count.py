"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 소수 찾기
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12921
    풀이일자   : 2026-07-24
===================================================================================
[문제 요약]
    1 이상 n 이하의 정수 중 소수의 개수 반환 (1은 소수 아님)

    제약 조건
        - n: 2 이상 1,000,000 이하
===================================================================================
[입출력 예시]
    n  | result
    ---|-------
    10 | 4      (소수: 2, 3, 5, 7)
    5  | 3      (소수: 2, 3, 5)
===================================================================================
[소수 판별 핵심 원리 - 제곱근까지만 탐색]
    x가 합성수라면 x = a × b (a <= b)로 표현 가능
    이때 a <= sqrt(x) 반드시 성립:
        a > sqrt(x)이고 b >= a이면 a×b > x → 모순
    따라서 sqrt(x) 이하의 수로만 나누어 봐도 약수 존재 여부 확인 가능
    sqrt(x) 이하에서 약수 발견 안 되면 소수

[에라토스테네스의 체 원리]
    소수 i의 배수는 모두 합성수 → is_prime 배열에서 False로 표시

    i*i부터 시작하는 이유:
        2i, 3i, ..., (i-1)*i는 이미 더 작은 소수의 배수로 처리됨
        예) i=5: 10=2×5(2에서처리), 15=3×5(3에서처리), 20=4×5(2에서처리)
        25=5×5 → 여기서 처음 나타남 → i*i에서 시작해도 누락 없음

    2부터 sqrt(n)까지만 순회하는 이유:
        i > sqrt(n)인 소수의 배수 중 n 이하는 이미 더 작은 소수에 의해 처리됨
        i*i > n이면 i의 배수 중 n 이하는 모두 이미 처리 완료

[set 방식 vs 리스트 방식 성능 비교]
    실측 (n=1,000,000, 10회 평균):
        에라토스테네스 리스트: 63ms
        에라토스테네스 set:   265ms  (4.2배 느림)

    set 방식이 느린 이유:
        nums -= set(range(...)): 매 호출마다 새 set 객체 생성 → 메모리 할당 비용
        set 해시 기반 → 해시 계산 + 메모리 분산 → 캐시 지역성 낮음
        차집합 연산: 두 set 순회하며 교차 → 추가 비용

    리스트 방식이 빠른 이유:
        is_prime[j] = False: 연속 메모리 직접 접근 → 캐시 지역성 높음
        range(i*i, n+1, i): 연속 메모리 순차 접근 → CPU 캐시 효율적
===================================================================================
[내 초기 풀이]
    solution_mine_one: 개별 소수 판별 (is_prime 함수)
    solution_mine_two: 에라토스테네스의 체 (리스트)

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Sub
                       개별 판별로 소수 판별 원리 명시적
                       is_prime 반환을 0/1로 해서 sum + 제너레이터로 간결하게 계수
    solution_mine_two: 개선 필요 없음 - Best
                       에라토스테네스의 체, 가장 빠른 방식
    solution_ref_one:  set 차집합 방식
                       코드 간결하나 리스트 방식 대비 4배 이상 느림
                       set 객체 반복 생성 + 해시 비용 + 낮은 캐시 지역성
===================================================================================
[복잡도 분석]
    N = n (최대 1,000,000)

    Mine_one - 시간: O(N*sqrt(N)) | 공간: O(1) - 각 수마다 sqrt(x) 탐색
    Mine_two - 시간: O(N log log N) | 공간: O(N) - 에라토스테네스의 체
    Ref_one  - 시간: O(N log log N) | 공간: O(N) - set 차집합 (상수 인자 큼)
    Best     - 시간: O(N log log N) | 공간: O(N) - Mine_two와 동일
    Sub      - 시간: O(N*sqrt(N))   | 공간: O(1) - Mine_one과 동일

    N=1,000,000:
        Mine_one: O(N*sqrt(N)) = O(10^9) -> 느림
        Mine_two: O(N log log N) ≈ O(4,000,000) -> 빠름
    실측: 에라토스테네스 63ms vs 개별 판별은 수십 배 느릴 것으로 예상
"""

import math
import time


# ==================================================================================
# Mine solution one - 개별 소수 판별
# ==================================================================================
def solution_mine_one(n: int) -> int:
    """
    각 수를 개별적으로 소수 판별하는 초기 풀이

    is_prime 함수:
        2부터 sqrt(x)까지 나누어서 약수 여부 확인
        약수 발견 -> 합성수 -> 0 반환
        약수 미발견 -> 소수 -> 1 반환
        반환값을 0/1 정수로 해서 sum 연산에 바로 활용

    sum(is_prime(num) for num in range(2, n+1)):
        제너레이터로 메모리 효율적으로 소수 개수 합산
        1은 소수 아니므로 range(2, n+1)에서 시작

    한계:
        각 수마다 sqrt(x)번 나눗셈 -> 전체 O(N*sqrt(N))
        N=1,000,000에서 약 10억 연산 -> 에라토스테네스 대비 느림
    """
    def is_prime(x: int) -> int:
        for i in range(2, math.isqrt(x) + 1):
            if x % i == 0:
                return 0
        return 1

    return sum(is_prime(num) for num in range(2, n + 1))


# ==================================================================================
# Mine solution two - 에라토스테네스의 체
# ==================================================================================
def solution_mine_two(n: int) -> int:
    """
    에라토스테네스의 체로 배수를 지워가며 소수를 찾는 풀이

    동작 원리:
        is_prime[i] = True: i는 소수 후보
        소수 i 발견 시 i*i, i*(i+1), ..., n 이하의 i 배수를 False로 표시

    i*i에서 시작하는 이유:
        2i ~ (i-1)*i: 이미 더 작은 소수에 의해 처리됨
        i*i: 처음으로 i에 의해서만 지워지는 배수 시작점

    2부터 sqrt(n)까지만 순회하는 이유:
        i > sqrt(n)인 소수의 배수 중 n 이하는 이미 더 작은 소수가 처리
        → sqrt(n) 이후 순회 불필요

    sum(is_prime):
        True=1, False=0으로 처리되어 소수 개수 직접 합산
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return sum(is_prime)


# ==================================================================================
# Ref solution one - 에라토스테네스의 체 (set 차집합 방식)
# ==================================================================================
def solution_ref_one(n: int) -> int:
    """
    set 차집합으로 에라토스테네스의 체를 구현하는 참고 풀이

    동작 원리:
        nums: 소수 후보 집합 {2, 3, ..., n}
        i가 소수(i in nums)이면 i*i 이상 i 배수를 차집합으로 제거
        최종 nums에 남은 원소 = 소수 집합

    Mine_two 대비:
        코드는 간결하나 성능은 4배 이상 느림 (실측 63ms vs 265ms)
        set 객체 반복 생성 + 해시 연산 + 낮은 캐시 지역성
        len(nums): sum(is_prime) 대신 집합 크기로 바로 개수 반환

    nums -= set(range(i*i, n+1, i)):
        매 호출마다 임시 set 생성 후 차집합 연산
        리스트 직접 접근 대비 오버헤드 큼
    """
    nums = set(range(2, n + 1))

    for i in range(2, math.isqrt(n) + 1):
        if i in nums:
            nums -= set(range(i * i, n + 1, i))

    return len(nums)


# ==================================================================================
# Best solution - 에라토스테네스의 체 리스트 (mine_two 주석 보강)
# ==================================================================================
def solution_best(n: int) -> int:
    """
    에라토스테네스의 체로 O(N log log N) 시간에 소수 개수를 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        리스트 연속 메모리: 배수 표시 시 캐시 지역성 높아 빠름
        O(N log log N): 에라토스테네스의 체의 이론적 복잡도
        실측 N=1,000,000: 63ms (set 방식 265ms 대비 4배 빠름)
        sum(is_prime): True/False가 1/0으로 처리되어 소수 개수 직접 합산
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return sum(is_prime)


# ==================================================================================
# Sub solution - 개별 소수 판별 (mine_one 주석 보강)
# ==================================================================================
def solution_sub(n: int) -> int:
    """
    각 수를 개별적으로 소수 판별하는 서브 풀이

    Best 대비 특징:
        에라토스테네스의 체 없이 소수 판별 원리 직접 표현
        is_prime(x): x 하나의 소수 여부만 판별, 다른 수 정보 불필요
        O(1) 추가 공간: 배열 없이 판별
        O(N*sqrt(N)) 시간: Best O(N log log N) 대비 느리나 원리 이해에 적합
    """
    def is_prime(x: int) -> int:
        for i in range(2, math.isqrt(x) + 1):
            if x % i == 0:
                return 0
        return 1

    return sum(is_prime(num) for num in range(2, n + 1))


# ==================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int]] = [
        # (n, 기댓값)
        # 손 추적:
        # n=10: 소수 = 2,3,5,7 -> 4
        (10, 4),
        # n=5: 소수 = 2,3,5 -> 3
        (5, 3),
        # 추가 케이스:
        # n=2: 가장 작은 소수 하나
        (2, 1),
        # n=20: 2,3,5,7,11,13,17,19 -> 8
        (20, 8),
        # n=100: 소수 25개
        (100, 25),
    ]

    solutions = [
        ("Mine_one (개별판별)    ", solution_mine_one),
        ("Mine_two (에라토스테네스)", solution_mine_two),
        ("Ref_one  (set차집합)   ", solution_ref_one),
        ("Best     (에라토스테네스)", solution_best),
        ("Sub      (개별판별)    ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _ = test_cases[0]
    for _, func in solutions:
        func(_n)

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


# ==================================================================================
# 실행 진입점
# ==================================================================================
if __name__ == "__main__":
    solution_comparison()
