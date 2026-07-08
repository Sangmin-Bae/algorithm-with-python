"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 카드 뭉치
    유형       : Stack / Queue
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/159994
    풀이일자   : 2026-07-08
===================================================================================
[문제 요약]
    두 카드 뭉치에서 순서대로 카드를 사용해 goal 순서를 만들 수 있는지 판별
    "Yes" 또는 "No" 반환

    규칙:
        - 카드는 순서대로만 사용 (건너뛰기 불가)
        - 한 번 사용한 카드는 재사용 불가
        - 카드를 사용하지 않고 다음 카드로 넘어갈 수 없음

    제약 조건
        - cards1, cards2 길이: 1~10
        - goal 길이: 2 이상, cards1 길이 + cards2 길이 이하
        - cards1, cards2에 서로 다른 단어만 존재 (중복 없음)
        - goal 원소는 cards1, cards2 원소들로만 구성
===================================================================================
[입출력 예시]
    cards1               | cards2         | goal                                  | result
    ---------------------|----------------|---------------------------------------|-------
    ["i","drink","water"] | ["want","to"] | ["i","want","to","drink","water"]     | "Yes"
    ["i","water","drink"] | ["want","to"] | ["i","want","to","drink","water"]     | "No"
===================================================================================
[핵심 조건 — goal이 두 뭉치를 전부 사용하지 않아도 됨]
    goal 길이 ≤ cards1 길이 + cards2 길이
    → goal은 두 뭉치의 일부만 사용할 수 있음
    → solution_one 실패 원인:
        cards1 == cards1_checker 비교는
        "goal에 사용된 cards1 단어 = cards1 전체"를 검사
        goal이 cards1 일부만 쓰는 경우 항상 False → 오답

[풀이 방식 비교 — "찾기" vs "포인터 전진"]
    solution_two (찾기 방식):
        goal 단어를 cards에서 index()로 탐색 → O(N)
        이전 사용 인덱스 + 1과 비교
        → 매번 탐색 발생, 불필요한 비교 복잡도

    solution_three (포인터 방식):
        "지금 사용해야 할 카드 위치" 포인터를 앞에서부터 전진
        goal 단어가 포인터 위치 카드와 같으면 포인터 전진 → O(1)
        → 탐색 없이 직접 비교, 더 효율적

    solution_four (deque 방식):
        각 카드 뭉치를 deque로 변환
        goal 단어가 deque[0]과 같으면 popleft() → O(1)
        → solution_three와 동일한 로직, 자료구조가 의도를 더 명시적으로 표현
===================================================================================
[내 초기 풀이]
    solution_mine_one  : goal 순회 → 카드 뭉치별 checker 리스트 누적 후 비교 (오답)
    solution_mine_two  : index()로 위치 탐색 후 이전 인덱스 + 1 비교
    solution_mine_three: 포인터(cards1_idx, cards2_idx) 전진 방식
    solution_mine_four : deque + popleft() 방식

[개선 포인트]
    solution_mine_one:
        오답 원인: goal이 카드 뭉치 전체를 사용하지 않아도 됨
                   cards1 == cards1_checker → 전체 비교라 항상 False
        개선: 카드를 "전부 쓰는지"가 아닌 "순서대로 쓰는지"를 검증해야 함

    solution_mine_two:
        cards1.index(c): 리스트 전체 탐색 O(N) → 불필요한 비용
        제약상 중복 없어서 통과하나 index()는 첫 번째 위치만 반환
        → 일반적으로 취약한 방식

    solution_mine_three: 개선 필요 없음 - Best
        포인터 전진으로 O(1) 비교, 추가 자료구조 없음

    solution_mine_four: 개선 필요 없음 - Sub
        deque 변환 O(N) 추가 비용 있으나 동작 의도가 가장 명확
===================================================================================
[복잡도 분석]
    N = len(goal) (최대 20), M = len(cards) (최대 10)

    Mine_one   - 시간: O(N×M)  | 공간: O(N) - in 탐색 O(M) × goal 순회, 오답
    Mine_two   - 시간: O(N×M)  | 공간: O(1) - index() O(M) × goal 순회
    Mine_three - 시간: O(N)    | 공간: O(1) - 포인터 비교 O(1) × goal 순회
    Mine_four  - 시간: O(N)    | 공간: O(M) - deque 변환 O(M) + popleft O(1)
    Best       - 시간: O(N)    | 공간: O(1) - Mine_three와 동일
    Sub        - 시간: O(N)    | 공간: O(M) - Mine_four와 동일

    N, M 모두 최대 20 이하 → 실질적으로 모두 O(1)에 수렴
    대규모에서 Mine_three/Best의 O(N) vs Mine_two의 O(N×M) 차이 의미 있음
"""

import time
from collections import deque


# =================================================================================
# Mine solution one - checker 리스트 누적 후 비교 (오답)
# =================================================================================
def solution_mine_one(cards1: list[str], cards2: list[str], goal: list[str]) -> str:
    """
    goal 순회 중 카드 뭉치별 사용 단어를 누적 후 전체 비교하는 초기 풀이 (오답)

    오답 원인: goal 길이 ≤ cards1 + cards2 길이
        cards1 == cards1_checker:
            cards1 전체와 비교 → goal이 일부만 쓰면 항상 False
        일부 케이스는 통과 (goal이 마침 전체를 사용하는 경우)
        나머지 케이스 실패 (goal이 일부만 사용하는 경우)

    개선 방향 (코드 수정 없이 비교 조건만 바꾸면 통과 가능):
        cards1 == cards1_checker
        → cards1[:len(cards1_checker)] == cards1_checker
        cards2 == cards2_checker
        → cards2[:len(cards2_checker)] == cards2_checker
        단, in 탐색 O(M) × goal 순회 O(N) = O(N×M)로 solution_three보다 비효율

    학습 의의:
        "전부 사용해야 하는가 vs 순서를 지켜야 하는가" 조건 구분의 중요성
    """
    cards1_checker = []
    cards2_checker = []

    for c in goal:
        if c in cards1:
            cards1_checker.append(c)
        elif c in cards2:
            cards2_checker.append(c)
        else:
            return "No"

    return "Yes" if cards1 == cards1_checker and cards2 == cards2_checker else "No"


# =================================================================================
# Mine solution two - index()로 위치 탐색 후 이전 인덱스 + 1 비교
# =================================================================================
def solution_mine_two(cards1: list[str], cards2: list[str], goal: list[str]) -> str:
    """
    goal 단어의 인덱스를 cards에서 직접 찾아 연속성을 검증하는 풀이

    핵심:
        cards1_idx: 마지막으로 사용된 cards1 인덱스 (-1로 초기화)
        cards1.index(c): c의 인덱스 탐색 O(M)
        idx == cards1_idx + 1: 연속된 순서인지 확인

    한계:
        index() O(M) × goal 순회 O(N) = O(N×M)
        제약상 중복 없어 통과하나 index()는 첫 번째 위치만 반환
        → solution_three의 포인터 방식이 더 효율적
    """
    flag = True
    cards1_idx = -1
    cards2_idx = -1

    for c in goal:
        if c in cards1:
            idx = cards1.index(c)
            if idx != cards1_idx + 1:
                flag = False
                break
            else:
                cards1_idx = idx
        elif c in cards2:
            idx = cards2.index(c)
            if idx != cards2_idx + 1:
                flag = False
                break
            else:
                cards2_idx = idx

    return "Yes" if flag else "No"


# =================================================================================
# Mine solution three - 포인터(cards1_idx, cards2_idx) 전진 방식
# =================================================================================
def solution_mine_three(cards1: list[str], cards2: list[str], goal: list[str]) -> str:
    """
    "지금 사용해야 할 카드 위치" 포인터를 전진시키며 검증하는 풀이

    solution_two 대비 개선:
        index() 탐색 없이 포인터가 가리키는 위치의 카드와 직접 비교
        O(1) 비교 × goal 순회 = O(N)

    포인터 방식 vs 찾기 방식:
        찾기(two): "단어를 cards에서 찾아서 위치를 확인"
        포인터(three): "위치를 직접 들고 다니며 단어를 확인"
        → 후자가 탐색 비용 없음

    else 조건:
        cards1의 현재 포인터 위치 카드도 아니고
        cards2의 현재 포인터 위치 카드도 아님
        → 순서가 맞지 않음 → "No" 즉시 반환
    """
    cards1_idx = 0
    cards2_idx = 0

    for c in goal:
        if cards1_idx < len(cards1) and cards1[cards1_idx] == c:
            cards1_idx += 1         # 포인터 전진
        elif cards2_idx < len(cards2) and cards2[cards2_idx] == c:
            cards2_idx += 1         # 포인터 전진
        else:
            return "No"

    return "Yes"


# =================================================================================
# Mine solution four - deque + popleft()
# =================================================================================
def solution_mine_four(cards1: list[str], cards2: list[str], goal: list[str]) -> str:
    """
    각 카드 뭉치를 deque로 변환해 popleft()로 순서를 유지하는 풀이

    핵심:
        deque: 양방향 큐, popleft() O(1) (리스트 pop(0) O(N) 대비)
        c1[0]: 현재 사용 가능한 카드 뭉치의 맨 앞 카드
        popleft(): 사용한 카드 제거 → 다음 카드가 자동으로 [0]

    solution_three 대비:
        deque 변환 O(M) 추가 비용
        popleft()로 "사용한 카드를 제거"하는 동작이 명시적으로 드러남
        포인터 전진과 동일한 효과, 가독성과 의도 표현 우위
    """
    c1 = deque(cards1)
    c2 = deque(cards2)

    for c in goal:
        if c1 and c1[0] == c:
            c1.popleft()            # 사용한 카드 제거, 다음 카드가 [0]으로
        elif c2 and c2[0] == c:
            c2.popleft()
        else:
            return "No"

    return "Yes"


# =================================================================================
# Best solution - 포인터 전진 방식 (mine_three 주석 보강)
# =================================================================================
def solution_best(cards1: list[str], cards2: list[str], goal: list[str]) -> str:
    """
    포인터 전진으로 O(N) 시간, O(1) 공간에 순서를 검증하는 최적 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        추가 자료구조 없이 정수 포인터 2개만 사용 → O(1) 공간
        O(1) 비교 × N번 순회 → O(N) 시간
        cards1, cards2 원본 변경 없음 (포인터만 전진)
        조건 검증 순서: cards1 먼저 → 없으면 cards2 → 없으면 "No" 즉시 반환
    """
    cards1_idx = 0
    cards2_idx = 0

    for c in goal:
        if cards1_idx < len(cards1) and cards1[cards1_idx] == c:
            cards1_idx += 1
        elif cards2_idx < len(cards2) and cards2[cards2_idx] == c:
            cards2_idx += 1
        else:
            return "No"

    return "Yes"


# =================================================================================
# Sub solution - deque + popleft() (mine_four 주석 보강)
# =================================================================================
def solution_sub(cards1: list[str], cards2: list[str], goal: list[str]) -> str:
    """
    deque로 카드 뭉치를 관리하며 순서를 검증하는 서브 풀이

    Best 대비 특징:
        deque 변환 O(M) 추가 비용
        "카드를 사용하면 제거된다"는 문제 조건이 popleft()로 명시적 표현
        c1이 비어있으면 c1[0] 접근 불가 → `c1 and c1[0] == c` 조건 필요
        동작 원리가 직관적으로 드러나는 구현
    """
    c1 = deque(cards1)
    c2 = deque(cards2)

    for c in goal:
        if c1 and c1[0] == c:
            c1.popleft()
        elif c2 and c2[0] == c:
            c2.popleft()
        else:
            return "No"

    return "Yes"


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[str], list[str], list[str], str]] = [
        # (cards1, cards2, goal, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # cards1=["i","drink","water"], cards2=["want","to"]
        # goal=["i","want","to","drink","water"]
        #   "i"     → cards1[0]="i" ✓ → ptr1=1
        #   "want"  → cards2[0]="want" ✓ → ptr2=1
        #   "to"    → cards2[1]="to" ✓ → ptr2=2
        #   "drink" → cards1[1]="drink" ✓ → ptr1=2
        #   "water" → cards1[2]="water" ✓ → ptr1=3
        #   → "Yes"
        (["i","drink","water"], ["want","to"],
         ["i","want","to","drink","water"], "Yes"),
        # cards1=["i","water","drink"]: "drink" 전에 "water" 써야 하는데
        # goal에서 "drink"가 먼저 요구됨 → "No"
        (["i","water","drink"], ["want","to"],
         ["i","want","to","drink","water"], "No"),
        # 추가 케이스:
        # goal이 한쪽 뭉치만 사용
        (["a","b","c"], ["d","e"],
         ["a","b"], "Yes"),
        # goal이 섞어서 사용하지만 순서 맞음
        (["a","b"], ["c","d"],
         ["a","c","b","d"], "Yes"),
        # 순서 위반
        (["a","b"], ["c","d"],
         ["b","a"], "No"),
    ]

    solutions = [
        ("Mine_one   (checker비교)", solution_mine_one),
        ("Mine_two   (index탐색)  ", solution_mine_two),
        ("Mine_three (포인터전진) ", solution_mine_three),
        ("Mine_four  (deque)      ", solution_mine_four),
        ("Best       (포인터전진) ", solution_best),
        ("Sub        (deque)      ", solution_sub),
    ]

    # 워밍업 스텝
    _c1, _c2, _goal, _ = test_cases[0]
    for _, func in solutions:
        func(_c1, _c2, _goal)

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (c1, c2, goal, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(c1[:], c2[:], goal[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
