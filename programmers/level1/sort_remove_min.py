"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 제일 작은 수 제거하기
    유형       : Sort
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12935
    풀이일자   : 2026-06-19
===================================================================================
[문제 요약]
    arr에서 가장 작은 수를 제거한 배열 반환
    결과가 빈 배열이면 [-1] 반환

    제약 조건
        - arr 길이: 1 이상 (최대 제약 없음)
        - arr[i] ≠ arr[j] (i ≠ j): 모든 원소 서로 다름 (중복 없음)
        → min()으로 찾은 값이 배열에서 정확히 한 번만 등장
        → remove(), index() 모두 안전하게 동작
===================================================================================
[입출력 예시]
    arr       | return
    ----------|-------
    [4,3,2,1] | [4,3,2]  (최솟값 1 제거)
    [10]      | [-1]     (원소 1개 → 제거 후 빈 배열 → [-1])
===================================================================================
[내 초기 풀이]
    solution_mine_one  : list.remove(min(arr)) — 값으로 직접 제거, 원본 수정
    solution_mine_two  : list.pop(arr.index(min(arr))) — 인덱스로 제거, 원본 수정
    solution_mine_three: min 1회 저장 + 리스트 컴프리헨션 — 새 리스트 생성
    solution_mine_four : min 인덱스 + 슬라이싱 결합 — 새 리스트 생성
    solution_mine_five : walrus + is not None + 삼항 연산자 한 줄 표현

[개선 포인트]
    solution_mine_one/two:
        원본 arr을 직접 수정 (remove, pop은 in-place 연산)
        solution_comparison()에서 arr[:]로 복사본 전달해야 정확한 검증 가능

    solution_mine_three: 개선 필요 없음 - Best
        m = min(arr) 1회 저장 → 컴프리헨션 내 min 반복 호출(O(N²)) 방지
        원본 보존, 의도 명확

    solution_mine_five:
        반환 타입 힌트: int | None | list[int] → 실제로는 항상 List[int]만 반환
            len(arr) > 1: [x for x in arr if x != m] → list
            len(arr) <= 1: [-1] → list
        is not None 필요 이유:
            (m := min(arr)) and [...]: m=0이면 0은 falsy → 단락 평가로 [...] 미실행
            (m := min(arr)) is not None and [...]: m=0이어도 True → 정상 동작
            이 문제 arr 원소 범위 명시 없음 → 0 포함 가능 → is not None 필수
===================================================================================
[구현 방식별 원본 수정 여부 비교]
    원본 수정 (in-place):
        list.remove(value): 첫 번째 일치 원소 제거, O(N) 탐색+이동
        list.pop(index)   : 인덱스 위치 원소 제거, O(N) 이동

    새 리스트 생성:
        리스트 컴프리헨션: 조건 만족 원소만 담은 새 리스트
        슬라이싱 결합    : arr[:idx] + arr[idx+1:] → 중간 객체 2개 생성

    원본 보존 여부:
        solution_mine_one/two: arr 원본 수정됨
        solution_mine_three/four/five: arr 원본 보존
===================================================================================
[walrus 연산자 (:=) 와 is not None 패턴]
    walrus 연산자 (Python 3.8+):
        m = min(arr): 문장(statement) → 조건문/단락 평가 항으로 사용 불가
        (m := min(arr)): 표현식(expression) → 값을 m에 바인딩하면서 m 자체를 반환

    0 포함 엣지케이스:
        (m := 0) and [...]: 0은 falsy → 단락 평가로 [...] 미실행, 0 반환 (오류)
        (m := 0) is not None and [...]: 0 is not None = True → [...] 정상 실행

    min(arr)이 None을 반환하는 경우:
        arr이 비어있지 않은 한 절대 None 반환 불가
        len(arr) > 1 조건이 True인 시점에서 arr은 항상 비어있지 않음
        → is not None은 항상 True이나, 0 포함 케이스에서 falsy 방지 목적으로 필요

    [x for x in arr if x != (m := min(arr))] 대안:
        walrus를 컴프리헨션 if 조건에서 사용
        if 절은 매 원소마다 평가 → (m := min(arr))도 N번 실행 → O(N²)
        결과는 맞지만 min()이 N번 호출되는 비효율 발생
        명시적 m = min(arr) 방식보다 성능 열위, 사용 지양
===================================================================================
[복잡도 분석]
    N = len(arr)

    Mine_one   - 시간: O(N) | 공간: O(1)  - min O(N) + remove O(N), 원본 수정
    Mine_two   - 시간: O(N) | 공간: O(1)  - min O(N) + index O(N) + pop O(N)
    Mine_three - 시간: O(N) | 공간: O(N)  - min O(N) + 컴프리헨션 O(N)
    Mine_four  - 시간: O(N) | 공간: O(N)  - min O(N) + index O(N) + 슬라이싱 O(N)
    Mine_five  - 시간: O(N) | 공간: O(N)  - min O(N) + 컴프리헨션 O(N)
    Best       - 시간: O(N) | 공간: O(N)  - Mine_three와 동일, 주석 보강
    Sub        - 시간: O(N) | 공간: O(1)  - Mine_one과 동일, 주석 보강

    min() 반복 호출 주의:
        [x for x in arr if x != min(arr)]: min이 N번 호출 → O(N²)
        m = min(arr) 1회 저장 후 사용 → O(N) (이 문제는 최대 길이 제약 없음)
"""

import time
from typing import List, Tuple


# =================================================================================
# Mine solution one - list.remove(min(arr))
# =================================================================================
def solution_mine_one(arr: List[int]) -> List[int]:
    """
    list.remove()로 최솟값을 직접 제거하는 초기 풀이

    핵심:
        list.remove(value): 첫 번째 일치 원소를 찾아 제거
        중복 없음 보장 → remove()가 항상 정확한 위치 제거
        원본 arr을 in-place 수정 → 반환된 arr과 원본이 동일 객체

    개선 가능:
        원본 수정이 문제가 되는 상황에서는 arr[:]으로 복사 후 사용
    """
    if len(arr) <= 1:
        return [-1]

    arr.remove(min(arr))    # min O(N) + remove O(N) 탐색+이동
    return arr


# =================================================================================
# Mine solution two - list.pop(arr.index(min(arr)))
# =================================================================================
def solution_mine_two(arr: List[int]) -> List[int]:
    """
    index()로 위치를 찾고 pop()으로 제거하는 풀이

    mine_one 대비 특징:
        index()로 최솟값 인덱스를 먼저 확인 → pop()으로 인덱스 제거
        mine_one(remove)보다 단계가 명시적이나 복잡도 동일 O(N)
        원본 arr을 in-place 수정
    """
    if len(arr) <= 1:
        return [-1]

    arr.pop(arr.index(min(arr)))    # index O(N) + pop O(N)
    return arr


# =================================================================================
# Mine solution three - min 1회 + 리스트 컴프리헨션
# =================================================================================
def solution_mine_three(arr: List[int]) -> List[int]:
    """
    min을 1회만 계산하고 컴프리헨션으로 새 리스트를 생성하는 풀이

    핵심:
        m = min(arr): 최솟값 1회만 계산, 변수에 저장
        [x for x in arr if x != m]: m을 제외한 원소만 담은 새 리스트
        원본 arr 보존

    min 반복 호출 방지:
        [x for x in arr if x != min(arr)]: min이 N번 호출 → O(N²)
        m = min(arr) 1회 저장 → O(N)
        최대 길이 제약 없는 이 문제에서 중요한 판단
    """
    if len(arr) <= 1:
        return [-1]

    m = min(arr)                        # 최솟값 1회 계산
    return [x for x in arr if x != m]  # m 제외 새 리스트 생성


# =================================================================================
# Mine solution four - min 인덱스 + 슬라이싱 결합
# =================================================================================
def solution_mine_four(arr: List[int]) -> List[int]:
    """
    최솟값 인덱스를 기준으로 슬라이싱을 결합하는 풀이

    핵심:
        idx = arr.index(min(arr)): 최솟값의 인덱스
        arr[:idx] + arr[idx+1:]: 인덱스 앞뒤를 잘라 이어붙이기
        슬라이싱 2회 → 중간 객체 2개 생성 후 결합
        원본 arr 보존
    """
    if len(arr) <= 1:
        return [-1]

    idx = arr.index(min(arr))       # 최솟값 인덱스
    return arr[:idx] + arr[idx + 1:]    # 앞뒤 슬라이싱 결합


# =================================================================================
# Mine solution five - walrus + is not None + 삼항 연산자 한 줄
# =================================================================================
def solution_mine_five(arr: List[int]) -> List[int]:
    """
    walrus 연산자, is not None, 삼항 연산자를 조합한 한 줄 표현 풀이

    구조 분해:
        len(arr) > 1이 False → [-1] 반환 (삼항 else 분기)
        len(arr) > 1이 True  → 앞 항 평가:
            (m := min(arr)): walrus로 min(arr) 계산 + m에 바인딩
            is not None: m이 0일 때 falsy로 단락 평가 오류 방지
                0 is not None = True → and 오른쪽 항 실행
            and [x for x in arr if x != m]: 최솟값 제외 리스트 반환

    is not None 필요 이유:
        (m := 0) and [...]: 0은 falsy → 단락 평가로 [...] 미도달, 0 반환
        (m := 0) is not None and [...]: True → 정상적으로 [...] 반환

    반환 타입: 실제로는 항상 List[int]만 반환
    """
    return (m := min(arr)) is not None and [x for x in arr if x != m] if len(arr) > 1 else [-1]


# =================================================================================
# Best solution - min 1회 + 리스트 컴프리헨션 (mine_three 주석 보강)
# =================================================================================
def solution_best(arr: List[int]) -> List[int]:
    """
    min 1회 저장 + 컴프리헨션으로 원본을 보존하며 새 리스트를 생성하는 최적 풀이

    mine_three와 동일한 로직, 근거 주석 보강:
        원본 보존: remove/pop과 달리 arr을 수정하지 않음
        m = min(arr) 1회: 컴프리헨션 내 min 반복 호출 O(N²) 방지
        중복 없음 보장: m이 배열에서 정확히 1번만 등장 → 컴프리헨션 결과 정확
        가독성: 로직이 명확하게 드러남
    """
    if len(arr) <= 1:
        return [-1]

    m = min(arr)
    return [x for x in arr if x != m]  # m 제외, 원본 보존


# =================================================================================
# Sub solution - list.remove(min(arr)) (mine_one 주석 보강)
# =================================================================================
def solution_sub(arr: List[int]) -> List[int]:
    """
    list.remove()로 최솟값을 직접 제거하는 서브 풀이

    Best 대비 특징:
        remove(min(arr)): 한 줄로 최솟값 탐색+제거
        코드 길이가 가장 짧고 의도가 직관적으로 드러남
        원본 arr을 in-place 수정 → 외부에서 arr 재사용 시 주의 필요
        중복 없음 보장 → remove()가 첫 번째 일치 원소만 제거해도 정확
    """
    if len(arr) <= 1:
        return [-1]

    arr.remove(min(arr))
    return arr


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], List[int]]] = [
        # (arr, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [4,3,2,1]: min=1, 제거 → [4,3,2]
        ([4, 3, 2, 1],  [4, 3, 2]),
        # [10]: len=1 → [-1]
        ([10],          [-1]),
        # 추가 케이스:
        # [0,1,2]: min=0, 제거 → [1,2]  (최솟값=0 엣지케이스)
        ([0, 1, 2],     [1, 2]),
        # [5,3]: min=3, 제거 → [5]
        ([5, 3],        [5]),
        # [1,2,3]: min=1, 제거 → [2,3]
        ([1, 2, 3],     [2, 3]),
    ]

    solutions = [
        ("Mine_one  (remove)      ", solution_mine_one),
        ("Mine_two  (pop+index)   ", solution_mine_two),
        ("Mine_three(min+컴프리)  ", solution_mine_three),
        ("Mine_four (index+슬라이)", solution_mine_four),
        ("Mine_five (walrus한줄)  ", solution_mine_five),
        ("Best      (min+컴프리)  ", solution_best),
        ("Sub       (remove)      ", solution_sub),
    ]

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (arr, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr[:])      # 원본 보존을 위해 복사본 전달
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
