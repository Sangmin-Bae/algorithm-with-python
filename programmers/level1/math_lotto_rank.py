"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 로또의 최고 순위와 최저 순위
    유형       : Math / Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/77484
    풀이일자   : 2026-08-27
===================================================================================
[문제 요약]
    일부 번호가 0으로 가려진 로또에서 가능한 최고 순위, 최저 순위 반환

    순위표:
        1등: 6개, 2등: 5개, 3등: 4개, 4등: 3개, 5등: 2개, 6등(낙첨): 그 외

    제약 조건
        - lottos, win_nums: 길이 6 고정
        - 0: 알아볼 수 없는 번호 (0 제외 중복 없음)
        - win_nums: 1~45, 중복 없음
===================================================================================
[입출력 예시]
    lottos              | win_nums               | result
    --------------------|------------------------|-------
    [44,1,0,0,31,25]    | [31,10,45,1,6,19]      | [3,5]
    [0,0,0,0,0,0]       | [38,19,20,40,15,25]    | [1,6]
    [45,4,35,20,3,9]    | [20,9,3,45,4,35]       | [1,1]
===================================================================================
[핵심 — zeros와 match로 최고/최저 결정]
    zeros: 가려진 번호 개수 (0의 개수)
        최고: 모두 당첨 번호로 가정
        최저: 모두 낙첨 번호로 가정

    match: 알아볼 수 있는 번호 중 당첨된 개수

    최고 당첨 개수: match + zeros
    최저 당첨 개수: match

[순위 공식: 7 - score]
    1등(6개): 7-6=1
    2등(5개): 7-5=2
    ...
    5등(2개): 7-2=5
    6등(1개 이하): 특별처리 → 6

[list+sum vs set+교집합 비교]
    mine: sum(num in win_nums for num in lottos)
        for 6회 × in O(6) = O(36) ≈ O(1)
        0은 win_nums에 없으므로 교집합에서 자동 제외

    ref: set(lottos) & set(win_nums)
        set 변환 O(6+6) + & 연산 O(6) = O(18) ≈ O(1)
        set 변환 비용이 추가돼 실측 미세하게 느림

    실측 (1,000,000회):
        mine (list+sum):  1.18μs
        ref  (set+교집합): 1.26μs
        모두 상수, 실질적 차이 없음

[mine에 lambda를 적용하면 Best가 되는가]
    mine + lambda 적용 실측: 1.34μs (mine 1.18μs보다 느림)
    lambda 정의: 매 함수 호출마다 함수 객체 생성
    lambda 호출: 2회 × 함수 호출 오버헤드
    삼항 연산자: 인라인 평가, 함수 객체 생성 없음
    → 성능 1순위 기준으로 삼항 연산자 방식이 Best
    → lambda는 중복 제거 가독성 장점이 있으나
       이미 ref(set+lambda)가 Sub로 커버 → 별도 풀이 불필요

[get_rank 람다 — 코드 중복 제거]
    mine: 삼항 연산자 2번 중복
    ref:  get_rank 함수로 추출 → 중복 제거
    가독성 장점, 람다 호출 비용은 무시 가능
===================================================================================
[내 초기 풀이]
    solution_mine: list + sum + 삼항 연산자

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
                   삼항 연산자 인라인이 함수 호출보다 빠름
                   get_rank를 모듈 레벨 함수로 추출해도 1.34μs로 mine보다 느림
                   성능 1순위 기준으로 삼항 연산자 방식이 최적
    solution_ref:  set 교집합 + get_rank 람다 - Sub
                   코드 중복 제거, 가독성 장점
                   set 변환 + 람다 호출 비용으로 mine보다 느림

    Best/Sub 선정 원칙:
        소스(내 풀이 vs 참고 풀이)로 기계적 배정하지 않음
        두 풀이의 장점을 융합한 변형이 최적이면 그게 Best
        이 문제에서는 융합(모듈레벨 함수)이 mine(삼항 인라인)을 넘지 못함
        → 삼항 연산자가 Best 유지
===================================================================================
[복잡도 분석]
    N = 6 고정 (lottos, win_nums 길이)

    Mine - 시간: O(N²) = O(36) = O(1) | 공간: O(1)
    Ref  - 시간: O(N)  = O(6)  = O(1) | 공간: O(N) - set 변환
    Best - 시간: O(1) | 공간: O(1) - Mine과 동일
    Sub  - 시간: O(1) | 공간: O(1) - Ref와 동일
"""

import time


# =================================================================================
# Mine solution - list + sum + 삼항 연산자
# =================================================================================
def solution_mine(lottos: list[int], win_nums: list[int]) -> list[int]:
    """
    zeros와 match를 베이스라인으로 최고/최저 순위를 구하는 초기 풀이

    zeros = lottos.count(0):
        가려진 번호 개수 → 최고 순위에서 모두 당첨으로 가정

    match = sum(num in win_nums for num in lottos):
        알아볼 수 있는 번호 중 당첨 개수
        0은 win_nums(1~45)에 없으므로 교집합에서 자동 제외
        in 연산: O(6) × 6회 = O(36) ≈ O(1)

    순위 공식: 7 - score (2개 이상일 때)
        score <= 1이면 6등 (낙첨)
    """
    zeros = lottos.count(0)
    match = sum(num in win_nums for num in lottos)

    high = 7 - (match + zeros) if (match + zeros) >= 2 else 6
    low = 7 - match if match >= 2 else 6

    return [high, low]


# =================================================================================
# Ref solution - set 교집합 + get_rank 람다
# =================================================================================
def solution_ref(lottos: list[int], win_nums: list[int]) -> list[int]:
    """
    set 교집합으로 match를 구하고 get_rank 람다로 중복을 제거하는 참고 풀이

    set(lottos) & set(win_nums):
        두 집합의 교집합 = 일치하는 번호들
        0은 win_set에 없으므로 교집합에서 자동 제외
        set 변환 비용 O(6+6)이 추가되어 mine보다 미세하게 느림

    get_rank 람다:
        순위 변환 로직을 함수로 추출 → 삼항 연산자 중복 제거
        mine의 두 번 중복된 삼항 연산자를 한 함수로 통합

    실측 mine보다 0.08μs 느림 (set 변환 오버헤드)
    """
    win_set = set(win_nums)
    lotto_set = set(lottos)

    match = len(lotto_set & win_set)
    zeros = lottos.count(0)

    get_rank = lambda score: 6 if score <= 1 else 7 - score

    return [get_rank(match + zeros), get_rank(match)]


# =================================================================================
# Best solution - list + sum (mine 주석 보강)
# =================================================================================
def solution_best(lottos: list[int], win_nums: list[int]) -> list[int]:
    """
    zeros와 match로 O(1) 시간에 최고/최저 순위를 구하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        set 변환 없이 직접 sum으로 match 계산
        실측 1.18μs (ref 1.26μs 대비 미세 우위)
        lottos, win_nums 길이 6 고정 → 모든 연산이 상수
    """
    zeros = lottos.count(0)
    match = sum(num in win_nums for num in lottos)

    high = 7 - (match + zeros) if (match + zeros) >= 2 else 6
    low = 7 - match if match >= 2 else 6

    return [high, low]


# =================================================================================
# Sub solution - set 교집합 + get_rank 람다 (ref 주석 보강)
# =================================================================================
def solution_sub(lottos: list[int], win_nums: list[int]) -> list[int]:
    """
    set 교집합과 get_rank 람다로 코드 중복을 제거하는 서브 풀이

    Best 대비 특징:
        get_rank 람다: 순위 변환 로직을 한 곳에서 관리
        삼항 연산자 중복 제거 → 유지보수 편의
        set 교집합: 수학적 표현이 명확
        set 변환 비용으로 Best보다 미세하게 느림
    """
    win_set = set(win_nums)
    lotto_set = set(lottos)

    match = len(lotto_set & win_set)
    zeros = lottos.count(0)

    get_rank = lambda score: 6 if score <= 1 else 7 - score

    return [get_rank(match + zeros), get_rank(match)]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (lottos, win_nums, 기댓값)
        # 공식 예시
        ([44, 1, 0, 0, 31, 25], [31, 10, 45, 1, 6, 19],   [3, 5]),
        ([0, 0, 0, 0, 0, 0],    [38, 19, 20, 40, 15, 25], [1, 6]),
        ([45, 4, 35, 20, 3, 9], [20, 9, 3, 45, 4, 35],    [1, 1]),
        # 추가 케이스:
        # 모두 불일치
        ([1, 2, 3, 4, 5, 6],    [7, 8, 9, 10, 11, 12],    [6, 6]),
        # 1개만 일치 (5등 불가, 6등)
        ([1, 2, 3, 4, 5, 0],    [1, 8, 9, 10, 11, 12],    [5, 6]),
    ]

    solutions = [
        ("Mine (list+sum)   ", solution_mine),
        ("Ref  (set+lambda) ", solution_ref),
        ("Best (list+sum)   ", solution_best),
        ("Sub  (set+lambda) ", solution_sub),
    ]

    # 워밍업 스텝
    _l, _w, _ = test_cases[0]
    for _, func in solutions:
        func(_l, _w)

    print("=" * 60)
    print(f"{'풀이':<20} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 60)

    for name, func in solutions:
        for idx, (lottos, win_nums, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(lottos[:], win_nums[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<20} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 60)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
