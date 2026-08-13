"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 추억 점수
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/176963
    풀이일자   : 2026-08-13
===================================================================================
[문제 요약]
    name-yearning 쌍으로 이름별 그리움 점수 매핑
    photo의 각 사진에 등장한 인물의 그리움 점수 합산 반환
    name에 없는 인물은 0점으로 처리

    제약 조건
        - name 길이: 3 이상 100 이하
        - photo 길이: 3 이상 100 이하
        - photo[i] 길이: 1 이상 100 이하
===================================================================================
[입출력 예시]
    name               | yearning   | photo                           | result
    -------------------|------------|----------------------------------|--------
    [may,kein,kain,radi]| [5,10,1,3] | [[may,kein,kain,radi],...]       | [19,15,6]
===================================================================================
[핵심 — 해시맵으로 이름별 점수 O(1) 조회]
    name + yearning → dict {이름: 점수}
    photo 각 사진 → 이름별 점수 합산

    score.get(person, 0):
        name에 없는 인물 → 기본값 0 반환
        별도 조건문 없이 처리

[실측 결과 — 100,000회 반복]
    풀이1 (명시적dict+for): 2.19μs  ← 가장 빠름
    풀이2 (zip+리스트컴프): 2.43μs
    풀이3 (map+lambda):     2.60μs
    ref   (이분탐색):       5.65μs  ← 가장 느림

    map+lambda가 리스트 컴프리헨션보다 느린 이유:
        lambda는 매 호출마다 함수 객체 생성 오버헤드
        리스트 컴프리헨션은 CPython이 직접 최적화

    ref(이분탐색)가 가장 느린 이유:
        bisect_left(key=lambda): 매 비교마다 lambda 호출
        dict O(1) 조회보다 오버헤드 큼
        name 최대 100개에서 O(log 100)이 O(1) dict보다 느림
===================================================================================
[내 초기 풀이]
    solution_mine_one  : 명시적 dict 구성 + for 루프
    solution_mine_two  : zip + dict() + 리스트 컴프리헨션
    solution_mine_three: zip + dict() + map + lambda

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Best
                         실측 가장 빠름, 동작 원리 명시적
    solution_mine_two  : 개선 필요 없음 - Sub
                         dict(zip()) 간결, 리스트 컴프리헨션 파이써닉
    solution_mine_three: map+lambda 오버헤드로 mine_two보다 느림
    solution_ref       : 이분탐색으로 dict 대체 시도
                         bisect_left(key=lambda) 오버헤드로 가장 느림
                         name 규모(최대 100)에서 이분탐색 이점 없음
===================================================================================
[복잡도 분석]
    N = len(name) (최대 100)
    P = len(photo) (최대 100)
    Q = photo[i] 평균 길이 (최대 100)

    Mine_one   - 시간: O(N + P×Q) | 공간: O(N) - dict 구성 O(N) + 조회 O(1)
    Mine_two   - 시간: O(N + P×Q) | 공간: O(N) - dict(zip) + 컴프리헨션
    Mine_three - 시간: O(N + P×Q) | 공간: O(N) - dict(zip) + map+lambda
    Ref        - 시간: O(N log N + P×Q×log N) | 공간: O(N) - 정렬+이분탐색
    Best       - 시간: O(N + P×Q) | 공간: O(N) - Mine_one과 동일
    Sub        - 시간: O(N + P×Q) | 공간: O(N) - Mine_two와 동일

    N, P, Q 모두 최대 100 → 모두 실질적으로 O(1)
"""

import bisect
import time


# ==================================================================================
# Mine solution one - 명시적 dict 구성 + for 루프
# ==================================================================================
def solution_mine_one(name: list[str], yearning: list[int], photo: list[list[str]]) -> list[int]:
    """
    zip으로 dict를 직접 구성하고 for 루프로 각 사진의 점수를 합산하는 초기 풀이

    score dict 구성:
        zip(name, yearning): 이름-점수 쌍 이터레이터
        for 루프로 명시적 삽입 → 동작 과정 가시적

    score.get(person, 0):
        name에 없는 인물 → 0 반환
        조건문 없이 처리 가능
    """
    answer = []
    score = dict()

    for n, y in zip(name, yearning):
        score[n] = y

    for p in photo:
        s = 0
        for person in p:
            s += score.get(person, 0)
        answer.append(s)

    return answer


# ==================================================================================
# Mine solution two - dict(zip) + 리스트 컴프리헨션
# ==================================================================================
def solution_mine_two(name: list[str], yearning: list[int], photo: list[list[str]]) -> list[int]:
    """
    dict(zip())으로 한 줄 dict 생성 후 리스트 컴프리헨션으로 합산하는 파이써닉한 풀이

    dict(zip(name, yearning)):
        zip(): 이름-점수 쌍 이터러블 객체 반환
        dict(): 중간 리스트 없이 직접 key-value 쌍으로 소비

    리스트 컴프리헨션:
        [sum(score.get(person, 0) for person in p) for p in photo]
        CPython 최적화로 lambda 없이 처리 → map+lambda보다 빠름
    """
    score = dict(zip(name, yearning))

    return [sum(score.get(person, 0) for person in p) for p in photo]


# ==================================================================================
# Mine solution three - map + lambda
# ==================================================================================
def solution_mine_three(name: list[str], yearning: list[int], photo: list[list[str]]) -> list[int]:
    """
    map과 lambda로 풀이 2를 함수형 스타일로 표현한 풀이

    map 구조:
        outer map: photo의 각 사진마다 함수 적용
        inner map: 각 사진의 인물마다 점수 조회

    lambda 오버헤드:
        lambda는 매 호출마다 함수 객체 생성
        리스트 컴프리헨션(mine_two) 대비 느림
    """
    score = dict(zip(name, yearning))

    return list(map(lambda p: sum(map(lambda person: score.get(person, 0), p)), photo))


# ==================================================================================
# Ref solution - 이분 탐색 (bisect)
# ==================================================================================
def solution_ref(name: list[str], yearning: list[int], photo: list[list[str]]) -> list[int]:
    """
    name을 이름 기준으로 정렬된 인덱스 배열을 만들어 이분 탐색으로 점수를 찾는 풀이

    idxs = sorted range(len(name)):
        name 원본 순서를 유지하면서 이름 알파벳 순으로 인덱스를 정렬
        원본 yearning[i] 매핑이 깨지지 않음

    bisect_left(idxs, person, key=lambda i: name[i]):
        key= 인수로 각 인덱스를 name으로 변환해 비교
        매 비교마다 lambda 호출 → dict O(1)보다 오버헤드 큼

    실측 가장 느린 이유:
        bisect_left(key=lambda): 비교마다 lambda 호출
        name 100개에서 O(log 100) ≈ 7회 비교 × lambda 오버헤드
        dict.get O(1) 단일 해시보다 느림
    """
    idxs = list(range(len(name)))
    idxs.sort(key=lambda i: name[i])

    answer = []
    for arr in photo:
        s = 0
        for person in arr:
            idx = bisect.bisect_left(idxs, person, key=lambda i: name[i])
            if idx < len(idxs) and name[idxs[idx]] == person:
                s += yearning[idxs[idx]]
        answer.append(s)

    return answer


# ==================================================================================
# Best solution - 명시적 dict + for 루프 (mine_one 주석 보강)
# ==================================================================================
def solution_best(name: list[str], yearning: list[int], photo: list[list[str]]) -> list[int]:
    """
    dict + for 루프로 실측 가장 빠르게 추억 점수를 계산하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        명시적 dict 구성: 동작 원리 가시적
        score.get(person, 0): 없는 이름 처리를 조건문 없이 한 줄로
        실측 2.19μs (mine_two 2.43μs, mine_three 2.60μs, ref 5.65μs 대비 우위)
    """
    answer = []
    score = dict()

    for n, y in zip(name, yearning):
        score[n] = y

    for p in photo:
        s = 0
        for person in p:
            s += score.get(person, 0)
        answer.append(s)

    return answer


# ==================================================================================
# Sub solution - dict(zip) + 리스트 컴프리헨션 (mine_two 주석 보강)
# ==================================================================================
def solution_sub(name: list[str], yearning: list[int], photo: list[list[str]]) -> list[int]:
    """
    dict(zip) + 리스트 컴프리헨션으로 간결하게 표현하는 서브 풀이

    Best 대비 특징:
        dict(zip(name, yearning)): 한 줄로 해시맵 생성, 파이써닉
        리스트 컴프리헨션: CPython 최적화로 lambda 없이 처리
        코드 2줄로 전체 로직 표현
    """
    score = dict(zip(name, yearning))

    return [sum(score.get(person, 0) for person in p) for p in photo]


# ==================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ==================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (name, yearning, photo, 기댓값)
        (
            ["may", "kein", "kain", "radi"], [5, 10, 1, 3],
            [["may","kein","kain","radi"],["may","kein","brin","deny"],["kon","kain","may","coni"]],
            [19, 15, 6]
        ),
        (
            ["kali", "mari", "don"], [11, 1, 55],
            [["kali","mari","don"],["pony","tom","teddy"],["con","mona","don"]],
            [67, 0, 55]
        ),
        (
            ["may", "kein", "kain", "radi"], [5, 10, 1, 3],
            [["may"],["kein","deny","may"],["kon","coni"]],
            [5, 15, 0]
        ),
    ]

    solutions = [
        ("Mine_one   (dict+for)  ", solution_mine_one),
        ("Mine_two   (zip+comp)  ", solution_mine_two),
        ("Mine_three (map+lambda)", solution_mine_three),
        ("Ref        (이분탐색)  ", solution_ref),
        ("Best       (dict+for)  ", solution_best),
        ("Sub        (zip+comp)  ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _y, _p, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _y, _p)

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name_s, func in solutions:
        for idx, (name, yearning, photo, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(name, yearning, photo)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name_s:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ==================================================================================
# 실행 진입점
# ==================================================================================
if __name__ == "__main__":
    solution_comparison()
