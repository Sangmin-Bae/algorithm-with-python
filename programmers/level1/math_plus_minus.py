"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 음양 더하기
    유형       : Math / Implementation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/76501
    풀이일자   : 2026-05-17
===================================================================================
[문제 요약]
    절대값 배열 absolutes와 부호 배열 signs가 주어질 때, signs[i]가 True이면
    absolutes[i]는 양수, False이면 음수
    실제 부호를 복원한 모든 정수의 합을 반환

    제약 조건
        - absolutes, signs의 길이 동일 보장 (1 이상 1,000 이하)
        - absolutes[i]: 1 이상 1,000 이하
===================================================================================
[입출력 예시]
    absolutes       | signs                 | return
    ----------------|-----------------------|----------
    [4, 7, 12]      | [True, False, True]     9
    [1, 2, 3]       | [False, False, True]    0
===================================================================================
[내 초기 풀이]
    solution_mine_one   : zip + 제너레이터 + 삼항 표현식 (1 if sign else -1)
    solution_mine_two   : zip + 명시적 반복 + values 리스트 누적 sum
    solution_mine_three : range(len) + 인덱스 접근 방식

    접근 발상:
        - 두 리스트 길이 동일 -> 인덱스 범위 초과 없음
        - zip()으로 동일 인덱스 원소를 튜플로 묶어 동시 순회
        - sign 조건에 따라 *1 또는 *-1 적용

[개선 포인트]
    - (1 if sign else -1) 곱셈 -> (absolute if sign else -absolute) 부호 직접 적용
        곱셈 연산 제거, 의도가 더 명확
    - solution_mine_two의 values 리스트 -> total 누적 변수로 교체
        공간복잡도 O(N) -> O(1) 개선
    - range(len) 방식은 인덱스가 목적일 때만 사용
        두 리스트 동시 순회는 zip이 의미상 더 자연스럽고 연산 횟수도 적음
===================================================================================
[풀이 전략]
    공통 핵심: signs[i] 기반 부호 복원 후 전체 합산

    Mine_one)   zip + 제너레이터 + (1 if sign else -1) 곱셈
    Mine_two)   zip + 명시적 반복 + values 리스트 누적
    Mine_three) range(len) + 인덱스 접근 + 제너레이터
    Best)       zip + 제너레이터 + 부호 직접 적용 (곱셈 제거)
    Sub)        zip + 명시적 반복 + total 변수 누적 (리스트 제거)
===================================================================================
[복잡도 분석]
    N = len(absolutes) = len(signs) (최대 1,000)

    Mine_one    - 시간: O(N) | 공간: O(1) - 제너레이터
    Mine_two    - 시간: O(N) | 공간: O(N) - values 리스트 생성
    Mine_three  - 시간: O(N) | 공간: O(1) - 제너레이터, 인덱스 접근 비용 추가
    Best        - 시간: O(N) | 공간: O(1) - 제너레이터, 곱셈 연산 제거
    Sub         - 시간: O(N) | 공간: O(1) - total 변수만 사용

    zip vs range(len) 실질 차이:
        시간복잡도 등급: 동일 O(N)
        연산 횟수: range(len)은 인덱스 참조 비용 추가
        -> 두 리스트 동시 순회 시 zip 우선
===================================================================================
"""

import time
from typing import List, Tuple

# =================================================================================
# Mine solution one - zip + 제너레이터 + 삼항 곱셈
# =================================================================================
def solution_mine_one(absolutes: List[int], signs: List[bool]) -> int:
    """
    zip으로 두 리스트를 동시 순회하고 삼항 표현식으로 부호를 곱하는 초기 풀이

    개선 전 상태:
        - (1 if sign else -1) 곱셈: 의도는 명확하나 곱셈 연산이 불필요하게 발생
        - 제너레이터 표현식으로 중간 리스트 생성은 이미 제거
    """
    return sum(absolute * (1 if sign else -1) for absolute, sign in zip(absolutes, signs))


# =================================================================================
# Mine solution two - zip + 명시적 반복 + values 리스트
# =================================================================================
def solution_mine_two(absolutes: List[int], signs: List[bool]) -> int:
    """
    명시적 반복문으로 단계를 분리한 풀이

    개선 전 상태:
        - values 리스트: 불필요한 O(N) 공간 사용
        - 로직 자체는 명확하나 중간 리스트가 낭비
    """
    values = []
    for absolute, sign in zip(absolutes, signs):
        if sign:
            values.append(absolute)         # 양수 그대로
        else:
            values.append(absolute * -1)    # 음수로 변환 후 추가
    return sum(values)


# =================================================================================
# Mine solution three - range(len) + 인덱스 접근
# =================================================================================
def solution_mine_three(absolutes: List[int], signs: List[bool]) -> int:
    """
    range(len)으로 인덱스를 생성해 두 리스트에 각각 접근하는 풀이

    특징:
        - zip 외의 접근법 탐색 목적으로 시도
        - 인덱스 접근 시 absolutes[idx], sings[idx] 두 번 참조 발생
        - 인덱스 자체가 필요 없는 상황에서 range(len) 사용은 비파이써닉
    """
    return sum(absolutes[idx] * (1 if signs[idx] else -1) for idx in range(len(absolutes)))


# =================================================================================
# Best solution - zip + 제너레이터 + 부호 직접 사용
# =================================================================================
def solution_best(absolutes: List[int], signs: List[bool]) -> int:
    """
    부호를 곱셈 없이 직접 적용해 연산을 최소화한 풀이

    Mine_one 대비 개선
        - (absolute * (1 if sign else -1)) -> (absolute if sign else -absolute)
        - 곱셈 연산 제거, 의도가 더 명확
        - 제너레이터로 중간 리스트 없이 바로 합산
    """
    # sign이 True이면 absolute 그래도, False면 음수 부호 적용
    return sum(absolute if sign else -absolute for absolute, sign in zip(absolutes, signs))


# =================================================================================
# Sub solution - zip + 명시적 반복 + total 누적 변수
# =================================================================================
def solution_sub(absolutes: List[int], signs: List[bool]) -> int:
    """
    명시적 반복문으로 total 변수에 직접 누적하는 풀이

    Mine_two 대비 개선:
        - values 리스트 제거 + total 변수로 교체
        - 공간복잡도 O(N) -> O(1)
        - 각 단계가 분리되어 디버깅 시 중간값 확인 용이
    """
    total = 0
    for absolute, sign in zip(absolutes, signs):
        total += absolute if sign else -absolute
    return total


# =================================================================================
# 다섯 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], List[bool], int]] = [
        # (absolutes, signs, 기댓값)
        ([4, 7, 12], [True, False, True], 9),   # 기본 예시 1
        ([1, 2, 3], [False, False, True], 0),   # 기본 예시 2
        ([1], [True], 1),                       # 단일 원소 양수
        ([1], [False], -1),                     # 단일 원소 음수
        ([5, 5], [True, False], 0),             # 합이 0
        ([1000], [True], 1000),                 # 최대 absolutes 값
        ([1, 1, 1], [False, False, False], -3), # 전부 음수
    ]

    solutions = [
        ("Mine_one   (zip + 곱셈)", solution_mine_one),
        ("Mine_two   (zip + 리스트)", solution_mine_two),
        ("Mine_three (range + idx)", solution_mine_three),
        ("Best       (zip + 부호직접)", solution_best),
        ("Sub        (zip + 누적변수)", solution_sub),
    ]

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (absolutes, signs, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(absolutes[:], signs[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)

# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
