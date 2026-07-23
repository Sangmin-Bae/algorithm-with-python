"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 타겟 넘버
    유형       : DFS / BFS (완전탐색)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/43165
    풀이일자   : 2026-07-23
================================================================================
[문제 요약]
    numbers의 각 정수에 +/- 부호를 순서대로 선택해서 합산했을 때
    target과 같은 값이 되는 경우의 수 반환

    제약 조건
        - numbers 길이: 2 이상 20 이하
        - 각 숫자: 1 이상 50 이하
        - target: 1 이상 1000 이하
        - 전체 경우의 수: 2^n (최대 2^20 = 1,048,576)
================================================================================
[입출력 예시]
    numbers           | target | return
    ------------------|--------|-------
    [1, 1, 1, 1, 1]  | 3      | 5
    [4, 1, 2, 1]     | 4      | 2
================================================================================
[핵심 구조 - 이진 결정 트리]
    각 numbers[i]에 +/-를 선택하는 문제
    -> 깊이 n의 완전 이진 트리 구조

          s=0
         +   -
      +n[0]  -n[0]
       + -    + -
   +n[1] -n[1] ...
    ...
    리프 노드 수 = 2^n

    이 트리를 완전 탐색해서 리프 값이 target인 개수를 셈

[solution_one - 결정 트리 DFS]
    일반 그래프 DFS와의 차이:
        일반 DFS: 그래프 노드 탐색, visited로 중복 방문 방지
        이 DFS:  결정 트리 탐색, visited 없음
                 각 레벨에서 두 가지 선택(+, -)만 존재
                 상태 = (인덱스, 누적합), 방문 개념 없음

    백트래킹을 인수로 처리한 이유:
        dfs(idx+1, s + sign*numbers[idx]) 형태로 호출
        각 재귀 호출이 독립적인 s 값을 가짐
        -> 재귀 복귀 시 s를 복원할 필요 없음
        명시적 s += ... -> dfs -> s -= ... 불필요

[solution_two - 레이어별 누적합 BFS]
    일반 BFS와의 차이:
        일반 BFS: 그래프 노드의 이웃 탐색, visited 필요
        이 BFS:  레이어(숫자) 단위로 누적합 경우의 수 확장
                 같은 누적합이 중복되어도 모두 유효한 경우
                 visited 개념 없음

    레이어 동작:
        layer = [0]             # 초기: 합이 0인 경우 1개
        n=1 처리: [1, -1]
        n=1 처리: [2, 0, 0, -2]
        n=1 처리: [3,1,1,-1,1,-1,-1,-3]
        ...
        최종 layer.count(target) = 정답

    layer 크기가 2배씩 증가 -> 최종 크기 2^n

[solution_ref_two - target 감소 재귀]
    발상: 누적합을 증가시키는 대신 target을 감소
    수식 변형:
        +a + b + c = target
        b + c = target - a   (a를 더하는 경우)
        b + c = target + a   (a를 빼는 경우, -a를 좌변으로)

    손 추적 (numbers=[1,1], target=0):
        solution([1], 0+1=1) -> solution([], 1+1=2) + solution([], 1-1=0)
                                  0                      1 (target==0 !)
        solution([1], 0-1=-1) -> solution([], -1+1=0) + solution([], -1-1=-2)
                                    1 (target==0 !)        0
        총 2 -> +1-1=0, -1+1=0 두 가지 ✓

    기저 조건: numbers가 빈 리스트 -> target==0이면 경우 발견(1), 아니면 0

[solution_ref_three - 비트마스킹]
    발상: n개 +/- 선택 = n비트 이진수 표현
    0부터 2^n-1까지 순회하면 모든 조합을 정확히 한 번 씩 커버

    비트마스킹:
        i & (2**j): i의 j번째 비트가 1인지 확인
        0이면 numbers[j] 양수, 1이면 numbers[j] 음수

    손 추적 (numbers=[4,1,2,1], i=5=0101₂):
        j=0: 5 & 1 = 1 -> -4
        j=1: 5 & 2 = 0 -> +1
        j=2: 5 & 4 = 4 -> -2 (0이 아니므로 음수)
        j=3: 5 & 8 = 0 -> +1
        sum = -4+1-2+1 = -4 (target=4와 다름)
================================================================================
[내 초기 풀이]
    solution_mine_one: 재귀 DFS (결정 트리 완전 탐색)
    solution_mine_two: 레이어 BFS (누적합 경우의 수 확장)

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       결정 트리 구조가 코드에 직접 드러남
                       sign in [-1, 1]으로 +/- 선택 간결하게 표현
    solution_mine_two: 개선 필요 없음 - Sub
                       재귀 없이 명시적으로 경우의 수 관리
                       layer 크기 2^n까지 증가 -> 공간 O(2^n)
================================================================================
[복잡도 분석]
    N = len(numbers) (최대 20)
    전체 경우의 수 = 2^N (최대 1,048,576)

    Mine_one   - 시간: O(2^N) | 공간: O(N)    - 재귀 스택 깊이 N
    Mine_two   - 시간: O(2^N) | 공간: O(2^N)  - 최종 layer 크기 2^N
    Ref_one    - 시간: O(2^N) | 공간: O(2^N)  - product 생성 + 합산 리스트
    Ref_two    - 시간: O(2^N) | 공간: O(N)    - 재귀 스택 깊이 N
    Ref_three  - 시간: O(N×2^N) | 공간: O(N)  - 2^N 루프 × 내부 N 순회
    Best       - 시간: O(2^N) | 공간: O(N)    - Mine_one과 동일
    Sub        - 시간: O(2^N) | 공간: O(2^N)  - Mine_two와 동일

    N=20: 2^20 = 1,048,576 -> 모든 풀이 충분히 빠름
    Mine_one / Ref_two: 공간 O(N)으로 가장 효율적
"""

from itertools import product
import time


# ================================================================================
# Mine solution one - 재귀 DFS (결정 트리 완전 탐색)
# ================================================================================
def solution_mine_one(numbers: list[int], target: int) -> int:
    """
    결정 트리를 재귀 DFS로 완전 탐색하는 풀이

    결정 트리 구조:
        각 레벨 = numbers의 인덱스
        각 노드에서 두 가지 선택: +numbers[idx], -numbers[idx]
        리프 노드(idx == len(numbers)): 모든 부호 결정 완료, s와 target 비교

    visited 없는 이유:
        그래프 노드 탐색이 아닌 결정 트리 탐색
        같은 (idx, s) 조합도 다른 경로로 도달할 수 있어 모두 유효

    인수로 백트래킹 처리:
        dfs(idx+1, s + sign*numbers[idx]): 각 재귀 호출이 독립적 s 보유
        재귀 복귀 시 s 복원 불필요

    ※ 설명 정정: sign * numbers[idx] (곱셈), sign + numbers[idx] 아님
    """
    answer = 0

    def dfs(idx: int, s: int) -> None:
        nonlocal answer

        if idx == len(numbers):
            if s == target:
                answer += 1
            return

        for sign in [-1, 1]:
            dfs(idx + 1, s + (sign * numbers[idx]))

    dfs(0, 0)
    return answer


# ================================================================================
# Mine solution two - 레이어 BFS (누적합 경우의 수 확장)
# ================================================================================
def solution_mine_two(numbers: list[int], target: int) -> int:
    """
    numbers를 레이어 단위로 처리하며 가능한 누적합 전체를 관리하는 풀이

    레이어 동작:
        layer: 현재까지의 모든 가능한 누적합 목록
        각 숫자 n을 처리할 때 이전 layer의 모든 값에 +n, -n 추가
        layer 크기가 매 단계 2배 증가 -> 최종 크기 2^N

    일반 BFS와 차이:
        일반 BFS: 특정 노드에서 이웃 탐색, visited 필요
        이 방식: 레이어 전체를 한꺼번에 확장, visited 없음
                 같은 누적합 값이 중복되어도 모두 유효한 경우

    최종 layer.count(target):
        2^N개 누적합 중 target과 같은 값의 수 = 정답
    """
    layer = [0]

    for n in numbers:
        next_layer = []
        for s in layer:
            next_layer.append(s + n)
            next_layer.append(s - n)
        layer = next_layer

    return layer.count(target)


# ================================================================================
# Ref solution one - product로 모든 부호 조합 생성
# ================================================================================
def solution_ref_one(numbers: list[int], target: int) -> int:
    """
    itertools.product로 모든 +/- 조합을 생성해 합산하는 참고 풀이

    핵심:
        choices = [(n, -n) for n in numbers]
            각 숫자의 (양수, 음수) 쌍 생성
        product(*choices):
            *로 언패킹해 각 쌍을 독립 인수로 전달
            모든 조합의 튜플 생성 (2^N개)
        sum(p) for p in product(*choices):
            각 조합의 합산
        .count(target): target 일치 횟수

    Mine_two와 동일한 아이디어를 product 라이브러리로 표현
    모든 조합 리스트를 메모리에 한 번에 생성 -> 공간 O(2^N)
    """
    choices = [(n, -n) for n in numbers]
    return [sum(p) for p in product(*choices)].count(target)


# ================================================================================
# Ref solution two - target 감소 재귀
# ================================================================================
def solution_ref_two(numbers: list[int], target: int) -> int:
    """
    누적합을 늘리는 대신 target을 줄여서 0이 되는 경우를 세는 참고 풀이

    수식 변형 원리:
        +a + (나머지) = target
        (나머지) = target - a   (a를 더하는 경우)
        (나머지) = target + a   (a를 빼는 경우, -a를 이항)

    즉 numbers[0]에 +를 선택하면 나머지 숫자들로 target-numbers[0]을 만들어야 하고
    -를 선택하면 나머지 숫자들로 target+numbers[0]을 만들어야 함

    기저 조건:
        numbers가 빈 리스트 = 모든 숫자 처리 완료
        target == 0: 수식 성립 -> 1 반환
        target != 0: 수식 불성립 -> 0 반환

    Mine_one과 동일한 O(2^N) 시간, O(N) 공간
    발상 방향이 반대 (합 증가 vs target 감소)
    """
    if not numbers:
        return 1 if target == 0 else 0

    return (solution_ref_two(numbers[1:], target + numbers[0])
          + solution_ref_two(numbers[1:], target - numbers[0]))


# ================================================================================
# Ref solution three - 비트마스킹으로 모든 부호 조합 열거
# ================================================================================
def solution_ref_three(numbers: list[int], target: int) -> int:
    """
    n개 +/- 선택을 n비트 이진수로 표현해 모든 조합을 열거하는 참고 풀이

    비트마스킹 원리:
        0 ~ 2^n-1을 순회하면 n비트의 모든 조합을 한 번씩 커버
        i의 j번째 비트: i & (2**j)
            0이면 numbers[j] 양수
            0이 아니면(1이면) numbers[j] 음수

    손 추적 (numbers=[4,1,2,1], i=5=0101₂):
        j=0: 5 & 1=1 -> -4
        j=1: 5 & 2=0 -> +1
        j=2: 5 & 4=4 (0 아님) -> -2
        j=3: 5 & 8=0 -> +1
        sum = -4 (target=4와 다름)

    시간 O(N × 2^N): 2^N 루프 × 내부 N 순회
    Mine_one/two O(2^N) 대비 N배 더 느림
    """
    answer = 0
    for i in range(2 ** len(numbers)):
        tmp = []
        for j in range(len(numbers)):
            if i & (2 ** j) == 0:
                tmp.append(numbers[j])
            else:
                tmp.append(-1 * numbers[j])
        if sum(tmp) == target:
            answer += 1
    return answer


# ================================================================================
# Best solution - 재귀 DFS (mine_one 주석 보강)
# ================================================================================
def solution_best(numbers: list[int], target: int) -> int:
    """
    결정 트리를 재귀 DFS로 탐색해 O(2^N) 시간, O(N) 공간으로 정답을 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        결정 트리 구조: 깊이 N, 분기 2 -> 2^N 리프 노드
        idx == len(numbers): 모든 부호 결정 완료, s와 target 비교
        공간 O(N): 재귀 스택 깊이 = numbers 길이, Mine_two O(2^N) 대비 효율적
        sign in [-1, 1]: +/- 선택을 간결하게 표현
    """
    answer = 0

    def dfs(idx: int, s: int) -> None:
        nonlocal answer

        if idx == len(numbers):
            if s == target:
                answer += 1
            return

        for sign in [-1, 1]:
            dfs(idx + 1, s + (sign * numbers[idx]))

    dfs(0, 0)
    return answer


# ================================================================================
# Sub solution - 레이어 BFS (mine_two 주석 보강)
# ================================================================================
def solution_sub(numbers: list[int], target: int) -> int:
    """
    레이어별 누적합 확장으로 재귀 없이 모든 경우를 관리하는 서브 풀이

    Best 대비 특징:
        재귀 없이 명시적 리스트로 경우의 수 관리
        layer가 각 단계마다 2배 증가 -> 최종 크기 2^N
        공간 O(2^N): Best O(N) 대비 많은 공간 사용
        동작 원리(레이어별 확장)가 직관적으로 드러남
    """
    layer = [0]

    for n in numbers:
        next_layer = []
        for s in layer:
            next_layer.append(s + n)
            next_layer.append(s - n)
        layer = next_layer

    return layer.count(target)


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int, int]] = [
        # (numbers, target, 기댓값)
        # 손 추적:
        # [1,1,1,1,1], target=3
        # 5가지 방법 존재
        ([1, 1, 1, 1, 1], 3, 5),
        # [4,1,2,1], target=4
        # +4+1-2+1=4, +4-1+2-1=4 -> 2가지
        ([4, 1, 2, 1], 4, 2),
        # 추가 케이스:
        # [1,1], target=0 -> +1-1=0, -1+1=0 -> 2가지
        ([1, 1], 0, 2),
        # [1], target=1 -> +1=1 -> 1가지
        ([1], 1, 1),
    ]

    solutions = [
        ("Mine_one   (재귀DFS)   ", solution_mine_one),
        ("Mine_two   (레이어BFS) ", solution_mine_two),
        ("Ref_one    (product)   ", solution_ref_one),
        ("Ref_two    (target감소)", solution_ref_two),
        ("Ref_three  (비트마스킹)", solution_ref_three),
        ("Best       (재귀DFS)   ", solution_best),
        ("Sub        (레이어BFS) ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _t, _ = test_cases[0]
    for _, func in solutions:
        func(_n[:], _t)

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (numbers, target, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(numbers[:], target)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
