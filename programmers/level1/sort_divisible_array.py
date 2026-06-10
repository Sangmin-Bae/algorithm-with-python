"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 나누어 떨어지는 숫자 배열
    유형       : Sort
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12910
    풀이일자   : 2026-06-10
===================================================================================
[문제 요약]
    arr에서 divisor로 나누어 떨어지는 원소만 추출해 오름차순 정렬 후 반환
    해당 원소가 없으면 [-1] 반환

    제약 조건
        - arr: 자연수 배열, 길이 1 이상, 중복 없음 (i≠j이면 arr[i]≠arr[j])
        - divisor: 자연수
===================================================================================
[입출력 예시]
    arr           | divisor | return
    --------------|---------|-------
    [5, 9, 7, 10] | 5       | [5, 10]       (5%5=0, 10%5=0)
    [2, 36, 1, 3] | 1       | [1, 2, 3, 36] (모든 원소 1로 나누어 떨어짐)
    [3, 2, 6]     | 10      | [-1]          (나누어 떨어지는 원소 없음)
===================================================================================
[내 초기 풀이]
    solution_mine_one: for 루프 + 조건 필터링 + 명시적 반환
        조건 필터링 → answer 리스트 누적 → 정렬 → 빈 경우 [-1] 반환
        문제 요구사항을 순차적으로 적용한 명시적 구조

    solution_mine_two: 리스트 컴프리헨션 + or 단락 평가
        solution_mine_one을 파이써닉하게 변환
        answer 변수 제거, 리스트 컴프리헨션으로 필터링과 순회를 원라인 표현
        빈 리스트 처리: sorted([]) → falsy → or 우측 피연산자 [-1] 반환

[개선 포인트]
    solution_mine_one: 개선 필요 없음
                        단, sorted(answer) if answer else [-1] 대신
                        sorted(answer) or [-1] 로도 표현 가능 (mine_two 방식)
    solution_mine_two: 개선 필요 없음 - Best
===================================================================================
[or 단락 평가 (Short-circuit Evaluation)]
    Python or 연산자: 좌측 피연산자가 truthy이면 좌측 반환, falsy이면 우측 반환

    피연산자(operand): 연산자 앞뒤의 요소를 지칭하는 공식 용어
        좌측 피연산자 (left operand) : sorted([...])
        우측 피연산자 (right operand): [-1]

    동작:
        sorted([5, 10]) or [-1] → [5, 10]  (비어 있지 않은 리스트 → truthy → 좌측 반환)
        sorted([])      or [-1] → [-1]     (빈 리스트 → falsy → 우측 반환)

    Python falsy 값: False, None, 0, 0.0, "", [], {}, set() 등 "비어 있거나 없음"
    sorted()는 한 번만 실행되고 그 결과가 or의 좌측 피연산자로 평가됨
    → 이중 실행 우려 없음
===================================================================================
[복잡도 분석]
    N = len(arr)
    K = divisor로 나누어 떨어지는 원소 수 (K ≤ N)

    Mine_one - 시간: O(N + K log K) | 공간: O(K) - 필터링 O(N) + 정렬 O(K log K)
    Mine_two - 시간: O(N + K log K) | 공간: O(K) - 컴프리헨션 O(N) + 정렬 O(K log K)
    Best     - 시간: O(N + K log K) | 공간: O(K) - Mine_two와 동일, 주석 보강
    Sub      - 시간: O(N + K log K) | 공간: O(K) - Mine_one과 동일, 주석 보강

    두 풀이 시간/공간 복잡도 동일, 차이는 가독성과 코드 길이뿐
    K log K ≤ N log N → 정렬이 지배하나 필터링 후 K ≤ N이므로 실질적으로 빠름
"""

import time
from typing import List, Tuple


# =================================================================================
# Mine solution one - for 루프 + 명시적 필터링
# =================================================================================
def solution_mine_one(arr: List[int], divisor: int) -> List[int]:
    """
    for 루프로 조건을 필터링해 누적하고 명시적으로 반환하는 초기 풀이

    핵심:
        i % divisor == 0: divisor로 나누어 떨어지는지 나머지 연산으로 확인
        sorted(answer) if answer else [-1]: 삼항 연산자로 빈 경우 처리

    개선 가능:
        sorted(answer) if answer else [-1]
        → sorted(answer) or [-1]  (빈 리스트 falsy 활용, mine_two 방식)
    """
    answer = []

    for i in arr:
        if i % divisor == 0:        # 나머지가 0 = divisor로 나누어 떨어짐
            answer.append(i)

    return sorted(answer) if answer else [-1]   # 빈 리스트면 [-1] 반환


# =================================================================================
# Mine solution two - 리스트 컴프리헨션 + or 단락 평가
# =================================================================================
def solution_mine_two(arr: List[int], divisor: int) -> List[int]:
    """
    리스트 컴프리헨션과 or 단락 평가로 mine_one을 파이써닉하게 변환한 풀이

    mine_one 대비 개선:
        answer 변수 제거
        for 루프 + if + append → 리스트 컴프리헨션 원라인 표현
        삼항 연산자 → or 단락 평가로 교체

    or 동작:
        sorted([5, 10]) or [-1] → [5, 10]  (truthy → 좌측 피연산자 반환)
        sorted([])      or [-1] → [-1]     (falsy  → 우측 피연산자 반환)
    """
    return sorted([i for i in arr if i % divisor == 0]) or [-1]


# =================================================================================
# Best solution - mine_two 주석 보강
# =================================================================================
def solution_best(arr: List[int], divisor: int) -> List[int]:
    """
    리스트 컴프리헨션 + or 단락 평가로 간결하게 표현한 최적 풀이

    mine_two와 동일한 로직, 근거 주석 보강:
        [i for i in arr if i % divisor == 0]: 조건 필터링 + 순회 원라인 표현
        sorted(...): 오름차순 정렬, 결과가 빈 리스트면 falsy
        or [-1]: 좌측이 falsy(빈 리스트)일 때 [-1] 반환

    단락 평가 원리:
        Python or는 좌측 피연산자가 truthy이면 즉시 좌측 반환 (우측 미평가)
        → sorted()는 단 한 번만 실행됨
    """
    return sorted([i for i in arr if i % divisor == 0]) or [-1]


# =================================================================================
# Sub solution - for 루프 + 명시적 필터링 (mine_one 주석 보강)
# =================================================================================
def solution_sub(arr: List[int], divisor: int) -> List[int]:
    """
    for 루프로 각 단계를 명시적으로 분리한 서브 풀이

    Best 대비 특징:
        각 단계(필터링 → 누적 → 정렬 → 반환)가 분리되어 가독성 우위
        중간 상태(answer 리스트)를 변수로 확인 가능 → 디버깅 용이
        코드 길이는 길지만 로직 흐름이 직관적으로 드러남
    """
    answer = []

    for i in arr:
        if i % divisor == 0:
            answer.append(i)

    return sorted(answer) or [-1]   # or 단락 평가로 빈 경우 처리


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], int, List[int]]] = [
        # (arr, divisor, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [5,9,7,10], divisor=5: 5%5=0 ✓, 9%5=4, 7%5=2, 10%5=0 ✓ → sorted([5,10])=[5,10]
        ([5, 9, 7, 10],  5,  [5, 10]),
        # [2,36,1,3], divisor=1: 모든 자연수 % 1 = 0 → sorted([2,36,1,3])=[1,2,3,36]
        ([2, 36, 1, 3],  1,  [1, 2, 3, 36]),
        # [3,2,6], divisor=10: 3%10=3, 2%10=2, 6%10=6 → 없음 → [-1]
        ([3, 2, 6],      10, [-1]),
        # 추가 케이스:
        # [1], divisor=2: 1%2=1 → 없음 → [-1]
        ([1],            2,  [-1]),
        # [4,8,12], divisor=4: 4%4=0, 8%4=0, 12%4=0 → sorted([4,8,12])=[4,8,12]
        ([4, 8, 12],     4,  [4, 8, 12]),
        # [7], divisor=7: 7%7=0 → [7]
        ([7],            7,  [7]),
    ]

    solutions = [
        ("Mine_one (for+명시적)  ", solution_mine_one),
        ("Mine_two (컴프리헨션)  ", solution_mine_two),
        ("Best     (컴프리헨션)  ", solution_best),
        ("Sub      (for+명시적)  ", solution_sub),
    ]

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (arr, divisor, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr[:], divisor)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
