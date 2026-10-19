"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 2047. 신문 헤드라인
    유형       : String (대소문자 변환)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5QKsLaAy0DFAUq&categoryId=AV5QKsLaAy0DFAUq&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=3
    풀이일자   : 2026-10-19
================================================================================
[문제 요약]
    문자열에서 알파벳 소문자를 모두 대문자로 바꿔 출력

    입력 방식 : 문자열 한 줄 (최대 80 bytes)
    적용 방식 : 입력 → 매개변수 s, output → 반환값
                제출 시에는 입력을 받아 반환값을 print
    참고      : 소문자가 아닌 문자(대문자, 숫자, 기호)는 그대로 유지
================================================================================
[입출력 예시]
    공식 예시
    s                                                                         | return
    --------------------------------------------------------------------------|-------------------------------------------------------------------------
    The_headline_is_the_text_indicating_the_nature_of_the_article_below_it.   | THE_HEADLINE_IS_THE_TEXT_INDICATING_THE_NATURE_OF_THE_ARTICLE_BELOW_IT.

    자체 검증 케이스 (전부 손 계산)
    s                | return
    -----------------|-----------------
    ""               | ""              (빈 문자열)
    "abc"            | "ABC"
    "ABC_123"        | "ABC_123"       (소문자 없음, 변화 없음)
    "a-b c.d!"       | "A-B C.D!"      (기호와 공백 유지)
    "az`{"           | "AZ`{"          (소문자 경계: 'a'~'z' 바로 앞 '`', 바로 뒤 '{'는 변환되지 않음)
    "a" * 80         | "A" * 80        (최대 길이)
    "ab_" * 333333   | "AB_" * 333333  (대용량, 닫힌 식으로 기댓값 계산)
================================================================================
[풀이 전략]
    핵심: str.upper()
        문자열의 모든 소문자를 대문자로 바꾼 새 문자열 반환
        소문자가 아닌 문자(대문자, 숫자, 기호)는 그대로 유지
        원본 문자열은 변경되지 않음 (문자열은 불변)
        비ASCII 문자도 변환 대상 ('ß'.upper() == 'SS'), 이 문제는 영문 입력 기준이라 해당 없음

    풀이 구성:
        mine_one : s.upper() (직접 작성한 풀이)
        best     : mine_one과 동일 (내장 메서드 한 번 호출, 더 나은 변형이 없음)

    손 추적 (공식 예시 앞부분) s = "The_headline...":
        'T' → 'T' (이미 대문자)
        'h' → 'H', 'e' → 'E'
        '_' → '_' (기호 유지)
        → "THE_" ... 이하 동일하게 변환 → 예시 출력과 일치 ✓
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 없음 - 내장 메서드 한 번 호출
    solution_best     : mine_one과 동일 로직 - Best
================================================================================
[복잡도 분석]
    n = len(s)

    Mine_one - 시간: O(n) | 공간: O(n) - 문자열 전체를 훑어 새 문자열 생성
    Best     - 시간: O(n) | 공간: O(n) - mine_one과 동일
"""

import time


# ================================================================================
# Mine solution one - str.upper()
# ================================================================================
def solution_mine_one(s: str) -> str:
    """
    str.upper() 메서드로 소문자를 대문자로 변환하는 직접 작성한 풀이

    핵심:
        s.upper() : 소문자만 대문자로 바꾸고 그 외 문자는 유지
        원본은 유지하고 새 문자열 반환
    """
    return s.upper()


# ================================================================================
# Best solution - mine_one과 동일 로직
# ================================================================================
def solution_best(s: str) -> str:
    """
    mine_one과 동일한 로직의 최적 풀이

    선정 근거:
        내장 메서드 한 번 호출로 가장 간결
    """
    return s.upper()


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (s, 기댓값) - 전부 손 계산
        ("The_headline_is_the_text_indicating_the_nature_of_the_article_below_it.",
         "THE_HEADLINE_IS_THE_TEXT_INDICATING_THE_NATURE_OF_THE_ARTICLE_BELOW_IT."),  # 공식 예시
        ("", ""),                                           # 빈 문자열 경계
        ("abc", "ABC"),                                     # 전부 소문자
        ("ABC_123", "ABC_123"),                             # 소문자 없음
        ("a-b c.d!", "A-B C.D!"),                           # 기호와 공백 유지
        ("az`{", "AZ`{"),                                   # 소문자 경계 바로 바깥 문자
        ("a" * 80, "A" * 80),                               # 최대 길이
        ("ab_" * 333333, "AB_" * 333333),                   # 대용량: 소문자만 변환
    ]

    solutions = [
        ("Mine (upper)", solution_mine_one),
        ("Best (upper)", solution_best),
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
