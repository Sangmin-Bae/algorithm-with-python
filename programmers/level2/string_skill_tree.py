"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 스킬트리
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/49993
    풀이일자   : 2026-09-07
===================================================================================
[문제 요약]
    선행 스킬 순서 skill과 유저의 스킬트리 배열 skill_trees가 주어질 때
    선행 순서를 위반하지 않는 스킬트리의 개수 반환

    규칙:
        skill에 포함된 스킬은 skill 순서대로만 배울 수 있음
        skill에 없는 스킬은 순서 무관

    제약 조건
        - skill 길이: 1~26, 중복 없음
        - skill_trees 길이: 1~20
        - 각 tree 길이: 2~26, 중복 없음
===================================================================================
[입출력 예시]
    skill  | skill_trees                       | return
    -------|-----------------------------------|-------
    "CBD"  | ["BACDE","CBADF","AECB","BDA"]   | 2
===================================================================================
[검증 방법 비교]
    방법1 (set + 포인터):
        skill에 포함된 스킬만 idx 포인터로 순서 비교
        불일치 즉시 break → 불필요한 순회 없음
        추가 객체 생성 없음

    방법2 (deque):
        방법1과 동일 로직, popleft()로 순서 비교
        deque in 연산이 O(N) → 방법1보다 느림
        매 tree마다 deque(skill) 생성 비용

    방법3 (filter + startswith):
        tree에서 skill 스킬만 걸러낸 filtered_tree 생성
        skill.startswith(filtered_tree)로 순서 검증

    startswith가 성립하는 이유:
        "선행 스킬 순서를 지킨다"
        = "tree에서 skill 스킬들만 뽑았을 때 skill의 접두사여야 한다"
        filtered_tree = "CB" → skill = "CBD".startswith("CB") = True
        배우지 않은 나머지(D)는 가능

    예시:
        skill="CBD", tree="BACDE"
        filtered: B,C있음 A없음 D있음 E없음 → "BCD"
        "CBD".startswith("BCD") → False ✓

        tree="AECB"
        filtered: A없음 E없음 C있음 B있음 → "CB"
        "CBD".startswith("CB") → True ✓

[실측 결과 — 200,000회]
    one (set+포인터):    3.4μs  ← 가장 빠름
    two (deque):        10.8μs
    ref (filter+starts):15.7μs

    ref가 느린 이유:
        매 tree마다 filtered_tree 문자열 객체 생성 (join 비용)
    one이 빠른 이유:
        추가 객체 생성 없음, 불일치 즉시 break
===================================================================================
[내 초기 풀이]
    solution_mine_one: set + 포인터
    solution_mine_two: deque + popleft

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       범용적, 추가 객체 없음, 조기 종료
    solution_mine_two: deque in 연산 O(N) → skill_set 병행 사용 권장
    solution_ref:      filter+startswith - Sub
                       간결한 Python 표현, 가독성 우수
                       join 비용으로 가장 느림
===================================================================================
[복잡도 분석]
    S = len(skill) (최대 26), T = len(skill_trees) (최대 20)
    L = 각 tree 길이 (최대 26)

    Mine_one - 시간: O(T × L) | 공간: O(S) - skill_set
    Mine_two - 시간: O(T × L) | 공간: O(S) - deque 생성
    Ref      - 시간: O(T × L) | 공간: O(L) - filtered_tree
    Best     - 시간: O(T × L) | 공간: O(S) - Mine_one과 동일
    Sub      - 시간: O(T × L) | 공간: O(L) - Ref와 동일

    모든 값이 상수 → 실질적 O(1)
"""

from collections import deque
import time


# =================================================================================
# Mine solution one - set + 인덱스 포인터
# =================================================================================
def solution_mine_one(skill: str, skill_trees: list[str]) -> int:
    """
    skill_set으로 O(1) 탐색 후 인덱스 포인터로 순서를 검증하는 초기 풀이

    skill_set:
        skill의 스킬 포함 여부를 O(1)로 판별
        skill 문자열 in 연산 O(len(skill)) 대비 상수 절감

    idx 포인터:
        skill에서 다음으로 배워야 할 스킬의 위치 추적
        char == skill[idx]이면 올바른 순서 → idx 증가
        char != skill[idx]이면 순서 위반 → break

    추가 객체 생성 없음 + 조기 종료 → 실측 가장 빠름
    """
    answer = 0
    skill_set = set(skill)

    for tree in skill_trees:
        idx = 0
        is_valid = True

        for char in tree:
            if char in skill_set:
                if char != skill[idx]:
                    is_valid = False
                    break
                else:
                    idx += 1

        if is_valid:
            answer += 1

    return answer


# =================================================================================
# Mine solution two - deque + popleft
# =================================================================================
def solution_mine_two(skill: str, skill_trees: list[str]) -> int:
    """
    deque(skill)을 매 tree마다 생성하고 popleft()로 순서를 검증하는 풀이

    deque(skill):
        skill을 순차적으로 꺼낼 수 있는 큐
        popleft(): 앞에서 O(1)로 꺼냄

    한계:
        in 연산: deque에서 O(len(queue)) 선형 탐색
        skill_set과 병행 사용하면 O(1)로 개선 가능
        매 tree마다 deque 생성 비용

    mine_one 대비 실측 3배 느림
    """
    answer = 0

    for tree in skill_trees:
        queue = deque(skill)
        is_valid = True

        for char in tree:
            if char in queue:
                if char != queue.popleft():
                    is_valid = False
                    break

        if is_valid:
            answer += 1

    return answer


# =================================================================================
# Ref solution - filter + startswith
# =================================================================================
def solution_ref(skill: str, skill_trees: list[str]) -> int:
    """
    tree에서 skill 스킬만 걸러내고 startswith로 순서를 검증하는 참고 풀이

    핵심 발상:
        "선행 스킬 순서를 지킨다"
        = "tree에서 skill 스킬만 뽑았을 때 skill의 접두사여야 한다"

    startswith가 성립하는 이유:
        배운 skill 스킬들은 skill 순서의 앞부분과 일치해야 함
        나머지 skill 스킬(아직 안 배운 것)은 가능
        filtered_tree = "CB" → "CBD".startswith("CB") = True ✓

    join 비용으로 mine_one보다 느리지만
    Python 내장 메서드로 가장 간결한 표현
    """
    answer = 0
    skill_set = set(skill)

    for tree in skill_trees:
        filtered_tree = "".join(char for char in tree if char in skill_set)

        if skill.startswith(filtered_tree):
            answer += 1

    return answer


# =================================================================================
# Best solution - set + 인덱스 포인터 (mine_one 주석 보강)
# =================================================================================
def solution_best(skill: str, skill_trees: list[str]) -> int:
    """
    set + 포인터로 O(T×L) 시간, O(S) 공간에 유효한 스킬트리를 찾는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        추가 문자열 객체 생성 없음 (ref의 join 비용 없음)
        불일치 즉시 break → 불필요한 순회 없음
        실측: 3.4μs (ref 15.7μs 대비 4.6배 우위)
        범용적 패턴 → 다른 언어에서도 동일하게 적용 가능
    """
    answer = 0
    skill_set = set(skill)

    for tree in skill_trees:
        idx = 0
        is_valid = True

        for char in tree:
            if char in skill_set:
                if char != skill[idx]:
                    is_valid = False
                    break
                else:
                    idx += 1

        if is_valid:
            answer += 1

    return answer


# =================================================================================
# Sub solution - filter + startswith (ref 주석 보강)
# =================================================================================
def solution_sub(skill: str, skill_trees: list[str]) -> int:
    """
    filter + startswith로 간결하게 순서를 검증하는 서브 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        전처리(filter) 후 검증(startswith) 구조가 명확
        "선행 관계없는 스킬 제거 → 남은 순서 확인"이 직관적
        Python 내장 startswith로 가독성 우수
        join 비용으로 Best 대비 4.6배 느림
    """
    answer = 0
    skill_set = set(skill)

    for tree in skill_trees:
        filtered_tree = "".join(char for char in tree if char in skill_set)

        if skill.startswith(filtered_tree):
            answer += 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (skill, skill_trees, 기댓값)
        # 공식 예시
        ("CBD", ["BACDE", "CBADF", "AECB", "BDA"], 2),
        # 추가 케이스:
        # AB 포함 → 'AB': ok, 'A': ok(B 아직 안배워도 가능), 'ACB': ok, 'BA': 불가
        ("AB", ["AB", "A", "ACB", "BA"],            3),
        # 단일 스킬
        ("A",  ["A", "BA", "AB"],                   3),
        # 모두 불가능
        ("ABC",["CBA", "BCA", "CAB"],               0),
    ]

    solutions = [
        ("Mine_one (set+포인터)   ", solution_mine_one),
        ("Mine_two (deque)        ", solution_mine_two),
        ("Ref      (filter+starts)", solution_ref),
        ("Best     (set+포인터)   ", solution_best),
        ("Sub      (filter+starts)", solution_sub),
    ]

    # 워밍업 스텝
    _s, _st, _ = test_cases[0]
    for _, func in solutions:
        func(_s, _st)

    print("=" * 66)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (skill, skill_trees, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(skill, skill_trees[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
