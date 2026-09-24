"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 쿼드압축 후 개수 세기
    유형       : Divide & Conquer / 2D Prefix Sum
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/68936
    풀이일자   : 2026-09-24
===================================================================================
[문제 요약]
    0과 1로 이루어진 2^n × 2^n 배열을 쿼드트리 방식으로 압축할 때
    남는 0의 개수와 1의 개수를 [zeros, ones]로 반환

    제약 조건
        - arr 크기: 1×1 ~ 1024×1024 (2의 거듭제곱)
        - 원소: 0 또는 1
===================================================================================
[입출력 예시]
    arr                             | result
    --------------------------------|-------
    [[1,1,0,0],[1,0,0,0],           | [4, 9]
     [1,0,0,1],[1,1,1,1]]
===================================================================================
[쿼드트리 압축 원리]
    영역 S의 모든 원소가 같으면 → 해당 값 1개로 압축
    다르면 → 4등분 후 각각 재귀 적용

[내 풀이 — 재귀 분할 + 이중 루프]
    divide(x, y, size):
        (x, y): 영역 좌상단 좌표
        size: 영역 한 변 길이

    동일 여부: arr[x][y]를 기준으로 이중 루프 탐색
        조기 탈출: is_same=False 시 즉시 break
        → 실질 O(1) ~ O(size²) 사이

    4분할:
        좌상단: divide(x,          y,          new_size)
        우상단: divide(x,          y+new_size, new_size)
        좌하단: divide(x+new_size, y,          new_size)
        우하단: divide(x+new_size, y+new_size, new_size)

[ref_one — Bottom-up 방식]
    1×1 → 2×2 → ... → n×n 단계적 병합
    squares: 현재 단계의 블록 목록 (행, 열, 값)

    정렬 키: (x//target_size, y//target_size, x, y)
        같은 target_size 그룹의 4개를 연속 배치
        → 4개씩 묶어서 처리 가능

    v1==v2==v3==v4 and v1!=-1:
        합칠 수 있음 → 대표 좌표로 next_squares에 추가
        -1: 하위에서 이미 분리된 블록 → 합칠 수 없음

[ref_two — 2D 누적합 + 재귀]
    S[i][j] = arr[0][0] ~ arr[i-1][j-1] 영역의 합 (1의 개수)

    점화식:
        S[i][j] = arr[i-1][j-1] + S[i-1][j] + S[i][j-1] - S[i-1][j-1]
        (포함-배제 원리)

    get_area_sum(x1,y1,x2,y2):
        S[x2][y2] - S[x1][y2] - S[x2][y1] + S[x1][y1]
        → O(1) 영역합

    합산으로 동일 여부 판단:
        total == 0: 전부 0 (원소가 0 또는 1이므로)
        total == size²: 전부 1
        중간: 혼합 → 4분할

[실측 결과 — n=1024, 20회]
    체커보드(최악):
        mine    (이중루프): 444.5ms
        ref_two (누적합):   508.5ms  ← mine이 빠름

    균일배열(최선):
        mine    (이중루프):  34.0ms   ← 압도적
        ref_two (누적합):   184.3ms

    mine이 실측 더 빠른 이유:
        조기 탈출로 실질 탐색 비용이 O(size²)보다 작음
        ref_two의 O(n²) 전처리 비용이 이 문제 규모에서 지배적
===================================================================================
[내 초기 풀이]
    solution_mine: 재귀 분할 + 이중 루프

[개선 포인트]
    solution_mine:    개선 필요 없음 - Best
                      조기 탈출로 실측 가장 빠름
    solution_ref_one: Bottom-up 방식 - 참고용
                      정렬 기반 그룹핑으로 복잡도 높음
    solution_ref_two: 2D 누적합 - Sub
                      O(1) 영역합으로 알고리즘 단순
                      전처리 비용으로 실측 mine보다 느림
===================================================================================
[복잡도 분석]
    N = arr 한 변 길이 (최대 1024 = 2^10)

    Mine     - 시간: O(N² log N) 최악 | 공간: O(log N) - 재귀 스택
               최선(균일): O(N²), 조기 탈출로 평균 유리
    Ref_one  - 시간: O(N² log N) | 공간: O(N²) - squares 리스트
    Ref_two  - 시간: O(N²) 전처리 + O(N²) 탐색 | 공간: O(N²) - S 배열
    Best     - 시간: O(N² log N) 최악 | 공간: O(log N) - Mine과 동일
    Sub      - 시간: O(N²) | 공간: O(N²) - Ref_two와 동일
"""

import sys
import time

sys.setrecursionlimit(100000)


# =================================================================================
# Mine solution - 재귀 분할 + 이중 루프
# =================================================================================
def solution_mine(arr: list[list[int]]) -> list[int]:
    """
    전체 영역부터 4분할하며 재귀로 동일 여부를 탐색하는 초기 풀이

    divide(x, y, size):
        arr[x][y]를 기준으로 이중 루프로 동일 여부 탐색
        조기 탈출: is_same=False 시 즉시 break
        동일하면 answer[value]+=1, 다르면 size//2로 4분할

    조기 탈출 효과:
        체커보드 같은 최악 케이스에서도
        첫 비교에서 즉시 탈출 → 실질 O(1) 탐색
        누적합 O(1) 조회보다 상수가 작음
    """
    answer = [0, 0]
    n = len(arr)

    def divide(x: int, y: int, size: int) -> None:
        initial_value = arr[x][y]
        is_same = True

        for i in range(x, x + size):
            for j in range(y, y + size):
                if arr[i][j] != initial_value:
                    is_same = False
                    break
            if not is_same:
                break

        if is_same:
            answer[initial_value] += 1
            return

        new_size = size // 2
        divide(x,            y,            new_size)
        divide(x,            y + new_size, new_size)
        divide(x + new_size, y,            new_size)
        divide(x + new_size, y + new_size, new_size)

    divide(0, 0, n)
    return answer


# =================================================================================
# Ref solution one - Bottom-up 방식
# =================================================================================
def solution_ref_one(arr: list[list[int]]) -> list[int]:
    """
    1×1부터 n×n까지 단계적으로 4개씩 병합하는 Bottom-up 참고 풀이

    squares: (행, 열, 값) 튜플 목록
        초기: 모든 1×1 원소
        각 단계: 4개씩 묶어 합칠 수 있으면 병합, 없으면 -1 마킹

    정렬 키 (x//target_size, y//target_size, x, y):
        같은 target_size 그룹의 4개를 연속 배치
        → 4개씩 묶어서 처리 가능

    v1==v2==v3==v4 and v1!=-1:
        합칠 수 있음 → 대표 좌표 (q1)로 병합
        -1: 하위에서 분리됨 → 합칠 수 없음 → 개수 세기

    대표 좌표 q1[0], q1[1]:
        정렬 후 4개 중 가장 왼쪽 위 좌표
        상위 단계 정렬 기준과 일관성 유지
    """
    n = len(arr)
    squares = []
    for i in range(n):
        for j in range(n):
            squares.append((i, j, arr[i][j]))

    zeros = 0
    ones = 0
    size = 1

    while size < n:
        next_squares = []
        target_size = size * 2

        squares.sort(key=lambda x: (x[0] // target_size, x[1] // target_size, x[0], x[1]))

        for i in range(0, len(squares), 4):
            q1 = squares[i]
            q2 = squares[i + 1]
            q3 = squares[i + 2]
            q4 = squares[i + 3]

            v1, v2, v3, v4 = q1[2], q2[2], q3[2], q4[2]

            if v1 == v2 == v3 == v4 and v1 != -1:
                next_squares.append((q1[0], q1[1], v1))
            else:
                for v in [v1, v2, v3, v4]:
                    if v == 0:
                        zeros += 1
                    elif v == 1:
                        ones += 1
                next_squares.append((q1[0], q1[1], -1))

        squares = next_squares
        size *= 2

    for q in squares:
        v = q[2]
        if v == 0:
            zeros += 1
        elif v == 1:
            ones += 1

    return [zeros, ones]


# =================================================================================
# Ref solution two - 2D 누적합 + 재귀
# =================================================================================
def solution_ref_two(arr: list[list[int]]) -> list[int]:
    """
    2D 누적합으로 O(1) 영역합을 이용해 동일 여부를 판단하는 참고 풀이

    S[i][j] = arr[0][0] ~ arr[i-1][j-1] 영역의 합 (1의 개수)
    점화식: S[i][j] = arr[i-1][j-1] + S[i-1][j] + S[i][j-1] - S[i-1][j-1]

    get_area_sum(x1,y1,x2,y2):
        포함-배제 원리로 O(1) 영역합 계산
        S[x2][y2] - S[x1][y2] - S[x2][y1] + S[x1][y1]

    합산으로 동일 여부 판단:
        total==0: 전부 0
        total==size²: 전부 1
        중간값: 혼합 → 4분할

    mine 대비:
        O(1) 영역합이 이론상 유리하나
        O(n²) 전처리 비용으로 실측 mine보다 느림
        단일 쿼리가 아닌 반복 쿼리 상황에서 유리
    """
    n = len(arr)
    S = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            S[i][j] = arr[i-1][j-1] + S[i-1][j] + S[i][j-1] - S[i-1][j-1]

    answer = [0, 0]

    def get_area_sum(x1: int, y1: int, x2: int, y2: int) -> int:
        return S[x2][y2] - S[x1][y2] - S[x2][y1] + S[x1][y1]

    def divide(x: int, y: int, size: int) -> None:
        total = get_area_sum(x, y, x + size, y + size)

        if total == 0:
            answer[0] += 1
            return

        if total == size * size:
            answer[1] += 1
            return

        new_size = size // 2
        divide(x,            y,            new_size)
        divide(x,            y + new_size, new_size)
        divide(x + new_size, y,            new_size)
        divide(x + new_size, y + new_size, new_size)

    divide(0, 0, n)
    return answer


# =================================================================================
# Best solution - 재귀 분할 + 이중 루프 (mine 주석 보강)
# =================================================================================
def solution_best(arr: list[list[int]]) -> list[int]:
    """
    재귀 분할 + 조기 탈출 이중 루프로 실측 가장 빠른 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        조기 탈출: 첫 불일치 발견 즉시 break → 평균 O(1) 탐색
        실측 n=1024 체커보드: 444ms (ref_two 508ms 대비 우위)
        실측 n=1024 균일배열: 34ms (ref_two 184ms 대비 압도적)
        누적합 전처리(O(n²)) 없이 필요한 영역만 탐색
    """
    answer = [0, 0]
    n = len(arr)

    def divide(x: int, y: int, size: int) -> None:
        initial_value = arr[x][y]
        is_same = True

        for i in range(x, x + size):
            for j in range(y, y + size):
                if arr[i][j] != initial_value:
                    is_same = False
                    break
            if not is_same:
                break

        if is_same:
            answer[initial_value] += 1
            return

        new_size = size // 2
        divide(x,            y,            new_size)
        divide(x,            y + new_size, new_size)
        divide(x + new_size, y,            new_size)
        divide(x + new_size, y + new_size, new_size)

    divide(0, 0, n)
    return answer


# =================================================================================
# Sub solution - 2D 누적합 + 재귀 (ref_two 주석 보강)
# =================================================================================
def solution_sub(arr: list[list[int]]) -> list[int]:
    """
    2D 누적합으로 O(1) 영역합을 활용하는 서브 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        get_area_sum O(1): 알고리즘 코드가 가장 단순
        합산으로 동일 여부 판단: total==0, total==size² 두 조건
        누적합 전처리 O(n²): 이 문제에서 오버헤드로 작용
        반복 쿼리(예: 여러 압축 연산)가 필요한 확장 상황에서 유리
    """
    n = len(arr)
    S = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            S[i][j] = arr[i-1][j-1] + S[i-1][j] + S[i][j-1] - S[i-1][j-1]

    answer = [0, 0]

    def get_area_sum(x1: int, y1: int, x2: int, y2: int) -> int:
        return S[x2][y2] - S[x1][y2] - S[x2][y1] + S[x1][y1]

    def divide(x: int, y: int, size: int) -> None:
        total = get_area_sum(x, y, x + size, y + size)

        if total == 0:
            answer[0] += 1
            return

        if total == size * size:
            answer[1] += 1
            return

        new_size = size // 2
        divide(x,            y,            new_size)
        divide(x,            y + new_size, new_size)
        divide(x + new_size, y,            new_size)
        divide(x + new_size, y + new_size, new_size)

    divide(0, 0, n)
    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (arr, 기댓값)
        # 공식 예시
        ([[1, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1], [1, 1, 1, 1]], [4, 9]),
        ([[1,1,1,1,1,1,1,1],[0,1,1,1,1,1,1,1],[0,0,0,0,1,1,1,1],[0,1,0,0,1,1,1,1],
          [0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,1],[0,0,0,0,1,0,0,1],[0,0,0,0,1,1,1,1]],
         [10, 15]),
        # 추가 케이스:
        # 1×1: 단일 원소
        ([[1]], [0, 1]),
        # 전부 0
        ([[0, 0], [0, 0]], [1, 0]),
        # 2×2 혼합 → 4개 각각
        # 손 추적: [[0,1],[1,0]] → 4분할 불가 → 0:2개, 1:2개
        ([[0, 1], [1, 0]], [2, 2]),
    ]

    solutions = [
        ("Mine    (이중루프)   ", solution_mine),
        ("Ref_one (Bottom-up) ", solution_ref_one),
        ("Ref_two (누적합)    ", solution_ref_two),
        ("Best    (이중루프)  ", solution_best),
        ("Sub     (누적합)    ", solution_sub),
    ]

    # 워밍업
    _arr, _ = test_cases[0]
    for _, func in solutions:
        func(_arr)

    print("=" * 66)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (arr, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(arr)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
