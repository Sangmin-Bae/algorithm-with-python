"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 자릿수 더하기
    유형       : Math / String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12931
    풀이일자   : 2026-07-28
===================================================================================
[문제 요약]
    자연수 N의 각 자릿수의 합 반환

    제약 조건
        - N: 1 이상 100,000,000 이하 자연수 (최대 9자리)
===================================================================================
[입출력 예시]
    N   | answer
    ----|-------
    123 | 6      (1+2+3)
    987 | 24     (9+8+7)
===================================================================================
[풀이 방법 비교]
    문자열 변환 방식:
        str(n)으로 문자열화 → 각 문자를 int로 변환 → sum
        형변환 비용 있으나 코드 간결

    수학적 방식:
        n % 10으로 1의 자리 추출 → n //= 10으로 자릿수 이동
        형변환 없이 정수 연산만 사용

[sum + 제너레이터 vs sum + 리스트 컴프리헨션]
    sum은 이터러블을 직접 소비 → 리스트를 미리 만들 필요 없음
    (int(i) for i in str(n)): 제너레이터, 지연 평가
    [int(i) for i in str(n)]: 리스트, 즉시 평가 후 메모리 적재
    → sum에서는 제너레이터가 메모리 효율 우위

    join과의 차이:
        join은 내부적으로 이터러블을 두 번 순회(길이 계산 + 결합)
        → 제너레이터보다 리스트가 유리
        sum은 한 번만 순회 → 제너레이터가 유리

[map vs 제너레이터]
    map(int, str(n)): C 레벨에서 동작하는 빌트인 함수
    (int(i) for i in str(n)): Python 레벨 제너레이터
    → map이 C 레벨 구현으로 더 빠름

[solution_three divmod 동작]
    손 추적 (n=123):
        quotient=123: divmod(123,10) -> (12, 3), answer=3
        quotient=12:  divmod(12,10)  -> (1, 2),  answer=5
        quotient=1:   divmod(1,10)   -> (0, 1),  answer=6
        quotient=0: while 종료
        return 6 ✓

    remainder=0 초기화: 루프 첫 실행에서 바로 갱신되므로 불필요
    동작에는 영향 없음
===================================================================================
[내 초기 풀이]
    solution_mine_one  : 제너레이터 + sum
    solution_mine_two  : map + sum
    solution_mine_three: divmod + while (수학적 접근)

[개선 포인트]
    solution_mine_one  : 개선 필요 없음
                         제너레이터로 메모리 효율적, sum이 직접 소비
    solution_mine_two  : 개선 필요 없음 - Best
                         map이 C 레벨 구현으로 Mine_one보다 빠름
    solution_mine_three: 개선 필요 없음 - Sub
                         형변환 없이 수학적으로 자릿수 추출
                         remainder=0 초기화는 불필요하나 가독성에 영향 없음
===================================================================================
[복잡도 분석]
    D = 자릿수 수 (최대 9, 사실상 상수)

    Mine_one   - 시간: O(D) | 공간: O(1) - 제너레이터, 지연 평가
    Mine_two   - 시간: O(D) | 공간: O(1) - map, C 레벨
    Mine_three - 시간: O(D) | 공간: O(1) - divmod 반복
    Best       - 시간: O(D) | 공간: O(1) - Mine_two와 동일
    Sub        - 시간: O(D) | 공간: O(1) - Mine_three와 동일

    D<=9 고정 -> 모두 실질적으로 O(1)
"""

import time


# =================================================================================
# Mine solution one - 제너레이터 + sum
# =================================================================================
def solution_mine_one(n: int) -> int:
    """
    str 변환 + 제너레이터로 각 자릿수를 합산하는 풀이

    제너레이터 선택 이유:
        sum은 이터러블을 직접 소비 → 리스트 사전 생성 불필요
        (int(i) for i in str(n)): 지연 평가, 메모리 O(1)
        리스트 컴프리헨션 [int(i) for i in str(n)]: 즉시 평가, 메모리 O(D)
        → sum에서는 제너레이터가 유리
    """
    return sum(int(i) for i in str(n))


# =================================================================================
# Mine solution two - map + sum
# =================================================================================
def solution_mine_two(n: int) -> int:
    """
    map으로 각 자릿수를 int 변환 후 sum으로 합산하는 풀이

    map(int, str(n)):
        str(n): 정수를 문자열로 변환 → 각 문자가 자릿수
        map(int, ...): C 레벨에서 각 문자를 int로 변환하는 이터레이터 반환
        Mine_one 제너레이터 대비 C 레벨 구현으로 더 빠름
    """
    return sum(map(int, str(n)))


# =================================================================================
# Mine solution three - divmod + while (수학적 접근)
# =================================================================================
def solution_mine_three(n: int) -> int:
    """
    10으로 반복 나눗셈으로 자릿수를 추출해 합산하는 풀이

    divmod(n, 10):
        몫: 상위 자릿수들 (다음 순회 대상)
        나머지: 현재 1의 자리 값

    손 추적 (n=123):
        divmod(123,10) -> (12, 3), answer=3
        divmod(12, 10) -> (1,  2), answer=5
        divmod(1,  10) -> (0,  1), answer=6
        while 0 > 0: False -> 종료

    형변환 없이 수학적 연산만으로 각 자릿수 추출
    N이 자연수(1 이상)이므로 n=0 엣지케이스 없음
    """
    answer = 0
    quotient = n

    while quotient > 0:
        quotient, remainder = divmod(quotient, 10)
        answer += remainder

    return answer


# =================================================================================
# Best solution - map + sum (mine_two 주석 보강)
# =================================================================================
def solution_best(n: int) -> int:
    """
    map + sum으로 가장 간결하고 빠르게 자릿수 합을 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        map(int, str(n)): C 레벨 구현 → Python 제너레이터보다 빠름
        sum: 이터러블 직접 소비 → 중간 리스트 불필요
        두 줄을 한 줄로 표현, 가독성과 성능 모두 우위
    """
    return sum(map(int, str(n)))


# =================================================================================
# Sub solution - divmod + while (mine_three 주석 보강)
# =================================================================================
def solution_sub(n: int) -> int:
    """
    divmod로 자릿수를 추출하는 수학적 접근의 서브 풀이

    Best 대비 특징:
        str, int 형변환 없이 순수 정수 연산
        10진수 자릿수 추출 원리를 직접 표현
        나머지: 현재 1의 자리, 몫: 상위 자릿수로 다음 순회
        while 조건(quotient > 0)이 종료 조건을 명시적으로 표현
    """
    answer = 0
    quotient = n

    while quotient > 0:
        quotient, remainder = divmod(quotient, 10)
        answer += remainder

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int]] = [
        # (N, 기댓값)
        # 공식 예시
        (123, 6),   # 1+2+3=6
        (987, 24),  # 9+8+7=24
        # 추가 케이스:
        (1,   1),   # 단일 자릿수
        (10,  1),   # 0이 자릿수에 포함되는 경우
        (100000000, 1),  # 최대값 1억: 1+0+...+0=1
        (99999999,  72), # 9×8=72
    ]

    solutions = [
        ("Mine_one   (제너레이터)", solution_mine_one),
        ("Mine_two   (map+sum)  ", solution_mine_two),
        ("Mine_three (divmod)   ", solution_mine_three),
        ("Best       (map+sum)  ", solution_best),
        ("Sub        (divmod)   ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _ = test_cases[0]
    for _, func in solutions:
        func(_n)

    print("=" * 62)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 62)

    for name, func in solutions:
        for idx, (n, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 62)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
