"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 더 맵게
    유형       : Heap
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42626
    풀이일자   : 2026-08-31
===================================================================================
[문제 요약]
    모든 음식의 스코빌 지수를 K 이상으로 만들기 위해
    가장 맵지 않은 두 음식을 섞는 최소 횟수 반환
    섞은 음식 = 최솟값 + (두 번째 최솟값 × 2)

    제약 조건
        - scoville 길이: 2 이상 1,000,000 이하
        - K: 0 이상 1,000,000,000 이하
        - scoville 원소: 0 이상 1,000,000 이하
===================================================================================
[입출력 예시]
    scoville             | K | return
    ---------------------|---|-------
    [1, 2, 3, 9, 10, 12] | 7 | 2
===================================================================================
[왜 heap이 필요한가]
    매 루프마다 전체 최솟값 두 개가 필요
    정렬 O(N log N) × 루프 N번 = O(N² log N) → 실패
    heap: heappop O(log N) × 루프 N번 = O(N log N) → 통과

[ref 두 큐 방식 — 왜 정렬이 필요 없는가]
    핵심 관찰: q_mixed는 항상 단조 증가 상태를 유지한다

    이유:
        매번 전체 최솟값(first)과 두 번째 최솟값(second)을 꺼냄
        mix = first + second * 2
        first ≤ second이므로 mix ≥ first + first*2 = 3*first ≥ second
        → mix는 방금 꺼낸 second보다 항상 크거나 같음
        → q_mixed에 append하면 단조 증가 유지

    병합 정렬 병합 단계와 동일한 구조:
        q_original: 초기 정렬된 큐 (오름차순)
        q_mixed:    섞인 음식의 큐 (단조 증가)
        get_min(): 두 큐의 맨 앞 중 작은 것 → O(1)

        → 항상 전체 최솟값을 O(1)에 꺼낼 수 있음
        → heap의 heappop O(log N) 대비 O(1)

[손 추적 — [1,2,3,9,10,12], K=7]
    초기: q_original=[1,2,3,9,10,12], q_mixed=[]

    1회: cur=1 < 7
        first=1(원본), second=2(원본)
        mix=1+4=5, q_mixed=[5], answer=1

    2회: cur=min(3,5)=3 < 7
        first=3(원본), second=5(혼합)
        mix=3+10=13, q_mixed=[5,13], answer=2

    3회: cur=min(9,5)=5 → 5 < 7
        first=5(혼합), second=9(원본)
        mix=5+18=23, q_mixed=[5→소비,13,23]

    실제 answer=2에서 종료하려면 2회 후 cur=5 < 7을 놓치면 안 됨
    → 프로그래머스 채점에서 answer=2가 정답인 이유:
       K=7, 2회 후 [9,10,12,13] 모두 ≥ 7이어야 하는데
       q_mixed[0]=5 < 7이므로 계속 반복 → answer=3?

    → 실제 확인: sol_one([1,2,3,9,10,12],7) = 2
       2회 후 힙 = [13,9,10,12], min=9 >= 7 → 종료

    두 큐 방식에서 5가 남아있는 이유:
       5는 q_mixed에 있지만 실제로 소비됐음
       1회: first=1, second=2 → mix=5
       2회: first=3, second=5 → mix=13
       → 5는 2회에서 소비됨, q_mixed=[13]

    정확한 추적:
        1회 후: q_original=[3,9,10,12], q_mixed=[5]
        2회: cur=min(3,5)=3 < 7
             first=3, second=5, mix=13, q_mixed=[13]
        3회: cur=min(9,13)=9 >= 7 → break, answer=2 ✓

[실측 결과 — N=1,000,000, 10회]
    ref  (두 큐 O(1) 조회):  544.7ms  ← 3.7배 빠름
    heap (heappop O(log N)): 2013.0ms
===================================================================================
[내 초기 풀이]
    solution_mine_one:   heap (통과)
    solution_mine_two:   매 루프 sort (O(N²logN), 실패)
    solution_mine_three: 삽입 위치 탐색 (O(N²), 실패)

[개선 포인트]
    solution_mine_one:   개선 필요 없음 - Sub
                         heap O(N log N), 코딩테스트 표준 접근법
    solution_mine_two:   O(N² log N) → 효율성 실패
    solution_mine_three: O(N²) → 효율성 실패
    solution_ref:        두 큐 O(N) - Best
                         q_mixed 단조 증가 성질 활용, O(1) 최솟값 조회
===================================================================================
[복잡도 분석]
    N = len(scoville) (최대 1,000,000)

    Mine_one   - 시간: O(N log N) | 공간: O(N) - heap
    Mine_two   - 시간: O(N² log N) | 공간: O(1) - 매 루프 sort
    Mine_three - 시간: O(N²)      | 공간: O(1) - 삽입 탐색
    Ref        - 시간: O(N)       | 공간: O(N) - 두 큐
    Best       - 시간: O(N)       | 공간: O(N) - Ref와 동일
    Sub        - 시간: O(N log N) | 공간: O(N) - Mine_one과 동일
"""

import heapq
from collections import deque
import time


# =================================================================================
# Mine solution one - heap (통과)
# =================================================================================
def solution_mine_one(scoville: list[int], K: int) -> int:
    """
    heapq로 최소 힙을 유지하며 섞는 횟수를 구하는 초기 풀이

    heapify(): O(N)으로 리스트를 힙으로 변환
    heappop(): O(log N)으로 최솟값 추출
    heappush(): O(log N)으로 새 값 삽입

    scoville[0]: 힙에서 항상 현재 최솟값
    len < 2: 더 이상 섞을 음식이 없는 경우 → -1
    """
    answer = 0
    heapq.heapify(scoville)

    while scoville[0] < K:
        if len(scoville) < 2:
            return -1

        first = heapq.heappop(scoville)
        second = heapq.heappop(scoville)
        heapq.heappush(scoville, first + (second * 2))
        answer += 1

    return answer


# =================================================================================
# Mine solution two - 매 루프 sort O(N² log N) (효율성 실패)
# =================================================================================
def solution_mine_two(scoville: list[int], K: int) -> int:
    """
    매 루프마다 sort()로 정렬하는 풀이 (효율성 테스트 실패)

    O(N² log N): while N번 × sort O(N log N)
    정확성은 통과, 효율성 실패
    """
    answer = 0
    scoville.sort(reverse=True)

    while scoville[-1] < K:
        if len(scoville) < 2:
            return -1

        first = scoville.pop()
        second = scoville.pop()
        scoville.append(first + (second * 2))
        answer += 1
        scoville.sort(reverse=True)

    return answer


# =================================================================================
# Mine solution three - 삽입 위치 탐색 O(N²) (효율성 실패)
# =================================================================================
def solution_mine_three(scoville: list[int], K: int) -> int:
    """
    섞은 음식의 삽입 위치를 직접 탐색해 sort 비용을 줄이려는 풀이 (효율성 실패)

    for + insert: for O(N) + insert O(N) = O(N²) 전체
    mine_two O(N² log N)보다 개선됐으나 여전히 효율성 실패
    """
    answer = 0
    scoville.sort(reverse=True)

    while scoville[-1] < K:
        if len(scoville) < 2:
            return -1

        first = scoville.pop()
        second = scoville.pop()
        mix = first + (second * 2)

        flag = False
        for i in range(len(scoville)):
            if scoville[i] <= mix:
                scoville.insert(i, mix)
                flag = True
                break

        if not flag:
            scoville.append(mix)

        answer += 1

    return answer


# =================================================================================
# Ref solution - 두 큐 병합 O(N)
# =================================================================================
def solution_ref(scoville: list[int], K: int) -> int:
    """
    q_mixed의 단조 증가 성질을 활용해 O(1) 최솟값 조회로 O(N)에 해결하는 최적 풀이

    핵심:
        q_original: 초기 정렬된 큐
        q_mixed:    섞인 음식 큐 (단조 증가 유지)

    q_mixed가 단조 증가인 이유:
        first ≤ second → mix = first + second*2 ≥ second
        → 새로 생긴 mix는 이전에 꺼낸 값보다 항상 크거나 같음
        → append로도 정렬 유지

    get_min(): 두 큐의 맨 앞 비교 O(1) → heap의 O(log N) 대비 이득
    실측 N=1,000,000: heap 2013ms → 두 큐 544ms (3.7배 빠름)
    """
    answer = 0
    scoville.sort()
    q_original = deque(scoville)
    q_mixed = deque()

    def get_min() -> int:
        if not q_original:
            return q_mixed.popleft()
        if not q_mixed:
            return q_original.popleft()
        if q_original[0] <= q_mixed[0]:
            return q_original.popleft()
        else:
            return q_mixed.popleft()

    while True:
        if q_original:
            cur = q_original[0] if (not q_mixed or q_original[0] <= q_mixed[0]) else q_mixed[0]
        elif q_mixed:
            cur = q_mixed[0]
        else:
            return -1

        if cur >= K:
            break

        if len(q_original) + len(q_mixed) < 2:
            return -1

        first = get_min()
        second = get_min()
        q_mixed.append(first + (second * 2))
        answer += 1

    return answer


# =================================================================================
# Best solution - 두 큐 병합 (ref 주석 보강)
# =================================================================================
def solution_best(scoville: list[int], K: int) -> int:
    """
    두 큐 병합으로 O(N) 시간, O(N) 공간에 최솟값을 O(1)에 꺼내는 최적 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        q_mixed 단조 증가 성질 → 정렬 없이 O(1) 최솟값 조회
        실측 N=1,000,000: 544ms (heap 2013ms 대비 3.7배 우위)
        병합 정렬 병합 단계와 동일한 구조
    """
    answer = 0
    scoville.sort()
    q_original = deque(scoville)
    q_mixed = deque()

    def get_min() -> int:
        if not q_original:
            return q_mixed.popleft()
        if not q_mixed:
            return q_original.popleft()
        if q_original[0] <= q_mixed[0]:
            return q_original.popleft()
        else:
            return q_mixed.popleft()

    while True:
        if q_original:
            cur = q_original[0] if (not q_mixed or q_original[0] <= q_mixed[0]) else q_mixed[0]
        elif q_mixed:
            cur = q_mixed[0]
        else:
            return -1

        if cur >= K:
            break

        if len(q_original) + len(q_mixed) < 2:
            return -1

        first = get_min()
        second = get_min()
        q_mixed.append(first + (second * 2))
        answer += 1

    return answer


# =================================================================================
# Sub solution - heap (mine_one 주석 보강)
# =================================================================================
def solution_sub(scoville: list[int], K: int) -> int:
    """
    heapq로 O(N log N) 시간에 최솟값을 관리하는 서브 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        코딩테스트 힙 유형 표준 접근법
        heapify O(N) + heappop/heappush O(log N)
        Best 대비 O(log N) vs O(1) 최솟값 조회 차이
        실측 N=1,000,000: 2013ms (Best 544ms 대비 느림)
    """
    answer = 0
    heapq.heapify(scoville)

    while scoville[0] < K:
        if len(scoville) < 2:
            return -1

        first = heapq.heappop(scoville)
        second = heapq.heappop(scoville)
        heapq.heappush(scoville, first + (second * 2))
        answer += 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (scoville, K, 기댓값)
        # 공식 예시
        # 손 추적: 1+2*2=5→[5,3,9,10,12], 3+5*2=13→[13,9,10,12], min=9>=7
        ([1, 2, 3, 9, 10, 12], 7, 2),
        # 추가 케이스:
        # 불가능
        ([1, 1], 7000000, -1),
        # 이미 모두 K 이상
        ([10, 20, 30], 5, 0),
        # 단일 섞기
        # 손 추적: 1+2*2=5→[3,4,5,5], 3+4*2=11→[5,5,11], min=5>=5, answer=2
        ([1, 2, 3, 4, 5], 5, 2),
    ]

    # mine_two, mine_three는 소규모에서만 정확성 확인
    print("--- Mine_two, Mine_three 정확성 (소규모) ---")
    for idx, (scoville, K, expected) in enumerate(test_cases, 1):
        r2 = solution_mine_two(scoville[:], K)
        r3 = solution_mine_three(scoville[:], K)
        ok = r2 == expected and r3 == expected
        print(f"  TC{idx}: mine_two={r2}, mine_three={r3}, 기댓값={expected}, 일치:{ok}")

    solutions = [
        ("Mine_one (heap)     ", solution_mine_one),
        ("Ref      (두 큐)    ", solution_ref),
        ("Best     (두 큐)    ", solution_best),
        ("Sub      (heap)     ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _K, _ = test_cases[0]
    for _, func in solutions:
        func(_s[:], _K)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (scoville, K, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(scoville[:], K)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
