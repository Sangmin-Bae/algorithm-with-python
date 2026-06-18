"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 의상
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42578
    풀이일자   : 2026-06-18
================================================================================
[문제 요약]
    의상 종류별로 최대 1가지만 착용 가능할 때 서로 다른 옷의 조합의 수 반환
    최소 한 가지 의상은 반드시 착용

    제약 조건
        - clothes 행: [의상 이름, 의상 종류]
        - 의상 수: 1 이상 30 이하
        - 같은 이름의 의상 없음 (중복 없음)
================================================================================
[입출력 예시]
    clothes                                                                               | return
    --------------------------------------------------------------------------------------|-------
    [["yellow_hat","headgear"],["blue_sunglasses","eyewear"],["green_turban","headgear"]] | 5
    [["crow_mask","face"],["blue_sunglasses","face"],["smoky_makeup","face"]]             | 3
================================================================================
[핵심 수학 — 경우의 수]
    각 의상 종류에서 "1가지 선택 또는 미선택"으로 독립적 경우의 수 계산:
        종류별 경우의 수 = 해당 종류 의상 개수 + 1 (미선택 1가지 추가)
        전체 경우의 수  = 각 종류별 경우의 수의 곱
        최소 1가지 착용 = 전체 경우의 수 - 1 (모두 미선택인 경우 제외)

    손 추적 (예제 1):
        headgear: yellow_hat, green_turban → 2개 → 2+1=3 (선택 2 + 미선택 1)
        eyewear:  blue_sunglasses          → 1개 → 1+1=2 (선택 1 + 미선택 1)
        전체: 3 × 2 = 6
        최소 1가지 조건: 6 - 1 = 5 ✓

    검증:
        headgear만: yellow_hat, green_turban             → 2가지
        eyewear만:  blue_sunglasses                      → 1가지
        둘 다:      yellow_hat+blue, green_turban+blue   → 2가지
        합계: 5 ✓

    손 추적 (예제 2):
        face: crow_mask, blue_sunglasses, smoky_makeup → 3개 → 3+1=4
        전체: 4 - 1 = 3 ✓
================================================================================
[내 초기 풀이]
    solution_mine_one: if/else + in 연산자로 dict 집계, for 루프로 곱셈

    핵심 판단:
        같은 이름의 의상 없음 → 의상 이름은 집계에서 불필요
        종류별 개수만 알면 경우의 수 계산 가능
        → clothes[i][1](의상 종류)만 key로 사용

    4가지 풀이 진화:
        mine_one  : if/else + in 연산자 dict 집계, for 루프 곱셈
        mine_two  : dict.get(key, 0) dict 집계, math.prod() 곱셈
        mine_three: dict.get(key, 0) dict 집계, functools.reduce() 곱셈
        mine_four : Counter + math.prod() 한 줄 표현

[개선 포인트]
    solution_mine_one:
        if c[1] in table / else → dict.get(kind, 0) + 1로 조건문 제거
        for 루프 곱셈 → math.prod() 또는 reduce()로 간결하게

    solution_mine_two/three: 개선 필요 없음
    solution_mine_four: 개선 필요 없음 - Best

    Counter(clothes) 오류 주의:
        Counter(clothes): ["의상명", "종류"] 리스트가 unhashable → TypeError
        Counter(c[1] for c in clothes): c[1]만 추출한 제너레이터 전달 → 정상 동작
================================================================================
[math.prod vs functools.reduce 비교]
    math.prod(iterable):
        Python 3.8+ 내장 수학 함수
        이터러블 원소들의 곱을 반환
        간결하고 의도가 명확

    functools.reduce(func, iterable, initializer):
        (함수, 이터러블, 초기값) 구조
        이터러블을 순차적으로 누적 연산
        초기값으로 1을 주어 곱셈 초기화

    reduce 손 추적 ([2,1] → 각 +1 후 곱):
        초기값=1, values=[2,1]
        step1: x=1, y=2 → 1*(2+1)=3
        step2: x=3, y=1 → 3*(1+1)=6
        결과: 6 → 6-1=5 ✓

    math.prod(v+1 for v in [2,1]):
        (2+1)*(1+1) = 3*2 = 6 → 6-1=5 ✓
================================================================================
[복잡도 분석]
    N = len(clothes) (최대 30)
    K = 의상 종류 수 (K ≤ N)

    Mine_one   - 시간: O(N+K) | 공간: O(K) - dict 집계 O(N) + for 곱셈 O(K)
    Mine_two   - 시간: O(N+K) | 공간: O(K) - dict 집계 O(N) + prod O(K)
    Mine_three - 시간: O(N+K) | 공간: O(K) - dict 집계 O(N) + reduce O(K)
    Mine_four  - 시간: O(N+K) | 공간: O(K) - Counter O(N) + prod O(K)
    Best       - 시간: O(N+K) | 공간: O(K) - Mine_four와 동일, 주석 보강
    Sub        - 시간: O(N+K) | 공간: O(K) - Mine_two와 동일, 주석 보강

    N ≤ 30 고정 → 모든 풀이 실질적으로 O(1)에 수렴
"""

import math
import time
from collections import Counter
from functools import reduce
from typing import List, Tuple


# ================================================================================
# Mine solution one - if/else + in 연산자 + for 루프 곱셈
# ================================================================================
def solution_mine_one(clothes: List[List[str]]) -> int:
    """
    if/else와 in 연산자로 dict를 집계하고 for 루프로 곱셈하는 초기 풀이

    핵심:
        c[1]: 의상 종류 (의상 이름 c[0]은 집계에서 불필요)
        table[c[1]] += 1: 종류별 개수 누적
        answer *= v + 1: 각 종류에서 미선택 1가지 추가 후 곱셈
        return answer - 1: 모두 미선택인 경우 제외

    개선 가능:
        if/else + in 연산자 → dict.get(kind, 0) + 1로 조건문 제거
        for 루프 곱셈 → math.prod()로 간결하게
    """
    answer = 1
    table = {}

    for c in clothes:
        if c[1] in table:
            table[c[1]] += 1
        else:
            table[c[1]] = 1             # key 없으면 1로 초기화

    for v in table.values():
        answer *= v + 1                 # 미선택 1가지 추가 후 곱

    return answer - 1                   # 모두 미선택 경우 제외


# ================================================================================
# Mine solution two - dict.get() + math.prod()
# ================================================================================
def solution_mine_two(clothes: List[List[str]]) -> int:
    """
    dict.get()으로 조건문을 제거하고 math.prod()로 곱셈을 간결하게 표현한 풀이

    mine_one 대비 개선:
        if/else → dict.get(kind, 0) + 1
            key 없으면 0 반환 → 0+1=1로 초기화, 있으면 기존값+1
        for 루프 곱셈 → math.prod(v+1 for v in table.values())
            제너레이터 표현식으로 +1 연산 포함해서 직접 전달
    """
    table = {}
    for c in clothes:
        kind = c[1]
        table[kind] = table.get(kind, 0) + 1   # key 없으면 0, 있으면 기존값

    return math.prod(v + 1 for v in table.values()) - 1


# ================================================================================
# Mine solution three - dict.get() + functools.reduce()
# ================================================================================
def solution_mine_three(clothes: List[List[str]]) -> int:
    """
    dict.get() + reduce()로 곱셈을 누적 연산으로 표현한 풀이

    reduce(lambda x, y: x * (y + 1), table.values(), 1):
        초기값 1에서 시작
        각 value y에 대해 x * (y+1) 누적
        step1: x=1, y=첫번째값 → 1*(y+1)
        step2: x=이전결과, y=두번째값 → 이전결과*(y+1)
        ...

    math.prod 대비 특징:
        초기값을 명시적으로 지정 가능
        lambda로 +1 연산을 곱셈 함수 내부에 포함
        reduce가 축약 개념을 직접 표현
    """
    table = {}
    for c in clothes:
        kind = c[1]
        table[kind] = table.get(kind, 0) + 1

    return reduce(lambda x, y: x * (y + 1), table.values(), 1) - 1


# ================================================================================
# Mine solution four - Counter + math.prod() 한 줄
# ================================================================================
def solution_mine_four(clothes: List[List[str]]) -> int:
    """
    Counter와 math.prod()로 한 줄에 표현한 가장 파이써닉한 풀이

    Counter(c[1] for c in clothes):
        c[1](의상 종류)만 추출한 제너레이터를 Counter에 전달
        → {종류: 개수} 딕셔너리 자동 집계
        Counter(clothes) 불가: 리스트는 unhashable → TypeError

    math.prod(v+1 for v in Counter(...).values()):
        Counter values에 +1 추가 후 전체 곱셈
        중간 변수 없이 한 줄 표현
    """
    return math.prod(v + 1 for v in Counter(c[1] for c in clothes).values()) - 1


# ================================================================================
# Best solution - Counter + math.prod() (mine_four 주석 보강)
# ================================================================================
def solution_best(clothes: List[List[str]]) -> int:
    """
    Counter + math.prod()로 한 줄에 표현한 최적 풀이

    mine_four와 동일한 로직, 근거 주석 보강:
        의상 이름 불필요: 같은 이름 없음 → 종류별 개수만으로 경우의 수 계산 가능
        Counter: 해시 기반 O(1) 탐색으로 O(N) 집계
        math.prod: Python 3.8+ 내장 함수, C 레벨 구현으로 빠름
        -1: 모든 종류에서 아무것도 선택하지 않는 경우(전체 미선택) 제외
    """
    return math.prod(v + 1 for v in Counter(c[1] for c in clothes).values()) - 1


# ================================================================================
# Sub solution - dict.get() + math.prod() (mine_two 주석 보강)
# ================================================================================
def solution_sub(clothes: List[List[str]]) -> int:
    """
    dict.get()으로 집계하고 math.prod()로 곱셈하는 서브 풀이

    Best 대비 특징:
        Counter 없이 dict.get()으로 집계 과정을 명시적으로 표현
        table 변수가 중간 단계로 드러나 디버깅 용이
        Counter 내부 동작을 이해하는 학습 관점에서 유의미
    """
    table = {}
    for c in clothes:
        kind = c[1]
        table[kind] = table.get(kind, 0) + 1   # 종류별 개수 집계

    return math.prod(v + 1 for v in table.values()) - 1


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[List[str]], int]] = [
        # (clothes, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # headgear:2, eyewear:1 → (2+1)*(1+1)-1 = 3*2-1 = 5
        ([["yellow_hat","headgear"],["blue_sunglasses","eyewear"],["green_turban","headgear"]], 5),
        # face:3 → (3+1)-1 = 3
        ([["crow_mask","face"],["blue_sunglasses","face"],["smoky_makeup","face"]], 3),
        # 추가 케이스:
        # 의상 1개만: kind_a:1 → (1+1)-1 = 1
        ([["hat","headgear"]], 1),
        # 3종류: a:1, b:2, c:3 → (1+1)*(2+1)*(3+1)-1 = 2*3*4-1 = 23
        ([["a","top"],["b","bottom"],["c","bottom"],["d","shoes"],["e","shoes"],["f","shoes"]], 23),
    ]

    solutions = [
        ("Mine_one  (if/else+for)  ", solution_mine_one),
        ("Mine_two  (get+prod)     ", solution_mine_two),
        ("Mine_three(get+reduce)   ", solution_mine_three),
        ("Mine_four (Counter+prod) ", solution_mine_four),
        ("Best      (Counter+prod) ", solution_best),
        ("Sub       (get+prod)     ", solution_sub),
    ]

    print("=" * 70)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (clothes, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func([c[:] for c in clothes])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
