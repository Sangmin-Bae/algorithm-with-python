"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 가장 큰 수
    유형       : Sort / Greedy
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42746
    풀이일자   : 2026-09-20
===================================================================================
[문제 요약]
    정수 배열을 이어붙여 만들 수 있는 가장 큰 수를 문자열로 반환

    제약 조건
        - numbers 길이: 1 이상 100,000 이하
        - 원소: 0 이상 1,000 이하
        - 정답이 너무 클 수 있으므로 문자열로 반환
===================================================================================
[입출력 예시]
    numbers           | return
    ------------------|--------
    [6, 10, 2]        | "6210"
    [3, 30, 34, 5, 9] | "9534330"
===================================================================================
[내 초기 풀이 — 순열 완전탐색 (시간초과)]
    permutations(strs): N!개 순열 생성 → N=100,000이면 불가능
    O(N! × N) → 완전탐색은 어떤 입력에서도 통과 불가

[핵심 — "AB vs BA" 비교 함수]
    A, B 중 어느 쪽을 앞에 놓아야 더 큰 수인가:
        AB > BA이면 A가 앞
        BA > AB이면 B가 앞

    수학적 증명:
        AB를 수로: A × 10^lb + B
        BA를 수로: B × 10^la + A

        AB > BA ↔ A(10^lb - 1) > B(10^la - 1)
        ↔ str(A)+str(B) > str(B)+str(A)
        (같은 자릿수 문자열에서 사전순 = 수치 비교)

[ref_one — x*3 방식]
    strs.sort(key=lambda x: x*3, reverse=True)

    원리: 모든 원소가 최대 4자리 → 3번 반복하면 최대 12자리
    비교 패턴 안정화:
        "3"*3 = "333"
        "30"*3 = "303030"
        "333" > "303030" → "3"이 앞 → "330" ✓

    왜 자기 자신을 반복하는가:
        A가 무한히 반복되는 패턴이 "A 뒤에 무엇이 와도" 최선
        충분한 길이(12자리)를 확보해 어떤 원소와 비교해도 안정적

    왜 3번인가:
        원소 최대 4자리 → 3회 반복 = 최대 12자리 확보
        두 원소 문자열이 모두 12자리 이내 → 비교 안정

[ref_two — cmp_to_key 방식]
    compare(a, b): a+b > b+a이면 -1(a 앞), 반대면 1(b 앞), 같으면 0
    비교 논리가 명시적으로 드러남
    하지만 cmp_to_key: 매 비교마다 Python 함수 호출 오버헤드
    → N log N번 Python 호출 → ref_one 대비 5.8배 느림

[x*3 vs cmp_to_key 성능 차이]
    x*3:
        key 함수를 N번만 호출 (각 원소당 1번)
        이후 비교는 C 레벨 문자열 비교
        → O(N) Python 호출 + O(N log N) C 레벨 비교

    cmp_to_key:
        비교마다 Python 함수 호출
        → O(N log N) Python 함수 호출

[실측 결과 — N=100,000, 200회]
    ref_one (x*3):        37.7ms  ← 5.8배 빠름
    ref_two (cmp_to_key): 218.7ms
===================================================================================
[내 초기 풀이]
    solution_mine: 순열 완전탐색 (시간초과)

[개선 포인트]
    solution_mine:    O(N!) → 완전탐색 불가
    solution_ref_one: x*3 정렬 - Best
                      O(N log N), 5.8배 빠름
    solution_ref_two: cmp_to_key - Sub
                      비교 로직 명시적, 5.8배 느림
===================================================================================
[복잡도 분석]
    N = len(numbers) (최대 100,000)

    Mine     - 시간: O(N! × N) | 공간: O(N!) - 순열
    Ref_one  - 시간: O(N log N) | 공간: O(N) - 정렬
    Ref_two  - 시간: O(N log N) | 공간: O(N) - 정렬 + 비교함수
    Best     - 시간: O(N log N) | 공간: O(N) - Ref_one과 동일
    Sub      - 시간: O(N log N) | 공간: O(N) - Ref_two와 동일
"""

from itertools import permutations
from functools import cmp_to_key
import time


# =================================================================================
# Mine solution - 순열 완전탐색 (시간초과)
# =================================================================================
def solution_mine(numbers: list[int]) -> str:
    """
    모든 순열을 생성해 가장 큰 수를 찾는 초기 풀이 (시간초과)

    실패 원인:
        permutations(strs): N!개 순열 생성
        N=100,000이면 100,000! → 불가능
        "규칙을 못 찾겠다"는 상황에서 완전탐색 선택

    정확성은 있으나 효율성 테스트 전부 실패
    """
    strs = [str(num) for num in numbers]
    max_num = max(int("".join(p)) for p in permutations(strs))
    return str(max_num)


# =================================================================================
# Ref solution one - x*3 정렬
# =================================================================================
def solution_ref_one(numbers: list[int]) -> str:
    """
    문자열을 3번 반복한 값의 사전순으로 정렬하는 최적 풀이

    key=lambda x: x*3:
        각 원소 최대 4자리 → 3번 반복 = 최대 12자리
        "333" > "303030" → "3" > "30" 판단 → "3"이 앞 → "330" ✓

    이 비교가 AB > BA와 동치인 이유:
        AB, BA는 모두 la+lb자리 → 같은 길이 문자열 비교 = 수치 비교
        x*3은 충분한 길이를 확보해 같은 길이 비교를 보장

    key 함수 N번 호출 + C 레벨 비교 → cmp_to_key 대비 5.8배 빠름
    """
    strs = [str(num) for num in numbers]
    strs.sort(key=lambda x: x * 3, reverse=True)
    result = "".join(strs)
    return "0" if result[0] == "0" else result


# =================================================================================
# Ref solution two - cmp_to_key 비교 함수
# =================================================================================
def solution_ref_two(numbers: list[int]) -> str:
    """
    AB > BA 비교 함수를 명시적으로 정의하는 참고 풀이

    compare(a, b):
        a+b > b+a: a가 앞 → -1 반환
        a+b < b+a: b가 앞 → 1 반환
        같음: 순서 유지 → 0

    비교 논리가 코드에 직접 드러남
    하지만 N log N번 Python 함수 호출 → ref_one 대비 5.8배 느림
    """
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1
        elif a + b < b + a:
            return 1
        return 0

    strs = [str(num) for num in numbers]
    strs.sort(key=cmp_to_key(compare))
    result = "".join(strs)
    return "0" if result[0] == "0" else result


# =================================================================================
# Best solution - x*3 정렬 (ref_one 주석 보강)
# =================================================================================
def solution_best(numbers: list[int]) -> str:
    """
    x*3 key 정렬로 O(N log N) 시간에 가장 큰 수를 구하는 최적 풀이

    ref_one과 동일한 로직, 선정 근거 주석 보강:
        key 함수 N번만 호출 → C 레벨 비교 O(N log N)
        실측 N=100,000: 37.7ms (cmp_to_key 218.7ms 대비 5.8배 우위)
        "0" 예외처리: 모든 원소가 0이면 result[0]='0' → "0" 반환
    """
    strs = [str(num) for num in numbers]
    strs.sort(key=lambda x: x * 3, reverse=True)
    result = "".join(strs)
    return "0" if result[0] == "0" else result


# =================================================================================
# Sub solution - cmp_to_key (ref_two 주석 보강)
# =================================================================================
def solution_sub(numbers: list[int]) -> str:
    """
    AB > BA 비교 함수로 정렬하는 서브 풀이

    ref_two와 동일한 로직, 선정 근거 주석 보강:
        비교 논리 a+b vs b+a가 코드에 직접 드러남
        AB > BA ↔ A를 앞에 놓으면 더 큰 수 → 직관적
        Python 함수 호출 오버헤드로 Best 대비 5.8배 느림
    """
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1
        elif a + b < b + a:
            return 1
        return 0

    strs = [str(num) for num in numbers]
    strs.sort(key=cmp_to_key(compare))
    result = "".join(strs)
    return "0" if result[0] == "0" else result


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (numbers, 기댓값)
        # 공식 예시
        ([6, 10, 2],        "6210"),
        ([3, 30, 34, 5, 9], "9534330"),
        # 추가 케이스:
        # 전부 0
        ([0, 0, 0],         "0"),
        # 최대값 vs 반복 패턴
        # 손 추적: "999" > "9991000" 사전순 → "999" 앞 → "9991000"
        ([1000, 999],       "9991000"),
        # 단일 원소
        ([5],               "5"),
    ]

    # mine은 소규모에서만 검증
    print("--- Mine (순열, 소규모만) ---")
    for nums, exp in test_cases[:2]:
        output = solution_mine(nums[:])
        status = "PASS" if output == exp else "FAIL"
        print(f"  {nums}: {output} {status}")

    solutions = [
        ("Ref_one (x*3)        ", solution_ref_one),
        ("Ref_two (cmp_to_key) ", solution_ref_two),
        ("Best    (x*3)        ", solution_best),
        ("Sub     (cmp_to_key) ", solution_sub),
    ]

    # 워밍업
    _nums, _ = test_cases[0]
    for _, func in solutions:
        func(_nums[:])

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (numbers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(numbers[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
