"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : [1차] 비밀지도
    유형       : String / Bit Manipulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17681
    풀이일자   : 2026-05-30
================================================================================
[문제 요약]
    두 정수 배열 arr1, arr2를 이진수로 변환해 OR 비트 연산 후
    1→'#', 0→' '으로 치환한 문자열 배열 반환

    제약 조건
        - n: 1 이상 16 이하
        - 각 원소: 0 이상 2^n - 1 이하
================================================================================
[입출력 예시]
    n=5, arr1=[9,20,28,18,11], arr2=[30,1,21,17,28]
    → ["#####","# # #","### #","#  ##","#####"]
================================================================================
[핵심 아이디어 — OR 비트 연산]
    "하나라도 벽이면 벽" = OR 비트 연산
        0|0=0 (둘 다 공백 → ' ')
        0|1=1 (하나가 벽 → '#')
        1|0=1 (하나가 벽 → '#')
        1|1=1 (둘 다 벽  → '#')

    정수 단위 OR: 각 비트 자리마다 동시에 수행
        9  = 01001(2)
        30 = 11110(2)
        OR = 11111(2) → "#####"
================================================================================
[format() 함수 — 이진수 변환]
    format(value, format_spec)

    format_spec = "0{n}b" 구조:
        b: binary (이진수 변환)
        {n}: 전체 자릿수
        0: 빈 자리를 0으로 채움 (zero-padding)

    예시:
        format(9, "05b")       → "01001"  (5자리, 앞에 0 채움)
        format(9, f"0{n}b")   → n자리 이진수 (n이 동적일 때)

    f-string과의 관계:
        format(9, "05b") = f"{9:05b}" 동일한 결과
        `:` 뒤 형식이 format()의 두 번째 인자와 동일한 규칙

    bin() 대신 format()을 쓴 이유:
        bin(9) = "0b1001"  → "0b" prefix 제거 + 자릿수 맞추기 추가 작업 필요
        format(9, "05b")   → prefix 없이 자릿수 포함 한 번에 처리
================================================================================
[solution_two 복잡도 분석 — 네 분석 수정]
    네 분석: O(n³)  수정: O(n²)

    외부 for 루프         : O(N)  배열 n개 순회
    format(r1|r2, f"0{n}b"): O(N)  n자리 문자열 생성
    replace × 2           : O(N)  n자리 문자열 각 1회 순회

    전체: N × (N + N + N) = 3N² → O(N²)

    N ≤ 16 고정 → 최대 256연산 → 사실상 O(1)
    변수 구분 체크리스트:
        외부 루프 변수: N (배열 길이)
        내부 연산 변수: N (문자열 길이)
        → 같은 N의 중첩 → O(N²) (O(N³) 아님)
================================================================================
[int2bin 함수 — raw 이진수 변환]
    3진법 뒤집기 문제의 divmod 패턴과 동일한 구조:
        나머지를 순서대로 누적 → 역순(낮은 자리부터)
        [::-1]로 뒤집어 올바른 이진수 문자열
        zfill(n)으로 n자리 zero-padding

    k=0 엣지케이스:
        while k > 0 → 루프 진입 안함 → b=""
        "".zfill(n) → "000...0" (n자리) → 올바르게 처리됨
================================================================================
[복잡도 분석]
    N = n (최대 16)

    Mine_one   - 시간: O(N²) | 공간: O(N) — re.sub 단일 순회
    Mine_two   - 시간: O(N²) | 공간: O(N) — replace 2회 순회
    Mine_three - 시간: O(N²) | 공간: O(N) — int2bin + 문자 비교
    Best       - 시간: O(N²) | 공간: O(N) — 리스트 컴프리헨션
    Sub        - 시간: O(N²) | 공간: O(N) — re.sub 리스트 컴프리헨션

    N ≤ 16 고정 → 모든 풀이 사실상 O(1)
================================================================================
"""

import re
import time
from typing import List, Tuple


# ==============================================================================
# Mine solution one — OR 비트 + format + re.sub
# ==============================================================================
def solution_mine_one(n: int, arr1: List[int], arr2: List[int]) -> List[str]:
    """
    OR 비트 연산 후 format으로 이진수 변환, re.sub으로 문자 치환하는 풀이

    학습 내용 적용:
        - format(value, f"0{n}b"): n자리 이진수 변환 (zero-padding 포함)
        - re.sub + lambda: 이전 '숫자 문자열과 영단어' 세션에서 학습한 패턴

    이 케이스에서 re.sub보다 replace가 더 적합한 이유:
        치환 대상이 '1', '0' 두 개뿐 → replace 체인이 더 간결
        re.sub의 이점(단일 순회)이 크지 않음
    """
    answer = []
    table = {'1': '#', '0': ' '}
    pattern = '|'.join(table.keys())

    for r1, r2 in zip(arr1, arr2):
        # OR 비트 연산 → n자리 이진수 문자열 → re.sub으로 문자 치환
        answer.append(re.sub(pattern, lambda m: table[m.group()], format(r1 | r2, f"0{n}b")))

    return answer


# ==============================================================================
# Mine solution two — OR 비트 + format + replace 체인
# ==============================================================================
def solution_mine_two(n: int, arr1: List[int], arr2: List[int]) -> List[str]:
    """
    OR 비트 연산 후 format으로 이진수 변환, replace 체인으로 치환하는 풀이

    Mine_one 대비:
        re.sub 대신 replace 체인 사용
        치환 대상 2개뿐 → replace가 더 간결하고 직관적
        복잡도: O(N²) (N ≤ 16이라 사실상 O(1))
    """
    answer = []

    for r1, r2 in zip(arr1, arr2):
        # OR 비트 연산 → n자리 이진수 → '1'→'#' → '0'→' '
        answer.append(format(r1 | r2, f"0{n}b").replace('1', '#').replace('0', ' '))

    return answer


# ==============================================================================
# int2bin — raw 이진수 변환 헬퍼 함수
# ==============================================================================
def int2bin(k: int, n: int) -> str:
    """
    divmod로 2진수 변환하는 raw 구현
    '3진법 뒤집기' 문제의 divmod 패턴과 동일한 구조

    동작:
        나머지를 낮은 자리부터 누적 → [::-1]로 뒤집기 → zfill(n)으로 자릿수 맞추기
            k=0 처리: while 미진입 → "" → zfill(n) → "000...0" (정상 처리)
    """
    b = ""
    while k > 0:
        k, r = divmod(k, 2)
        b += str(r)         # 낮은 자리부터 누적
    return b[::-1].zfill(n) # 뒤집기 + n자리 zero-padding


# ==============================================================================
# Mine solution three — raw 이진수 변환 + 문자 비교
# ==============================================================================
def solution_mine_three(n: int, arr1: List[int], arr2: List[int]) -> List[str]:
    """
    내장 함수 없이 직접 구현한 raw 풀이

    목적:
        기본기 연습 — format, replace 없이 이진수 변환과 문자 비교를 직접 구현
        '3진법 뒤집기' 패턴(divmod + 뒤집기)을 다른 문제에 적용
    """
    answer = []

    for r1, r2 in zip(arr1, arr2):
        b_r1 = int2bin(r1, n)   # r1을 n자리 이진수 문자열로 변환
        b_r2 = int2bin(r2, n)   # r2를 n자리 이진수 문자열로 변환

        row = ""
        for e1, e2 in zip(b_r1, b_r2):
            if e1 == '1' or e2 == '1':  # 하나라도 '1' → 벽
                row += '#'
            else:                        # 둘 다 '0' → 공백
                row += ' '

        answer.append(row)

    return answer


# ==============================================================================
# Best solution — 리스트 컴프리헨션 + format + replace 체인
# ==============================================================================
def solution_best(n: int, arr1: List[int], arr2: List[int]) -> List[str]:
    """
    Mine_two를 리스트 컴프리헨션으로 압축한 최적 풀이

    Mine_two 대비 개선:
        answer 변수와 append() 제거
        리스트 컴프리헨션으로 한 줄 표현
    """
    return [format(r1 | r2, f"0{n}b").replace('1', '#').replace('0', ' ') for r1, r2 in zip(arr1, arr2)]


# ==============================================================================
# Sub solution — 리스트 컴프리헨션 + format + re.sub
# ==============================================================================
def solution_sub(n: int, arr1: List[int], arr2: List[int]) -> List[str]:
    """
    Mine_one을 리스트 컴프리헨션으로 압축하고 table을 함수 외부로 분리한 풀이

    Best 대비 특징:
        re.sub + lambda 방식 — 이전 학습 내용 적용
        치환 대상이 2개뿐이라 Best(replace)보다 코드가 복잡
    """
    table = {'1': '#', '0': ' '}
    pattern = '|'.join(table.keys())

    return [re.sub(pattern, lambda m: table[m.group()], format(r1 | r2, f"0{n}b")) for r1, r2 in zip(arr1, arr2)]


# ==============================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==============================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple] = [
        # (n, arr1, arr2, 기댓값)
        (5, [9,20,28,18,11], [30,1,21,17,28], ["#####","# # #","### #","#  ##","#####"]),
        (6, [46,33,33,22,31,50], [27,56,19,14,14,10], ["######","###  #","##  ##"," #### "," #####","### # "]),
        (1, [0], [0], [" "]),            # 최솟값: 둘 다 0 → 공백
        (1, [1], [0], ["#"]),            # 하나만 1 → 벽
        (16, [65535], [0], ["#"*16]),    # 최대 n, 최대 원소
    ]

    solutions = [
        ("Mine_one   (re.sub)",       solution_mine_one),
        ("Mine_two   (replace체인)",  solution_mine_two),
        ("Mine_three (raw구현)",      solution_mine_three),
        ("Best       (컴프리헨션)",   solution_best),
        ("Sub        (re.sub+컴프)",  solution_sub),
    ]

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (n, arr1, arr2, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, arr1[:], arr2[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 68)


# ==============================================================================
# 실행 진입점
# ==============================================================================
if __name__ == "__main__":
    solution_comparison()
