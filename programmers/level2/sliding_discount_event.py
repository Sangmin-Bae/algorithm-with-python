"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 할인 행사
    유형       : 슬라이딩 윈도우 (Sliding Window)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/131127
    풀이일자   : 2026-06-06
================================================================================
[문제 요약]
    정현이는 할인 행사 기간 동안 연속된 10일 안에
    원하는 제품(want)이 원하는 수량(number)만큼 할인될 경우 회원가입을 할 수 있음
    할인 일정(discount)이 주어질 때, 회원가입이 가능한 시작일의 수를 반환

    제약 조건
        - 1 ≤ len(want) ≤ 10
        - 1 ≤ number[i] ≤ 10  →  number 합계 최대 100 (10일 안에 담김을 보장)
        - 10 ≤ len(discount) ≤ 10,000
================================================================================
[입출력 예시]
    want        |   number  | discount (20개)                               | return
    ------------|-----------|-----------------------------------------------|-------
    참조 아래   | 참조 아래 | chicken apple apple banana rice apple chicken | 3
                |           | banana rice pork banana apple banana pork     |
                |           | rice banana chicken rice apple banana         |

    want   = ["banana", "apple", "rice", "pork", "pot"]
    number = [3, 2, 2, 2, 1]
================================================================================
[내 초기 풀이]
    solution_mine_one: want 원소마다 list.count()로 빈도 비교, 불일치 시 early exit
    solution_mine_two: Counter로 윈도우 빈도 집계 후 table 딕셔너리와 직접 비교

    발상 진화:
        1단계(mine_one): table 딕셔너리 + list.count() 반복 비교, flag + break 구조
        2단계(mine_two): Counter 도입으로 count() 반복 제거, 딕셔너리와 직접 비교

[개선 포인트]
    solution_mine_two:
        table이 dict, Counter(discount[...])가 Counter → 타입 불일치
        Python Counter.__eq__ 가 dict와의 비교도 처리하므로 기능상 동작하지만
        명시적으로 table도 Counter로 만들면 타입 일관성 확보 및 의도 명확화
================================================================================
[슬라이딩 윈도우 원리]
    크기 10의 윈도우를 discount 리스트 위에서 1칸씩 이동하며
    각 구간의 제품 빈도와 want-number 조건을 비교

    가능한 시작점: 0 ~ len(discount) - 10
        → range(len(discount) - 9) = range(0, len(discount) - 10 + 1)
            마지막 시작점 포함을 위해 -10 + 1 = -9

    예시:
        discount = [c, a, a, b, r, a, c, b, r, p, b, a, b, p, r, b, c, r, a, b]
                   [<--------- i=0, 10일 윈도우 --------->]
                      [<--------- i=1, 10일 윈도우 --------->]
================================================================================
[복잡도 분석]
    N = len(discount) ≤ 10,000
    W = len(want)     ≤ 10
    윈도우 크기 = 10 (고정)

    Mine_one - 시간: O(N × W × 10) | 공간: O(W) — want 원소마다 count() 반복
    Mine_two - 시간: O(N × 10)     | 공간: O(W) — Counter 1회 집계
    Best     - 시간: O(N × 10)     | 공간: O(W) — Counter 1회 집계 (타입 일관성)
    Sub      - 시간: O(N × W × 10) | 공간: O(W) — early exit 방식 명시

    solution_best : Counter() 1회 O(10) → 최대 100,000번 연산
    solution_sub  : list.count() W회 × O(10) → 최대 1,000,000번 연산
================================================================================
"""

import time
from collections import Counter
from typing import List, Tuple


# ==============================================================================
# Mine solution one — want 원소마다 count() 비교 + early exit
# ==============================================================================
def solution_mine_one(want: List[str], number: List[int], discount: List[str]) -> int:
    """
    want, number를 딕셔너리로 결합한 뒤,
    10일 윈도우마다 want 원소별로 list.count()로 빈도를 직접 비교

    핵심:
        불일치 발생 즉시 break로 조기 탈출 → 불필요한 연산 절감
        ten_days.count(w): ten_days 리스트를 처음부터 끝까지 순회 O(10)

    개선 가능:
        want 원소 수(W)만큼 count() 반복 호출 → 중복 순회 발생
        Counter로 1회 집계 후 비교하면 순회 횟수 절감 가능
    """
    # want, number를 key: value 딕셔너리로 결합
    table = {key: value for key, value in zip(want, number)}

    answer = 0
    for i in range(len(discount) - 9):
        flag = True
        ten_days = discount[i:i + 10]
        for w in want:
            # 원하는 수량과 실제 할인 횟수가 다르면 조기 탈출
            if table[w] != ten_days.count(w):
                flag = False
                break
        if flag:
            answer += 1

    return answer


# ==============================================================================
# Mine solution two — Counter 집계 후 dict 직접 비교
# ==============================================================================
def solution_mine_two(want: List[str], number: List[int], discount: List[str]) -> int:
    """
    Counter로 10일 윈도우 빈도를 1회 집계한 뒤 table 딕셔너리와 직접 비교

    핵심:
        Counter(list): 리스트를 단 1회 순회해 모든 원소 빈도 집계
        dict == Counter 비교는 Python 내부적으로 Counter.__eq__ 호출
        → 값이 같으면 True 반환 (기능상 정상 동작)

    개선 가능:
        table이 dict, Counter(discount[...])가 Counter → 타입 불일치
        명시적으로 table도 Counter로 만들면 타입 일관성 확보
    """
    # want, number를 key: value 딕셔너리로 결합
    table = {key: value for key, value in zip(want, number)}

    answer = 0
    for i in range(len(discount) - 9):
        # Counter로 10일 구간 빈도 집계 후 table과 직접 비교
        if table == Counter(discount[i:i + 10]):
            answer += 1

    return answer


# ==============================================================================
# Best solution — Counter 타입 일관성 확보
# ==============================================================================
def solution_best(want: List[str], number: List[int], discount: List[str]) -> int:
    """
    table도 Counter로 생성해 타입 일관성을 확보한 최적 풀이

    Mine_two 대비 개선:
        Counter(dict(zip(want, number)))로 table을 Counter 타입으로 생성
        → 비교 양쪽 모두 Counter로 타입 일관성 확보
        → 의도를 명확히 표현

    Counter 비교 원리:
        Counter.__eq__: 두 Counter의 key-value가 모두 동일할 때 True
        want에 없는 제품이 discount에 포함되면 key 불일치 → False
    """
    # table을 Counter로 생성해 타입 일관성 확보
    table = Counter(dict(zip(want, number)))

    answer = 0
    for i in range(len(discount) - 9):
        if table == Counter(discount[i:i + 10]):
            answer += 1

    return answer


# ==============================================================================
# Sub solution — early exit 방식 명시
# ==============================================================================
def solution_sub(want: List[str], number: List[int], discount: List[str]) -> int:
    """
    solution_mine_one과 동일 구조. early exit 방식의 명시적 비교

    Best 대비 특징:
        want 원소 수(W)만큼 count() 반복 호출 → O(N × W × 10)
        불일치 즉시 break → 최선의 경우 early exit 유리
        로직 흐름이 직관적으로 드러나 가독성 우위
    """
    table = {key: value for key, value in zip(want, number)}

    answer = 0
    for i in range(len(discount) - 9):
        flag = True
        ten_days = discount[i:i + 10]
        for w in want:
            if table[w] != ten_days.count(w):
                flag = False
                break
        if flag:
            answer += 1

    return answer


# ==============================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==============================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    want = ["banana", "apple", "rice", "pork", "pot"]
    number = [3, 2, 2, 2, 1]
    discount = [
        "chicken", "apple", "apple", "banana", "rice", "apple", "chicken",
        "banana", "rice", "pork", "banana", "apple", "banana", "pork",
        "rice", "banana", "chicken", "rice", "apple", "banana"
    ]

    test_cases: List[Tuple[List[str], List[int], List[str], int]] = [
        # (want, number, discount, 기댓값)
        # 손 계산:
        # i=0: [chicken,apple,apple,banana,rice,apple,chicken,banana,rice,pork]
        #   banana:2 ≠ want:3 → FAIL
        # i=3: [banana,rice,apple,chicken,banana,rice,pork,banana,apple,banana]
        #   banana:4 ≠ want:3 → FAIL
        # 정답 3개 구간은 20개 원소 전체 추적 필요
        # → 프로그래머스 공식 예시 기준 expected = 3
        (want, number, discount, 3),
    ]

    solutions = [
        ("Mine_one (count+early exit)", solution_mine_one),
        ("Mine_two (dict+Counter)    ", solution_mine_two),
        ("Best     (Counter+Counter) ", solution_best),
        ("Sub      (count+early exit)", solution_sub),
    ]

    print("=" * 72)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 72)

    for name, func in solutions:
        for idx, (w, n, d, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(w, n, d)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 72)


# ==============================================================================
# 실행 진입점
# ==============================================================================
if __name__ == "__main__":
    solution_comparison()
