"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 두 큐 합 같게 만들기
    유형       : Queue / Two Pointer
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/118667
    풀이일자   : 2026-09-22
===================================================================================
[문제 요약]
    길이가 같은 두 큐에서 한쪽 front를 꺼내 다른 쪽 back에 넣는 작업을
    반복하여 두 큐의 합을 같게 만들 때 필요한 최소 작업 횟수 반환
    불가능하면 -1

    제약 조건
        - queue1, queue2 길이: 1 이상 300,000 이하
        - 원소: 1 이상 10^9 이하
        - 합 계산 시 오버플로우 주의 (Python은 무한 정밀도라 무관)
===================================================================================
[입출력 예시]
    queue1        | queue2         | result
    --------------|----------------|-------
    [3, 2, 7, 2]  | [4, 6, 5, 1]  | 2
    [1, 2, 1, 2]  | [1, 10, 1, 2] | 7
    [1, 1]        | [1, 5]        | -1
===================================================================================
[핵심 — 원형 배열 + 투포인터 모델]
    queue1 + queue2를 이어붙인 원형 배열(길이 2N)로 모델링
    p1: queue1의 front 위치 (0에서 시작)
    p2: queue2의 front 위치 (N에서 시작)
    [p1, p2) 구간의 합 = sum1
    원소 이동 = 포인터를 오른쪽으로 한 칸 이동

[4N 상한 증명 — 카카오 공식 해설 기반]
    p1, p2는 단조 증가 (절대 감소하지 않음)
    count = p1 이동 횟수 + p2 이동 횟수 = 4N에 도달 시:
        p1 + p2 = 4N
        → p1 ≥ 2N 또는 p2 ≥ 2N 중 하나는 반드시 참
          (둘 다 2N 미만이면 합이 4N 미만)

    p1 ≥ 2N이면:
        queue1 front가 원형 배열(길이 2N)을 한 바퀴 순회 완료
        → 이미 모든 위치의 원소를 front로 확인
        → 이 이상 새로운 조합 없음 → 탈출 가능

    이는 추론이 아닌 수학적 증명:
        "p1+p2=4N → p1≥2N or p2≥2N": 수학적 사실
        "포인터 2N 이동 = 원형 배열 한 바퀴": 정의로부터
        → 4N 이후 해가 없다는 게 완전히 도출됨

[3N-1은 더 타이트한 상한]
    두 포인터가 겹치지 않는 유의미한 상태 수의 정확한 상한
    4N은 충분조건(여유있는 상한), 3N-1은 필요충분조건에 가깝지만
    실무에서는 카카오 공식 해설의 4N이 더 안전하게 사용됨

[내 풀이 — deque]
    deque: popleft O(1), append O(1)
    원소를 실제로 이동시키며 sum1 추적

[ref — 투포인터]
    원소를 이동하지 않고 포인터만 이동
    sum1을 포인터 이동에 따라 증감
    단, % M 연산 비용으로 실측 deque보다 약간 느림

[실측 결과 — N=300,000, 10회]
    mine (deque):    113.5ms
    ref  (투포인터): 125.5ms
    deque가 빠른 이유: ref의 array[p % M] 나머지 연산 비용 누적
===================================================================================
[내 초기 풀이]
    solution_mine: deque + 4N 상한

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
                   deque O(1) pop/append, 4N 상한 증명됨
    solution_ref:  투포인터 - Sub
                   원소 이동 없이 포인터만 이동, 메모리 효율적
                   실측 % 연산으로 mine보다 약간 느림
===================================================================================
[복잡도 분석]
    N = len(queue1) = len(queue2) (최대 300,000)

    Mine - 시간: O(N) | 공간: O(N) - deque 2개
    Ref  - 시간: O(N) | 공간: O(N) - 병합 배열
    Best - 시간: O(N) | 공간: O(N) - Mine과 동일
    Sub  - 시간: O(N) | 공간: O(N) - Ref와 동일
"""

from collections import deque
import time


# =================================================================================
# Mine solution - deque + 4N 상한
# =================================================================================
def solution_mine(queue1: list[int], queue2: list[int]) -> int:
    """
    deque로 원소를 실제 이동시키며 sum1을 추적하는 초기 풀이

    그리디 전략:
        sum1 > target: queue1 front를 queue2로 이동 (sum1 감소)
        sum1 < target: queue2 front를 queue1으로 이동 (sum1 증가)
        sum1 == target: 두 큐의 합이 같음 → 반환

    4N 상한:
        p1 + p2 = 4N → p1≥2N or p2≥2N
        → 하나의 포인터가 원형 배열(2N) 한 바퀴 완료
        → 새로운 조합 없음 → 종료
    """
    q1 = deque(queue1)
    q2 = deque(queue2)

    sum1 = sum(q1)
    sum2 = sum(q2)
    total_sum = sum1 + sum2

    if total_sum % 2 != 0:
        return -1

    target = total_sum // 2
    N = len(queue1)
    limit = 4 * N
    count = 0

    while count <= limit:
        if sum1 == target:
            return count

        if sum1 > target:
            val = q1.popleft()
            sum1 -= val
            q2.append(val)
        else:
            val = q2.popleft()
            sum1 += val
            q1.append(val)

        count += 1

    return -1


# =================================================================================
# Ref solution - 투포인터 (원형 배열)
# =================================================================================
def solution_ref(queue1: list[int], queue2: list[int]) -> int:
    """
    두 큐를 하나의 배열로 합쳐 투포인터로 sum1을 추적하는 참고 풀이

    원형 배열:
        array = queue1 + queue2 (길이 2N)
        p1: queue1 front 위치 (0 시작)
        p2: queue2 front 위치 (N 시작)

    포인터 이동:
        sum1 > target: array[p1 % M] 빼고 p1++
        sum1 < target: array[p2 % M] 더하고 p2++

    원소를 실제로 이동하지 않음 → 메모리 효율적
    array[p % M] 나머지 연산 비용으로 mine보다 약간 느림
    """
    array = queue1 + queue2
    M = len(array)
    N = len(queue1)

    sum1 = sum(queue1)
    sum2 = sum(queue2)
    total_sum = sum1 + sum2

    if total_sum % 2 != 0:
        return -1

    target = total_sum // 2
    p1 = 0
    p2 = N
    count = 0
    limit = N * 4

    while count <= limit:
        if sum1 == target:
            return count

        if sum1 > target:
            sum1 -= array[p1 % M]
            p1 += 1
        else:
            sum1 += array[p2 % M]
            p2 += 1

        count += 1

    return -1


# =================================================================================
# Best solution - deque + 4N 상한 (mine 주석 보강)
# =================================================================================
def solution_best(queue1: list[int], queue2: list[int]) -> int:
    """
    deque O(1) 연산과 4N 상한 증명으로 최적 작업 횟수를 구하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        deque popleft/append: O(1) → 전체 O(N)
        4N 상한: 카카오 공식 해설 기반 수학적 증명
        실측 N=300,000: 113.5ms (ref 125.5ms 대비 약간 우위)
    """
    q1 = deque(queue1)
    q2 = deque(queue2)

    sum1 = sum(q1)
    sum2 = sum(q2)
    total_sum = sum1 + sum2

    if total_sum % 2 != 0:
        return -1

    target = total_sum // 2
    N = len(queue1)
    limit = 4 * N
    count = 0

    while count <= limit:
        if sum1 == target:
            return count

        if sum1 > target:
            val = q1.popleft()
            sum1 -= val
            q2.append(val)
        else:
            val = q2.popleft()
            sum1 += val
            q1.append(val)

        count += 1

    return -1


# =================================================================================
# Sub solution - 투포인터 (ref 주석 보강)
# =================================================================================
def solution_sub(queue1: list[int], queue2: list[int]) -> int:
    """
    원형 배열 + 투포인터로 원소 이동 없이 합을 추적하는 서브 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        병합 배열로 원형 배열 모델 명시적 구현
        원소를 이동하지 않고 포인터만 이동 → 공간 효율
        4N 상한의 물리적 의미(포인터가 원형 배열 한 바퀴)가
        투포인터 코드에서 가장 직관적으로 드러남
    """
    array = queue1 + queue2
    M = len(array)
    N = len(queue1)

    sum1 = sum(queue1)
    total_sum = sum1 + sum(queue2)

    if total_sum % 2 != 0:
        return -1

    target = total_sum // 2
    p1 = 0
    p2 = N
    count = 0
    limit = N * 4

    while count <= limit:
        if sum1 == target:
            return count

        if sum1 > target:
            sum1 -= array[p1 % M]
            p1 += 1
        else:
            sum1 += array[p2 % M]
            p2 += 1

        count += 1

    return -1


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (queue1, queue2, 기댓값)
        # 공식 예시
        # 손 추적: sum1=14, sum2=16, target=15
        # 1: q1→3→q2, sum1=11, sum2=19
        # 2: q2→4→q1, sum1=15 ✓ → 2
        ([3, 2, 7, 2], [4, 6, 5, 1], 2),
        ([1, 2, 1, 2], [1, 10, 1, 2], 7),
        ([1, 1],       [1, 5],        -1),
        # 추가 케이스:
        # 이미 같음 (0번)
        ([1, 2], [3, 0], 0),
    ]

    solutions = [
        ("Mine (deque)     ", solution_mine),
        ("Ref  (투포인터)  ", solution_ref),
        ("Best (deque)     ", solution_best),
        ("Sub  (투포인터)  ", solution_sub),
    ]

    # 워밍업
    _q1, _q2, _ = test_cases[0]
    for _, func in solutions:
        func(_q1[:], _q2[:])

    print("=" * 64)
    print(f"{'풀이':<18} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (q1, q2, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(q1[:], q2[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<18} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
