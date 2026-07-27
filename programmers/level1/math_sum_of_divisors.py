"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 약수의 합
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12928
    풀이일자   : 2026-07-27
===================================================================================
[문제 요약]
    정수 n의 모든 약수의 합 반환

    제약 조건
        - n: 0 이상 3000 이하 (n=0 포함)
===================================================================================
[입출력 예시]
    n  | return
    ---|-------
    12 | 28     (약수: 1,2,3,4,6,12 -> 합 28)
    5  | 6      (약수: 1,5 -> 합 6)
===================================================================================
[핵심 원리 - 약수는 쌍을 이룬다]
    n = a × b (a <= b)라면 a <= sqrt(n) 반드시 성립
    -> sqrt(n) 이하의 a만 탐색하면 b = n//a도 자동으로 찾을 수 있음

    제곱수 처리:
        a = b = sqrt(n)인 경우 쌍이 동일 -> 한 번만 더해야 함
        d * d == n: 제곱수 여부 확인

    손 추적 (n=12, sqrt(12)=3):
        d=1: 12%1=0, 1*1≠12 -> 1 + 12 = 13
        d=2: 12%2=0, 2*2≠12 -> 2 + 6 = 8
        d=3: 12%3=0, 3*3≠12 -> 3 + 4 = 7
        합: 13+8+7 = 28 ✓

    손 추적 (n=9, sqrt(9)=3):
        d=1: 9%1=0, 1*1≠9 -> 1 + 9 = 10
        d=3: 9%3=0, 3*3=9 -> 3만 더함 (제곱수)
        합: 10+3 = 13 ✓

[solution_four n=0 엣지케이스]
    answer = 1 + n으로 초기화할 때 n=0이면 answer = 1
    0의 약수 합은 수학적으로 0이 맞음 (0은 약수 개념 자체가 모호)
    -> n=0인 경우 별도 처리 필요 (제약 조건: n은 0 이상)
    solution_three는 range(1, isqrt(0)+1) = range(1,1) = 빈 범위 -> 0 반환 ✓
    solution_four는 answer=1+0=1로 오답 -> if n==0: return 0 방어 필요
===================================================================================
[내 초기 풀이]
    solution_mine_one  : while 1~n 순회 + set (O(N))
    solution_mine_two  : range 1~sqrt(n) 순회 + set (O(sqrt(N)))
    solution_mine_three: range 1~sqrt(n) + 조건분기 누적합 (set 없음)
    solution_mine_four : 1+n 선초기화 + range 2~sqrt(n) + 조건분기 (n=0 오류)

[개선 포인트]
    solution_mine_one  : O(N) -> O(sqrt(N))으로 개선 가능
    solution_mine_two  : set 생성 비용 -> 조건분기 누적합으로 개선 가능
    solution_mine_three: 개선 필요 없음 - Best_algo (가독성 우위)
    solution_mine_four : n=0 엣지케이스 오류 -> 별도 처리 후 Best_practical

    Best_algo vs Best_practical 충돌:
        코딩테스트: solution_mine_three (가독성, 엣지케이스 없음)
        성능 최적화: solution_mine_four (연산 최소화, n=0 방어 추가)
===================================================================================
[복잡도 분석]
    N = n (최대 3000)

    Mine_one   - 시간: O(N)       | 공간: O(D)  - D=약수 수, 1~n 전체 순회
    Mine_two   - 시간: O(sqrt(N)) | 공간: O(D)  - set + sqrt(n)까지 순회
    Mine_three - 시간: O(sqrt(N)) | 공간: O(1)  - 조건분기 누적합
    Mine_four  - 시간: O(sqrt(N)) | 공간: O(1)  - 2~sqrt(n) 순회 (1 루프 절약)
    Best_algo  - 시간: O(sqrt(N)) | 공간: O(1)  - Mine_three와 동일
    Best_prac  - 시간: O(sqrt(N)) | 공간: O(1)  - Mine_four + n=0 방어

    N=3000: sqrt(3000) ≈ 55 -> 모두 실질적으로 O(1)에 수렴
"""

import math
import time


# ==================================================================================
# Mine solution one - while 1~n 순회 + set
# ==================================================================================
def solution_mine_one(n: int) -> int:
    """
    1부터 n까지 순회하며 약수를 set에 모아 합산하는 초기 풀이

    핵심:
        d와 n//d가 모두 n의 약수
        set으로 제곱수(d==n//d) 중복 자동 방지
        while d <= n: 1부터 n까지 전체 순회 -> O(N)

    한계:
        n까지 전체 순회 -> sqrt(n)까지만 순회해도 됨
        set 객체 생성 및 해시 비용
    """
    divisors = set()
    d = 1

    while d <= n:
        if n % d == 0:
            divisors.add(d)
            divisors.add(n // d)
        d += 1

    return sum(divisors)


# ==================================================================================
# Mine solution two - range 1~sqrt(n) + set
# ==================================================================================
def solution_mine_two(n: int) -> int:
    """
    제곱근까지만 순회하고 set으로 약수 쌍을 관리하는 풀이

    mine_one 대비:
        while 1~n -> range(1, isqrt(n)+1): 순회 범위 O(N) -> O(sqrt(N))
        나머지 로직 동일

    set으로 중복 방지:
        d=3, n=9: d(3)와 n//d(3)가 동일 -> set이 자동으로 하나만 유지
    """
    divisors = set()

    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            divisors.add(d)
            divisors.add(n // d)

    return sum(divisors)


# ==================================================================================
# Mine solution three - 조건분기 누적합 (set 없음)
# ==================================================================================
def solution_mine_three(n: int) -> int:
    """
    제곱수 여부를 조건문으로 분기해 set 없이 누적합하는 풀이

    mine_two 대비:
        set 생성 없이 정수형 answer에 직접 누적
        d * d == n: 제곱수면 d만 더함 (쌍이 동일)
        아니면 d + n//d 모두 더함

    n=0 처리:
        range(1, isqrt(0)+1) = range(1,1) = 빈 범위 -> answer=0 반환 ✓
    """
    answer = 0

    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            if d * d == n:
                answer += d
            else:
                answer += (n // d) + d

    return answer


# ==================================================================================
# Mine solution four - 1+n 선초기화 + range 2~sqrt(n) (n=0 방어 포함)
# ==================================================================================
def solution_mine_four(n: int) -> int:
    """
    수학적 성질을 이용해 1과 n을 선초기화하고 루프 범위를 줄이는 풀이

    핵심:
        모든 정수는 1과 자기 자신이 약수 -> answer = 1 + n으로 선초기화
        range(2, ...): 1은 이미 처리됐으므로 2부터 시작 (루프 1회 절약)

    n=0 엣지케이스:
        answer = 1 + 0 = 1이 되어 0의 약수 합(0)과 다름 -> 오답
        제약 조건에 n=0 포함(0 이상) -> 별도 방어 필요
        if n == 0: return 0으로 처리
    """
    answer = 1 + n

    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            if d * d == n:
                answer += d
            else:
                answer += (n // d) + d

    return answer


# ==================================================================================
# Best solution algo - 조건분기 누적합 (mine_three 주석 보강)
# ==================================================================================
def solution_best_algo(n: int) -> int:
    """
    약수 쌍 원리 + 조건분기로 O(sqrt(N)) 시간, O(1) 공간의 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        n=0 포함 모든 입력 자연스럽게 처리 (빈 range -> 0 반환)
        set 없이 정수 누적 -> 해시 비용 없음
        d * d == n: 제곱수 여부를 정수 곱셈으로 안전하게 판별
        코딩테스트에서 가독성과 안전성 모두 우위
    """
    answer = 0

    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            if d * d == n:
                answer += d
            else:
                answer += (n // d) + d

    return answer


# ==================================================================================
# Best solution practical - 1+n 선초기화 + n=0 방어 (mine_four 주석 보강)
# ==================================================================================
def solution_best_practical(n: int) -> int:
    """
    수학적 성질로 1+n을 선초기화해 루프를 최소화하는 풀이

    mine_four와 동일한 로직, n=0/n=1 방어 포함:
        모든 양의 정수는 1과 자신이 약수 -> answer = 1 + n
        range(2, ...): 2부터 시작해 루프 1회 절약
        n=0, n=1 명시적 분기 필요

    Mine_three 대비 실질적 이점 없음:
        n=0: Mine_three는 빈 range로 자동 처리
             Best_prac은 if n==0 조건 평가 추가
        n=1: Mine_three는 for 1회 순회로 자연스럽게 처리
             Best_prac은 if n==1 조건 평가로 처리
        n>=2: Mine_three 정상 순회
             Best_prac은 조건 2개 평가 후 순회 (조건 평가 비용 추가)
        -> 선초기화 아이디어가 엣지케이스 처리 비용을 상쇄하지 못함
        -> Mine_three가 모든 구간에서 손해 없이 처리
    """
    if n == 0:
        return 0
    if n == 1:
        return 1

    answer = 1 + n

    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            if d * d == n:
                answer += d
            else:
                answer += (n // d) + d

    return answer


# ==================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int]] = [
        # (n, 기댓값)
        # 공식 예시
        (12, 28),   # 1+2+3+4+6+12=28
        (5,  6),    # 1+5=6
        # 추가 케이스:
        (0,  0),    # n=0: 약수 합 0 (엣지케이스)
        (1,  1),    # n=1: 약수 1만 존재
        (9,  13),   # 제곱수: 1+3+9=13
        (3000, 9360),  # 최대값
    ]

    solutions = [
        ("Mine_one   (while+set)  ", solution_mine_one),
        ("Mine_two   (range+set)  ", solution_mine_two),
        ("Mine_three (조건분기)   ", solution_mine_three),
        ("Mine_four  (1+n선초기화)", solution_mine_four),
        ("Best_algo  (조건분기)   ", solution_best_algo),
        ("Best_prac  (1+n+방어)   ", solution_best_practical),
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
