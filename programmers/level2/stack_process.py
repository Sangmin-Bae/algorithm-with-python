"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 프로세스
    유형       : Stack / Queue
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42587
    풀이일자   : 2026-07-19
================================================================================
[문제 요약]
    우선순위 기반 큐에서 프로세스를 실행할 때
    location 인덱스 프로세스의 실행 순서 반환

    규칙:
        큐에서 프로세스를 꺼낸 후 더 높은 우선순위가 남아있으면 맨 뒤로 재삽입
        없으면 실행 (실행 후 큐에 다시 넣지 않음)

    제약 조건
        - priorities 길이: 1 이상 100 이하
        - priorities 원소: 1 이상 9 이하
        - location: 0 이상 len(priorities)-1 이하
================================================================================
[입출력 예시]
    priorities          | location | return
    --------------------|----------|-------
    [2, 1, 3, 2]        | 2        | 1
    [1, 1, 9, 1, 1, 1]  | 0        | 5
================================================================================
[풀이 방향 — 내부 반복 제거]
    풀이 1: any()로 매 꺼낼 때마다 큐 전체 탐색 → O(N) × while 횟수
    풀이 2: max()로 매 루프마다 priorities 전체 탐색 → O(N) × while 횟수
    풀이 3: sorted_ps 사전 정렬 + target_idx 포인터로 내부 반복 제거 → O(1)

[손 추적 — [2,1,3,2], location=2]
    초기: queue = [(2,0),(1,1),(3,2),(2,3)]
    sorted_ps = [3,2,2,1], target_idx=0

    풀이 3:
        (2,0): 2 == sorted_ps[0]=3? No → 맨 뒤로
        (1,1): 1 == 3? No → 맨 뒤로
        (3,2): 3 == 3? Yes → answer=1, target_idx=1, curr_idx=2==location → break
        → return 1 ✓

[solution_two priorities 오염 방식]
    priorities[curr_idx] = 0: 처리된 프로세스를 0으로 표시
    다음 루프에서 max() 재계산 시 0은 최댓값이 될 수 없음 → 자동 제외

    처리 순서 주의:
        answer += 1
        if curr_idx == location: break   ← location 체크를 먼저
        priorities[curr_idx] = 0         ← 오염은 break 이후 없으므로 이후 처리
        순서가 바뀌어도 동작은 같으나 현재 순서가 의도 명확

[복잡도 분석]
    N = len(priorities) (최대 100)
    K = while 루프 총 반복 횟수 (최악 O(N²): 각 프로세스가 최대 N번 재삽입)

    Mine_one   - 시간: O(N²) | 공간: O(N) - any() O(N) × K번
    Mine_two   - 시간: O(N²) | 공간: O(1) - max() O(N) × K번, 추가 자료구조 없음
    Mine_three - 시간: O(N²) | 공간: O(N) - 정렬 O(N log N) + 내부 O(1) × K번
    Best       - 시간: O(N²) | 공간: O(N) - Mine_three와 동일
    Sub        - 시간: O(N²) | 공간: O(N) - Mine_one과 동일

    모든 풀이 O(N²) 최악이나 상수 인자 차이:
        Mine_one/two: O(N²) × O(N) 내부 탐색 = O(N³) 최악에 가까움
        Mine_three:   O(N²) × O(1) 내부 탐색 = O(N²) 엄밀히 성립
    N≤100 고정 → 실질 모두 충분히 빠름
================================================================================
[내 초기 풀이]
    solution_mine_one  : deque + any() 탐색
    solution_mine_two  : 포인터 방식 + max() 탐색 + priorities 오염
    solution_mine_three: deque + sorted 사전 정렬 + target_idx 포인터

[개선 포인트]
    solution_mine_one  : any() O(N) → sorted 방식으로 내부 반복 제거 가능
                         지문 알고리즘을 가장 직접적으로 표현 → Sub
    solution_mine_two  : max() O(N) → while 내부 반복 존재
                         초기 deque 생성 없음, 포인터 방식으로 직관적
    solution_mine_three: 내부 반복 없음, 상수 인자 작음 → Best
"""

import time
from collections import deque


# ================================================================================
# Mine solution one - deque + any() 탐색
# ================================================================================
def solution_mine_one(priorities: list[int], location: int) -> int:
    """
    deque로 큐를 시뮬레이션하고 any()로 높은 우선순위 존재 여부를 확인하는 초기 풀이

    핵심:
        queue: (우선순위, 원본인덱스) 튜플로 관리
        any(p > curr[0] for p, i in queue): 더 높은 우선순위가 있으면 재삽입
        curr[1] == location: 실행된 프로세스가 대상이면 answer 반환

    한계:
        any() O(N): 매 popleft마다 큐 전체 탐색
        while 반복 횟수 × O(N) = 최악 O(N³)에 가까움

    지문 알고리즘 규칙 1~3을 코드에 가장 직접적으로 표현한 풀이
    """
    answer = 0
    queue = deque((p, i) for i, p in enumerate(priorities))

    while queue:
        curr = queue.popleft()

        if any(p > curr[0] for p, i in queue):
            queue.append(curr)
            continue

        answer += 1

        if curr[1] == location:
            break

    return answer


# ================================================================================
# Mine solution two - 포인터 방식 + max() + priorities 오염
# ================================================================================
def solution_mine_two(priorities: list[int], location: int) -> int:
    """
    인덱스 포인터와 max()로 처리 여부를 판단하고 처리된 항목을 0으로 오염하는 풀이

    핵심:
        max_p: 현재 남은 프로세스 중 최대 우선순위
        priorities[curr_idx] == max_p: 현재 포인터가 최우선순위이면 실행
        priorities[curr_idx] = 0: 처리 후 오염 → 다음 max() 계산에서 제외
        curr_idx = (curr_idx + 1) % n: 원형 포인터 순회

    한계:
        max() O(N): 매 루프마다 전체 탐색
        초기 deque 생성 없음 → mine_one 대비 초기화 비용 없음
    """
    answer = 0
    n = len(priorities)
    curr_idx = 0

    while True:
        max_p = max(priorities)

        if priorities[curr_idx] == max_p:
            answer += 1

            if curr_idx == location:
                break

            priorities[curr_idx] = 0   # 처리 후 오염 → 다음 max()에서 제외

        curr_idx = (curr_idx + 1) % n

    return answer


# ================================================================================
# Mine solution three - deque + sorted 사전 정렬 + target_idx 포인터
# ================================================================================
def solution_mine_three(priorities: list[int], location: int) -> int:
    """
    사전 정렬된 sorted_ps와 target_idx 포인터로 내부 반복을 제거한 풀이

    핵심:
        sorted_ps: priorities를 내림차순 정렬 → 실행 순서대로 나열
        target_idx: 다음 실행할 우선순위 포인터
        curr_p == sorted_ps[target_idx]: 현재 프로세스가 다음 실행 대상인지 확인

    mine_one 대비 개선:
        any() O(N) 내부 탐색 → sorted_ps[target_idx] O(1) 비교로 대체
        내부 반복 없음 → 상수 인자 작음

    초기 비용:
        deque 생성: O(N)
        sorted(): O(N log N)
        1회성 비용 → while 내부 반복 제거로 보상
    """
    answer = 0
    queue = deque((p, i) for i, p in enumerate(priorities))
    sorted_ps = sorted(priorities, reverse=True)   # 실행 순서 사전 계산
    target_idx = 0

    while queue:
        curr_p, curr_idx = queue.popleft()

        if curr_p == sorted_ps[target_idx]:
            answer += 1
            target_idx += 1             # 다음 실행 우선순위로 포인터 전진

            if curr_idx == location:
                break
        else:
            queue.append((curr_p, curr_idx))

    return answer


# ================================================================================
# Best solution - deque + sorted + target_idx (mine_three 주석 보강)
# ================================================================================
def solution_best(priorities: list[int], location: int) -> int:
    """
    sorted_ps와 target_idx 포인터로 내부 반복 없이 O(N²) × O(1)을 달성하는 최적 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        sorted_ps 사전 정렬: "다음에 실행할 우선순위"를 O(1)로 조회
        target_idx 포인터: 처리된 프로세스 수만큼 전진
        while 내부 O(1): any/max O(N) 없음 → 상수 인자 최소화
        priorities 불변: 원본 변경 없음 (mine_two의 오염 방식과 대비)
    """
    answer = 0
    queue = deque((p, i) for i, p in enumerate(priorities))
    sorted_ps = sorted(priorities, reverse=True)
    target_idx = 0

    while queue:
        curr_p, curr_idx = queue.popleft()

        if curr_p == sorted_ps[target_idx]:
            answer += 1
            target_idx += 1

            if curr_idx == location:
                break
        else:
            queue.append((curr_p, curr_idx))

    return answer


# ================================================================================
# Sub solution - deque + any() (mine_one 주석 보강)
# ================================================================================
def solution_sub(priorities: list[int], location: int) -> int:
    """
    지문의 알고리즘 규칙을 deque + any()로 직접 표현하는 서브 풀이

    Best 대비 특징:
        지문 규칙 1~3을 코드에 가장 직접적으로 표현
        규칙 2 "더 높은 우선순위가 있다면": any(p > curr[0] for ...)로 명시
        any() O(N): N≤100 제약에서 실질 차이 없음
        동작 원리가 직관적으로 드러나는 학습 목적에 적합
    """
    answer = 0
    queue = deque((p, i) for i, p in enumerate(priorities))

    while queue:
        curr = queue.popleft()

        if any(p > curr[0] for p, i in queue):
            queue.append(curr)
            continue

        answer += 1

        if curr[1] == location:
            break

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int, int]] = [
        # (priorities, location, 기댓값)
        # 손 추적:
        # [2,1,3,2], location=2
        # sorted_ps=[3,2,2,1]
        # (2,0): 2≠3 → 뒤로, (1,1): 1≠3 → 뒤로
        # (3,2): 3==3 → answer=1, idx=2==location → return 1
        ([2, 1, 3, 2], 2, 1),
        # [1,1,9,1,1,1], location=0
        # sorted_ps=[9,1,1,1,1,1]
        # A(1,0): 1≠9 → 뒤로 ... C(9,2): 9==9 → answer=1, target=1
        # D(1,3): 1==1 → answer=2, E(1,4): answer=3, F(1,5): answer=4
        # A(1,0): 1==1 → answer=5, idx=0==location → return 5
        ([1, 1, 9, 1, 1, 1], 0, 5),
        # 추가 케이스:
        # 단일 프로세스
        ([1], 0, 1),
        # 모두 동일 우선순위 → 순서대로 실행
        ([1, 1, 1], 2, 3),
        # location이 최고 우선순위
        ([1, 2, 3, 4], 3, 1),
    ]

    solutions = [
        ("Mine_one   (deque+any)   ", solution_mine_one),
        ("Mine_two   (포인터+max)  ", solution_mine_two),
        ("Mine_three (sorted+ptr)  ", solution_mine_three),
        ("Best       (sorted+ptr)  ", solution_best),
        ("Sub        (deque+any)   ", solution_sub),
    ]

    # 워밍업 스텝
    _p, _l, _ = test_cases[0]
    for _, func in solutions:
        func(_p[:], _l)

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (priorities, location, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(priorities[:], location)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
