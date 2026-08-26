"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 대충 만든 자판
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/160586
    풀이일자   : 2026-08-26
===================================================================================
[문제 요약]
    keymap의 각 키로 알파벳을 입력할 때 최소 press 횟수를 구해
    targets의 각 문자열을 입력하는 최소 press 총합 반환 (불가능하면 -1)

    제약 조건
        - keymap 길이: 1~100, 각 원소 길이: 1~100
        - targets 길이: 1~100, 각 원소 길이: 1~100
        - 알파벳 대문자로만 구성
===================================================================================
[입출력 예시]
    keymap           | targets          | result
    -----------------|------------------|-------
    ["ABACD","BCEFD"]| ["ABCD","AABB"]  | [9, 4]
    ["AA"]           | ["B"]            | [-1]
    ["AGZ","BSSS"]   | ["ASA","BGZ"]    | [4, 6]
===================================================================================
[핵심 — 사전 구축 필요성]
    greedy 방식 (폐기):
        target의 각 문자마다 keymap 전체 순회
        O(targets × target_len × keymap × key_len) = O(10^8) 최악

    사전 구축 방식:
        keymap 집계 O(10,000) + targets 조회 O(10,000) = O(20,000)
        각 알파벳의 최소 press 횟수를 미리 계산해두면 O(1) 조회

[dict vs 배열(수동 해시) 비교]
    실측 (최대 규모 keymap×100, targets×100, 50,000회):
        mine (dict):  0.907ms  ← 더 빠름
        ref  (array): 1.506ms

    ref가 느린 이유:
        ord(char) - 65 연산이 매 문자마다 발생
        keymap 집계 + targets 조회 합계 20,000번의 ord() 호출

    dict가 빠른 이유:
        char 자체가 key → 변환 없이 직접 해시 조회
        Python dict는 문자열 해시를 캐싱하므로 추가 비용 최소

    배열 방식이 유리한 경우:
        C, Java, C++: dict/HashMap 오버헤드 > ord() 비용
        Python: dict가 C 레벨 최적화 → ord() 비용 > dict 절감분
        → 저수준 언어의 최적화를 Python으로 옮긴 방식
===================================================================================
[내 초기 풀이]
    solution_mine: dict hash map + 최솟값 조건문 갱신

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
                   dict로 가장 빠름, 조건문으로 min 오버헤드 없음
    solution_ref:  배열(수동 해시) - Sub
                   ord() 변환 비용으로 Python에서 dict보다 느림
                   저수준 언어 방식 학습 목적
===================================================================================
[복잡도 분석]
    K = keymap 길이, L = keymap 원소 평균 길이 (최대 100×100=10,000)
    T = targets 길이, M = targets 원소 평균 길이 (최대 100×100=10,000)

    Mine - 시간: O(K×L + T×M) | 공간: O(26) - dict 최대 26개 키
    Ref  - 시간: O(K×L + T×M) | 공간: O(26) - 배열 26개 원소
    Best - 시간: O(K×L + T×M) | 공간: O(26) - Mine과 동일
    Sub  - 시간: O(K×L + T×M) | 공간: O(26) - Ref와 동일

    모두 O(20,000) 이하, 실질적 O(1)
"""

import time


# =================================================================================
# Mine solution - dict hash map
# =================================================================================
def solution_mine(keymap: list[str], targets: list[str]) -> list[int]:
    """
    dict로 각 알파벳의 최소 press 횟수를 집계하는 초기 풀이

    table 구축:
        keymap 전체 순회하며 각 알파벳의 최소 press 횟수 저장
        조건문으로 min 함수 오버헤드 없이 최솟값 갱신

    for-else 패턴:
        target 문자열 순회 중 keymap에 없는 문자 발견 → break → -1 추가
        break 없이 완료 → else → count 추가
    """
    answer = []
    table = {}

    for s in keymap:
        for idx, char in enumerate(s):
            press = idx + 1
            if char not in table:
                table[char] = press
            else:
                if press < table[char]:
                    table[char] = press

    for t in targets:
        count = 0
        for char in t:
            if char not in table:
                answer.append(-1)
                break
            count += table[char]
        else:
            answer.append(count)

    return answer


# =================================================================================
# Ref solution - 배열(수동 해시)
# =================================================================================
def solution_ref(keymap: list[str], targets: list[str]) -> list[int]:
    """
    알파벳 26자 배열로 수동 해시를 구현하는 참고 풀이

    ord(char) - 65:
        대문자 아스키코드 65~90 → 0~25 인덱스로 변환
        'A' → 0, 'B' → 1, ..., 'Z' → 25

    Python에서 dict보다 느린 이유:
        ord() 연산이 매 문자마다 발생 (집계+조회 합계 ~20,000회)
        Python dict는 문자열 해시를 캐싱해서 직접 조회가 더 빠름

    배열 방식이 의미 있는 경우:
        C, Java, C++에서 dict/HashMap 오버헤드 > ord() 비용
        → 저수준 언어의 최적화 방식을 Python으로 옮긴 형태
    """
    answer = []
    table = [float('inf')] * 26

    for key in keymap:
        for idx, char in enumerate(key):
            arr_idx = ord(char) - 65
            if idx + 1 < table[arr_idx]:
                table[arr_idx] = idx + 1

    for t in targets:
        count = 0
        for char in t:
            arr_idx = ord(char) - 65
            if table[arr_idx] == float('inf'):
                answer.append(-1)
                break
            count += table[arr_idx]
        else:
            answer.append(count)

    return answer


# =================================================================================
# Best solution - dict hash map (mine 주석 보강)
# =================================================================================
def solution_best(keymap: list[str], targets: list[str]) -> list[int]:
    """
    dict로 O(K×L + T×M) 시간, O(26) 공간에 최소 press 횟수를 구하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        dict 직접 해시 조회 → ord() 변환 불필요
        실측 최대 규모: 0.907ms (ref 1.506ms 대비 우위)
        Python dict는 C 레벨 최적화로 배열 방식보다 빠름
    """
    answer = []
    table = {}

    for s in keymap:
        for idx, char in enumerate(s):
            press = idx + 1
            if char not in table:
                table[char] = press
            else:
                if press < table[char]:
                    table[char] = press

    for t in targets:
        count = 0
        for char in t:
            if char not in table:
                answer.append(-1)
                break
            count += table[char]
        else:
            answer.append(count)

    return answer


# =================================================================================
# Sub solution - 배열 수동 해시 (ref 주석 보강)
# =================================================================================
def solution_sub(keymap: list[str], targets: list[str]) -> list[int]:
    """
    26자 배열로 수동 해시를 구현하는 서브 풀이

    Best 대비 특징:
        ord(char) - 65로 알파벳을 0~25 인덱스로 변환
        C/Java/C++ 에서 dict보다 빠른 저수준 최적화 방식
        Python에서는 ord() 변환 비용으로 dict보다 느림
        float('inf') 초기화로 미할당 알파벳 구분
    """
    answer = []
    table = [float('inf')] * 26

    for key in keymap:
        for idx, char in enumerate(key):
            arr_idx = ord(char) - 65
            if idx + 1 < table[arr_idx]:
                table[arr_idx] = idx + 1

    for t in targets:
        count = 0
        for char in t:
            arr_idx = ord(char) - 65
            if table[arr_idx] == float('inf'):
                answer.append(-1)
                break
            count += table[arr_idx]
        else:
            answer.append(count)

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (keymap, targets, 기댓값)
        # 공식 예시
        (["ABACD", "BCEFD"], ["ABCD", "AABB"], [9, 4]),
        (["AA"],              ["B"],            [-1]),
        (["AGZ", "BSSS"],    ["ASA", "BGZ"],   [4, 6]),
        # 추가 케이스:
        # 단일 키, 단일 타겟
        (["A"],              ["A"],            [1]),
        # 불가능한 문자 포함
        (["ABC"],            ["ABZ"],          [-1]),
    ]

    solutions = [
        ("Mine (dict)  ", solution_mine),
        ("Ref  (array) ", solution_ref),
        ("Best (dict)  ", solution_best),
        ("Sub  (array) ", solution_sub),
    ]

    # 워밍업 스텝
    _km, _t, _ = test_cases[0]
    for _, func in solutions:
        func(_km, _t)

    print("=" * 60)
    print(f"{'풀이':<16} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 60)

    for name, func in solutions:
        for idx, (keymap, targets, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(keymap, targets)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<16} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 60)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
