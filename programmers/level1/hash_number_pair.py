"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 숫자 짝꿍
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/131128
    풀이일자   : 2026-09-14
===================================================================================
[문제 요약]
    X, Y의 공통 자리수(다중집합 교집합)로 만들 수 있는 가장 큰 정수 반환
    공통 자리수 없으면 '-1', 0으로만 구성되면 '0'

    제약 조건
        - X, Y 길이: 3 이상 3,000,000 이하
        - X, Y는 0으로 시작하지 않음
===================================================================================
[입출력 예시]
    X       | Y        | result
    --------|----------|-------
    "100"   | "2345"   | "-1"
    "100"   | "203045" | "0"
    "100"   | "123450" | "10"
    "12321" | "42531"  | "321"
    "5525"  | "1255"   | "552"
===================================================================================
[핵심 — 다중집합 교집합 min(count_X[i], count_Y[i])]
    동일 자리수가 양쪽에 여러 개 있을 때
    짝지을 수 있는 개수 = min(X의 개수, Y의 개수)

    Counter & 연산 내부 동작:
        같은 키에 대해 min(v1, v2)
        결과가 0 이하면 결과 Counter에서 제외
    → "[1차] 뉴스 클러스터링"에서 다뤘던 패턴 재활용

[startswith("0") 조건이 충분한 이유]
    내림차순 정렬 후 첫 문자가 '0'
    → 교집합의 가장 큰 수가 0
    → 모든 공통 자리수가 0
    → "0" 반환

[정렬 키 '0'~'9' 문자열 내림차순 = 수치 내림차순]
    '9' > '8' > ... > '0' 사전 순이 수치 순과 동일
    sorted(items(), reverse=True) 로 올바른 짝꿍 생성

[Counter & vs 고정배열 성능 역전]
    예상: 고정배열(크기 10) > Counter (해시 오버헤드)
    실측: Counter& 186ms, 고정배열 494ms (N=3,000,000)

    Counter가 빠른 이유:
        C 레벨 구현 + 문자 자체를 키로 사용
        int(c) 변환 없음

    고정배열이 느린 이유:
        int(c) 함수 호출이 3,000,000번 반복
        파이썬 레벨 함수 호출 오버헤드 × N

[ref_two 정렬 방식 분석]
    sorted(list(X)): O(N log N) × 2회
    투포인터 순회: O(N)
    → O(N log N) 지배

    공간복잡도:
        sorted_X, sorted_Y: 각 O(N) 추가 공간
        mine/ref_one: O(1) 고정 공간 (10개 배열 또는 Counter)

[실측 결과 — N=3,000,000, 20회]
    mine    (Counter&):      186.4ms  ← 가장 빠름
    ref_one (고정배열):       494.0ms
    ref_two (정렬+투포인터):  913.0ms  ← 5배 느림
===================================================================================
[내 초기 풀이]
    solution_mine: Counter & 다중집합 교집합

[개선 포인트]
    solution_mine:    개선 필요 없음 - Best
                      Counter C 레벨 최적화로 가장 빠름
    solution_ref_one: 고정배열 + min() - Sub
                      Counter & 내부 동작을 명시적으로 표현
                      int() 변환 오버헤드로 mine보다 느림
    solution_ref_two: O(N log N) 정렬 2회 → 가장 느림
===================================================================================
[복잡도 분석]
    N = max(len(X), len(Y)) (최대 3,000,000)

    Mine     - 시간: O(N) | 공간: O(1) - Counter 크기 최대 10
    Ref_one  - 시간: O(N) | 공간: O(1) - 배열 크기 10
    Ref_two  - 시간: O(N log N) | 공간: O(N) - 정렬 결과 리스트
    Best     - 시간: O(N) | 공간: O(1) - Mine과 동일
    Sub      - 시간: O(N) | 공간: O(1) - Ref_one과 동일
"""

from collections import Counter
import time


# =================================================================================
# Mine solution - Counter & 다중집합 교집합
# =================================================================================
def solution_mine(X: str, Y: str) -> str:
    """
    Counter & 연산으로 X, Y의 다중집합 교집합을 구하는 초기 풀이

    Counter(X) & Counter(Y):
        같은 키에 대해 min(v1, v2) 적용
        0 이하인 항목은 제외

    sorted(intersection.items(), reverse=True):
        '0'~'9' 사전 내림차순 = 수치 내림차순
        가장 큰 수부터 배치해 최대 짝꿍 생성

    startswith('0'):
        내림차순 첫 문자가 '0' → 모두 0 → '0' 반환
    """
    intersection = Counter(X) & Counter(Y)

    if not intersection:
        return "-1"

    answer = "".join([k * v for k, v in sorted(intersection.items(), reverse=True)])

    return "0" if answer.startswith("0") else answer


# =================================================================================
# Ref solution one - 고정 배열 + min()
# =================================================================================
def solution_ref_one(X: str, Y: str) -> str:
    """
    자리수별 개수를 고정 배열로 집계하고 min()으로 교집합을 구하는 참고 풀이

    count_X[i], count_Y[i]:
        숫자 i가 X, Y에 각각 몇 번 등장하는지 카운팅

    min(count_X[i], count_Y[i]):
        Counter & 의 내부 동작을 명시적으로 표현
        짝지을 수 있는 개수

    9→0 역순 순회:
        내림차순으로 answer 생성 → 별도 정렬 불필요

    int(c) 변환 3,000,000번 반복:
        파이썬 함수 호출 오버헤드 × N
        Counter(C 레벨) 대비 2.7배 느림
    """
    count_X = [0] * 10
    count_Y = [0] * 10

    for char in X:
        count_X[int(char)] += 1
    for char in Y:
        count_Y[int(char)] += 1

    answer = []
    for i in range(9, -1, -1):
        match_count = min(count_X[i], count_Y[i])
        answer.append(str(i) * match_count)

    result = "".join(answer)

    if not result:
        return "-1"
    if result[0] == "0":
        return "0"

    return result


# =================================================================================
# Ref solution two - 정렬 + 투포인터
# =================================================================================
def solution_ref_two(X: str, Y: str) -> str:
    """
    X, Y를 내림차순 정렬 후 투포인터로 공통 자리수를 찾는 참고 풀이

    sorted(list(X), reverse=True):
        O(N log N) 정렬 × 2회

    투포인터:
        정렬된 두 배열에서 같은 값 찾기
        X[i] == Y[j]: 공통 → 수집, 양 포인터 전진
        X[i] > Y[j]: i 전진 (더 작은 X 원소 건너뜀)
        X[i] < Y[j]: j 전진

    한계:
        O(N log N) 지배적 → 최대 규모에서 가장 느림
        추가 공간 O(N) 필요
    """
    sorted_X = sorted(list(X), reverse=True)
    sorted_Y = sorted(list(Y), reverse=True)

    i, j = 0, 0
    answer = []

    while i < len(sorted_X) and j < len(sorted_Y):
        if sorted_X[i] == sorted_Y[j]:
            answer.append(sorted_X[i])
            i += 1
            j += 1
        elif sorted_X[i] > sorted_Y[j]:
            i += 1
        else:
            j += 1

    result = "".join(answer)

    if not result:
        return "-1"
    if result[0] == "0":
        return "0"

    return result


# =================================================================================
# Best solution - Counter & (mine 주석 보강)
# =================================================================================
def solution_best(X: str, Y: str) -> str:
    """
    Counter & 로 O(N) 시간, O(1) 공간에 최대 짝꿍을 구하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        Counter: C 레벨 구현 + int() 변환 없음
        실측 N=3,000,000: 186ms (ref_one 494ms 대비 2.7배 우위)
        뉴스 클러스터링에서 학습한 Counter & 패턴 재활용
    """
    intersection = Counter(X) & Counter(Y)

    if not intersection:
        return "-1"

    answer = "".join([k * v for k, v in sorted(intersection.items(), reverse=True)])

    return "0" if answer.startswith("0") else answer


# =================================================================================
# Sub solution - 고정 배열 + min() (ref_one 주석 보강)
# =================================================================================
def solution_sub(X: str, Y: str) -> str:
    """
    고정 배열로 Counter & 내부 동작을 명시적으로 표현하는 서브 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        min(count_X[i], count_Y[i]): Counter & 의 핵심 연산을 직접 표현
        9→0 역순: 정렬 없이 내림차순 짝꿍 생성
        int(c) × N 호출로 Best보다 2.7배 느림
    """
    count_X = [0] * 10
    count_Y = [0] * 10

    for char in X:
        count_X[int(char)] += 1
    for char in Y:
        count_Y[int(char)] += 1

    answer = []
    for i in range(9, -1, -1):
        match_count = min(count_X[i], count_Y[i])
        answer.append(str(i) * match_count)

    result = "".join(answer)

    if not result:
        return "-1"
    if result[0] == "0":
        return "0"

    return result


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, str, str]] = [
        # (X, Y, 기댓값)
        # 공식 예시 전체
        ("100",   "2345",   "-1"),
        ("100",   "203045", "0"),
        ("100",   "123450", "10"),
        ("12321", "42531",  "321"),
        ("5525",  "1255",   "552"),
    ]

    solutions = [
        ("Mine    (Counter&)  ", solution_mine),
        ("Ref_one (고정배열)  ", solution_ref_one),
        ("Ref_two (정렬+투포인터)", solution_ref_two),
        ("Best    (Counter&)  ", solution_best),
        ("Sub     (고정배열)  ", solution_sub),
    ]

    # 워밍업 스텝
    _x, _y, _ = test_cases[0]
    for _, func in solutions:
        func(_x, _y)

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (X, Y, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(X, Y)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
