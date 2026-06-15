"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : n^2 배열 자르기
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/87390
    풀이일자   : 2026-06-15
================================================================================
[문제 요약]
    n×n 2차원 배열을 규칙에 따라 채운 뒤 1차원으로 펼쳤을 때
    인덱스 left 이상 right 이하의 원소를 반환

    채우기 규칙:
        i=1,2,...,n에 대해 1행1열~i행i열 영역의 빈 칸을 i로 채움
        → 위치 (행, 열)의 값 = max(행, 열) (1-indexed)

    제약 조건
        - 1 ≤ n ≤ 10^7
        - 0 ≤ left ≤ right < n²
        - right - left < 10^5
================================================================================
[입출력 예시]
    n | left | right | result
    --|------|-------|--------------------
    3 | 2    | 5     | [3,2,2,3]
    4 | 7    | 14    | [4,3,3,3,4,4,4,4]
================================================================================
[핵심 수학 규칙 — 1차원 인덱스 → 원소 값]
    n×n 배열을 1차원으로 펼쳤을 때 인덱스 i의 위치:
        행 (0-indexed) = i // n
        열 (0-indexed) = i % n
        원소 값        = max(행, 열) + 1  (1-indexed 변환)

    손 추적 (n=3):
        인덱스  행      열      원소
        i=0  : 0//3=0, 0%3=0 → max(0,0)+1 = 1
        i=1  : 1//3=0, 1%3=1 → max(0,1)+1 = 2
        i=2  : 2//3=0, 2%3=2 → max(0,2)+1 = 3
        i=3  : 3//3=1, 3%3=0 → max(1,0)+1 = 2
        i=4  : 4//3=1, 4%3=1 → max(1,1)+1 = 2
        i=5  : 5//3=1, 5%3=2 → max(1,2)+1 = 3
        전체: [1,2,3,2,2,3,3,3,3]
        left=2, right=5: [3,2,2,3] ✓

    n=3의 2차원 배열:
        1 2 3   ← 행0: max(0,0)=0, max(0,1)=1, max(0,2)=2 (+1)
        2 2 3   ← 행1: max(1,0)=1, max(1,1)=1, max(1,2)=2 (+1)
        3 3 3   ← 행2: max(2,0)=2, max(2,1)=2, max(2,2)=2 (+1)

    max(a+1, b+1) = max(a, b) + 1 수학적 동치:
        어느 쪽이 크든 1을 더하는 건 동일 → max 밖으로 추출 가능
        solution_two: max(i//n+1, i%n+1)
        solution_three/four: max(i//n, i%n)+1  ← 동일한 결과, 더 간결
================================================================================
[내 초기 풀이]
    solution_mine_one: 이중 for문으로 2차원 배열 생성 후 슬라이싱 (시간 초과)
        n×n 이중 순회로 전체 배열 생성 → n²개 원소 생성
        시간 초과 원인: n=10^7이면 n²=10^14개 생성 → 불가능

    solution_mine_two: 단일 for문 + 수학 연산으로 전체 배열 생성 (시간 초과)
        이중 for문 → 단일 for문으로 상수 개선 시도
        근본 복잡도 O(N²) 유지 → 시간 초과 동일하게 발생
        의의: i//n, i%n으로 행/열을 수학적으로 계산하는 규칙 발견

    solution_mine_three: 필요한 범위만 생성 (통과)
        solution_mine_two의 수학 규칙을 그대로 유지
        range(left, right+1)으로 순회 범위를 필요한 인덱스로 제한
        전체 배열 생성 제거 → O(right-left) = O(10^5) 이내

    solution_mine_four: solution_mine_three를 리스트 컴프리헨션으로 압축 (통과)
        max(i//n, i%n)+1로 더 간결하게 표현

[개선 포인트]
    solution_mine_one/two: 전체 배열 생성이 근본 원인
        n ≤ 10^7 → n² ≤ 10^14 → 생성 자체가 불가능
        제약 조건 확인이 선행되었다면 solution_three 방향으로 바로 접근 가능
    solution_mine_three/four: 개선 필요 없음
================================================================================
[시간 초과 원인 및 풀이 진화]
    제약 조건 핵심:
        n ≤ 10^7 → 전체 배열 n²개 생성 불가 (메모리 + 시간 초과)
        right - left < 10^5 → 반환 배열은 최대 10만 개
        → 필요한 인덱스(left~right)만 계산하면 충분

    풀이 진화 과정:
        mine_one  : 이중 for문 O(N²) → 전체 생성 후 슬라이싱 (시간 초과)
        mine_two  : 단일 for문 O(N²) → 상수 개선, 근본 복잡도 동일 (시간 초과)
        mine_three: range(left, right+1) O(right-left) → 필요한 범위만 생성 (통과)
        mine_four : 리스트 컴프리헨션 압축 → mine_three와 동일한 복잡도 (통과)

    코딩테스트 판단 기준:
        n ≤ 10^7 → O(N²) 불가, O(N) 또는 그 이하 필요
        right-left < 10^5 → 반환 크기 힌트 → 이 범위만 처리하면 됨
================================================================================
[복잡도 분석]
    N = n (최대 10^7)
    K = right - left + 1 (최대 10^5)

    Mine_one   - 시간: O(N²) | 공간: O(N²) - 전체 배열 생성 (시간 초과)
    Mine_two   - 시간: O(N²) | 공간: O(N²) - 전체 배열 생성 (시간 초과)
    Mine_three - 시간: O(K)  | 공간: O(K)  - 필요한 범위만 생성 (통과)
    Mine_four  - 시간: O(K)  | 공간: O(K)  - 리스트 컴프리헨션 (통과)
    Best       - 시간: O(K)  | 공간: O(K)  - Mine_four와 동일, 주석 보강
    Sub        - 시간: O(K)  | 공간: O(K)  - Mine_three와 동일, 주석 보강

    K ≤ 10^5 → Best/Sub 최대 10만 번 연산으로 충분
"""

import time
from typing import List, Tuple


# ================================================================================
# Mine solution one - 이중 for문 전체 배열 생성 (시간 초과)
# ================================================================================
def solution_mine_one(n: int, left: int, right: int) -> List[int]:
    """
    이중 for문으로 n×n 전체 배열을 생성한 뒤 슬라이싱으로 반환하는 초기 풀이

    시간 초과 원인:
        n²개 원소 전체 생성 → n=10^7이면 10^14개 → 불가능
        필요한 건 최대 10^5개인데 10^14개를 만들어 버림

    의의:
        max(i+1, j+1): 행(i), 열(j) 중 큰 값이 원소 값이라는 규칙 도출
    """
    arr = []
    for i in range(n):
        for j in range(n):
            arr.append(max(i + 1, j + 1))  # 행, 열 중 큰 값 (1-indexed)

    return arr[left:right + 1]


# ================================================================================
# Mine solution two - 단일 for문 + 수학 연산 전체 배열 생성 (시간 초과)
# ================================================================================
def solution_mine_two(n: int, left: int, right: int) -> List[int]:
    """
    단일 for문 + i//n, i%n으로 행/열을 계산해 전체 배열을 생성하는 풀이

    mine_one 대비 개선 시도:
        이중 for문 → 단일 for문 (상수 개선)
        i//n: 1차원 인덱스 i의 행 (0-indexed)
        i%n : 1차원 인덱스 i의 열 (0-indexed)

    근본 복잡도 O(N²) 유지 → 시간 초과 동일하게 발생
    의의: 1차원 인덱스에서 행/열을 수학적으로 계산하는 규칙 발견
            → mine_three에서 범위 제한으로 활용
    """
    arr = []
    for i in range(n ** 2):
        arr.append(max(i // n + 1, i % n + 1))  # 행=i//n, 열=i%n (0-indexed → +1)

    return arr[left:right + 1]


# ================================================================================
# Mine solution three - 필요한 범위만 생성 (통과)
# ================================================================================
def solution_mine_three(n: int, left: int, right: int) -> List[int]:
    """
    range(left, right+1)로 필요한 인덱스만 순회해 반환하는 풀이

    mine_two 대비 핵심 개선:
        전체 배열 생성 제거 → 필요한 인덱스(left~right)만 계산
        mine_two의 수학 규칙 i//n, i%n을 그대로 유지
        range 범위를 left~right+1로 제한 → O(N²) → O(K)

    max(i//n+1, i%n+1):
        i//n: 행 (0-indexed), i%n: 열 (0-indexed) → +1로 1-indexed 변환 후 비교
        = max(i//n, i%n) + 1  (수학적 동치)
    """
    arr = []
    for i in range(left, right + 1):       # 전체 아닌 필요한 범위만 순회
        arr.append(max(i // n + 1, i % n + 1))
    return arr


# ================================================================================
# Mine solution four - 리스트 컴프리헨션 압축 (통과)
# ================================================================================
def solution_mine_four(n: int, left: int, right: int) -> List[int]:
    """
    mine_three를 리스트 컴프리헨션으로 압축한 풀이

    mine_three 대비 개선:
        for 루프 + append → 리스트 컴프리헨션 원라인 표현
        max(i//n+1, i%n+1) → max(i//n, i%n)+1 (더 간결한 동치 표현)
            max(a+1, b+1) = max(a,b)+1 이므로 동일한 결과
    """
    return [max(i // n, i % n) + 1 for i in range(left, right + 1)]


# ================================================================================
# Best solution - 리스트 컴프리헨션 (mine_four 주석 보강)
# ================================================================================
def solution_best(n: int, left: int, right: int) -> List[int]:
    """
    필요한 인덱스만 순회하며 수학 규칙으로 원소를 계산하는 최적 풀이

    mine_four와 동일한 로직, 근거 주석 보강:
        range(left, right+1): 전체 n² 아닌 필요한 K개만 순회
        i // n: 1차원 인덱스 i의 행 (0-indexed)
        i % n : 1차원 인덱스 i의 열 (0-indexed)
        max(i//n, i%n)+1: 행/열 중 큰 값 + 1 (1-indexed 원소 값)

    핵심 판단 기준:
        n ≤ 10^7 → n² ≤ 10^14 → 전체 배열 생성 불가
        right-left < 10^5 → 이 범위만 계산하면 충분
    """
    return [max(i // n, i % n) + 1 for i in range(left, right + 1)]


# ================================================================================
# Sub solution - 명시적 for 루프 (mine_three 주석 보강)
# ================================================================================
def solution_sub(n: int, left: int, right: int) -> List[int]:
    """
    명시적 for 루프로 각 단계를 분리해 표현한 서브 풀이

    Best 대비 특징:
        arr 리스트와 append로 각 단계가 명시적으로 드러남
        중간 값(i//n, i%n) 확인 가능 → 디버깅 용이
        max(i//n+1, i%n+1): 행/열 각각 +1 후 비교 (동치이나 의도 명시적)
    """
    arr = []
    for i in range(left, right + 1):
        row = i // n                        # 행 (0-indexed)
        col = i % n                         # 열 (0-indexed)
        arr.append(max(row, col) + 1)       # 1-indexed 원소 값
    return arr


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[int, int, int, List[int]]] = [
        # (n, left, right, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # n=3, left=2, right=5:
        #   i=2: 2//3=0, 2%3=2 → max(0,2)+1=3
        #   i=3: 3//3=1, 3%3=0 → max(1,0)+1=2
        #   i=4: 4//3=1, 4%3=1 → max(1,1)+1=2
        #   i=5: 5//3=1, 5%3=2 → max(1,2)+1=3
        #   → [3,2,2,3]
        (3, 2,  5,  [3, 2, 2, 3]),
        # n=4, left=7, right=14:
        #   i=7 : 7//4=1, 7%4=3  → max(1,3)+1=4
        #   i=8 : 8//4=2, 8%4=0  → max(2,0)+1=3
        #   i=9 : 9//4=2, 9%4=1  → max(2,1)+1=3
        #   i=10: 10//4=2, 10%4=2 → max(2,2)+1=3
        #   i=11: 11//4=2, 11%4=3 → max(2,3)+1=4
        #   i=12: 12//4=3, 12%4=0 → max(3,0)+1=4
        #   i=13: 13//4=3, 13%4=1 → max(3,1)+1=4
        #   i=14: 14//4=3, 14%4=2 → max(3,2)+1=4
        #   → [4,3,3,3,4,4,4,4]
        (4, 7,  14, [4, 3, 3, 3, 4, 4, 4, 4]),
        # 추가 케이스:
        # n=2, left=0, right=3: 전체 배열 [1,2,2,2]
        #   i=0: max(0,0)+1=1, i=1: max(0,1)+1=2
        #   i=2: max(1,0)+1=2, i=3: max(1,1)+1=2
        (2, 0,  3,  [1, 2, 2, 2]),
        # n=1, left=0, right=0: 1×1 배열, 유일한 원소=1
        #   i=0: 0//1=0, 0%1=0 → max(0,0)+1=1
        (1, 0,  0,  [1]),
    ]

    # mine_one/two는 n이 큰 케이스에서 시간 초과 → 소규모 입력만 검증
    small_solutions = [
        ("Mine_one  (이중for 전체생성)", solution_mine_one),
        ("Mine_two  (단일for 전체생성)", solution_mine_two),
    ]
    all_solutions = [
        ("Mine_three(범위제한 for)    ", solution_mine_three),
        ("Mine_four (범위제한 컴프리)", solution_mine_four),
        ("Best      (컴프리헨션)      ", solution_best),
        ("Sub       (명시적 for)      ", solution_sub),
    ]

    print("=" * 72)
    print(f"{'풀이':<32} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 72)

    for name, func in small_solutions:
        for idx, (n, left, right, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, left, right)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<32} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 72)

    for name, func in all_solutions:
        for idx, (n, left, right, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, left, right)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<32} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 72)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
