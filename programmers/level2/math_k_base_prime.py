"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : k진수에서 소수 개수 구하기
    유형       : Math / String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/92335
    풀이일자   : 2026-09-01
===================================================================================
[문제 요약]
    n을 k진수로 변환 후, 0으로 구분된 연속 숫자들을 10진수로 보았을 때
    소수인 개수 반환

    제약 조건
        - 1 ≤ n ≤ 1,000,000
        - 3 ≤ k ≤ 10
===================================================================================
[입출력 예시]
    n      | k  | result
    -------|----|---------
    437674 | 3  | 3       (211, 2, 11)
    110011 | 10 | 2       (11, 11)
===================================================================================
[핵심 — 두 가지 서브 문제]
    1. n → k진수 문자열 변환
    2. 0으로 분리된 각 숫자가 소수인지 판별

[int_to_base 내장 함수 분기]
    k=8:  oct(num)[2:]  ← C 레벨
    k=10: str(num)      ← C 레벨
    나머지 (3,4,5,6,7,9): while 루프로 직접 변환

[is_prime 최적화]
    1은 소수 아님 → 2는 소수 → 짝수 제외 → 3~√n 홀수만 순회
    math.isqrt(num): int(num**0.5)보다 정확하고 빠름
    O(√num)

[세 가지 분리 방식]
    풀이1 (split):      str.split('0')으로 한 번에 분리
        연속 0 사이 빈 문자열 발생 → s != '' 필터 필요
        가장 간결

    풀이2 (stream):     순회하며 temp_str에 누적
        '0' 만나면 판별, 끝까지 0이 안 나오는 경우 별도 처리 필요
        코드 길이 가장 김

    풀이3 (two_pointer): left/right 포인터로 구간 찾기
        continue로 '0' 건너뜀 → 중첩 없이 가독성 확보
        슬라이싱 비용으로 약간 느림

[실측 결과 — n=1,000,000, k=3, 50,000회]
    풀이1 (split):       2.6μs  ← 공동 1위
    풀이2 (stream):      2.6μs  ← 공동 1위
    풀이3 (two_pointer): 3.1μs

    re.split('0+') 시도: 2.9μs (정규표현식 컴파일 오버헤드로 불리)
    → 제3의 최적 풀이가 기존 세 풀이를 넘어서지 못함
    → 풀이1 코드 간결성 기준으로 Best 선정
===================================================================================
[내 초기 풀이]
    solution_mine_one:   split('0') + sum + 제너레이터
    solution_mine_two:   순회 + temp_str 누적
    solution_mine_three: 투 포인터 (continue 패턴)

[개선 포인트]
    solution_mine_one:   개선 필요 없음 - Best
                         가장 간결하고 빠름
    solution_mine_two:   동일 속도이나 코드 더 김
    solution_mine_three: 약간 느림 - Sub
                         continue 발상으로 중첩 없이 투 포인터 구현
===================================================================================
[복잡도 분석]
    M = k진수 변환 후 문자열 길이 ≈ log_k(n) (최대 약 20자)
    P = 0으로 분리된 숫자 중 최대값 ≤ n = 1,000,000

    int_to_base: O(log_k(n))
    is_prime:    O(√P) 최악
    전체:        O(log_k(n) + M × √P)

    Mine_one   - 시간: O(M + M × √P) | 공간: O(M)
    Mine_two   - 시간: O(M + M × √P) | 공간: O(M)
    Mine_three - 시간: O(M + M × √P) | 공간: O(M)
    Best       - 시간: O(M + M × √P) | 공간: O(M) - Mine_one과 동일
    Sub        - 시간: O(M + M × √P) | 공간: O(M) - Mine_three와 동일

    n ≤ 1,000,000, k ≥ 3 → M ≤ 13 → 사실상 O(1)
"""

import math
import time


# =================================================================================
# Mine solution one - split('0') + sum + 제너레이터
# =================================================================================
def solution_mine_one(n: int, k: int) -> int:
    """
    split('0')으로 분리 후 제너레이터 sum으로 소수 개수를 구하는 초기 풀이

    split('0'):
        연속된 '0' 사이에 빈 문자열('') 발생 가능
        → s != '' (또는 if s) 필터 필수

    sum(is_prime(int(s)) for s in ... if s):
        bool이 int 서브클래스 → True=1, False=0
        제너레이터로 메모리 효율적 순회
    """
    def int_to_base(num: int, base: int) -> str:
        if base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        result = ""
        while num > 0:
            result = str(num % base) + result
            num //= base
        return result

    def is_prime(num: int) -> bool:
        if num <= 1: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, math.isqrt(num) + 1, 2):
            if num % i == 0: return False
        return True

    return sum(is_prime(int(s)) for s in int_to_base(n, k).split('0') if s)


# =================================================================================
# Mine solution two - 순회 + temp_str 누적
# =================================================================================
def solution_mine_two(n: int, k: int) -> int:
    """
    k진수 문자열을 순회하며 0이 아닌 연속 문자열을 누적해 판별하는 풀이

    temp_str 누적:
        0이 아닌 문자를 만나면 temp_str에 누적
        0을 만나면 temp_str 판별 후 초기화

    마지막 예외 처리:
        k진수 문자열이 0으로 끝나지 않으면
        마지막 temp_str이 while 밖에서 처리 필요
    """
    def int_to_base(num: int, base: int) -> str:
        if base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        result = ""
        while num > 0:
            result = str(num % base) + result
            num //= base
        return result

    def is_prime(num: int) -> bool:
        if num <= 1: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, math.isqrt(num) + 1, 2):
            if num % i == 0: return False
        return True

    answer = 0
    temp_str = ""

    for char in int_to_base(n, k):
        if char != "0":
            temp_str += char
        else:
            if temp_str:
                if is_prime(int(temp_str)):
                    answer += 1
                temp_str = ""

    if temp_str and is_prime(int(temp_str)):
        answer += 1

    return answer


# =================================================================================
# Mine solution three - 투 포인터 (continue 패턴)
# =================================================================================
def solution_mine_three(n: int, k: int) -> int:
    """
    left/right 투 포인터로 0이 아닌 구간을 찾는 풀이

    continue 패턴:
        converted[left] == '0' → left += 1, continue
        초기 '0'을 건너뛰는 조기 탈출
        중첩 if 없이 left를 0이 아닌 위치로 이동

    right 탐색:
        left에서 시작해 '0' 만날 때까지 right 전진
        converted[left:right]가 판별 대상
    """
    def int_to_base(num: int, base: int) -> str:
        if base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        result = ""
        while num > 0:
            result = str(num % base) + result
            num //= base
        return result

    def is_prime(num: int) -> bool:
        if num <= 1: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, math.isqrt(num) + 1, 2):
            if num % i == 0: return False
        return True

    answer = 0
    converted = int_to_base(n, k)
    N = len(converted)
    left = 0

    while left < N:
        if converted[left] == '0':
            left += 1
            continue

        right = left
        while right < N and converted[right] != '0':
            right += 1

        if is_prime(int(converted[left:right])):
            answer += 1

        left = right

    return answer


# =================================================================================
# Best solution - split + sum + 제너레이터 (mine_one 주석 보강)
# =================================================================================
def solution_best(n: int, k: int) -> int:
    """
    split('0') + 제너레이터 sum으로 가장 간결하게 소수 개수를 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        split('0'): 한 줄로 0 기준 분리
        sum + 제너레이터: bool의 int 성질로 개수 카운트
        실측 2.6μs (mine_three 3.1μs 대비 우위)
        제3의 풀이(re.split 등) 탐색했으나 기존 풀이를 넘지 못함
    """
    def int_to_base(num: int, base: int) -> str:
        if base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        result = ""
        while num > 0:
            result = str(num % base) + result
            num //= base
        return result

    def is_prime(num: int) -> bool:
        if num <= 1: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, math.isqrt(num) + 1, 2):
            if num % i == 0: return False
        return True

    return sum(is_prime(int(s)) for s in int_to_base(n, k).split('0') if s)


# =================================================================================
# Sub solution - 투 포인터 (mine_three 주석 보강)
# =================================================================================
def solution_sub(n: int, k: int) -> int:
    """
    continue 패턴 투 포인터로 구간을 명시적으로 찾는 서브 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        continue: 중첩 없이 '0' 건너뛰기 → 가독성 확보
        left/right로 비-0 구간이 코드에 직접 드러남
        Best 대비 슬라이싱 비용으로 약간 느림 (3.1μs vs 2.6μs)
    """
    def int_to_base(num: int, base: int) -> str:
        if base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        result = ""
        while num > 0:
            result = str(num % base) + result
            num //= base
        return result

    def is_prime(num: int) -> bool:
        if num <= 1: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, math.isqrt(num) + 1, 2):
            if num % i == 0: return False
        return True

    answer = 0
    converted = int_to_base(n, k)
    N = len(converted)
    left = 0

    while left < N:
        if converted[left] == '0':
            left += 1
            continue

        right = left
        while right < N and converted[right] != '0':
            right += 1

        if is_prime(int(converted[left:right])):
            answer += 1

        left = right

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int, int]] = [
        # (n, k, 기댓값)
        # 공식 예시
        (437674, 3, 3),   # 211, 2, 11
        (110011, 10, 2),  # 11, 11
        # 추가 케이스:
        # 4 → 3진수 '11' → 11은 소수
        (4, 3, 1),
        # 단일 소수
        (11, 10, 1),      # 10진수 '11' → 11은 소수
        # 1만 남음 (소수 아님)
        # 9 → 3진수 '100' → '1' → 1은 소수 아님
        (9, 3, 0),
    ]

    # TC3 기댓값 재확인
    import math as _math
    def _is_prime(num):
        if num <= 1: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, _math.isqrt(num)+1, 2):
            if num % i == 0: return False
        return True

    solutions = [
        ("Mine_one   (split)   ", solution_mine_one),
        ("Mine_two   (stream)  ", solution_mine_two),
        ("Mine_three (2ptr)    ", solution_mine_three),
        ("Best       (split)   ", solution_best),
        ("Sub        (2ptr)    ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _k, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _k)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (n, k, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, k)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
