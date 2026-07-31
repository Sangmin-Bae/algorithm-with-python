"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 평균 구하기
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12944
    풀이일자   : 2026-07-31
===================================================================================
[문제 요약]
    정수 배열 arr의 평균값 반환

    제약 조건
        - arr 길이: 1 이상 100 이하 (빈 배열 없음)
        - arr 원소: -10,000 이상 10,000 이하 정수
===================================================================================
[입출력 예시]
    arr       | return
    ----------|-------
    [1,2,3,4] | 2.5
    [5,5]     | 5
===================================================================================
[5.0 vs 5 반환 타입 문제]
    입출력 예시에서 [5,5]의 return이 5(정수)로 표기됨
    Python의 / 연산은 항상 float 반환 → 5.0이 반환됨

    프로그래머스 채점 방식:
        Python에서 5.0 == 5 → True
        float 5.0과 int 5를 동등하게 처리
        → solution_one(5.0 반환)도 정확히 통과

    is_integer() 분기 방어:
        지문 예시 표기에 맞춰 int/float을 분리하는 시도
        프로그래머스 채점에서 실질적으로 불필요
        제약 조건("길이 1 이상")에 보장된 빈 배열 예외처리도 불필요
        알고리즘 문제에서 과도한 방어는 복잡성만 증가

[두 풀이 성능 비교]
    sum(arr) / len(arr): O(N) 합산 + O(1) 나눗셈
    is_integer() 분기:  O(N) 합산 + O(1) 나눗셈 + O(1) is_integer + O(1) 분기
    → 성능 차이 없음 (사실상 동일)
    → 2순위 기준(가독성)으로 Best 결정 → solution_one 우위
===================================================================================
[내 초기 풀이]
    solution_mine_one: sum(arr) / len(arr) (가장 간결)
    solution_mine_two: 빈 배열 예외처리 + is_integer() 분기 (과도한 방어)

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       간결하고 정확, 5.0 == 5 동등 처리로 채점 통과
                       제약 조건 보장을 신뢰하는 적절한 방어 수준
    solution_mine_two: 과도한 방어 - Sub
                       빈 배열: 제약 조건에서 보장, 불필요한 분기
                       is_integer(): 채점에서 불필요, 복잡성만 증가
                       함수명 오타(solution → solution_mine_two) 교정 필요

    선정 기준:
        성능 차이 없음 → 2순위 가독성 기준
        solution_one이 간결하고 의도 명확 → Best
===================================================================================
[복잡도 분석]
    N = len(arr) (최대 100)

    Mine_one - 시간: O(N) | 공간: O(1) - sum 순회 + 나눗셈
    Mine_two - 시간: O(N) | 공간: O(1) - sum 순회 + 나눗셈 + is_integer
    Best     - 시간: O(N) | 공간: O(1) - Mine_one과 동일
    Sub      - 시간: O(N) | 공간: O(1) - Mine_two와 동일
"""

import time


# =================================================================================
# Mine solution one - sum(arr) / len(arr)
# =================================================================================
def solution_mine_one(arr: list[int]) -> float:
    """
    배열 합을 원소 수로 나눠 평균을 구하는 초기 풀이

    sum(arr) / len(arr):
        sum(arr): O(N) 전체 합산
        len(arr): O(1) 길이
        /: Python 나눗셈은 항상 float 반환

    5.0 vs 5:
        [5,5] → 5.0 반환
        프로그래머스 채점에서 5.0 == 5 → True로 처리
        → 정확히 통과

    ZeroDivisionError:
        제약 조건 "arr 길이 1 이상" 보장
        → len(arr) == 0 불가능 → 방어 불필요
    """
    return sum(arr) / len(arr)


# =================================================================================
# Mine solution two - 빈 배열 예외처리 + is_integer() 분기
# =================================================================================
def solution_mine_two(arr: list[int]) -> int | float:
    """
    빈 배열 예외처리와 is_integer()로 int/float을 분기하는 풀이

    if not arr: return 0
        제약 조건에서 보장된 경우를 방어
        알고리즘 문제에서 불필요한 복잡성
        실무 코드라면 적절하나 코딩테스트에서 과도한 방어

    is_integer():
        float.is_integer(): 소수점 이하가 0인지 확인
        5.0.is_integer() → True → int(5.0) = 5
        2.5.is_integer() → False → 2.5 그대로 반환

    프로그래머스 채점에서 실질적으로 불필요:
        5.0 == 5 → True로 처리되어 solution_one과 동일하게 통과
    """
    if not arr:
        return 0

    avg = sum(arr) / len(arr)
    return int(avg) if avg.is_integer() else avg


# =================================================================================
# Best solution - sum / len (mine_one 주석 보강)
# =================================================================================
def solution_best(arr: list[int]) -> float:
    """
    배열 합을 원소 수로 나눠 평균을 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        성능 차이 없음 → 2순위 가독성 기준으로 선정
        한 줄로 평균 공식을 직접 표현
        제약 조건 보장을 신뢰 → 불필요한 예외처리 없음
        float 반환도 채점에서 정확히 통과
    """
    return sum(arr) / len(arr)


# =================================================================================
# Sub solution - is_integer() 분기 (mine_two 주석 보강)
# =================================================================================
def solution_sub(arr: list[int]) -> int | float:
    """
    is_integer()로 반환 타입을 분기하는 서브 풀이

    Best 대비 특징:
        입출력 예시 표기(5 vs 2.5)에 맞춰 int/float 명시적 분리
        float.is_integer(): 소수점 이하 0 여부 확인
        코딩테스트에서 불필요하나 반환 타입을 엄밀하게 맞추려는 의도

    과도한 방어 포인트:
        if not arr: 제약 조건 보장으로 불필요
        is_integer() 분기: 5.0 == 5 처리로 실질적 불필요
    """
    if not arr:
        return 0

    avg = sum(arr) / len(arr)
    return int(avg) if avg.is_integer() else avg


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], float | int]] = [
        # (arr, 기댓값)
        # 공식 예시 — 기댓값을 float로 통일 (5.0 == 5 Python 동등 처리)
        ([1, 2, 3, 4], 2.5),
        ([5, 5],       5.0),
        # 추가 케이스:
        ([1],          1.0),    # 단일 원소
        ([-1, 1],      0.0),    # 합이 0
        ([10000] * 100, 10000.0),  # 최대 원소 최대 개수
    ]

    solutions = [
        ("Mine_one (sum/len)    ", solution_mine_one),
        ("Mine_two (is_integer) ", solution_mine_two),
        ("Best     (sum/len)    ", solution_best),
        ("Sub      (is_integer) ", solution_sub),
    ]

    # 워밍업 스텝
    _a, _ = test_cases[0]
    for _, func in solutions:
        func(_a[:])

    print("=" * 62)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 62)

    for name, func in solutions:
        for idx, (arr, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 62)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
