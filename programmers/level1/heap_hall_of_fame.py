"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 명예의 전당 (1)
    유형       : Heap
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/138477
    풀이일자   : 2026-07-07
===================================================================================
[문제 요약]
    매일 1명씩 점수 추가, 상위 k개 점수를 명예의 전당으로 유지
    매일 명예의 전당 최하위 점수를 반환

    제약 조건
        - k: 3 이상 100 이하
        - score 길이: 7 이상 1,000 이하
        - score[i]: 0 이상 2,000 이하
===================================================================================
[입출력 예시]
    k | score                             | result
    --|-----------------------------------|---------------------------
    3 | [10,100,20,150,1,100,200]         | [10,10,10,20,20,100,100]
    4 | [0,300,40,300,20,70,150,50,500,1000] | [0,0,0,0,20,40,70,70,150,300]
===================================================================================
[핵심 아이디어 — 명예의 전당 최하위 점수를 효율적으로 관리]
    매일 명예의 전당 최하위(k번째) 점수가 필요
    → 상위 k개 중 최솟값을 빠르게 조회/갱신하는 자료구조 필요

    자료구조별 접근 방식:
        완전탐색:  매번 전체 정렬 → O(N² log N) 전체
        정렬 유지: 최대 k+1개만 정렬 → O(Nk log k) 전체
        힙(heapq): 최솟값을 O(1) 조회, 삽입/삭제 O(log k) → O(N log k) 전체
        bisect:    이진탐색 삽입 O(log k), 삭제 O(k) → O(Nk) 전체

[heapq 최소 힙 동작 원리]
    Python heapq는 최소 힙(min-heap):
        hof[0]: 항상 최솟값 유지
        완전 이진트리 구조로 리스트에 저장 (정렬된 리스트 아님)

    heappush(hof, s):
        리스트 맨 뒤에 s 추가 → sift-up(부모와 비교하며 올라감)
        O(log k)

    heappop(hof):
        hof[0] 반환 → 마지막 원소를 루트로 이동 → sift-down
        O(log k)

    heappushpop(hof, s):
        heappush + heappop이지만 sift-up 과정 생략
        s를 루트 자리에 놓고 sift-down만 수행 → 더 효율적
        단, s < hof[0]이면 s를 그대로 반환 (힙 변경 없음)
        O(log k)

[bisect 음수 트릭 — solution_mine_five]
    bisect는 오름차순 정렬만 지원
    값에 음수(-s)를 적용하면 오름차순 정렬이 내림차순 효과
    → hof[-1]이 절댓값 최솟값 = 실제 최솟값
    → hof.pop()으로 O(1) 삭제 가능 (del hof[0]의 O(k) 회피)
    k≤100 제약에서 유의미한 차이는 아니나 개념적으로 의미 있는 최적화 시도
===================================================================================
[내 초기 풀이]
    solution_mine_one  : 매번 score[:i] 전체 정렬 (완전탐색)
    solution_mine_two  : hof를 k+1개로 제한하며 정렬
    solution_mine_three: heapq 최소 힙으로 k개 유지
    solution_mine_four : bisect 이진탐색 삽입 + del hof[0]
    solution_mine_five : bisect 음수 트릭으로 pop() O(1) 달성

[개선 포인트]
    solution_mine_one  : O(N² log N) → 규모 증가 시 비효율
    solution_mine_two  : O(Nk log k) → k≤100 실용적, 가독성 우위 → Sub
    solution_mine_three: O(N log k) → Best, 코딩테스트 힙 표준 패턴
    solution_mine_four : bisect O(log k) 삽입 + del O(k) 삭제
    solution_mine_five : bisect + 음수 트릭으로 O(1) 삭제, 개념 학습 목적

    heappop 동작 정정 (Simon 설명 보완):
        "앞의 부모 원소들을 한칸씩 앞으로" → 정확히는:
        마지막 원소를 루트(hof[0])로 이동 후 sift-down
        (부모들을 이동하는 게 아니라 마지막 → 루트 → sift-down)
===================================================================================
[복잡도 분석]
    N = len(score) (최대 1,000), K = k (최대 100)

    Mine_one   - 시간: O(N² log N) | 공간: O(N) - 매번 score[:i] 정렬
    Mine_two   - 시간: O(Nk log k) | 공간: O(k) - k+1개 정렬
    Mine_three - 시간: O(N log k)  | 공간: O(k) - heapq 힙 연산
    Mine_four  - 시간: O(Nk)       | 공간: O(k) - bisect O(log k) + del O(k)
    Mine_five  - 시간: O(N log k)  | 공간: O(k) - bisect O(log k) + pop O(1)
    Best       - 시간: O(N log k)  | 공간: O(k) - Mine_three와 동일
    Sub        - 시간: O(Nk log k) | 공간: O(k) - Mine_two와 동일

    N=1,000, K=100:
        Mine_one:   약 10,000,000 연산
        Mine_two:   약 700,000 연산
        Mine_four:  약 100,000 연산  ← bisect O(log k) + del O(k) = O(k) × N
        Mine_three: 약 10,000 연산  ← Best
        Mine_five:  약 10,000 연산  ← Best와 동급이나 상수 인자 있음
"""

import bisect
import heapq
import time


# =================================================================================
# Mine solution one - 매번 score[:i] 전체 정렬 (완전탐색)
# =================================================================================
def solution_mine_one(k: int, score: list[int]) -> list[int]:
    """
    매 날짜마다 score[:i]를 전체 정렬해 상위 k개의 최솟값을 반환하는 초기 풀이

    핵심:
        sorted(score[:i], reverse=True)[:k]: i번째까지 내림차순 정렬 후 상위 k개
        hof[-1]: 상위 k개 중 최솟값 (k번째 점수)

    한계:
        매 반복마다 점점 길어지는 score[:i] 정렬 → O(i log i)
        전체: O(N² log N)
    """
    answer = []
    for i in range(1, len(score) + 1):
        hof = sorted(score[:i], reverse=True)[:k]
        answer.append(hof[-1])
    return answer


# =================================================================================
# Mine solution two - hof를 k+1개로 제한하며 정렬
# =================================================================================
def solution_mine_two(k: int, score: list[int]) -> list[int]:
    """
    hof 크기를 k로 제한하며 매번 정렬하는 풀이

    mine_one 대비 개선:
        전체 score 정렬 → hof(최대 k+1개)만 정렬
        del hof[k:]: 정렬 후 k개 초과분 제거 → 항상 크기 k 유지
        k≤100으로 정렬 대상 고정 → 실용적

    시간: O(Nk log k) — k 작으면 빠름
    """
    answer = []
    hof = []
    for s in score:
        hof.append(s)
        hof.sort(reverse=True)
        del hof[k:]
        answer.append(hof[-1])
    return answer


# =================================================================================
# Mine solution three - heapq 최소 힙
# =================================================================================
def solution_mine_three(k: int, score: list[int]) -> list[int]:
    """
    최소 힙(heapq)으로 상위 k개를 유지하는 풀이

    heapq 최소 힙 특성:
        hof[0]: 항상 최솟값 → 명예의 전당 k번째 점수
        완전 이진트리 구조로 삽입/삭제 O(log k)

    로직:
        hof 크기 < k: heappush로 삽입
        hof 크기 = k, s > hof[0]: heappushpop으로 최솟값 교체
            heappushpop: sift-up 생략, s를 루트에 놓고 sift-down만 수행
            heappush + heappop보다 효율적
        s ≤ hof[0]: hof 변경 없음 → hof[0] 그대로 반환

    heappop 동작 (보완):
        hof[0] 반환 → 마지막 원소을 루트로 이동 → sift-down
        (부모들을 이동하는 게 아니라 마지막 원소 → 루트 → sift-down)
    """
    answer = []
    hof = []
    for s in score:
        if len(hof) < k:
            heapq.heappush(hof, s)
        elif s > hof[0]:
            heapq.heappushpop(hof, s)
        answer.append(hof[0])
    return answer


# =================================================================================
# Mine solution four - bisect 이진탐색 삽입 + del hof[0]
# =================================================================================
def solution_mine_four(k: int, score: list[int]) -> list[int]:
    """
    bisect.insort로 정렬 상태를 유지하며 삽입하는 풀이

    bisect 조건:
        항상 정렬된 리스트에만 사용 가능 (이진탐색 전제)
        insort: 이진탐색으로 삽입 위치 탐색 O(log k) + 삽입 O(k)

    del hof[0]: 오름차순 최솟값(hof[0]) 제거
        리스트 첫 원소 삭제 → 나머지 원소 한칸 이동 → O(k)
        k≤100으로 실질 부담 없음

    mine_three 대비:
        bisect insort O(k) + del O(k) = O(k) → heapq O(log k) 대비 느림
        전체: O(Nk)
    """
    answer = []
    hof = []
    for s in score:
        if len(hof) < k:
            bisect.insort(hof, s)
        elif s > hof[0]:
            del hof[0]
            bisect.insort(hof, s)
        answer.append(hof[0])
    return answer


# =================================================================================
# Mine solution five - bisect 음수 트릭으로 pop() O(1) 달성
# =================================================================================
def solution_mine_five(k: int, score: list[int]) -> list[int]:
    """
    음수 변환으로 bisect 내림차순 + O(1) pop() 달성하는 풀이

    음수 트릭:
        bisect는 오름차순만 지원
        -s로 음수 저장 → 오름차순 정렬 = 절댓값 내림차순
        hof[-1]: 가장 큰 음수 = 절댓값 최솟값 = 실제 최솟값
        hof.pop(): 리스트 맨 뒤 제거 → O(1) (del hof[0]의 O(k) 회피)

    mine_four 대비:
        del hof[0] O(k) → hof.pop() O(1)
        answer와 비교에서 -hof[-1] 변환 필요
        k≤100 제약에서 실측 차이 미미, 개념 학습 목적

    비교 방식:
        s > -hof[-1]: s가 현재 최솟값보다 크면 교체
        answer.append(-hof[-1]): 음수 복원
    """
    answer = []
    hof = []
    for s in score:
        if len(hof) < k:
            bisect.insort(hof, -s)
        elif s > -hof[-1]:
            hof.pop()
            bisect.insort(hof, -s)
        answer.append(-hof[-1])
    return answer


# =================================================================================
# Best solution - heapq 최소 힙 (mine_three 주석 보강)
# =================================================================================
def solution_best(k: int, score: list[int]) -> list[int]:
    """
    최소 힙으로 상위 k개를 O(N log k)로 유지하는 최적 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        heapq: 코딩테스트에서 "상위 k개 유지" 문제의 표준 패턴
        O(N log k): N=1,000, k=100 → 약 10,000번 연산
        Mine_one(O(N² log N)) 대비 압도적으로 효율적
        hof[0]으로 최솟값 O(1) 조회 → 매 날 최하위 점수 즉시 반환
    """
    answer = []
    hof = []
    for s in score:
        if len(hof) < k:
            heapq.heappush(hof, s)
        elif s > hof[0]:
            heapq.heappushpop(hof, s)
        answer.append(hof[0])
    return answer


# =================================================================================
# Sub solution - k+1개 제한 정렬 (mine_two 주석 보강)
# =================================================================================
def solution_sub(k: int, score: list[int]) -> list[int]:
    """
    hof 크기를 k로 제한하며 정렬하는 서브 풀이

    Best 대비 특징:
        sort() 방식으로 각 단계가 직관적으로 드러남
        k≤100 고정 → O(Nk log k)가 O(N log k)와 실질 차이 작음
        구현 복잡도 낮고 가독성 높음
        heapq 없이도 "상위 k개 유지" 로직을 명시적으로 표현
    """
    answer = []
    hof = []
    for s in score:
        hof.append(s)
        hof.sort(reverse=True)
        del hof[k:]
        answer.append(hof[-1])
    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[int], list[int]]] = [
        # (k, score, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # k=3, [10,100,20,150,1,100,200]:
        #   일1: hof=[10]         최하위=10
        #   일2: hof=[10,100]     최하위=10
        #   일3: hof=[10,100,20]  최하위=10 (3개 차면 최솟값=10)
        #   일4: 150>10 → hof=[20,100,150] 최하위=20
        #   일5: 1<20  → hof 변경없음 최하위=20
        #   일6: 100=100 → hof 변경없음 최하위=20 (100은 최솟값 20보다 크지 않음)
        #   일7: 200>20 → hof=[100,150,200] 최하위=100
        (3, [10, 100, 20, 150, 1, 100, 200], [10, 10, 10, 20, 20, 100, 100]),
        # k=4, [0,300,40,300,20,70,150,50,500,1000]
        (4, [0,300,40,300,20,70,150,50,500,1000], [0,0,0,0,20,40,70,70,150,300]),
    ]

    solutions = [
        ("Mine_one   (전체정렬)    ", solution_mine_one),
        ("Mine_two   (k+1정렬)    ", solution_mine_two),
        ("Mine_three (heapq)      ", solution_mine_three),
        ("Mine_four  (bisect+del) ", solution_mine_four),
        ("Mine_five  (bisect+pop) ", solution_mine_five),
        ("Best       (heapq)      ", solution_best),
        ("Sub        (k+1정렬)    ", solution_sub),
    ]

    # 워밍업 스텝
    _k, _score, _ = test_cases[0]
    for _, func in solutions:
        func(_k, _score[:])

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (k, score, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(k, score[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
