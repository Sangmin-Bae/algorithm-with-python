"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 문자열 다루기 기본
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12918
    풀이일자   : 2026-06-24
===================================================================================
[문제 요약]
    문자열 s의 길이가 4 또는 6이고 숫자로만 구성돼있는지 확인

    제약 조건
        - s 길이: 1 이상 8 이하
        - 영문 대소문자 또는 0~9 숫자로만 구성 (특수문자, 공백 없음)
        - 2022년 7월 테스트케이스 추가 (강화된 케이스 존재)
===================================================================================
[입출력 예시]
    s      | return
    -------|-------
    "a234" | False  (영문자 포함)
    "1234" | True   (길이 4, 숫자만 구성)
===================================================================================
[내 초기 풀이]
    solution_mine_one  : for 루프 + in 연산 + 조기 탈출
    solution_mine_two  : 정렬 트릭 — sorted(s)[-1]로 마지막 문자 판별
    solution_mine_three: 정규표현식 re.match(r'^[0-9]+$', s)
    solution_mine_four : s.isdecimal() 내장 메서드 활용

    isdecimal() 미생각 시 접근 순서:
        1단계(one)  : for 루프 + "0123456789" in 비교 → 조기 탈출
        2단계(two)  : 정렬 트릭으로 최댓값만 확인
        3단계(three): 정규표현식으로 패턴 매칭
        4단계(four) : isdecimal() 내장 메서드 (뒤늦게 기억)

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                        동작 원리를 코드로 직접 표현, 내장 함수 없이 구현
    solution_mine_two  : 정렬 트릭 — 범용성 낮음, O(N log N)으로 비효율
                        제약 조건(특수문자 없음) 덕에 통과하나 권장 안 함
    solution_mine_three: 정규표현식 — 이 문제에는 오버스펙
                        re.match()에서 ^ 중복 → re.fullmatch(r'[0-9]+', s)가 더 명확
    solution_mine_four : 개선 필요 없음 - Best
===================================================================================
[isdecimal() vs isdigit() vs isnumeric() 비교]
    isdecimal(): 10진수 숫자(0~9)만 True
    isdigit()  : 위첨자(²³) 등 수학적 기호도 True
    isnumeric(): 분수(½), 로마자 등 더 넓은 범위도 True

    예시:
        '²'.isdecimal() → False   '²'.isdigit() → True
        '½'.isnumeric() → True    '½'.isdigit() → False

    이 문제 제약: 영문 대소문자 또는 0~9만 → 위첨자 없음
    → isdigit()도 동작하나 isdecimal()이 더 엄격하고 안전한 선택

[solution_mine_two 정렬 트릭 취약점]
    sorted(s)[-1] in "0123456789":
        오름차순 정렬 후 마지막 문자가 숫자인지 확인
        숫자(ASCII 48~57) < 대문자(65~90) < 소문자(97~122)
        → 마지막 문자가 숫자면 모두 숫자 → True

    취약점:
        공백(ASCII 32)이나 특수문자가 포함되면 오판 가능
        예) "12 4": 공백=32 < 숫자 → sorted[-1]='4' → True (오답)
        이 문제 제약(영문 대소문자 또는 숫자만)으로 통과, 범용적이지 않음
        O(N log N) 정렬 비용 → 다른 풀이 대비 비효율

[solution_mine_three 정규표현식 개선]
    re.match(r'^[0-9]+$', s):
        re.match()는 문자열 시작부터 매칭 → ^ 중복
        re.match(r'[0-9]+$', s) 또는 re.fullmatch(r'[0-9]+', s)가 더 명확
        bool() 래핑: match 객체(truthy) 또는 None(falsy) → bool 변환

[len(s) O(1) 근거]
    CPython 문자열 객체는 생성 시 길이를 ob_size 필드에 저장
    len(s) 호출 = 저장된 값 읽기 → O(1)
    리스트도 동일 → len(list) = O(1)
    → 변수에 담지 않고 직접 사용해도 비용 없음
===================================================================================
[복잡도 분석]
    N = len(s) (최대 8, 사실상 상수)

    Mine_one   - 시간: O(N)       | 공간: O(1) - for 루프 + 조기 탈출
    Mine_two   - 시간: O(N log N) | 공간: O(N) - sorted() 정렬 + 결과 리스트
    Mine_three - 시간: O(N)       | 공간: O(1) - 정규표현식 매칭
    Mine_four  - 시간: O(N)       | 공간: O(1) - isdecimal() 내부 순회
    Best       - 시간: O(N)       | 공간: O(1) - Mine_four와 동일, 주석 보강
    Sub        - 시간: O(N)       | 공간: O(1) - Mine_one과 동일, 주석 보강

    N ≤ 8 고정 → 모든 풀이 실질적으로 O(1)에 수렴
    Mine_two: O(N log N) 정렬 → 다른 풀이 대비 불필요한 비용
"""

import re
import time
from typing import List, Tuple


# =================================================================================
# Mine solution one - for 루프 + in 연산 + 조기 탈출
# =================================================================================
def solution_mine_one(s: str) -> bool:
    """
    for 루프로 순회하며 숫자가 아닌 문자 발견 시 즉시 False 반환하는 초기 풀이

    핵심:
        len(s) != 4 and len(s) != 6: 길이 조건 불만족 → 즉시 False
        i not in "0123456789": 숫자가 아닌 문자 발견 → 즉시 False (조기 탈출)
        default return True: 모든 조건 통과

    len(s) O(1):
        CPython 문자열 객체 내 ob_size 저장값 조회 → 변수 불필요
    """
    if len(s) != 4 and len(s) != 6:
        return False

    for i in s:
        if i not in "0123456789":   # 숫자 아닌 문자 발견 → 조기 탈출
            return False

    return True


# =================================================================================
# Mine solution two - 정렬 트릭 (sorted(s)[-1] 판별)
# =================================================================================
def solution_mine_two(s: str) -> bool:
    """
    정렬 후 마지막 문자가 숫자인지 확인하는 트릭 풀이

    아이디어:
        숫자(48~57) < 대문자(65~90) < 소문자(97~122) (ASCII 순서)
        오름차순 정렬 시 숫자가 앞, 영문자가 뒤
        마지막 문자가 숫자 → 전체가 숫자로만 구성

    취약점:
        공백(32), 특수문자 등이 포함되면 오판 가능
        이 문제 제약(영문 대소문자 또는 숫자만)으로 통과하나 범용적이지 않음
        O(N log N) 정렬 비용 → 다른 풀이 대비 비효율

    학습 의의:
        ASCII 코드 순서를 활용한 트릭 방식
        제약 조건이 보장하는 범위 안에서만 안전한 패턴
    """
    return (len(s) == 4 or len(s) == 6) and sorted(s)[-1] in "0123456789"


# =================================================================================
# Mine solution three - 정규표현식 re.match
# =================================================================================
def solution_mine_three(s: str) -> bool:
    """
    정규표현식으로 숫자 구성 여부를 판별하는 풀이

    r'^[0-9]+$':
        ^: 문자열 시작 (re.match는 이미 시작부터 매칭 → ^ 중복)
        [0-9]+: 0~9 숫자가 하나 이상
        $: 문자열 끝
        → re.fullmatch(r'[0-9]+', s)가 더 명확한 동치 표현

    re.match 반환값:
        패턴 일치: match 객체 (truthy)
        불일치:   None (falsy)
        bool() 래핑으로 bool 변환

    이 문제에는 오버스펙:
        단순 숫자 구성 판별에 정규표현식 엔진 초기화 비용 불필요
        대규모 패턴 매칭이나 복잡한 조건 검증에 적합
    """
    return (len(s) == 4 or len(s) == 6) and bool(re.match(r'^[0-9]+$', s))


# =================================================================================
# Mine solution four - s.isdecimal() 내장 메서드
# =================================================================================
def solution_mine_four(s: str) -> bool:
    """
    isdecimal()로 10진수 구성 여부를 판별하는 풀이

    isdecimal() vs isdigit():
        isdecimal(): 순수 10진수(0~9)만 True
        isdigit()  : 위첨자(²³) 등 수학적 기호도 True
        → isdecimal()이 더 엄격하고 안전한 선택
        이 문제 제약(영문 대소문자 또는 숫자만)에서는 둘 다 동일하게 동작

    and 단락 평가:
        길이 조건 False → isdecimal() 미평가 (단락 평가)
        길이 조건 True  → isdecimal() 평가
    """
    return (len(s) == 4 or len(s) == 6) and s.isdecimal()


# =================================================================================
# Best solution - isdecimal() (mine_four 주석 보강)
# =================================================================================
def solution_best(s: str) -> bool:
    """
    isdecimal()로 10진수 구성 여부를 판별하는 최적 풀이

    mine_four와 동일한 로직, 근거 주석 보강:
        (len(s) == 4 or len(s) == 6): 길이 조건, len(s)는 O(1)
        s.isdecimal(): 문자열 전체가 0~9 10진수만 구성 → O(N) 내부 순회
        가장 직접적이고 의도가 명확한 표현
        for 루프(Sub) 대비 C 레벨 구현으로 내부 처리
    """
    return (len(s) == 4 or len(s) == 6) and s.isdecimal()


# =================================================================================
# Sub solution - for 루프 + 조기 탈출 (mine_one 주석 보강)
# =================================================================================
def solution_sub(s: str) -> bool:
    """
    for 루프 + 조기 탈출로 동작 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        isdecimal() 없이 직접 순회하며 숫자 여부 확인
        숫자 아닌 문자 발견 즉시 return False → 조기 탈출
        동작 원리(문자별 범위 확인)가 코드에 직접 드러남

    "0123456789" in 비교:
        문자열 in 연산: O(K), K=10 → O(1) 상수
        매 문자마다 "0~9" 범위 내 존재 여부 확인
    """
    if len(s) != 4 and len(s) != 6:
        return False

    for i in s:
        if i not in "0123456789":
            return False            # 숫자 아닌 문자 발견 → 즉시 False

    return True


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[str, bool]] = [
        # (s, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # "a234": len=4 ✓, 'a' not in "0~9" → False
        ("a234",    False),
        # "1234": len=4 ✓, 모두 숫자 → True
        ("1234",    True),
        # 추가 케이스:
        # "123456": len=6 ✓, 모두 숫자 → True
        ("123456",  True),
        # "1234567": len=7 → 길이 불만족 → False
        ("1234567", False),
        # "12a4": len=4 ✓, 'a' 포함 → False
        ("12a4",    False),
        # "ABCD": len=4 ✓, 영문자 → False
        ("ABCD",    False),
        # "123": len=3 → 길이 불만족 → False
        ("123",     False),
        # "1234A6": len=6 ✓, 'A' 포함 → False
        ("1234A6",  False),
    ]

    solutions = [
        ("Mine_one   (for+in)      ", solution_mine_one),
        ("Mine_two   (정렬트릭)    ", solution_mine_two),
        ("Mine_three (정규표현식)  ", solution_mine_three),
        ("Mine_four  (isdecimal)   ", solution_mine_four),
        ("Best       (isdecimal)   ", solution_best),
        ("Sub        (for+in)      ", solution_sub),
    ]

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
