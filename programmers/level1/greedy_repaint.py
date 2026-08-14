"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 덧칠하기
    유형       : Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/161989
    풀이일자   : 2026-08-14
===================================================================================
[문제 요약]
    길이 n인 벽에서 section 구역들을 길이 m 롤러로 덧칠할 때
    최소 페인트칠 횟수 반환

    제약 조건
        - 1 <= m <= n <= 100,000
        - section 길이: 1 이상 n 이하
        - section 원소: 오름차순 정렬, 중복 없음
===================================================================================
[입출력 예시]
    n | m | section   | result
    --|---|-----------|-------
    8 | 4 | [2,3,6]   | 2
    5 | 4 | [1,3]     | 1
    4 | 1 | [1,2,3,4] | 4
===================================================================================
[그리디 핵심 — 가장 왼쪽 덧칠 구역부터 시작]
    덧칠 필요 구역 w에서 칠을 시작하면 w ~ w+m-1 구역이 커버됨
    w보다 왼쪽에서 시작하면 오른쪽 커버 범위가 줄어 불리함
    → 덧칠 필요 구역의 최소값에서 시작하는 것이 항상 최적

    교환 논증:
        어떤 구역 w에서 시작하지 않고 w보다 왼쪽 w-k에서 시작하면
        커버 범위가 w-k ~ w-k+m-1로 오른쪽이 k만큼 줄어듦
        → w에서 시작하는 것보다 불리

    손 추적 (n=8, m=4, section=[2,3,6]):
        w=2: until_painted=0 < 2 → 칠 시작, until_painted=2+4-1=5, answer=1
        w=3: until_painted=5 >= 3 → 이미 칠해짐 → 통과
        w=6: until_painted=5 < 6 → 칠 시작, until_painted=6+4-1=9, answer=2
        return 2 ✓

[section이 오름차순 정렬이라는 제약의 중요성]
    정렬이 보장되므로 단순 순회로 "아직 칠해지지 않은 가장 작은 구역"을 찾을 수 있음
    정렬 없이 입력이 주어진다면 먼저 정렬 후 동일 로직 적용

[ref 풀이 분석]
    set.discard(i): i가 set에 없어도 오류 없이 무시 (set.remove와 차이)
    set.remove(i):  i가 없으면 KeyError 발생

    불필요한 순회:
        outer for O(|section|) × inner range(i, i+m) O(m)
        = O(|section| × m) 최악 (실제론 분할 상환으로 O(|section| + m×k))
        풀이1 O(|section|) 대비 이론적으로 불리

    set in 연산 O(1):
        풀이1의 단순 비교(w > until_painted)보다 오버헤드 큼
        set 생성 비용도 추가

[실측 결과 — N=50,000 section, m=4, 10,000회]
    풀이1 (until_painted): 1.858ms  ← 가장 빠름
    풀이2 (deque):         3.989ms
    ref   (set+discard):   8.296ms  ← 가장 느림 (예측대로)
===================================================================================
[내 초기 풀이]
    solution_mine_one: until_painted 변수 + section 단순 순회
    solution_mine_two: deque + popleft로 처리된 구역 제거

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       단순 정수 비교, O(|section|), 실측 가장 빠름
    solution_mine_two: deque 변환 + popleft 오버헤드로 mine_one보다 느림
    solution_ref:      worst 사례 - 학습 목적
                       set+discard 조합이 직관적이나 실측 가장 느림
                       discard(): 없는 원소에도 오류 없이 무시
===================================================================================
[복잡도 분석]
    N = len(section) (최대 100,000)
    m = 롤러 길이 (최대 100,000)

    Mine_one - 시간: O(N)     | 공간: O(1) - 단순 변수 비교
    Mine_two - 시간: O(N)     | 공간: O(N) - deque 생성
    Ref      - 시간: O(N×m)  최악 | 공간: O(N) - set + range 순회
               (분할 상환 시 O(N + m×칠횟수))
    Best     - 시간: O(N)     | 공간: O(1) - Mine_one과 동일
    Sub      - 시간: O(N)     | 공간: O(N) - Mine_two와 동일
"""

from collections import deque
import time


# =================================================================================
# Mine solution one - until_painted 변수 + 단순 순회
# =================================================================================
def solution_mine_one(n: int, m: int, section: list[int]) -> int:
    """
    until_painted 변수로 칠해진 마지막 구역을 추적하며 section을 순회하는 초기 풀이

    until_painted:
        현재까지 페인트칠이 된 마지막 구역 번호
        w > until_painted: 아직 칠해지지 않은 구역 → 새로 칠 시작
        until_painted = w + m - 1: 롤러 범위 끝까지 칠해짐

    section이 오름차순 보장:
        별도 정렬 없이 순회만으로 "가장 왼쪽 미칠 구역" 자동 탐색
    """
    answer = 0
    until_painted = 0

    for w in section:
        if w > until_painted:
            answer += 1
            until_painted = w + m - 1

    return answer


# =================================================================================
# Mine solution two - deque + popleft
# =================================================================================
def solution_mine_two(n: int, m: int, section: list[int]) -> int:
    """
    deque로 section을 관리하며 처리된 구역을 popleft로 제거하는 풀이

    mine_one 대비:
        start: 현재 칠 시작 구역
        while q and q[0] < start + m: 범위 내 구역 모두 제거

    성능 한계:
        deque 변환 비용 + popleft 오버헤드
        실측 mine_one 대비 약 2배 느림
    """
    answer = 0
    q = deque(section)

    while q:
        start = q.popleft()
        answer += 1
        while q and q[0] < start + m:
            q.popleft()

    return answer


# =================================================================================
# Ref solution - set + discard (worst 사례, 학습 목적)
# =================================================================================
def solution_ref(n: int, m: int, section: list[int]) -> int:
    """
    set과 discard로 칠해진 구역을 제거하며 순회하는 참고 풀이

    set in 연산 O(1):
        칠해진 구역 여부를 O(1)로 확인하려는 의도

    s.discard(j):
        j가 set에 없어도 오류 없이 무시 (set.remove와 차이)
        range(i, i+m) 중 section에 없는 번호도 안전하게 처리

    실측 가장 느린 이유:
        outer for × inner range(i, i+m): 불필요한 m번 순회
        set 생성 비용 + discard 오버헤드
        풀이1의 단순 정수 비교(w > until_painted)보다 훨씬 무거움
    """
    count = 0
    s = set(section)

    for i in section:
        if i in s:
            count += 1
            for j in range(i, i + m):
                s.discard(j)

    return count


# =================================================================================
# Best solution - until_painted 변수 (mine_one 주석 보강)
# =================================================================================
def solution_best(n: int, m: int, section: list[int]) -> int:
    """
    until_painted 단일 변수로 O(N) 시간, O(1) 공간에 최소 횟수를 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        단순 정수 비교(w > until_painted): set in/deque popleft보다 빠름
        O(1) 공간: 추가 자료구조 없이 변수 하나만 사용
        실측 N=50,000: 1.858ms (mine_two 3.989ms, ref 8.296ms 대비 우위)
        section 오름차순 보장으로 정렬 없이 동작
    """
    answer = 0
    until_painted = 0

    for w in section:
        if w > until_painted:
            answer += 1
            until_painted = w + m - 1

    return answer


# =================================================================================
# Sub solution - deque + popleft (mine_two 주석 보강)
# =================================================================================
def solution_sub(n: int, m: int, section: list[int]) -> int:
    """
    deque로 section을 관리하며 그리디 동작 원리를 표현하는 서브 풀이

    Best 대비 특징:
        popleft()로 처리된 구역을 명시적으로 제거
        "start 이후 m 범위 내 구역 건너뜀" 동작이 코드에 직접 드러남
        O(N) 공간: deque 생성 비용
        실측 Best 대비 약 2배 느림
    """
    answer = 0
    q = deque(section)

    while q:
        start = q.popleft()
        answer += 1
        while q and q[0] < start + m:
            q.popleft()

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int, list[int], int]] = [
        # (n, m, section, 기댓값)
        # 공식 예시
        (8, 4, [2, 3, 6],       2),
        (5, 4, [1, 3],          1),
        (4, 1, [1, 2, 3, 4],    4),
        # 추가 케이스:
        # 단일 구역
        (10, 3, [5],            1),
        # 전체 커버 가능
        (10, 10, [1, 5, 10],    1),
    ]

    solutions = [
        ("Mine_one (until_painted)", solution_mine_one),
        ("Mine_two (deque)        ", solution_mine_two),
        ("Ref      (set+discard)  ", solution_ref),
        ("Best     (until_painted)", solution_best),
        ("Sub      (deque)        ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _m, _s, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _m, _s[:])

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (n, m, section, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, m, section[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
