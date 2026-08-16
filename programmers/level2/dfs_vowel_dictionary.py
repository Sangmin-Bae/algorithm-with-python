"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 모음 사전
    유형       : DFS / 완전탐색
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/84512
    풀이일자   : 2026-08-16
================================================================================
[문제 요약]
    A, E, I, O, U로 만들 수 있는 1~5글자 단어들의 사전에서
    주어진 word의 사전 순위 반환

    사전 순서: A, AA, AAA, AAAA, AAAAA, AAAAE, ..., UUUUU
    총 단어 수: 5 + 25 + 125 + 625 + 3125 = 3905개

    제약 조건
        - word 길이: 1 이상 5 이하
        - word는 A, E, I, O, U로만 구성
================================================================================
[입출력 예시]
    word    | result
    --------|-------
    "AAAAE" | 6
    "AAAE"  | 10
    "I"     | 1563
    "EI"    | 1095
    "UUUUU" | 3905
================================================================================
[사전 구조 — DFS 탐색 순서 = 사전 순서]
    A → AA → AAA → AAAA → AAAAA → AAAAE → ... → AAAAU → AAAE → ...
    깊이 우선 탐색으로 끝까지 내려간 후 백트래킹

    재귀 호출 전 cnt 증가:
        cnt를 먼저 증가시켜야 "이 단어를 방문했다"가 됨
        word를 찾으면 그때의 cnt가 사전 순위

[ref 풀이 — 자리별 가중치 계산]
    핵심 아이디어:
        사전 전체를 생성/탐색하지 않고
        word의 각 자리에서 "이전 모음들이 차지하는 단어 수"를 계산

    자리별 가중치 = 그 자리에서 모음 하나가 바뀔 때 건너뛰는 단어 수

    1번째 자리 가중치:
        A로 시작하는 단어 수 = 1 + 5 + 25 + 125 + 625 = 781
    2번째 자리 가중치: 1 + 5 + 25 + 125 = 156
    3번째 자리 가중치: 1 + 5 + 25 = 31
    4번째 자리 가중치: 1 + 5 = 6
    5번째 자리 가중치: 1

    공식: answer += idx * weights[i] + 1
        idx:        현재 모음의 AEIOU 순서 (A=0, E=1, ...)
        weights[i]: i번째 자리 가중치
        + 1:        단어 자체가 사전에 1개로 포함됨

    손 추적 (word="EI"):
        i=0, 'E': idx=1, 1×781+1 = 782  (A 781개 건너뜀 + E 자체)
        i=1, 'I': idx=2, 2×156+1 = 313  (EA,EE 156×2개 건너뜀 + EI 자체)
        answer = 782+313 = 1095 ✓

    시간복잡도 O(len(word)) = O(5):
        사전 3905개와 무관, word 길이만큼만 연산
        → 모든 입력에서 일정하게 빠름

[세 풀이 속도 비교]
    풀이1 (DFS):        O(총 단어 수) = O(3905) 최악
    풀이2 (product):    O(3905 log 3905) ≈ O(46,000)
    ref   (가중치):     O(len(word)) = O(5) 최대

    ref가 빠른 이유:
        "사전을 만들거나 탐색한다" → 단어 수에 비례
        "수학적 공식으로 직접 계산한다" → word 길이에만 비례
================================================================================
[내 초기 풀이]
    solution_mine_one: DFS 재귀로 사전 탐색
    solution_mine_two: product로 사전 직접 생성 후 인덱스 탐색

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Sub
                       DFS 탐색 순서 = 사전 순서의 원리 명시적
    solution_mine_two: product + sort로 사전 전체 생성
                       정렬까지 필요해 가장 느림
    solution_ref:      자리별 가중치 계산 O(5) - Best
                       수학적 성질 발견으로 탐색 자체를 제거
================================================================================
[복잡도 분석]
    N = 총 단어 수 = 3905 (상수)
    L = len(word) (최대 5)

    Mine_one - 시간: O(N)       | 공간: O(N) - 재귀 스택 + cnt/answer
    Mine_two - 시간: O(N log N) | 공간: O(N) - 사전 리스트 + 정렬
    Ref      - 시간: O(L)       | 공간: O(1) - word 순회만
    Best     - 시간: O(L)       | 공간: O(1) - Ref와 동일
    Sub      - 시간: O(N)       | 공간: O(N) - Mine_one과 동일

    N=3905, L=5 고정이라 모두 O(1)이지만
    ref는 실측에서 풀이1 대비 수백~수천 배 빠름
"""

from itertools import product
import time


# ================================================================================
# Mine solution one - DFS 재귀 탐색
# ================================================================================
def solution_mine_one(word: str) -> int:
    """
    DFS로 사전 순서대로 단어를 탐색해 word의 순위를 찾는 초기 풀이

    DFS 탐색 순서 = 사전 순서:
        A → AA → AAA → AAAA → AAAAA → AAAAE → ... (깊이 우선)

    cnt += 1 위치:
        재귀 호출 전에 증가 → "이 단어를 방문함" 표시
        word를 찾으면 그때의 cnt = 사전 순위

    len(curr_word) >= 5 종료 조건:
        > 5로 하면 길이 5에서 for 루프 진입 → 길이 6 단어 생성
        >= 5로 제한해서 길이 초과 방지
    """
    answer = 0
    cnt = 0
    vowels = ['A', 'E', 'I', 'O', 'U']

    def dfs(curr_word: str) -> None:
        nonlocal cnt, answer

        if curr_word == word:
            answer = cnt
            return

        if len(curr_word) >= 5:
            return

        for v in vowels:
            cnt += 1
            dfs(curr_word + v)

    dfs('')
    return answer


# ================================================================================
# Mine solution two - product로 사전 생성 후 인덱스 탐색
# ================================================================================
def solution_mine_two(word: str) -> int:
    """
    product로 가능한 모든 단어를 생성하고 정렬 후 인덱스를 반환하는 풀이

    product(vowels, repeat=i):
        모음 5개 중 중복 허용으로 i개를 뽑는 모든 경우
        각 결과는 튜플 → ''.join()으로 문자열 변환

    words.sort() 필요 이유:
        길이별로 생성하면 A, E, ... U, AA, AE, ... 순서
        사전 순서는 A, AA, AAA, ... 이어야 함
        → 길이와 무관하게 전체 정렬 필요

    O(N log N): 3905개 생성 + 정렬
    """
    words = []
    vowels = ['A', 'E', 'I', 'O', 'U']

    for i in range(1, 6):
        for p in product(vowels, repeat=i):
            words.append(''.join(p))

    words.sort()

    return words.index(word) + 1


# ================================================================================
# Ref solution - 자리별 가중치 계산 O(L)
# ================================================================================
def solution_ref(word: str) -> int:
    """
    자리별 가중치로 사전 탐색 없이 O(len(word))에 순위를 계산하는 참고 풀이

    weights = [781, 156, 31, 6, 1]:
        i번째 자리 모음 하나가 바뀔 때 건너뛰는 단어 수
        1번째: A로 시작하는 단어 수 = 1+5+25+125+625 = 781
        2번째: 1+5+25+125 = 156
        3번째: 1+5+25 = 31
        4번째: 1+5 = 6
        5번째: 1

    answer += idx * weights[i] + 1:
        idx: 현재 모음의 순서 (A=0, E=1, I=2, O=3, U=4)
        idx * weights[i]: 이전 모음들이 차지하는 단어 수
        + 1: 현재 단어(길이가 i+1 이하인 것 포함) 자체 카운트

    O(L): word 길이만큼만 연산 → 3905개 탐색과 무관
    """
    weights = [781, 156, 31, 6, 1]
    vowels = "AEIOU"
    answer = 0

    for i, char in enumerate(word):
        idx = vowels.index(char)
        answer += idx * weights[i] + 1

    return answer


# ================================================================================
# Best solution - 자리별 가중치 계산 (ref 주석 보강)
# ================================================================================
def solution_best(word: str) -> int:
    """
    자리별 가중치로 O(len(word)) 시간, O(1) 공간에 순위를 계산하는 최적 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        수학적 성질 발견으로 탐색 자체 제거
        O(5): 단어 수 3905와 완전히 무관
        모든 입력에서 일정하게 빠름 (실측 0.1ms 이하)
        weights 유도: 각 자리에서 가능한 단어 수의 합
    """
    weights = [781, 156, 31, 6, 1]
    vowels = "AEIOU"
    answer = 0

    for i, char in enumerate(word):
        idx = vowels.index(char)
        answer += idx * weights[i] + 1

    return answer


# ================================================================================
# Sub solution - DFS 재귀 탐색 (mine_one 주석 보강)
# ================================================================================
def solution_sub(word: str) -> int:
    """
    DFS로 사전 탐색 순서와 단어 순서의 동치를 표현하는 서브 풀이

    Best 대비 특징:
        DFS 탐색 순서 = 사전 순서가 코드에 직접 드러남
        "A부터 시작해 깊이 우선으로 순서대로 방문"이 직관적
        O(3905): 최악 UUUUU를 찾으려면 전체를 탐색
        Best O(5) 대비 느리나 완전탐색 원리 이해에 적합
    """
    answer = 0
    cnt = 0
    vowels = ['A', 'E', 'I', 'O', 'U']

    def dfs(curr_word: str) -> None:
        nonlocal cnt, answer

        if curr_word == word:
            answer = cnt
            return

        if len(curr_word) >= 5:
            return

        for v in vowels:
            cnt += 1
            dfs(curr_word + v)

    dfs('')
    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int]] = [
        # (word, 기댓값)
        # 공식 예시
        ("AAAAE", 6),
        ("AAAE",  10),
        ("I",     1563),
        ("EI",    1095),
        ("UUUUU", 3905),
        # 추가 케이스:
        ("A",     1),       # 첫 번째 단어
        ("AAAAA", 5),       # 5번째
    ]

    solutions = [
        ("Mine_one (DFS)     ", solution_mine_one),
        ("Mine_two (product) ", solution_mine_two),
        ("Ref      (가중치)  ", solution_ref),
        ("Best     (가중치)  ", solution_best),
        ("Sub      (DFS)     ", solution_sub),
    ]

    # 워밍업 스텝
    _w, _ = test_cases[0]
    for _, func in solutions:
        func(_w)

    print("=" * 62)
    print(f"{'풀이':<20} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 62)

    for name, func in solutions:
        for idx, (word, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(word)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<20} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 62)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
