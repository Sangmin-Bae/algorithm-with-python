"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 기지국 설치
    유형       : Greedy / Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12979
    풀이일자   : 2026-10-02
===================================================================================
[문제 요약]
    N개 아파트가 일렬로 배치, 일부 아파트 옥상에 기존 기지국 설치
    기지국은 설치된 아파트 기준 양쪽 W칸까지 전파 전달
    모든 아파트에 전파를 전달하기 위해 추가로 설치할 기지국 수의 최솟값 반환

    제약 조건
        - N: 200,000,000 이하 자연수
        - stations 크기: 10,000 이하, 오름차순 정렬
        - W: 10,000 이하 자연수
===================================================================================
[입출력 예시]
    N  | stations | W | result
    ---|----------|---|-------
    11 | [4, 11]  | 1 | 3      (1, 7, 9번 아파트에 설치)
    16 | [9]      | 2 | 3      (3, 6, 14번 아파트에 설치)
===================================================================================
[핵심 — start와 gap 계산]
    start: 전파 여부가 아직 확인되지 않은 가장 왼쪽 아파트 번호 (초기값 1)
    기존 기지국 station의 커버 구간: [station - W, station + W]

    gap(전파 미도달 구간) = [start, station - W - 1]
        길이 = (station - W) - start   (start < station - W 일 때만 존재)
        마지막 station 뒤 gap = [start, N], 길이 = N - start + 1
    기존 기지국 처리 후 start = station + W + 1

    추가 기지국 1개의 커버 폭: cover = 2W + 1
    길이 L인 gap에 필요한 추가 기지국 수 = ceil(L / cover)

[gap별 독립 합산이 최적인 이유]
    gap 사이에는 기존 기지국의 커버 구간(2W + 1칸 이상) 존재
    추가 기지국 하나가 두 gap에 걸치려면 사이 구간 전체 + 양쪽 1칸씩 = 2W + 3칸 필요
    -> 폭 2W + 1칸의 기지국 하나로는 불가
    gap마다 독립, 각 gap의 최소 = ceil(L / cover)

[mine — 포인터 skip 방식]
    start >= stations[idx] - W : 이미 커버 구간에 도달 -> start = stations[idx] + W + 1
    그 외(남은 기지국 없음 포함) : 추가 기지국 1개 설치, start += 2W + 1

    start 후진 없음의 근거:
        추가 설치 분기는 start < stations[idx] - W 일 때만 진입 (start <= station - W - 1)
        -> 새 start = start + 2W + 1 <= station + W
        -> 점프 목표 station + W + 1보다 항상 작음

    반복 횟수 = 기존 기지국 수 + 추가 기지국 수 -> 답의 크기에 비례
        최악: N = 2억, W = 1 -> 약 6,667만 회

[ref — gap 길이 나눗셈 방식]
    mine과 같은 의미의 start 사용, 반복 덧셈(start += cover)을 올림 나눗셈으로 대체
    반복 횟수 = 기존 기지국 수 + 1 -> N, W와 무관

[올림 방식 비교]
    math.ceil(length / cover): float 나눗셈
        이 제약에서는 안전
        정수가 아닌 몫은 가장 가까운 정수와 최소 1/cover(약 5e-5) 차이
        float 오차는 몫(최대 약 6.7e7) x 상대오차 약 1.1e-16 = 약 7e-9 -> 오판 불가
    (length + cover - 1) // cover: 정수 연산
        부동소수점 논증 불필요, math import 불필요 -> 채택

[검증]
    공식 예시 + 무작위 2,500케이스(N 1~13, W 1~3, 기지국 1~4개)를
    무차별 대입(모든 설치 조합 탐색)과 대조 -> 불일치 0건
    float 올림 vs 정수 올림: 무작위 200만 샘플 불일치 0건

[실측 결과]
    일반 입력 (N=2억, 기지국 10,000개, W=10,000, 반복 측정 최솟값)
        mine              1.646ms
        ref (math.ceil)   0.804ms
        best (정수 올림)   0.750ms  <- ref와 동률 수준

    최악 입력 (N=2억, 기지국 [1], W=1, 1회 측정)
        mine              3.724s   (반복 66,666,667회)
        best (정수 올림)   2.54us

    절대 시간은 실행 환경 측정값 (채점 서버 한도와 별개)
===================================================================================
[내 초기 풀이]
    solution_mine: start 포인터 skip 방식

[개선 포인트]
    solution_mine: 로직 정확, 반복 횟수가 추가 기지국 수에 비례 - Sub
    solution_ref:  gap 길이 올림 나눗셈, 반복 횟수 O(기지국 수) - Best의 기반
    solution_best: ref에서 올림만 정수 연산으로 교체
===================================================================================
[복잡도 분석]
    N = 아파트 수 (최대 2억), K = len(stations) (최대 10,000), W = 전파 도달 거리 (최대 10,000)
    R = 추가 기지국 수 (최대 약 N / (2W + 1))

    Mine - 시간: O(K + R) | 공간: O(1) - 최악 R 약 6,667만
    Ref  - 시간: O(K)     | 공간: O(1) - gap 올림 나눗셈
    Best - 시간: O(K)     | 공간: O(1) - Ref와 동일, 올림만 정수 연산
    Sub  - 시간: O(K + R) | 공간: O(1) - Mine과 동일
"""

import math
import time


# =================================================================================
# Mine solution - start 포인터 skip
# =================================================================================
def solution_mine(n: int, stations: list[int], w: int) -> int:
    """
    start를 전진시키며 기존 기지국 구간은 점프, 미도달 구간은 기지국 1개씩 추가하는 초기 풀이

    분기:
        start >= stations[idx] - w : start = stations[idx] + w + 1, idx 증가
        그 외 : answer 증가, start += 2 * w + 1 (추가 기지국 커버 폭만큼 전진)

    start 후진 없음:
        추가 설치 분기 진입 조건 start < stations[idx] - w
        -> 새 start <= stations[idx] + w < 점프 목표

    반복 횟수가 추가 기지국 수에 비례
        N = 2억, W = 1 최악 입력에서 약 3.7s
    """
    answer = 0
    start = 1
    idx = 0

    while start <= n:
        if idx < len(stations) and start >= stations[idx] - w:
            start = stations[idx] + w + 1
            idx += 1
        else:
            answer += 1
            start += 2 * w + 1

    return answer


# =================================================================================
# Ref solution - gap 길이 올림 나눗셈 (math.ceil)
# =================================================================================
def solution_ref(n: int, stations: list[int], w: int) -> int:
    """
    기존 기지국 사이 gap 길이를 구해 올림 나눗셈으로 추가 기지국 수를 계산하는 참고 풀이

    gap = [start, station - w - 1] -> 길이 = station - w - start
    마지막 station 뒤 gap = [start, n] -> 길이 = n - start + 1
    gap마다 독립, 필요 기지국 수 = ceil(길이 / cover), cover = 2w + 1

    math.ceil(length / cover): float 나눗셈
        이 제약에서는 안전, 정수 올림이 더 견고
    """
    answer = 0
    start = 1
    cover = 2 * w + 1

    for station in stations:
        left = station - w

        if start < left:
            length = left - start
            answer += math.ceil(length / cover)

        start = station + w + 1

    if start <= n:
        length = n - start + 1
        answer += math.ceil(length / cover)

    return answer


# =================================================================================
# Best solution - gap 길이 올림 나눗셈 (정수 올림)
# =================================================================================
def solution_best(n: int, stations: list[int], w: int) -> int:
    """
    ref와 동일한 로직, 올림만 정수 연산으로 교체한 최적 풀이

    선정 근거:
        반복 횟수 O(K): N, W와 무관 (mine 최악 3.7s -> 2.54us)
        (x + cover - 1) // cover : float 오차 논증 불필요, math import 불필요
        일반 입력 실측 ref와 동률 수준 (0.750ms vs 0.804ms)

    마지막 gap:
        길이 = n - start + 1
        (길이 + cover - 1) // cover = (n - start + cover) // cover
    """
    answer = 0
    start = 1
    cover = 2 * w + 1

    for station in stations:
        left = station - w

        if start < left:
            answer += (left - start + cover - 1) // cover

        start = station + w + 1

    if start <= n:
        answer += (n - start + cover) // cover

    return answer


# =================================================================================
# Sub solution - start 포인터 skip (mine 주석 보강)
# =================================================================================
def solution_sub(n: int, stations: list[int], w: int) -> int:
    """
    mine과 동일한 로직, 선정 근거 주석 보강:
        "설치 -> 커버 폭만큼 전진"이 코드에 명시적
        기존 기지국 구간은 커버 오른쪽 끝 다음 칸으로 점프
        반복 횟수가 추가 기지국 수에 비례해 Best 대비 최악 입력에서 크게 느림
        반복 덧셈(start += cover)을 올림 나눗셈으로 대체한 것이 Best
    """
    answer = 0
    start = 1
    idx = 0

    while start <= n:
        if idx < len(stations) and start >= stations[idx] - w:
            start = stations[idx] + w + 1
            idx += 1
        else:
            answer += 1
            start += 2 * w + 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[int], int, int]] = [
        # (n, stations, w, 기댓값)
        # 공식 예시
        # 손 추적(gap 계산): cover = 3, start = 1
        #   station 4 : left = 3,  gap 길이 2 -> ceil(2/3) = 1대, start = 6
        #   station 11: left = 10, gap 길이 4 -> ceil(4/3) = 2대, start = 13
        #   마지막: start > n -> 추가 없음  => 3
        (11, [4, 11], 1, 3),
        # cover = 5
        #   station 9: left = 7, gap 길이 6 -> ceil(6/5) = 2대, start = 12
        #   마지막 gap: 16 - 12 + 1 = 5 -> 1대  => 3
        (16, [9], 2, 3),
        # 추가 케이스:
        # 전부 커버: station 3, w = 2 -> [1, 5] 전체 커버 => 0
        (5, [3], 2, 0),
        # 기지국이 왼쪽 끝: 커버 [1, 2], 남은 [3, 10] 길이 8 -> ceil(8/3) = 3
        (10, [1], 1, 3),
        # 커버 구간 겹침: [2, 4]와 [3, 5]
        #   미도달: 1 / 6~10
        #   앞 gap 길이 1 -> 1대, 뒤 gap 길이 5 -> ceil(5/3) = 2대  => 3
        (10, [3, 4], 1, 3),
        # 최대 규모 경계: cover = 20,001, 양쪽 gap 길이 각각 99,989,999
        #   ceil(99,989,999 / 20,001) = 5,000
        #   (20,001 x 4,999 = 99,984,999 < 99,989,999 <= 20,001 x 5,000 = 100,005,000)
        #   양쪽 합 => 10,000
        (200_000_000, [100_000_000], 10_000, 10_000),
    ]

    solutions = [
        ("Mine (포인터 skip)   ", solution_mine),
        ("Ref  (math.ceil)     ", solution_ref),
        ("Best (정수 올림)     ", solution_best),
        ("Sub  (포인터 skip)   ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _stations, _w, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _stations[:], _w)

    print("=" * 66)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (n, stations, w, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, stations[:], w)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
