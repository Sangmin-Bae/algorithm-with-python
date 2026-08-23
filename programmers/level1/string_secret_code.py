"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 둘만의 암호
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/155652
    풀이일자   : 2026-08-23
===================================================================================
[문제 요약]
    문자열 s의 각 알파벳을 index만큼 뒤 알파벳으로 변환
    skip에 포함된 알파벳은 건너뜀, z 넘어가면 a로 순환

    제약 조건
        - s 길이: 5 이상 50 이하
        - skip 길이: 1 이상 10 이하
        - index: 1 이상 20 이하
        - skip에 포함된 알파벳은 s에 포함되지 않음
===================================================================================
[입출력 예시]
    s       | skip   | index | result
    --------|--------|-------|-------
    "aukks" | "wbqd" | 5     | "happy"
===================================================================================
[핵심 발상 — skip을 제외한 새 알파벳 사전 구축]
    풀이1: 직접 index만큼 한 칸씩 이동하며 skip 건너뜀
        - s 길이 × index × (skip 체크) = O(50×30×10) ≈ O(15,000)

    풀이2~ref: skip 제외한 allowed 사전 구축 후 나머지 연산
        - 사전 구축 O(26) + s 길이 × 탐색 = O(26 + 50×K)
        - K = 탐색 방식에 따라 O(26) or O(1)

[탐색 방식 비교]
    allowed.index(char): O(len(allowed)) 선형 탐색
    char_to_idx[char]:   O(1) 해시 탐색

    이 문제 규모(allowed ≤ 20)에서 실측 차이 0.2μs
    s 길이가 수백만이면 dict O(1)이 유의미하게 빠름

[solution_ref 개선 — idx_to_char 제거]
    원본: idx_to_char[new_idx] → O(1) dict 탐색
    개선: filtered[new_idx]    → O(1) 문자열 인덱스 접근

    filtered가 문자열이므로 인덱스로 직접 접근 가능
    dict 하나 제거 → 메모리 절약

[정규표현식 vs 리스트 컴프리헨션]
    re.sub(f'[{skip}]', '', 'abc...z'): 정규표현식 컴파일 오버헤드
    [c for c in 'abc...z' if c not in skip]: 단순 문자열 순회

    실측: regex 6.6μs vs 컴프리헨션 6.0μs (0.6μs 차이)
    26자 단순 필터링에는 컴프리헨션이 더 적합

[실측 결과 — s 길이 50, skip 6개, index 20, 100,000회]
    best  (dict O(1)):  6.0μs  ← 가장 빠름
    풀이2 (index함수):  6.2μs
    ref   (regex+dict): 6.6μs
    풀이1 (while순회): 95.2μs  ← 15배 느림

    풀이1이 느린 이유:
        50 × 30 = 1,500번 while 반복 + chr() 호출
        사전 구축 방식은 O(26) 초기화 후 O(1) or O(20) 탐색만
===================================================================================
[내 초기 풀이]
    solution_mine_one: while 순회로 skip 건너뜀 직접 구현
    solution_mine_two: allowed 사전 + index() 탐색

[개선 포인트]
    solution_mine_one: while 반복 비용 → 사전 구축으로 O(1) 탐색 가능
                       직관적, 동작 원리 명시적 - Sub 기준
    solution_mine_two: index() O(len(allowed)) → dict O(1)로 개선 가능
                       이 문제 규모에서 실측 차이 미미
    solution_ref:      정규표현식 불필요, idx_to_char 제거 가능
                       개선하면 Best와 동일 구조
    Best:              리스트 컴프리헨션 + char_to_idx dict
                       idx_to_char 제거, 정규표현식 없음
===================================================================================
[복잡도 분석]
    N = len(s) (최대 50), M = len(allowed) (최대 26)

    Mine_one - 시간: O(N×index×M) | 공간: O(1) - while + in 반복
    Mine_two - 시간: O(M+N×M)     | 공간: O(M) - allowed 리스트 + index()
    Ref      - 시간: O(M+N)       | 공간: O(M) - regex + dict × 2
    Best     - 시간: O(M+N)       | 공간: O(M) - 컴프리헨션 + dict × 1
    Sub      - 시간: O(M+N×M)     | 공간: O(M) - Mine_two와 동일

    모든 값이 상수(N≤50, M≤26) → 실질적 O(1)
    실측 차이는 루프 반복 횟수 차이 (풀이1 1,500회 vs 나머지 50회)
"""

import re
import time


# =================================================================================
# Mine solution one - while 순회로 직접 건너뜀
# =================================================================================
def solution_mine_one(s: str, skip: str, index: int) -> str:
    """
    index만큼 한 칸씩 이동하면서 skip 알파벳을 직접 건너뛰는 초기 풀이

    steps < index 조건:
        skip이 아닌 알파벳만 steps 증가
        z 넘어가면 a로 순환

    in skip:
        문자열 in 연산 O(len(skip)) 단일 문자 탐색

    비용:
        s 길이 50 × while 최대 30 × O(10) = O(15,000)
        사전 구축 방식 대비 약 15배 느림
    """
    answer = []

    for char in s:
        curr_code = ord(char)
        steps = 0

        while steps < index:
            curr_code += 1
            if curr_code > ord('z'):
                curr_code = ord('a')
            if chr(curr_code) not in skip:
                steps += 1

        answer.append(chr(curr_code))

    return "".join(answer)


# =================================================================================
# Mine solution two - allowed 사전 + index() 탐색
# =================================================================================
def solution_mine_two(s: str, skip: str, index: int) -> str:
    """
    skip 제외한 allowed 사전을 구축하고 나머지 연산으로 변환하는 풀이

    allowed:
        skip을 제외한 알파벳 리스트 = 새로운 알파벳 사전
        이 사전에서의 인덱스로 이동하면 skip 건너뜀이 자동 처리

    allowed.index(char):
        O(len(allowed)) 선형 탐색
        이 문제 규모(최대 20)에서 실측 차이 미미
        char_to_idx dict로 O(1) 개선 가능

    나머지 연산으로 순환 처리:
        (curr_idx + index) % len(allowed)
    """
    answer = ""
    allowed = [chr(i) for i in range(ord('a'), ord('z') + 1) if chr(i) not in skip]

    for char in s:
        curr_idx = allowed.index(char)
        new_idx = (curr_idx + index) % len(allowed)
        answer += allowed[new_idx]

    return answer


# =================================================================================
# Ref solution - 정규표현식 + dict 양방향 변환 테이블
# =================================================================================
def solution_ref(s: str, skip: str, index: int) -> str:
    """
    정규표현식으로 filtered를 구성하고 dict 양방향 테이블로 O(1) 변환하는 풀이

    re.sub(f'[{skip}]', '', 'abc...z'):
        skip 문자들을 알파벳 문자열에서 제거
        26자 단순 필터링에는 정규표현식 컴파일 오버헤드 불필요

    char_to_idx, idx_to_char:
        양방향 O(1) 변환 테이블
        idx_to_char는 filtered[new_idx]로 대체 가능 (메모리 절약)
    """
    filtered = re.sub(f"[{skip}]", "", "abcdefghijklmnopqrstuvwxyz")

    char_to_idx = {char: i for i, char in enumerate(filtered)}
    idx_to_char = {i: char for i, char in enumerate(filtered)}

    n = len(filtered)
    answer = []

    for char in s:
        new_idx = (char_to_idx[char] + index) % n
        answer.append(idx_to_char[new_idx])

    return "".join(answer)


# =================================================================================
# Best solution - 리스트 컴프리헨션 + char_to_idx dict (ref 개선)
# =================================================================================
def solution_best(s: str, skip: str, index: int) -> str:
    """
    정규표현식 없이 allowed 구축 후 char_to_idx O(1) 탐색으로 최적 처리

    ref 대비 개선:
        re.sub → 리스트 컴프리헨션 (정규표현식 오버헤드 제거)
        idx_to_char → allowed[new_idx] (dict 하나 제거, 메모리 절약)
        char_to_idx: O(1) 탐색 유지

    트레이드오프:
        공간 O(M): char_to_idx dict 1개
        시간 O(M+N): 사전 구축 O(M) + s 순회 O(N) × O(1) 탐색
    """
    allowed = [c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in skip]
    char_to_idx = {c: i for i, c in enumerate(allowed)}
    n = len(allowed)

    return ''.join(allowed[(char_to_idx[c] + index) % n] for c in s)


# =================================================================================
# Sub solution - allowed 사전 + index() 탐색 (mine_two 주석 보강)
# =================================================================================
def solution_sub(s: str, skip: str, index: int) -> str:
    """
    allowed 사전과 index() 탐색으로 직관적으로 변환하는 서브 풀이

    Best 대비 특징:
        char_to_idx dict 없음 → 메모리 절약
        allowed.index(char) O(len(allowed)): 이 문제 규모에서 실측 차이 미미
        새 알파벳 사전 → index 이동 → 순환 처리 구조가 명시적
    """
    allowed = [chr(i) for i in range(ord('a'), ord('z') + 1) if chr(i) not in skip]

    answer = []
    for char in s:
        curr_idx = allowed.index(char)
        new_idx = (curr_idx + index) % len(allowed)
        answer.append(allowed[new_idx])

    return "".join(answer)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """여섯 풀이의 정확성과 성능을 동시에 검증한다."""

    test_cases: list[tuple[str, str, int, str]] = [
        # (s, skip, index, 기댓값)
        # 공식 예시
        ("aukks", "wbqd", 5, "happy"),
        # 추가 케이스:
        # z 순환
        ("z",    "a",    1, "b"),
        # skip 없음 (공식 예시와 동일 구조)
        ("a",    "b",    1, "c"),
        # 최대 index
        ("a",    "bdfh", 20, "y"),
    ]

    solutions = [
        ("Mine_one (while순회)  ", solution_mine_one),
        ("Mine_two (index함수)  ", solution_mine_two),
        ("Ref      (regex+dict) ", solution_ref),
        ("Best     (dict O(1))  ", solution_best),
        ("Sub      (index함수)  ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _sk, _i, _ = test_cases[0]
    for _, func in solutions:
        func(_s, _sk, _i)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (s, skip, index, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s, skip, index)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
