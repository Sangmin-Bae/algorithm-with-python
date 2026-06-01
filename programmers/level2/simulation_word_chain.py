"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 영어 끝말잇기
    유형       : Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12981
    풀이일자   : 2025-06-01
================================================================================
[문제 요약]
    n명이 순서대로 끝말잇기. 탈락 시 [번호, 차례] 반환
    탈락 조건:
        1. 이전 단어 끝문자 ≠ 현재 단어 첫문자
        2. 이전에 사용된 단어 재사용
    탈락자 없으면 [0, 0]

    제약 조건
        - n: 2 이상 10 이하
        - words 길이: n 이상 100 이하
        - 단어 길이: 2 이상 50 이하 (한 글자 단어 없음 보장)
================================================================================
[입출력 예시]
    n=3, ["tank","kick","know","wheel","land","dream","mother","robot","tank"]
    → [3,3]  (3번 사람 3번째 차례에 "tank" 재사용)

    n=5, ["hello","observe",...,"executive"]
    → [0,0]  (탈락자 없음)

    n=2, ["hello","one","even","never","now","world","draw"]
    → [1,3]  (1번 사람 3번째 차례에 끝말잇기 실패)
================================================================================
[내 초기 풀이]
    words를 순회하며 used 리스트로 사용 단어 추적
    두 탈락 조건을 분리된 if문으로 확인 (가독성 기준)
    user, turn 변수 직접 증감 관리

[개선 포인트]
    1. print(user, turn) 디버깅 코드 제거 필요
    2. used 리스트 → 역할 분리:
        - 중복 확인: set O(1) (리스트 in 연산은 O(N))
        - 이전 단어 끝문자: prev_end 변수로 분리
    3. user/turn 계산: enumerate + idx % n + 1, idx // n + 1
================================================================================
[used 자료구조 설계 판단]
    Mine의 used 리스트 두 가지 역할:
        1. 중복 확인 → "이 단어가 있는가?" → set이 O(1)로 최적
        2. 이전 단어 끝문자 → used[-1][-1] → 순서 필요, 리스트 필요

    두 역할을 분리하면:
        set: 중복 확인 전용 O(1)
        prev_end 변수: 이전 단어 끝문자만 별도 유지
        → used 리스트 불필요, 더 효율적

[조건문 분리 판단]
    두 탈락 조건을 합치면:
        if word in used or (prev_end and prev_end != word[0]):
    → 가독성 저하, 각 조건의 의미가 불명확
    → 분리가 맞는 선택 (네 판단 정확)
================================================================================
[복잡도 분석]
    N = len(words) (최대 100)

    Mine - 시간: O(N²) | 공간: O(N) — 리스트 in 연산 O(N) × N번
    Best - 시간: O(N)  | 공간: O(N) — set in 연산 O(1) × N번
    Sub  - 시간: O(N)  | 공간: O(N) — set in 연산 O(1) × N번

    N ≤ 100이라 실질 차이 없음
    "중복 확인은 set" 습관이 큰 입력에서 빛을 발함
================================================================================
"""

import time
from typing import List, Tuple


# ==============================================================================
# Mine solution — 리스트 used + 직접 user/turn 관리
# ==============================================================================
def solution_mine(n: int, words: List[str]) -> List[int]:
    """
    used 리스트로 사용 단어 추적하며 두 탈락 조건을 순차 확인하는 초기 풀이

    개선 전 상태:
        - print(user, turn): 디버깅 코드, 제출 전 제거 필요
        - word in used: 리스트 in 연산 O(N) → set으로 O(1) 개선 가능
        - used[-1][-1]: 이전 단어 끝문자 접근 (prev_end 변수로 분리 가능)

    잘 된 점:
        - 두 탈락 조건 분리 → 가독성 유지 (조건 합치면 오히려 나빠짐)
        - if used: 초기 빈 리스트 방어 처리
    """
    used = []
    user = 1
    turn = 1

    for word in words:
        # print(user, turn)   # 디버깅 코드 → 제거

        if word in used:                           # 중복 단어 확인 O(N)
            return [user, turn]

        if used and used[-1][-1] != word[0]:       # 끝말잇기 규칙 확인
            return [user, turn]

        used.append(word)
        user += 1

        if user > n:
            user = 1
            turn += 1

    return [0, 0]


# ==============================================================================
# Best solution — enumerate + set + prev_end 변수
# ==============================================================================
def solution_best(n: int, words: List[str]) -> List[int]:
    """
    enumerate로 user/turn 계산, set으로 중복 O(1) 확인하는 최적 풀이

    Mine 대비 개선:
        - enumerate: idx % n + 1 → user, idx // n + 1 → turn
            별도 user, turn 변수 관리 불필요
        - set: 중복 확인 O(N) → O(1)
        - prev_end: 이전 단어 끝문자만 별도 변수로 유지
            used 리스트에서 used[-1][-1] 접근 불필요

    탈락 조건 순서:
        끝말잇기 실패 먼저 확인 → 중복 확인
        (둘 다 같은 시점에 탈락이므로 순서 무관, 가독성 기준 선택)
    """
    used = set()
    prev_end = ''       # 이전 단어 끝문자 (초기: 빈 문자열)

    for idx, word in enumerate(words):
        user = idx % n + 1      # 1~n 순환 (0-indexed → 1-indexed)
        turn = idx // n + 1     # 몇 번째 라운드

        # 탈락 조건 1: 끝말잇기 실패 (이전 단어 끝문자 ≠ 현재 단어 첫문자)
        if prev_end and prev_end != word[0]:
            return [user, turn]

        # 탈락 조건 2: 중복 단어
        if word in used:                # set in 연산: O(1)
            return [user, turn]

        used.add(word)
        prev_end = word[-1]             # 현재 단어 끝문자 갱신

    return [0, 0]


# ==============================================================================
# Sub solution — 네 풀이 구조 유지 + set + prev_end 적용
# ==============================================================================
def solution_sub(n: int, words: List[str]) -> List[int]:
    """
    Mine의 user/turn 직접 관리 구조를 유지하며 set + prev_end로 개선한 풀이

    Mine 대비 개선:
        - used 리스트 → set (중복 확인 O(N) → O(1))
        - used[-1][-1] → prev_end 변수 (이전 단어 끝문자 직접 유지)
        - print 제거

    Best 대비 특징:
        - user/turn을 직접 증감으로 관리 → 흐름이 직관적
        - enumerate idx 계산식보다 이해하기 쉬움
    """
    used = set()
    prev_end = ''
    user = 1
    turn = 1

    for word in words:
        if prev_end and prev_end != word[0]:    # 끝말잇기 실패
            return [user, turn]

        if word in used:                        # 중복 단어
            return [user, turn]

        used.add(word)
        prev_end = word[-1]
        user += 1

        if user > n:
            user = 1
            turn += 1

    return [0, 0]


# ==============================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==============================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple] = [
        # (n, words, 기댓값)
        (3,
            ["tank","kick","know","wheel","land","dream","mother","robot","tank"],
            [3, 3]),
        (5,
            ["hello","observe","effect","take","either","recognize",
            "encourage","ensure","establish","hang","gather","refer",
            "reference","estimate","executive"],
            [0, 0]),
        (2,
            ["hello","one","even","never","now","world","draw"],
            [1, 3]),
        (2,
            ["hello", "one"],
            [0, 0]),    # "hello"→'o', "one"→'o'로 시작 ✓, 중복 없음 → 탈락자 없음
        (2,
            ["hello", "yellow"],
            [2, 1]),    # "yellow"는 'y'로 시작, hello 끝이 'o' → 2번 사람 1번째 탈락
    ]

    solutions = [
        ("Mine (리스트+직접관리)", solution_mine),
        ("Best (enumerate+set)", solution_best),
        ("Sub  (직접관리+set)",  solution_sub),
    ]

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (*args, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(*args)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 64)


# ==============================================================================
# 실행 진입점
# ==============================================================================
if __name__ == "__main__":
    solution_comparison()
