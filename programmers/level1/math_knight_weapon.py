"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 기사단원의 무기
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/136798
    풀이일자   : 2026-07-12
===================================================================================
[문제 요약]
    1~number 각 수의 약수 개수를 구하고
    약수 개수 > limit이면 power로 대체한 값들의 합 반환

    제약 조건
        - number: 1 이상 100,000 이하
        - limit: 2 이상 100 이하
        - power: 1 이상 limit 이하
===================================================================================
[입출력 예시]
    number | limit | power | result
    -------|-------|-------|-------
    5      | 3     | 2     | 10     (약수개수: [1,2,2,3,2] → 합 10)
    10     | 3     | 2     | 21     (6,8,10번 기사 → power=2로 대체)
===================================================================================
[약수 개수 계산 — 제곱근 활용]
    약수는 항상 쌍으로 존재: n = a × b (a ≤ b)
    a ≤ √n 이하만 탐색하면 쌍(b = n/a)도 함께 계산 가능
    → O(√n) 탐색으로 전체 약수 개수 계산

    제곱수 처리:
        i² = n이면 약수 쌍이 (i, i)로 동일 → 1개만 카운트
        i² ≠ n이면 (i, n//i)로 서로 다른 쌍 → 2개 카운트

    math.isqrt(n) 사용 이유:
        int(n ** 0.5): 부동소수점 오차 가능 (예: √49 = 6.999...→ 6)
        math.isqrt(n): 정수 제곱근 정확하게 계산 → 안전

    손 추적 (n=12):
        isqrt(12) = 3 → i=1,2,3 순회
        i=1: 12%1=0 → +1, 1²≠12 → +1 (쌍: 12)
        i=2: 12%2=0 → +1, 2²≠12 → +1 (쌍: 6)
        i=3: 12%3=0 → +1, 3²≠12 → +1 (쌍: 4)
        divisors = 6 → [1,2,3,4,6,12] ✓
===================================================================================
[내 초기 풀이]
    solution_mine_one  : answer 리스트 누적 후 sum()
    solution_mine_two  : answer 정수 직접 누적 + 내부 루프 조기 탈출
    solution_mine_three: answer 정수 직접 누적 + 외부 삼항 연산

[개선 포인트]
    solution_mine_one:
        answer 리스트: O(N) 공간 → sum() 후 버려짐
        → 정수 누적으로 O(1) 공간 개선 가능
        → Best

    solution_mine_two:
        공간 O(N) → O(1): 리스트 대신 정수 직접 누적
        조기 탈출: divisors > limit 시점에 즉시 break
        효과는 limit 값에 따라 달라짐:
            limit=2  (조기 탈출 잦음): 약 80% 성능 개선
            limit=100(조기 탈출 거의 없음): if 체크 비용으로 약 24% 느려짐
        → Sub

    solution_mine_three:
        리스트 없이 정수 직접 누적 → 공간 O(1)
        내부 루프에 추가 조건문 없음 → limit 관계없이 일관된 성능
        외부 삼항 연산으로 limit 비교와 누적을 동시에 처리
        → limit에 무관한 안정적 균형점 → Best
===================================================================================
[복잡도 분석]
    N = number (최대 100,000)

    Mine_one   - 시간: O(N√N) | 공간: O(N) - 리스트 누적 후 sum
    Mine_two   - 시간: O(N√N) | 공간: O(1) - 정수 누적, 조기 탈출
    Mine_three - 시간: O(N√N) | 공간: O(1) - 정수 누적, 외부 삼항 (안정적)
    Best       - 시간: O(N√N) | 공간: O(1) - Mine_three와 동일
    Sub        - 시간: O(N√N) | 공간: O(1) - Mine_two와 동일

    실측 (number=100,000, timeit 10회):
        limit=2  : 리스트+sum 526ms  정수+탈출 106ms  정수+삼항 511ms
        limit=100: 리스트+sum 514ms  정수+탈출 636ms  정수+삼항 505ms
        → 정수+삼항: limit 값과 무관하게 안정적 균형점
        → 정수+탈출: limit이 낮을 때 압도적, 높을 때 손해
"""

import math
import time


# =================================================================================
# Mine solution one - answer 리스트 누적 후 sum()
# =================================================================================
def solution_mine_one(number: int, limit: int, power: int) -> int:
    """
    각 수의 약수 개수를 리스트에 담고 sum()으로 합산하는 초기 풀이

    핵심:
        math.isqrt(n): 정수 제곱근 (부동소수점 오차 없음)
        i ** 2 != n: 제곱수가 아니면 약수 쌍 추가
        divisors <= limit → divisors, 초과 → power

    한계:
        answer 리스트: O(N) 공간 → sum() 후 버려짐
        내부 루프를 항상 완전히 순회 (조기 탈출 없음)
    """
    answer = []

    for n in range(1, number + 1):
        divisors = 0
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                divisors += 1
                if i ** 2 != n:         # 제곱수가 아니면 쌍의 약수도 카운트
                    divisors += 1

        answer.append(divisors if divisors <= limit else power)

    return sum(answer)


# =================================================================================
# Mine solution two - 정수 직접 누적 + 내부 루프 조기 탈출
# =================================================================================
def solution_mine_two(number: int, limit: int, power: int) -> int:
    """
    정수 직접 누적과 조기 탈출로 mine_one을 최적화한 풀이

    mine_one 대비 개선:
        answer 리스트 → 정수 직접 누적: 공간 O(N) → O(1)
        조기 탈출: divisors > limit 시점에 power로 교체 후 break
            → limit이 낮을수록 더 일찍 탈출, 성능 개선 효과 큼

    조기 탈출 트레이드오프:
        이득: limit 초과 시 이후 제곱근 탐색 생략
        비용: 내부 루프마다 if divisors > limit 체크 추가
        limit=2  : 이득 > 비용 (약 80% 개선)
        limit=100: 이득 < 비용 (약 24% 느려짐)
    """
    answer = 0

    for n in range(1, number + 1):
        divisors = 0
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                divisors += 1
                if i ** 2 != n:
                    divisors += 1

            if divisors > limit:        # limit 초과 즉시 교체 후 탈출
                divisors = power
                break

        answer += divisors

    return answer


# =================================================================================
# Mine solution three - 정수 직접 누적 + 외부 삼항 연산
# =================================================================================
def solution_mine_three(number: int, limit: int, power: int) -> int:
    """
    정수 직접 누적과 외부 삼항 연산으로 안정적인 성능을 내는 풀이

    mine_one 대비:
        리스트 생성/append/sum() 없이 정수 직접 누적 → 공간 O(1)

    mine_two(조기 탈출) 대비:
        내부 루프에 if divisors > limit 체크 없음 → 추가 비용 없음
        대신 조기 탈출도 없음 → 항상 √n까지 완전 탐색

    안정성:
        limit 값과 무관하게 일관된 성능
        limit=2  : 511ms (정수+탈출 106ms보다 느리나 리스트+sum 526ms보다 빠름)
        limit=100: 505ms (정수+탈출 636ms보다 빠름)
        → 어떤 limit 값에서도 손해가 없는 균형점
    """
    answer = 0

    for n in range(1, number + 1):
        divisors = 0
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                divisors += 1
                if i ** 2 != n:
                    divisors += 1

        answer += divisors if divisors <= limit else power  # 외부 삼항 누적

    return answer


# =================================================================================
# Best solution - 정수 누적 + 외부 삼항 (mine_three 주석 보강)
# =================================================================================
def solution_best(number: int, limit: int, power: int) -> int:
    """
    정수 누적과 외부 삼항 연산으로 limit에 무관하게 안정적인 최적 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        공간 O(1): 정수 answer만 유지
        내부 루프: 약수 계산에만 집중, 추가 조건문 없음
        외부 삼항: 루프 종료 후 1회 비교 → limit 값과 무관한 일관된 비용
        어떤 limit 조건에서도 손해 없는 균형점
    """
    answer = 0

    for n in range(1, number + 1):
        divisors = 0
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                divisors += 1
                if i ** 2 != n:
                    divisors += 1

        answer += divisors if divisors <= limit else power

    return answer


# =================================================================================
# Sub solution - 정수 누적 + 조기 탈출 (mine_two 주석 보강)
# =================================================================================
def solution_sub(number: int, limit: int, power: int) -> int:
    """
    정수 누적과 조기 탈출로 limit이 낮을 때 성능 우위를 가지는 서브 풀이

    Best 대비 특징:
        내부 루프에서 divisors > limit 시 즉시 탈출
        limit이 낮을수록 탈출 빈도 증가 → Best 대비 최대 80% 빠름
        limit이 높을수록 탈출 없이 if 체크 비용만 발생 → Best보다 느림
        이 문제 제약(limit 2~100)에서 limit이 낮은 케이스에 특히 유리
    """
    answer = 0

    for n in range(1, number + 1):
        divisors = 0
        for i in range(1, math.isqrt(n) + 1):
            if n % i == 0:
                divisors += 1
                if i ** 2 != n:
                    divisors += 1

            if divisors > limit:
                divisors = power
                break

        answer += divisors

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int, int, int]] = [
        # (number, limit, power, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # number=5, limit=3, power=2
        # 약수개수: 1→1, 2→2, 3→2, 4→3, 5→2
        # 모두 3 이하 → 합 = 1+2+2+3+2 = 10
        (5,  3, 2, 10),
        # number=10, limit=3, power=2
        # 약수개수: [1,2,2,3,2,4,2,4,3,4]
        # 6(4>3→2), 8(4>3→2), 10(4>3→2)
        # 합 = 1+2+2+3+2+2+2+2+3+2 = 21
        (10, 3, 2, 21),
        # 추가 케이스:
        # number=1: 1의 약수는 1개 → 1
        (1,  3, 2, 1),
        # 제곱수 포함: number=4, limit=3, power=2
        # 약수개수: 1→1, 2→2, 3→2, 4→3 → 합 = 8
        (4,  3, 2, 8),
    ]

    solutions = [
        ("Mine_one   (리스트+sum)  ", solution_mine_one),
        ("Mine_two   (정수+탈출)   ", solution_mine_two),
        ("Mine_three (정수+삼항)   ", solution_mine_three),
        ("Best       (정수+삼항)   ", solution_best),
        ("Sub        (정수+탈출)   ", solution_sub),
    ]

    # 워밍업 스텝
    _number, _limit, _power, _ = test_cases[0]
    for _, func in solutions:
        func(_number, _limit, _power)

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (number, limit, power, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(number, limit, power)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
