"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 야근 지수
    유형       : Heap / Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12927
    풀이일자   : 2026-09-08
===================================================================================
[문제 요약]
    n시간 동안 작업량을 줄여 야근 피로도(남은 작업량 제곱합)를 최소화
    최소화한 피로도 반환

    제약 조건
        - works 길이: 1 이상 20,000 이하
        - works 원소: 50,000 이하 자연수
        - n: 1,000,000 이하 자연수
===================================================================================
[입출력 예시]
    works     | n | result
    ----------|---|-------
    [4, 3, 3] | 4 | 12     ([2,2,2] → 4+4+4)
    [2, 1, 2] | 1 | 6      ([1,1,2] → 1+1+4)
    [1, 1]    | 3 | 0
===================================================================================
[greedy 핵심 — 왜 최대값을 줄여야 하는가]
    피로도 = Σ(작업량²)
    제곱 함수의 볼록성(convexity):
        큰 값을 줄이는 감소량이 작은 값을 줄이는 것보다 항상 피로도 감소에 유리
        예) 값 4 → 3: 4²-3² = 7 감소
            값 2 → 1: 2²-1² = 3 감소
        → 항상 최대값을 1씩 줄이는 것이 최적

[풀이1 실패 원인 — 작업량 증가 불가 조건 위반]
    works=[10,1,1], n=3
    rest = 12-3 = 9
    avg = 3, remain = 0
    → [3,3,3]으로 균등 배분 시도
    문제: works[1]=1, works[2]=1을 3으로 올리는 것은 불가능
          작업량은 줄일 수만 있고 늘릴 수 없음
    → individual works의 하한선을 무시한 결함

[풀이2 — heap 방식]
    n번 개별 감소: 매번 heappop + heappush
    n=1,000,000이면 1,000,000번 × O(log N) 연산
    → O(n log N) ≈ O(15,000,000) → 실측 293ms

[풀이3 — 정렬 + 배치 감소]
    정렬 후 최대값과 같은 그룹을 한꺼번에 감소
    heap 없이도 동일한 greedy 원칙 구현
    O(N²/k) 수준 → 실측 64.9ms

[ref — 카운팅 배열 방식]
    핵심 발상: "개별 감소"가 아닌 "그룹 이동"

    counts[i] = "작업량이 i인 일의 개수"
    예) works=[4,3,3] → counts=[0,0,0,2,1]

    최대값 그룹 전체를 한 번에 (i) → (i-1)로 이동:
        counts[current_max] -= reduce_amount
        counts[current_max - 1] += reduce_amount

    "같은 높이의 공을 한꺼번에 한 칸 내림"

    왜 빠른가:
        heap: n번 개별 연산 → O(n log N)
        ref:  max_work 수준 반복 → O(max_work) = O(50,000)
        n이 아무리 커도 max_work(50,000)을 넘지 않음

[손 추적 — works=[4,3,3], n=4]
    counts = [0,0,0,2,1], current_max=4

    1단계: counts[4]=1, reduce=min(4,1)=1
           counts[4]=0, counts[3]=3, n=3

    2단계: counts[4]=0 → current_max=3
           counts[3]=3, reduce=min(3,3)=3
           counts[3]=0, counts[2]=3, n=0

    counts=[0,0,3,0,0] → answer=2²×3=12 ✓

[실측 결과 — works=20,000, n=1,000,000, 30회]
    ref   (counting): 3.6ms   ← 82배 빠름
    three (sort):    64.9ms
    two   (heap):   293.2ms   ← 가장 느림
===================================================================================
[내 초기 풀이]
    solution_mine_one:   평균 배분 (정확성 실패)
    solution_mine_two:   heap O(n log N)
    solution_mine_three: 정렬+배치감소

[개선 포인트]
    solution_mine_one:   작업량 증가 불가 조건 위반 → 결함 있음
    solution_mine_two:   heap 직관적 - Sub
                         O(n log N)으로 대규모 입력에서 느림
    solution_mine_three: O(N²/k) 수준 → ref보다 느림
    solution_ref:        카운팅 배열 O(max_work) - Best
                         압도적 성능 우위
===================================================================================
[복잡도 분석]
    N = len(works) (최대 20,000)
    W = max(works) (최대 50,000)
    n = 야근 시간 (최대 1,000,000)

    Mine_one   - 시간: O(N) | 공간: O(1) — 정확성 실패
    Mine_two   - 시간: O(n log N) | 공간: O(N) — heap
    Mine_three - 시간: O(N²/k) | 공간: O(N) — 정렬+배치
    Ref        - 시간: O(N + W) | 공간: O(W) — 카운팅
    Best       - 시간: O(N + W) | 공간: O(W) — Ref와 동일
    Sub        - 시간: O(n log N) | 공간: O(N) — Mine_two와 동일
"""

import heapq
import time


# =================================================================================
# Mine solution one - 평균 배분 (정확성 실패)
# =================================================================================
def solution_mine_one(n: int, works: list[int]) -> int:
    """
    n시간 후 남은 총 작업량을 균등 배분하려는 초기 풀이 (정확성 실패)

    실패 원인:
        avg = rest // N, remain = rest % N으로 균등 배분 시도
        works[i] < avg인 경우 작업량을 올려야 해서 조건 위반
        예) works=[10,1,1], n=3 → [3,3,3] 시도하지만 1→3은 불가
        개별 works의 하한선(현재 값)을 무시한 결함
    """
    N = len(works)
    rest = sum(works) - n

    if rest <= 0:
        return 0

    avg = rest // N
    remain = rest % N

    return (avg ** 2) * (N - remain) + ((avg + 1) ** 2) * remain


# =================================================================================
# Mine solution two - heap O(n log N)
# =================================================================================
def solution_mine_two(n: int, works: list[int]) -> int:
    """
    최대 힙으로 n번 개별 감소시키는 풀이

    음수 변환 최대 힙:
        heapq는 최소 힙 → 음수로 변환하면 최대 힙 구현
        heappop: 가장 큰 값(음수 최솟값) 추출

    n번 반복:
        매번 최대값 1 감소 → heappush로 재삽입
        → O(n log N) 연산

    한계:
        n=1,000,000이면 1,000,000번 × O(log N) 연산
        실측 293ms (ref 3.6ms 대비 82배 느림)
    """
    if sum(works) <= n:
        return 0

    max_heap = [-w for w in works]
    heapq.heapify(max_heap)

    for _ in range(n):
        max_work = heapq.heappop(max_heap)
        if max_work == 0:
            break
        heapq.heappush(max_heap, max_work + 1)

    return sum(w ** 2 for w in max_heap)


# =================================================================================
# Mine solution three - 정렬 + 배치 감소
# =================================================================================
def solution_mine_three(n: int, works: list[int]) -> int:
    """
    정렬 후 최대값 그룹을 배치로 감소시키는 풀이

    핵심:
        내림차순 정렬 후 works[0]과 같은 값의 개수(count) 파악
        count만큼 또는 n까지 동시에 1씩 감소

    heap 없이 동일한 greedy 원칙:
        최대값 그룹 전체를 한 번에 감소
        but 매 루프마다 정렬 상태 유지를 위해 for문으로 count 계산

    실측 64.9ms (ref 3.6ms 대비 18배 느림)
    """
    if sum(works) <= n:
        return 0

    works = sorted(works, reverse=True)
    N = len(works)

    while n > 0:
        max_work = works[0]
        count = 0
        for i in range(N):
            if works[i] == max_work:
                count += 1
            else:
                break

        reduce = min(n, count)
        for i in range(reduce):
            works[i] -= 1

        n -= reduce

    return sum(w ** 2 for w in works)


# =================================================================================
# Ref solution - 카운팅 배열 O(N + max_work)
# =================================================================================
def solution_ref(n: int, works: list[int]) -> int:
    """
    카운팅 배열로 최대값 그룹을 한 번에 이동시키는 최적 풀이

    counts[i] = "작업량이 i인 일의 개수"
    최대값 그룹을 (i) → (i-1)로 한 번에 이동:
        counts[current_max] -= reduce_amount
        counts[current_max - 1] += reduce_amount

    왜 O(max_work)인가:
        heap: n번 개별 연산
        카운팅: 같은 값의 작업들을 1번에 처리
        → 반복 횟수 = max_work 수준 (최대 50,000)
        → n이 아무리 커도 max_work(50,000) 이하로 수렴

    실측: 3.6ms (heap 293ms 대비 82배 빠름)
    """
    if sum(works) <= n:
        return 0

    max_work = max(works)
    counts = [0] * (max_work + 1)
    for i in works:
        counts[i] += 1

    current_max = max_work
    while n > 0:
        if counts[current_max] == 0:
            current_max -= 1
            continue

        num_of_works = counts[current_max]
        reduce_amount = min(n, num_of_works)

        counts[current_max] -= reduce_amount
        counts[current_max - 1] += reduce_amount

        n -= reduce_amount

    answer = 0
    for score, count in enumerate(counts):
        if count > 0:
            answer += (score ** 2) * count

    return answer


# =================================================================================
# Best solution - 카운팅 배열 (ref 주석 보강)
# =================================================================================
def solution_best(n: int, works: list[int]) -> int:
    """
    카운팅 배열로 O(N + max_work) 시간에 최소 피로도를 구하는 최적 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        n번이 아닌 max_work번 반복 → n에 독립적
        실측 3.6ms (heap 293ms 대비 82배 우위)
        "같은 높이의 공을 한꺼번에 내리는" 발상
    """
    if sum(works) <= n:
        return 0

    max_work = max(works)
    counts = [0] * (max_work + 1)
    for i in works:
        counts[i] += 1

    current_max = max_work
    while n > 0:
        if counts[current_max] == 0:
            current_max -= 1
            continue

        num_of_works = counts[current_max]
        reduce_amount = min(n, num_of_works)

        counts[current_max] -= reduce_amount
        counts[current_max - 1] += reduce_amount

        n -= reduce_amount

    answer = 0
    for score, count in enumerate(counts):
        if count > 0:
            answer += (score ** 2) * count

    return answer


# =================================================================================
# Sub solution - heap (mine_two 주석 보강)
# =================================================================================
def solution_sub(n: int, works: list[int]) -> int:
    """
    heap으로 n번 최대값을 감소시키는 서브 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        greedy 원칙(최대값 우선 감소)을 heap으로 직접 구현
        코드 구조가 알고리즘 흐름과 1:1 대응 → 직관적
        O(n log N)으로 대규모에서 Best 대비 82배 느림
    """
    if sum(works) <= n:
        return 0

    max_heap = [-w for w in works]
    heapq.heapify(max_heap)

    for _ in range(n):
        max_work = heapq.heappop(max_heap)
        if max_work == 0:
            break
        heapq.heappush(max_heap, max_work + 1)

    return sum(w ** 2 for w in max_heap)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (n, works, 기댓값)
        # 공식 예시
        # 손 추적: [4,3,3], n=4 → [2,2,2] → 4+4+4=12
        (4,  [4, 3, 3], 12),
        # 손 추적: [2,1,2], n=1 → 4 감소 → [1,1,2] → 1+1+4=6
        (1,  [2, 1, 2], 6),
        # 남은 작업 없음
        (3,  [1, 1],    0),
        # 추가 케이스:
        # works=[10,1,1], n=3 → 10을 3번 감소 → [7,1,1] → 49+1+1=51
        (3,  [10, 1, 1], 51),
    ]

    print("--- Mine_one (정확성 실패 케이스 포함) ---")
    for idx, (n, works, expected) in enumerate(test_cases, 1):
        output = solution_mine_one(n, works[:])
        status = "PASS" if output == expected else "FAIL"
        print(f"  TC{idx}: {status} (결과={output}, 기댓값={expected})")

    solutions = [
        ("Mine_two   (heap)     ", solution_mine_two),
        ("Mine_three (sort)     ", solution_mine_three),
        ("Ref        (counting) ", solution_ref),
        ("Best       (counting) ", solution_best),
        ("Sub        (heap)     ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _w, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _w[:])

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (n, works, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, works[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
