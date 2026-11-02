"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D2
    문제명     : 4865. [S/W 문제해결 기본] 3일차 - 글자수
    유형       : String (글자 개수 세기), Dictionary
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWTQSs6qQL0DFAVT&categoryId=AWTQSs6qQL0DFAVT&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=4
    풀이일자   : 2026-11-02
================================================================================
[문제 요약]
    문자열 str1에 포함된 글자들이 str2에 몇 개씩 들어있는지 찾고
    그중 가장 많은 글자의 개수를 구함

    입력 방식 : 테스트 케이스 T개, 케이스마다 str1(길이 N)과 str2(길이 M)
                (5 ≤ N ≤ 100, 10 ≤ M ≤ 1000, N ≤ M)
    적용 방식 : 한 케이스의 입력 → 매개변수 str1, str2, output → 최대 글자 수를 반환
                (케이스 번호 "#T" 출력 형식은 제외)
================================================================================
[입출력 예시]
    공식 예시
    str1           | str2                  | return
    ---------------|-----------------------|-------
    "XYPV"         | "EOGGXYPVSY"          | 2      (Y가 2개)
    "STJJ"         | "HOFSTJPVPP"          | 1      (S, T, J 각 1개)
    "ZYJZXZTIBSDG" | "TTXGZYJZXZTIBSDGWQLW" | 3     (Z가 3개, T도 3개)

    자체 검증 케이스 (전부 손 계산)
    str1                | str2                 | return
    --------------------|----------------------|--------
    "ABCA"              | "ABABCA"             | 3      (지문 예시, A가 3개)
    "AAAAA"             | "BBBBBBBBBB"         | 0      (str1의 글자가 str2에 없음)
    "AAAAA"             | "AAAAAAAAAA"         | 10     (전부 같은 글자)
    "ABCDE"             | "ABCDEABCDE"         | 2      (모든 글자가 동률)
    "ABCDE"             | "BBBBBAAAAA"         | 5      (B와 A가 동률, C, D, E는 0)
    알파벳 26자          | 알파벳 26자 * 10000   | 10000  (대용량, 글자마다 10000개, 닫힌 식으로 기댓값 계산)
================================================================================
[풀이 전략]
    핵심: str1의 각 글자가 str2에 나오는 횟수를 세고 그중 최댓값
        str1의 같은 글자를 반복해서 세지 않도록 중복 제거 (set(str1))
        str2에 없는 글자는 0개 (최댓값에는 영향 없음)

    풀이 구성:
        mine_one   : set(str1)의 글자마다 str2.count로 개수를 세어 리스트에 담고 max
        mine_two   : str1의 글자를 key로 하는 딕셔너리를 만들고 str2를 한 번 순회하며 개수 증가
                     str2를 한 번만 훑지만 순회가 파이썬 코드로 실행됨
        mine_three : mine_one에서 리스트와 max 대신 변수 하나로 최댓값을 갱신
                     counts 리스트가 없어 추가 메모리가 필요 없음
                     max도 직접 비교 갱신도 글자 하나당 한 번씩 확인하므로 시간은 같음
        best       : max(str2.count(글자) for 글자 in set(str1)), mine_one에서 중간 리스트를 제거
        sub        : collections.Counter(str2)로 str2의 글자 수를 한 번에 센 뒤 str1의 글자를 조회
                     mine_two의 딕셔너리 방식을 라이브러리로 간결하게 개선, 없는 글자는 0

    str.count:
        str2.count(글자) : str2에서 글자가 나오는 횟수 (겹치지 않는 부분 문자열 개수, 한 글자면 글자 수)
        글자마다 str2 전체를 한 번씩 훑음 → 서로 다른 글자 수 k개면 k번 훑음

    손 추적 (공식 예시 1) str1 = "XYPV", str2 = "EOGGXYPVSY":
        set(str1) = {X, Y, P, V}
        X → 1, Y → 2, P → 1, V → 1
        max → 2 ✓
================================================================================
[개선 포인트]
    solution_mine_one   : 개선 여지 작음 - 중간 리스트 없이 max에 바로 전달 가능
    solution_mine_two   : 개선 여지 있음 - 순회와 개수 증가를 Counter로 대체 가능
    solution_mine_three : 개선 여지 작음 - 메모리는 절약하나 코드가 길어짐
    solution_best       : 중간 리스트 제거 - Best
    solution_sub        : 딕셔너리 방식을 Counter로 간결하게 - str2를 한 번만 훑음
================================================================================
[복잡도 분석]
    N = len(str1), M = len(str2), k = str1의 서로 다른 글자 수 (k ≤ N)

    Mine_one   - 시간: O(k * M) | 공간: O(k) - 글자마다 str2를 훑어 개수를 리스트에 저장
    Mine_two   - 시간: O(N + M) | 공간: O(k) - str2를 한 번 순회하며 딕셔너리 갱신
    Mine_three - 시간: O(k * M) | 공간: O(k) - 변수로 갱신 (set(str1) 저장)
    Best       - 시간: O(k * M) | 공간: O(k) - set(str1) 저장, 개수 리스트 없음
    Sub        - 시간: O(N + M) | 공간: O(M) - str2의 서로 다른 글자 수만큼 저장
"""

import time
from collections import Counter


# ================================================================================
# Mine solution one - set + count + 리스트 + max
# ================================================================================
def solution_mine_one(str1: str, str2: str) -> int:
    """
    str1의 중복을 제거한 글자마다 str2.count로 개수를 세어 최댓값을 구하는 풀이

    핵심:
        set(str1) : 같은 글자를 반복해서 세지 않도록 중복 제거
        str2.count(char) : str2에서 글자가 나오는 횟수
        counts 리스트에 모아 max로 최댓값
    """
    counts = []

    for char in set(str1):
        counts.append(str2.count(char))

    return max(counts)


# ================================================================================
# Mine solution two - 딕셔너리로 개수 세기
# ================================================================================
def solution_mine_two(str1: str, str2: str) -> int:
    """
    str1의 글자를 key로 하는 딕셔너리에 str2의 글자 수를 세는 풀이

    핵심:
        {char: 0 for char in str1} : 세어야 할 글자만 key로 초기화
        str2를 한 번 순회하며 key에 있는 글자만 1씩 증가
        max(values())로 최댓값
    """
    char_dict = {char: 0 for char in str1}

    for char in str2:
        if char in char_dict:
            char_dict[char] += 1

    return max(char_dict.values())


# ================================================================================
# Mine solution three - 변수 하나로 최댓값 갱신
# ================================================================================
def solution_mine_three(str1: str, str2: str) -> int:
    """
    mine_one에서 리스트와 max 대신 변수 하나로 최댓값을 갱신하는 풀이

    핵심:
        max_val = -1 : 개수는 0 이상이므로 어떤 값이든 첫 비교에서 갱신
        if current_count > max_val : 더 큰 개수가 나오면 갱신
    """
    max_val = -1

    for char in set(str1):
        current_count = str2.count(char)

        if current_count > max_val:
            max_val = current_count

    return max_val


# ================================================================================
# Best solution - 제너레이터 식 + count + max
# ================================================================================
def solution_best(str1: str, str2: str) -> int:
    """
    mine_one에서 중간 리스트를 없애 max에 개수를 바로 전달하는 최적 풀이

    핵심:
        max(str2.count(char) for char in set(str1))
        제너레이터 식이 개수를 하나씩 만들어 max에 전달
    """
    return max(str2.count(char) for char in set(str1))


# ================================================================================
# Sub solution - Counter
# ================================================================================
def solution_sub(str1: str, str2: str) -> int:
    """
    Counter로 str2의 글자 수를 한 번에 센 뒤 str1의 글자를 조회하는 풀이

    핵심:
        Counter(str2) : 글자별 개수를 딕셔너리처럼 저장
        counter[char] : 없는 글자는 KeyError 없이 0
        str2를 한 번만 훑음
    """
    counter = Counter(str2)

    return max(counter[char] for char in set(str1))


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    test_cases: list[tuple] = [
        # (str1, str2, 기댓값) - 전부 손 계산
        ("XYPV", "EOGGXYPVSY", 2),                          # 공식 예시 1
        ("STJJ", "HOFSTJPVPP", 1),                          # 공식 예시 2
        ("ZYJZXZTIBSDG", "TTXGZYJZXZTIBSDGWQLW", 3),        # 공식 예시 3
        ("ABCA", "ABABCA", 3),                              # 지문 예시
        ("AAAAA", "BBBBBBBBBB", 0),                         # str2에 없는 글자만
        ("AAAAA", "AAAAAAAAAA", 10),                        # 전부 같은 글자
        ("ABCDE", "ABCDEABCDE", 2),                         # 모든 글자가 동률
        ("ABCDE", "BBBBBAAAAA", 5),                         # 두 글자 동률, 나머지는 0
        (alphabet, alphabet * 10000, 10000),                # 대용량: 26글자 각 10000개
    ]

    solutions = [
        ("Mine1 (count+list)", solution_mine_one),
        ("Mine2 (dict)", solution_mine_two),
        ("Mine3 (max 변수)", solution_mine_three),
        ("Best (count+gen)", solution_best),
        ("Sub (Counter)", solution_sub),
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
