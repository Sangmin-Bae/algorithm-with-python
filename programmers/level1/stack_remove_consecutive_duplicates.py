"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 같은 숫자는 싫어
    유형       : Stack
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12906
    풀이일자   : 2026-06-22
===================================================================================
[문제 요약]
    배열 arr에서 연속으로 나타나는 같은 숫자를 하나만 남기고 제거
    순서 유지하여 반환

    제약 조건
        - arr 크기: 1,000,000 이하의 자연수 → 최소 1, 빈 배열 없음
        - 원소: 0 이상 9 이하 정수
        - O(N²) 불가 → O(N) 필요
===================================================================================
[입출력 예시]
    arr             | answer
    ----------------|--------
    [1,1,3,3,0,1,1] | [1,3,0,1]
    [4,4,4,3,3]     | [4,3]
===================================================================================
[부적합한 접근 방식과 그 이유]
    set() 방식:
        list(set(arr)): 전체 중복 제거 + 순서 미보장
        [1,1,3,3,0,1,1] → {0,1,3} → 순서 불보장, 비연속 중복도 제거 → 부적합

    in 비교 방식:
        if i not in answer: answer.append(i)
        순서는 보장되나 비연속 중복 그룹도 제거됨
        [1,1,3,3,0,1,1] → [1,3,0] → 마지막 1 그룹 사라짐 → 부적합

    올바른 접근:
        직전 값(previous)과 현재 값만 비교 → 연속 중복만 제거
        비연속 동일 값 그룹은 별개로 유지

[내 초기 풀이]
    solution_mine_one: previous 변수로 직전 값 추적 + 비교
    solution_mine_two: itertools.groupby로 연속 그룹화 후 key만 추출

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best_algo (코딩테스트 맥락)
        스택 패턴을 직접 구현 → 알고리즘 이해를 코드로 표현
        면접/화이트보드에서 스택 원리로 설명 가능
    solution_mine_two: 개선 필요 없음 - Best_practical (실무/대규모 데이터 맥락)
        groupby: CPython C 레벨 구현 → Python 루프 대비 빠름
        대규모 데이터(N=1,000,000)에서 상수 인자 차이 발생
        간결하고 의도가 명확, 라이브러리 활용이 권장되는 환경에 적합

    Best 분기 기준:
        코딩테스트 맥락과 실무/대규모 맥락에서 최선이 달라지는 경우
        → Best_algo: 코딩테스트, 알고리즘 원리 표현 우선
        → Best_practical: 실무, 성능/간결성 우선
        Sub는 두 Best 모두 별개의 최선이므로 생략
===================================================================================
[스택 유형 분류 근거]
    스택의 핵심: LIFO + top 접근

    이 문제의 스택 패턴:
        현재 값 != 스택 top → push (새 원소)
        현재 값 == 스택 top → 무시 (연속 중복)

    solution_mine_one에서:
        previous = 스택 top 역할 (직전에 추가된 값)
        answer   = 스택 역할 (결과 저장)

    명시적 스택으로 표현하면:
        stack = []
        for i in arr:
            if not stack or stack[-1] != i:
                stack.append(i)
        return stack

    → solution_mine_one이 스택을 previous 변수로 암묵적으로 구현한 것

[groupby 동작 특성]
    itertools.groupby(iterable):
        연속된 동일 값을 하나의 그룹으로 묶어 (key, group_iterator) yield
        정렬 여부와 무관하게 연속성만 기준으로 그룹화

    SQL GROUP BY와의 차이:
        SQL: 전체에서 동일 값 그룹화 (정렬 포함)
        groupby: 연속된 값만 그룹화 → 비연속 동일 값은 별개 그룹

    예시:
        groupby([1,1,3,3,1,1]) → (1,<iter>), (3,<iter>), (1,<iter>)
        → 비연속 1이 두 그룹으로 분리됨 → 이 문제 조건에 정확히 부합
===================================================================================
[예외 처리 기준]
    코딩테스트: 제약 조건이 보장하는 범위 안에서만 동작하면 됨
        arr 최소 크기 1 → 빈 배열 불가 → 예외 처리 불필요
        불필요한 예외 처리는 코드 복잡도만 높임

    실무: 외부 입력일 경우 방어 코드 필요
        if not arr: return []  또는
        if len(arr) == 0: raise ValueError(...)
        맥락에 따라 다른 판단
===================================================================================
[복잡도 분석]
    N = len(arr) (최대 1,000,000)

    Mine_one        - 시간: O(N) | 공간: O(N) - 단일 순회, answer 리스트
    Mine_two        - 시간: O(N) | 공간: O(N) - groupby 단일 순회, key 리스트
    Best_algo       - 시간: O(N) | 공간: O(N) - Mine_one과 동일, 스택 원리 명시
    Best_practical  - 시간: O(N) | 공간: O(N) - Mine_two와 동일, C 레벨 구현

    시간복잡도 동일(O(N))이나 상수 인자 차이:
        Best_algo:       Python 레벨 루프 → 상수 인자 큼
        Best_practical:  C 레벨 groupby → 상수 인자 작음
        N=1,000,000: 두 방식 모두 효율성 통과, 대규모에서 groupby 유리

    N=1,000,000: O(N²) 접근은 10^12 연산 → 시간 초과 확정
    O(N) 풀이만 효율성 테스트 통과 가능
"""

import time
from itertools import groupby
from typing import List, Tuple


# =================================================================================
# Mine solution one - previous 변수로 직전 값 추적
# =================================================================================
def solution_mine_one(arr: List[int]) -> List[int]:
    """
    직전 값(previous)과 현재 값을 비교해 연속 중복을 제거하는 초기 풀이

    핵심:
        previous = arr[0]: 첫 원소로 초기화
        i != previous: 현재 값이 직전 값과 다를 때만 추가
        previous = i: 추가할 때 직전 값 갱신

    스택 관점:
        previous = 스택 top (직전에 추가된 값)
        answer = 스택 (결과)
        현재 값 != top → push, 현재 값 == top → 무시

    빈 배열 예외 처리 불필요:
        제약 조건에서 arr 최소 크기 1 보장 → arr[0] 항상 안전
    """
    previous = arr[0]
    answer = [previous]

    for i in arr[1:]:
        if i != previous:       # 직전 값과 다를 때만 추가 (연속 중복 제거)
            answer.append(i)
            previous = i        # 직전 값 갱신

    return answer


# =================================================================================
# Mine solution two - itertools.groupby 활용
# =================================================================================
def solution_mine_two(arr: List[int]) -> List[int]:
    """
    itertools.groupby로 연속 그룹화 후 key만 추출하는 풀이

    groupby 동작:
        연속된 동일 값을 (key, group_iterator) 쌍으로 yield
        [1,1,3,3,0,1,1] → (1,<iter>), (3,<iter>), (0,<iter>), (1,<iter>)
        k(key)만 취하면 연속 중복이 제거된 순서 보장 리스트

    SQL GROUP BY와의 차이:
        연속된 값만 그룹화 → 비연속 동일 값은 별개 그룹으로 유지
        [1,1,3,3,1,1] → key: 1, 3, 1  (비연속 1은 두 그룹)
    """
    return [k for k, g in groupby(arr)]    # key만 추출, group iterator는 무시


# =================================================================================
# Best_algo solution - previous 변수 방식 (코딩테스트 맥락)
# =================================================================================
def solution_best_algo(arr: List[int]) -> List[int]:
    """
    스택 패턴을 직접 구현한 코딩테스트 맥락 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        스택 top(previous)과 현재 값 비교 → 스택/큐 유형 출제 의도에 부합
        알고리즘 원리를 코드로 직접 표현 → 면접/화이트보드에서 설명 가능
        라이브러리 의존 없이 동작 원리 명확히 드러남

    실무/대규모 맥락에서는 Best_practical(groupby) 선택:
        groupby: CPython C 레벨 구현 → 동일 O(N)이나 상수 인자 작음
        N=1,000,000 규모에서 실질적인 속도 차이 발생 가능
    """
    previous = arr[0]
    answer = [previous]

    for i in arr[1:]:
        if i != previous:
            answer.append(i)    # 직전 값과 다를 때만 추가 (스택 push)
            previous = i        # 스택 top 갱신

    return answer


# =================================================================================
# Best_practical solution - groupby (실무/대규모 데이터 맥락)
# =================================================================================
def solution_best_practical(arr: List[int]) -> List[int]:
    """
    CPython C 레벨 groupby로 간결하게 처리하는 실무/대규모 맥락 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        groupby: CPython C 레벨 구현 → Python 루프보다 상수 인자 작음
        동일 O(N)이나 N=1,000,000 규모에서 실질적 속도 차이 발생 가능
        한 줄 리스트 컴프리헨션으로 간결하게 표현, 의도 명확

    코딩테스트 맥락에서는 Best_algo(previous 방식) 선택:
        스택/큐 유형 출제 의도에 부합
        알고리즘 원리를 직접 표현하는 방식이 평가에 유리

    group iterator(g)는 사용하지 않으므로 _ 관례도 가능:
        [k for k, _ in groupby(arr)]
    """
    return [k for k, g in groupby(arr)]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], List[int]]] = [
        # (arr, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [1,1,3,3,0,1,1]:
        #   1→answer=[1], prev=1
        #   1==prev → skip
        #   3!=prev → answer=[1,3], prev=3
        #   3==prev → skip
        #   0!=prev → answer=[1,3,0], prev=0
        #   1!=prev → answer=[1,3,0,1], prev=1
        #   1==prev → skip → [1,3,0,1]
        ([1, 1, 3, 3, 0, 1, 1], [1, 3, 0, 1]),
        # [4,4,4,3,3]: 4→[4], 4skip, 4skip, 3→[4,3], 3skip → [4,3]
        ([4, 4, 4, 3, 3],       [4, 3]),
        # 추가 케이스:
        # [1]: 원소 1개 → [1]
        ([1],                   [1]),
        # [0,0,0,0]: 모두 동일 → [0]
        ([0, 0, 0, 0],          [0]),
        # [1,2,3,4]: 연속 중복 없음 → 그대로 반환
        ([1, 2, 3, 4],          [1, 2, 3, 4]),
        # [1,1,2,2,1,1]: 비연속 1 보존 → [1,2,1]
        ([1, 1, 2, 2, 1, 1],    [1, 2, 1]),
    ]

    solutions = [
        ("Mine_one       (previous 추적)", solution_mine_one),
        ("Mine_two       (groupby)      ", solution_mine_two),
        ("Best_algo      (previous 추적)", solution_best_algo),
        ("Best_practical (groupby)      ", solution_best_practical),
    ]

    print("=" * 66)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (arr, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()

