"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 이중우선순위큐
    유형       : Heap
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42628
    풀이일자   : 2026-09-09
===================================================================================
[문제 요약]
    operations 배열의 명령을 처리 후 큐의 [최댓값, 최솟값] 반환
    I value: value 삽입
    D 1:     최댓값 삭제
    D -1:    최솟값 삭제
    빈 큐 삭제 명령은 무시, 큐가 비면 [0, 0]

    제약 조건
        - operations 길이: 1 이상 1,000,000 이하
===================================================================================
[입출력 예시]
    operations                                           | return
    -----------------------------------------------------|-------
    ["I 16","I -5643","D -1","D 1","D 1","I 123","D -1"]| [0, 0]
    ["I -45","I 653","D 1","I -642","I 45","I 97",
     "D 1","D -1","I 333"]                              | [333, -45]
===================================================================================
[핵심 — 이중 힙 + lazy deletion]
    최솟값 O(log N): 최소힙
    최댓값 O(log N): 최대힙 (음수 변환)

    문제: 한쪽 힙에서 삭제한 원소가 다른 힙에 남아있음
    해결: lazy deletion (지연 삭제)
        삭제 시 visited[idx] = False로 무효화
        꺼낼 때 visited 체크로 무효 원소 skip

    (num, i) 튜플 저장 이유:
        동일한 값 여러 번 삽입 가능 → 삽입 순서 i로 구분
        visited[i]로 개별 원소를 독립적으로 관리

[lazy deletion이 필요한 이유]
    최솟값 삭제 후 최대힙에 해당 원소가 중간에 있을 수 있음
    → 즉시 찾아서 삭제: O(N) 순회 필요
    → lazy: 맨 앞에 올 때 제거 → O(log N) 유지

[ref_one — nlargest + heapify 한계]
    heapq.nlargest(1, heap): O(N) 전체 순회
    heap.remove(max_num):    O(N) 선형 탐색
    heapq.heapify(heap):     O(N) 재구성
    → 최대값 삭제 1회당 O(N)
    → operations N번이면 O(N²) → 대규모 TLE

[ref_two — bisect 방식]
    bisect.insort(arr, num): 삽입 위치 O(log N) 탐색 + 삽입 O(N)
    arr.pop():               O(1) 뒤에서 삭제 (최댓값)
    arr.pop(0):              O(N) 앞에서 삭제 (최솟값)

    deque로 pop(0)를 O(1)로 개선 불가한 이유:
        bisect 모듈은 리스트를 가정
        deque 인덱스 접근이 O(N) → 이진탐색이 O(N²)로 악화
        삽입(O(N))과 앞 삭제(O(N)) 동시 최적화 불가

    소규모에서 mine보다 빠른 이유:
        bisect.insort가 C 레벨 구현 → 상수가 매우 작음
        튜플 생성/visited 배열 관리 없음

[실측 결과 — N=10,000, 500회]
    ref_two (bisect):      3.57ms  ← 소규모 빠름
    mine    (이중힙+lazy): 5.44ms
    ref_one (nlargest):   O(N²) 측정 생략

    N=1,000,000에서 역전 예상:
        bisect O(N²) 최악 vs mine O(N log N)
===================================================================================
[내 초기 풀이]
    solution_mine: 이중힙 + lazy deletion + visited 배열

[개선 포인트]
    solution_mine:    개선 필요 없음 - Best
                      O(N log N) 이론적으로 가장 올바름
    solution_ref_one: O(N²) → 대규모 TLE
    solution_ref_two: 소규모 빠름, 대규모 O(N²) 위험 - Sub
===================================================================================
[복잡도 분석]
    N = len(operations) (최대 1,000,000)

    Mine     - 시간: O(N log N) | 공간: O(N) - 이중힙 + visited
    Ref_one  - 시간: O(N²)      | 공간: O(N) - nlargest + heapify
    Ref_two  - 시간: O(N²) 최악 | 공간: O(N) - bisect + pop(0)
    Best     - 시간: O(N log N) | 공간: O(N) - Mine과 동일
    Sub      - 시간: O(N²) 최악 | 공간: O(N) - Ref_two와 동일
"""

import heapq
import bisect
import time


# =================================================================================
# Mine solution - 이중힙 + lazy deletion
# =================================================================================
def solution_mine(operations: list[str]) -> list[int]:
    """
    최소힙과 최대힙을 동시에 운영하고 visited로 동기화하는 lazy deletion 풀이

    (num, i) 튜플 저장:
        i: 삽입 순서 ID → 동일값 여러 개를 구분
        visited[i]: True=유효, False=이미 삭제됨

    삭제 시 lazy:
        visited[idx] = False로 무효화
        반대 힙에서는 꺼낼 때 visited 체크로 skip

    종료 후 정리:
        마지막 명령 이후 반대 힙에 무효 원소가 맨 앞에 있을 수 있음
        → 최종 반환 전 while로 제거
    """
    N = len(operations)
    visited = [False] * N
    max_heap = []
    min_heap = []

    for i in range(N):
        command, num = operations[i].split()
        num = int(num)

        if command == "I":
            heapq.heappush(min_heap, (num, i))
            heapq.heappush(max_heap, (-num, i))
            visited[i] = True

        elif command == "D":
            if num == 1:
                while max_heap and not visited[max_heap[0][1]]:
                    heapq.heappop(max_heap)
                if max_heap:
                    _, idx = heapq.heappop(max_heap)
                    visited[idx] = False
            elif num == -1:
                while min_heap and not visited[min_heap[0][1]]:
                    heapq.heappop(min_heap)
                if min_heap:
                    _, idx = heapq.heappop(min_heap)
                    visited[idx] = False

    while max_heap and not visited[max_heap[0][1]]:
        heapq.heappop(max_heap)
    while min_heap and not visited[min_heap[0][1]]:
        heapq.heappop(min_heap)

    if not min_heap or not max_heap:
        return [0, 0]
    return [-max_heap[0][0], min_heap[0][0]]


# =================================================================================
# Ref solution one - 단일 힙 + nlargest + heapify (O(N²))
# =================================================================================
def solution_ref_one(operations: list[str]) -> list[int]:
    """
    단일 최소힙으로 운영하고 nlargest로 최대값을 찾는 참고 풀이 (O(N²))

    heapq.nlargest(k, iterable):
        전체 순회 후 최대값 k개 반환 O(N log k)
        k=1이면 O(N) → max()와 동일 비용

    최대값 삭제 시:
        nlargest(1): O(N)
        remove():    O(N) 선형 탐색
        heapify():   O(N) 재구성
        → 1회당 O(N), N번이면 O(N²)

    대규모 입력에서 TLE 위험
    """
    heap = []

    for op in operations:
        command, num = op.split()
        num = int(num)

        if command == "I":
            heapq.heappush(heap, num)
        elif command == "D":
            if num == 1 and heap:
                max_num = heapq.nlargest(1, heap)[0]
                heap.remove(max_num)
                heapq.heapify(heap)
            elif num == -1 and heap:
                heapq.heappop(heap)

    if not heap:
        return [0, 0]
    return [heapq.nlargest(1, heap)[0], heap[0]]


# =================================================================================
# Ref solution two - bisect 정렬 삽입 + pop
# =================================================================================
def solution_ref_two(operations: list[str]) -> list[int]:
    """
    bisect.insort로 정렬 상태를 유지하며 양 끝 삭제로 처리하는 참고 풀이

    bisect.insort(arr, num):
        이진탐색 O(log N)으로 삽입 위치 탐색
        C 레벨 구현 → 상수가 작음
        하지만 중간 삽입 시 원소 이동 O(N)

    pop():    O(1) 뒤에서 삭제 (최댓값)
    pop(0):   O(N) 앞에서 삭제 (최솟값)

    deque로 pop(0) 개선 불가:
        bisect가 리스트를 가정
        deque 인덱스 접근 O(N) → 이진탐색 O(N²)로 악화

    소규모(N≤10,000)에서 mine보다 빠르나
    대규모(N=1,000,000)에서 O(N²) 위험
    """
    arr = []

    for op in operations:
        command, num = op.split()
        num = int(num)

        if command == "I":
            bisect.insort(arr, num)
        elif command == "D" and arr:
            if num == 1:
                arr.pop()
            elif num == -1:
                arr.pop(0)

    if not arr:
        return [0, 0]
    return [arr[-1], arr[0]]


# =================================================================================
# Best solution - 이중힙 + lazy deletion (mine 주석 보강)
# =================================================================================
def solution_best(operations: list[str]) -> list[int]:
    """
    이중힙 + lazy deletion으로 O(N log N) 시간을 보장하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        O(N log N): ref_one O(N²), ref_two O(N²) 최악 대비 이론적으로 가장 올바름
        lazy deletion: 삭제를 즉시 반영하지 않고 꺼낼 때 확인
        대규모(N=1,000,000) 입력에서 유일하게 안전한 방식
    """
    N = len(operations)
    visited = [False] * N
    max_heap = []
    min_heap = []

    for i in range(N):
        command, num = operations[i].split()
        num = int(num)

        if command == "I":
            heapq.heappush(min_heap, (num, i))
            heapq.heappush(max_heap, (-num, i))
            visited[i] = True

        elif command == "D":
            if num == 1:
                while max_heap and not visited[max_heap[0][1]]:
                    heapq.heappop(max_heap)
                if max_heap:
                    _, idx = heapq.heappop(max_heap)
                    visited[idx] = False
            elif num == -1:
                while min_heap and not visited[min_heap[0][1]]:
                    heapq.heappop(min_heap)
                if min_heap:
                    _, idx = heapq.heappop(min_heap)
                    visited[idx] = False

    while max_heap and not visited[max_heap[0][1]]:
        heapq.heappop(max_heap)
    while min_heap and not visited[min_heap[0][1]]:
        heapq.heappop(min_heap)

    if not min_heap or not max_heap:
        return [0, 0]
    return [-max_heap[0][0], min_heap[0][0]]


# =================================================================================
# Sub solution - bisect 정렬 삽입 (ref_two 주석 보강)
# =================================================================================
def solution_sub(operations: list[str]) -> list[int]:
    """
    bisect로 정렬 상태를 유지하며 코드를 단순화한 서브 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        visited/튜플 없이 코드 간결
        C 레벨 bisect.insort → 소규모(N≤10,000)에서 Best보다 빠름
        pop(0) O(N)이 병목 → 대규모에서 O(N²) 위험
        deque 전환 불가: bisect가 리스트의 연속 메모리를 가정
    """
    arr = []

    for op in operations:
        command, num = op.split()
        num = int(num)

        if command == "I":
            bisect.insort(arr, num)
        elif command == "D" and arr:
            if num == 1:
                arr.pop()
            elif num == -1:
                arr.pop(0)

    if not arr:
        return [0, 0]
    return [arr[-1], arr[0]]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (operations, 기댓값)
        # 공식 예시
        (["I 16","I -5643","D -1","D 1","D 1","I 123","D -1"], [0, 0]),
        (["I -45","I 653","D 1","I -642","I 45","I 97","D 1","D -1","I 333"], [333, -45]),
        # 추가 케이스:
        # 빈 큐 삭제 무시
        (["D 1"],                                                [0, 0]),
        # 단일 원소 삽입
        (["I 5"],                                                [5, 5]),
        # 동일값 여러 개
        (["I 3","I 3","D 1"],                                   [3, 3]),
    ]

    solutions = [
        ("Mine    (이중힙+lazy) ", solution_mine),
        ("Ref_one (nlargest)    ", solution_ref_one),
        ("Ref_two (bisect)      ", solution_ref_two),
        ("Best    (이중힙+lazy) ", solution_best),
        ("Sub     (bisect)      ", solution_sub),
    ]

    # 워밍업 스텝
    _ops, _ = test_cases[0]
    for _, func in solutions:
        func(_ops[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (operations, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(operations[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
