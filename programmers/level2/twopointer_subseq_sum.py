"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 연속된 부분 수열의 합
    유형       : Two Pointer / Prefix Sum
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/178870
    풀이일자   : 2026-09-25
===================================================================================
[문제 요약]
    비내림차순 수열에서 합이 k인 연속 부분 수열 중
    가장 짧은 수열의 [시작, 끝] 인덱스 반환
    같은 길이면 앞쪽 수열 우선

    제약 조건
        - sequence 길이: 5 이상 1,000,000 이하
        - 원소: 1~1,000 (양수만, 비내림차순)
        - k: 5~1,000,000,000
===================================================================================
[입출력 예시]
    sequence              | k | result
    ----------------------|---|-------
    [1, 2, 3, 4, 5]       | 7 | [2, 3]
    [1, 1, 1, 2, 3, 4, 5] | 5 | [6, 6]
    [2, 2, 2, 2, 2]       | 6 | [0, 2]
===================================================================================
[풀이 접근법 비교]
    투포인터:
        left, right로 [left, right] 구간 합 추적
        sum < k: right 확장, sum > k: left 축소, sum == k: 기록 후 이동
        원소가 양수라 단조성 보장 → O(N)

    해시 누적합 (ref_one):
        P[i] = sequence[0..i-1]의 합
        P[j] - P[i] = k → P[i] = P[j] - k
        curr_sum - k가 prefix_map에 있으면 구간 [i, j] 발견
        O(N) + dict 해시 상수

    bisect 누적합 (ref_two):
        P[left] + k = P[right+1]을 bisect_left로 탐색
        O(N log N)

[정방향 vs 역방향 투포인터]
    정방향 (two):
        앞에서 먼저 발견한 수열이 우선 → 같은 길이 curr_len < min_len만 갱신
        포인터 관리 단순, 코드 간결

    역방향 (one):
        뒤에서 앞으로 이동 → 같은 길이도 앞쪽 수열로 갱신 필요 (<=)
        right < left 역전 상황 처리 필요 → 코드 복잡
        오름차순 조건의 이점 없음 (내림차순 수열이라면 의미 있었을 것)

[prefix_map[curr_sum] 덮어쓰지 않는 이유]
    같은 누적합이 두 번 나오면 두 위치 사이 구간합이 0
    원소가 양수만이라 0 구간이 존재 불가
    → 실제로 같은 누적합이 중복 등장하지 않음
    → 더 앞쪽 위치를 유지하는 것이 더 짧은 구간 발견에 유리

[실측 결과 — N=1,000,000, 100회]
    two   (정방향투포인터): 194.5ms  ← 가장 빠름
    one   (역방향투포인터): 205.6ms
    ref_one (해시누적합):   357.6ms
    ref_two (bisect누적합): 403.1ms
===================================================================================
[내 초기 풀이]
    solution_mine_one: 역방향 투포인터
    solution_mine_two: 정방향 투포인터

[개선 포인트]
    solution_mine_one: 역방향 포인터 관리 복잡 - 참고용
    solution_mine_two: 개선 필요 없음 - Best
                       가장 빠르고 코드 간결
    solution_ref_one:  해시 누적합 - Sub
                       P[j]-P[i]=k 발상이 명시적
    solution_ref_two:  bisect O(N log N) → 가장 느림
===================================================================================
[복잡도 분석]
    N = len(sequence) (최대 1,000,000)

    Mine_one  - 시간: O(N) | 공간: O(1) - 역방향 투포인터
    Mine_two  - 시간: O(N) | 공간: O(1) - 정방향 투포인터
    Ref_one   - 시간: O(N) | 공간: O(N) - 해시맵
    Ref_two   - 시간: O(N log N) | 공간: O(N) - 누적합 + bisect
    Best      - 시간: O(N) | 공간: O(1) - Mine_two와 동일
    Sub       - 시간: O(N) | 공간: O(N) - Ref_one과 동일
"""

import bisect
import time


# =================================================================================
# Mine solution one - 역방향 투포인터
# =================================================================================
def solution_mine_one(sequence: list[int], k: int) -> list[int]:
    """
    오른쪽에서 왼쪽으로 탐색하는 역방향 투포인터 풀이

    역방향 선택 이유:
        오름차순이라 뒤에서 탐색하면 큰 값부터 → 짧은 수열 빠른 발견 기대
        하지만 같은 길이 수열의 앞쪽 우선 조건 때문에 전체 순회 필요

    <= 조건:
        역방향이라 동일 길이의 앞쪽 수열이 나중에 발견됨
        → 같은 길이도 갱신해야 앞쪽 수열 유지

    right < left 역전 처리:
        포인터 관리 복잡도 발생 → 정방향보다 코드 까다로움
    """
    answer = []
    left = right = len(sequence) - 1
    curr_sum = sequence[right]
    min_len = float('inf')

    while left >= 0:
        if curr_sum == k:
            curr_len = right - left + 1
            if curr_len <= min_len:
                min_len = curr_len
                answer = [left, right]
            curr_sum -= sequence[right]
            right -= 1
        elif curr_sum < k:
            left -= 1
            if left >= 0:
                curr_sum += sequence[left]
        elif curr_sum > k:
            curr_sum -= sequence[right]
            right -= 1
            if right < left:
                left = right
                if left >= 0:
                    curr_sum = sequence[left]

    return answer


# =================================================================================
# Mine solution two - 정방향 투포인터
# =================================================================================
def solution_mine_two(sequence: list[int], k: int) -> list[int]:
    """
    왼쪽에서 오른쪽으로 탐색하는 정방향 투포인터 풀이

    sum < k: right 확장 (더 큰 값 포함)
    sum > k: left 축소 (더 작은 값 제외)
    sum == k: 기록 후 left 축소 (더 짧은 수열 탐색)

    < 조건:
        정방향이라 앞쪽 수열이 먼저 발견됨
        → 동일 길이는 갱신하지 않아도 앞쪽 수열 유지

    실측 가장 빠른 이유:
        O(N) 단순 순회, 포인터 조작만
    """
    answer = []
    left = right = 0
    n = len(sequence)
    curr_sum = sequence[0]
    min_len = float('inf')

    while right < n:
        if curr_sum == k:
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                answer = [left, right]
            curr_sum -= sequence[left]
            left += 1
        elif curr_sum < k:
            right += 1
            if right < n:
                curr_sum += sequence[right]
        elif curr_sum > k:
            curr_sum -= sequence[left]
            left += 1

    return answer


# =================================================================================
# Ref solution one - 해시맵 누적합
# =================================================================================
def solution_ref_one(sequence: list[int], k: int) -> list[int]:
    """
    누적합과 해시맵으로 구간합 = k인 구간을 찾는 참고 풀이

    핵심 수식:
        P[j] - P[i] = k → target = curr_sum - k = P[i]
        prefix_map에서 target 탐색 → O(1)

    prefix_map[curr_sum] 덮어쓰지 않는 이유:
        원소가 양수만 → 같은 누적합 중복 없음
        더 앞쪽 위치 유지가 더 짧은 구간 발견에 유리

    dict 해시 탐색 상수로 투포인터보다 약 1.8배 느림
    """
    answer = []
    prefix_map = {0: -1}
    curr_sum = 0
    min_len = float('inf')

    for i, num in enumerate(sequence):
        curr_sum += num
        target = curr_sum - k
        if target in prefix_map:
            left = prefix_map[target] + 1
            right = i
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                answer = [left, right]
        if curr_sum not in prefix_map:
            prefix_map[curr_sum] = i

    return answer


# =================================================================================
# Ref solution two - bisect 누적합
# =================================================================================
def solution_ref_two(sequence: list[int], k: int) -> list[int]:
    """
    누적합 배열 P에서 bisect로 P[left]+k를 탐색하는 참고 풀이

    P[right+1] - P[left] = k → P[right+1] = P[left] + k
    bisect_left로 target 탐색 → O(log N)
    P[idx] == target 검사로 정확성 보장

    O(N log N): 투포인터 O(N) 대비 느림
    """
    answer = []
    n = len(sequence)
    P = [0] * (n + 1)
    for i in range(n):
        P[i + 1] = P[i] + sequence[i]

    min_len = float('inf')

    for left in range(n):
        target = P[left] + k
        idx = bisect.bisect_left(P, target)
        if idx <= n and P[idx] == target:
            right = idx - 1
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                answer = [left, right]

    return answer


# =================================================================================
# Best solution - 정방향 투포인터 (mine_two 주석 보강)
# =================================================================================
def solution_best(sequence: list[int], k: int) -> list[int]:
    """
    정방향 투포인터로 O(N) 시간, O(1) 공간에 최단 구간을 찾는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        O(N) + O(1) 공간 → 누적합 O(N) 공간 대비 유리
        실측 N=1,000,000: 194ms (해시누적합 357ms 대비 1.8배 우위)
        < 조건으로 앞쪽 수열 자동 우선
    """
    answer = []
    left = right = 0
    n = len(sequence)
    curr_sum = sequence[0]
    min_len = float('inf')

    while right < n:
        if curr_sum == k:
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                answer = [left, right]
            curr_sum -= sequence[left]
            left += 1
        elif curr_sum < k:
            right += 1
            if right < n:
                curr_sum += sequence[right]
        elif curr_sum > k:
            curr_sum -= sequence[left]
            left += 1

    return answer


# =================================================================================
# Sub solution - 해시맵 누적합 (ref_one 주석 보강)
# =================================================================================
def solution_sub(sequence: list[int], k: int) -> list[int]:
    """
    해시맵 누적합으로 구간합 k인 구간을 찾는 서브 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        P[j] - P[i] = k 수식이 코드에 직접 드러남
        curr_sum - k = target → prefix_map 탐색
        투포인터 대비 수학적 관계 표현이 명시적
        dict 해시 상수로 Best 대비 1.8배 느림
    """
    answer = []
    prefix_map = {0: -1}
    curr_sum = 0
    min_len = float('inf')

    for i, num in enumerate(sequence):
        curr_sum += num
        target = curr_sum - k
        if target in prefix_map:
            left = prefix_map[target] + 1
            right = i
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                answer = [left, right]
        if curr_sum not in prefix_map:
            prefix_map[curr_sum] = i

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (sequence, k, 기댓값)
        # 공식 예시
        ([1, 2, 3, 4, 5],       7, [2, 3]),
        ([1, 1, 1, 2, 3, 4, 5], 5, [6, 6]),
        ([2, 2, 2, 2, 2],       6, [0, 2]),
        # 추가 케이스:
        # 단일 원소가 정답
        # 손 추적: k=5, [1,1,1,2,3,4,5]에서 5 자체가 존재 → 길이 1
        ([1, 1, 1, 2, 3, 5],    5, [5, 5]),
        # 단일 원소가 최단: [1,2](길이2), [3](길이1) → [2,2]
        ([1, 2, 3, 4],          3, [2, 2]),
    ]

    solutions = [
        ("Mine_one  (역방향투포인터)", solution_mine_one),
        ("Mine_two  (정방향투포인터)", solution_mine_two),
        ("Ref_one   (해시누적합)    ", solution_ref_one),
        ("Ref_two   (bisect누적합)  ", solution_ref_two),
        ("Best      (정방향투포인터)", solution_best),
        ("Sub       (해시누적합)    ", solution_sub),
    ]

    # 워밍업
    _s, _k, _ = test_cases[0]
    for _, func in solutions:
        func(_s[:], _k)

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (sequence, k, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(sequence[:], k)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
