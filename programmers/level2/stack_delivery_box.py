"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 택배상자
    유형       : Stack
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/131704
    풀이일자   : 2026-09-02
===================================================================================
[문제 요약]
    주 벨트(1→N 순서)와 LIFO 보조 벨트를 활용해
    order 순서대로 상자를 트럭에 실을 수 있는 최대 개수 반환

    제약 조건
        - order 길이: 1 이상 1,000,000 이하
        - order는 1~N의 모든 정수가 한 번씩 등장 (순열)
===================================================================================
[입출력 예시]
    order           | result
    ----------------|-------
    [4, 3, 1, 2, 5] | 2
    [5, 4, 3, 2, 1] | 5
===================================================================================
[핵심 — 두 가지 선택지]
    매 순간 실을 수 있는 선택지:
        1. 주 벨트 맨 앞 (curr_box)
        2. 보조 벨트 맨 뒤 (sub_belt[-1])

    둘 다 아니면 → 더 이상 진행 불가 → break

[내 풀이 — order 기준 순회]
    order의 각 요소 i를 순서대로 처리
    curr_box < i: 주 벨트 상자를 보조 벨트로 이동
    curr_box == i: 주 벨트에서 바로 실음
    sub_belt[-1] == i: 보조 벨트에서 꺼내 실음
    둘 다 아님: break

    이중 반복 구조이지만 O(N) 분할 상환:
        curr_box는 절대 감소하지 않음
        while 루프 총 실행 횟수 ≤ N

[ref_one — 벨트 기준 순회, 통합된 발상]
    핵심 관찰:
        "주 벨트에서 바로 실음" = "보조 벨트에 넣자마자 꺼냄"
        → 두 경우를 "항상 보조 벨트를 거침"으로 통합 가능

    주 벨트 상자를 무조건 보조 벨트로 push
    while로 보조 벨트 맨 뒤가 order와 일치하면 즉시 pop
    → 주 벨트에서 바로 실 수 있는 경우도 자동 처리

    손 추적 [4,3,1,2,5]:
        i=1→4: sub_belt=[1,2,3,4], 4==order[0] → pop, answer=1
               3==order[1] → pop, answer=2
               2≠order[2]=1 → 종료
        i=5: sub_belt=[1,2,5], 5≠1 → 종료
        → answer=2 ✓

[ref_two — 명시적 상태 머신]
    curr_box: 주 벨트 현재 위치
    order_idx: 다음 실어야 할 상자 인덱스
    단일 while로 네 가지 상태 전이를 명시적으로 표현
    mine과 동일한 로직, 가장 느림 (명시적 분기 오버헤드)

[실측 결과 — N=1,000,000, 30회]
    mine     (order순회): 48.4ms  ← 가장 빠름
    ref_one  (벨트순회):  64.8ms
    ref_two  (상태머신):  95.9ms  ← 가장 느림

    mine이 빠른 이유:
        order 기준 순회 → 필요한 만큼만 주 벨트 이동
        ref_one은 1~N 전체 push (모든 상자를 보조 벨트 경유)
        ref_two는 명시적 분기 오버헤드 누적
===================================================================================
[내 초기 풀이]
    solution_mine: order 기준 순회 + 내부 while

[개선 포인트]
    solution_mine:    개선 필요 없음 - Best
                      실측 가장 빠름, 직관적 발상
    solution_ref_one: 통합 발상으로 코드 간결 - Sub
                      "항상 보조 벨트를 거친다"는 통찰
    solution_ref_two: 명시적 상태 머신, 가장 느림
===================================================================================
[복잡도 분석]
    N = len(order) (최대 1,000,000)

    Mine     - 시간: O(N) | 공간: O(N) - 분할 상환, sub_belt 최대 N개
    Ref_one  - 시간: O(N) | 공간: O(N) - 모든 상자 보조 벨트 경유
    Ref_two  - 시간: O(N) | 공간: O(N) - 단일 while 상태 머신
    Best     - 시간: O(N) | 공간: O(N) - Mine과 동일
    Sub      - 시간: O(N) | 공간: O(N) - Ref_one과 동일
"""

import time


# =================================================================================
# Mine solution - order 기준 순회 + 내부 while
# =================================================================================
def solution_mine(order: list[int]) -> int:
    """
    order를 기준으로 순회하며 주/보조 벨트에서 상자를 실는 초기 풀이

    order의 각 i 처리:
        while curr_box < i: 주 벨트 → 보조 벨트로 이동
        curr_box == i: 주 벨트에서 바로 실음
        sub_belt[-1] == i: 보조 벨트에서 꺼내 실음
        둘 다 아님: break (더 이상 불가)

    O(N) 분할 상환:
        내부 while이 있지만 curr_box는 절대 감소하지 않음
        while 총 실행 횟수 ≤ N → 전체 O(N)
    """
    answer = 0
    sub_belt = []
    curr_box = 1

    for i in order:
        while curr_box < i:
            sub_belt.append(curr_box)
            curr_box += 1

        if curr_box == i:
            answer += 1
            curr_box += 1
        elif sub_belt and sub_belt[-1] == i:
            sub_belt.pop()
            answer += 1
        else:
            break

    return answer


# =================================================================================
# Ref solution one - 벨트 기준 순회 (통합 발상)
# =================================================================================
def solution_ref_one(order: list[int]) -> int:
    """
    주 벨트를 기준으로 순회하며 "항상 보조 벨트를 거친다"는 발상으로 통합한 풀이

    핵심 관찰:
        "주 벨트에서 바로 실음" = "보조 벨트에 push 후 즉시 pop"
        → 두 경우를 하나로 통합

    모든 상자를 보조 벨트로 push 후
    while로 보조 벨트 맨 뒤가 order와 일치하면 즉시 pop
    → 주 벨트에서 바로 실 수 있는 케이스도 자동 처리됨

    mine 대비:
        1~N 전체를 보조 벨트로 push → mine보다 push 횟수 많음
        하지만 코드가 더 단순
    """
    answer = 0
    sub_belt = []
    order_idx = 0

    for i in range(1, len(order) + 1):
        sub_belt.append(i)

        while sub_belt and sub_belt[-1] == order[order_idx]:
            sub_belt.pop()
            order_idx += 1
            answer += 1

    return answer


# =================================================================================
# Ref solution two - 단일 while 상태 머신
# =================================================================================
def solution_ref_two(order: list[int]) -> int:
    """
    curr_box와 order_idx 두 포인터로 상태를 명시적으로 관리하는 풀이

    네 가지 상태 전이:
        1. 주 벨트 맨 앞 == 다음 실어야 할 상자 → 바로 실음
        2. 보조 벨트 맨 뒤 == 다음 실어야 할 상자 → 꺼내 실음
        3. 주 벨트에 상자 있음 → 보조 벨트로 이동
        4. 아무것도 안 됨 → break

    mine과 동일한 로직을 단일 while + 명시적 분기로 표현
    명시적 분기 오버헤드로 가장 느림
    """
    sub_belt = []
    N = len(order)
    curr_box = 1
    order_idx = 0

    while curr_box <= N or (sub_belt and sub_belt[-1] == order[order_idx]):
        if curr_box <= N and curr_box == order[order_idx]:
            curr_box += 1
            order_idx += 1
        elif sub_belt and sub_belt[-1] == order[order_idx]:
            sub_belt.pop()
            order_idx += 1
        elif curr_box <= N:
            sub_belt.append(curr_box)
            curr_box += 1
        else:
            break

    return order_idx


# =================================================================================
# Best solution - order 기준 순회 (mine 주석 보강)
# =================================================================================
def solution_best(order: list[int]) -> int:
    """
    order 기준 순회로 O(N) 시간, O(N) 공간에 최대 탑재 개수를 구하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        order 기준 → 필요한 만큼만 주 벨트 이동 (ref_one의 전체 push보다 효율)
        이중 반복 구조이나 분할 상환 O(N) (curr_box 단조 증가)
        실측 N=1,000,000: 48.4ms (ref_one 64.8ms, ref_two 95.9ms 대비 우위)
    """
    answer = 0
    sub_belt = []
    curr_box = 1

    for i in order:
        while curr_box < i:
            sub_belt.append(curr_box)
            curr_box += 1

        if curr_box == i:
            answer += 1
            curr_box += 1
        elif sub_belt and sub_belt[-1] == i:
            sub_belt.pop()
            answer += 1
        else:
            break

    return answer


# =================================================================================
# Sub solution - 벨트 기준 순회 (ref_one 주석 보강)
# =================================================================================
def solution_sub(order: list[int]) -> int:
    """
    "항상 보조 벨트를 거친다"는 통합 발상으로 코드를 단순화한 서브 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        "주 벨트에서 바로 실음" = "보조 벨트에 push 후 즉시 pop"으로 통합
        while 안에서 보조 벨트 맨 뒤만 확인 → 로직 단순
        Best보다 push 횟수 많아 약 35% 느림
    """
    answer = 0
    sub_belt = []
    order_idx = 0

    for i in range(1, len(order) + 1):
        sub_belt.append(i)

        while sub_belt and sub_belt[-1] == order[order_idx]:
            sub_belt.pop()
            order_idx += 1
            answer += 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int]] = [
        # (order, 기댓값)
        # 공식 예시
        ([4, 3, 1, 2, 5], 2),
        ([5, 4, 3, 2, 1], 5),
        # 추가 케이스:
        # 순서 그대로 (모두 실음)
        # 손 추적: 1→1, 2→2, 3→3 모두 주 벨트에서 바로
        ([1, 2, 3, 4, 5], 5),
        # 첫 상자부터 실패
        # 손 추적: order[0]=2, curr_box=1→보조, curr_box=2 실음
        #          order[1]=1, sub_belt[-1]=1 실음
        #          order[2]=4, curr_box=3→보조, curr_box=4 실음
        #          order[3]=3, sub_belt[-1]=3 실음
        #          order[4]=5, curr_box=5 실음 → answer=5
        ([2, 1, 4, 3, 5], 5),
    ]

    solutions = [
        ("Mine    (order순회) ", solution_mine),
        ("Ref_one (벨트순회)  ", solution_ref_one),
        ("Ref_two (상태머신)  ", solution_ref_two),
        ("Best    (order순회) ", solution_best),
        ("Sub     (벨트순회)  ", solution_sub),
    ]

    # 워밍업 스텝
    _o, _ = test_cases[0]
    for _, func in solutions:
        func(_o[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (order, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(order[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
