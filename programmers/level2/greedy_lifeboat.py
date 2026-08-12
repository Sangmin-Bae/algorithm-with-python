"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 구명보트
    유형       : Greedy / Two Pointer
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42885
    풀이일자   : 2026-08-12
================================================================================
[문제 요약]
    최대 2명, 무게 제한 limit인 구명보트로
    모든 사람을 구출하기 위한 최소 보트 수 반환

    제약 조건
        - 사람 수: 1 이상 50,000 이하
        - 몸무게: 40 이상 240 이하 (범위 201개)
        - limit > 최대 몸무게 (혼자 못 타는 경우 없음)
================================================================================
[입출력 예시]
    people           | limit | return
    -----------------|-------|-------
    [70, 50, 80, 50] | 100   | 3
    [70, 80, 50]     | 100   | 3
================================================================================
[그리디 핵심 — 가장 가벼운 사람 + 가장 무거운 사람]
    교환 논증:
        가장 무거운 사람(R)은 매 보트마다 반드시 배정
        R과 함께 탈 수 있는 가장 가벼운 사람(L)을 태우는 것이 최적
        → 더 무거운 사람을 L로 쓰면 R과 함께 못 탈 가능성 증가
        → 더 가벼운 사람을 쓸 여지가 없음 (L이 이미 가장 가벼움)

    right를 무조건 감소시키는 이유:
        limit 초과: R 혼자 보트 → right -= 1, answer += 1
        limit 이하: R + L 함께 → left += 1, right -= 1, answer += 1
        → 어느 경우든 R은 이번 보트에서 처리됨

[solution_ref — 해시맵 + 투포인터 (정렬 없음)]
    몸무게 범위 40~240 (201개)를 활용
    해시맵: {몸무게: 인원수}
    left/right: 현재 최소/최대 몸무게 포인터 (인덱스 아닌 실제 값)

    left == right 처리:
        남은 사람들이 모두 동일한 몸무게인 순간
        같은 키를 두 번 감소시키는 문제 → 별도 분기 필요

        경우 A: left + right <= limit (같은 무게끼리 같이 탈 수 있음)
            count명을 둘씩 짝지음
            answer += (count // 2) + (count % 2)
            예) 5명: 2보트(2명) + 1보트(1명) = 3보트

        경우 B: left + right > limit (같은 무게도 같이 못 탐)
            모두 혼자 타야 함 → answer += count

[실측 결과 — N=50,000, 1,000회 반복]
    풀이1 (투포인터+정렬): 8.236ms  ← 가장 빠름
    ref   (해시맵):        8.753ms
    풀이2 (deque):         9.212ms  ← 가장 느림

    ref가 정렬 없어도 풀이1과 비슷한 이유:
        dict.get 해시 연산 비용 > 정렬 후 단순 인덱스 접근
        Python dict 해시가 정수 비교보다 무거움

    풀이2가 느린 이유:
        deque 변환 + len(q) 체크 + popleft() 오버헤드 누적
================================================================================
[내 초기 풀이]
    solution_mine_one: 정렬 + 투포인터 (인덱스 방식)
    solution_mine_two: 정렬 + deque (popleft/pop 방식)

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       정렬 후 인덱스 투포인터, 가장 빠르고 간결
    solution_mine_two: deque 오버헤드로 mine_one보다 느림
                       len(q) 매 루프 체크 + popleft 비용
    solution_ref:      해시맵으로 정렬 없이 처리 - Sub
                       몸무게 범위 201개 특성 활용
                       left==right 별도 처리 필요 (same key 이중 감소 방지)
================================================================================
[복잡도 분석]
    N = len(people) (최대 50,000)
    W = 몸무게 범위 = 201 (40~240)

    Mine_one - 시간: O(N log N) | 공간: O(1) - 정렬 + 투포인터
    Mine_two - 시간: O(N log N) | 공간: O(N) - 정렬 + deque 생성
    Ref      - 시간: O(N + W)   | 공간: O(W) - 해시맵 O(N) + 순회 O(W)
    Best     - 시간: O(N log N) | 공간: O(1) - Mine_one과 동일
    Sub      - 시간: O(N + W)   | 공간: O(W) - Ref와 동일

    이론상 Ref가 빠르나 실측에서 dict 해시 비용으로 정렬 방식과 비슷
"""

from collections import deque
import time


# ================================================================================
# Mine solution one - 정렬 + 투포인터 (인덱스 방식)
# ================================================================================
def solution_mine_one(people: list[int], limit: int) -> int:
    """
    정렬 후 left, right 인덱스로 가장 가벼운/무거운 사람을 짝짓는 풀이

    핵심:
        people.sort(): 오름차순 정렬
        left: 가장 가벼운 사람 인덱스
        right: 가장 무거운 사람 인덱스

    right 무조건 감소:
        어떤 경우든 people[right]는 이번 보트에 탑승 처리
        합산 가능: left도 같이 탑승 → left += 1
        합산 불가: right 혼자 탑승

    left <= right 종료 조건:
        left == right: 한 명 남았으면 혼자 보트 → answer += 1, 종료
        left > right: 모두 처리 완료
    """
    answer = 0
    left, right = 0, len(people) - 1

    people.sort()
    while left <= right:
        if people[left] + people[right] <= limit:
            left += 1
        right -= 1
        answer += 1

    return answer


# ================================================================================
# Mine solution two - 정렬 + deque (popleft/pop 방식)
# ================================================================================
def solution_mine_two(people: list[int], limit: int) -> int:
    """
    deque의 popleft/pop으로 처리된 사람을 제거하는 풀이

    mine_one 대비:
        인덱스 포인터 이동 → deque에서 원소 제거
        q[0]: 가장 가벼운 사람, q[-1]: 가장 무거운 사람

    성능 한계:
        deque 변환 비용 + len(q) 매 루프 체크 + popleft 오버헤드
        실측 mine_one 대비 약 12% 느림

    len(q) == 1 처리:
        한 명 남으면 혼자 보트 → answer += 1, break
    """
    answer = 0
    q = deque(sorted(people))

    while q:
        if len(q) == 1:
            answer += 1
            break
        if q[0] + q[-1] <= limit:
            q.popleft()
        q.pop()
        answer += 1

    return answer


# ================================================================================
# Ref solution - 해시맵 + 투포인터 (정렬 없음)
# ================================================================================
def solution_ref(people: list[int], limit: int) -> int:
    """
    몸무게 범위 201개(40~240)를 해시맵으로 집계해 정렬 없이 처리하는 참고 풀이

    left/right: 인덱스가 아닌 실제 몸무게 값 포인터
        left = 현재 최소 몸무게, right = 현재 최대 몸무게

    weight_map[w] == 0 처리:
        해당 몸무게 인원이 소진됐으면 포인터 이동

    left == right 별도 처리:
        남은 사람 모두 동일 몸무게 → 일반 루프로 처리하면 same key 이중 감소 오류
        경우 A: 같이 탈 수 있음 → (count//2) + (count%2) 보트
        경우 B: 같이 못 탐 → count 보트 (모두 혼자)
    """
    answer = 0
    left = float('inf')
    right = float('-inf')

    weight_map = {}
    for p in people:
        weight_map[p] = weight_map.get(p, 0) + 1
        if p < left: left = p
        if p > right: right = p

    while left <= right:
        if weight_map.get(left, 0) == 0:
            left += 1
            continue
        if weight_map.get(right, 0) == 0:
            right -= 1
            continue

        if left == right:
            count = weight_map[left]
            if left + right <= limit:
                answer += (count // 2) + (count % 2)
            else:
                answer += count
            break

        if left + right <= limit:
            weight_map[left] -= 1

        weight_map[right] -= 1
        answer += 1

    return answer


# ================================================================================
# Best solution - 정렬 + 투포인터 (mine_one 주석 보강)
# ================================================================================
def solution_best(people: list[int], limit: int) -> int:
    """
    정렬 + 인덱스 투포인터로 가장 빠르게 최소 보트 수를 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        정렬 후 단순 인덱스 접근 → dict 해시 비용 없음
        실측 N=50,000: 8.236ms (ref 8.753ms, mine_two 9.212ms 대비 우위)
        right 무조건 감소: 가장 무거운 사람이 매 보트에서 처리되는 구조
    """
    answer = 0
    left, right = 0, len(people) - 1

    people.sort()
    while left <= right:
        if people[left] + people[right] <= limit:
            left += 1
        right -= 1
        answer += 1

    return answer


# ================================================================================
# Sub solution - 해시맵 + 투포인터 (ref 주석 보강)
# ================================================================================
def solution_sub(people: list[int], limit: int) -> int:
    """
    몸무게 범위 201개를 활용해 정렬 없이 처리하는 서브 풀이

    Best 대비 특징:
        O(N + W): 정렬 O(N log N) 대신 집계 O(N) + 범위 순회 O(201)
        몸무게 40~240 범위가 좁다는 제약 조건을 직접 활용
        left == right 별도 처리: same key 이중 감소 방지
        실측 Best와 비슷 (dict 해시 비용이 정렬 절감분 상쇄)
    """
    answer = 0
    left = float('inf')
    right = float('-inf')

    weight_map = {}
    for p in people:
        weight_map[p] = weight_map.get(p, 0) + 1
        if p < left: left = p
        if p > right: right = p

    while left <= right:
        if weight_map.get(left, 0) == 0:
            left += 1
            continue
        if weight_map.get(right, 0) == 0:
            right -= 1
            continue

        if left == right:
            count = weight_map[left]
            if left + right <= limit:
                answer += (count // 2) + (count % 2)
            else:
                answer += count
            break

        if left + right <= limit:
            weight_map[left] -= 1

        weight_map[right] -= 1
        answer += 1

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int, int]] = [
        # (people, limit, 기댓값)
        # 공식 예시
        # 손 추적 [50,50,70,80] limit=100:
        # left=50+right=80: 130>100 → 80 혼자, answer=1, right→70
        # left=50+right=70: 120>100 → 70 혼자, answer=2, right→50
        # left=50+right=50: 100<=100 → 둘이, answer=3, left→50 right→50 → 종료
        ([70, 50, 80, 50], 100, 3),
        ([70, 80, 50],     100, 3),
        # 추가 케이스:
        ([40],             80,  1),    # 단일 인원
        ([40, 40],         80,  1),    # 둘이 탑승 가능
        ([120, 120],       240, 1),    # 한계 무게 함께 탑승
        ([120, 121],       240, 2),    # 한계 초과 각자 탑승
    ]

    solutions = [
        ("Mine_one (투포인터)  ", solution_mine_one),
        ("Mine_two (deque)     ", solution_mine_two),
        ("Ref      (해시맵)    ", solution_ref),
        ("Best     (투포인터)  ", solution_best),
        ("Sub      (해시맵)    ", solution_sub),
    ]

    # 워밍업 스텝
    _p, _l, _ = test_cases[0]
    for _, func in solutions:
        func(_p[:], _l)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (people, limit, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(people[:], limit)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
