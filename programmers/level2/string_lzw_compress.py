"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : [3차] 압축
    유형       : String / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17684
    풀이일자   : 2026-09-06
===================================================================================
[문제 요약]
    LZW 압축 알고리즘으로 영문 대문자 문자열 msg를 압축해
    사전 색인 번호 배열을 반환

    LZW 알고리즘:
        1. 길이 1 단어로 사전 초기화 (A=1 ~ Z=26)
        2. 사전에서 현재 입력과 일치하는 가장 긴 문자열 w 탐색
        3. w의 색인 번호 출력, 입력에서 w 제거
        4. 다음 글자 c가 있으면 w+c를 사전에 등록
        5. 2로 돌아감

    제약 조건
        - msg 길이: 1 이상 1,000 이하
        - 영문 대문자만
===================================================================================
[입출력 예시]
    msg                       | answer
    --------------------------|---------------------------------------
    "KAKAO"                   | [11, 1, 27, 15]
    "TOBEORNOTTOBEORTOBEORNOT"| [20,15,2,5,15,18,14,15,20,27,29,31,36,30,32,34]
    "ABABABABABABABAB"        | [1, 2, 27, 29, 28, 31, 30]
===================================================================================
[mine — 투포인터 방식]
    인덱스 i: 현재 w의 시작
    인덱스 j: 확장 중인 wc의 끝 (j-1까지가 w, j까지가 wc)

    내부 while:
        msg[i:j]가 사전에 있는 동안 j 증가
        종료 시: w = msg[i:j-1], wc = msg[i:j]

    if j <= N: 다음 글자 c가 있을 때만 wc 등록
        j > N: 문자열 끝, LZW 4단계 조건 "다음 글자가 있다면" 불만족

    슬라이싱 비용:
        j 증가마다 msg[i:j] 새 문자열 생성 → 누적 비용 발생
        ref의 w+c 단일 문자 누적 대비 2.5배 느림

[ref — 단일 순회 + 문자 누적 방식]
    w: 현재까지 사전에 있는 가장 긴 입력
    c: 다음 글자
    wc = w + c: 사전 검색 대상

    wc in dict → w = wc (확장)
    wc not in dict → answer에 w 색인 추가, wc 등록, w = c (리셋)

    마지막 예외처리:
        for 루프 안에서 answer에 추가되는 시점은 wc not in dict일 때
        마지막 w는 그 조건을 만족하지 않아 루프 안에서 미추가
        → 루프 종료 후 w가 있으면 수동 추가

    슬라이싱 없음: w+c는 문자 하나만 누적 → 빠름

[손 추적 — "KAKAO"]
    초기: w=""

    c='K': wc="K", K in dict → w="K"
    c='A': wc="KA", KA not in dict
           → answer=[11], dict["KA"]=27, w="A"
    c='K': wc="AK", AK not in dict
           → answer=[11,1], dict["AK"]=28, w="K"
    c='A': wc="KA", KA in dict(27) → w="KA"
    c='O': wc="KAO", KAO not in dict
           → answer=[11,1,27], dict["KAO"]=29, w="O"

    루프 종료, w="O" → answer=[11,1,27,15] ✓

[실측 결과 — msg 길이 1000, 50,000회]
    ref  (단일순회+누적):     100.1μs  ← 2.5배 빠름
    mine (투포인터+슬라이싱): 258.4μs
===================================================================================
[내 초기 풀이]
    solution_mine: 투포인터 + 슬라이싱

[개선 포인트]
    solution_mine: 슬라이싱 비용으로 느림 - Sub
                   LZW 알고리즘의 w/wc 구조가 코드에 명시적
    solution_ref:  단일 순회 + 문자 누적 - Best
                   슬라이싱 없이 w+c 1회 연산만 수행
===================================================================================
[복잡도 분석]
    N = len(msg) (최대 1,000)
    K = 사전 크기 (26 + 압축 과정에서 추가된 단어 수)

    Mine - 시간: O(N²) 최악 | 공간: O(K) - 슬라이싱 누적
    Ref  - 시간: O(N)       | 공간: O(K) - 단일 순회
    Best - 시간: O(N)       | 공간: O(K) - Ref와 동일
    Sub  - 시간: O(N²) 최악 | 공간: O(K) - Mine과 동일
"""

import string
import time


# =================================================================================
# Mine solution - 투포인터 + 슬라이싱
# =================================================================================
def solution_mine(msg: str) -> list[int]:
    """
    i, j 투포인터로 w와 wc를 슬라이싱으로 찾는 초기 풀이

    내부 while 종료 조건:
        j > N: 문자열 끝 초과 방지
        msg[i:j] not in dict: wc가 사전에 없는 시점

    j > N 처리 (j <= N 조건):
        마지막 w 출력 후 다음 글자 c가 없으면 wc 등록 안 함
        LZW 4단계 "다음 글자가 있다면" 조건과 대응

    슬라이싱 한계:
        j 증가마다 msg[i:j] 새 문자열 객체 생성
        ref의 w+c 단일 문자 누적 대비 2.5배 느림
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha_to_num = {alphabet[i]: i + 1 for i in range(26)}

    N = len(msg)
    i = 0
    next_num = 27
    answer = []

    while i < N:
        j = i + 1

        while j <= N and msg[i:j] in alpha_to_num:
            j += 1

        w = msg[i:j - 1]
        wc = msg[i:j]

        answer.append(alpha_to_num[w])

        if j <= N:
            alpha_to_num[wc] = next_num
            next_num += 1

        i = j - 1

    return answer


# =================================================================================
# Ref solution - 단일 순회 + 문자 누적
# =================================================================================
def solution_ref(msg: str) -> list[int]:
    """
    c를 하나씩 누적하며 단일 순회로 LZW를 구현하는 참고 풀이

    w 확장:
        wc = w + c가 사전에 있으면 w = wc (계속 확장)
        없으면 w를 출력하고 wc 등록, c를 새 w로 설정

    마지막 예외처리:
        for 루프에서 answer 추가 = wc not in dict 시점
        마지막 w는 그 조건을 만족하지 않아 루프 안에서 미추가
        → if w: answer.append()로 수동 처리

    슬라이싱 없음:
        w + c: 문자 하나만 누적
        매 단계 dict 탐색 1회 → 실측 mine 대비 2.5배 빠름
    """
    alpha_to_num = {char: idx for idx, char in enumerate(string.ascii_uppercase, start=1)}
    next_num = 27
    w = ""
    answer = []

    for c in msg:
        wc = w + c
        if wc in alpha_to_num:
            w = wc
        else:
            answer.append(alpha_to_num[w])
            alpha_to_num[wc] = next_num
            next_num += 1
            w = c

    if w:
        answer.append(alpha_to_num[w])

    return answer


# =================================================================================
# Best solution - 단일 순회 + 문자 누적 (ref 주석 보강)
# =================================================================================
def solution_best(msg: str) -> list[int]:
    """
    단일 순회 + 문자 누적으로 O(N) 시간에 LZW 압축을 구현하는 최적 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        슬라이싱 없음 → 매 단계 dict 탐색 O(1) 1회만
        실측 msg=1000: 100.1μs (mine 258.4μs 대비 2.5배 우위)
        LZW 알고리즘 5단계를 가장 간결하게 구현
    """
    alpha_to_num = {char: idx for idx, char in enumerate(string.ascii_uppercase, start=1)}
    next_num = 27
    w = ""
    answer = []

    for c in msg:
        wc = w + c
        if wc in alpha_to_num:
            w = wc
        else:
            answer.append(alpha_to_num[w])
            alpha_to_num[wc] = next_num
            next_num += 1
            w = c

    if w:
        answer.append(alpha_to_num[w])

    return answer


# =================================================================================
# Sub solution - 투포인터 (mine 주석 보강)
# =================================================================================
def solution_sub(msg: str) -> list[int]:
    """
    투포인터로 w와 wc를 명시적으로 분리해 LZW를 구현하는 서브 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        w = msg[i:j-1], wc = msg[i:j] 구조가 LZW 알고리즘과 1:1 대응
        알고리즘 흐름이 코드에 명시적으로 드러남
        슬라이싱 비용으로 Best 대비 2.5배 느림
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha_to_num = {alphabet[i]: i + 1 for i in range(26)}

    N = len(msg)
    i = 0
    next_num = 27
    answer = []

    while i < N:
        j = i + 1

        while j <= N and msg[i:j] in alpha_to_num:
            j += 1

        w = msg[i:j - 1]
        wc = msg[i:j]

        answer.append(alpha_to_num[w])

        if j <= N:
            alpha_to_num[wc] = next_num
            next_num += 1

        i = j - 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, list[int]]] = [
        # (msg, 기댓값)
        # 공식 예시
        ("KAKAO",                    [11, 1, 27, 15]),
        ("TOBEORNOTTOBEORTOBEORNOT", [20, 15, 2, 5, 15, 18, 14, 15, 20,
                                      27, 29, 31, 36, 30, 32, 34]),
        ("ABABABABABABABAB",         [1, 2, 27, 29, 28, 31, 30]),
        # 추가 케이스:
        # 단일 문자
        ("A",  [1]),
        # 모두 같은 문자 (연속 반복)
        # 손 추적: A→1, AA 없음→dict["AA"]=27, A→1, AA in dict
        #          → w="AA", A없음... msg="AAA"
        # c='A': wc="A" in dict → w="A"
        # c='A': wc="AA" not in dict → answer=[1], dict["AA"]=27, w="A"
        # c='A': wc="AA" in dict → w="AA"
        # 루프 종료, w="AA" → answer=[1, 27]
        ("AAA", [1, 27]),
    ]

    solutions = [
        ("Mine (투포인터+슬라이싱)", solution_mine),
        ("Ref  (단일순회+누적)    ", solution_ref),
        ("Best (단일순회+누적)    ", solution_best),
        ("Sub  (투포인터+슬라이싱)", solution_sub),
    ]

    # 워밍업 스텝
    _m, _ = test_cases[0]
    for _, func in solutions:
        func(_m)

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (msg, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(msg)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
