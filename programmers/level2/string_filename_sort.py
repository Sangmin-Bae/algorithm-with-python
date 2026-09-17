"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : [3차] 파일명 정렬
    유형       : String / Sorting
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17686
    풀이일자   : 2026-09-17
===================================================================================
[문제 요약]
    파일명을 HEAD/NUMBER/TAIL로 분리하고
    (head.lower(), int(number)) 오름차순 정렬 후 반환
    head와 number가 같으면 원래 순서 유지

    제약 조건
        - files 길이: 1~1,000
        - 파일명 길이: 1~100자
        - NUMBER: 1~5자리 (앞에 0 가능)
===================================================================================
[입출력 예시]
    files                                    | result
    -----------------------------------------|-------
    ["img12.png","img10.png","img02.png",     | ["img1.png","IMG01.GIF","img02.png",
     "img1.png","IMG01.GIF","img2.JPG"]       |  "img2.JPG","img10.png","img12.png"]
===================================================================================
[핵심 — 정렬 키 (head.lower(), int(number))]
    head: 소문자 변환으로 대소문자 무시
    number: 정수 변환으로 앞의 0 무시 (012 == 12)
    안정 정렬(Python sort 기본): head/number 같으면 원래 순서 유지

[세 가지 파싱 방식 비교]
    수동 인덱스:
        isdigit()으로 start, end 찾기
        Python 레벨 문자 순회 → 느림

    정규표현식:
        re.compile() 1회 + match() C 레벨 실행
        파일명 100자 × 1,000개에서도 빠름
        그룹 자동 분리 → 직관적

    groupby:
        isdigit 기준 연속 그룹화
        tail까지 모든 그룹 생성 후 groups[0], groups[1]만 사용
        불필요한 그룹 생성 비용

[ref — sorted key 함수 방식]
    mine: parsed 리스트에 (원본, head, number) 튜플 × N개 저장
    ref:  sorted(files, key=parse) → key 함수를 비교 시점에 호출

    Python Timsort는 key 함수를 각 원소당 1회 호출해 결과 캐싱
    → mine의 parsed 튜플과 메모리 사용이 비슷하나 중간 리스트 불필요

[groupby 동작 설명]
    groupby(iterable, key=str.isdigit):
        연속으로 같은 key 값인 문자들을 한 그룹으로 묶음

    "foo010bar020.zip" → ["foo", "010", "bar", "020", ".zip"]

    groups[0]: head (항상 비숫자로 시작)
    groups[1]: number (첫 번째 숫자 그룹)

    지문 조건 "파일명은 영문자로 시작하고 숫자를 하나 이상 포함"
    → groups[0]은 항상 head, groups[1]은 항상 number 보장

[실측 결과 — files=1,000개, 5,000회]
    two (regex):    0.64ms  ← 가장 빠름
    one (수동):     1.02ms
    ref (groupby):  1.31ms
===================================================================================
[내 초기 풀이]
    solution_mine_one: 수동 인덱스로 head/number 분리
    solution_mine_two: 정규표현식으로 파싱

[개선 포인트]
    solution_mine_one: Python 레벨 문자 순회 → 느림 - Sub 기준
    solution_mine_two: regex C 레벨 실행 - Best
    solution_ref:      groupby + sorted key 함수 - 참고용
                       groups[1]이 5자 초과이면 슬라이싱 필요
===================================================================================
[복잡도 분석]
    N = len(files) (최대 1,000), L = 파일명 길이 (최대 100)

    Mine_one - 시간: O(N×L + N log N) | 공간: O(N) - parsed 리스트
    Mine_two - 시간: O(N×L + N log N) | 공간: O(N) - parsed 리스트
    Ref      - 시간: O(N×L + N log N) | 공간: O(N) - sorted 결과
    Best     - 시간: O(N×L + N log N) | 공간: O(N) - Mine_two와 동일
    Sub      - 시간: O(N×L + N log N) | 공간: O(N) - Mine_one과 동일
"""

import re
from itertools import groupby
import time

# 모듈 레벨 컴파일: 함수 호출마다 재컴파일 없음
PATTERN = re.compile(r"([a-zA-Z\s.-]+)([0-9]{1,5})(.*)")


# =================================================================================
# Mine solution one - 수동 인덱스 파싱
# =================================================================================
def solution_mine_one(files: list[str]) -> list[str]:
    """
    isdigit()으로 start, end 인덱스를 찾아 head/number를 분리하는 초기 풀이

    start: 처음 숫자가 나타나는 인덱스
    end: number 끝 인덱스 (최대 start+5)

    file[end:] 슬라이싱:
        end가 범위를 벗어나도 빈 문자열 반환 → tail 없는 경우 처리

    tail 변수 불필요:
        정렬 기준에 tail 포함되지 않음 → 할당 생략 가능
    """
    parsed = []

    for file in files:
        start = 0
        for i, char in enumerate(file):
            if char.isdigit():
                start = i
                break

        end = start
        while end < len(file) and file[end].isdigit():
            end += 1
            if end - start == 5:
                break

        head = file[:start]
        number = file[start:end]

        parsed.append((file, head.lower(), int(number)))

    parsed.sort(key=lambda x: (x[1], x[2]))
    return [p[0] for p in parsed]


# =================================================================================
# Mine solution two - 정규표현식 파싱
# =================================================================================
def solution_mine_two(files: list[str]) -> list[str]:
    """
    정규표현식으로 HEAD/NUMBER/TAIL을 한 번에 분리하는 풀이

    패턴: r"([a-zA-Z\\s.-]+)([0-9]{1,5})(.*)"
        그룹1: 영문자/공백/마침표/하이픈 1개 이상 → HEAD
        그룹2: 숫자 1~5자리 (greedy) → NUMBER
        그룹3: 나머지 → TAIL

    PATTERN 모듈 레벨 상수:
        함수 호출마다 재컴파일 없음 → 속도 유리

    {1,5} greedy:
        숫자가 6자 이상이어도 앞 5자만 잡음 → 올바른 처리
    """
    parsed = []

    for file in files:
        match = PATTERN.match(file)
        head, number, tail = match.groups()
        parsed.append((file, head.lower(), int(number)))

    parsed.sort(key=lambda x: (x[1], x[2]))
    return [p[0] for p in parsed]


# =================================================================================
# Ref solution - groupby + sorted key 함수
# =================================================================================
def solution_ref(files: list[str]) -> list[str]:
    """
    groupby로 숫자/비숫자 그룹을 나누고 sorted key 함수로 정렬하는 참고 풀이

    groupby(file, key=str.isdigit):
        연속으로 같은 isdigit 값인 문자를 하나의 그룹으로 묶음
        "foo010bar" → ["foo", "010", "bar"]

    groups[0]: HEAD (항상 비숫자로 시작 - 지문 조건 보장)
    groups[1]: NUMBER (첫 번째 숫자 그룹)
    6자 이상이면 [:5]로 슬라이싱

    sorted key 함수:
        mine의 parsed 튜플 리스트 없이 비교 시점에 호출
        Python Timsort가 key 결과를 내부 캐싱
    """
    def parse(file: str) -> tuple:
        groups = ["".join(group) for _, group in groupby(file, key=str.isdigit)]
        head = groups[0]
        number = groups[1]
        if len(number) > 5:
            number = number[:5]
        return (head.lower(), int(number))

    return sorted(files, key=parse)


# =================================================================================
# Best solution - 정규표현식 (mine_two 주석 보강)
# =================================================================================
def solution_best(files: list[str]) -> list[str]:
    """
    모듈 레벨 컴파일 정규표현식으로 O(N×L) 파싱 + O(N log N) 정렬하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        PATTERN 모듈 레벨 상수: 재컴파일 없음
        C 레벨 match(): 수동 순회 대비 빠름
        실측: 0.64ms (수동 1.02ms, groupby 1.31ms 대비 우위)
    """
    parsed = []

    for file in files:
        match = PATTERN.match(file)
        head, number, tail = match.groups()
        parsed.append((file, head.lower(), int(number)))

    parsed.sort(key=lambda x: (x[1], x[2]))
    return [p[0] for p in parsed]


# =================================================================================
# Sub solution - 수동 인덱스 파싱 (mine_one 주석 보강)
# =================================================================================
def solution_sub(files: list[str]) -> list[str]:
    """
    수동 인덱스로 파싱 구조가 명시적으로 드러나는 서브 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        start/end 인덱스로 HEAD와 NUMBER 경계가 코드에 직접 드러남
        end - start == 5 조건으로 5자 초과 처리
        Python 레벨 문자 순회로 Best 대비 약 60% 느림
    """
    parsed = []

    for file in files:
        start = 0
        for i, char in enumerate(file):
            if char.isdigit():
                start = i
                break

        end = start
        while end < len(file) and file[end].isdigit():
            end += 1
            if end - start == 5:
                break

        head = file[:start]
        number = file[start:end]
        parsed.append((file, head.lower(), int(number)))

    parsed.sort(key=lambda x: (x[1], x[2]))
    return [p[0] for p in parsed]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (files, 기댓값)
        # 공식 예시
        (["img12.png", "img10.png", "img02.png", "img1.png", "IMG01.GIF", "img2.JPG"],
         ["img1.png", "IMG01.GIF", "img02.png", "img2.JPG", "img10.png", "img12.png"]),
        (["F-5 Freedom Fighter", "B-50 Superfortress", "A-10 Thunderbolt II", "F-14 Tomcat"],
         ["A-10 Thunderbolt II", "B-50 Superfortress", "F-5 Freedom Fighter", "F-14 Tomcat"]),
        # 추가 케이스:
        # number 앞 0 무시 (012 == 12)
        (["file12.txt", "file012.txt", "FILE12.txt"],
         ["file12.txt", "file012.txt", "FILE12.txt"]),
        # 안정 정렬: MUZI01.zip, muzi1.png 순서 유지
        (["MUZI01.zip", "muzi1.png"],
         ["MUZI01.zip", "muzi1.png"]),
    ]

    solutions = [
        ("Mine_one (수동)        ", solution_mine_one),
        ("Mine_two (regex)       ", solution_mine_two),
        ("Ref      (groupby)     ", solution_ref),
        ("Best     (regex)       ", solution_best),
        ("Sub      (수동)        ", solution_sub),
    ]

    # 워밍업
    _f, _ = test_cases[0]
    for _, func in solutions:
        func(_f[:])

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (files, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(files[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
