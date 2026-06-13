"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 서울에서 김서방 찾기
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12919
    풀이일자   : 2026-06-13
===================================================================================
[문제 요약]
    String형 배열 seoul에서 "Kim"의 인덱스 x를 찾아
    "김서방은 x에 있다" 문자열을 반환

    제약 조건
        - seoul 길이: 1 이상 1,000 이하
        - seoul 원소 길이: 1 이상 20 이하
        - "Kim"은 반드시 존재하고 정확히 한 번만 등장
            → list.index() 항상 안전하게 동작, ValueError 불가
===================================================================================
[입출력 예시]
    seoul           | return
    ----------------|---------------------
    ["Jane", "Kim"] | "김서방은 1에 있다"
===================================================================================
[내 초기 풀이]
    solution_mine: list.index()로 "Kim" 인덱스를 찾아 f-string으로 반환

    "Kim"이 반드시 존재하고 중복 없음이 보장되므로
    list.index()가 이 문제에 가장 직접적인 선택

[개선 포인트]
    f-string 따옴표 충돌 주의:
        f"...{seoul.index("Kim")}..." → Python 3.12 이전 SyntaxError
        f'...{seoul.index("Kim")}...' 또는
        f"...{seoul.index('Kim')}..." 로 따옴표 구분 필요
        Python 3.12부터 f-string 내부 동일 따옴표 허용
===================================================================================
[list.index() 동작 원리]
    list.index(value): 리스트를 앞에서부터 순회하며 value와 일치하는 첫 번째 원소의 인덱스를 반환
    시간복잡도: O(N) — 최악의 경우 전체 순회
    "Kim"이 반드시 존재 → 항상 유효한 인덱스 반환
    "Kim"이 중복 없음  → index()가 항상 정확한 위치 반환

    조기 탈출:
        list.index()도 내부적으로 일치하는 값 발견 즉시 반환
        enumerate() + return과 조기 탈출 유무 자체는 동일
        → 조기 탈출 여부는 두 방식의 차이가 아님

    구현 레벨 차이 (같은 O(N)이지만 상수 인자가 다름):
        list.index(): CPython C 레벨 구현
            → Python 인터프리터 개입 없이 C 루프로 직접 탐색
            → 상수 인자 c₁ (매우 작음)
        enumerate() + for: Python 레벨 루프
            → 매 반복마다 Python 인터프리터 오버헤드 발생
            → 상수 인자 c₂ (c₁보다 큼)
        Big-O 표기상 동일(O(N))이나 실제 수행 시간: c₁×N < c₂×N
        N이 작은 이 문제에서는 차이 미미
        N이 크고 복잡한 탐색 로직에서는 구현 레벨 차이가 효율성 테스트에 영향
===================================================================================
[복잡도 분석]
    N = len(seoul) (최대 1,000)

    Mine - 시간: O(N) | 공간: O(1) - list.index() 순차 탐색, 추가 자료구조 없음
    Best - 시간: O(N) | 공간: O(1) - Mine과 동일, 주석 보강
    Sub  - 시간: O(N) | 공간: O(1) - enumerate() 순회, 명시적 비교

    N ≤ 1,000 고정 → 사실상 O(1)에 수렴
"""

import time
from typing import List, Tuple


# =================================================================================
# Mine solution - list.index() + f-string
# =================================================================================
def solution_mine(seoul: List[str]) -> str:
    """
    list.index()로 "Kim"의 인덱스를 찾아 f-string으로 반환하는 초기 풀이

    핵심:
        seoul.index("Kim"): 리스트 순차 탐색으로 "Kim" 첫 등장 인덱스 반환
        f-string: {} 내부에 표현식 직접 삽입 가능
        따옴표 구분: 외부 f' ', 내부 "Kim" → 충돌 없음

    "Kim" 반드시 존재, 중복 없음 보장 → 예외 처리 불필요
    """
    return f'김서방은 {seoul.index("Kim")}에 있다'


# =================================================================================
# Best solution - Mine 주석 보강
# =================================================================================
def solution_best(seoul: List[str]) -> str:
    """
    list.index()로 "Kim" 인덱스를 찾는 최적 풀이

    Mine과 동일한 로직, 근거 주석 보강:
        list.index(): CPython C 레벨 구현, 일치 값 발견 즉시 조기 탈출
        "Kim" 반드시 존재 → ValueError 불가
        "Kim" 중복 없음  → 항상 정확한 인덱스 반환
        enumerate() 방식 대비 C 레벨 구현으로 상수 인자가 작음
        → 단순 일치 탐색에서 list.index()가 Python 루프보다 빠름
    """
    return f'김서방은 {seoul.index("Kim")}에 있다'  # index()로 O(N) 탐색 후 f-string 조합


# =================================================================================
# Sub solution - enumerate() 명시적 순회
# =================================================================================
def solution_sub(seoul: List[str]) -> str:
    """
    enumerate()로 인덱스와 값을 동시에 순회해 "Kim"을 찾는 서브 풀이

    Best 대비 특징:
        index() 내장 메서드 없이 동작 원리를 코드로 명시적으로 표현
        enumerate(seoul): (인덱스, 원소) 튜플을 순서대로 생성
        "Kim" 발견 즉시 return → 조기 탈출 (list.index()와 동일하게 존재)

        구현 레벨 차이:
            list.index(): C 레벨 루프 → 상수 인자 c₁
            enumerate() + for: Python 레벨 루프 → 상수 인자 c₂ (c₁보다 큼)
            시간복잡도 O(N)으로 동일하나 c₁ < c₂
            단순 일치 탐색: list.index() 우위
            복잡한 조건 탐색(단순 == 비교 불가): enumerate() 불가피
    """
    for idx, name in enumerate(seoul):
        if name == "Kim":
            return f'김서방은 {idx}에 있다'   # "Kim" 발견 즉시 반환


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[str], str]] = [
        # (seoul, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # ["Jane", "Kim"]: index("Kim")=1 → "김서방은 1에 있다"
        (["Jane", "Kim"],           "김서방은 1에 있다"),
        # 추가 케이스:
        # ["Kim"]: index("Kim")=0 → "김서방은 0에 있다"
        (["Kim"],                   "김서방은 0에 있다"),
        # ["A","B","C","Kim","D"]: index("Kim")=3 → "김서방은 3에 있다"
        (["A", "B", "C", "Kim", "D"], "김서방은 3에 있다"),
        # ["A","Kim"이 마지막]: index("Kim")=4 → "김서방은 4에 있다"
        (["A", "B", "C", "D", "Kim"], "김서방은 4에 있다"),
    ]

    solutions = [
        ("Mine (index)      ", solution_mine),
        ("Best (index)      ", solution_best),
        ("Sub  (enumerate)  ", solution_sub),
    ]

    print("=" * 62)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 62)

    for name, func in solutions:
        for idx, (seoul, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(seoul[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 62)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
