"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 최대공약수와 최소공배수
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12940
    풀이일자   : 2026-06-28
===================================================================================
[문제 요약]
    두 자연수 n, m의 최대공약수(GCD)와 최소공배수(LCM)를 반환

    제약 조건
        - n, m: 1 이상 1,000,000 이하 자연수
===================================================================================
[입출력 예시]
    n  | m  | return
    ---|----|---------
    3  | 12 | [3, 12]   (GCD=3, LCM=12)
    2  | 5  | [1, 10]   (GCD=1, LCM=10)
===================================================================================
[유클리드 호제법 — 핵심 아이디어]
    "나머지도 공약수를 공유한다"

    증명:
        a = b × q + r  (q는 몫, r = a % b)
        a, b의 공약수 d가 있으면:
            a = d × p,  b = d × q_
            r = a - b×q = d×(p - q_×q)
            → r도 d의 배수 → d는 b와 r의 공약수
        ∴ GCD(a, b) = GCD(b, a % b)

    나머지가 0이면 GCD인 이유:
        GCD(b, 0) = b  (0은 모든 수의 배수)

    손 추적 (a=12, b=8):
        GCD(12, 8) → GCD(8, 4) → GCD(4, 0) → 4  ✓

    기억 고리 — 공식보다 이 한 문장:
        "나머지가 0이 될 때까지 (a, b) → (b, a%b) 반복"

[GCD × LCM = n × m 증명]
    n = GCD × a,  m = GCD × b  (a, b는 서로소)
    LCM = GCD × a × b = n × m / GCD
    ∴ LCM = n × m // GCD
===================================================================================
[내 초기 풀이]
    solution_mine_one    : math.gcd() + n*m//gcd 공식
    solution_mine_two    : GCD 완전탐색(brute force) 직접 구현
    solution_mine_three  : GCD 유클리드 반복문(loop) 직접 구현
    solution_mine_four   : GCD 유클리드 재귀(recursive) 직접 구현

    brute_force 방식:
        min(n,m)부터 1씩 감소하며 두 수 모두 나누는 수를 탐색
        최악의 경우 min(n,m)번 순회 → O(min(n,m))

    유클리드 loop/recursive:
        (a, b) → (b, a%b) 반복, 나머지 0이면 종료
        매 단계 b가 절반 이하로 줄어듦 → O(log min(n,m))

[개선 포인트]
    solution_mine_one    : 개선 필요 없음 - Best
    solution_mine_two    : brute_force O(min(n,m)) → 학습 목적, 실전 비추천
    solution_mine_three  : 개선 필요 없음 - Sub
                           스택 오버헤드 없는 가장 안전한 유클리드 구현
    solution_mine_four   : 재귀 깊이 ≤ log₂(1,000,000) ≈ 20 → 안전하나 스택 비용
===================================================================================
[GCD 구현 방식별 성능 비교]
    brute_force: O(min(n,m))  → n,m=1,000,000이면 최대 100만 순회
    gcd_loop:    O(log min)   → 최대 약 20번 반복, 스택 오버헤드 없음
    gcd_recursive: O(log min) → 최대 약 20번 재귀, 각 호출마다 PyFrameObject 생성

    풀이 분리 이유:
        하나의 함수에 3개 내부 함수를 담으면 첫 호출 시
        내부 함수 3개의 PyFrameObject가 모두 생성되어 오버헤드 중첩
        각 GCD 구현을 별도 풀이로 분리 → 순수 GCD 구현 방식별 성능 비교 가능
===================================================================================
[복잡도 분석]
    N = min(n, m) (최대 1,000,000)

    Mine_one   - 시간: O(log N) | 공간: O(1)      - math.gcd() C 레벨 구현
    Mine_two   - 시간: O(N)     | 공간: O(1)      - 완전탐색
    Mine_three - 시간: O(log N) | 공간: O(1)      - 유클리드 반복문
    Mine_four  - 시간: O(log N) | 공간: O(log N)  - 유클리드 재귀 (호출 스택)
    Best       - 시간: O(log N) | 공간: O(1)      - Mine_one과 동일
    Sub        - 시간: O(log N) | 공간: O(1)      - Mine_three와 동일

    log₂(1,000,000) ≈ 20 → 유클리드 방식은 최대 20번 반복/재귀
"""

import math
import time
from typing import List, Tuple


# =================================================================================
# Mine solution one - math.gcd() + LCM 공식
# =================================================================================
def solution_mine_one(n: int, m: int) -> List[int]:
    """
    math.gcd() 라이브러리와 GCD×LCM=n×m 공식으로 구하는 초기 풀이

    math.gcd(): CPython C 레벨 유클리드 호제법 구현
    lcm = n * m // gcd: GCD×LCM=n×m 수학적 정리 활용
    Python int 임의 정밀도 → n*m=10^12도 오버플로우 없음
    """
    gcd = math.gcd(n, m)
    lcm = (n * m) // gcd
    return [gcd, lcm]


# =================================================================================
# Mine solution two - GCD 완전탐색(brute force)
# =================================================================================
def solution_mine_two(n: int, m: int) -> List[int]:
    """
    완전탐색으로 GCD를 구하는 풀이

    brute_force 원리:
        min(n,m)부터 1씩 감소하며 두 수 모두의 약수인 첫 수 = GCD
        첫 번째 발견 즉시 반환 (조기 탈출)

    시간복잡도 O(min(n,m)):
        n,m=1,000,000이면 최대 100만 순회
        유클리드 O(log N) 대비 매우 비효율
        학습 목적: 완전탐색 vs 유클리드 성능 차이 확인용
    """
    def gcd_brute_force(a: int, b: int) -> int:
        for i in range(min(a, b), 0, -1):
            if a % i == 0 and b % i == 0:
                return i

    gcd = gcd_brute_force(n, m)
    lcm = (n * m) // gcd
    return [gcd, lcm]


# =================================================================================
# Mine solution three - GCD 유클리드 반복문(loop)
# =================================================================================
def solution_mine_three(n: int, m: int) -> List[int]:
    """
    유클리드 호제법을 반복문으로 구현한 풀이

    gcd_loop 원리:
        "나머지가 0이 될 때까지 (a, b) → (b, a%b) 반복"
        b가 0이 되면 a가 GCD

    재귀(mine_four) 대비 장점:
        함수 호출 스택 없음 → PyFrameObject 생성 오버헤드 없음
        재귀 깊이 제한(sys.setrecursionlimit) 무관
    """
    def gcd_loop(a: int, b: int) -> int:
        while b > 0:
            a, b = b, a % b     # (a,b) → (b, a%b)
        return a                # b==0이 되면 a가 GCD

    gcd = gcd_loop(n, m)
    lcm = (n * m) // gcd
    return [gcd, lcm]


# =================================================================================
# Mine solution four - GCD 유클리드 재귀(recursive)
# =================================================================================
def solution_mine_four(n: int, m: int) -> List[int]:
    """
    유클리드 호제법을 재귀로 구현한 풀이

    gcd_recursive 원리:
        기저 조건: b==0이면 a가 GCD
        재귀: GCD(a,b) = GCD(b, a%b)

    반복문(mine_three) 대비 특징:
        수학적 정의를 재귀로 직접 표현 → 가독성 우위
        각 재귀 호출마다 PyFrameObject 생성 → 스택 비용
        최대 재귀 깊이: log₂(1,000,000) ≈ 20 → Python 기본 제한 1,000 이내 안전
    """
    def gcd_recursive(a: int, b: int) -> int:
        if b == 0:
            return a
        return gcd_recursive(b, a % b)

    gcd = gcd_recursive(n, m)
    lcm = (n * m) // gcd
    return [gcd, lcm]


# =================================================================================
# Best solution - math.gcd() (mine_one 주석 보강)
# =================================================================================
def solution_best(n: int, m: int) -> List[int]:
    """
    math.gcd() + LCM 공식으로 GCD, LCM을 구하는 최적 풀이

    mine_one과 동일한 로직, 근거 주석 보강:
        math.gcd(): C 레벨 유클리드 → Python 구현 대비 빠름
        LCM = n × m // GCD: 수학 정리 직접 활용, 추가 순회 없음
    """
    gcd = math.gcd(n, m)
    lcm = (n * m) // gcd
    return [gcd, lcm]


# =================================================================================
# Sub solution - GCD 유클리드 반복문 (mine_three 주석 보강)
# =================================================================================
def solution_sub(n: int, m: int) -> List[int]:
    """
    유클리드 호제법 반복문으로 직접 구현하는 서브 풀이

    Best 대비 특징:
        math.gcd() 없이 유클리드 원리를 코드로 직접 표현
        "나머지가 0이 될 때까지 (a,b) → (b, a%b) 반복" 원리 가시화
        재귀(mine_four) 대비 스택 오버헤드 없음 → 더 안전한 구현
    """
    a, b = n, m
    while b > 0:
        a, b = b, a % b
    gcd = a
    lcm = (n * m) // gcd
    return [gcd, lcm]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[int, int, List[int]]] = [
        # (n, m, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # GCD(3,12): 3→12%3=0 → GCD=3, LCM=3*12//3=12
        (3,  12,        [3, 12]),
        # GCD(2,5): 2→5%2=1→2%1=0 → GCD=1, LCM=10
        (2,  5,         [1, 10]),
        # 추가 케이스:
        # GCD(12,8): 12→8,4→4,0 → GCD=4, LCM=24
        (12, 8,         [4, 24]),
        # GCD(1,1): GCD=1, LCM=1
        (1,  1,         [1, 1]),
        # 대규모: GCD(1000000,999999)=1, LCM=999999000000
        (1_000_000, 999_999, [1, 999_999_000_000]),
    ]

    solutions = [
        ("Mine_one   (math.gcd)  ", solution_mine_one),
        ("Mine_two   (brute_force)", solution_mine_two),
        ("Mine_three (gcd_loop)  ", solution_mine_three),
        ("Mine_four  (gcd_recur) ", solution_mine_four),
        ("Best       (math.gcd)  ", solution_best),
        ("Sub        (gcd_loop)  ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _m, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _m)

    print("=" * 66)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (n, m, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, m)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
