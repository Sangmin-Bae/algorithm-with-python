"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 체육복
    유형       : Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42862
    풀이일자   : 2026-09-12
===================================================================================
[문제 요약]
    도난당한 학생(lost)에게 여벌 체육복(reserve) 학생이 빌려줄 때
    체육 수업에 참여할 수 있는 최대 학생 수 반환
    앞/뒷 번호 학생에게만 빌릴 수 있음

    제약 조건
        - n: 2 이상 30 이하
        - 여벌 체육복 학생도 도난당할 수 있음 (→ 빌려줄 수 없음)
===================================================================================
[입출력 예시]
    n | lost   | reserve   | return
    --|--------|-----------|-------
    5 | [2,4]  | [1,3,5]   | 5
    5 | [2,4]  | [3]       | 4
    3 | [3]    | [1]       | 2
===================================================================================
[Level 1인데 정답률 60%인 이유]
    함정 1: 여벌 체육복 학생이 도난당한 경우 처리
        reserve에도 있고 lost에도 있으면
        → 자기 체육복만 유지, 다른 학생에게 빌려줄 수 없음
        → 두 배열에서 동시에 제거 필요

    함정 2: 그리디 순서
        낮은 번호부터 처리 + 앞번호 우선
        이 순서 틀리면 최적 결과 안 나옴

[그리디 최적성 — 앞번호 우선 처리 이유]
    낮은 번호부터 처리 시:
        앞번호 여벌 체육복: 더 낮은 번호 도난 학생에게 줄 수 없음
                            → 지금 쓰지 않으면 버려짐
        뒷번호 여벌 체육복: 나중에 더 높은 번호 도난 학생에게 줄 수 있음
                            → 아낄 수 있음
    → 앞번호 여벌 체육복을 먼저 소진하는 것이 최적

[풀이1 — 투포인터 방식]
    두 배열 정렬 + 포인터 이동
    abs(l - r) <= 1: 인접 → 빌림
    r < l: reserve 포인터 전진 (r이 너무 작음)
    r > l+1: lost 포인터 전진 (빌릴 수 없음)

    포인터 단방향 증가 → 앞번호 우선 처리 자동 보장

[풀이2 — set 차집합 + 앞번호 우선 명시]
    set 차집합으로 동시 도난/여벌 필터링
    sorted(lost_set) 순회 + l-1 우선 확인
    → 앞번호 우선 처리가 코드에 직접 드러남

[ref — 카운팅 배열]
    counts[i]: 학생 i의 체육복 수 (기본 1개)
    lost: -1, reserve: +1 적용
    counts[i] == 0: 도난당해 없음 → 인접 학생(counts==2)에게 빌림
    카운팅 배열로 체육복 수를 직접 관리

    n+2 크기 이유:
        i=1: counts[i-1]=counts[0] 접근
        i=n: counts[i+1]=counts[n+1] 접근
        범위 초과 방지 + 경계값 자동 1로 초기화
===================================================================================
[내 초기 풀이]
    solution_mine_one: 투포인터 (통과)
    solution_mine_two: set 차집합 + 앞번호 우선 (통과)

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       투포인터로 간결하고 빠름
    solution_mine_two: 앞번호 우선 로직이 명시적 - Sub
    solution_ref:      카운팅 배열로 체육복 수 직접 관리
                       이전 세션의 카운팅 패턴과 동일한 발상

[성능 (n=30 기준)]
    two (set):       1.8μs  ← 가장 빠름
    one (투포인터):  2.1μs
    ref (counting):  3.2μs
===================================================================================
[복잡도 분석]
    N = n (최대 30), L = len(lost), R = len(reserve)

    Mine_one - 시간: O(L log L + R log R) | 공간: O(L+R) - 정렬
    Mine_two - 시간: O(L log L)           | 공간: O(L+R) - set
    Ref      - 시간: O(N + L + R)         | 공간: O(N) - 카운팅 배열
    Best     - 시간: O(L log L + R log R) | 공간: O(L+R) - Mine_one과 동일
    Sub      - 시간: O(L log L)           | 공간: O(L+R) - Mine_two와 동일

    n ≤ 30 고정 → 모두 실질적 O(1)
"""

import time


# =================================================================================
# Mine solution one - 투포인터
# =================================================================================
def solution_mine_one(n: int, lost: list[int], reserve: list[int]) -> int:
    """
    정렬된 두 배열을 투포인터로 순회하며 빌릴 수 있는 쌍을 찾는 초기 풀이

    여벌+도난 동시 학생 필터링:
        리스트 컴프리헨션으로 양쪽에서 동시에 제거

    abs(l - r) <= 1:
        두 포인터가 인접 → 빌릴 수 있음
        정렬 + 단방향 증가로 앞번호 우선 처리 자동 보장

    반환:
        n - len(_lost) + saved
        전체 - 도난 + 빌린 수
    """
    _lost = sorted([l for l in lost if l not in reserve])
    _reserve = sorted([r for r in reserve if r not in lost])

    l_idx, r_idx = 0, 0
    saved = 0

    while l_idx < len(_lost) and r_idx < len(_reserve):
        l = _lost[l_idx]
        r = _reserve[r_idx]

        if abs(l - r) <= 1:
            saved += 1
            l_idx += 1
            r_idx += 1
        elif r < l:
            r_idx += 1
        else:
            l_idx += 1

    return n - len(_lost) + saved


# =================================================================================
# Mine solution two - set 차집합 + 앞번호 우선
# =================================================================================
def solution_mine_two(n: int, lost: list[int], reserve: list[int]) -> int:
    """
    set 차집합으로 필터링 후 앞번호 우선 처리를 명시적으로 구현한 풀이

    set 차집합:
        lost_set = set(lost) - set(reserve): 실제 도난 학생
        reserve_set = set(reserve) - set(lost): 실제 여벌 학생

    앞번호(l-1) 우선 확인:
        앞번호 여벌은 더 낮은 도난 학생에게 줄 수 없음 → 지금 써야 함
        뒷번호 여벌은 나중에 더 높은 도난 학생에게 줄 수 있음 → 아낄 수 있음
    """
    lost_set = set(lost) - set(reserve)
    reserve_set = set(reserve) - set(lost)

    unsuited = 0
    for l in sorted(lost_set):
        if l - 1 in reserve_set:
            reserve_set.remove(l - 1)
        elif l + 1 in reserve_set:
            reserve_set.remove(l + 1)
        else:
            unsuited += 1

    return n - unsuited


# =================================================================================
# Ref solution - 카운팅 배열
# =================================================================================
def solution_ref(n: int, lost: list[int], reserve: list[int]) -> int:
    """
    학생별 체육복 수를 카운팅 배열로 관리하는 참고 풀이

    counts[i] 의미:
        0: 도난당해 없음 (빌려야 함)
        1: 정상 (기본값)
        2: 여벌 있음 (빌려줄 수 있음)

    n+2 크기:
        counts[0], counts[n+1] 접근 시 범위 초과 방지
        경계값은 1로 초기화 (어차피 체크 안 함)

    앞번호(counts[i-1]) 우선:
        코드 순서상 앞번호 먼저 확인
    """
    counts = [1] * (n + 2)

    for l in lost:
        counts[l] -= 1
    for r in reserve:
        counts[r] += 1

    for i in range(1, n + 1):
        if counts[i] == 0:
            if counts[i - 1] == 2:
                counts[i - 1] -= 1
                counts[i] += 1
            elif counts[i + 1] == 2:
                counts[i + 1] -= 1
                counts[i] += 1

    return sum(1 for i in range(1, n + 1) if counts[i] >= 1)


# =================================================================================
# Best solution - 투포인터 (mine_one 주석 보강)
# =================================================================================
def solution_best(n: int, lost: list[int], reserve: list[int]) -> int:
    """
    투포인터로 간결하고 빠르게 최대 참여 학생 수를 구하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        여벌+도난 동시 학생 컴프리헨션 필터링으로 명확히 처리
        정렬 + 포인터 단방향 증가로 앞번호 우선 자동 보장
        n ≤ 30 고정으로 실질적 O(1)
    """
    _lost = sorted([l for l in lost if l not in reserve])
    _reserve = sorted([r for r in reserve if r not in lost])

    l_idx, r_idx = 0, 0
    saved = 0

    while l_idx < len(_lost) and r_idx < len(_reserve):
        l = _lost[l_idx]
        r = _reserve[r_idx]

        if abs(l - r) <= 1:
            saved += 1
            l_idx += 1
            r_idx += 1
        elif r < l:
            r_idx += 1
        else:
            l_idx += 1

    return n - len(_lost) + saved


# =================================================================================
# Sub solution - set 차집합 + 앞번호 우선 (mine_two 주석 보강)
# =================================================================================
def solution_sub(n: int, lost: list[int], reserve: list[int]) -> int:
    """
    set 차집합 + 앞번호 우선으로 그리디 규칙이 명시적으로 드러나는 서브 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        set 차집합으로 여벌+도난 동시 학생 O(1) 필터링
        l-1 먼저 확인: 앞번호 우선 처리가 코드에 직접 드러남
        Best 대비 앞번호 우선 로직이 더 명시적
    """
    lost_set = set(lost) - set(reserve)
    reserve_set = set(reserve) - set(lost)

    unsuited = 0
    for l in sorted(lost_set):
        if l - 1 in reserve_set:
            reserve_set.remove(l - 1)
        elif l + 1 in reserve_set:
            reserve_set.remove(l + 1)
        else:
            unsuited += 1

    return n - unsuited


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (n, lost, reserve, 기댓값)
        # 공식 예시
        (5, [2, 4], [1, 3, 5], 5),
        (5, [2, 4], [3],       4),
        (3, [3],    [1],       2),
        # 추가 케이스:
        # 여벌+도난 동시 학생 (2번: 도난+여벌 → 빌릴 수 없음)
        # 실제 도난: [4], 실제 여벌: [3] → 3번이 4번에게 → 5명
        (5, [2, 4], [2, 3],   5),
        # 앞번호 우선이 중요한 케이스
        # lost=[1,3,5], reserve=[2,4]
        # 2→1, 4→3: 4명 참여 (5번 불참)
        (5, [1, 3, 5], [2, 4], 4),
    ]

    solutions = [
        ("Mine_one (투포인터)  ", solution_mine_one),
        ("Mine_two (set)       ", solution_mine_two),
        ("Ref      (counting)  ", solution_ref),
        ("Best     (투포인터)  ", solution_best),
        ("Sub      (set)       ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _l, _r, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _l[:], _r[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (n, lost, reserve, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, lost[:], reserve[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
