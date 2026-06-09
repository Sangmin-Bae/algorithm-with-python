"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 소수 만들기
    유형       : Math / Combination
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12977
    풀이일자   : 2026-06-08
===================================================================================
[문제 요약]
    nums 배열에서 서로 다른 3개를 골라 합산했을 때
    그 합이 소수인 경우의 수를 반환

    제약 조건
        - 3 ≤ len(nums) ≤ 50
        - 1 ≤ nums[i] ≤ 1,000
        - 최대 조합 수: C(50,3) = 19,600 → 완전 탐색 가능
        - 합의 최댓값: 1,000 × 3 = 3,000 → isqrt(3000) ≈ 55 이내 판별
===================================================================================
[입출력 예시]
    nums          | result
    --------------|-------
    [1,2,3,4]     | 1      (조합: (1,2,4)=7 소수, 나머지 비소수)
    [1,2,7,6,4]   | 4      (소수인 합: 4가지)
===================================================================================
[내 초기 풀이]
    solution_zero : itertools.combinations 라이브러리 활용 (초기 시도)
    solution_one  : combinations_one (재귀 + 리스트 누적) 활용
    solution_two  : combinations_two (재귀 + yield from 제너레이터) 활용
    solution_three: combinations_three (재귀 + 슬라이싱) 활용

    공통 구조:
        직접 구현한 combinations 함수 또는 itertools로 3개 조합 생성
        → 각 조합의 합에 is_prime() 적용
        → 소수인 경우 카운트

[개선 포인트]
    combinations_one/two: arr.index(chosen[-1])는 O(N) 순차 탐색
                            중복 원소 입력 시 항상 첫 번째 위치 반환 → 잘못된 start 가능
                            → start 인덱스를 파라미터로 직접 전달하는 방식으로 개선
                            → combinations_four에서 개선 구현
    combinations_three: arr[i+1:] 슬라이싱으로 중복 원소 없이 자연스럽게 제거
                        → arr.index() 미사용, 안전하나 매 재귀마다 새 리스트 생성
    combinations_four: start 인덱스를 generate() 파라미터로 직접 전달
                        → arr.index() 제거, O(N) 탐색 → O(1)
                        → 중복 원소 입력에도 안전 + 슬라이싱 공간 비용 없음
    is_prime: n < 2 가드 없음 → n=1 입력 시 True 반환 (이 문제 합 최솟값=6 이라 통과)
                범용 함수로 사용 시 if n < 2: return False 가드 필요
===================================================================================
[소수 판별 - math.isqrt() 최적화]
    약수 쌍 성질: N의 약수 쌍 (a, b)에서 a × b = N이면 min(a,b) ≤ √N
    → 2 ~ √N 범위만 나눠보면 약수 존재 여부 완전 판별 가능

    is_prime 손 추적:
        n=7: isqrt(7)=2, range(2,3) → i=2: 7%2=1 → True  (소수)
        n=9: isqrt(9)=3, range(2,4) → i=2: 9%2=1, i=3: 9%3=0 → False (비소수)
        n=1: isqrt(1)=1, range(2,2) → 루프 미실행 → True  (버그: 1은 소수 아님)
                → 이 문제 합 최솟값=1+2+3=6 이라 실제 n=1 미입력, 통과
===================================================================================
[combinations 구현 방식 비교]
    combinations_one (재귀 + 리스트 누적):
        모든 조합을 cases 리스트에 담아 한 번에 반환
        arr.index(chosen[-1]): O(N) 순차 탐색, 중복 원소 입력 시 취약
        결과를 여러 번 재사용하는 경우에 유리

    combinations_two (재귀 + yield from 제너레이터):
        조합을 하나씩 yield → 현재 조합 1개만 메모리에 유지
        yield from: 재귀 호출로 생성된 제너레이터 객체를 내부 순회해 값을 위로 전달
                    (yield만 쓰면 제너레이터 객체 자체가 yield되어 값 미전달)
        arr.index() 문제 그대로 보유

    combinations_three (재귀 + 슬라이싱):
        arr[i+1:]을 넘겨 이미 선택된 앞 원소를 후보에서 자연스럽게 제거
        arr.index() 미사용 → 중복 원소 입력에도 안전
        단, 매 재귀마다 슬라이싱으로 새 리스트 생성 → 공간 비용 발생

    combinations_four (재귀 + 인덱스 파라미터 직접 전달):
        combinations_two의 arr.index() 문제를 개선한 버전
        start 인덱스를 generate() 파라미터로 직접 전달
        → 값으로 인덱스를 역추적하지 않음 → O(N) 탐색 제거, O(1) 접근
        → 중복 원소 입력에도 안전 + 슬라이싱 공간 비용 없음
        제너레이터 구조 유지 → 공간 O(R)
===================================================================================
[복잡도 분석]
    N = len(nums) (최대 50)
    S = 합의 최댓값 = 3,000

    조합 수: C(N,3) = N(N-1)(N-2)/6
    is_prime: O(√S) ≈ O(55) ≈ O(1)
    전체 시간: O(C(N,3) × √S) ≈ O(N³)
    N=50: C(50,3) = 19,600 × 55 ≈ 1,078,000번 연산 → 충분히 통과

    solution_zero   - 시간: O(N³) | 공간: O(1)        - C 레벨 구현, 조합 객체 1개씩
    solution_one    - 시간: O(N³) | 공간: O(C(N,3))   - 전체 조합 리스트 메모리 보유
    solution_two    - 시간: O(N³) | 공간: O(R)        - 재귀 깊이 R=3, 조합 1개씩
    solution_three  - 시간: O(N³) | 공간: O(R²)       - 매 재귀 슬라이싱 새 리스트 생성
    solution_four   - 시간: O(N³) | 공간: O(R)        - 인덱스 직접 전달, arr.index() 제거
    Best            - 시간: O(N³) | 공간: O(1)        - solution_zero와 동일, 주석 보강
    Sub             - 시간: O(N³) | 공간: O(R)        - solution_four와 동일, 선정 근거 보강
"""

import math
import time
from itertools import combinations
from typing import Iterator, List, Tuple


# =================================================================================
# 공통 헬퍼 - 소수 판별
# =================================================================================
def is_prime(n: int) -> bool:
    """
    2 ~ √n 범위의 수로 나누어 소수 여부를 판별

    math.isqrt(n): 정수 제곱근 (float 오차 없음)
    범용 사용 시 n < 2 가드 필요:
        이 문제 합 최솟값 = 1+2+3 = 6 이므로 n=1 미입력, 가드 없이 통과
    """
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True


# =================================================================================
# combinations_one - 재귀 + 리스트 누적
# =================================================================================
def combinations_one(arr: List[int], r: int) -> List[List[int]]:
    """
    재귀 + 리스트 누적 방식으로 조합을 생성하는 함수

    핵심:
        len(chosen) == r: 원하는 깊이 도달 시 cases에 복사본 저장
        start = arr.index(chosen[-1]) + 1: 현재 값 이후 인덱스부터 탐색 (중복 제거)

    주의:
        arr.index(chosen[-1]): O(N) 순차 탐색
        중복 원소 입력 시 항상 첫 번째 위치를 반환 → 잘못된 start 가능
        → combinations_four에서 인덱스 직접 전달 방식으로 개선
    """
    arr = sorted(arr)
    cases = []

    def generate(chosen: List[int]) -> None:
        if len(chosen) == r:
            cases.append(chosen[:])    # 현재 조합 복사본 저장
            return

        start = arr.index(chosen[-1]) + 1 if chosen else 0  # 값으로 인덱스 역추적 (취약)

        for i in range(start, len(arr)):
            chosen.append(arr[i])
            generate(chosen)
            chosen.pop()               # 백트래킹: 이전 상태로 복원

    generate([])
    return cases


# =================================================================================
# combinations_two - 재귀 + yield from 제너레이터
# =================================================================================
def combinations_two(arr: List[int], r: int) -> Iterator[List[int]]:
    """
    재귀 + yield from 제너레이터 방식으로 조합을 하나씩 생성하는 함수

    combinations_one 대비:
        모든 조합을 리스트에 보관하지 않고 하나씩 yield
        → 현재 조합 1개만 메모리에 유지, 한 번만 순회하는 경우 메모리 효율 우위

    yield from 역할:
        yield generate(chosen): 제너레이터 객체 자체를 yield → 값 미전달
        yield from generate(chosen): 제너레이터 내부를 순회하며 값을 위로 전달
        재귀 구조에서 중간 제너레이터를 거쳐 최상위 호출자까지 값이 도달

    주의:
        arr.index() 문제를 combinations_one과 동일하게 보유
        → combinations_four에서 개선
    """
    arr = sorted(arr)

    def generate(chosen: List[int]) -> Iterator[List[int]]:
        if len(chosen) == r:
            yield chosen[:]            # 현재 조합 복사본 yield
            return

        start = arr.index(chosen[-1]) + 1 if chosen else 0  # 값으로 인덱스 역추적 (취약)

        for i in range(start, len(arr)):
            chosen.append(arr[i])
            yield from generate(chosen)  # 재귀 제너레이터 내부 순회 후 값 전달
            chosen.pop()

    yield from generate([])


# =================================================================================
# combinations_three - 재귀 + 슬라이싱
# =================================================================================
def combinations_three(arr: List[int], r: int) -> Iterator[List[int]]:
    """
    재귀 + 슬라이싱으로 앞 원소를 고정하며 조합을 생성하는 함수

    combinations_one/two 대비:
        arr[i+1:]을 넘겨 이미 선택된 앞 원소를 후보에서 자연스럽게 제거
        arr.index() 미사용 → 중복 원소 입력에도 안전

    손 추적 ([1,2,3,4], r=3):
        i=0, arr[0]=1 고정 → combinations_three([2,3,4], 2)
            i=0, arr[0]=2 고정 → combinations_three([3,4], 1)
                i=0: yield [3] → [1]+[2]+[3] = [1,2,3]
                i=1: yield [4] → [1]+[2]+[4] = [1,2,4]
            i=1, arr[1]=3 고정 → combinations_three([4], 1)
                i=0: yield [4] → [1]+[3]+[4] = [1,3,4]
        i=1, arr[1]=2 고정 → combinations_three([3,4], 2)
                → [2,3,4]

    단점:
        arr[i+1:] 슬라이싱이 매 재귀마다 새 리스트 생성 → 공간 비용 O(R²)
    """
    for i in range(len(arr)):
        if r == 1:
            yield [arr[i]]             # 기저 조건: 원소 1개 yield
        else:
            for j in combinations_three(arr[i + 1:], r - 1):  # 나머지 r-1개 재귀
                yield [arr[i]] + j     # 현재 원소 + 재귀 결과 연결


# =================================================================================
# combinations_four - 재귀 + 인덱스 파라미터 직접 전달 (combinations_two 개선)
# =================================================================================
def combinations_four(arr: List[int], r: int) -> Iterator[List[int]]:
    """
    start 인덱스를 generate() 파라미터로 직접 전달해 arr.index() 문제를 개선한 함수

    combinations_two 대비 개선:
        기존: start = arr.index(chosen[-1]) + 1
                → chosen[-1] 값으로 arr에서 인덱스를 역추적 → O(N) 순차 탐색
                → 중복 원소 존재 시 항상 첫 번째 위치 반환 → 잘못된 start

        개선: generate(start, chosen) → start를 파라미터로 직접 전달
                → 값 역추적 불필요 → O(1) 접근
                → 중복 원소 입력에도 항상 정확한 인덱스 유지

    손 추적 ([1,1,1], r=3):
        generate(0, []):
            i=0: chosen=[1], generate(1, [1])
                i=1: chosen=[1,1], generate(2, [1,1])
                    i=2: chosen=[1,1,1] → len==r → yield [1,1,1] ✓
                chosen=[1]
            i=1: chosen=[1], generate(2, [1])
                i=2: chosen=[1,1], generate(3, [1,1])
                    range(3,3) → 루프 미실행
                chosen=[1]
            i=2: chosen=[1], generate(3, [1])
                range(3,3) → 루프 미실행
        → yield [1,1,1] 1회만 생성 ✓  (combinations_two는 12회 중복 생성)

    combinations_three 대비:
        슬라이싱 없이 인덱스 직접 전달 → 매 재귀마다 새 리스트 생성 없음
        공간: O(R²) → O(R)
    """
    arr = sorted(arr)

    def generate(start: int, chosen: List[int]) -> Iterator[List[int]]:
        if len(chosen) == r:
            yield chosen[:]                    # 현재 조합 복사본 yield
            return

        for i in range(start, len(arr)):
            chosen.append(arr[i])
            yield from generate(i + 1, chosen) # i+1을 직접 전달 → 역추적 불필요
            chosen.pop()                        # 백트래킹: 이전 상태로 복원

    yield from generate(0, [])


# =================================================================================
# solution_zero - itertools.combinations (초기 시도)
# =================================================================================
def solution_zero(nums: List[int]) -> int:
    """
    itertools.combinations 라이브러리로 3개 조합을 생성하는 초기 풀이

    itertools.combinations:
        C 레벨 구현으로 직접 구현 대비 가장 빠름
        실무에서 조합이 필요할 때 최우선 선택
    """
    answer = 0

    for i in combinations(nums, 3):
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# solution_one - combinations_one 활용
# =================================================================================
def solution_one(nums: List[int]) -> int:
    """combinations_one (재귀 + 리스트 누적)으로 조합 생성"""
    answer = 0

    for i in combinations_one(nums, 3):
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# solution_two - combinations_two 활용
# =================================================================================
def solution_two(nums: List[int]) -> int:
    """combinations_two (재귀 + yield from)으로 조합 생성"""
    answer = 0

    for i in combinations_two(nums, 3):
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# solution_three - combinations_three 활용
# =================================================================================
def solution_three(nums: List[int]) -> int:
    """combinations_three (재귀 + 슬라이싱)으로 조합 생성"""
    answer = 0

    for i in combinations_three(nums, 3):
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# solution_four - combinations_four 활용 (arr.index 개선)
# =================================================================================
def solution_four(nums: List[int]) -> int:
    """combinations_four (인덱스 직접 전달)으로 조합 생성"""
    answer = 0

    for i in combinations_four(nums, 3):
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# Best solution - itertools.combinations (solution_zero 주석 보강)
# =================================================================================
def solution_best(nums: List[int]) -> int:
    """
    itertools.combinations로 3개 조합을 생성하는 최적 풀이

    solution_zero와 동일한 로직, 선정 근거 주석 보강:
        itertools.combinations: CPython C 레벨 구현
            → Python 재귀 구현(one~four) 대비 함수 호출 오버헤드 없음
            → 동일 O(N³) 시간복잡도지만 상수 인자가 가장 작음
        조합 객체를 하나씩 yield → 전체 리스트 메모리 보유 없음 (공간 O(1))
        실무에서 조합이 필요한 모든 경우의 최우선 선택
    """
    answer = 0

    for i in combinations(nums, 3):     # C 레벨 조합 생성, 하나씩 yield
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# Sub solution - combinations_four (인덱스 직접 전달)
# =================================================================================
def solution_sub(nums: List[int]) -> int:
    """
    직접 구현한 combinations 중 combinations_four (개선 버전)를 활용하는 서브 풀이

    직접 구현 네 방식(one~four) 중 선정 근거:
        combinations_one/two (arr.index) 대비:
            start 인덱스를 파라미터로 직접 전달 → O(N) 역추적 제거
            중복 원소 입력에도 항상 정확한 조합 생성
        combinations_three (슬라이싱) 대비:
            매 재귀마다 슬라이싱으로 새 리스트 생성하지 않음
            공간: O(R²) → O(R)
        제너레이터 구조 유지 → 한 번만 순회하는 이 문제에서 메모리 효율 우위
    """
    answer = 0

    for i in combinations_four(nums, 3): # 인덱스 직접 전달: 안전 + 효율
        if is_prime(sum(i)):
            answer += 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], int]] = [
        # (nums, 기댓값)
        # 손 추적:
        # [1,2,3,4]: C(4,3)=4가지
        #   (1,2,3)=6  → 6%2=0 → False
        #   (1,2,4)=7  → isqrt(7)=2, 7%2=1 → True
        #   (1,3,4)=8  → 8%2=0 → False
        #   (2,3,4)=9  → 9%3=0 → False
        #   → 정답 1
        ([1, 2, 3, 4],   1),
        # [1,2,7,6,4]: C(5,3)=10가지
        #   (1,2,7)=10 → False, (1,2,6)=9 → False, (1,2,4)=7 → True
        #   (1,7,6)=14 → False, (1,7,4)=12 → False, (1,6,4)=11 → True
        #   (2,7,6)=15 → False, (2,7,4)=13 → True
        #   (2,6,4)=12 → False, (7,6,4)=17 → True
        #   → 정답 4
        ([1, 2, 7, 6, 4], 4),
        # [2,4,6]: C(3,3)=1가지
        #   (2,4,6)=12 → 12%2=0 → False → 정답 0
        ([2, 4, 6],       0),
        # [3,5,7]: 합=15 → 15%3=0 → False → 정답 0
        ([3, 5, 7],       0),
        # [1,1,1]: 중복 원소 — combinations_one/two 취약 케이스
        #   C(3,3) 정상이면 조합 1개: (1,1,1)=3 → isqrt(3)=1, range(2,2) 미실행 → True
        #   → 정답 1
        #   combinations_one/two: arr.index(1) 항상 0 반환 → start 오류 → 중복 생성
        #   combinations_three/four: 안전하게 1개만 생성 → 정상 동작
        ([1, 1, 1],       1),
    ]

    solutions = [
        ("Zero  (itertools)      ", solution_zero),
        ("One   (재귀+리스트)    ", solution_one),
        ("Two   (재귀+yield)     ", solution_two),
        ("Three (재귀+슬라이싱)  ", solution_three),
        ("Four  (인덱스직접전달) ", solution_four),
        ("Best  (itertools)      ", solution_best),
        ("Sub   (인덱스직접전달) ", solution_sub),
    ]

    print("=" * 70)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (nums, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(nums[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
