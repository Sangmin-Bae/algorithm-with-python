"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 행렬의 곱셈
    유형       : Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12949
    풀이일자   : 2026-06-27
================================================================================
[문제 요약]
    2차원 행렬 arr1과 arr2를 입력받아 행렬 곱셈 결과를 반환

    제약 조건
        - arr1, arr2 행/열 길이: 2 이상 100 이하
        - 원소: -10 이상 20 이하
        - 곱할 수 있는 배열만 주어짐 → arr1 열 수 = arr2 행 수 보장
================================================================================
[입출력 예시]
    arr1                          | arr2          | return
    ------------------------------|---------------|---------------------
    [[1,4],[3,2],[4,1]]           | [[3,3],[3,3]] | [[15,15],[15,15],[15,15]]
    [[2,3,2],[4,2,4],[3,1,4]]     | [[5,4,3],[2,4,1],[3,1,1]] | [[22,22,11],[36,28,18],[29,20,14]]
================================================================================
[행렬 곱셈 수학적 정의]
    arr1(N×M) × arr2(M×K) = result(N×K)
    result[i][j] = Σ arr1[i][k] * arr2[k][j]  (k: 0~M-1)
                 = arr1의 i번째 행 · arr2의 j번째 열 (내적)

    손 추적 ([[1,4],[3,2],[4,1]] × [[3,3],[3,3]]):
        result[0][0] = 1×3 + 4×3 = 3+12 = 15
        result[0][1] = 1×3 + 4×3 = 3+12 = 15
        result[1][0] = 3×3 + 2×3 = 9+6  = 15
        → [[15,15],[15,15],[15,15]] ✓

[전치행렬(Transpose)이 필요한 이유]
    Python 리스트에서 arr2의 j번째 열 추출:
        [row[j] for row in arr2]  → 매번 O(M) 순회 필요

    arr2를 전치하면:
        transposed_arr2[j] = arr2의 j번째 열  → O(1) 접근
        zip(row, col)로 내적 계산이 자연스러워짐

[zip(*arr2) 전치 원리]
    arr2 = [[3,3],[3,3]]
    *arr2 언패킹: [3,3], [3,3]  → zip([3,3],[3,3])
    같은 인덱스끼리 묶음: (3,3), (3,3)
    → 원래 arr2의 열들이 행으로 변환 = 전치행렬

    일반화:
        zip(*matrix): matrix의 전치행렬을 튜플의 이터레이터로 반환
        list(zip(*matrix)): 리스트로 변환 (각 원소는 튜플)
================================================================================
[내 초기 풀이]
    solution_mine_one  : 전치 수동 생성 (빈 리스트 + append) + zip 내적
    solution_mine_two  : 전치 인덱스 스왑 (0 초기화 + [j][i]=[i][j]) + zip 내적
    solution_mine_three: 전치 zip(*arr2) + zip 내적
    solution_mine_four : 전치 없이 3중 for 루프 + 인덱스 직접 접근
    solution_mine_five : zip(*arr2) 전치 + 중첩 리스트 컴프리헨션 원라인

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 (명시적 전치 생성 방식)
    solution_mine_two  : 개선 필요 없음 (인덱스 스왑으로 전치 수학적 정의 직접 표현)
    solution_mine_three:
        [x for x in zip(*arr2)] → list(zip(*arr2))로 간결하게
        컴프리헨션 없이 list()로 변환하면 충분
    solution_mine_four :
        n→k→m 루프 순서: arr2[m][k] 접근 시 m 변화 = 행 변경 → 캐시 미스
        n→m→k 순서로 변경하면 arr2[m] 행이 캐시에 유지 → 캐시 더 친화적
    solution_mine_five : 개선 필요 없음 - Best
================================================================================
[solution_mine_four 루프 순서와 캐시 효율]
    현재 n→k→m 순서:
        for n: arr1 행 고정
            for k: arr2 열 고정 (결과 열)
                for m: arr2[m][k] 접근 → m 변화 = 행이 바뀜 → 캐시 미스

    캐시 친화적 n→m→k 순서:
        for n: arr1 행 고정
            for m: arr2[m] 행 전체가 캐시에 올라옴
                for k: arr2[m][k] 접근 → 같은 행 내 이동 → 캐시 히트

    이 문제 규모(100×100)에서는 차이 미미하나
    대규모 행렬에서 메모리 접근 패턴이 성능에 직접 영향
================================================================================
[복잡도 분석]
    N = len(arr1), M = len(arr2), K = len(arr2[0])
    최대: N=M=K=100 → 최대 1,000,000번 연산

    Mine_one   - 시간: O(N×M×K) | 공간: O(M×K) - 전치 저장
    Mine_two   - 시간: O(N×M×K) | 공간: O(M×K) - 전치 저장
    Mine_three - 시간: O(N×M×K) | 공간: O(M×K) - 전치 저장
    Mine_four  - 시간: O(N×M×K) | 공간: O(N×K) - 결과 행렬만 저장
    Mine_five  - 시간: O(N×M×K) | 공간: O(M×K) - zip(*arr2) 이터레이터
    Best       - 시간: O(N×M×K) | 공간: O(M×K) - Mine_five와 동일
    Sub        - 시간: O(N×M×K) | 공간: O(N×K) - Mine_four와 동일

    모든 풀이 시간복잡도 동일 O(N×M×K)
    Mine_four(Sub): 전치 행렬 생성 없음 → 추가 공간 O(M×K) 절감
"""

import time
from typing import List, Tuple


# ================================================================================
# Mine solution one - 전치 수동 생성 (빈 리스트 + append) + zip 내적
# ================================================================================
def solution_mine_one(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    arr2를 수동으로 전치한 뒤 zip으로 내적을 계산하는 초기 풀이

    전치 생성:
        arr2의 열 수만큼 반복하며 각 열 원소를 리스트로 수집
        col에 각 행의 i번째 원소를 추가 → arr2의 i번째 열

    내적 계산:
        zip(row, col): arr1의 행과 전치의 열(원래 arr2의 열) 원소 쌍 추출
        sum(x*y for ...): 원소곱의 합 = 내적
    """
    answer = []
    transposed_arr2 = []

    for i in range(len(arr2[0])):       # arr2 열 수만큼 반복
        col = []
        for row in arr2:
            col.append(row[i])          # 각 행의 i번째 원소 = i번째 열
        transposed_arr2.append(col)

    for row in arr1:
        temp = []
        for col in transposed_arr2:
            temp.append(sum(x * y for x, y in zip(row, col)))  # 내적
        answer.append(temp)

    return answer


# ================================================================================
# Mine solution two - 인덱스 스왑으로 전치 생성 + zip 내적
# ================================================================================
def solution_mine_two(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    0 초기화 후 [j][i] = [i][j] 인덱스 스왑으로 전치를 생성하는 풀이

    전치의 수학적 정의 직접 표현:
        전치행렬 T[j][i] = A[i][j]
        0으로 초기화된 K×M 행렬에 인덱스를 반전시켜 값 대입
    """
    answer = []
    n = len(arr2)
    m = len(arr2[0])
    transposed_arr2 = [[0] * n for _ in range(m)]  # K×M 크기 0 초기화

    for i in range(n):
        for j in range(m):
            transposed_arr2[j][i] = arr2[i][j]     # 인덱스 반전 = 전치 정의

    for row in arr1:
        temp = []
        for col in transposed_arr2:
            temp.append(sum(x * y for x, y in zip(row, col)))
        answer.append(temp)

    return answer


# ================================================================================
# Mine solution three - zip(*arr2) 전치 + zip 내적
# ================================================================================
def solution_mine_three(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    zip(*arr2)로 전치를 한 줄에 생성하는 풀이

    zip(*arr2) 동작:
        *arr2: arr2의 각 행을 언패킹 → zip의 별도 인자로 전달
        zip: 같은 인덱스끼리 묶음 → arr2의 열이 행으로 변환 = 전치

    개선 가능:
        [x for x in zip(*arr2)] → list(zip(*arr2))로 간결하게 표현 가능
        컴프리헨션 없이 list()로 변환하면 충분
    """
    answer = []
    transposed_arr2 = list(zip(*arr2))  # [x for x in zip(*arr2)]와 동일

    for row in arr1:
        temp = []
        for col in transposed_arr2:
            temp.append(sum(x * y for x, y in zip(row, col)))
        answer.append(temp)

    return answer


# ================================================================================
# Mine solution four - 전치 없이 3중 for 루프 + 인덱스 직접 접근
# ================================================================================
def solution_mine_four(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    전치 없이 3중 루프와 인덱스로 행렬 곱셈을 직접 구현하는 풀이

    행렬 곱셈 정의 직접 구현:
        answer[n][k] = Σ arr1[n][m] * arr2[m][k]
        n(arr1 행) → k(arr2 열) → m(공통 차원) 순 순회

    전치 불필요:
        추가 공간 O(M×K) 없이 결과 행렬 O(N×K)만 사용
        전치 생성 비용(O(M×K)) 없음

    루프 순서 개선 가능:
        현재 n→k→m: arr2[m][k] 접근 시 m 변화 = 행 변경 → 캐시 미스
        n→m→k 순서: arr2[m] 행이 캐시에 유지 → 캐시 더 친화적
        이 문제 규모(100×100)에서 차이 미미하나 대규모에서 유의미
    """
    answer = [[0] * len(arr2[0]) for _ in range(len(arr1))]  # N×K 결과 행렬

    for n in range(len(arr1)):
        for k in range(len(arr2[0])):   # arr2 열 = 결과 열
            for m in range(len(arr2)):  # 공통 차원 순회
                answer[n][k] += arr1[n][m] * arr2[m][k]

    return answer


# ================================================================================
# Mine solution five - zip(*arr2) 전치 + 중첩 리스트 컴프리헨션 원라인
# ================================================================================
def solution_mine_five(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    zip(*arr2) 전치와 중첩 컴프리헨션으로 원라인 반환하는 가장 파이써닉한 풀이

    읽는 순서:
        바깥: for row in arr1        → arr1의 각 행 순회
        안쪽: for col in zip(*arr2)  → arr2 전치의 각 열(원래 arr2의 열) 순회
        핵심: sum(x*y for x,y in zip(row,col)) → 행과 열의 내적

    zip(*arr2): 이터레이터로 반환, 컴프리헨션 내 순회 시 메모리 효율적
    """
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*arr2)] for row in arr1]


# ================================================================================
# Best solution - 중첩 컴프리헨션 원라인 (mine_five 주석 보강)
# ================================================================================
def solution_best(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    zip(*arr2) + 중첩 리스트 컴프리헨션으로 행렬 곱셈을 표현하는 최적 풀이

    mine_five와 동일한 로직, 선정 근거 주석 보강:
        zip(*arr2): 전치를 이터레이터로 생성 → 추가 리스트 없이 순회
        중첩 컴프리헨션: 행렬 곱셈 로직을 가장 간결하게 표현
        가독성과 간결성 모두 충족
    """
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*arr2)] for row in arr1]


# ================================================================================
# Sub solution - 3중 for 루프 (mine_four 주석 보강)
# ================================================================================
def solution_sub(arr1: List[List[int]], arr2: List[List[int]]) -> List[List[int]]:
    """
    전치 없이 3중 루프와 인덱스로 행렬 곱셈을 직접 구현하는 서브 풀이

    Best 대비 특징:
        전치 행렬 생성 없음 → 공간 O(M×K) 절감 (결과 O(N×K)만 사용)

    n→m→k 루프 순서 (캐시 친화적, mine_four의 n→k→m 대비):
        arr2[m][k]: m이 외부 루프 → arr2[m] 행이 캐시에 유지
                    k가 내부 루프 → 같은 행 내 연속 접근 = 캐시 히트
        n→k→m(mine_four): arr2[m][k]에서 m이 내부 → 행이 바뀜 = 캐시 미스

    직관성은 n→k→m이 우위:
        행렬 곱셈 정의: "하나의 행 × 하나의 열 → 내적"
        n→k→m: k(열) 고정 → m 순회로 내적 완성 → 다음 열로 이동
                한 번의 m 루프에 answer[n][k] 완성 → 직관적
        n→m→k: m 고정 → k를 순회하며 answer[n][k]에 부분 기여값 분산
                m 루프 전체가 끝난 후 answer[n][k] 완성 → 덜 직관적
        수학적으로 Σ arr1[n][m]*arr2[m][k] 는 더하는 순서와 무관하게 동일

    실행 결과에서 Sub가 mine_four보다 빠른 것이 캐시 효율 차이
    """
    answer = [[0] * len(arr2[0]) for _ in range(len(arr1))]

    for n in range(len(arr1)):
        for m in range(len(arr2)):      # arr2[m] 행이 캐시에 유지
            for k in range(len(arr2[0])):   # 같은 행 내 연속 접근
                answer[n][k] += arr1[n][m] * arr2[m][k]

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[List[int]], List[List[int]], List[List[int]]]] = [
        # (arr1, arr2, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [[1,4],[3,2],[4,1]] × [[3,3],[3,3]]:
        #   result[0][0] = 1×3+4×3 = 15
        #   result[0][1] = 1×3+4×3 = 15
        #   result[1][0] = 3×3+2×3 = 15
        #   result[1][1] = 3×3+2×3 = 15
        #   result[2][0] = 4×3+1×3 = 15
        #   result[2][1] = 4×3+1×3 = 15
        #   → [[15,15],[15,15],[15,15]]
        ([[1,4],[3,2],[4,1]], [[3,3],[3,3]],[[15,15],[15,15],[15,15]]),
        # [[2,3,2],[4,2,4],[3,1,4]] × [[5,4,3],[2,4,1],[3,1,1]]:
        #   result[0][0] = 2×5+3×2+2×3 = 10+6+6 = 22
        #   result[0][1] = 2×4+3×4+2×1 = 8+12+2 = 22
        #   result[0][2] = 2×3+3×1+2×1 = 6+3+2  = 11
        #   (나머지는 공식 예시 기준)
        ([[2,3,2],[4,2,4],[3,1,4]], [[5,4,3],[2,4,1],[3,1,1]],[[22,22,11],[36,28,18],[29,20,14]]),
        # 추가 케이스:
        # 2×2 단위행렬 × 2×2: 결과 = 원본 (단위행렬 성질)
        #   [[1,0],[0,1]] × [[3,4],[5,6]]:
        #   result[0][0]=1×3+0×5=3, result[0][1]=1×4+0×6=4
        #   result[1][0]=0×3+1×5=5, result[1][1]=0×4+1×6=6
        ([[1,0],[0,1]], [[3,4],[5,6]],[[3,4],[5,6]]),
    ]

    solutions = [
        ("Mine_one   (수동전치+zip) ", solution_mine_one),
        ("Mine_two   (인덱스스왑)   ", solution_mine_two),
        ("Mine_three (zip전치)      ", solution_mine_three),
        ("Mine_four  (3중루프n,k,m) ", solution_mine_four),
        ("Mine_five  (컴프리헨션)   ", solution_mine_five),
        ("Best       (컴프리헨션)   ", solution_best),
        ("Sub        (3중루프n,m,k) ", solution_sub),
    ]

    # 워밍업 스텝 ──────────────────────────────────────────────────
    _arr1, _arr2, _ = test_cases[0]
    for _, func in solutions:
        func(_arr1, _arr2)
    # ───────────────────────────────────────────────────────────────

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (arr1, arr2, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr1, arr2)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
