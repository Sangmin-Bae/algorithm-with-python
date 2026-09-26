"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 다리를 지나는 트럭
    유형       : Queue / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42583
    풀이일자   : 2026-09-26
===================================================================================
[문제 요약]
    bridge_length 길이, weight 한도의 다리에서
    truck_weights 순서대로 건널 때 모든 트럭이 건너는 최소 시간 반환

    제약 조건
        - bridge_length: 1~10,000
        - weight: 1~10,000
        - truck_weights 길이: 1~10,000
===================================================================================
[입출력 예시]
    bridge_length | weight | truck_weights       | return
    --------------|--------|---------------------|-------
    2             | 10     | [7, 4, 5, 6]        | 8
    100           | 100    | [10]                | 101
    100           | 100    | [10]*10             | 110
===================================================================================
[핵심 — 두 가지 설계 선택]

    방법 A (0-패딩):
        bridge를 0으로 채워 시작
        → bridge가 항상 bridge_length 크기 유지
        → while bridge 조건 사용 가능
        → 매 tick마다 1칸씩 이동 시뮬레이션
        → O(bridge_length × truck_count) 최악 O(10^8)

    방법 B (time skip):
        bridge에 (무게, 다리 통과 절대시간) 튜플 저장
        → 무게 초과 시 다음 통과 시점으로 time 점프
        → O(truck_count) = 최악 O(10,000)

[ref_one — 0-패딩 방식]
    bridge = deque([0] * bridge_length)
    매 tick: popleft()로 앞 제거, append()로 뒤 추가
    trucks 없으면 0 추가 → bridge 크기 유지
    while bridge: bridge가 완전히 빌 때 종료

    손 추적 bl=2, w=10, trucks=[7,4,5,6]:
        t=1: out=0, 7≤10 → bridge=[0,7], curr=7
        t=2: out=0, 4+7>10 → bridge=[7,0], curr=7
        t=3: out=7, 4≤10 → bridge=[0,4], curr=4
        t=4: out=0, 4+5≤10 → bridge=[4,5], curr=9
        t=5: out=4, 5+6>10 → bridge=[5,0], curr=5
        t=6: out=5, 6≤10 → bridge=[0,6], curr=6
        t=7: out=0, trucks없음 → bridge=[6,0]
        t=8: out=6, bridge=[0] → 다음 popleft 시 빔
        return 8 ✓

[ref_two — time skip 방식]
    bridge = deque()  (비어있는 상태로 시작)
    bridge에 (무게, time + bridge_length) 튜플 저장
    bridge[0][1] == time: 이번 tick에 맨 앞 트럭이 다리 통과

    time skip:
        무게 초과 시 time = bridge[0][1] - 1
        다음 while 루프에서 time += 1 → bridge[0][1] 시점으로 점프
        불필요한 tick 건너뜀 → O(truck_count)

    while trucks or bridge:
        trucks가 남았거나 bridge 위 트럭이 있으면 계속

[ref_three — 인덱스 포인터 방식]
    0-패딩과 동일하지만 trucks를 deque 대신 인덱스로 접근
    while curr_weight > 0 or truck_idx < num_of_trucks
    deque 객체 생성 비용 절감, 실측 차이 미미

[실측 결과 — bridge_length=10000, trucks=10000, 5회]
    ref_two   (time skip):    2.4ms  ← 16배 빠름
    ref_three (인덱스포인터): 36.9ms
    ref_one   (0-패딩):      39.0ms
===================================================================================
[내 초기 풀이]
    해결 못함 — while 조건 구성에서 막힘
    구조까지는 설계했으나 빈 bridge 초기화 문제 해결 못함

[핵심 돌파구]
    1. 0-패딩: 더미 0 트럭으로 bridge를 채워 시작
    2. time skip: 무게 초과 시 다음 통과 시점으로 직접 점프

[Best/Sub 선정]
    Best: ref_two (time skip) — O(N), 16배 빠름
    Sub:  ref_one (0-패딩) — 직관적, 구조 이해 쉬움
===================================================================================
[복잡도 분석]
    N = len(truck_weights) (최대 10,000)
    L = bridge_length (최대 10,000)

    Ref_one   - 시간: O(N×L) | 공간: O(L+N) - 최악 O(10^8)
    Ref_two   - 시간: O(N)   | 공간: O(N) - time skip으로 tick 최소화
    Ref_three - 시간: O(N×L) | 공간: O(L) - 인덱스 포인터
    Best      - 시간: O(N)   | 공간: O(N) - Ref_two와 동일
    Sub       - 시간: O(N×L) | 공간: O(L+N) - Ref_one과 동일
"""

from collections import deque
import time


# =================================================================================
# Ref solution one - 0-패딩 bridge + trucks deque
# =================================================================================
def solution_ref_one(bridge_length: int, weight: int, truck_weights: list[int]) -> int:
    """
    bridge를 0으로 채워 매 tick마다 1칸씩 이동하는 시뮬레이션 풀이

    0-패딩 핵심:
        bridge = deque([0] * bridge_length)
        매 tick: popleft()로 앞 제거, append()로 뒤 추가
        trucks 없으면 0 추가 → bridge 크기 유지
        while bridge: bridge가 완전히 빌 때 종료

    O(N×L) 최악: bridge_length=10,000, trucks=10,000이면 10^8 tick
    """
    time_val = 0
    trucks = deque(truck_weights)
    bridge = deque([0] * bridge_length)
    curr_weight = 0

    while bridge:
        time_val += 1
        out_truck = bridge.popleft()
        curr_weight -= out_truck

        if trucks:
            if curr_weight + trucks[0] <= weight:
                next_truck = trucks.popleft()
                bridge.append(next_truck)
                curr_weight += next_truck
            else:
                bridge.append(0)

    return time_val


# =================================================================================
# Ref solution two - time skip
# =================================================================================
def solution_ref_two(bridge_length: int, weight: int, truck_weights: list[int]) -> int:
    """
    (무게, 통과 절대시간) 튜플로 time skip을 구현하는 최적 풀이

    bridge에 (truck_weight, time + bridge_length) 저장
    bridge[0][1] == time: 이번 tick에 맨 앞 트럭 통과

    time skip:
        무게 초과 → time = bridge[0][1] - 1
        다음 루프 time += 1 → bridge[0][1] 시점으로 점프
        불필요한 tick 없음 → O(N)

    실측 O(N×L) 대비 16배 빠름
    """
    trucks = deque(truck_weights)
    bridge = deque()
    time_val = 0
    curr_weight = 0

    while trucks or bridge:
        time_val += 1

        if bridge and bridge[0][1] == time_val:
            out_truck, _ = bridge.popleft()
            curr_weight -= out_truck

        if trucks:
            if curr_weight + trucks[0] <= weight:
                next_truck = trucks.popleft()
                curr_weight += next_truck
                bridge.append((next_truck, time_val + bridge_length))
            else:
                time_val = bridge[0][1] - 1

    return time_val


# =================================================================================
# Ref solution three - 0-패딩 bridge + 인덱스 포인터
# =================================================================================
def solution_ref_three(bridge_length: int, weight: int, truck_weights: list[int]) -> int:
    """
    0-패딩 방식에서 trucks를 deque 대신 인덱스로 접근하는 풀이

    ref_one과 동일한 방식이지만:
        trucks deque 생성 없이 truck_idx 포인터로 접근
        while curr_weight > 0 or truck_idx < num_of_trucks

    deque 객체 생성 비용 절감, 실측 차이 미미
    """
    bridge = deque([0] * bridge_length)
    time_val = 0
    curr_weight = 0
    truck_idx = 0
    num_of_trucks = len(truck_weights)

    while curr_weight > 0 or truck_idx < num_of_trucks:
        time_val += 1

        out_truck = bridge.popleft()
        curr_weight -= out_truck

        if truck_idx < num_of_trucks:
            if curr_weight + truck_weights[truck_idx] <= weight:
                next_truck = truck_weights[truck_idx]
                bridge.append(next_truck)
                curr_weight += next_truck
                truck_idx += 1
            else:
                bridge.append(0)
        elif curr_weight > 0:
            bridge.append(0)

    return time_val


# =================================================================================
# Best solution - time skip (ref_two 주석 보강)
# =================================================================================
def solution_best(bridge_length: int, weight: int, truck_weights: list[int]) -> int:
    """
    time skip으로 O(N) 시간에 모든 트럭이 건너는 시간을 구하는 최적 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        O(N): tick을 트럭 수만큼만 실행 (O(N×L) 대비 압도적)
        실측 최악 규모: 2.4ms (0-패딩 39ms 대비 16배 우위)
        bridge[0][1] - 1로 점프 → 불필요한 tick 완전 제거
    """
    trucks = deque(truck_weights)
    bridge = deque()
    time_val = 0
    curr_weight = 0

    while trucks or bridge:
        time_val += 1

        if bridge and bridge[0][1] == time_val:
            out_truck, _ = bridge.popleft()
            curr_weight -= out_truck

        if trucks:
            if curr_weight + trucks[0] <= weight:
                next_truck = trucks.popleft()
                curr_weight += next_truck
                bridge.append((next_truck, time_val + bridge_length))
            else:
                time_val = bridge[0][1] - 1

    return time_val


# =================================================================================
# Sub solution - 0-패딩 (ref_one 주석 보강)
# =================================================================================
def solution_sub(bridge_length: int, weight: int, truck_weights: list[int]) -> int:
    """
    0-패딩 bridge로 직관적으로 시뮬레이션하는 서브 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        0으로 채운 bridge → "빈 자리를 무게 0 트럭이 점유"로 모델링
        while bridge 조건: bridge가 완전히 빌 때 = 마지막 트럭 통과 완료
        매 tick마다 1칸 이동 → 코드와 지문이 1:1 대응
        Best 대비 O(N×L)로 최악 규모에서 16배 느림
    """
    time_val = 0
    trucks = deque(truck_weights)
    bridge = deque([0] * bridge_length)
    curr_weight = 0

    while bridge:
        time_val += 1
        out_truck = bridge.popleft()
        curr_weight -= out_truck

        if trucks:
            if curr_weight + trucks[0] <= weight:
                next_truck = trucks.popleft()
                bridge.append(next_truck)
                curr_weight += next_truck
            else:
                bridge.append(0)

    return time_val


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (bridge_length, weight, truck_weights, 기댓값)
        # 공식 예시
        (2,   10,  [7, 4, 5, 6],     8),
        (100, 100, [10],              101),
        (100, 100, [10] * 10,         110),
        # 추가 케이스:
        # 단일 트럭, 짧은 다리
        # 손 추적: bl=1, w=10, [5] → t=1: bridge=[5] → t=2: bridge=[] → return 2
        (1,   10,  [5],               2),
        # 모든 트럭이 한번에 올라갈 수 있음
        (5,   100, [1, 1, 1, 1, 1],  10),
    ]

    solutions = [
        ("Ref_one   (0-패딩)       ", solution_ref_one),
        ("Ref_two   (time skip)    ", solution_ref_two),
        ("Ref_three (인덱스포인터) ", solution_ref_three),
        ("Best      (time skip)    ", solution_best),
        ("Sub       (0-패딩)       ", solution_sub),
    ]

    # 워밍업
    _bl, _w, _tw, _ = test_cases[0]
    for _, func in solutions:
        func(_bl, _w, _tw[:])

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (bridge_length, weight, truck_weights, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(bridge_length, weight, truck_weights[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
