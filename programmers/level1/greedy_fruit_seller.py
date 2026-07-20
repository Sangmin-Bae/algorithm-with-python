"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 과일 장수
    유형       : Greedy / Sort
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/135808
    풀이일자   : 2026-07-20
===================================================================================
[문제 요약]
    사과를 m개씩 묶어 박스 단위로 판매
    박스 가격 = 박스 내 최저 등급 × m
    최대 이익 반환 (m개 미만 남는 사과는 폐기)

    제약 조건
        - k: 3 이상 9 이하 (등급 상한, 상수)
        - m: 3 이상 10 이하
        - score 길이: 7 이상 1,000,000 이하
        - score[i]: 1 이상 k 이하
===================================================================================
[입출력 예시]
    k | m | score                                  | result
    --|---|----------------------------------------|-------
    3 | 4 | [1,2,3,1,2,3,1]                        | 8
    4 | 3 | [4,1,2,2,4,4,4,4,1,2,4,2]             | 33
===================================================================================
[핵심 아이디어 — 높은 등급끼리 묶어야 최대 이익]
    박스 가격 = 최저 등급 × m
    낮은 등급 사과가 높은 등급과 섞이면 박스 전체 가격을 낮춤
    → 내림차순 정렬 후 m개씩 묶으면 높은 등급끼리 자동으로 같은 박스

    손 추적 (k=3, m=4, [1,2,3,1,2,3,1]):
        내림차순: [3,3,2,2,1,1,1]
        인덱스:    0 1 2 3 4 5 6
        m=4이므로 인덱스 3(=m-1)이 첫 번째 박스 최저 등급 → 2
        인덱스 4~6: 3개 남음 → 폐기
        answer = 2 × 4 = 8 ✓

[풀이 1, 2, 3 공통 원리 — 정렬 후 m번째마다 최저 등급 추출]
    내림차순 정렬 후 인덱스 m-1, 2m-1, 3m-1, ...이 각 박스의 최저 등급
    → range(m-1, N, m) 또는 슬라이싱 [m-1::m]으로 추출

    풀이 2의 분배법칙:
        (A×m) + (B×m) + ... = (A+B+...) × m
        sum(최저등급들) × m으로 단순화

    풀이 3 오름차순 방식:
        버려지는 사과가 앞에 위치
        start_idx = len(score) % m으로 건너뛰고 시작

[solution_ref — 카운팅 방식 O(K + N)]
    정렬 O(N log N) 대신 등급별 개수 세기 O(N) 활용
    k ≤ 9 상수이므로 실질적으로 O(N)

    분할 상환 분석 (Amortized Analysis):
        for grade in range(k, 0, -1):      ← K번 실행
            while apple_counts[grade] > 0: ← 총합 N번 실행

        겉보기에는 O(K × N) 같아 보이나 실제로는 O(K + N)
        이유: while 루프의 총 실행 횟수가 K번의 for 루프 전체에서 N번
              apple_counts[k] + apple_counts[k-1] + ... + apple_counts[1] = N

        비유:
            10개 지갑에 총 100개 동전 분산 보관
            각 지갑의 동전을 꺼내는 총 비용: O(지갑 수 + 동전 수) = O(10 + 100)
            "각 지갑 × 최대 동전 수"가 아님

        초기 접근:
            "K번째 루프에서 처리된 사과는 다음 K 루프에서 다시 다루어지지 않음"
            → 전체 K 루프에서 총합 N이 다루어짐 → O(K + N)
===================================================================================
[내 초기 풀이]
    solution_mine_one  : 내림차순 정렬 + range(m-1, N, m) 순회
    solution_mine_two  : 내림차순 정렬 + 슬라이싱 [m-1::m] + sum × m
    solution_mine_three: 오름차순 정렬 + start_idx + range 순회

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         range로 박스 구성 원리가 명시적
    solution_mine_two  : 개선 필요 없음 - Best
                         슬라이싱 + 분배법칙으로 한 줄 표현, 가장 간결
    solution_mine_three: 개선 필요 없음
                         오름차순 관점에서의 동일 로직, start_idx 처리 필요
    solution_ref       : O(K + N) 카운팅 방식 (학습 목적)
                         정렬 O(N log N) 대비 이론적 우위
                         k ≤ 9 상수로 실측 차이 미미
===================================================================================
[복잡도 분석]
    N = len(score) (최대 1,000,000), K = k (최대 9, 상수)

    Mine_one   - 시간: O(N log N) | 공간: O(N) - sorted + range 순회
    Mine_two   - 시간: O(N log N) | 공간: O(N) - sorted + 슬라이싱
    Mine_three - 시간: O(N log N) | 공간: O(N) - sorted + range 순회
    Ref        - 시간: O(K + N)   | 공간: O(K) - 카운팅 + 분할 상환
    Best       - 시간: O(N log N) | 공간: O(N) - Mine_two와 동일
    Sub        - 시간: O(N log N) | 공간: O(N) - Mine_one과 동일

    K=9 상수 → Ref의 O(K + N) = O(N)으로 정렬 O(N log N)보다 이론적 우위
    score 100만 기준: 정렬 ≈ 20,000,000 연산, Ref ≈ 1,000,009 연산
"""

import time


# ==================================================================================
# Mine solution one - 내림차순 정렬 + range(m-1, N, m) 순회
# ==================================================================================
def solution_mine_one(k: int, m: int, score: list[int]) -> int:
    """
    내림차순 정렬 후 m번째 위치(박스 최저 등급)마다 누적하는 초기 풀이

    핵심:
        내림차순 정렬 → 높은 등급이 앞에 오면서 같은 박스에 묶임
        인덱스 m-1, 2m-1, 3m-1, ...: 각 박스의 최저 등급 위치
        range(m-1, N, m): 해당 위치만 순회

    나머지 처리:
        m개 미만 남는 사과는 range 범위에 포함되지 않아 자동 제외
    """
    answer = 0
    sorted_score = sorted(score, reverse=True)

    for idx in range(m - 1, len(sorted_score), m):
        answer += sorted_score[idx] * m

    return answer


# ==================================================================================
# Mine solution two - 슬라이싱 [m-1::m] + sum × m
# ==================================================================================
def solution_mine_two(k: int, m: int, score: list[int]) -> int:
    """
    슬라이싱으로 최저 등급만 추출 후 분배법칙으로 한 줄 표현하는 풀이

    슬라이싱 [m-1::m]:
        m-1부터 시작, m씩 건너뛰며 추출
        → 각 박스의 최저 등급 값만 모은 리스트

    분배법칙:
        (A×m) + (B×m) + ... = (A+B+...) × m
        sum(최저등급들) × m으로 단순화 → 곱셈 1회로 감소
    """
    return sum(sorted(score, reverse=True)[m - 1::m]) * m


# ==================================================================================
# Mine solution three - 오름차순 정렬 + start_idx + range 순회
# ==================================================================================
def solution_mine_three(k: int, m: int, score: list[int]) -> int:
    """
    오름차순 정렬 후 버려지는 사과를 건너뛰고 순회하는 풀이

    mine_one 대비:
        내림차순 → 오름차순: 버려지는 사과 위치가 뒤에서 앞으로 이동
        start_idx = len(score) % m: 버려지는 사과(m개 미만) 개수 = 시작 오프셋
        start_idx부터 m씩 건너뛰면 각 박스의 최저 등급 위치

    오름차순에서 최저 등급 위치:
        [1,1,2,2,2,3,3,3] m=3, start_idx=2
        인덱스 2(=start_idx): 첫 번째 박스 최저 등급 (2)
        인덱스 5(=start_idx+m): 두 번째 박스 최저 등급 (3)
    """
    answer = 0
    sorted_score = sorted(score)
    start_idx = len(sorted_score) % m

    for idx in range(start_idx, len(sorted_score), m):
        answer += sorted_score[idx] * m

    return answer


# ==================================================================================
# Ref solution - 카운팅 방식 O(K + N) (분할 상환 분석)
# ==================================================================================
def solution_ref(k: int, m: int, score: list[int]) -> int:
    """
    등급별 카운팅과 분할 상환으로 O(K + N)을 달성하는 참고 풀이

    정렬 없이 카운팅으로 등급별 사과 수 집계 O(N)
    높은 등급부터 m개씩 박스 채우기 O(K + N)

    분할 상환 분석:
        for K번, while 총합 N번 → O(K + N)
        while이 K번 × N번이 아닌 이유:
            처리된 사과는 다음 grade 루프에서 다시 처리되지 않음
            → 전체 K 루프에서 while 총 실행 = N번

    take = min(m - box_apples, apple_counts[grade]):
        현재 박스에 넣을 수 있는 개수와 남은 해당 등급 사과 중 작은 값
        → 박스가 차거나 해당 등급 사과가 소진될 때 중단

    box_apples == m: 박스 완성 → grade(현재 최저 등급) × m 가격 산정
    """
    answer = 0
    apple_counts = [0] * (k + 1)

    for s in score:
        apple_counts[s] += 1          # 등급별 사과 수 카운팅 O(N)

    box_apples = 0

    for grade in range(k, 0, -1):    # 높은 등급부터 순회 O(K)
        if apple_counts[grade] == 0:
            continue

        while apple_counts[grade] > 0:
            take = min(m - box_apples, apple_counts[grade])
            apple_counts[grade] -= take
            box_apples += take

            if box_apples == m:
                answer += grade * m   # 현재 채워진 사과 중 최저 등급 = grade
                box_apples = 0

    return answer


# ==================================================================================
# Best solution - 슬라이싱 + sum × m (mine_two 주석 보강)
# ==================================================================================
def solution_best(k: int, m: int, score: list[int]) -> int:
    """
    슬라이싱 + 분배법칙으로 최대 이익을 한 줄에 계산하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        sorted(reverse=True): 높은 등급 사과를 앞으로 모아 같은 박스에 묶음
        [m-1::m]: 각 박스의 최저 등급만 O(N/m)개 추출
        sum(...) × m: 분배법칙으로 전체 가격 계산
        코드 한 줄로 정렬 방식의 핵심을 완전히 표현
    """
    return sum(sorted(score, reverse=True)[m - 1::m]) * m


# ==================================================================================
# Sub solution - 내림차순 정렬 + range (mine_one 주석 보강)
# ==================================================================================
def solution_sub(k: int, m: int, score: list[int]) -> int:
    """
    내림차순 정렬 후 range로 박스 구성 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        range(m-1, N, m): 박스 최저 등급 위치가 코드에 명시적으로 드러남
        sorted_score[idx] × m: 각 박스 가격 계산 과정이 단계별로 보임
        분배법칙 적용 전 형태로 박스별 가격 계산 원리 이해에 적합
    """
    answer = 0
    sorted_score = sorted(score, reverse=True)

    for idx in range(m - 1, len(sorted_score), m):
        answer += sorted_score[idx] * m

    return answer


# ==================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, int, list[int], int]] = [
        # (k, m, score, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # k=3, m=4, [1,2,3,1,2,3,1]
        # 내림차순: [3,3,2,2,1,1,1]
        # 인덱스 3(m-1=3): 값 2 → 2×4=8
        # 인덱스 7(2m-1=7): 범위 초과 → 폐기
        (3, 4, [1, 2, 3, 1, 2, 3, 1], 8),
        # k=4, m=3, [4,1,2,2,4,4,4,4,1,2,4,2]
        # 내림차순: [4,4,4,4,4,2,2,2,2,1,1,2]
        # 정렬: [4,4,4,4,4,4,2,2,2,2,1,1]
        # 인덱스 2: 4→12, 인덱스 5: 4→12, 인덱스 8: 2→6, 인덱스 11: 1→3
        # → 12+12+6+3=33
        (4, 3, [4, 1, 2, 2, 4, 4, 4, 4, 1, 2, 4, 2], 33),
        # 추가 케이스:
        # 모든 사과 폐기 (m개 미만)
        (3, 4, [3, 3, 3], 0),
        # 정확히 m개
        (3, 3, [3, 2, 1], 3),
    ]

    solutions = [
        ("Mine_one   (내림차순+range)", solution_mine_one),
        ("Mine_two   (슬라이싱+sum) ", solution_mine_two),
        ("Mine_three (오름차순+idx) ", solution_mine_three),
        ("Ref        (카운팅O(K+N)) ", solution_ref),
        ("Best       (슬라이싱+sum) ", solution_best),
        ("Sub        (내림차순+range)", solution_sub),
    ]

    # 워밍업 스텝
    _k, _m, _s, _ = test_cases[0]
    for _, func in solutions:
        func(_k, _m, _s[:])

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (k, m, score, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(k, m, score[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ==================================================================================
# 실행 진입점
# ==================================================================================
if __name__ == "__main__":
    solution_comparison()
