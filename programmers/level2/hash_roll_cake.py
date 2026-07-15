"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 롤케이크 자르기
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/132265
    풀이일자   : 2026-07-15
================================================================================
[문제 요약]
    topping 배열에서 한 위치를 기준으로 잘랐을 때
    왼쪽과 오른쪽의 토핑 종류 수가 같은 경우의 수 반환

    제약 조건
        - topping 길이: 1 이상 1,000,000 이하
        - topping 원소: 1 이상 10,000 이하
================================================================================
[입출력 예시]
    topping                  | result
    -------------------------|-------
    [1, 2, 1, 3, 1, 4, 1, 2] | 2
    [1, 2, 3, 1, 4]          | 0
================================================================================
[핵심 아이디어 — 포인터 방식으로 양측 종류 수 추적]
    매 슬라이싱 위치마다 양쪽을 새로 계산하는 대신
    "형(older): 전체에서 시작, 동생(younger): 비어서 시작"으로 설정
    topping을 왼쪽에서 오른쪽으로 한 개씩 넘기면서 양측 종류 수 갱신

    손 추적 ([1,2,1,3,1,4,1,2]):
        초기: older={1:4,2:2,3:1,4:1}, older_type=4, younger={}

        t=1: younger={1}, older[1]=3, type=4 → 1 vs 4 ✗
        t=2: younger={1,2}, older[2]=1, type=4 → 2 vs 4 ✗
        t=1: younger={1,2}, older[1]=2, type=4 → 2 vs 4 ✗
        t=3: younger={1,2,3}, older[3]=0→type=3 → 3 vs 3 ✓ answer=1
        t=1: younger={1,2,3}, older[1]=1, type=3 → 3 vs 3 ✓ answer=2
        t=4: younger={1,2,3,4}, older[4]=0→type=2 → 4 vs 2 ✗
        t=1: younger={1,2,3,4}, older[1]=0→type=1 → 4 vs 1 ✗
        t=2: younger={1,2,3,4}, older[2]=0→type=0 → 4 vs 0 ✗
        → answer = 2 ✓

[시간 초과 원인 분석 — 풀이 1~3]
    풀이 1:
        매 루프마다 topping[:i], topping[i:] 슬라이싱 → 새 리스트 O(N)
        set() 변환 → O(N)
        → 전체 O(N²) → 시간 초과

    풀이 2, 3:
        sum(1 for v in older.values() if v != 0)
        → older 전체 순회 O(K) (K=토핑 종류 수, 최대 10,000)
        → 상위 루프 N과 곱하면 O(N×K) = 최대 100억 연산 → 시간 초과

        딕셔너리 초기화 for문: O(N) 1회 → 병목 아님
        Counter(풀이 3): C 레벨 구현으로 딕셔너리 초기화보다 빠르나
                         핵심 병목인 sum(제너레이터) O(K) 미해결

    풀이 4, 5 핵심 개선:
        older_type_count 정수 변수로 관리
        older[t] == 0일 때만 -=1 → O(1) 갱신
        sum(제너레이터) O(K) → 정수 비교 O(1) 대체
        → 전체 O(N) → 시간 초과 해결

[Counter 특성 주의]
    Counter는 없는 키 접근 시 0 반환 (KeyError 없음)
    older[t] -= 1 후 값이 0이 되어도 키는 남음
    → older[t] == 0 조건이 정확하게 동작
    이 문제에서 topping 순서대로 순회하므로
    존재하는 키만 접근 → 안전하게 동작
================================================================================
[내 초기 풀이]
    solution_mine_one  : 슬라이싱 + set 변환 (시간 초과)
    solution_mine_two  : older 딕셔너리 + younger set + sum(제너레이터) (시간 초과)
    solution_mine_three: Counter + younger set + sum(제너레이터) (시간 초과)
    solution_mine_four : older 딕셔너리 + younger set + older_type_count 정수 관리 (통과)
    solution_mine_five : Counter + younger set + older_type_count 정수 관리 (통과)

[개선 포인트]
    solution_mine_one  : O(N²) → 시간 초과, 학습 목적
    solution_mine_two  : sum(제너레이터) O(K) 병목 → older_type_count로 해결 필요
    solution_mine_three: Counter로 딕셔너리 초기화 개선, sum(제너레이터) 병목 미해결
    solution_mine_four : 개선 필요 없음 - Sub
                         older_type_count 정수 관리로 핵심 병목 해결
    solution_mine_five : 개선 필요 없음 - Best
                         Counter + older_type_count 조합으로 최적화
================================================================================
[복잡도 분석]
    N = len(topping) (최대 1,000,000)
    K = 토핑 종류 수 (최대 10,000)

    Mine_one   - 시간: O(N²)   | 공간: O(N) - 슬라이싱 + set 변환 × N번
    Mine_two   - 시간: O(N×K)  | 공간: O(N) - sum(제너레이터) O(K) × N번
    Mine_three - 시간: O(N×K)  | 공간: O(N) - Counter 초기화 개선, 병목 미해결
    Mine_four  - 시간: O(N)    | 공간: O(N) - older_type_count O(1) 갱신
    Mine_five  - 시간: O(N)    | 공간: O(N) - Mine_four와 동일, Counter 추가
    Best       - 시간: O(N)    | 공간: O(N) - Mine_five와 동일
    Sub        - 시간: O(N)    | 공간: O(N) - Mine_four와 동일
"""

import time
from collections import Counter


# ================================================================================
# Mine solution one - 슬라이싱 + set 변환 (시간 초과)
# ================================================================================
def solution_mine_one(topping: list[int]) -> int:
    """
    매 위치마다 슬라이싱하고 set으로 종류 수를 비교하는 초기 풀이 (시간 초과)

    핵심:
        topping[:i]: 왼쪽 조각 → set으로 종류 수 계산
        topping[i:]: 오른쪽 조각 → set으로 종류 수 계산
        len(set) 비교

    시간 초과 원인:
        매 루프마다 슬라이싱 O(N) + set 변환 O(N) × N번 → O(N²)
        N=1,000,000에서 1조 연산 → 시간 초과
    """
    answer = 0

    for i in range(1, len(topping)):
        if len(set(topping[:i])) == len(set(topping[i:])):
            answer += 1

    return answer


# ================================================================================
# Mine solution two - older 딕셔너리 + sum(제너레이터) (시간 초과)
# ================================================================================
def solution_mine_two(topping: list[int]) -> int:
    """
    포인터 방식으로 older/younger를 관리하나 sum(제너레이터)로 시간 초과

    개선 방향 발견:
        older 전체 시작, younger 비어서 시작
        한 개씩 younger로 넘기며 양측 종류 수 갱신

    시간 초과 원인:
        sum(1 for v in older.values() if v != 0): O(K) × N번 = O(N×K)
        K=10,000, N=1,000,000 → 최대 100억 연산
        딕셔너리 초기화 for문: O(N) 1회 → 병목 아님
    """
    answer = 0
    older = {}
    younger = set()

    for t in topping:
        older[t] = older.get(t, 0) + 1

    for t in topping:
        younger.add(t)
        older[t] -= 1

        if len(younger) == sum(1 for v in older.values() if v != 0):
            answer += 1

    return answer


# ================================================================================
# Mine solution three - Counter + sum(제너레이터) (시간 초과)
# ================================================================================
def solution_mine_three(topping: list[int]) -> int:
    """
    Counter로 딕셔너리 초기화를 개선했으나 sum(제너레이터) 병목 미해결

    mine_two 대비:
        딕셔너리 초기화 for문 → Counter(topping) C 레벨 구현
        초기화 속도는 개선되나 핵심 병목인 sum(제너레이터) O(K) 미해결
        → 시간 초과 동일 발생
    """
    answer = 0
    older = Counter(topping)
    younger = set()

    for t in topping:
        younger.add(t)
        older[t] -= 1

        if len(younger) == sum(1 for v in older.values() if v != 0):
            answer += 1

    return answer


# ================================================================================
# Mine solution four - older 딕셔너리 + older_type_count 정수 관리 (통과)
# ================================================================================
def solution_mine_four(topping: list[int]) -> int:
    """
    older_type_count 정수 변수로 sum(제너레이터) 병목을 O(1)로 대체 (통과)

    핵심 개선:
        sum(1 for v in older.values() if v != 0): O(K)
        → older_type_count 정수 변수로 대체: O(1)

    older_type_count 갱신 조건:
        older[t] -= 1 후 older[t] == 0이면 해당 토핑이 older에서 사라짐
        → older_type_count -= 1

    O(N) 달성:
        딕셔너리 초기화: O(N) 1회
        순회: O(N) × O(1) 갱신 = O(N)
        전체: O(N)
    """
    answer = 0
    older = {}
    younger = set()

    for t in topping:
        older[t] = older.get(t, 0) + 1

    older_type_count = len(older)

    for t in topping:
        younger.add(t)
        older[t] -= 1

        if older[t] == 0:
            older_type_count -= 1      # 해당 토핑 older에서 소멸 → 종류 수 감소

        if len(younger) == older_type_count:
            answer += 1

    return answer


# ================================================================================
# Mine solution five - Counter + older_type_count 정수 관리 (통과)
# ================================================================================
def solution_mine_five(topping: list[int]) -> int:
    """
    Counter + older_type_count로 mine_three와 mine_four를 통합한 풀이 (통과)

    mine_four 대비:
        딕셔너리 초기화 for문 → Counter(topping) C 레벨 구현
        나머지 로직 동일

    Counter 특성:
        없는 키 접근 시 0 반환 → KeyError 없음
        older[t] -= 1 후 값 0이 되어도 키 유지
        이 문제에서 topping 순서대로 순회하므로 존재 키만 접근 → 안전
    """
    answer = 0
    older = Counter(topping)
    younger = set()
    older_type_count = len(older)

    for t in topping:
        younger.add(t)
        older[t] -= 1

        if older[t] == 0:
            older_type_count -= 1

        if len(younger) == older_type_count:
            answer += 1

    return answer


# ================================================================================
# Best solution - Counter + older_type_count (mine_five 주석 보강)
# ================================================================================
def solution_best(topping: list[int]) -> int:
    """
    Counter + older_type_count로 O(N) 시간에 공평한 자르기 수를 구하는 최적 풀이

    mine_five와 동일한 로직, 선정 근거 주석 보강:
        Counter: C 레벨 구현으로 딕셔너리 초기화보다 빠름
        older_type_count: sum(제너레이터) O(K) → O(1) 정수 갱신으로 핵심 병목 해결
        전체 O(N): Counter O(N) + 순회 O(N) × O(1) 갱신

    포인터 방식:
        older: 전체에서 시작 → 한 개씩 감소
        younger: 비어서 시작 → 한 개씩 증가
        양측 종류 수를 O(1)로 추적
    """
    answer = 0
    older = Counter(topping)
    younger = set()
    older_type_count = len(older)

    for t in topping:
        younger.add(t)
        older[t] -= 1

        if older[t] == 0:
            older_type_count -= 1

        if len(younger) == older_type_count:
            answer += 1

    return answer


# ================================================================================
# Sub solution - older 딕셔너리 + older_type_count (mine_four 주석 보강)
# ================================================================================
def solution_sub(topping: list[int]) -> int:
    """
    직접 딕셔너리 초기화 + older_type_count로 동작 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        Counter 없이 딕셔너리를 직접 초기화 → 초기화 과정이 코드에 드러남
        older.get(t, 0) + 1: Counter의 동작을 직접 구현
        나머지 로직 동일, older_type_count로 핵심 병목 해결
        O(N) 동일
    """
    answer = 0
    older = {}
    younger = set()

    for t in topping:
        older[t] = older.get(t, 0) + 1

    older_type_count = len(older)

    for t in topping:
        younger.add(t)
        older[t] -= 1

        if older[t] == 0:
            older_type_count -= 1

        if len(younger) == older_type_count:
            answer += 1

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int]] = [
        # (topping, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [1,2,1,3,1,4,1,2]:
        #   t=3 위치에서 [1,2,1,3] vs [1,4,1,2] → 3 vs 3 ✓
        #   t=5 위치에서 [1,2,1,3,1] vs [4,1,2] → 3 vs 3 ✓
        #   → 2
        ([1, 2, 1, 3, 1, 4, 1, 2], 2),
        # [1,2,3,1,4]: 공평하게 자를 수 없음 → 0
        ([1, 2, 3, 1, 4], 0),
        # 추가 케이스:
        # 모두 동일 → 자르는 모든 위치에서 양측이 {1} → N-1
        ([1, 1, 1], 2),
        # 단일 원소 → 자를 수 없음 (range(1,1) 비어있음) → 0
        ([1], 0),
        # 딱 반씩 → 1
        ([1, 2], 1),
    ]

    solutions = [
        ("Mine_one   (슬라이싱+set) ", solution_mine_one),
        ("Mine_two   (dict+sum_gen) ", solution_mine_two),
        ("Mine_three (Counter+gen)  ", solution_mine_three),
        ("Mine_four  (dict+int카운터)", solution_mine_four),
        ("Mine_five  (Counter+int)  ", solution_mine_five),
        ("Best       (Counter+int)  ", solution_best),
        ("Sub        (dict+int카운터)", solution_sub),
    ]

    # 워밍업 스텝
    _t, _ = test_cases[0]
    for _, func in solutions:
        func(_t[:])

    print("=" * 68)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (topping, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(topping[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
