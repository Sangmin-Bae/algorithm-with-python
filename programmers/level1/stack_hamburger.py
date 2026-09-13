"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 햄버거 만들기
    유형       : Stack
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/133502
    풀이일자   : 2026-09-13
===================================================================================
[문제 요약]
    재료 배열 ingredient에서 [1,2,3,1](빵-야채-고기-빵) 패턴이
    연속으로 등장할 때마다 제거하고 포장 횟수 반환

    제약 조건
        - ingredient 길이: 1 이상 1,000,000 이하
        - 원소: 1(빵), 2(야채), 3(고기)
===================================================================================
[입출력 예시]
    ingredient             | result
    -----------------------|-------
    [2,1,1,2,3,1,2,3,1]   | 2
    [1,3,2,1,2,1,3,1,2]   | 0
===================================================================================
[핵심 — 스택으로 패턴 탐지]
    ingredient를 순차적으로 스택에 쌓으며
    스택 끝 4개가 [1,2,3,1]이면 제거 + 카운트

    스택 방식이 유효한 이유:
        패턴 제거 후 이전 원소와 새 원소가 인접
        → 연쇄 패턴 발견 가능
        예) [1,1,2,3,1,2,3,1]: 6번째에 1개 제거 → [1] 남고 계속 쌓으면 또 패턴 발생

[stack = stack[:-4] 슬라이싱 실패 원인]
    새 리스트 객체 생성 O(N) + 기존 원소 복사
    N=1,000,000에서 최악 O(N²) → TC12 TLE

    del stack[-4:]:
        리스트 끝 제거 → C 레벨 메모리 크기 조정
        O(1) 상수 비용

[ref_two 고정배열이 Python에서도 빠른 이유]
    mine(동적 스택):
        append(): 주기적 메모리 재할당 발생
        del: O(1)이지만 내부 카운터 갱신 비용

    ref_two(고정배열):
        미리 len(ingredient) 크기 할당 → 재할당 없음
        size -= 4: 정수 연산 1회
        슬라이싱 없이 4번 인덱스 직접 비교

    실측 N=1,000,000:
        ref_two: 66.2ms ← 가장 빠름
        ref_one: 107.7ms (슬라이싱 비교 반복)
        mine:    110.4ms (append 재할당)

[ref_one in-place 인덱스 방식]
    ingredient 배열 자체를 스택으로 재사용
    별도 스택 메모리 없음
    idx -= 4: 포인터를 뒤로 당겨 덮어쓰기 효과
    슬라이싱 비교 ingredient[idx-4:idx] == pattern이 반복 비용 발생
===================================================================================
[내 초기 풀이]
    solution_mine: 동적 스택 + del

[개선 포인트]
    solution_mine:    del로 O(1) 제거 → 직관적 - Sub
                      append 재할당 비용 존재
    solution_ref_one: in-place 인덱스, 추가 메모리 없음
                      슬라이싱 비교 반복으로 mine과 비슷
    solution_ref_two: 고정배열 + 정수 포인터 - Best
                      Python에서도 재할당 방지 효과 유효
===================================================================================
[복잡도 분석]
    N = len(ingredient) (최대 1,000,000)

    Mine     - 시간: O(N) | 공간: O(N) - 동적 스택
    Ref_one  - 시간: O(N) | 공간: O(1) - in-place
    Ref_two  - 시간: O(N) | 공간: O(N) - 고정배열 (초기화)
    Best     - 시간: O(N) | 공간: O(N) - Ref_two와 동일
    Sub      - 시간: O(N) | 공간: O(N) - Mine과 동일
"""

import time


# =================================================================================
# Mine solution - 동적 스택 + del
# =================================================================================
def solution_mine(ingredient: list[int]) -> int:
    """
    동적 리스트 스택으로 패턴을 탐지하고 del로 제거하는 초기 풀이

    stack[-4:] == BURGER:
        슬라이싱 O(4) = O(1) 상수 → 문제없음

    del stack[-4:]:
        리스트 끝 제거 O(1)
        stack = stack[:-4] 슬라이싱은 O(N) → TLE (TC12 실패)

    한계:
        append(): 동적 확장 시 주기적 메모리 재할당
        고정배열(ref_two) 대비 약 40% 느림
    """
    answer = 0
    stack = []
    BURGER = [1, 2, 3, 1]

    for i in ingredient:
        stack.append(i)

        if len(stack) >= 4 and stack[-4:] == BURGER:
            answer += 1
            del stack[-4:]

    return answer


# =================================================================================
# Ref solution one - in-place 인덱스 포인터
# =================================================================================
def solution_ref_one(ingredient: list[int]) -> int:
    """
    ingredient 배열 자체를 스택으로 재사용하는 in-place 풀이

    ingredient[idx] = x:
        원소를 앞부분에 덮어쓰며 쌓는 효과

    idx -= 4:
        포인터를 뒤로 당겨 패턴 제거 효과
        다음 원소가 빈자리에 덮어쓰여짐

    추가 메모리 없음:
        ingredient 원본을 스택으로 재활용
        하지만 ingredient[idx-4:idx] == pattern 슬라이싱 반복 비용
    """
    answer = 0
    idx = 0
    pattern = [1, 2, 3, 1]

    for x in ingredient:
        ingredient[idx] = x
        idx += 1

        if idx >= 4 and ingredient[idx - 4:idx] == pattern:
            answer += 1
            idx -= 4

    return answer


# =================================================================================
# Ref solution two - 고정배열 + 정수 포인터
# =================================================================================
def solution_ref_two(ingredient: list[int]) -> int:
    """
    미리 할당된 고정배열과 size 포인터로 메모리 재할당을 방지하는 최적 풀이

    고정배열 [0]*len(ingredient):
        최대 크기를 미리 할당 → append 재할당 없음
        Python에서도 메모리 재할당 방지 효과 유효

    size 포인터:
        stack의 유효 원소 수를 추적
        size -= 4: 정수 연산 1회 → 패턴 제거 효과

    슬라이싱 없는 4번 인덱스 직접 비교:
        stack[size-4]==1 and ... and stack[size-1]==1
        슬라이싱 생성 비용 없음

    실측 N=1,000,000: 66.2ms (mine 110.4ms 대비 40% 빠름)
    """
    answer = 0
    stack = [0] * len(ingredient)
    size = 0

    for i in ingredient:
        stack[size] = i
        size += 1

        if size >= 4 and (
                stack[size - 4] == 1 and stack[size - 3] == 2 and
                stack[size - 2] == 3 and stack[size - 1] == 1):
            answer += 1
            size -= 4

    return answer


# =================================================================================
# Best solution - 고정배열 + 정수 포인터 (ref_two 주석 보강)
# =================================================================================
def solution_best(ingredient: list[int]) -> int:
    """
    고정배열로 재할당 없이 O(N) 시간에 최대 포장 수를 구하는 최적 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        고정배열 + 정수 포인터: C/로우레벨 패턴이 Python에서도 유효
        append 재할당 방지 + 슬라이싱 없는 직접 비교
        실측 40% 우위 (mine 110ms → 66ms)
    """
    answer = 0
    stack = [0] * len(ingredient)
    size = 0

    for i in ingredient:
        stack[size] = i
        size += 1

        if size >= 4 and (
                stack[size - 4] == 1 and stack[size - 3] == 2 and
                stack[size - 2] == 3 and stack[size - 1] == 1):
            answer += 1
            size -= 4

    return answer


# =================================================================================
# Sub solution - 동적 스택 + del (mine 주석 보강)
# =================================================================================
def solution_sub(ingredient: list[int]) -> int:
    """
    동적 스택과 del로 직관적으로 패턴을 탐지하고 제거하는 서브 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        스택 패턴이 코드에 직관적으로 드러남
        del stack[-4:]: O(1) 리스트 끝 제거
        stack = stack[:-4] 슬라이싱 대비 O(N) → O(1) 개선
        Best 대비 append 재할당 비용으로 40% 느림
    """
    answer = 0
    stack = []
    BURGER = [1, 2, 3, 1]

    for i in ingredient:
        stack.append(i)

        if len(stack) >= 4 and stack[-4:] == BURGER:
            answer += 1
            del stack[-4:]

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (ingredient, 기댓값)
        # 공식 예시
        ([2, 1, 1, 2, 3, 1, 2, 3, 1], 2),
        ([1, 3, 2, 1, 2, 1, 3, 1, 2], 0),
        # 추가 케이스:
        # 연쇄 패턴: 첫 번째 제거 후 두 번째 생성
        # [1,1,2,3,1,1,2,3,1] → [1,2,3,1] 제거 → [1] → 다시 쌓으면 [1,1,2,3,1] → 2개
        ([1, 1, 2, 3, 1, 1, 2, 3, 1], 2),
        # 단일 패턴
        ([1, 2, 3, 1],                 1),
        # 패턴 없음
        ([1, 1, 1, 1],                 0),
    ]

    solutions = [
        ("Mine    (동적스택+del) ", solution_mine),
        ("Ref_one (in-place)    ", solution_ref_one),
        ("Ref_two (고정배열)    ", solution_ref_two),
        ("Best    (고정배열)    ", solution_best),
        ("Sub     (동적스택+del)", solution_sub),
    ]

    # 워밍업 스텝
    _ing, _ = test_cases[0]
    for _, func in solutions:
        func(_ing[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (ingredient, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(ingredient[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
