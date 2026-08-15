"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : [PCCE 기출문제] 9번 / 지폐 접기
    유형       : Greedy / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/340199
    풀이일자   : 2026-08-15
===================================================================================
[문제 요약]
    지폐(bill)를 지갑(wallet)에 넣기 위해 최소 몇 번 접어야 하는지 반환
    접을 때: 항상 긴 쪽을 반으로 접음, 홀수는 소수점 이하 버림
    지폐는 90도 돌려서 넣을 수 있음

    제약 조건
        - wallet, bill 길이 = 2
        - wallet 원소: 10 이상 100 이하
        - bill 원소: 10 이상 2,000 이하
===================================================================================
[입출력 예시]
    wallet   | bill        | result
    ---------|-------------|-------
    [30, 15] | [26, 17]    | 1
    [50, 50] | [100, 241]  | 4
===================================================================================
[핵심 — 긴 쪽과 짧은 쪽 매칭]
    지폐와 지갑의 긴 쪽끼리, 짧은 쪽끼리 비교해야 함
    지폐의 긴 쪽을 지갑의 짧은 쪽과 비교하면 항상 들어가지 않을 수 있음

    지폐를 90도 돌려서 넣을 수 있다는 조건:
        풀이1~3: 정렬/min/max로 긴쪽-짧은쪽 정규화
        ref: 두 방향(그대로 / 90도 회전) 모두 직접 비교

    손 추적 [50,50], [100,241]:
        b1=100, b2=241 → b2>b1 → b2//=2=120, answer=1
        b1=100, b2=120 → b2>b1 → b2//=2=60, answer=2
        b1=100, b2=60  → b1>b2 → b1//=2=50, answer=3
        b1=50,  b2=60  → b2>b1 → b2//=2=30, answer=4
        (50<=50 and 30<=50) → 종료, return 4 ✓

[실측 결과 — 500,000회 반복]
    케이스              | one(min/max) | two(sorted반복) | three(swap) | ref(직접비교)
    --------------------|-------------|-----------------|-------------|-------------
    TC1 [30,15],[26,17] | 1.01μs      | 0.75μs          | 0.55μs      | 0.27μs
    TC2 [50,50],[100,241]| 2.18μs     | 1.53μs          | 0.91μs      | 0.39μs
    최악 [10,10],[2000,2000]| 5.99μs   | 3.77μs          | 1.19μs      | 0.98μs

    ref가 가장 빠른 이유:
        while 조건이 단순 정수 비교 4개
        함수 호출(min/max/sorted) 오버헤드 없음

    one이 two보다 느린 이유:
        min×2 + max×2 = 4회 함수 호출/루프
        sorted() 1회 호출보다 오버헤드 큼

    three가 two보다 빠른 이유:
        초기 정렬 1회 + while 내부에서 swap(정수 치환)만 수행
        sorted() 반복 없음

[의사코드 대비 개선 방향]
    의사코드(풀이1 기반): min/max 4회/루프
    풀이2: sorted 1회/루프 (함수 호출 감소)
    풀이3: 초기 1회 정렬 + swap (루프 내 함수 없음)
    ref:   초기 정렬 없음 + 두 방향 직접 비교 (발상 전환)
===================================================================================
[내 초기 풀이]
    solution_mine_one  : min/max + while
    solution_mine_two  : 초기 정렬 + while 내 sorted 반복
    solution_mine_three: 초기 정렬 + while 내 swap

[개선 포인트]
    solution_mine_one  : 루프당 min/max 4회 호출 → 개선 가능
    solution_mine_two  : sorted 반복 → swap으로 개선 가능
    solution_mine_three: 개선 필요 없음 - Sub
                         초기 정렬 1회 + swap, 변수명 명시적
    solution_ref       : 개선 필요 없음 - Best
                         발상 전환: 두 방향 직접 비교로 정렬 완전 제거
===================================================================================
[복잡도 분석]
    K = 접는 횟수 (최대 log₂(2000/10) ≈ 8회, 실제 최대 약 16회)

    Mine_one   - 시간: O(K) | 공간: O(1) - min/max 4회/루프
    Mine_two   - 시간: O(K) | 공간: O(1) - sorted 1회/루프
    Mine_three - 시간: O(K) | 공간: O(1) - swap O(1)/루프
    Ref        - 시간: O(K) | 공간: O(1) - 단순 정수 비교
    Best       - 시간: O(K) | 공간: O(1) - Ref와 동일
    Sub        - 시간: O(K) | 공간: O(1) - Mine_three와 동일

    K 최대 16 → 모두 실질적으로 O(1)
    실측 차이는 루프당 함수 호출 횟수의 상수 인자
"""

import time


# =================================================================================
# Mine solution one - min/max + while
# =================================================================================
def solution_mine_one(wallet: list[int], bill: list[int]) -> int:
    """
    min/max로 긴쪽-짧은쪽을 구분해 비교하는 초기 풀이

    min(bill) vs min(wallet): 짧은 쪽 비교
    max(bill) vs max(wallet): 긴 쪽 비교

    루프당 min×2 + max×2 = 4회 함수 호출
    bill 원소가 2개이므로 각 O(1)이지만 반복 오버헤드 존재
    """
    answer = 0

    while min(bill) > min(wallet) or max(bill) > max(wallet):
        if bill[0] > bill[1]:
            bill[0] //= 2
        else:
            bill[1] //= 2
        answer += 1

    return answer


# =================================================================================
# Mine solution two - 초기 정렬 + while 내 sorted 반복
# =================================================================================
def solution_mine_two(wallet: list[int], bill: list[int]) -> int:
    """
    정렬로 긴쪽-짧은쪽을 구분하고 접을 때마다 재정렬하는 풀이

    초기 정렬 후 인덱스 0=짧은쪽, 1=긴쪽
    접은 후 bill 원소의 순서가 바뀔 수 있어 재정렬 필요

    mine_one 대비:
        min/max 4회 → sorted 1회로 감소
        단, while 내부에서 sorted 반복 발생
    """
    answer = 0
    wallet, bill = sorted(wallet), sorted(bill)

    while bill[0] > wallet[0] or bill[1] > wallet[1]:
        if bill[0] > bill[1]:
            bill[0] //= 2
        else:
            bill[1] //= 2
        answer += 1
        bill = sorted(bill)

    return answer


# =================================================================================
# Mine solution three - 초기 정렬 + swap
# =================================================================================
def solution_mine_three(wallet: list[int], bill: list[int]) -> int:
    """
    초기 1회 정렬 후 while 내부에서 swap으로 min/max 관계를 유지하는 풀이

    b_max를 항상 반으로 접음 (큰 쪽을 접는 원칙)
    접은 후 b_min > b_max이면 swap으로 min/max 재정렬
    → while 내부에서 sorted() 호출 없음

    mine_two 대비:
        sorted 반복 → 정수 swap O(1)로 대체
        함수 호출 오버헤드 제거
    """
    answer = 0
    w_min, w_max = sorted(wallet)
    b_min, b_max = sorted(bill)

    while b_min > w_min or b_max > w_max:
        b_max //= 2
        answer += 1
        if b_min > b_max:
            b_min, b_max = b_max, b_min

    return answer


# =================================================================================
# Ref solution - 두 방향 직접 비교 (정렬 없음)
# =================================================================================
def solution_ref(wallet: list[int], bill: list[int]) -> int:
    """
    지폐를 그대로 또는 90도 돌렸을 때 두 방향을 모두 직접 비교하는 풀이

    발상 전환:
        정렬로 긴쪽-짧은쪽 정규화 대신
        (그대로: b1<=w1 and b2<=w2) or (90도: b1<=w2 and b2<=w1)
        두 경우 모두 직접 체크

    루프당 단순 정수 비교만 수행 → 함수 호출 오버헤드 없음
    실측 가장 빠름 (mine_one 대비 최악 케이스에서 6배 차이)
    """
    answer = 0
    w1, w2 = wallet[0], wallet[1]
    b1, b2 = bill[0], bill[1]

    while not ((b1 <= w1 and b2 <= w2) or (b1 <= w2 and b2 <= w1)):
        if b1 > b2:
            b1 //= 2
        else:
            b2 //= 2
        answer += 1

    return answer


# =================================================================================
# Best solution - 두 방향 직접 비교 (ref 주석 보강)
# =================================================================================
def solution_best(wallet: list[int], bill: list[int]) -> int:
    """
    두 방향 직접 비교로 정렬 없이 O(K) 시간, O(1) 공간의 최적 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        정렬/min/max 없이 단순 정수 비교만 사용
        루프당 비교 연산만 → 함수 호출 오버헤드 없음
        실측 최악 케이스: mine_one 5.99μs → 0.98μs (6배 차이)
        "그대로 또는 90도 돌려서"를 조건문으로 직접 표현
    """
    answer = 0
    w1, w2 = wallet[0], wallet[1]
    b1, b2 = bill[0], bill[1]

    while not ((b1 <= w1 and b2 <= w2) or (b1 <= w2 and b2 <= w1)):
        if b1 > b2:
            b1 //= 2
        else:
            b2 //= 2
        answer += 1

    return answer


# =================================================================================
# Sub solution - 초기 정렬 + swap (mine_three 주석 보강)
# =================================================================================
def solution_sub(wallet: list[int], bill: list[int]) -> int:
    """
    초기 정렬 1회 + swap으로 루프 내 함수 호출 없이 처리하는 서브 풀이

    Best 대비 특징:
        w_min, w_max, b_min, b_max 변수명 → 역할이 명시적
        초기 정렬 1회로 긴쪽-짧은쪽 정규화
        b_max를 항상 접고 swap으로 min/max 관계 유지
        Best보다 느리나 변수명으로 의도가 더 명확
    """
    answer = 0
    w_min, w_max = sorted(wallet)
    b_min, b_max = sorted(bill)

    while b_min > w_min or b_max > w_max:
        b_max //= 2
        answer += 1
        if b_min > b_max:
            b_min, b_max = b_max, b_min

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], list[int], int]] = [
        # (wallet, bill, 기댓값)
        # 공식 예시
        ([30, 15], [26, 17],   1),
        ([50, 50], [100, 241], 4),
        # 추가 케이스:
        ([10, 10], [10, 10],   0),   # 이미 들어감
        ([100, 100], [10, 10], 0),   # 작은 지폐
        ([10, 10], [2000, 2000], 16), # 최악 케이스
    ]

    solutions = [
        ("Mine_one   (min/max)    ", solution_mine_one),
        ("Mine_two   (sorted반복) ", solution_mine_two),
        ("Mine_three (swap)       ", solution_mine_three),
        ("Ref        (직접비교)   ", solution_ref),
        ("Best       (직접비교)   ", solution_best),
        ("Sub        (swap)       ", solution_sub),
    ]

    # 워밍업 스텝
    _w, _b, _ = test_cases[0]
    for _, func in solutions:
        func(_w[:], _b[:])

    print("=" * 68)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (wallet, bill, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(wallet[:], bill[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
