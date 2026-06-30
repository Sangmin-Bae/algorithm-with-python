"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 삼총사
    유형       : 완전탐색 (Brute Force) / Combination
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/131705
    풀이일자   : 2026-06-30
===================================================================================
[문제 요약]
    학생들의 정수 번호 배열 number에서 중복 없이 3명을 뽑아
    합이 0이 되는 조합의 개수를 반환

    제약 조건
        - number 길이: 3 이상 13 이하
        - number 각 원소: -1,000 이상 1,000 이하
        - 값이 같아도 인덱스가 다르면 서로 다른 학생 (값 중복 허용)
        - 최대 C(13,3) = 286개 조합 → 완전탐색으로 충분
===================================================================================
[입출력 예시]
    number                   | result
    -------------------------|-------
    [-2, 3, 0, 2, -5]        | 2
    [-3,-2,-1, 0, 1, 2, 3]   | 5
    [-1, 1,-1, 1]            | 0
===================================================================================
[내 초기 풀이]
    solution_one  : itertools.combinations + for 루프 명시적 카운트
    solution_two  : itertools.combinations + sum(1 for ...) 원라인
    solution_three: combinations 직접 구현 (재귀 + yield 제너레이터)
    solution_four : combinations 직접 구현 (DFS 백트래킹, 리스트 수집)
    solution_five : solution_three 변형 — 누적합 방식으로 0 판별까지 재귀에서 처리
    solution_six  : solution_four 변형 — DFS 중 합이 0이면 즉시 카운트 (nonlocal)

    핵심 판단: "중복과 순서 없이 3개 선택" = combination(조합)
        comb(): 조합의 개수만 필요할 때
        combinations(): 실제 조합 자체가 필요할 때 (이번 문제, 합을 계산해야 함)

[개선 포인트]
    solution_one  : 개선 필요 없음 (명시적, 가독성 우위)
    solution_two  : 개선 필요 없음 - Best
    solution_three/four: 모든 조합을 먼저 생성한 뒤 필터링
        → solution_five/six처럼 재귀 중 합을 누적하면
          불필요한 조합 생성 없이 판별 가능 (학습 목적으로 의미 있음)
    solution_five/six: 재귀/DFS 중 합 누적 판별로 효율적
        → solution_six을 Sub로 채택 (라이브러리 없는 직접 구현)
===================================================================================
[재귀 제너레이터 combinations 직접 구현 원리 - solution_three]
    recursive_comb(arr, c):
        c==0: 기저 조건 → 빈 튜플 yield (더 이상 선택할 게 없음)
        그 외: arr의 각 원소를 현재 선택(current)으로 삼고
               그 뒤 원소들(rest)에서 c-1개를 재귀로 선택
               (current,) + next_comb로 튜플 조립 후 yield

    손 추적 (arr=[1,2,3], c=2):
        i=0: current=1, rest=[2,3]
            recursive_comb([2,3], 1):
                i=0: current=2, rest=[3] → recursive_comb([3],0) yield ()
                     → yield (2,)
                i=1: current=3, rest=[] → recursive_comb([],0) yield ()
                     → yield (3,)
            → (1,2), (1,3)
        i=1: current=2, rest=[3]
            recursive_comb([3], 1): yield (3,)
            → (2,3)
        전체: (1,2),(1,3),(2,3) = C(3,2)=3개 ✓

[DFS 백트래킹 combinations 직접 구현 원리 - solution_four]
    dfs(start, current):
        len(current)==c: 완성된 조합 → result에 추가
        그 외: start부터 끝까지 순회하며
               current.append(arr[i]) → 선택
               dfs(i+1, current) → 다음 위치부터 재귀 (중복 방지)
               current.pop() → 백트래킹 (선택 취소, 이전 상태로 복원)

    append → 재귀 → pop 패턴이 백트래킹의 전형적 구조
===================================================================================
[nonlocal 키워드 — 변수 바인딩 규칙 정확한 이해]
    오해하기 쉬운 설명: "정수가 불변 객체라서 자식 함수에서 변경 불가능"
    정확한 이유: Python의 변수 바인딩 규칙 때문

    def outer():
        answer = 0
        def inner():
            answer += 1   # UnboundLocalError!
        inner()

    에러 원인:
        answer += 1 은 answer = answer + 1 과 동일
        inner() 내부에 answer에 대한 "할당문"이 있으면
        Python이 컴파일 시점에 answer를 inner()의 지역 변수로 취급
        → 우변의 answer를 평가하려 할 때 아직 정의되지 않음 → 오류
        → 불변성이 아니라 "이름에 대한 재할당 여부"가 핵심

    가변 객체로 우회 가능한 이유:
        def outer():
            answer = [0]
            def inner():
                answer[0] += 1   # 정상 동작
        answer[0] += 1 은 answer라는 이름 자체를 재할당하지 않음
        → answer가 가리키는 리스트 객체의 내용만 변경
        → Python이 answer를 지역 변수로 새로 선언하지 않음

    nonlocal 키워드:
        inner() 안에서 answer에 대한 할당이 있어도
        outer()의 answer를 가리키도록 명시적으로 지정
        → UnboundLocalError 없이 외부 변수 직접 수정 가능
===================================================================================
[복잡도 분석]
    N = len(number) (최대 13)
    K = C(N,3) (최대 286)

    Mine_one   - 시간: O(K)   | 공간: O(1)  - combinations 제너레이터, 즉시 처리
    Mine_two   - 시간: O(K)   | 공간: O(1)  - 동일, 원라인 표현
    Mine_three - 시간: O(K)   | 공간: O(N)  - 재귀 깊이 3, 제너레이터 체인
    Mine_four  - 시간: O(K)   | 공간: O(K)  - 모든 조합을 result 리스트에 저장
    Mine_five  - 시간: O(K)   | 공간: O(N)  - 재귀 중 누적합 판별, 조합 저장 없음
    Mine_six   - 시간: O(K)   | 공간: O(N)  - DFS 중 즉시 판별, 조합 저장 없음
    Best       - 시간: O(K)   | 공간: O(1)  - Mine_two와 동일
    Sub        - 시간: O(K)   | 공간: O(N)  - Mine_six과 동일

    N≤13 고정 → 최대 286개 조합, 모든 풀이 실질적으로 빠르게 수렴
"""

import time
from collections.abc import Iterator
from itertools import combinations


# =================================================================================
# Mine solution one - itertools.combinations + 명시적 for 루프
# =================================================================================
def solution_one(number: list[int]) -> int:
    """
    combinations로 모든 3개 조합을 생성하고 합이 0인 개수를 세는 초기 풀이

    핵심:
        combinations(number, 3): 중복 없이 순서 무관 3개 조합을 제너레이터로 생성
        sum(i) == 0: 조합의 원소 합 판별
    """
    answer = 0
    for i in combinations(number, 3):
        if sum(i) == 0:
            answer += 1
    return answer


# =================================================================================
# Mine solution two - combinations + sum(1 for ...) 원라인
# =================================================================================
def solution_two(number: list[int]) -> int:
    """
    제너레이터 + sum()으로 mine_one을 원라인으로 압축한 풀이

    sum(1 for i in ... if 조건): 조건 만족 개수를 세는 Python 관용 패턴
    """
    return sum(1 for i in combinations(number, 3) if sum(i) == 0)


# =================================================================================
# Mine solution three - combinations 직접 구현 (재귀 + yield)
# =================================================================================
def solution_three(number: list[int]) -> int:
    """
    재귀 + yield로 combinations를 직접 구현하는 풀이

    recursive_comb(arr, c):
        c==0: 기저 조건, 빈 튜플 yield
        그 외: arr[i]를 current로, arr[i+1:]를 rest로 재귀 호출
               (current,) + next_comb로 튜플 조립

    라이브러리 없이 조합 생성 원리를 직접 구현 → 학습 목적
    """
    def recursive_comb(arr: list[int], c: int) -> Iterator[tuple]:
        if c == 0:
            yield ()
            return

        for i in range(len(arr)):
            current = arr[i]
            rest = arr[i + 1:]

            for next_comb in recursive_comb(rest, c - 1):
                yield (current,) + next_comb

    return sum(1 for i in recursive_comb(number, 3) if sum(i) == 0)


# =================================================================================
# Mine solution four - combinations 직접 구현 (DFS 백트래킹)
# =================================================================================
def solution_four(number: list[int]) -> int:
    """
    DFS 백트래킹으로 combinations를 직접 구현하는 풀이

    dfs(start, current):
        len(current)==c: 완성된 조합 → result에 추가
        append → 재귀(다음 위치부터) → pop: 백트래킹 패턴

    mine_three(재귀+yield) 대비:
        제너레이터 아닌 리스트로 모든 조합을 한 번에 수집 → 공간 O(K)
    """
    def dfs_comb(arr: list[int], c: int) -> list[tuple[int]]:
        result = []

        def dfs(start: int, current: list[None | int]) -> None:
            if len(current) == c:
                result.append(tuple(current))
                return

            for i in range(start, len(arr)):
                current.append(arr[i])
                dfs(i + 1, current)
                current.pop()           # 백트래킹: 선택 취소 후 이전 상태 복원

        dfs(0, [])
        return result

    return sum(1 for i in dfs_comb(number, 3) if sum(i) == 0)


# =================================================================================
# Mine solution five - 재귀 + 누적합 (combinations 생성 없이 즉시 판별)
# =================================================================================
def solution_five(number: list[int]) -> int:
    """
    mine_three를 변형해 재귀 중 합을 누적하며 0 여부를 즉시 판별하는 풀이

    mine_three 대비 개선:
        조합 자체를 생성하지 않고 누적합 s를 재귀로 전달
        c==0 도달 시 s==0이면 1, 아니면 0을 yield
        → sum(제너레이터)로 1들의 합 = 조건 만족 개수

    불필요한 조합 생성 없이 판별 → 큰 N에서 의미 있는 최적화
    (이 문제 규모 N≤13에서는 체감 차이 적음)
    """
    def recursive_comb_sum(arr: list[int], c: int, s: int) -> Iterator[int]:
        if c == 0:
            if s == 0:
                yield 1
            else:
                yield 0
            return

        for i in range(len(arr)):
            current = arr[i]
            rest = arr[i + 1:]

            for next_sum in recursive_comb_sum(rest, c - 1, s + current):
                yield next_sum

    return sum(recursive_comb_sum(number, 3, 0))


# =================================================================================
# Mine solution six - DFS + nonlocal (조합 생성 없이 즉시 카운트)
# =================================================================================
def solution_six(number: list[int]) -> int:
    """
    mine_four를 변형해 DFS 중 합이 0이면 즉시 answer를 증가시키는 풀이

    mine_four 대비 개선:
        조합을 result 리스트에 저장하지 않고 합 판별 즉시 처리
        nonlocal answer: 내부 함수에서 외부 변수 직접 수정

    nonlocal이 필요한 이유:
        dfs_comb_sum 내부의 'answer += 1'은 재할당이라
        nonlocal 없이는 Python이 answer를 새 지역 변수로 취급 → UnboundLocalError
        nonlocal로 명시하면 solution_six()의 answer를 직접 참조/수정
    """
    answer = 0

    def dfs_comb_sum(start: int, current: list[None | int]) -> None:
        nonlocal answer

        if len(current) == 3:
            if sum(current) == 0:
                answer += 1      # nonlocal로 외부 answer 직접 수정
            return

        for i in range(start, len(number)):
            current.append(number[i])
            dfs_comb_sum(i + 1, current)
            current.pop()

    dfs_comb_sum(0, [])
    return answer


# =================================================================================
# Best solution - combinations + sum(1 for ...) (mine_two 주석 보강)
# =================================================================================
def solution_best(number: list[int]) -> int:
    """
    itertools.combinations + sum(1 for ...)으로 가장 간결하게 표현하는 최적 풀이

    mine_two와 동일한 로직, 근거 주석 보강:
        combinations(number, 3): C 레벨 구현, 중복 없이 3개 조합 생성
        sum(1 for ... if 조건): 조건 만족 개수를 세는 표준 관용 패턴
        표준 라이브러리 활용으로 가장 간결하고 신뢰할 수 있는 표현
    """
    return sum(1 for i in combinations(number, 3) if sum(i) == 0)


# =================================================================================
# Sub solution - DFS 백트래킹 + nonlocal (mine_six 주석 보강)
# =================================================================================
def solution_sub(number: list[int]) -> int:
    """
    DFS 백트래킹으로 조합 생성과 합 판별을 동시에 처리하는 서브 풀이

    Best 대비 특징:
        라이브러리 없이 combinations 원리를 직접 구현
        조합을 별도로 저장하지 않고 DFS 중 즉시 판별 → 메모리 효율적
        백트래킹(append→재귀→pop) 패턴이 코드에 명시적으로 드러남
        nonlocal로 재귀 내부에서 외부 카운터 직접 수정
    """
    answer = 0

    def dfs(start: int, current: list[int]) -> None:
        nonlocal answer

        if len(current) == 3:
            if sum(current) == 0:
                answer += 1
            return

        for i in range(start, len(number)):
            current.append(number[i])   # 선택
            dfs(i + 1, current)         # 다음 위치부터 재귀 (중복 방지)
            current.pop()               # 백트래킹

    dfs(0, [])
    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int]] = [
        # (number, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [-2,3,0,2,-5]: (-2,0,2)=0✓, (3,0,-5)는 X, (-2,3,-5)=-4, (-2,2,-5)=-5,
        #   (-2,3,0)=1, (-2,3,2)=3, (3,0,2)=5, (3,2,-5)=0✓, (0,2,-5)=-3
        #   → (-2,0,2), (3,2,-5) = 2개
        ([-2, 3, 0, 2, -5], 2),
        # [-3,-2,-1,0,1,2,3]: (-3,0,3),(-2,0,2),(-1,0,1),(-2,-1,3),(-3,1,2) = 5개
        ([-3, -2, -1, 0, 1, 2, 3], 5),
        # [-1,1,-1,1]: 가능한 조합 모두 0이 아님 → 0개
        ([-1, 1, -1, 1], 0),
        # 추가 케이스:
        # [0,0,0]: 유일한 조합 (0,0,0)=0 → 1개
        ([0, 0, 0], 1),
    ]

    solutions = [
        ("Mine_one   (comb+for)      ", solution_one),
        ("Mine_two   (comb+sum)      ", solution_two),
        ("Mine_three (재귀+yield)    ", solution_three),
        ("Mine_four  (DFS+백트래킹)  ", solution_four),
        ("Mine_five  (재귀+누적합)   ", solution_five),
        ("Mine_six   (DFS+nonlocal)  ", solution_six),
        ("Best       (comb+sum)      ", solution_best),
        ("Sub        (DFS+nonlocal)  ", solution_sub),
    ]

    # 워밍업 스텝
    _number, _ = test_cases[0]
    for _, func in solutions:
        func(_number)

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (number, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(number)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
