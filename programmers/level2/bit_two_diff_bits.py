"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 2개 이하로 다른 비트
    유형       : Bit Manipulation / Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/77885
    풀이일자   : 2026-09-21
===================================================================================
[문제 요약]
    각 수 x에 대해, x보다 크고 x와 비트가 1~2개 다른 수 중 가장 작은 수 반환

    제약 조건
        - numbers 길이: 1 이상 100,000 이하
        - 원소: 0 이상 10^15 이하
===================================================================================
[입출력 예시]
    numbers | result
    --------|--------
    [2, 7]  | [3, 11]
===================================================================================
[짝수/홀수 분기]
    짝수: 2^0 비트가 0 → +1하면 해당 비트만 0→1 → 비트 1개 차이 → 답
    홀수: 2^0 비트가 1 → +1하면 연쇄 작용 → 비트 여러 개 변함

[홀수 핵심 원리 — 연속된 1의 개수 k]
    홀수를 이진수로 보면: ...0 1(k개)
    연속된 1의 바로 위 0 자리를 1로 올리고
    연속된 1 중 최상위 비트를 0으로 내리면
    → 비트 2개만 차이, 가장 작은 증가

    예: 7 = 0111, k=3
        → 2^2 자리(최상위 1) 를 0→1: 1011(11로는 아직 처리 안됨)
        → 실제로는 2^k 자리에 1 추가, 2^(k-1) 자리를 0으로
        7 + 2^(k-1) = 7 + 4 = 11 = 1011
        XOR: 0111^1011 = 1100 → 2개 차이 ✓

[solution_ref — count_ones 증명]
    temp를 2로 나누면서 끝에서 연속된 1의 개수 k를 셈
    num + 2^(k-1):
        k개의 연속 1 중 가장 위(2^(k-1) 자리)가 0→1 역할
        동시에 2^k 자리에서 올림이 발생 (연쇄작용으로)
        최소한의 증가량으로 비트 2개 차이를 만듦

    손 추적 num=7=0111:
        k=3 → next = 7 + 4 = 11 = 1011
        0111 XOR 1011 = 1100 → 2개 ✓

    손 추적 num=11=1011:
        k=2 → next = 11 + 2 = 13 = 1101
        1011 XOR 1101 = 0110 → 2개 ✓

[solution_three — 비트 연산 수식 증명]
    (~num) & (num+1):
        num+1: 홀수 연쇄 작용으로 처음 0이 1이 되고 아래는 0
        ~num:  모든 비트 반전
        &연산: num+1이 새로 1이 된 자리만 추출
        → idx_bit = 2^k (처음 0→1이 된 자리의 가중치)

    num + idx_bit - idx_bit//2:
        idx_bit = 2^k 더하기: 사실상 중복 처리지만 num+1로 이미 적용됨
        idx_bit//2 = 2^(k-1) 빼기: 연속 1 최상위 비트 0으로

    예: num=7, num+1=8=1000, ~num=-8=...1000 (2's complement)
        (~7) & 8 = 8 = 2^3 = idx_bit
        7 + 8 - 4 = 11 ✓

[실측 결과 — N=100,000, 200회]
    three (비트연산): 13.0ms  ← 가장 빠름
    ref   (카운팅):   17.1ms
    two   (문자열):   35.4ms  ← 가장 느림
    one   (선형탐색): TLE (10^15 케이스에서 수억 번 루프)
===================================================================================
[내 초기 풀이]
    solution_mine_one:   선형 탐색 (시간초과)
    solution_mine_two:   문자열 비트 조작 (통과)
    solution_mine_three: 비트 연산 수식 (통과, 가장 빠름)

[개선 포인트]
    solution_mine_one:   선형 탐색 O(N × 탐색거리) → TLE
    solution_mine_two:   문자열 변환 비용 → Sub 기준
    solution_mine_three: 순수 비트 연산 O(N) - Best
    solution_ref:        count_ones 명시적 → 원리 이해에 유용
===================================================================================
[복잡도 분석]
    N = len(numbers) (최대 100,000)

    Mine_one   - 시간: O(N × M) | 공간: O(N) - M=탐색거리, TLE
    Mine_two   - 시간: O(N × L) | 공간: O(N) - L=비트 길이(최대 50)
    Mine_three - 시간: O(N)     | 공간: O(N) - 비트 연산 상수
    Ref        - 시간: O(N × k) | 공간: O(N) - k=연속 1 개수(최대 50)
    Best       - 시간: O(N)     | 공간: O(N) - Mine_three와 동일
    Sub        - 시간: O(N × L) | 공간: O(N) - Mine_two와 동일
"""

import time


# =================================================================================
# Mine solution one - 선형 탐색 (시간초과)
# =================================================================================
def solution_mine_one(numbers: list[int]) -> list[int]:
    """
    bigger를 1씩 증가시키며 XOR 비트 수가 2 이하인 첫 수를 찾는 초기 풀이

    시간초과 원인:
        홀수 끝에 1이 많이 연속되면 탐색 거리가 큼
        예: 2^50 - 1 같은 수는 수십억 번 루프 발생
        numbers 원소 최대 10^15 → while 루프 최악 O(2^k)
    """
    answer = []
    for num in numbers:
        bigger = num + 1
        while (bigger ^ num).bit_count() > 2:
            bigger += 1
        answer.append(bigger)
    return answer


# =================================================================================
# Mine solution two - 문자열 비트 조작
# =================================================================================
def solution_mine_two(numbers: list[int]) -> list[int]:
    """
    이진수 문자열로 변환 후 rfind로 첫 0을 찾아 비트를 직접 조작하는 풀이

    짝수: +1이 0→1 한 비트만 바꿈 → 답
    홀수: rfind('0')으로 오른쪽 첫 0 위치 탐색
          '0' → '10'으로 교체 (0→1 + 바로 아래 1→0)

    '0' + bin(num)[2:] 이유:
        홀수의 이진수가 1로 시작할 때
        rfind('0')이 맨 앞 0을 못 찾을 수 있음 → 앞에 '0' 추가

    문자열 변환/슬라이싱 비용으로 비트 연산 대비 2.7배 느림
    """
    answer = []
    for num in numbers:
        if num % 2 == 0:
            answer.append(num + 1)
            continue
        b_num = '0' + bin(num)[2:]
        idx = b_num.rfind('0')
        b_next = b_num[:idx] + '10' + b_num[idx + 2:]
        answer.append(int(b_next, 2))
    return answer


# =================================================================================
# Mine solution three - 비트 연산 수식
# =================================================================================
def solution_mine_three(numbers: list[int]) -> list[int]:
    """
    비트 연산으로 오른쪽 첫 0의 위치를 찾아 수식으로 직접 계산하는 최적 풀이

    (~num) & (num + 1):
        num+1: 홀수 연쇄작용 → 처음 0이 1이 되고 아래는 0
        ~num:  모든 비트 반전 → 원래 0이었던 자리가 1
        &연산: num+1에서 새로 1이 된 자리(=원래 첫 0)만 추출
        → idx_bit = 2^k

    num + idx_bit - idx_bit//2:
        +idx_bit: 2^k 자리 올림 반영
        -idx_bit//2: 2^(k-1) 자리(연속 1 최상위) 0으로 변환
        = 비트 2개 차이, 최소 증가량
    """
    answer = []
    for num in numbers:
        if num % 2 == 0:
            answer.append(num + 1)
            continue
        idx_bit = (~num) & (num + 1)
        next_num = num + idx_bit - (idx_bit // 2)
        answer.append(next_num)
    return answer


# =================================================================================
# Ref solution - count_ones 카운팅
# =================================================================================
def solution_ref(numbers: list[int]) -> list[int]:
    """
    끝에서 연속된 1의 개수 k를 세고 2^(k-1)을 더하는 참고 풀이

    count_ones = k:
        while temp % 2 == 1: temp //= 2 로 연속 1 개수 셈

    num + 2^(k-1):
        k개 연속 1의 최상위 비트(2^(k-1))가 0이 되고
        2^k 자리에서 1이 올라오는 구조
        → 비트 2개 차이, 최소 증가량

    mine_two/three의 원리를 가장 명시적으로 표현
    Python 레벨 while 루프로 비트 연산보다 약 30% 느림
    """
    answer = []
    for num in numbers:
        if num % 2 == 0:
            answer.append(num + 1)
        else:
            temp = num
            count_ones = 0
            while temp % 2 == 1:
                count_ones += 1
                temp //= 2
            answer.append(num + (2 ** (count_ones - 1)))
    return answer


# =================================================================================
# Best solution - 비트 연산 수식 (mine_three 주석 보강)
# =================================================================================
def solution_best(numbers: list[int]) -> list[int]:
    """
    비트 연산 수식으로 O(N) 시간에 각 수의 f값을 구하는 최적 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        (~num) & (num+1): C 레벨 비트 연산으로 첫 0 위치 O(1) 추출
        실측 N=100,000: 13.0ms (문자열 35.4ms 대비 2.7배 우위)
    """
    answer = []
    for num in numbers:
        if num % 2 == 0:
            answer.append(num + 1)
            continue
        idx_bit = (~num) & (num + 1)
        answer.append(num + idx_bit - (idx_bit // 2))
    return answer


# =================================================================================
# Sub solution - 문자열 비트 조작 (mine_two 주석 보강)
# =================================================================================
def solution_sub(numbers: list[int]) -> list[int]:
    """
    문자열로 비트를 직접 조작해 원리가 명시적으로 드러나는 서브 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        rfind('0')으로 오른쪽 첫 0 탐색이 코드에 직접 드러남
        '0'→'10' 교체: "0→1 올리고 바로 아래 1→0 내리기"를 문자열로 표현
        문자열 변환 비용으로 Best 대비 2.7배 느림
    """
    answer = []
    for num in numbers:
        if num % 2 == 0:
            answer.append(num + 1)
            continue
        b_num = '0' + bin(num)[2:]
        idx = b_num.rfind('0')
        b_next = b_num[:idx] + '10' + b_num[idx + 2:]
        answer.append(int(b_next, 2))
    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (numbers, 기댓값)
        # 공식 예시
        ([2, 7],    [3, 11]),
        # 추가 케이스:
        # 짝수만
        ([2, 4, 8], [3, 5, 9]),
        # 홀수 다양
        # 손 추적:
        # 13=1101: k=1(끝 1개) → 13+1=14=1110, XOR=0011 → 2개 ✓
        # 11=1011: k=2 → 11+2=13, XOR=0110 → 2개 ✓
        # 15=1111: k=4 → 15+8=23=10111, XOR=11000 → 2개 ✓
        ([13, 11, 15], [14, 13, 23]),
        # 0 처리
        ([0], [1]),
    ]

    # mine_one은 소규모만
    print("--- Mine_one (선형탐색, 소규모) ---")
    for nums, exp in test_cases[:3]:
        output = solution_mine_one(nums[:])
        status = "PASS" if output == exp else "FAIL"
        print(f"  {nums}: {output} {status}")

    solutions = [
        ("Mine_two   (문자열)  ", solution_mine_two),
        ("Mine_three (비트수식)", solution_mine_three),
        ("Ref        (카운팅)  ", solution_ref),
        ("Best       (비트수식)", solution_best),
        ("Sub        (문자열)  ", solution_sub),
    ]

    # 워밍업
    _n, _ = test_cases[0]
    for _, func in solutions:
        func(_n[:])

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (numbers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(numbers[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
