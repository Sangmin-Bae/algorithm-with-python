"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 카펫
    유형       : Math / 완전탐색
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42842
    풀이일자   : 2026-08-10
================================================================================
[문제 요약]
    테두리가 갈색(brown), 내부가 노란색(yellow)인 격자 카펫의
    가로(w), 세로(h) 크기 반환 (w >= h)

    제약 조건
        - brown: 8 이상 5,000 이하 자연수
        - yellow: 1 이상 2,000,000 이하 자연수
        - 가로 >= 세로
================================================================================
[입출력 예시]
    brown | yellow | return
    ------|--------|-------
    10    | 2      | [4, 3]
    8     | 1      | [3, 3]
    24    | 24     | [8, 6]
================================================================================
[수식 유도]
    카펫 전체 면적: w * h = brown + yellow         ... (1) 곱
    내부 노란색:   (w-2) * (h-2) = yellow
        = w*h - 2w - 2h + 4 = yellow
        = (brown+yellow) - 2(w+h) + 4 = yellow
        → 2(w+h) = brown + 4
        → w + h = (brown + 4) // 2 = (brown // 2) + 2  ... (2) 합

    (1)과 (2)에서:
        w * h = p (곱 알려짐)
        w + h = s (합 알려짐)

[이차방정식 근의 공식 적용 판단 기준]
    "합과 곱이 동시에 알려진 두 미지수" → 이차방정식 실근으로 환원 가능

    w, h를 두 실근으로 가지는 이차방정식:
        (x - w)(x - h) = 0
        x² - (w+h)x + (w*h) = 0
        x² - sx + p = 0

    근의 공식: x = (s ± sqrt(s² - 4p)) / 2
        w = (s + sqrt(s²-4p)) / 2  (더 큰 값 = 가로)
        h = (s - sqrt(s²-4p)) / 2  (더 작은 값 = 세로)

    이 패턴 적용 조건:
        미지수 2개, 방정식 2개가 (합 = 상수), (곱 = 상수) 형태일 때

[실측 결과 — 100,000회 반복]
    케이스              | one(면적약수) | two(둘레합) | ref(근의공식)
    --------------------|--------------|-------------|-------------
    TC1 w=4,h=3         | 0.47μs       | 0.34μs      | 0.31μs
    TC2 w=3,h=3         | 0.38μs       | 0.34μs      | 0.30μs
    TC3 w=8,h=6         | 0.62μs       | 0.50μs      | 0.30μs
    대형 w=1000,h=3     | 0.46μs       | 0.46μs      | 0.48μs
    대형 w=500,h=500    | 25.70μs      | 54.59μs     | 0.42μs

    ref가 압도적인 이유: 탐색 없이 O(1) 계산
    two가 large에서 느린 이유:
        h=3~border//2 모두 검사 (약수 필터 없음)
        w=h=500이면 497회 순회
    one은 area%h 약수 필터로 실제 검사 횟수 적음
================================================================================
[내 초기 풀이]
    solution_mine_one: 면적 약수 탐색 (isqrt까지 순회, 약수 필터)
    solution_mine_two: 둘레 합 기반 탐색 (border//2까지 순회)

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Sub
                       약수 탐색으로 불필요 연산 줄임, 완전탐색 의도 명확
    solution_mine_two: 순회 범위가 one보다 넓어 대형 케이스에서 느림
                       border//2 범위로 불필요 h값도 모두 검사
    solution_ref:      이차방정식 근의 공식 O(1) - Best
                       "합과 곱이 알려진 두 미지수" → 이차방정식 환원
================================================================================
[복잡도 분석]
    A = brown + yellow (최대 2,005,000)

    Mine_one - 시간: O(sqrt(A)) | 공간: O(1) - isqrt(A)까지 약수 탐색
    Mine_two - 시간: O(s)       | 공간: O(1) - s=border//2 = (brown/2)+2 ≤ 2502
    Ref      - 시간: O(1)       | 공간: O(1) - 근의 공식 상수 연산
    Best     - 시간: O(1)       | 공간: O(1) - Ref와 동일
    Sub      - 시간: O(sqrt(A)) | 공간: O(1) - Mine_one과 동일
"""

import math
import time


# ================================================================================
# Mine solution one - 면적 약수 탐색
# ================================================================================
def solution_mine_one(brown: int, yellow: int) -> list[int]:
    """
    전체 면적의 약수를 탐색하며 조건을 만족하는 w, h를 찾는 초기 풀이

    area = w * h = brown + yellow:
        w, h는 area의 약수 쌍
        h를 순회하며 w = area // h로 쌍 구성

    탐색 범위:
        h >= 3: 내부 노란색 격자 존재 위해 h 최소 3 (위아래 갈색 1칸씩)
        h <= isqrt(area): 약수 쌍 성질 (h <= sqrt(area)이면 w >= sqrt(area))

    검증: (w-2) * (h-2) == yellow
        테두리 제외 내부 격자 = 노란색 격자 수
    """
    area = brown + yellow

    for h in range(3, math.isqrt(area) + 1):
        if area % h == 0:
            w = area // h
            if (w - 2) * (h - 2) == yellow:
                return [w, h]


# ================================================================================
# Mine solution two - 둘레 합(w+h) 기반 탐색
# ================================================================================
def solution_mine_two(brown: int, yellow: int) -> list[int]:
    """
    w+h 합을 이용해 h를 순회하며 조건을 만족하는 w, h를 찾는 풀이

    border = w + h = (brown // 2) + 2:
        내부 노란색 공식에서 유도

    탐색 범위:
        h = 3 ~ border // 2
        border // 2 초과 시 h > w가 되어 가로 >= 세로 조건 위배

    mine_one 대비:
        약수 필터(area%h) 없어 순회마다 모두 검사
        w=h 대형 케이스에서 mine_one보다 느림
    """
    border = (brown // 2) + 2

    for h in range(3, (border // 2) + 1):
        w = border - h
        if (w - 2) * (h - 2) == yellow:
            return [w, h]


# ================================================================================
# Ref solution - 이차방정식 근의 공식 O(1)
# ================================================================================
def solution_ref(brown: int, yellow: int) -> list[int]:
    """
    w, h를 이차방정식의 두 실근으로 보고 근의 공식으로 직접 구하는 풀이

    수식:
        s = w + h = (brown + 4) // 2
        p = w * h = brown + yellow
        x² - sx + p = 0 → x = (s ± sqrt(s²-4p)) / 2

    근의 공식 선택 기준:
        "합(s)과 곱(p)이 동시에 알려진 두 미지수"
        → (x-w)(x-h) = x² - (w+h)x + wh = 0 이차방정식으로 환원 가능
        → 탐색 없이 O(1)에 직접 계산

    discriminant = isqrt(s² - 4p):
        판별식: 실근 존재 보장 (유효 입력만 주어짐)
        w = (s + discriminant) // 2 (가로, 더 큰 값)
        h = (s - discriminant) // 2 (세로, 더 작은 값)
    """
    s = (brown + 4) // 2
    p = brown + yellow
    discriminant = math.isqrt(s ** 2 - 4 * p)
    w = (s + discriminant) // 2
    h = (s - discriminant) // 2
    return [w, h]


# ================================================================================
# Best solution - 이차방정식 근의 공식 (ref 주석 보강)
# ================================================================================
def solution_best(brown: int, yellow: int) -> list[int]:
    """
    이차방정식 근의 공식으로 O(1)에 w, h를 구하는 최적 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        O(1): 탐색 없이 상수 시간
        대형 케이스(w=h=500): mine_one 25.70μs, mine_two 54.59μs 대비 0.42μs
        "합과 곱이 알려진 두 미지수" 패턴 인식 → 이차방정식 환원
    """
    s = (brown + 4) // 2
    p = brown + yellow
    discriminant = math.isqrt(s ** 2 - 4 * p)
    w = (s + discriminant) // 2
    h = (s - discriminant) // 2
    return [w, h]


# ================================================================================
# Sub solution - 면적 약수 탐색 (mine_one 주석 보강)
# ================================================================================
def solution_sub(brown: int, yellow: int) -> list[int]:
    """
    완전탐색으로 면적 약수를 순회해 조건을 만족하는 w, h를 찾는 서브 풀이

    Best 대비 특징:
        약수 탐색: 탐색 과정이 코드에 명시적으로 드러남
        isqrt 상한으로 탐색 범위 최적화 (약수 쌍 성질)
        (w-2)*(h-2)==yellow 검증으로 노란색 격자 조건 직접 확인
        O(sqrt(A)): 대형 케이스에서 Best O(1) 대비 느릴 수 있음
    """
    area = brown + yellow

    for h in range(3, math.isqrt(area) + 1):
        if area % h == 0:
            w = area // h
            if (w - 2) * (h - 2) == yellow:
                return [w, h]


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """다섯 풀이의 정확성과 성능을 동시에 검증한다."""

    test_cases: list[tuple[int, int, list[int]]] = [
        # (brown, yellow, 기댓값)
        # 공식 예시
        (10,  2,      [4, 3]),
        (8,   1,      [3, 3]),
        (24,  24,     [8, 6]),
        # 추가 케이스:
        # 대형 w=1000,h=3: brown=2*(1000+3)-4=2002, yellow=998*1=998
        (2002, 998,   [1000, 3]),
        # 대형 w=500,h=500: brown=2*(500+500)-4=1996, yellow=498*498=248004
        (1996, 248004, [500, 500]),
    ]

    solutions = [
        ("Mine_one (면적약수)  ", solution_mine_one),
        ("Mine_two (둘레합)    ", solution_mine_two),
        ("Ref      (근의공식)  ", solution_ref),
        ("Best     (근의공식)  ", solution_best),
        ("Sub      (면적약수)  ", solution_sub),
    ]

    # 워밍업 스텝
    _b, _y, _ = test_cases[0]
    for _, func in solutions:
        func(_b, _y)

    print("=" * 66)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (brown, yellow, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(brown, yellow)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
