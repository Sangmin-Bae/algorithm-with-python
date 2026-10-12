"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6326. [파이썬 프로그래밍 기초(1) 파이썬의 기본 구조와 기초 문법] 8. 함수의 기초 7
    유형       : Math (팩토리얼), Function, Recursion
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcWL1iq5dkDFAU4&categoryId=AWcWL1iq5dkDFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=2
    풀이일자   : 2026-10-12
================================================================================
[문제 요약]
    팩토리얼을 구하는 함수를 정의하고, 입력된 숫자의 팩토리얼 값을 출력

    입력 방식 : 표준 입력 한 줄 (정수 N)
    적용 방식 : input → 매개변수 N, output → 반환값 (정수)
    참고      : 지문에 N의 범위가 명시되어 있지 않아 N >= 0 (음이 아닌 정수)로 가정
================================================================================
[입출력 예시]
    공식 예시
    N | return
    --|-------
    5 | 120

    자체 검증 케이스 (전부 손 계산)
    N  | return
    ---|----------------------------------
    0  | 1
    1  | 1
    2  | 2
    3  | 6
    10 | 3628800
    12 | 479001600
    20 | 2432902008176640000
    21 | 51090942171709440000
    25 | 15511210043330985984000000
================================================================================
[풀이 전략]
    정의: N! = 1 * 2 * ... * N, 0! = 1 (빈 곱)

    풀이 구성:
        mine_one   : for 반복문으로 2부터 N까지 누적 곱 (가장 명시적)
        mine_two   : math.factorial(N) (내장 라이브러리)
        mine_three : 재귀 f(n) = n * f(n - 1), f(n <= 1) = 1
        best       : math.factorial (mine_two와 동일)
        Sub는 차별점 있는 변형이 없어 생략
            (math.prod(range), functools.reduce(mul)은 for 누적곱과 비슷하고
             math.perm(N)은 math.factorial과 비슷해 별도 Sub로 두지 않음)

    Best 판단 (코딩테스트 맥락 vs 학습 맥락):
        코딩테스트에서 math 모듈은 허용되므로 두 맥락에서 Best가 충돌하지 않아 best 하나로 기록
        단, "함수의 기초" 학습이 목적이면 for 누적곱(mine_one)이 정의를 가장 직접 보여줌

    mine_one 손 추적 (공식 예시) N = 5:
        result = 1, i = 2..5
        i = 2 → 2    i = 3 → 6    i = 4 → 24    i = 5 → 120
        → 120 ✓

    mine_three 손 추적 (공식 예시) N = 5:
        f(5) = 5 * f(4) = 5 * 4 * f(3) = 5 * 4 * 3 * f(2) = 5 * 4 * 3 * 2 * f(1)
        f(1) = 1 (n <= 1 이면 종료) → 5 * 4 * 3 * 2 * 1 = 120 ✓

    재귀 버그 주의 (제출 전 코드):
        함수 안에 정의한 recursive_factorial이 자기 자신이 아닌 factorial을 호출
        → 함수 형태로 옮기면 NameError (N = 5에서 재현 확인)
        SWEA 제출 형태처럼 함수 이름이 factorial이면 문제없지만
        함수 이름을 바꾸면서 호출부를 놓친 경우
        → 이 파일에서는 f가 자기 자신을 호출하도록 수정

    N 범위와 한계:
        재귀 깊이 : 파이썬 기본 한도 1000 (sys.getrecursionlimit())
                    이 파일의 호출 구조에서 N = 999부터 RecursionError (측정 환경 기준)
                    호출 스택이 얕은 환경에서는 N이 조금 더 커질 수 있음
        출력 한도 : 정수를 문자열로 바꾸는 한도 4300자리 (sys.get_int_max_str_digits())
                    N = 1559부터 print(N!)에서 ValueError (3.12.3 측정)
                    1558!은 정확히 4300자리, 1559!는 한도 초과
                    (계산은 되나 print 시점에 실패, 한도는 Python 3.11 이후 적용)
        음수      : for 누적곱과 재귀는 1을 반환, math.factorial은 ValueError

    SWEA 제출 형태 (함수 본문 아래에 이어 붙여 제출, best는 파일 상단의 import math 포함):
        N = int(input())
        print(solution_best(N))

    제출 이력:
        solution_mine_one, solution_mine_two와 동일한 로직으로 SWEA 제출 테스트 통과 (2026-10-12)
        solution_mine_three와 동일한 로직(함수명 factorial)으로 SWEA 제출 테스트 통과 (2026-10-12)
        solution_best는 mine_two와 같은 코드라 별도 제출 없음
================================================================================
[실측 결과 — 팩토리얼 계산 방식 비교]
    측정: 호출당 중앙값, Python 3.12.3 샌드박스 (python3.12 고정, 입력 크기는 자체 기준)
          교차 측정 7~15라운드 (N = 5는 100,000회, 20은 50,000회, 100은 10,000회,
          900은 300회, 5,000은 10회, 20,000은 2회)
          표의 값은 for 누적곱 대비 비율 (재귀는 깊이 한도로 N = 900까지만)

    방식              N=5     N=20    N=100   N=900   N=5,000   N=20,000
    for 누적곱         1.00    1.00    1.00    1.00    1.00      1.00
    math.factorial    0.30    0.10    0.17    0.19    0.15      0.11
    재귀               3.05    2.29    1.63    1.59    -         -
    math.prod(range)  0.90    0.42    0.80    0.97    1.01      1.19
    reduce(mul)       1.53    1.21    1.06    1.02    1.02      1.02
    math.perm(N)      0.31    0.10    0.16    0.19    0.16      0.11

    for 누적곱의 절대값: 0.176µs (N=5) / 0.668µs (20) / 4.64µs (100) /
                         147µs (900) / 4.61ms (5,000) / 81.9ms (20,000)

    해석:
        math.factorial은 모든 N에서 for 누적곱보다 빠름 (약 3~10배)
        표준편차가 평균의 최대 약 47%라 작은 N의 비율 순서는 대략적 값으로만 사용
            (N = 5에서는 표준편차 1~5%로 안정적)
        재귀는 for 누적곱보다 1.6~3배 느림 (함수 호출 비용)
        math.prod, reduce는 for 누적곱과 비슷한 수준 (0.4~1.5배 범위, 노이즈가 큼)
        math.perm(N)은 math.factorial과 같은 수준
        N이 4배(5,000 → 20,000)가 될 때 for 누적곱은 약 17.8배, math.factorial은 약 12.6배 증가
        (결과 정수가 계속 커져 곱셈 비용이 늘어나는 영향이며 math.factorial의 증가가 더 완만함)
        math.factorial이 빠른 이유는 C로 구현되어 있기 때문으로 보이나 내부 알고리즘은 확인하지 않음
        N = 5(공식 예시)의 절대 차이는 0.1µs 수준이라 이 문제에서는 의미가 없음

    Best 선정 근거:
        - 모든 N에서 가장 빠르거나 동률
        - 코드가 가장 짧고 입력 범위 오류(음수)를 ValueError로 명확히 알림
        - 직접 구현한 풀이와 비교해 정확성을 검증할 기준으로도 사용 가능
    일반성 대가:
        - 직접 구현이 목적이면 알고리즘 학습 효과가 없음
================================================================================
[개선 포인트]
    solution_mine_one   : 개선 여지 작음 - 명시적이며 재귀 한도와 무관, math.factorial보다는 느림
    solution_mine_two   : 개선 여지 없음 - 실측 최상위
    solution_mine_three : 개선 여지 있음 - 호출 비용과 재귀 깊이 한도 (N 약 1000 미만) 문제
    solution_best       : math.factorial - Best (mine_two와 동일)
================================================================================
[복잡도 분석]
    N = 입력 정수 (큰 정수 곱셈 비용 포함, 결과는 약 N log N 비트)

    Mine_one   - 시간: 곱셈 N회, 각 곱셈이 현재 결과 크기에 비례 (실측 N 4배에 약 17.8배)
                 공간: O(결과 크기)
    Mine_two   - 시간: 곱셈 횟수는 같으나 실측 증가가 더 완만 (N 4배에 약 12.6배)
                 공간: O(결과 크기)
    Mine_three - 시간: for 누적곱과 같은 곱셈 N회 + 호출 N회
                 공간: 호출 스택 O(N) + 결과 크기 (깊이 한도 때문에 N 약 1000 미만)
    Best       - mine_two와 동일
"""

import math
import time


# ================================================================================
# Mine solution one - for 누적곱
# ================================================================================
def solution_mine_one(N: int) -> int:
    """
    2부터 N까지 차례로 곱해 누적하는 직접 작성한 풀이

    핵심:
        result = 1에서 시작 (0!과 1!은 반복 없이 1)
        range(2, N + 1) : 2부터 N까지 (끝이 미포함이라 N + 1)
        재귀 깊이 한도와 무관
    """
    result = 1
    for i in range(2, N + 1):
        result *= i

    return result


# ================================================================================
# Mine solution two - math.factorial
# ================================================================================
def solution_mine_two(N: int) -> int:
    """
    math 내장 라이브러리의 factorial을 사용하는 직접 작성한 풀이

    핵심:
        math.factorial(N) : C로 구현된 팩토리얼
        음수 입력은 ValueError
    """
    return math.factorial(N)


# ================================================================================
# Mine solution three - 재귀
# ================================================================================
def solution_mine_three(N: int) -> int:
    """
    f(n) = n * f(n - 1)의 재귀 구조로 계산하는 직접 작성한 풀이

    핵심:
        종료 조건 : n <= 1 이면 1 (0!과 1!)
        재귀 호출 : n * f(n - 1)
        함수 안의 재귀 함수는 자기 자신(f)을 호출해야 함 (바깥 이름을 호출하면 NameError)

    한계:
        재귀 깊이 한도(기본 1000)로 N이 약 1000 이상이면 RecursionError
    """
    def f(n: int) -> int:
        if n <= 1:
            return 1
        return n * f(n - 1)

    return f(N)


# ================================================================================
# Best solution - math.factorial
# ================================================================================
def solution_best(N: int) -> int:
    """
    math.factorial을 사용하는 최적 풀이 (mine_two와 동일)

    핵심:
        실측에서 for 누적곱보다 약 3~10배 빠름
        재귀 깊이 한도와 무관, 음수는 ValueError로 명확히 알림
    """
    return math.factorial(N)


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    def summarize(value: int) -> tuple[int, int, int]:
        """대용량 결과를 직접 적을 수 없어 요약 값(자릿수, 끝의 0 개수, 907로 나눈 나머지)으로 비교"""
        s = str(value)
        return len(s), len(s) - len(s.rstrip("0")), value % 907

    big_n = 906

    test_cases: list[tuple] = [
        # (N, 기댓값) - 전부 손 계산
        (5, 120),                                  # 공식 예시
        (0, 1),                                    # 0! = 1 (빈 곱)
        (1, 1),
        (2, 2),
        (3, 6),
        (10, 3628800),
        (12, 479001600),
        (20, 2432902008176640000),                 # 부호 있는 64비트 정수에 들어가는 마지막 팩토리얼
        (21, 51090942171709440000),                # 21 * 20!
        (25, 15511210043330985984000000),
        # 대용량: 906! (재귀 깊이 한도 안에서 가능한 크기), 요약 값의 기댓값은 닫힌 형태 공식으로 계산
        #   자릿수      = floor(log10(906!)) + 1 = floor(lgamma(907) / ln 10) + 1
        #   끝의 0 개수 = 906 // 5 + 906 // 25 + 906 // 125 + 906 // 625 = 181 + 36 + 7 + 1 = 225
        #   907은 소수 → 윌슨 정리: 906! ≡ -1 (mod 907) → 나머지 906
        (big_n, (int(math.lgamma(big_n + 1) / math.log(10)) + 1,
                 big_n // 5 + big_n // 25 + big_n // 125 + big_n // 625,
                 906)),
    ]

    def is_correct(output: int, expected) -> bool:
        if isinstance(expected, tuple):
            return summarize(output) == expected
        return output == expected

    solutions = [
        ("Mine one (for 누적곱)", solution_mine_one),
        ("Mine two (math)",       solution_mine_two),
        ("Mine three (재귀)",      solution_mine_three),
        ("Best (math)",           solution_best),
    ]

    # 워밍업: 첫 테스트 케이스로 모든 풀이를 1회씩 실행
    warmup_args = test_cases[0][:-1]
    for _, func in solutions:
        func(*warmup_args)

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'평균 소요시간':>12}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (*args, expected) in enumerate(test_cases, 1):
            output = func(*args)

            start = time.perf_counter()
            for _ in range(repeat):
                func(*args)
            elapsed = (time.perf_counter() - start) / repeat

            status = "PASS" if is_correct(output, expected) else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed*1000:>10.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
