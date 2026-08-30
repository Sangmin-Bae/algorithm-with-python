"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 주식가격
    유형       : Stack
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42584
    풀이일자   : 2026-08-30
===================================================================================
[문제 요약]
    초 단위로 기록된 주식가격 배열 prices에서
    각 가격이 떨어지지 않은 기간(초)을 반환

    제약 조건
        - prices 길이: 2 이상 100,000 이하
        - 가격: 1 이상 10,000 이하
===================================================================================
[입출력 예시]
    prices          | return
    ----------------|------------------
    [1, 2, 3, 2, 3] | [4, 3, 1, 1, 0]
===================================================================================
[핵심 — "뒤에 있는 큰 수 찾기"와 거울 관계]
    뒤에 있는 큰 수 찾기:
        "나보다 뒤에 있으면서 나보다 큰 첫 번째 수"
        → 단조 감소 스택

    주식가격:
        "나보다 뒤에 있으면서 나보다 작은 첫 번째 수"
        → 단조 증가 스택 (아래→위로 커지는 구조)

    스택에 인덱스를 담는 이유:
        가격이 떨어지는 순간 i - idx로 시간 차이 계산 필요
        가격(값)만 담으면 시간 계산 불가

[ref_one — 단조 증가 스택]
    손 추적 [1,2,3,2,3]:
        i=0: stack=[0]
        i=1: 1<=2 → stack=[0,1]
        i=2: 2<=3 → stack=[0,1,2]
        i=3: 3>2 → pop(2), answer[2]=3-2=1, stack=[0,1,3]
        i=4: 2<=3 → stack=[0,1,3,4]
        남은 스택: pop(4)→answer[4]=0, pop(3)→1, pop(1)→3, pop(0)→4
        → [4,3,1,1,0] ✓

[ref_two — 점프 DP (Bottom-up)]
    핵심 아이디어:
        prices[j] >= prices[i]이면 → i가 버티는 동안 j도 버팀
            → j가 꺾이는 시점 = i가 꺾이는 시점
            → answer[j]로 점프: j += answer[j]
        prices[j] < prices[i]이면 → answer[i] = j - i

    answer[j] == 0 처리:
        j가 마지막 위치 → 끝까지 버팀 → j = n-1로 이동

    뒤에서 앞으로 채우는 Bottom-up DP
    (탑다운 아님: 재귀 없음, 명시적 역방향 반복문)

    손 추적 [1,2,3,2,3]:
        i=3: j=4, prices[4]=3>=2, answer[4]=0 → j=4, break
             answer[3]=4-3=1
        i=2: j=3, prices[3]=2<3 → break
             answer[2]=3-2=1
        i=1: j=2→3→4(answer=0)→break, answer[1]=4-1=3
        i=0: j=1→4(answer=0)→break, answer[0]=4-0=4
        → [4,3,1,1,0] ✓

[실측 결과 — N=100,000, 100회]
    ref_one (단조스택): 9.44ms   ← 가장 빠름
    ref_two (점프DP):  11.18ms
    mine    (O(N²)):   N=100,000에서 측정 생략 (수분 이상 예상)
===================================================================================
[내 초기 풀이]
    solution_mine: brute force O(N²) 이중 반복문
                   논리는 정확하나 효율성 통과 불확실

[개선 포인트]
    solution_mine:    O(N²) → 단조 스택 O(N)으로 개선 필요
                      "뒤에 있는 큰 수 찾기"와 동일 패턴, 부등호 방향만 반대
    solution_ref_one: 단조 증가 스택 O(N) - Best
    solution_ref_two: 점프 DP O(N) 평균 - Sub
                      이전 계산값 재사용으로 불필요한 탐색 건너뜀
===================================================================================
[단조 스택 패턴 신호]
    "각 원소에 대해 뒤에서 가장 가까운 [크거나/작은] 원소를 찾아라"
    → 단조 스택 (감소 또는 증가)
    → O(N) 분할 상환 (push 1회, pop 최대 1회)
===================================================================================
[복잡도 분석]
    N = len(prices) (최대 100,000)

    Mine     - 시간: O(N²)  | 공간: O(1) - 이중 반복문
    Ref_one  - 시간: O(N)   | 공간: O(N) - 스택 최대 N개
    Ref_two  - 시간: O(N) 평균 | 공간: O(1) - 점프로 중복 탐색 건너뜀
    Best     - 시간: O(N)   | 공간: O(N) - Ref_one과 동일
    Sub      - 시간: O(N) 평균 | 공간: O(1) - Ref_two와 동일
"""

import time


# =================================================================================
# Mine solution - brute force O(N²) (효율성 통과 불확실)
# =================================================================================
def solution_mine(prices: list[int]) -> list[int]:
    """
    이중 반복문으로 각 가격이 떨어질 때까지 탐색하는 초기 풀이 (O(N²))

    answer[i]를 1씩 누적하다가 가격이 떨어지면 break:
        자연스럽게 "버틴 초 수"가 됨

    한계:
        O(N²): N=100,000이면 최악 10^10 연산
        효율성 테스트 통과 불확실
        "뒤에 있는 작은 수 찾기" = 단조 스택 패턴임을 캐치 못함
    """
    n = len(prices)
    answer = [0] * n

    for i in range(n - 1):
        for j in range(i + 1, n):
            answer[i] += 1
            if prices[i] > prices[j]:
                break

    return answer


# =================================================================================
# Ref solution one - 단조 증가 스택 O(N)
# =================================================================================
def solution_ref_one(prices: list[int]) -> list[int]:
    """
    단조 증가 스택으로 O(N)에 각 가격이 버틴 기간을 구하는 최적 풀이

    스택 = "아직 가격이 떨어지지 않은 인덱스들" (단조 증가 유지)
    새 가격 price 등장 시:
        stack[-1] 가격 > price → 가격 하락 → pop, 버틴 시간 = i - idx
        stack[-1] 가격 <= price → 아직 버팀 → 그대로 유지

    순회 종료 후 남은 스택:
        끝까지 가격이 안 떨어진 인덱스들
        버틴 시간 = (n-1) - idx

    "뒤에 있는 큰 수 찾기"와 거울 관계:
        큰 수 찾기: 단조 감소 스택, prices[stack[-1]] < price 조건
        주식가격:   단조 증가 스택, prices[stack[-1]] > price 조건
    """
    n = len(prices)
    answer = [0] * n
    stack = []

    for i, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            idx = stack.pop()
            answer[idx] = i - idx
        stack.append(i)

    while stack:
        idx = stack.pop()
        answer[idx] = (n - 1) - idx

    return answer


# =================================================================================
# Ref solution two - 점프 DP (Bottom-up)
# =================================================================================
def solution_ref_two(prices: list[int]) -> list[int]:
    """
    이미 계산된 answer[j]를 재사용해서 불필요한 탐색을 건너뛰는 Bottom-up DP

    핵심:
        prices[j] >= prices[i]: j가 버티는 동안 i도 버팀
            → j가 꺾이는 다음 위치 j+answer[j]로 점프
        prices[j] < prices[i]: 버틴 시간 = j - i

    answer[j] == 0 처리:
        j가 마지막 위치(끝까지 버팀) → j = n-1로 이동 후 break

    뒤에서 앞으로 채우는 Bottom-up DP:
        answer[j]가 확정된 상태에서 answer[i]를 계산
        (탑다운이 아닌 Bottom-up: 재귀 없음, 명시적 역방향 반복문)
    """
    n = len(prices)
    answer = [0] * n

    for i in range(n - 2, -1, -1):
        j = i + 1

        while j < n and prices[i] <= prices[j]:
            if answer[j] == 0:
                j = n - 1
                break
            j += answer[j]

        answer[i] = j - i

    return answer


# =================================================================================
# Best solution - 단조 증가 스택 (ref_one 주석 보강)
# =================================================================================
def solution_best(prices: list[int]) -> list[int]:
    """
    단조 증가 스택으로 O(N) 시간, O(N) 공간에 버틴 기간을 구하는 최적 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        분할 상환 O(N): 각 인덱스 push 1회, pop 최대 1회
        실측 N=100,000: 9.44ms (ref_two 11.18ms 대비 우위)
        "뒤에 있는 작은 수 찾기" → 단조 증가 스택 패턴
    """
    n = len(prices)
    answer = [0] * n
    stack = []

    for i, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            idx = stack.pop()
            answer[idx] = i - idx
        stack.append(i)

    while stack:
        idx = stack.pop()
        answer[idx] = (n - 1) - idx

    return answer


# =================================================================================
# Sub solution - 점프 DP (ref_two 주석 보강)
# =================================================================================
def solution_sub(prices: list[int]) -> list[int]:
    """
    점프 DP로 O(N) 평균 시간, O(1) 공간에 버틴 기간을 구하는 서브 풀이

    Best 대비 특징:
        추가 스택 없이 answer 배열만 사용 → O(1) 공간
        이미 계산된 answer[j]로 점프 → 중복 탐색 건너뜀
        뒤에서 앞으로 Bottom-up DP 방향
        실측 Best 대비 약 18% 느림
    """
    n = len(prices)
    answer = [0] * n

    for i in range(n - 2, -1, -1):
        j = i + 1

        while j < n and prices[i] <= prices[j]:
            if answer[j] == 0:
                j = n - 1
                break
            j += answer[j]

        answer[i] = j - i

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], list[int]]] = [
        # (prices, 기댓값)
        # 공식 예시
        # 손 추적: 1→끝까지=4, 2→끝까지=3, 3→1초후하락=1, 2→끝=1, 3→0
        ([1, 2, 3, 2, 3], [4, 3, 1, 1, 0]),
        # 추가 케이스:
        # 계속 하락
        ([3, 2, 1],        [1, 1, 0]),
        # 계속 상승
        ([1, 2, 3],        [2, 1, 0]),
        # 동일 가격
        ([2, 2, 2],        [2, 1, 0]),
    ]

    solutions = [
        ("Mine    (O(N²))     ", solution_mine),
        ("Ref_one (단조스택)  ", solution_ref_one),
        ("Ref_two (점프DP)    ", solution_ref_two),
        ("Best    (단조스택)  ", solution_best),
        ("Sub     (점프DP)    ", solution_sub),
    ]

    # 워밍업 스텝
    _p, _ = test_cases[0]
    for _, func in solutions:
        func(_p[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (prices, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(prices[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
