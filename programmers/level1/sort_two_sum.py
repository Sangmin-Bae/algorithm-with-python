"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 두 개 뽑아서 더하기
    유형       : Sort / Combination
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/68644
    풀이일자   : 2026-05-26
================================================================================
[문제 요약]
    서로 다른 인덱스의 두 수를 뽑아 더한 모든 합을 중복 제거 후 오름차순 반환

    제약 조건
        - numbers 길이: 2 이상 100 이하
        - 원소값: 0 이상 100 이하
        - "서로 다른 인덱스" → 같은 값이라도 인덱스가 다르면 유효한 쌍
            예: [1,1] → 1+1=2 가능
================================================================================
[입출력 예시]
    numbers       | result
    --------------|------------------
    [2,1,3,4,1]   | [2,3,4,5,6,7]
    [5,0,2,7]     | [2,5,7,9,12]
================================================================================
[Mine_one 실패 원인 — 반례 분석]
    가정: "정렬 후 앞에서부터 더하면 결과가 오름차순으로 나온다"
    반례: numbers = [1, 9, 6, 0, 0, 1]
        sorted  = [0, 0, 1, 1, 6, 9]

    순회 과정:
        0+0=0, 0+1=1, 0+1=1(중복), 0+6=6, 0+9=9  ← 6,9가 먼저
        0+1=1(중복), 0+1(중복), 0+6(중복), 0+9(중복)
        1+1=2  ← 2가 6,9 뒤에 나옴!
        ...
        Mine_one 결과: [0,1,6,9,2,7,10,15]  ← 오름차순 아님 (오답)
        정답:          [0,1,2,6,7,9,10,15]

    실패 이유:
        x가 증가할수록 y 범위가 좁아지는 구조에서
        "큰 x + 작은 y"가 "작은 x + 큰 y"보다 나중에 나올 수 있음
        → 정렬된 배열에서 순서대로 더한다고 결과가 오름차순이 아님
        → 반드시 마지막에 정렬하거나 set으로 모은 후 sorted() 필요
================================================================================
[내 초기 풀이]
    Mine_one  : 정렬 후 이중루프 + 리스트 in 비교 → 오름차순 보장 안됨 (일부 실패)
    Mine_two  : 이중루프 + 리스트 in 비교 + 마지막 sorted() → 통과
    Mine_three: 이중루프 + set 중복제거 + sorted() → 통과
    Mine_four : pop()으로 원소 추출 + set + sorted() → 통과 (원본 파괴 주의)

[개선 포인트]
    Mine_two/three: answer 리스트 → set에 바로 담아 변수 하나 제거
    Mine_four: pop()이 원본 numbers 직접 수정
                → 함수 외부에서 numbers 재사용 시 빈 리스트가 됨
    Best: set에 바로 add, sorted()로 마지막 정렬
    Sub:  itertools.combinations 활용 → "두 개 뽑기"를 명시적으로 표현
================================================================================
[복잡도 분석]
    N = len(numbers) (최대 100)
    모든 쌍의 수 = C(N,2) = N(N-1)/2 ≤ 4,950

    Mine_one   - 시간: O(N²×M) | 공간: O(M)  — 리스트 in O(M), 오답
    Mine_two   - 시간: O(N²×M) | 공간: O(M)  — 리스트 in O(M)
    Mine_three - 시간: O(N²)   | 공간: O(N²) — set add O(1)
    Mine_four  - 시간: O(N²)   | 공간: O(N²) — set add O(1), 원본 파괴
    Best       - 시간: O(N²)   | 공간: O(N²) — set add O(1)
    Sub        - 시간: O(N²)   | 공간: O(N²) — combinations + set

    N ≤ 100이라 모든 풀이 즉시 실행
================================================================================
"""

from itertools import combinations
import time
from typing import List, Tuple


# ==============================================================================
# Mine solution one — 정렬 후 이중루프 + 리스트 in (일부 실패)
# ==============================================================================
def solution_mine_one(numbers: List[int]) -> List[int]:
    """
    오름차순 정렬 후 순서대로 더하면 오름차순이 보장된다는 가정으로 푼 풀이

    실패 이유:
        x가 증가할수록 y 범위가 좁아져
        "작은 x + 큰 y"가 "큰 x + 작은 y"보다 먼저 나올 수 있음
        → 정렬 후 순회해도 결과가 오름차순이 아닐 수 있음
        반례: [1,9,6,0,0,1] → [0,1,6,9,2,...] (6,9 뒤에 2 등장)
    """
    answer = []
    s_numbers = sorted(numbers)

    for x in range(len(s_numbers)):
        for y in range(x + 1, len(s_numbers)):
            if s_numbers[x] + s_numbers[y] not in answer:
                answer.append(s_numbers[x] + s_numbers[y])

    return answer   # 오름차순 보장 안됨


# ==============================================================================
# Mine solution two — 이중루프 + 리스트 in + 마지막 sorted()
# ==============================================================================
def solution_mine_two(numbers: List[int]) -> List[int]:
    """
    Mine_one의 실패를 확인 후 정렬 시점을 마지막으로 옮긴 수정 풀이

    Mine_one 대비 변경:
        초기 정렬 제거, 마지막에 sorted() 적용
        → 오름차순 보장

    개선 가능:
        리스트 in 연산: O(M), set add: O(1)
        answer 리스트 → set으로 교체하면 중복 검사 자동화
    """
    answer = []

    for x in range(len(numbers)):
        for y in range(x + 1, len(numbers)):
            if numbers[x] + numbers[y] not in answer:  # 리스트 in: O(M)
                answer.append(numbers[x] + numbers[y])

    return sorted(answer)


# ==============================================================================
# Mine solution three — 이중루프 + set + sorted()
# ==============================================================================
def solution_mine_three(numbers: List[int]) -> List[int]:
    """
    set으로 중복 제거, sorted()로 정렬하는 풀이

    Mine_two 대비 개선:
        리스트 in → set add O(1)로 중복 처리 개선
        answer 리스트 대신 set에 직접 담음

    개선 가능:
        answer 리스트 → sums set으로 변수명/타입 통일
    """
    answer = []

    for x in range(len(numbers)):
        for y in range(x + 1, len(numbers)):
            answer.append(numbers[x] + numbers[y])

    return sorted(list(set(answer)))


# ==============================================================================
# Mine solution four — pop() 순차 추출 + set + sorted()
# ==============================================================================
def solution_mine_four(numbers: List[int]) -> List[int]:
    """
    pop()으로 원소를 순차 추출하며 남은 원소들과 더하는 풀이

    핵심 발상:
        pop(): 마지막 원소 추출 O(1) (pop(0)는 O(N)이라 비효율)
        item과 남은 numbers 원소들의 합 → 모든 쌍 커버됨

    주의:
        pop()이 원본 numbers를 직접 수정
        → 함수 외부에서 numbers 재사용 시 빈 리스트가 됨
        → 원본 보존이 필요하면 numbers[:] 복사본 사용
    """
    answer = []

    while numbers:
        item = numbers.pop()        # 원본 직접 수정 주의

        for j in numbers:
            answer.append(item + j)

    return sorted(list(set(answer)))


# ==============================================================================
# Best solution — 이중루프 + set 직접 add + sorted()
# ==============================================================================
def solution_best(numbers: List[int]) -> List[int]:
    """
    set에 바로 합산값을 add해 중복 자동 제거 + sorted()로 오름차순 반환

    Mine_three 대비 개선:
        - answer 리스트 → sums set으로 직접 담아 변수 하나 제거
        - set add: O(1), 중복 자동 처리

    핵심:
        - 이중루프: range(x+1, N)으로 같은 쌍 중복 탐색 방지
        - set: 같은 합산값 중복 제거
        - sorted(): 오름차순 정렬
    """
    sums = set()

    for x in range(len(numbers)):
        for y in range(x + 1, len(numbers)):
            sums.add(numbers[x] + numbers[y])  # set add: O(1)

    return sorted(sums)


# ==============================================================================
# Sub solution — itertools.combinations 활용
# ==============================================================================
def solution_sub(numbers: List[int]) -> List[int]:
    """
    combinations로 두 개 뽑기를 명시적으로 표현한 파이써닉한 풀이

    combinations(numbers, 2):
        서로 다른 인덱스에서 2개를 뽑는 모든 쌍 생성
        → "서로 다른 인덱스" 조건을 라이브러리로 보장
        → 이중루프를 대체

    한 줄 구현:
        sorted(set(a + b for a, b in combinations(numbers, 2)))
    """
    return sorted(set(a + b for a, b in combinations(numbers, 2)))


# ==============================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==============================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], List[int]]] = [
        # (numbers, 기댓값)
        ([2, 1, 3, 4, 1],       [2, 3, 4, 5, 6, 7]),            # 기본 예시 1
        ([5, 0, 2, 7],          [2, 5, 7, 9, 12]),              # 기본 예시 2
        ([1, 1],                [2]),                           # 최소 길이, 동일값
        ([0, 0],                [0]),                           # 0+0=0
        ([1, 9, 6, 0, 0, 1],    [0, 1, 2, 6, 7, 9, 10, 15]),    # Mine_one 반례
        ([100, 100],            [200]),                         # 최대 원소값
    ]

    solutions = [
        ("Mine_one   (정렬후+in)",    solution_mine_one),
        ("Mine_two   (in+마지막sort)", solution_mine_two),
        ("Mine_three (set+sorted)",   solution_mine_three),
        ("Mine_four  (pop+set)",      solution_mine_four),
        ("Best       (set직접add)",   solution_best),
        ("Sub        (combinations)", solution_sub),
    ]

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (numbers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(numbers[:])   # 원본 보존 (Mine_four pop 대비)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed*1000:>8.4f}ms")
        print("-" * 70)


# ==============================================================================
# 실행 진입점
# ==============================================================================
if __name__ == "__main__":
    solution_comparison()