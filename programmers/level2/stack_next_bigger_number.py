"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 뒤에 있는 큰 수 찾기
    유형       : Stack
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/154539
    풀이일자   : 2026-08-18
================================================================================
[문제 요약]
    numbers 배열의 각 원소에 대해 자신보다 뒤에 있으면서
    자신보다 크고 가장 가까운 수(뒷 큰수)를 담은 배열 반환
    뒷 큰수가 없으면 -1

    제약 조건
        - numbers 길이: 1 이상 1,000,000 이하
        - numbers 원소: 1 이상 1,000,000 이하
================================================================================
[입출력 예시]
    numbers          | result
    -----------------|------------------
    [2, 3, 3, 5]     | [3, 5, 5, -1]
    [9, 1, 5, 3, 6, 2]| [-1, 5, 6, 6, -1, -1]
================================================================================
[완전탐색 → 스택 발상의 전환]
    완전탐색: 현재 원소 → 미래를 탐색
        "나(현재 원소)의 뒷 큰수가 누구야?"
        → 오른쪽으로 직접 탐색 O(N²)

    스택: 현재 원소 → 과거를 해결 (ref_one)
        "내(새로 등장한 수)가 앞에 있는 누군가의 뒷 큰수가 될 수 있어?"
        → 스택에서 나보다 작은 것들의 답을 해결

    시점이 완전히 반대:
        완전탐색: 내가 앞으로 나가며 찾음
        스택:     뒤에서 등장한 수가 앞의 수들에게 답을 알려줌

[단조 스택 (Monotonic Stack)]
    스택이 항상 아래에서 위로 갈수록 값이 작아지는 구조 유지
    새 원소가 스택 맨 위보다 작으면 그냥 쌓음
    새 원소가 스택 맨 위보다 크면 맨 위를 꺼내며 answer 채움

    스택[-1] = 가장 나중에 쌓인 것 = 현재 위치에서 가장 가까운 미처리 원소
    후입선출(LIFO) 덕에 가장 가까운 것부터 처리됨

[ref_one — 정방향 (왼쪽→오른쪽)]
    스택 = "아직 뒷 큰수를 못 찾은 원소들의 인덱스"
    새 원소 등장 → 스택에서 나보다 작은 것들의 답 해결
    스택에 인덱스 저장 (answer[last_index] = numbers[i])

    손 추적 [4,2,5,1,3]:
        i=0: stack=[0]
        i=1: 2<4, stack=[0,1]
        i=2: 5>2→answer[1]=5, 5>4→answer[0]=5, stack=[2]
        i=3: 1<5, stack=[2,3]
        i=4: 3>1→answer[3]=3, 3<5, stack=[2,4]
        남은 [2,4] → -1
        → [5,5,-1,3,-1] ✓

[ref_two — 역방향 (오른쪽→왼쪽)]
    스택 = "오른쪽에서 쌓아온 답 후보들"
    현재 원소 → 스택에서 나보다 큰 첫 번째가 답
    나보다 작거나 같은 후보는 버려도 됨:
        이미 numbers[i] >= stack[-1]이므로
        왼쪽 원소들한테도 numbers[i]가 먼저 답이 돼버림
    스택에 값 저장 (answer[i] = stack[-1])

    손 추적 [4,2,5,1,3]:
        i=4: stack=[], answer[4]=-1, stack=[3]
        i=3: 3>1, stack=[3], answer[3]=3, stack=[3,1]
        i=2: 1<=5 pop, 3<=5 pop, stack=[], answer[2]=-1, stack=[5]
        i=1: 5>2, stack=[5], answer[1]=5, stack=[5,2]
        i=0: 2<=4 pop, stack=[5], answer[0]=5, stack=[5,4]
        → [5,5,-1,3,-1] ✓

[왜 O(N)인가 — 분할 상환 분석]
    각 원소는 스택에 정확히 1번 push, 최대 1번 pop
    총 push: N번, 총 pop: 최대 N번
    while 루프가 있어도 전체 pop이 N을 넘을 수 없음
    → O(2N) = O(N)
================================================================================
[내 초기 풀이]
    solution_mine: 완전탐색 O(N²) → 시간 초과

[개선 포인트]
    solution_mine:    O(N²) → 시간 초과 (N=1,000,000이면 10^12 연산)
    solution_ref_one: 단조 스택 정방향 O(N) - Best
                      "앞 원소들의 답을 현재 원소가 해결"
    solution_ref_two: 단조 스택 역방향 O(N) - Sub
                      "현재 원소의 답을 오른쪽 후보 풀에서 가져옴"
================================================================================
[복잡도 분석]
    N = len(numbers) (최대 1,000,000)

    Mine     - 시간: O(N²) | 공간: O(N) - 이중 루프
    Ref_one  - 시간: O(N)  | 공간: O(N) - 스택 최대 N개
    Ref_two  - 시간: O(N)  | 공간: O(N) - 스택 최대 N개
    Best     - 시간: O(N)  | 공간: O(N) - Ref_one과 동일
    Sub      - 시간: O(N)  | 공간: O(N) - Ref_two와 동일
"""

import time


# ================================================================================
# Mine solution - 완전탐색 (시간 초과)
# ================================================================================
def solution_mine(numbers: list[int]) -> list[int]:
    """
    각 원소에서 오른쪽을 직접 탐색해 뒷 큰수를 찾는 초기 풀이 (시간 초과)

    for-else 패턴:
        break로 탈출하지 않고 루프가 끝나면 else 실행
        뒷 큰수를 못 찾은 경우 -1 추가

    시간 초과 이유:
        각 원소마다 최악 N번 탐색 → O(N²)
        N=1,000,000이면 10^12 연산 불가능
    """
    answer = []

    for idx in range(len(numbers) - 1):
        num = numbers[idx]
        for k in numbers[idx + 1:]:
            if k > num:
                answer.append(k)
                break
        else:
            answer.append(-1)

    answer.append(-1)
    return answer


# ================================================================================
# Ref solution one - 단조 스택 정방향
# ================================================================================
def solution_ref_one(numbers: list[int]) -> list[int]:
    """
    정방향 단조 스택으로 O(N)에 뒷 큰수를 구하는 풀이

    스택 = "아직 뒷 큰수를 못 찾은 원소들의 인덱스"
    새 원소 numbers[i] 등장 시:
        스택 맨 위(가장 가까운 미처리 원소)보다 크면
        → 그 원소의 뒷 큰수 = numbers[i] → answer 채우고 pop
        → 반복 (다음 미처리 원소도 확인)
        크지 않으면 → 스택에 i 추가

    스택에 인덱스 저장 이유:
        answer[last_index] = numbers[i] 로 정답을 써야 하기 때문
    """
    answer = [-1] * len(numbers)
    stack = []

    for i in range(len(numbers)):
        while stack and numbers[i] > numbers[stack[-1]]:
            last_index = stack.pop()
            answer[last_index] = numbers[i]
        stack.append(i)

    return answer


# ================================================================================
# Ref solution two - 단조 스택 역방향
# ================================================================================
def solution_ref_two(numbers: list[int]) -> list[int]:
    """
    역방향 단조 스택으로 O(N)에 뒷 큰수를 구하는 풀이

    스택 = "오른쪽에서 쌓아온 답 후보들"
    현재 원소 numbers[i] 처리 시:
        스택 맨 위가 numbers[i] 이하면 → 후보 자격 없음 → pop
        (왼쪽 원소들한테 numbers[i]가 먼저 답이 되므로 영원히 쓸모없음)
        스택에 남은 맨 위 = 현재 원소의 뒷 큰수

    스택에 값 저장 이유:
        answer[i] = stack[-1] 로 바로 쓰기 때문
    """
    n = len(numbers)
    answer = [-1] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and stack[-1] <= numbers[i]:
            stack.pop()

        if stack:
            answer[i] = stack[-1]

        stack.append(numbers[i])

    return answer


# ================================================================================
# Best solution - 단조 스택 정방향 (ref_one 주석 보강)
# ================================================================================
def solution_best(numbers: list[int]) -> list[int]:
    """
    정방향 단조 스택으로 O(N) 시간, O(N) 공간에 뒷 큰수를 구하는 최적 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        발상: "새 원소가 앞 원소들의 뒷 큰수가 될 수 있는가"
        단조 스택: 스택이 항상 아래→위로 값이 감소하는 구조 유지
        분할 상환 O(N): 각 원소는 push 1회, pop 최대 1회
        완전탐색 O(N²) 대비 N=1,000,000에서 압도적 우위
    """
    answer = [-1] * len(numbers)
    stack = []

    for i in range(len(numbers)):
        while stack and numbers[i] > numbers[stack[-1]]:
            last_index = stack.pop()
            answer[last_index] = numbers[i]
        stack.append(i)

    return answer


# ================================================================================
# Sub solution - 단조 스택 역방향 (ref_two 주석 보강)
# ================================================================================
def solution_sub(numbers: list[int]) -> list[int]:
    """
    역방향 단조 스택으로 뒷 큰수를 구하는 서브 풀이

    Best 대비 특징:
        발상: "오른쪽에서 쌓아온 후보 풀에서 현재 원소의 답을 가져옴"
        역방향 순회: 오른쪽 정보를 먼저 쌓고 왼쪽을 처리
        스택에 값 저장 (Best는 인덱스 저장)
        answer[i] = stack[-1] 로 바로 기록
        O(N) 시간, O(N) 공간으로 Best와 동일
    """
    n = len(numbers)
    answer = [-1] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and stack[-1] <= numbers[i]:
            stack.pop()

        if stack:
            answer[i] = stack[-1]

        stack.append(numbers[i])

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], list[int]]] = [
        # (numbers, 기댓값)
        ([2, 3, 3, 5],        [3, 5, 5, -1]),
        ([9, 1, 5, 3, 6, 2],  [-1, 5, 6, 6, -1, -1]),
        # 추가 케이스:
        ([1],                  [-1]),           # 단일 원소
        ([5, 4, 3, 2, 1],     [-1,-1,-1,-1,-1]), # 내림차순 (최악)
        ([1, 2, 3, 4, 5],     [2, 3, 4, 5, -1]), # 오름차순
    ]

    solutions = [
        ("Mine    (완전탐색)    ", solution_mine),
        ("Ref_one (정방향스택) ", solution_ref_one),
        ("Ref_two (역방향스택) ", solution_ref_two),
        ("Best    (정방향스택) ", solution_best),
        ("Sub     (역방향스택) ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _ = test_cases[0]
    for _, func in solutions:
        func(_n[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (numbers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(numbers[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
