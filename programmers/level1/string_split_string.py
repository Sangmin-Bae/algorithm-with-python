"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 문자열 나누기
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/140108
    풀이일자   : 2026-08-25
===================================================================================
[문제 요약]
    문자열 s를 규칙에 따라 분리하고 분리된 문자열 개수 반환
    규칙: 첫 글자 x 기준 x 횟수와 x 아닌 횟수가 같아지면 분리

    제약 조건
        - s 길이: 1 이상 10,000 이하
        - 영어 소문자로만 구성
===================================================================================
[입출력 예시]
    s                 | result
    ------------------|-------
    "banana"          | 3      (ba-na-na)
    "abracadabra"     | 6      (ab-ra-ca-da-br-a)
    "aaabbaccccabba"  | 3      (aaabbacc-ccab-ba)
===================================================================================
[핵심 — 마지막 분리 엣지케이스]
    equal == no_equal로 순회 끝남:
        마지막 루프에서 이미 answer += 1, equal = no_equal = 0
        → else에서 추가 카운트 불필요 (equal == 0)

    equal != no_equal로 순회 끝남:
        for-else 실행 → equal > 0 → answer += 1

    equal > 0 조건 분석:
        마지막 글자에서 equal == no_equal이 되면
        answer += 1, equal = no_equal = 0으로 초기화 후 else 진입
        이때 equal == 0이므로 else에서 answer를 더 증가시키면 안 됨
        → equal > 0은 필수 조건 (방어적 코드가 아님)

        equal > 0이 True: 중간 분리 후 남은 문자열 → 마지막 분리 포함
        equal > 0이 False: 마지막 글자에서 정확히 끝남 → 이미 포함됨

[풀이별 슬라이싱 비용]
    풀이2: s = s[i+1:] → 새 문자열 객체 O(len(s))
        분리 K번: O(N) + O(N-a) + ... 최악 O(N²/2)
        N=10,000에서 이론상 5,000만 연산

    풀이1: 슬라이싱 없음
        단일 인덱스 순회 O(N), 공간 O(1)

    실측 N=10,000: 모든 방식 0.93~1.04ms (거의 동일)
    → s 길이 상한(10,000)이 작아서 차이 없음

[deque vs 문자열 인덱스 접근]
    ref_one deque 방식:
        deque(s): 변환 비용 O(N)
        popleft(): O(1) (리스트 pop(0)는 O(N))
        deque 변환 + popleft가 문자열 인덱스 직접 접근보다 오버헤드 큼

    실측: ref_one(deque) 0.93ms ← 가장 빠르나 미미한 차이

[start/end 투포인터 vs 단일 인덱스]
    ref_two: start = 분리 시작점, end = 탐색 위치
             분리 구간 [start, end]가 코드에 명시적
    풀이1:   단일 인덱스 i, 분리 시 x와 equal 갱신
             더 간결하나 구간 경계가 덜 명시적
===================================================================================
[내 초기 풀이]
    solution_mine_one: 단일 인덱스 순회 + for-else
    solution_mine_two: while + 문자열 슬라이싱 + for-else

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       O(N) 시간, O(1) 공간, 슬라이싱 없음
    solution_mine_two: 슬라이싱 O(len(s)) 비용
                       직관적이나 메모리 비용 발생
    solution_ref_one:  deque 변환 비용 존재
                       popleft O(1)이지만 변환이 더 비쌈
    solution_ref_two:  start/end로 구간 명시 - Sub
                       로직은 풀이1과 동일, 가독성 차이
===================================================================================
[복잡도 분석]
    N = len(s) (최대 10,000)

    Mine_one - 시간: O(N) | 공간: O(1) - 단일 순회, 슬라이싱 없음
    Mine_two - 시간: O(N) | 공간: O(N) - 슬라이싱으로 새 문자열 생성
    Ref_one  - 시간: O(N) | 공간: O(N) - deque 변환 O(N)
    Ref_two  - 시간: O(N) | 공간: O(1) - start/end 인덱스만 사용
    Best     - 시간: O(N) | 공간: O(1) - Mine_one과 동일
    Sub      - 시간: O(N) | 공간: O(1) - Ref_two와 동일
"""

from collections import deque
import time


# =================================================================================
# Mine solution one - 단일 인덱스 순회 + for-else
# =================================================================================
def solution_mine_one(s: str) -> int:
    """
    단일 인덱스로 전체를 순회하며 x 갱신과 equal 초기화로 분리하는 초기 풀이

    x 갱신:
        equal == no_equal 시 i+1 글자가 있으면 x = s[i+1]
        없으면 for 루프가 n-1번째로 끝남 → else에서 처리

    for-else 마지막 처리:
        break 없이 루프 종료 후 else 진입
        equal > 0: 중간 분리 후 남은 문자열이 있는 경우 → answer 포함
        equal == 0: 마지막 글자에서 equal==no_equal로 정확히 끝난 경우
                    이미 answer에 포함됨 → 추가 불필요

    equal > 0은 필수 조건:
        마지막 글자에서 equal==no_equal 달성 시
        equal = 0으로 초기화 후 else 진입
        조건 없으면 answer를 하나 더 잘못 추가

    O(N) 시간, O(1) 공간: 슬라이싱 없음
    """
    answer = 0
    x = s[0]
    n = len(s)
    equal = no_equal = 0

    for i in range(n):
        if s[i] == x:
            equal += 1
        else:
            no_equal += 1

        if equal == no_equal:
            answer += 1
            if i + 1 < n:
                x = s[i + 1]
            equal = no_equal = 0
    else:
        if equal > 0:
            answer += 1

    return answer


# =================================================================================
# Mine solution two - while + 문자열 슬라이싱 + for-else
# =================================================================================
def solution_mine_two(s: str) -> int:
    """
    문자열을 직접 잘라내며 순회하는 직관적인 풀이

    s = s[i+1:]:
        분리 후 남은 문자열로 갱신
        새 문자열 객체 생성 O(len(s)) 비용 발생

    for-else:
        break → else 실행 안 됨 (equal == no_equal로 분리)
        루프 완료 → else 실행 (마지막 문자열 분리)

    로직 직관적이나 슬라이싱 메모리 비용 존재
    """
    answer = 0

    while s:
        x = s[0]
        equal = no_equal = 0

        for i in range(len(s)):
            if s[i] == x:
                equal += 1
            else:
                no_equal += 1

            if equal == no_equal:
                s = s[i + 1:]
                answer += 1
                break
        else:
            answer += 1
            break

    return answer


# =================================================================================
# Ref solution one - deque + popleft
# =================================================================================
def solution_ref_one(s: str) -> int:
    """
    deque로 문자를 앞에서 꺼내며 처리하는 참고 풀이

    deque(s): 문자열을 deque로 변환 O(N)
    popleft(): O(1) 앞 원소 추출

    한계:
        deque 변환 비용 O(N)이 문자열 인덱스 접근보다 비쌈
        a != b 조건으로 마지막 처리가 while 밖에 위치해 구조 주의 필요
    """
    answer = 0
    q = deque(s)

    while q:
        a, b = 1, 0
        x = q.popleft()

        while q:
            n = q.popleft()
            if n == x:
                a += 1
            else:
                b += 1

            if a == b:
                answer += 1
                break
    if a != b:
        answer += 1

    return answer


# =================================================================================
# Ref solution two - start/end 투포인터
# =================================================================================
def solution_ref_two(s: str) -> int:
    """
    start와 end 인덱스로 분리 구간을 명시적으로 표현하는 참고 풀이

    start: 현재 분리 시작점
    end:   탐색 끝점 (range(start, N))

    equal == no_equal 시: start = end + 1로 다음 구간 시작
    for-else: 루프 완료 → 마지막 문자열 분리

    풀이1과 동일한 O(N) 시간, O(1) 공간
    분리 구간 [start, end]가 코드에 더 명시적
    """
    answer = 0
    N = len(s)
    start = 0

    while start < N:
        x = s[start]
        cnt1 = cnt2 = 0

        for end in range(start, N):
            if s[end] == x:
                cnt1 += 1
            else:
                cnt2 += 1

            if cnt1 == cnt2:
                start = end + 1
                answer += 1
                break
        else:
            answer += 1
            break

    return answer


# =================================================================================
# Best solution - 단일 인덱스 순회 (mine_one 주석 보강)
# =================================================================================
def solution_best(s: str) -> int:
    """
    단일 인덱스 O(N) 순회, O(1) 공간으로 문자열을 분리하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        슬라이싱 없음 → 새 문자열 객체 생성 비용 없음
        for-else로 마지막 분리 처리
        equal > 0: 마지막 글자에서 equal==no_equal로 끝난 경우 False
               → 이미 answer에 포함됨, 필수 조건
    """
    answer = 0
    x = s[0]
    n = len(s)
    equal = no_equal = 0

    for i in range(n):
        if s[i] == x:
            equal += 1
        else:
            no_equal += 1

        if equal == no_equal:
            answer += 1
            if i + 1 < n:
                x = s[i + 1]
            equal = no_equal = 0
    else:
        if equal > 0:
            answer += 1

    return answer


# =================================================================================
# Sub solution - start/end 투포인터 (ref_two 주석 보강)
# =================================================================================
def solution_sub(s: str) -> int:
    """
    start/end로 분리 구간을 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        start: 현재 분리 구간의 시작 인덱스
        end: 탐색 끝 인덱스
        [start, end] 구간이 코드에 직접 드러남
        O(N) 시간, O(1) 공간으로 Best와 동일
        구간 경계를 명시적으로 다루는 스타일 선호 시 적합
    """
    answer = 0
    N = len(s)
    start = 0

    while start < N:
        x = s[start]
        cnt1 = cnt2 = 0

        for end in range(start, N):
            if s[end] == x:
                cnt1 += 1
            else:
                cnt2 += 1

            if cnt1 == cnt2:
                start = end + 1
                answer += 1
                break
        else:
            answer += 1
            break

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int]] = [
        # (s, 기댓값)
        # 공식 예시
        ("banana",         3),
        ("abracadabra",    6),
        ("aaabbaccccabba", 3),
        # 추가 케이스:
        ("a",              1),   # 단일 문자 (equal > 0으로 끝)
        ("aa",             1),   # equal 먼저 2, no_equal 없음 → 1개
        ("ab",             1),   # equal==no_equal → 1개
        ("aab",            1),   # x=a, a→eq=2, b→ne=1, 끝까지 eq≠ne → 1개
                                 # 손 추적: x=a, a→eq=1, a→eq=2, b→ne=1
                                 # eq≠ne 계속, 끝까지 → 1개
    ]

    solutions = [
        ("Mine_one (단일순회)  ", solution_mine_one),
        ("Mine_two (슬라이싱) ", solution_mine_two),
        ("Ref_one  (deque)    ", solution_ref_one),
        ("Ref_two  (투포인터) ", solution_ref_two),
        ("Best     (단일순회) ", solution_best),
        ("Sub      (투포인터) ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start_t = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start_t

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
