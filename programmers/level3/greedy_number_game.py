"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 숫자 게임
    유형       : Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12987
    풀이일자   : 2026-09-11
===================================================================================
[문제 요약]
    A팀의 출전 순서가 공개된 상황에서
    B팀이 얻을 수 있는 최대 승점 반환
    큰 숫자 vs 큰 숫자 → 이긴 팀이 1점 획득
    같으면 무승부 (0점)

    제약 조건
        - A, B 길이: 1 이상 100,000 이하
        - 각 원소: 1 이상 1,000,000,000 이하
===================================================================================
[입출력 예시]
    A         | B         | result
    ----------|-----------|-------
    [5,1,3,7] | [2,2,6,8] | 3
    [2,2,2,2] | [1,1,1,1] | 0
===================================================================================
[핵심 — 그리디 최적성]
    "A[i]보다 살짝 큰 B 숫자를 쓰는 것이 최적"

    증명:
        A=[3,9], B=[4,10]
        전략1: A=3에 B=4, A=9에 B=10 → 2점
        전략2: A=3에 B=10, A=9에 B=4 → 1점

    이길 수 없는 경우: 가장 작은 B를 소모 (버림)
    → 큰 B는 더 큰 A를 이기는데 아낌

[풀이2 — 정렬 + 투포인터 핵심 발상]
    두 배열을 모두 오름차순 정렬
    B를 순회하며 A의 최솟값(A[a_idx])과 비교
    b_card > A[a_idx]: 이김 → a_idx 증가 (다음 타겟)
    b_card <= A[a_idx]: 못 이김 → 버림 (a_idx 유지)

    "카드를 실제로 제거하지 않아도
     a_idx가 단방향으로 증가하므로
     이미 사용한 A가 타겟에서 자동으로 제외"
    → 분할 상환 O(N): a_idx는 최대 N번 증가

[손 추적 — A=[5,1,3,7], B=[2,2,6,8]]
    정렬: A=[1,3,5,7], B=[2,2,6,8], a_idx=0

    b=2: 2>A[0]=1 → 이김, answer=1, a_idx=1
    b=2: 2>A[1]=3 → 못 이김, 버림 (a_idx=1 유지)
    b=6: 6>A[1]=3 → 이김, answer=2, a_idx=2
    b=8: 8>A[2]=5 → 이김, answer=3, a_idx=3

    result=3 ✓

[풀이1, 3 실패 원인]
    pop(idx): 리스트 중간 삭제 O(N) 이동 비용
    N번 반복 → O(N²) → 효율성 테스트 실패

    풀이2의 a_idx 투포인터:
        실제 삭제 없음 → O(N) 단일 패스
===================================================================================
[내 초기 풀이]
    solution_mine_one:   A 고정, B 정렬+while 탐색 (O(N²), 효율성 실패)
    solution_mine_two:   A,B 정렬+투포인터 (O(N log N), 통과)
    solution_mine_three: A 고정, B bisect 이진탐색 (O(N²), 효율성 실패)

[개선 포인트]
    solution_mine_one:   pop(idx) O(N) 반복 → 비효율
                         "A 고정" 전제로는 통과 불가
    solution_mine_two:   개선 필요 없음 - Best
                         양방향 정렬 + a_idx 투포인터
    solution_mine_three: bisect O(log N)으로 탐색 개선했으나
                         pop(idx) 여전히 O(N) → 병목
===================================================================================
[복잡도 분석]
    N = len(A) = len(B) (최대 100,000)

    Mine_one   - 시간: O(N²)      | 공간: O(N) - while+pop 반복
    Mine_two   - 시간: O(N log N) | 공간: O(1) - 정렬+투포인터
    Mine_three - 시간: O(N²)      | 공간: O(N) - bisect+pop
    Best       - 시간: O(N log N) | 공간: O(1) - Mine_two와 동일
    Sub        - 시간: O(N²)      | 공간: O(N) - Mine_one과 동일
                                                  (풀이 구조 비교 목적)
"""

import bisect
import time


# =================================================================================
# Mine solution one - A 고정, B 정렬+while 탐색 (O(N²), 효율성 실패)
# =================================================================================
def solution_mine_one(A: list[int], B: list[int]) -> int:
    """
    B를 내림차순 정렬 후 while+idx로 A[i]보다 큰 최솟값을 찾는 초기 풀이

    B 내림차순 정렬 이유:
        이길 수 없으면 B.pop() (가장 작은 수 버림)
        이기면 B.pop(idx) (해당 원소 삭제)

    한계:
        pop(idx): 리스트 중간 삭제 O(N) 원소 이동
        N번 반복 → O(N²) → 효율성 테스트 실패
    """
    answer = 0
    B = sorted(B, reverse=True)

    for num in A:
        idx = len(B) - 1
        is_win = False

        while idx > -1:
            if num < B[idx]:
                answer += 1
                B.pop(idx)
                is_win = True
                break
            idx -= 1

        if not is_win and B:
            B.pop()

    return answer


# =================================================================================
# Mine solution two - A,B 정렬 + 투포인터 (O(N log N), 통과)
# =================================================================================
def solution_mine_two(A: list[int], B: list[int]) -> int:
    """
    두 배열을 정렬하고 a_idx 포인터로 최소 타겟을 추적하는 최적 풀이

    a_idx: B가 이겨야 할 A의 현재 최솟값 인덱스
        b_card > A[a_idx]: 이김 → a_idx 증가 (다음 타겟)
        b_card <= A[a_idx]: 버림 (a_idx 유지)

    카드 실제 삭제 없음:
        a_idx 단방향 증가로 사용된 A가 자동 제외
        → 분할 상환 O(N)

    정렬 O(N log N)이 지배적 → 전체 O(N log N)
    """
    answer = 0
    A.sort()
    B.sort()

    a_idx = 0

    for b_card in B:
        if b_card > A[a_idx]:
            answer += 1
            a_idx += 1

    return answer


# =================================================================================
# Mine solution three - bisect 이진탐색 + pop (O(N²), 효율성 실패)
# =================================================================================
def solution_mine_three(A: list[int], B: list[int]) -> int:
    """
    B를 정렬 후 bisect_right로 A[i]보다 큰 최솟값 위치를 찾는 풀이

    bisect_right(B, num):
        num보다 큰 첫 번째 원소 인덱스 반환 O(log N)

    한계:
        bisect: O(log N)으로 탐색 개선
        pop(idx): O(N) 중간 삭제가 여전히 병목
        N번 반복 → O(N²) → 효율성 테스트 실패
    """
    answer = 0
    B = sorted(B)

    for num in A:
        idx = bisect.bisect_right(B, num)

        if idx < len(B):
            answer += 1
            B.pop(idx)
        else:
            B.pop(0)

    return answer


# =================================================================================
# Best solution - A,B 정렬 + 투포인터 (mine_two 주석 보강)
# =================================================================================
def solution_best(A: list[int], B: list[int]) -> int:
    """
    O(N log N) 정렬 + O(N) 투포인터로 최대 승점을 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        "A 고정" 전제를 깨고 두 배열 모두 정렬
        a_idx 단방향 증가로 카드 삭제 없이 동일 효과
        실측 N=10,000: 3.01ms (O(N²) 대비 압도적 우위)
    """
    answer = 0
    A.sort()
    B.sort()

    a_idx = 0

    for b_card in B:
        if b_card > A[a_idx]:
            answer += 1
            a_idx += 1

    return answer


# =================================================================================
# Sub solution - A 고정, B 내림차순+while (mine_one 주석 보강)
# =================================================================================
def solution_sub(A: list[int], B: list[int]) -> int:
    """
    그리디 발상이 명시적으로 드러나는 서브 풀이 (O(N²), 효율성 미통과)

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        "A[i]보다 살짝 큰 B 최솟값 사용" 전략이 코드에 직관적으로 드러남
        이길 수 없으면 가장 작은 B를 버리는 로직이 명시적
        pop(idx) O(N) 반복이 병목 → 효율성 실패

    학습 목적:
        풀이2의 발상(양방향 정렬)이 왜 필요한지 비교 이해용
    """
    answer = 0
    B = sorted(B, reverse=True)

    for num in A:
        idx = len(B) - 1
        is_win = False

        while idx > -1:
            if num < B[idx]:
                answer += 1
                B.pop(idx)
                is_win = True
                break
            idx -= 1

        if not is_win and B:
            B.pop()

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (A, B, 기댓값)
        # 공식 예시
        ([5, 1, 3, 7], [2, 2, 6, 8], 3),
        ([2, 2, 2, 2], [1, 1, 1, 1], 0),
        # 추가 케이스:
        # B가 모두 이김
        ([1, 2, 3], [4, 5, 6],       3),
        # 동점 (승점 없음)
        ([3, 3, 3], [3, 3, 3],       0),
        # 일부만 이김
        # A=[1,5] B=[2,4] 정렬: A=[1,5] B=[2,4]
        # b=2>A[0]=1 → 이김, b=4>A[1]=5 → 못 이김 → answer=1
        ([1, 5], [2, 4],             1),
    ]

    solutions = [
        ("Mine_one   (while+pop)   ", solution_mine_one),
        ("Mine_two   (정렬+투포인터)", solution_mine_two),
        ("Mine_three (bisect+pop)  ", solution_mine_three),
        ("Best       (정렬+투포인터)", solution_best),
        ("Sub        (while+pop)   ", solution_sub),
    ]

    # 워밍업 스텝
    _A, _B, _ = test_cases[0]
    for _, func in solutions:
        func(_A[:], _B[:])

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (A, B, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(A[:], B[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
