"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 문자열 내 마음대로 정렬하기
    유형       : Sort
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12915
    풀이일자   : 2026-07-05
===================================================================================
[문제 요약]
    문자열 리스트 strings를 각 문자열의 n번째 글자 기준으로 오름차순 정렬
    n번째 글자가 같으면 전체 문자열 사전순 정렬

    제약 조건
        - strings 길이: 1 이상 50 이하
        - strings 원소 길이: 1 이상 100 이하 (소문자 알파벳)
        - 모든 원소 길이 > n 보장 → IndexError 없음
===================================================================================
[입출력 예시]
    strings                   | n | return
    --------------------------|---|------------------------
    ["sun","bed","car"]       | 1 | ["car","bed","sun"]
    ["abce","abcd","cdx"]     | 2 | ["abcd","abce","cdx"]
===================================================================================
[핵심 포인트 — 튜플 키의 필요성]
    key=lambda x: x[n]        → n번째 글자만 기준
    key=lambda x: (x[n], x)   → 1순위: n번째 글자, 2순위: 전체 문자열 사전순

    key=lambda x: x[n]만 쓰면 안 되는 이유:
        Python sorted()는 안정 정렬(stable sort)
        key 값이 같을 때 원본 순서(strings 입력 순서)를 유지
        → 문제가 요구하는 "사전순 정렬"이 아닌 "원본 순서 유지"가 됨

        예: strings = ["bcd", "bad"], n=0
            key=x[0]: 둘 다 'b' → 원본 순서 유지 → ["bcd", "bad"]
            사전순 기대값: ["bad", "bcd"]  ← 다름!

        key=(x[n], x) 튜플 키:
            1순위 x[n]이 같으면 2순위 x(전체 문자열) 사전순으로 결정
            → 문제 조건 정확히 충족

[삽입 정렬 구현 핵심]
    올바른 위치를 찾아 insert():
        w[n] < answer[i][n]: 현재 위치보다 앞에 와야 함 → insert(i, w)
        w[n] == answer[i][n] and w < answer[i]: 사전순 앞 → insert(i, w)
        w[n] > answer[i][n] 또는 w >= answer[i]: 루프 계속 (더 뒤로)
        루프 끝까지 못 찾으면: 가장 크므로 append()
    flag 변수: insert 발생 여부 추적 → False면 append 실행
===================================================================================
[내 초기 풀이]
    solution_mine_one: sorted() + 튜플 key
    solution_mine_two: 삽입 정렬 직접 구현 (insert + flag)

[개선 포인트]
    solution_mine_one:
        key=lambda x: x[n] → 안정 정렬 특성으로 원본 순서 유지 → 오답 가능
        key=lambda x: (x[n], x) → 튜플 키로 2순위 조건 명시적 보장 ✓
        개선 필요 없음 - Best

    solution_mine_two:
        insert() 연산: O(N) (삽입 위치 이후 원소 이동)
        전체 삽입 정렬: O(N²)
        Best(O(N log N)) 대비 큰 입력에서 성능 차이 발생
        개선 필요 없음 - Sub (정렬 원리 학습 목적)
===================================================================================
[복잡도 분석]
    N = len(strings) (최대 50)
    L = strings 원소 평균 길이 (최대 100)

    Mine_one - 시간: O(N log N × L) | 공간: O(N) - sorted() Timsort
    Mine_two - 시간: O(N² × L)      | 공간: O(N) - 삽입 정렬 + 문자열 비교 O(L)
    Best     - 시간: O(N log N × L) | 공간: O(N) - Mine_one과 동일
    Sub      - 시간: O(N² × L)      | 공간: O(N) - Mine_two와 동일

    N≤50, L≤100 고정 → 실질적으로 O(1)에 수렴
    대규모 입력에서 O(N log N) vs O(N²) 차이 의미 있음
"""

import time


# =================================================================================
# Mine solution one - sorted() + 튜플 key
# =================================================================================
def solution_mine_one(strings: list[str], n: int) -> list[str]:
    """
    sorted()의 튜플 key로 n번째 글자 기준 + 사전순 2순위를 처리하는 초기 풀이

    key=lambda x: (x[n], x):
        1순위: x[n] → n번째 글자 오름차순
        2순위: x    → 전체 문자열 사전순 (1순위 동일할 때)

    key=lambda x: x[n]만 쓰면 안 되는 이유:
        Python sorted()는 안정 정렬 → key 동일 시 원본 순서 유지
        → 문제 요구 사항인 "사전순 정렬" 보장 불가
    """
    return sorted(strings, key=lambda x: (x[n], x))


# =================================================================================
# Mine solution two - 삽입 정렬 직접 구현
# =================================================================================
def solution_mine_two(strings: list[str], n: int) -> list[str]:
    """
    insert()를 이용한 삽입 정렬로 정렬 원리를 직접 구현하는 풀이

    알고리즘:
        answer가 비어있으면 첫 원소 그냥 추가
        비어있지 않으면 answer를 순회하며 올바른 위치 탐색:
            w[n] < answer[i][n]: w가 앞에 와야 함 → insert(i, w), break
            w[n] == answer[i][n] and w < answer[i]: 사전순 앞 → insert(i, w), break
            위 조건 미충족: 루프 계속 (w가 더 뒤로)
        flag=True이면 루프 끝까지 자리 못 찾음 → append (가장 뒤)

    시간복잡도:
        insert() O(N) × N번 = O(N²)
        Best(sorted Timsort O(N log N)) 대비 비효율
    """
    answer = []

    for w in strings:
        if not answer:
            answer.append(w)
        else:
            flag = True
            for i in range(len(answer)):
                if w[n] < answer[i][n]:
                    answer.insert(i, w)
                    flag = False
                    break
                elif w[n] == answer[i][n]:
                    if w < answer[i]:
                        answer.insert(i, w)
                        flag = False
                        break
            if flag:
                answer.append(w)

    return answer


# =================================================================================
# Best solution - sorted() + 튜플 key (mine_one 주석 보강)
# =================================================================================
def solution_best(strings: list[str], n: int) -> list[str]:
    """
    sorted() 튜플 key로 두 가지 정렬 조건을 동시에 처리하는 최적 풀이

    mine_one과 동일한 로직, 근거 주석 보강:
        sorted(): C 레벨 Timsort → O(N log N), 안정 정렬
        (x[n], x) 튜플 key:
            Python 튜플 비교는 첫 원소 같으면 두 번째 원소 비교
            x[n] 같으면 x 전체 문자열 사전순 비교 → 문제 조건 정확히 충족
        key=x[n]만 쓰면 안정 정렬로 원본 순서 유지 → 오답 가능
    """
    return sorted(strings, key=lambda x: (x[n], x))


# =================================================================================
# Sub solution - 삽입 정렬 (mine_two 주석 보강)
# =================================================================================
def solution_sub(strings: list[str], n: int) -> list[str]:
    """
    삽입 정렬로 정렬 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        sorted() 없이 비교/삽입을 직접 구현 → 정렬 동작 원리가 코드에 드러남
        insert(i, w): O(N) 이동 × N번 = O(N²) → Best O(N log N) 대비 느림
        flag 패턴: 루프 내 삽입 여부 추적, 미삽입 시 append
        N≤50 제약에서 차이 무시 가능, 대규모 입력에서 유의미한 차이
    """
    answer = []

    for w in strings:
        if not answer:
            answer.append(w)
        else:
            flag = True
            for i in range(len(answer)):
                if w[n] < answer[i][n]:
                    answer.insert(i, w)
                    flag = False
                    break
                elif w[n] == answer[i][n]:
                    if w < answer[i]:
                        answer.insert(i, w)
                        flag = False
                        break
            if flag:
                answer.append(w)

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[str], int, list[str]]] = [
        # (strings, n, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # ["sun","bed","car"], n=1:
        #   sun[1]='u', bed[1]='e', car[1]='a'
        #   오름차순: a<e<u → ["car","bed","sun"]
        (["sun", "bed", "car"], 1, ["car", "bed", "sun"]),
        # ["abce","abcd","cdx"], n=2:
        #   abce[2]='c', abcd[2]='c', cdx[2]='x'
        #   c==c → 사전순: abcd < abce → ["abcd","abce","cdx"]
        (["abce", "abcd", "cdx"], 2, ["abcd", "abce", "cdx"]),
        # 추가 케이스 — key=x[n]만 썼을 때 오답이 나오는 케이스:
        # ["bcd","bad"], n=0:
        #   bcd[0]='b', bad[0]='b' → 동일 → 사전순: bad < bcd
        #   key=x[n]만: 안정 정렬 → 원본 순서 ["bcd","bad"] 유지 → 오답
        #   key=(x[n],x): ["bad","bcd"] ← 정답
        (["bcd", "bad"], 0, ["bad", "bcd"]),
        # 단일 원소
        (["abc"], 1, ["abc"]),
    ]

    solutions = [
        ("Mine_one (sorted+튜플key)", solution_mine_one),
        ("Mine_two (삽입정렬)      ", solution_mine_two),
        ("Best     (sorted+튜플key)", solution_best),
        ("Sub      (삽입정렬)      ", solution_sub),
    ]

    # 워밍업 스텝
    _strings, _n, _ = test_cases[0]
    for _, func in solutions:
        func(_strings, _n)

    print("=" * 66)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (strings, n, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(strings[:], n)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
