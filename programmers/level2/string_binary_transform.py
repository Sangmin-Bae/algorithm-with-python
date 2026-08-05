"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 이진 변환 반복하기
    유형       : String / Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/70129
    풀이일자   : 2026-08-05
================================================================================
[문제 요약]
    '0'과 '1'로 이루어진 문자열 s가 '1'이 될 때까지 이진 변환을 반복
    반환: [이진 변환 횟수, 제거된 '0'의 총 개수]

    이진 변환:
        1. s의 모든 '0'을 제거
        2. 남은 길이(='1'의 개수)를 2진수 문자열로 변환

    제약 조건
        - s 길이: 1 이상 150,000 이하
        - s에 '1'이 최소 하나 이상 포함 (count('1') == 0인 경우 없음)
================================================================================
[입출력 예시]
    s                | result
    -----------------|-------
    "110010101001"   | [3, 8]
    "01110"          | [3, 3]
    "1111111"        | [4, 1]
================================================================================
[핵심 발상 — '0'을 세지 말고 '1'을 세라]
    이진 변환 후 s = format('1'의 개수, 'b')
    즉: '0'을 제거한 문자열의 길이 == '1'의 개수

    solution_one:
        count('0') → replace('0','') → format(len(s),'b')
        count와 replace 두 번 문자열 순회 + 새 문자열 객체 생성

    solution_two:
        count('1') → len(s)-one_cnt → format(one_cnt,'b')
        count 한 번 순회만 + 새 문자열 객체 생성 없음
        → replace 비용 완전 제거

[실측 결과 — N=10,000회 반복]
    케이스          | one(count+replace) | two(count1) | three(subn)
    ----------------|--------------------|--------------|-----------
    짧은 (12자)     | 0.002ms            | 0.001ms     | 0.002ms
    긴 (150,000 '1')| 0.196ms            | 0.149ms     | 0.052ms
    혼합 (01반복)   | 1.366ms            | 0.121ms     | 4.382ms  ← 가장 느림

    solution_two가 혼합 케이스에서 11배 빠른 이유:
        replace와 subn은 '0' 개수에 비례하는 치환 비용 발생
        solution_two는 치환 없이 count + 뺄셈만 수행

    solution_three(subn)가 느린 이유:
        정규표현식 엔진 오버헤드 + 치환 횟수에 비례하는 비용
        '0'이 많을수록 replace보다도 느려짐

[solution_four 재귀 방식]
    기저 조건: s == '1' → [times, zero_cnt] 반환
    s != '1': one_cnt 계산 → 재귀 호출
================================================================================
[내 초기 풀이]
    solution_mine_one  : count('0') + replace + format (직관적)
    solution_mine_two  : count('1') + 뺄셈 + format (replace 제거)
    solution_mine_three: re.subn + format
    solution_mine_four : 재귀 방식 (mine_two 로직 재귀화)

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         지문 로직과 1:1 대응, 직관적
                         count + replace로 두 번 순회
    solution_mine_two  : 개선 필요 없음 - Best
                         replace 없이 count('1') + 뺄셈만으로 처리
                         혼합 케이스에서 one 대비 11배 빠름
    solution_mine_three: re.subn 사용
                         정규표현식 오버헤드로 혼합 케이스에서 가장 느림
                         단순 문자 치환에는 replace가 적합
    solution_mine_four : 재귀 방식, mine_two와 동일한 로직
                         실측 while과 성능 차이 없음 (K가 극히 작아 함수 호출
                         오버헤드가 s.count('1') O(N) 비용에 묻힘)
================================================================================
[복잡도 분석]
    N = len(s), K = 이진 변환 횟수 (s가 최대 150,000이면 K는 매우 작음)

    이진 변환 횟수 K:
        각 변환마다 s 길이가 log₂(N) 수준으로 급격히 감소
        실제 K는 수십 회 이내

    Mine_one   - 시간: O(N×K) | 공간: O(N) - count+replace 각 O(N) × K번
    Mine_two   - 시간: O(N×K) | 공간: O(1) - count('1') O(N) × K번, 새 문자열 없음
    Mine_three - 시간: O(N×K) | 공간: O(N) - subn O(N) + 정규식 오버헤드 × K번
    Mine_four  - 시간: O(N×K) | 공간: O(K) - 재귀 스택 K 깊이
                                              실측 K≈3 (혼합 케이스), while과 차이 없음
    Best       - 시간: O(N×K) | 공간: O(1) - Mine_two와 동일
    Sub        - 시간: O(N×K) | 공간: O(N) - Mine_one과 동일

    K가 작으므로 실질적 차이는 각 변환 단계의 상수 인자
    → '0'이 많은 케이스에서 replace 비용이 결정적
"""

import re
import time


# ================================================================================
# Mine solution one - count('0') + replace + format
# ================================================================================
def solution_mine_one(s: str) -> list[int]:
    """
    지문 로직과 1:1 대응하는 직관적인 초기 풀이

    각 이진 변환:
        s.count('0'): 제거할 '0' 개수 누적
        s.replace('0', ''): '0' 제거 후 새 문자열 생성
        format(len(s), 'b'): 남은 길이를 2진수 문자열로 변환

    한계:
        count('0'): O(N) 순회
        replace('0',''): O(N) 순회 + 새 문자열 객체 생성
        '0'이 많은 케이스에서 두 번 순회 비용 발생
    """
    times = 0
    zero_cnt = 0

    while s != '1':
        zero_cnt += s.count('0')
        s = s.replace('0', '')
        s = format(len(s), 'b')
        times += 1

    return [times, zero_cnt]


# ================================================================================
# Mine solution two - count('1') + 뺄셈 + format (replace 제거)
# ================================================================================
def solution_mine_two(s: str) -> list[int]:
    """
    '1'의 개수로 '0'을 세고 replace를 제거한 핵심 발상 풀이

    핵심 동치:
        '0' 제거 후 길이 == '1'의 개수
        → replace 없이 count('1') 하나로 처리 가능

    one_cnt = s.count('1'):
        이진 변환 후 s의 길이 = one_cnt
        zero_cnt += len(s) - one_cnt: '0' 개수 = 전체 - '1' 개수
        s = format(one_cnt, 'b'): 직접 '1' 개수를 변환

    replace 비용 완전 제거:
        새 문자열 객체 생성 없음 → '0'이 많은 케이스에서 압도적 우위
        혼합(01반복 75,000개) 케이스: mine_one 대비 11배 빠름
    """
    times = 0
    zero_cnt = 0

    while s != "1":
        one_cnt = s.count('1')
        zero_cnt += len(s) - one_cnt
        s = format(one_cnt, 'b')
        times += 1

    return [times, zero_cnt]


# ================================================================================
# Mine solution three - re.subn + format
# ================================================================================
def solution_mine_three(s: str) -> list[int]:
    """
    re.subn으로 '0' 제거와 개수를 동시에 처리하는 풀이

    re.subn(pattern, repl, string):
        re.sub와 동일하나 (치환된_문자열, 치환_횟수) 반환
        subn('0', '', s): '0' 제거 + 제거 개수 반환

    한계:
        정규표현식 엔진 오버헤드 존재
        단순 문자 하나('0') 치환에는 replace가 더 효율적
        '0'이 많은 케이스에서 mine_one보다도 느림

    re.compile 최적화:
        패턴을 함수 외부에서 컴파일하면 반복 호출 시 컴파일 비용 1회만
        하지만 단순 문자 패턴에서는 큰 효과 없음
    """
    pattern = re.compile('0')
    times = 0
    zero_cnt = 0

    while s != "1":
        s, cnt = pattern.subn('', s)
        zero_cnt += cnt
        s = format(len(s), 'b')
        times += 1

    return [times, zero_cnt]


# ================================================================================
# Mine solution four - 재귀 방식 (mine_two 로직 재귀화)
# ================================================================================
def solution_mine_four(s: str, times: int = 0, zero_cnt: int = 0) -> list[int]:
    """
    mine_two와 동일한 로직을 재귀 함수로 표현한 풀이

    기저 조건:
        s == '1' → [times, zero_cnt] 반환

    재귀 호출:
        format(one_cnt, 'b'): 다음 s
        times + 1: 변환 횟수 증가
        zero_cnt + curr_zero_cnt: 제거된 '0' 누적
    """
    if s == "1":
        return [times, zero_cnt]

    one_cnt = s.count('1')
    curr_zero_cnt = len(s) - one_cnt

    return solution_mine_four(format(one_cnt, 'b'), times + 1, zero_cnt + curr_zero_cnt)


# ================================================================================
# Best solution - count('1') + 뺄셈 + format (mine_two 주석 보강)
# ================================================================================
def solution_best(s: str) -> list[int]:
    """
    '1'의 개수만으로 replace 없이 이진 변환을 처리하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        replace 비용 완전 제거: '0' 제거 없이 '1' 개수만 추적
        혼합 케이스(150,000자): mine_one 1.366ms → 0.121ms (11배 향상)
        count('1') 한 번으로 이진 변환과 '0' 개수 계산 동시 처리
    """
    times = 0
    zero_cnt = 0

    while s != "1":
        one_cnt = s.count('1')
        zero_cnt += len(s) - one_cnt
        s = format(one_cnt, 'b')
        times += 1

    return [times, zero_cnt]


# ================================================================================
# Sub solution - count('0') + replace + format (mine_one 주석 보강)
# ================================================================================
def solution_sub(s: str) -> list[int]:
    """
    지문 이진 변환 로직을 그대로 표현하는 서브 풀이

    Best 대비 특징:
        count('0') + replace('0','') + format: 지문 단계와 1:1 대응
        이진 변환의 의미가 코드에 직접 드러남
        count + replace: O(N) 순회 2회 + 새 문자열 생성
        '0'이 많은 케이스에서 Best 대비 느림
    """
    times = 0
    zero_cnt = 0

    while s != '1':
        zero_cnt += s.count('0')
        s = s.replace('0', '')
        s = format(len(s), 'b')
        times += 1

    return [times, zero_cnt]


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, list[int]]] = [
        # (s, 기댓값)
        # 공식 예시
        ("110010101001", [3, 8]),
        ("01110",        [3, 3]),
        ("1111111",      [4, 1]),
        # 추가 케이스:
        ("1",            [0, 0]),   # 이미 '1' → 변환 없음
        ("10",           [1, 1]),   # 1회: '0' 1개 제거 → '1'
    ]

    solutions = [
        ("Mine_one   (count0+replace)", solution_mine_one),
        ("Mine_two   (count1+뺄셈)   ", solution_mine_two),
        ("Mine_three (subn)          ", solution_mine_three),
        ("Mine_four  (재귀)          ", solution_mine_four),
        ("Best       (count1+뺄셈)   ", solution_best),
        ("Sub        (count0+replace)", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
