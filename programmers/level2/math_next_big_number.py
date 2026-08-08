"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 다음 큰 숫자
    유형       : Math / Bit Manipulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12911
    풀이일자   : 2026-08-08
================================================================================
[문제 요약]
    자연수 n의 다음 큰 숫자 반환
    조건: n보다 크고, 2진수 변환 시 1의 개수가 같으며, 조건을 만족하는 최솟값

    제약 조건
        - n: 1,000,000 이하 자연수
================================================================================
[입출력 예시]
    n  | result
    ---|-------
    78 | 83      (1001110 → 1010011)
    15 | 23      (1111 → 10111)
================================================================================
[내 풀이 최악 케이스]
    n=917504 (11100000000000000000₂, 1이 앞에 몰림)
    반복 131,075회 → 비트 연산 O(1) 대비 불리

    최악 구조: 1이 앞에 몰린 경우
        다음 큰 숫자는 1이 뒤로 이동한 형태 → 큰 갭 발생

[ref_one 비트 연산 원리]
    n = 1001110 (78) 기준 손 추적:

    lowest_one_bit = n & -n:
        -n = 2의 보수: 비트 반전 + 1
        1001110 & (-1001110) = 1001110 & 0110010 = 0000010 (가장 낮은 1비트)

    higher_bits = n + lowest_one_bit:
        1001110 + 0000010 = 1010000 (올림 발생)
        n보다 큰 수를 만드는 과정

    changed_bits = n ^ higher_bits:
        1001110 ^ 1010000 = 0011110 (변화한 비트들)
        올림으로 변화한 비트: 기존 연속 1(m개) + 올림된 1(1개) = m+1개

    >> 2 의미:
        changed_bits // lowest_one_bit: 가장 낮은 유효 비트를 1의 자리로 정렬
        >> 2 추가: m+1개 중 2개 제거
            - 1개: 올림으로 생긴 1 (higher_bits에 이미 포함)
            - 1개: 원래 lowest_one_bit 자리의 1 (higher_bits에 이미 포함)
        → lower_bits = m-1개의 1 (보존해야 할 나머지)

    higher_bits | lower_bits:
        1010000 | 0000000 = 1010000... 아니고
        실제: 1010000 | 0000011 = 1010011 (83) ✓
        (연속 1이 3개인 78의 경우: m=3, lower_bits=1개)

[ref_two 문자열 방식 원리]
    rfind('01'): 가장 오른쪽의 '01' 위치
        '0' 다음 '1' = 올림 적용 가능한 가장 낮은 비트
        '01' → '10': 최소 증가 보장

    '0' 접두사 추가 이유:
        올림 발생 시 비트 수 증가 대비 (1111 → 10111)

[bin() vs format(n, 'b') 성능 차이]
    실측 (timeit 1,000,000회):
        bin(n):              0.062μs  ← 가장 빠름
        format(n, 'b'):      0.108μs  ← 1.7배 느림

    bin()이 빠른 이유:
        CPython 전용 최적화 경로로 직접 2진 변환
        format()은 범용 포맷 프로토콜 + 파싱 오버헤드

    while 루프에서 매 반복 bin() 호출 → 최악 131,075회 누적
    → 효율성 테스트에서 format() 대비 의미 있는 차이
================================================================================
[내 초기 풀이]
    solution_mine: +1씩 증가하며 1의 개수 비교 (단순 순회)

[개선 포인트]
    solution_mine  : 직관적, 최악 131,075회 반복
                     효율성은 통과하나 비트 연산 대비 불리
    solution_ref_one: 비트 연산 O(1) - Best
                      lowest_one_bit, higher_bits, changed_bits, lower_bits
                      4단계 비트 연산으로 즉시 계산
    solution_ref_two: 문자열 트릭 - Sub
                      rfind('01')로 올림 위치 찾고 재조합
                      bin() 사용 필수 (format() 대비 1.7배 빠름)
================================================================================
[복잡도 분석]
    N = n (최대 1,000,000)

    Mine     - 시간: O(K) | 공간: O(1) - K=다음 큰 숫자까지 거리 (최악 131,075)
    Ref_one  - 시간: O(1) | 공간: O(1) - 비트 연산 상수 횟수
    Ref_two  - 시간: O(log N) | 공간: O(log N) - 비트 수에 비례한 문자열 처리
    Best     - 시간: O(1) | 공간: O(1) - Ref_one과 동일
    Sub      - 시간: O(K) | 공간: O(1) - Mine과 동일
"""

import time


# ================================================================================
# Mine solution - +1씩 증가하며 1의 개수 비교
# ================================================================================
def solution_mine(n: int) -> int:
    """
    n에서 +1씩 증가하며 2진수 1의 개수가 같은 수를 찾는 초기 풀이

    ones = bin(n).count('1'):
        기준 1의 개수 저장

    while True: target += 1, break 조건:
        1의 개수가 같은 수를 발견하면 즉시 반환

    bin() 선택 이유:
        format(n, 'b') 대비 1.7배 빠름 (CPython 전용 최적화)
        최악 131,075회 반복에서 누적 차이 의미 있음

    최악 케이스: n=917504 (1이 앞에 몰린 경우) → 131,075회 반복
    """
    target = n
    ones = bin(n).count('1')

    while True:
        target += 1
        if bin(target).count('1') == ones:
            break

    return target


# ================================================================================
# Ref solution one - 비트 연산 O(1)
# ================================================================================
def solution_ref_one(n: int) -> int:
    """
    4단계 비트 연산으로 O(1)에 다음 큰 숫자를 구하는 참고 풀이

    lowest_one_bit = n & -n:
        -n: 2의 보수 (비트 반전 + 1)
        가장 낮은 자리의 1비트만 추출

    higher_bits = n + lowest_one_bit:
        올림을 통해 n보다 큰 수 생성
        연속 1비트들이 올림으로 0이 되고 그 위 0이 1로 전환

    changed_bits = n ^ higher_bits:
        XOR로 변화한 비트 추출
        연속 1(m개) + 올림된 1(1개) = m+1개의 1이 연속

    lower_bits = (changed_bits // lowest_one_bit) >> 2:
        // lowest_one_bit: 최하위 유효 비트를 1의 자리로 정렬
        >> 2: m+1개 중 2개 제거
              (higher_bits에 이미 포함된 1 2개: 올림 1 + 원래 lowest 1)
        → 보존해야 할 나머지 m-1개의 1

    higher_bits | lower_bits:
        OR로 비트 합산 (단순 덧셈 아닌 비트 자리 결합)
    """
    lowest_one_bit = n & -n
    higher_bits = n + lowest_one_bit
    changed_bits = n ^ higher_bits
    lower_bits = (changed_bits // lowest_one_bit) >> 2
    return higher_bits | lower_bits


# ================================================================================
# Ref solution two - 문자열 트릭
# ================================================================================
def solution_ref_two(n: int) -> int:
    """
    2진수 문자열에서 '01' 위치를 찾아 '10'으로 교체하고 재조합하는 참고 풀이

    '0' + bin(n)[2:]:
        '0' 접두사: 올림 발생 시 비트 수 증가 대비 (1111 → 10111)
        bin(n)[2:]: '0b' 접두사 제거

    rfind('01'):
        가장 오른쪽 '01' 위치 탐색
        '0' 다음 '1' = 올림 적용 가능한 가장 낮은 비트
        rfind: 오른쪽에서 탐색 → 최소 증가 보장

    left = bits[:idx] + '10':
        '01' → '10' 교체: 올림 반영

    right 재조합:
        1의 개수 보존 + 최솟값: 0을 앞에, 1을 뒤에
        ('0' * zeros) + ('1' * ones)

    bin() 필수:
        format(n, 'b') 사용 시 효율성 테스트 3번 시간 초과
        bin()이 format() 대비 1.7배 빠름
    """
    bits = '0' + bin(n)[2:]
    idx = bits.rfind('01')
    left = bits[:idx] + '10'
    right = bits[idx + 2:]
    ones = right.count('1')
    zeros = len(right) - ones
    final_binary = left + ('0' * zeros) + ('1' * ones)
    return int(final_binary, 2)


# ================================================================================
# Best solution - 비트 연산 O(1) (ref_one 주석 보강)
# ================================================================================
def solution_best(n: int) -> int:
    """
    비트 연산 4단계로 O(1)에 다음 큰 숫자를 구하는 최적 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        O(1): n의 크기와 무관하게 상수 시간
        최악 케이스(n=917504): mine의 131,075회 반복 대비 즉시 계산
        비트 연산만 사용 → 정수 변환/문자열 생성 없음
    """
    lowest_one_bit = n & -n
    higher_bits = n + lowest_one_bit
    changed_bits = n ^ higher_bits
    lower_bits = (changed_bits // lowest_one_bit) >> 2
    return higher_bits | lower_bits


# ================================================================================
# Sub solution - +1씩 증가 (mine 주석 보강)
# ================================================================================
def solution_sub(n: int) -> int:
    """
    +1씩 증가하며 1의 개수가 같은 수를 찾는 서브 풀이

    Best 대비 특징:
        직관적: "1의 개수가 같은 더 큰 수"를 그대로 표현
        bin() 사용: format() 대비 1.7배 빠름 (효율성 테스트 통과)
        최악 O(K): K=131,075 (1이 앞에 몰린 경우)
        n이 작거나 1이 고르게 분포된 경우 실용적
    """
    target = n
    ones = bin(n).count('1')

    while True:
        target += 1
        if bin(target).count('1') == ones:
            break

    return target


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int]] = [
        # (n, 기댓값)
        # 공식 예시
        (78,  83),      # 1001110 → 1010011
        (15,  23),      # 1111 → 10111
        # 추가 케이스:
        (1,   2),       # 1 → 10
        (2,   4),       # 10 → 100
        # 최악 케이스 (mine 불리)
        (917504, 1048579),
    ]

    solutions = [
        ("Mine    (+1순회)  ", solution_mine),
        ("Ref_one (비트연산)", solution_ref_one),
        ("Ref_two (문자열) ", solution_ref_two),
        ("Best    (비트연산)", solution_best),
        ("Sub     (+1순회)  ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _ = test_cases[0]
    for _, func in solutions:
        func(_n)

    print("=" * 62)
    print(f"{'풀이':<20} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 62)

    for name, func in solutions:
        for idx, (n, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<20} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 62)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
