"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 시저 암호
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12926
    풀이일자   : 2026-07-03
===================================================================================
[문제 요약]
    문자열 s의 각 알파벳을 n만큼 밀어서 암호화
    대소문자 구분, 공백은 그대로, 알파벳 끝에서 순환

    제약 조건
        - s 길이: 8,000 이하
        - s: 알파벳 소문자, 대문자, 공백으로만 구성
        - n: 1 이상 25 이하 자연수
          → n % 26 처리 불필요 (범위 보장)
===================================================================================
[입출력 예시]
    s       | n | result
    --------|---|-------
    "AB"    | 1 | "BC"
    "z"     | 1 | "a"
    "a B z" | 4 | "e F d"
===================================================================================
[시저 암호 핵심 수학]
    아스키 코드 기반 shift 공식:
        chr((ord(char) - base + n) % 26 + base)
        base: 대문자 65('A'), 소문자 97('a')

    손 추적 (char='Z', n=1, base=65):
        ord('Z') = 90
        90 - 65 = 25      → 0-indexed 위치 (Z=25번째)
        25 + 1  = 26      → n만큼 shift
        26 % 26 = 0       → 순환 (26 → 0, 'A'로 돌아옴)
        0 + 65  = 65      → 아스키 복원
        chr(65) = 'A' ✓

    손 추적 (char='a', n=4, base=97):
        ord('a') = 97
        97 - 97 = 0       → 0-indexed (a=0번째)
        0 + 4   = 4       → shift
        4 % 26  = 4       → 순환 없음
        4 + 97  = 101
        chr(101) = 'e' ✓
===================================================================================
[maketrans + translate 방식]
    str.maketrans(from_str, to_str): from_str 각 문자를 to_str 대응 문자로
                                     매핑하는 변환 테이블(dict) 생성
    str.translate(table): table 기반으로 문자열 일괄 치환

    슬라이싱으로 shift된 알파벳 문자열 생성:
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        n=1: upper[1:] + upper[:1] = "BCDEFGHIJKLMNOPQRSTUVWXYZA"
             A→B, B→C, ..., Z→A 매핑

    주의 — 슬라이싱 방향:
        lower[n:] + lower[:n]  → n만큼 shift (정답)
        lower[:n] + lower[n:]  → 원본 그대로 (shift 없음, 오답)

    공백 처리:
        maketrans에 포함되지 않은 문자 → translate가 그대로 유지
        → 별도 공백 처리 코드 불필요
===================================================================================
[내 초기 풀이]
    solution_mine_one: ord/chr + 아스키 수학으로 직접 shift
    solution_mine_two: maketrans + translate 일괄 치환

    solution_mine_two 슬라이싱 주의점:
        lower[:n] + lower[n:] = 원본 (shift 없음)
        lower[n:] + lower[:n] = n만큼 shift ✓

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Sub
        아스키 수학 원리가 코드에 직접 드러남, 가독성 우위
    solution_mine_two: 개선 필요 없음 - Best
        maketrans + translate: C 레벨 일괄 치환으로 가장 빠름
        공백 자동 처리, 코드 간결
===================================================================================
[복잡도 분석]
    N = len(s) (최대 8,000)

    Mine_one - 시간: O(N) | 공간: O(N) - 문자별 순회 + answer 문자열 누적
    Mine_two - 시간: O(N) | 공간: O(1) - maketrans O(1) + translate O(N)
    Best     - 시간: O(N) | 공간: O(1) - Mine_two와 동일, 주석 보강
    Sub      - 시간: O(N) | 공간: O(N) - Mine_one과 동일, 주석 보강

    translate: C 레벨 일괄 처리 → Python 루프(Sub) 대비 상수 인자 작음
    maketrans 테이블: 최대 52개 항목(알파벳 대소문자) → O(1) 상수
"""

import string
import time


# =================================================================================
# Mine solution one - ord/chr 아스키 수학 직접 shift
# =================================================================================
def solution_mine_one(s: str, n: int) -> str:
    """
    ord()와 chr()로 아스키 코드 값을 직접 조작해 shift하는 초기 풀이

    핵심 수식:
        chr((ord(char) - base + n) % 26 + base)
        - base 빼기: 0-indexed 알파벳 위치로 변환
        - +n: n만큼 shift
        - %26: 알파벳 범위 순환 ('z' 이후 'a'로)
        - +base: 아스키 코드 복원

    공백 처리:
        else 분기로 변환 없이 그대로 추가
    """
    answer = ''

    for char in s:
        if 'A' <= char <= 'Z':
            answer += chr((ord(char) - 65 + n) % 26 + 65)
        elif 'a' <= char <= 'z':
            answer += chr((ord(char) - 97 + n) % 26 + 97)
        else:
            answer += char  # 공백 등 알파벳 아닌 문자 그대로

    return answer


# =================================================================================
# Mine solution two - maketrans + translate 일괄 치환
# =================================================================================
def solution_mine_two(s: str, n: int) -> str:
    """
    maketrans로 변환 테이블을 만들고 translate로 일괄 치환하는 풀이

    shift된 알파벳 문자열 생성:
        upper[n:] + upper[:n]: 앞 n개를 뒤로 보냄
        n=1: "BCDEFGHIJKLMNOPQRSTUVWXYZA" (A→B, B→C, ..., Z→A)

    슬라이싱 방향 주의:
        upper[n:] + upper[:n] → n shift ✓
        upper[:n] + upper[n:] → 원본 그대로 (오답)

    str.maketrans(from, to):
        from의 각 문자를 to의 대응 문자로 매핑하는 변환 테이블 반환
        변환 테이블에 없는 문자(공백 등)는 translate가 그대로 유지

    Best 대비 동일, maketrans + translate가 C 레벨 처리로 가장 빠름
    """
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase

    shifted_upper = upper[n:] + upper[:n]
    shifted_lower = lower[n:] + lower[:n]

    table = str.maketrans(upper + lower, shifted_upper + shifted_lower)

    return s.translate(table)


# =================================================================================
# Best solution - maketrans + translate (mine_two 주석 보강)
# =================================================================================
def solution_best(s: str, n: int) -> str:
    """
    maketrans + translate로 일괄 치환하는 최적 풀이

    mine_two와 동일한 로직, 근거 주석 보강:
        translate: C 레벨 구현으로 Python 루프(Sub) 대비 상수 인자 작음
        공백: maketrans 테이블에 없는 문자 → translate가 자동으로 그대로 유지
        maketrans 테이블: 52개 항목(대소문자 각 26개) → O(1) 생성
    """
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase

    shifted_upper = upper[n:] + upper[:n]   # n만큼 앞글자를 뒤로
    shifted_lower = lower[n:] + lower[:n]

    table = str.maketrans(upper + lower, shifted_upper + shifted_lower)
    return s.translate(table)


# =================================================================================
# Sub solution - ord/chr 아스키 수학 (mine_one 주석 보강)
# =================================================================================
def solution_sub(s: str, n: int) -> str:
    """
    아스키 수학으로 시저 암호 원리를 직접 표현하는 서브 풀이

    Best 대비 특징:
        ord/chr로 shift 수식을 명시적으로 표현
        시저 암호 동작 원리(0-indexed 변환 → shift → 순환 → 복원)가 코드에 드러남
        Python 루프 → C 레벨 translate 대비 상수 인자 큼
        공백을 else 분기로 명시적 처리
    """
    answer = ''

    for char in s:
        if 'A' <= char <= 'Z':
            answer += chr((ord(char) - 65 + n) % 26 + 65)
        elif 'a' <= char <= 'z':
            answer += chr((ord(char) - 97 + n) % 26 + 97)
        else:
            answer += char

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int, str]] = [
        # (s, n, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # "AB", n=1: A→B, B→C → "BC"
        ("AB",    1, "BC"),
        # "z", n=1: z→a (순환) → "a"
        ("z",     1, "a"),
        # "a B z", n=4: a→e, ' '→' ', B→F, ' '→' ', z→d → "e F d"
        ("a B z", 4, "e F d"),
        # 추가 케이스:
        # 순환 확인: "XYZ", n=3: X→A, Y→B, Z→C
        ("XYZ",   3, "ABC"),
        # 공백 여러 개: "A Z", n=1: A→B, ' '→' ', Z→A
        ("A Z",   1, "B A"),
    ]

    solutions = [
        ("Mine_one (ord/chr)     ", solution_mine_one),
        ("Mine_two (maketrans)   ", solution_mine_two),
        ("Best     (maketrans)   ", solution_best),
        ("Sub      (ord/chr)     ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _n, _ = test_cases[0]
    for _, func in solutions:
        func(_s, _n)

    print("=" * 64)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (s, n, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s, n)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
