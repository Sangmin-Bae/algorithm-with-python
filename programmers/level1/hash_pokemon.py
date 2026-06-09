"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 포켓몬
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/1845
    풀이일자   : 2026-06-09
===================================================================================
[문제 요약]
    nums 배열에서 N/2개의 포켓몬을 선택할 때
    선택한 포켓몬의 종류 수를 최대화해서 반환

    제약 조건
        - 1 ≤ N ≤ 10,000 (N은 항상 짝수)
        - 1 ≤ nums[i] ≤ 200,000
===================================================================================
[입출력 예시]
    nums              | result
    ------------------|-------
    [3,1,2,3,2,4]     | 3      (chose=3, kind=4 → min(3,4)=3)
    [3,3,3,2,2,4]     | 3      (chose=3, kind=3 → min(3,3)=3)
    [3,3,3,2,2,2]     | 2      (chose=3, kind=2 → min(3,2)=2)
===================================================================================
[내 초기 풀이]
    solution_mine: set으로 중복 제거 후 min(chose, kind) 반환

    chose = len(nums) // 2   → 선택 가능한 포켓몬 수
    kind  = len(set(nums))   → 존재하는 포켓몬 종류 수
    return min(chose, kind)

    두 케이스 분석:
        kind > chose: 종류가 충분히 많음 → chose만큼 전부 다른 종류 선택 가능
        kind ≤ chose: 종류가 부족함     → 모든 종류를 선택해도 chose를 못 채움
                                            남은 자리는 중복으로 채워야 함
                                            최대 종류 수 = kind
        → if문 대신 min()으로 두 케이스를 한 번에 표현

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
    solution_sub : Counter 활용 방식 — len(Counter(nums))로 종류 수 산출
                    set 대비 {번호: 개수} 전체를 집계하는 오버스펙
                    단, 해시 자료구조 활용을 코드로 명시적으로 드러냄
===================================================================================
[Hash 유형 분류 근거]
    set(nums)의 내부 구현이 해시 테이블:
        각 원소를 hash() 함수로 버킷 위치 계산 → O(1) 중복 탐지
        중복 원소 발견 시 무시, 새 원소만 추가

    set 변환 내부 동작 (nums=[3,1,2,3,2,4]):
        3 → hash(3) → 버킷에 없음 → 추가
        1 → hash(1) → 버킷에 없음 → 추가
        2 → hash(2) → 버킷에 없음 → 추가
        3 → hash(3) → 이미 있음   → 무시  (O(1) 탐지)
        2 → hash(2) → 이미 있음   → 무시
        4 → hash(4) → 버킷에 없음 → 추가
        결과: {1, 2, 3, 4}

    Counter나 dict로 key-value를 명시적으로 쓰지 않아도
    set 사용 자체가 해시 기반 중복 제거 → 해시 유형 분류의 근거
    Counter는 {번호: 개수}까지 집계하는 오버스펙 → set이 적합
===================================================================================
[복잡도 분석]
    N = len(nums) (최대 10,000)

    Mine - 시간: O(N) | 공간: O(K) - set 변환 O(N), K=고유 원소 수
    Best - 시간: O(N) | 공간: O(K) - Mine과 동일, 주석 보강
    Sub  - 시간: O(N) | 공간: O(K) - Counter 변환 O(N), K=고유 원소 수
                                        set 대비 {번호:개수} 딕셔너리 추가 공간
"""

import time
from collections import Counter
from typing import List, Tuple


# =================================================================================
# Mine solution - set 중복 제거 + min()
# =================================================================================
def solution_mine(nums: List[int]) -> int:
    """
    set으로 종류 수를 구한 뒤 min()으로 최대 선택 가능 종류 수를 반환하는 초기 풀이

    핵심:
        chose = N/2: 선택 가능한 포켓몬 수 (항상 정수, N은 짝수 보장)
        kind = len(set(nums)): 해시 테이블 기반 중복 제거로 종류 수 O(N) 산출
        min(chose, kind): 두 케이스를 if문 없이 한 번에 처리
    """
    chose = len(nums) // 2      # 선택 가능한 포켓몬 수
    kind = len(set(nums))       # 해시 기반 중복 제거로 종류 수 산출
    return min(chose, kind)     # 두 케이스를 min()으로 한 번에 처리


# =================================================================================
# Best solution - Mine 주석 보강
# =================================================================================
def solution_best(nums: List[int]) -> int:
    """
    set 중복 제거 + min()으로 최대 종류 수를 반환하는 최적 풀이

    Mine과 동일한 로직, 근거 주석 보강:
        kind > chose: 종류 충분 → chose 자리를 전부 다른 종류로 채울 수 있음
        kind ≤ chose: 종류 부족 → 모든 종류 선택 후 남은 자리는 중복
                                    최대 종류 수 = kind

        set: 해시 테이블 내부 구현 → 중복 탐지 O(1), 전체 변환 O(N)
        Counter 미사용 이유: {번호: 개수} 집계는 이 문제에 불필요한 오버스펙
                                종류 수(len)만 필요하므로 set이 적합
    """
    chose = len(nums) // 2      # N은 짝수 보장 → // 2 항상 정수
    kind = len(set(nums))       # set: 해시 기반 중복 제거, O(N)
    return min(chose, kind)     # kind>chose → chose, kind≤chose → kind


# =================================================================================
# Sub solution - Counter 활용
# =================================================================================
def solution_sub(nums: List[int]) -> int:
    """
    Counter로 종류 수를 구하는 서브 풀이

    Best 대비 특징:
        Counter(nums): {번호: 개수} 딕셔너리 생성 → 해시 자료구조를 명시적으로 활용
        len(Counter(nums)): key 수 = 고유 원소 수 = 종류 수
        set 대비 {번호: 개수} 값까지 집계하는 오버스펙
            → 이 문제에서 개수 정보는 사용하지 않음
        해시 key-value 구조를 명시적으로 드러내는 학습 목적 풀이로 의미 있음
    """
    chose = len(nums) // 2
    kind = len(Counter(nums))   # Counter key 수 = 고유 원소 수 = 종류 수
    return min(chose, kind)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], int]] = [
        # (nums, 기댓값)
        # 손 추적:
        # [3,1,2,3,2,4]: chose=3, kind=len({1,2,3,4})=4 → min(3,4)=3
        ([3, 1, 2, 3, 2, 4],    3),
        # [3,3,3,2,2,4]: chose=3, kind=len({2,3,4})=3 → min(3,3)=3
        ([3, 3, 3, 2, 2, 4],    3),
        # [1,1]: chose=1, kind=len({1})=1 → min(1,1)=1
        ([1, 1],                 1),
        # [1,2,3,4]: chose=2, kind=len({1,2,3,4})=4 → min(2,4)=2
        ([1, 2, 3, 4],           2),
        # [1,1,1,1,1,1]: chose=3, kind=len({1})=1 → min(3,1)=1
        ([1, 1, 1, 1, 1, 1],    1),
        # [1,2]: chose=1, kind=len({1,2})=2 → min(1,2)=1
        ([1, 2],                 1),
    ]

    solutions = [
        ("Mine (set+min)    ", solution_mine),
        ("Best (set+min)    ", solution_best),
        ("Sub  (Counter+min)", solution_sub),
    ]

    print("=" * 62)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 62)

    for name, func in solutions:
        for idx, (nums, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(nums[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 62)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
