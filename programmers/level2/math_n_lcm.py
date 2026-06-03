"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : N개의 최소공배수
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12953
    풀이일자   : 2025-06-03
================================================================================
[문제 요약]
    N개의 수의 최소공배수(LCM)를 반환.

    제약 조건
        - arr 길이: 1 이상 15 이하
        - arr 원소: 100 이하 자연수
================================================================================
[입출력 예시]
    arr        | result
    -----------|-------
    [2,6,8,14] | 168
    [1,2,3]    | 6
================================================================================
[유클리드 호제법 증명 — GCD(x,y) = GCD(y, x%y)]
    x = y×q + r  (q는 몫, r = x%y)

    x,y의 공약수 d가 있으면:
        x = d×a, y = d×b
        r = x - y×q = d×(a - b×q) → r도 d의 배수
        → d는 y,r의 공약수이기도 함

    y,r의 공약수 d'가 있으면:
        x = y×q + r = d'×(cq+e) → x도 d'의 배수
        → d'는 x,y의 공약수이기도 함

    ∴ "x,y의 공약수 집합" = "y,r의 공약수 집합"
        → GCD(x,y) = GCD(y, x%y)

    나머지가 0일 때 GCD인 이유:
        GCD(y, 0) = y
        (0은 모든 수의 배수 → 0의 약수 = 모든 자연수 → GCD(y,0) = y)

[LCM = x×y // GCD 증명]
    x = GCD×a, y = GCD×b (a,b는 서로소)
    LCM = GCD×a×b = x×b = x×(y/GCD) = x×y/GCD

    손 추적: x=12, y=8
        GCD(12,8) = GCD(8,4) = GCD(4,0) = 4
        12=4×3, 8=4×2, LCM = 4×3×2 = 24
        공식: 12×8/4 = 24  ✓

[N개 LCM이 순차 적용으로 구해지는 이유]
    LCM(a,b,c) = LCM(LCM(a,b), c)
    LCM이 결합법칙을 만족하므로 왼쪽부터 순차 적용 가능
================================================================================
[내 초기 풀이]
    초기 시도 — 소인수분해 방식 (구현 실패):
        소인수분해 후 소인수별 최대 지수의 곱으로 LCM 구하는 방식 시도
        접근법 자체는 수학적으로 완벽히 맞음 (LCM의 정의 자체)
        막힌 지점: 소인수분해 결과를 리스트로 담으려 했으나
            count()로 개수 세는 과정에서 중첩 루프 발생 → 구현 포기
        → 딕셔너리 {소인수: 지수}로 집계했어야 함 (solution_sub_prime 참고)

    GCD 공식(유클리드 호제법)이 기억나지 않아 찾아보고 풀이 완성:
    solution_mine_one: 직접 구현한 gcd/lcm 함수를 순차 적용
    solution_mine_two: math.gcd() 라이브러리로 간결하게 구현

[개선 포인트]
    solution_mine_one/two: for 루프 + answer 변수 → reduce로 더 간결하게
    Best: functools.reduce + lambda로 한 줄 표현
    Sub_prime: 소인수분해 방식 — 초기 시도 방향을 딕셔너리로 완성한 참고 풀이
                소인수 정보가 직접 필요한 문제에서 활용 가능
================================================================================
[복잡도 분석]
    N = len(arr) (최대 15), M = max(arr) (최대 100)

    GCD 1회: O(log M) — 유클리드 호제법 단계 수
    전체:    O(N log M) — N-1번 LCM 적용

    소인수분해 방식 (Sub_prime):
        prime_factors 1회: O(√M) — √M까지 나눗셈 시도
        전체: O(N × √M) — 유클리드 대비 약 10배 느림
        이 문제(N≤15, M≤100): 모두 통과 가능

    N≤15, M≤100 → 사실상 O(1)
================================================================================
"""

import math
from functools import reduce
from typing import List, Tuple


# ==============================================================================
# GCD 헬퍼 함수들 — 직접 구현
# ==============================================================================
def gcd_while(x: int, y: int) -> int:
    """while 반복문으로 구현한 유클리드 호제법"""
    if x < y:
        x, y = y, x
    while y != 0:
        x, y = y, x % y
    return x


def gcd_recursive(x: int, y: int) -> int:
    """재귀 함수로 구현한 유클리드 호제법"""
    if x < y:
        x, y = y, x
    if y == 0:
        return x
    return gcd_recursive(y, x % y)


def lcm(x: int, y: int) -> int:
    """두 수의 최소공배수: x×y // GCD(x,y)"""
    return (x * y) // gcd_while(x, y)


# ==============================================================================
# Mine solution one — 직접 구현 GCD/LCM + for 루프
# ==============================================================================
def solution_mine_one(arr: List[int]) -> int:
    """
    직접 구현한 gcd, lcm 함수를 순차 적용하는 초기 풀이

    핵심:
        N개 LCM = LCM(LCM(...LCM(arr[0], arr[1])...), arr[N-1])
        LCM이 결합법칙 만족 → 왼쪽부터 순차 적용 가능

    개선 가능:
        for 루프 → functools.reduce로 더 간결하게 표현
    """
    answer = arr[0]
    for i in arr[1:]:
        answer = lcm(answer, i)
    return answer


# ==============================================================================
# Mine solution two — math.gcd() 라이브러리 활용
# ==============================================================================
def solution_mine_two(arr: List[int]) -> int:
    """
    math.gcd() 내장 라이브러리로 GCD를 구하는 간결한 풀이

    Mine_one 대비:
        직접 구현 gcd → math.gcd() 라이브러리
        별도 lcm 함수 없이 인라인으로 처리

    개선 가능:
        for 루프 → reduce로 더 간결하게
    """
    answer = arr[0]
    for i in arr[1:]:
        answer = (answer * i) // math.gcd(answer, i)
    return answer


# ==============================================================================
# Best solution — functools.reduce + lambda
# ==============================================================================
def solution_best(arr: List[int]) -> int:
    """
    reduce로 LCM을 순차 적용하는 최적 풀이.

    Mine_two 대비 개선:
        for 루프 + answer 변수 → reduce + lambda로 압축
        reduce(f, [a,b,c,d]) = f(f(f(a,b), c), d)
        → 왼쪽부터 순차 LCM 적용과 동일

    lambda x,y: x*y//math.gcd(x,y) = lcm(x,y)
    """
    return reduce(lambda x, y: x * y // math.gcd(x, y), arr)


# ==============================================================================
# Sub solution — 직접 구현 GCD + reduce
# ==============================================================================
def solution_sub(arr: List[int]) -> int:
    """
    직접 구현한 GCD를 reduce와 결합한 풀이

    Best 대비 특징:
        math.gcd 대신 직접 구현 gcd_while 사용
        라이브러리 없이 동작 원리를 코드로 표현
    """
    return reduce(lambda x, y: x * y // gcd_while(x, y), arr)


# ==============================================================================
# Sub solution two — 소인수분해 방식 LCM (참고용)
# ==============================================================================
def prime_factors(n: int) -> dict:
    """
    n을 소인수분해해서 {소인수: 지수} 딕셔너리로 반환

    알고리즘:
        2부터 √n까지 시도 (√n 초과 소인수는 최대 1개 → 나머지로 처리)
        나누어 떨어지면 지수 증가, 나누어질 때까지 반복
        루프 종료 후 남은 n > 1이면 그 자체가 소인수

    손 추적 (n=12):
        d=2: 12%2=0 → {2:1}, n=6 → 6%2=0 → {2:2}, n=3 → 3%2≠0
        d=3: 3*3=9 > 3 → 루프 종료
        남은 n=3 > 1 → {2:2, 3:1}  → 12 = 2² × 3¹  ✓
    """
    factors = {}
    d = 2

    while d * d <= n:  # √n까지만 시도
        while n % d == 0:  # d로 나누어 떨어지는 동안
            factors[d] = factors.get(d, 0) + 1  # 지수 누적
            n //= d
        d += 1

    if n > 1:  # 남은 수가 있으면 소인수
        factors[n] = factors.get(n, 0) + 1

    return factors


def solution_sub_prime(arr: List[int]) -> int:
    """
    소인수분해로 각 원소의 소인수별 최대 지수를 구해 LCM을 계산하는 풀이

    수학적 근거:
        LCM = 각 소인수의 최대 지수들의 곱
        예) 12=2²×3¹, 18=2¹×3² → LCM=2²×3²=36

    핵심 자료구조 — 딕셔너리 선택 이유:
        리스트 [2,2,3] 방식: count()로 개수 세야 해서 루프 추가 발생
            → arr 순회 × unique 순회 × count 순회 = O(N³) 수준
        딕셔너리 {2:2, 3:1} 방식: 지수를 O(1)로 접근/비교 가능
            → arr 순회 × 소인수 종류 = O(N × √M)

    max_factors 누적 과정 ([2,6,8,14]):
        n=2:  {2:1}
        n=6:  {2:1, 3:1}         (3 새로 추가)
        n=8:  {2:3, 3:1}         (2의 지수 1→3 갱신)
        n=14: {2:3, 3:1, 7:1}    (7 새로 추가)
        LCM = 2³×3¹×7¹ = 8×3×7 = 168  ✓

    유클리드 호제법 대비:
        접근법은 수학적으로 완벽히 맞음 (LCM의 정의 자체)
        성능: 약 10배 느림, 이 문제 제약에서는 통과 가능
        활용: 소인수분해 중점 문제나 개별 소인수 정보가 필요할 때 유용
    """
    max_factors = {}  # 소인수별 최대 지수 저장

    for n in arr:
        for prime, exp in prime_factors(n).items():
            # 없으면 추가, 있으면 더 큰 지수로 갱신
            if prime not in max_factors:
                max_factors[prime] = exp
            else:
                max_factors[prime] = max(max_factors[prime], exp)

    # 각 소인수의 최대 지수 거듭제곱의 곱 = LCM
    result = 1
    for prime, exp in max_factors.items():
        result *= prime ** exp

    return result


# ==============================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==============================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], int]] = [
        # (arr, 기댓값)
        # 손 추적:
        # [2,6,8,14]:
        #   lcm(2,6) = 2×6//gcd(2,6) = 12//2 = 6
        #   lcm(6,8) = 6×8//gcd(6,8) = 48//2 = 24
        #   lcm(24,14) = 24×14//gcd(24,14) = 336//2 = 168
        ([2, 6, 8, 14], 168),
        # [1,2,3]:
        #   lcm(1,2) = 1×2//gcd(1,2) = 2//1 = 2
        #   lcm(2,3) = 2×3//gcd(2,3) = 6//1 = 6
        ([1, 2, 3],     6),
        # [1]: 원소 하나 → 그대로 반환
        ([1],           1),
        # [2,4]: lcm(2,4) = 8//2 = 4
        ([2, 4],        4),
        # [3,5]: lcm(3,5) = 15//1 = 15 (서로소)
        ([3, 5],        15),
        # [6,10,15]: lcm(6,10)=30, lcm(30,15)=30
        #   gcd(6,10)=2, 6×10//2=30
        #   gcd(30,15)=15, 30×15//15=30
        ([6, 10, 15],   30),
    ]

    solutions = [
        ("Mine_one (직접구현+for)",   solution_mine_one),
        ("Mine_two (math.gcd+for)",  solution_mine_two),
        ("Best     (reduce+lambda)", solution_best),
        ("Sub      (직접구현+reduce)",solution_sub),
        ("Sub_prime(소인수분해방식)", solution_sub_prime),
    ]

    print("=" * 64)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    import time
    for name, func in solutions:
        for idx, (arr, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 64)


# ==============================================================================
# 실행 진입점
# ==============================================================================
if __name__ == "__main__":
    solution_comparison()
