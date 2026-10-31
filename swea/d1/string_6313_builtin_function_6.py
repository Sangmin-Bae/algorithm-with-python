"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6313. [파이썬 프로그래밍 기초(1) 파이썬의 기본 구조와 기초 문법] 9. 내장함수 6
    유형       : String (ASCII 코드 → 문자 변환, chr)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcWETX65WADFAU4&categoryId=AWcWETX65WADFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=4
    풀이일자   : 2026-10-31
================================================================================
[문제 요약]
    ASCII 코드 값을 입력받아 해당 문자를 "ASCII 코드값 => 문자" 형식으로 출력

    입력 방식 : ASCII 코드 값 정수 한 개
    적용 방식 : 입력 → 매개변수 n, output → 형식에 맞는 문자열을 반환
================================================================================
[입출력 예시]
    공식 예시
    n  | return
    ---|--------------------
    65 | "ASCII 65 => A"

    자체 검증 케이스 (전부 손 계산, ASCII 표 기준)
    n   | return
    ----|----------------------
    48  | "ASCII 48 => 0"      ('0'의 코드)
    65  | "ASCII 65 => A"      ('A'의 코드)
    90  | "ASCII 90 => Z"
    97  | "ASCII 97 => a"      ('a'의 코드, 'A'보다 32 큼)
    122 | "ASCII 122 => z"
    32  | "ASCII 32 => " + " " (공백 문자)
    126 | "ASCII 126 => ~"
================================================================================
[풀이 전략]
    핵심: chr(n)
        chr(정수) : 해당 코드 값의 문자 반환 (ord의 반대)
        chr은 유니코드 코드 포인트를 받음, 0~127 범위에서는 ASCII와 동일
        (예: chr(233) == 'é', ASCII 범위 밖)

    출력 형식:
        f"ASCII {n} => {chr(n)}" : 정수와 문자를 문자열 안에 바로 삽입

    풀이 구성:
        mine_one : f-string + chr (직접 작성한 풀이)
        best     : mine_one과 동일 (% 포맷, format, 문자열 연결도 같은 결과이나
                   f-string이 가장 간결하고 변환 없이 값을 바로 삽입)
        Sub는 차별점 있는 변형이 없어 생략

    손 추적 (공식 예시) n = 65:
        chr(65) → 'A'
        f"ASCII {65} => {'A'}" → "ASCII 65 => A" ✓
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 없음 - 내장 함수 chr과 f-string으로 간결
    solution_best     : mine_one과 동일 로직 - Best
================================================================================
[복잡도 분석]
    Mine_one - 시간: O(1) | 공간: O(1) - 문자 1개 변환 후 짧은 문자열 생성
    Best     - 시간: O(1) | 공간: O(1) - mine_one과 동일
"""

import time


# ================================================================================
# Mine solution one - chr + f-string
# ================================================================================
def solution_mine_one(n: int) -> str:
    """
    chr로 ASCII 코드 값을 문자로 변환하고 f-string으로 형식을 만드는 직접 작성한 풀이

    핵심:
        chr(n) : 코드 값 → 문자
        f-string : 코드 값과 문자를 형식에 맞게 삽입
    """
    return f"ASCII {n} => {chr(n)}"


# ================================================================================
# Best solution - mine_one과 동일 로직
# ================================================================================
def solution_best(n: int) -> str:
    """
    mine_one과 동일한 로직의 최적 풀이

    선정 근거:
        내장 함수 한 번과 f-string 한 줄로 가장 간결
    """
    return f"ASCII {n} => {chr(n)}"


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (n, 기댓값) - 전부 손 계산 (ASCII 표 기준)
        (65, "ASCII 65 => A"),                              # 공식 예시
        (48, "ASCII 48 => 0"),                              # 숫자 '0'
        (90, "ASCII 90 => Z"),                              # 대문자 끝
        (97, "ASCII 97 => a"),                              # 소문자 시작
        (122, "ASCII 122 => z"),                            # 소문자 끝
        (32, "ASCII 32 =>  "),                              # 공백 문자
        (126, "ASCII 126 => ~"),                            # 출력 가능 문자의 끝
    ]

    solutions = [
        ("Mine (f-string)", solution_mine_one),
        ("Best (f-string)", solution_best),
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

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed*1000:>10.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
