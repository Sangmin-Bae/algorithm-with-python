"""
================================================================================
[문제 정보]
    사이트   : Programmers
    레벨     : Level 1
    문제명   : 부족한 금액 계산하기
    유형     : Math
    링크     : https://school.programmers.co.kr/learn/courses/30/lessons/82612
    풀이일자 : 2026-05-22
================================================================================
[문제 요약]
    N번째 이용료 = price × N
    count번 탑승 시 총 비용 = price×1 + price×2 + ... + price×count
    부족한 금액 반환 (충분하면 0)

    제약 조건
        - price : 1 이상 2,500 이하
        - money : 1 이상 1,000,000,000 이하 (10억)
        - count : 1 이상 2,500 이하

    총비용 최댓값 = 2,500 × (2,500×2,501/2) ≈ 78억
        → 파이썬 int: 임의 정밀도로 문제 없음
        → Java/C++: int 범위(약 21억) 초과 → long 필요
================================================================================
[입출력 예시]
    price | money | count | result
    ------|-------|-------|-------
    3     | 20    | 4     | 10    (3+6+9+12=30, 30-20=10)
================================================================================
[내 초기 풀이]
    solution_one  : 지문 그대로 구현, price×c를 c=1~count까지 money에서 뺌
    solution_two  : 분배법칙 적용, price×(1+2+...+count)로 변환
    solution_three: 등차수열 합 공식 적용, for문 제거 → O(1)

    발상 진화:
        1단계(one)  : 직역 구현
        2단계(two)  : price×(Σc) 분배법칙으로 묶기
        3단계(three): Σc = count×(1+count)/2 등차수열 공식 적용

[개선 포인트]
    solution_two  : sum(c for c in range()) → sum(range()) 로 간결화
                    range 자체가 이터러블이라 제너레이터 래핑 불필요
    solution_three: (count*(1+count)) / 2 → // 2 로 변경
                    / 연산자는 파이썬에서 항상 float 반환
                    money(int)에서 float를 빼면 반환값이 float가 될 수 있음
                    → // 정수 나눗셈으로 int 반환 보장
    공통:   abs(money) if money < 0 else 0
            → max(0, total - money) 로 개선
            의도 직관적, money 원본 훼손 없음
================================================================================
[수학적 근거 — 등차수열 합]
    총 비용 = price×1 + price×2 + ... + price×count
            = price × (1 + 2 + ... + count)
            = price × count×(1+count) / 2   ← 등차수열 합 공식
            (초항=1, 말항=count, 항수=count, 공차=1)
================================================================================
[복잡도 분석]
    N = count (최대 2,500)

    Mine_one   - 시간: O(N) | 공간: O(1) — count번 반복
    Mine_two   - 시간: O(N) | 공간: O(1) — sum(range()) 내부 순회
    Mine_three - 시간: O(1) | 공간: O(1) — 산술 연산만 사용, / → // 필요
    Best       - 시간: O(1) | 공간: O(1) — // + max(0, ...) 개선
    Sub        - 시간: O(N) | 공간: O(1) — sum(range()) 간결화

    N=2,500이라 체감 차이는 미미
    But Best는 count가 아무리 커져도 상수 시간 보장
================================================================================
"""

import time
from typing import List, Tuple


# ==============================================================================
# Mine solution one — 지문 직역 + 명시적 반복
# ==============================================================================
def solution_mine_one(price: int, money: int, count: int) -> int:
    """
    문제 조건을 그대로 구현한 초기 풀이

    개선 전 상태:
        - count번 반복하며 매번 price×c를 차감 → O(N)
        - money를 직접 수정 → 원본 훼손
        - abs(money) if money < 0 else 0 → max()로 개선 가능
    """
    for c in range(1, count + 1):
        money -= price * c          # N번째 이용료 차감

    return abs(money) if money < 0 else 0


# ==============================================================================
# Mine solution two — 분배법칙 적용 + sum() 제너레이터
# ==============================================================================
def solution_mine_two(price: int, money: int, count: int) -> int:
    """
    분배법칙으로 총비용을 price × Σc 형태로 변환한 풀이

    핵심 발상:
        price×1 + price×2 + ... = price × (1+2+...+count)

    개선 전 상태:
        - sum(c for c in range()): range 자체가 이터러블
            → sum(range())로 제너레이터 래핑 없이 직접 전달 가능
        - 여전히 O(N) 순회 발생
    """
    money -= price * sum(c for c in range(1, count + 1))
    return abs(money) if money < 0 else 0


# ==============================================================================
# Mine solution three — 등차수열 합 공식 적용 (O(1))
# ==============================================================================
def solution_mine_three(price: int, money: int, count: int) -> int:
    """
    등차수열 합 공식으로 for문을 제거한 O(1) 풀이

    핵심 발상:
        1+2+...+count = count×(1+count)/2  (등차수열 합)
        → 총비용 = price × count×(1+count)/2

    개선 전 상태:
        - (count*(1+count)) / 2 : / 연산자는 float 반환
            money(int) - float → 반환값이 float가 될 수 있음
            → // 정수 나눗셈으로 교체 필요
    """
    money -= price * ((count * (1 + count)) / 2)   # / → float 반환 주의
    return abs(money) if money < 0 else 0


# ==============================================================================
# Best solution — 등차수열 공식 + // + max(0, ...)
# ==============================================================================
def solution_best(price: int, money: int, count: int) -> int:
    """
    등차수열 합 공식으로 O(1) 구현, 정수 연산 보장

    Mine_three 대비 개선:
        - / → // : 정수 나눗셈으로 int 반환 보장
            count×(count+1)은 항상 짝수 (연속 두 정수의 곱)
        → // 2 결과가 항상 정수
            - abs(money) if money < 0 else 0
        → max(0, total - money): 의도 직관적, money 원본 훼손 없음
    """
    # 총비용 = price × count×(count+1)//2  (등차수열 합, 정수 보장)
    total = price * (count * (count + 1) // 2)
    return max(0, total - money)    # 부족하면 차액, 충분하면 0


# ==============================================================================
# Sub solution — 분배법칙 + sum(range()) 간결화
# ==============================================================================
def solution_sub(price: int, money: int, count: int) -> int:
    """
    분배법칙 + sum(range()) 직접 전달로 간결화한 풀이

    Mine_two 대비 개선:
        - sum(c for c in range()) → sum(range())
            range는 이터러블 → 제너레이터 래핑 불필요
        - max(0, total - money)로 반환 개선
    """
    # 총비용 = price × (1+2+...+count), range 직접 sum()에 전달
    total = price * sum(range(1, count + 1))
    return max(0, total - money)


# ==============================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==============================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[int, int, int, int]] = [
        # (price, money, count, 기댓값)
        (3,    20,          4,    10),   # 기본 예시: 30-20=10
        (3,    30,          4,     0),   # 정확히 충분: 30-30=0
        (3,    31,          4,     0),   # 충분: 31>30 → 0
        (1,     1,          1,     0),   # 최솟값: 1-1=0
        (2500,  1, 2500, 7815624999),   # 최댓값 케이스
        (1,     1, 2500,     3126249),   # price=1, money=1: 총비용=3126250
        (100, 1000000000, 2500,        0),  # money가 충분한 경우
    ]

    solutions = [
        ("Mine_one   (직역+반복)",     solution_mine_one),
        ("Mine_two   (분배+generator)", solution_mine_two),
        ("Mine_three (등차수열+/)",    solution_mine_three),
        ("Best       (등차수열+//)",   solution_best),
        ("Sub        (분배+range)",    solution_sub),
    ]

    print("=" * 68)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (price, money, count, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(price, money, count)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 68)


# ==============================================================================
# 실행 진입점
# ==============================================================================
if __name__ == "__main__":
    solution_comparison()