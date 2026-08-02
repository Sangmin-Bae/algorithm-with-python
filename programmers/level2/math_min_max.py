"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 최댓값과 최솟값
    유형       : Math / String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12939
    풀이일자   : 2026-08-02
================================================================================
[문제 요약]
    공백으로 구분된 숫자 문자열 s에서 최솟값과 최댓값을 찾아
    "(최솟값) (최댓값)" 형태로 반환

    제약 조건
        - s에는 둘 이상의 정수가 공백으로 구분되어 있음
================================================================================
[입출력 예시]
    s              | return
    ---------------|-------
    "1 2 3 4"      | "1 4"
    "-1 -2 -3 -4"  | "-4 -1"
    "-1 -1"        | "-1 -1"
================================================================================
[풀이별 int() 변환 횟수 비교]
    풀이1: int() × N회 → min O(N) → max O(N)
           변환 N회, 이후 비교는 이미 변환된 정수 대상

    풀이2: sorted에서 key=int로 비교마다 int() 호출
           정렬 O(N log N) + 비교마다 형변환 → 가장 느림

    풀이3: min에서 int() × N회 + max에서 int() × N회
           변환 2N회 → 풀이1보다 int() 호출 2배
           key=int 방식의 숨겨진 비용

    풀이4: map(int, ...)으로 이터레이터 생성
           단일 순회에서 int() × N회 + 비교 × N회
           리스트 생성 없음 → 가장 빠름

[실측 결과 — 숫자 1,000개, 10,000회 반복]
    풀이4 (map+단일순회): 0.132ms  ← 가장 빠름
    풀이1 (list+min/max): 0.144ms
    풀이2 (sorted+인덱스): 0.190ms
    풀이3 (split+key=int): 0.255ms  ← 가장 느림

    풀이3이 느린 이유:
        key=int: min, max 각각이 N번 int() 호출 → 총 2N회
        풀이1은 변환 N회만 → 풀이3 대비 int() 호출 절반

    풀이4가 빠른 이유:
        리스트 생성 없이 map 이터레이터로 스트리밍
        단일 순회로 min/max 동시 추적
================================================================================
[내 초기 풀이]
    solution_mine_one  : list(map(int)) + min/max
    solution_mine_two  : sorted(key=int) + 인덱스 접근
    solution_mine_three: split + min/max(key=int)
    solution_mine_four : map 이터레이터 + 단일 순회

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         가독성 우위, int() 변환 N회
    solution_mine_two  : O(N log N) 정렬 + 매 비교마다 key=int
                         최댓값은 nums[-1] (설명 오타: 인덱스 1 → 마지막)
    solution_mine_three: key=int로 int() 2N회 발생 → 실측 가장 느림
                         O(N) + O(N) 분석은 맞으나 상수 인자 큼
    solution_mine_four : 개선 필요 없음 - Best
                         리스트 생성 없이 단일 순회, 실측 가장 빠름
                         스트리밍 환경에서도 적용 가능한 패턴
================================================================================
[복잡도 분석]
    N = 숫자 개수

    Mine_one   - 시간: O(N) | 공간: O(N) - int 리스트 생성 + min/max 각 O(N)
    Mine_two   - 시간: O(N log N) | 공간: O(N) - sorted
    Mine_three - 시간: O(N) | 공간: O(N) - split 리스트 + key=int 2N회
    Mine_four  - 시간: O(N) | 공간: O(1) - map 이터레이터 + 단일 순회
    Best       - 시간: O(N) | 공간: O(1) - Mine_four와 동일
    Sub        - 시간: O(N) | 공간: O(N) - Mine_one과 동일
"""

import time


# ================================================================================
# Mine solution one - list(map(int)) + min/max
# ================================================================================
def solution_mine_one(s: str) -> str:
    """
    문자열을 정수 리스트로 변환 후 min/max로 최솟값/최댓값을 구하는 초기 풀이

    list(map(int, s.split())):
        s.split(): 공백 기준 분리 → 문자열 리스트
        map(int, ...): 각 문자열을 int로 변환하는 이터레이터
        list(...): 이터레이터를 리스트로 수집 → int 리스트

    int() 변환 N회, 이후 min/max는 이미 변환된 정수 대상
    가독성 우위 → Sub 선정
    """
    nums = list(map(int, s.split()))
    return f"{min(nums)} {max(nums)}"


# ================================================================================
# Mine solution two - sorted(key=int) + 인덱스 접근
# ================================================================================
def solution_mine_two(s: str) -> str:
    """
    정렬 후 첫 번째/마지막 원소로 최솟값/최댓값을 반환하는 풀이

    sorted(s.split(), key=int):
        문자열 원소를 int로 변환해 비교하되 원소 자체는 문자열 유지
        오름차순 정렬: nums[0] = 최솟값, nums[-1] = 최댓값

    한계:
        O(N log N) 정렬 → min/max O(N)보다 불리
        정렬 중 매 비교마다 key=int 호출 → 추가 변환 비용
    """
    nums = sorted(s.split(), key=int)
    return f"{nums[0]} {nums[-1]}"


# ================================================================================
# Mine solution three - split + min/max(key=int)
# ================================================================================
def solution_mine_three(s: str) -> str:
    """
    문자열 리스트에서 key=int로 비교해 최솟값/최댓값을 찾는 풀이

    min(nums, key=int), max(nums, key=int):
        int 변환 없이 문자열 리스트 사용
        key=int: 비교 시 int로 변환해 비교 (원소는 문자열 유지)

    숨겨진 비용:
        min에서 int() × N회 + max에서 int() × N회 = 총 2N회
        풀이1(N회) 대비 int() 호출 2배 → 실측 가장 느림
        이론상 O(N) + O(N) = O(N)이나 상수 인자가 커서 실측 불리
    """
    nums = s.split()
    return f"{min(nums, key=int)} {max(nums, key=int)}"


# ================================================================================
# Mine solution four - map 이터레이터 + 단일 순회
# ================================================================================
def solution_mine_four(s: str) -> str:
    """
    map 이터레이터로 리스트 없이 단일 순회해 최솟값/최댓값을 구하는 풀이

    map(int, s.split()):
        리스트 생성 없이 int 변환 이터레이터
    next(nums):
        첫 원소를 꺼내 min_v, max_v 초기화
    for n in nums:
        나머지 원소를 순회하며 조건으로 갱신

    장점:
        리스트 생성 없음 → 공간 O(1)
        단일 순회로 min/max 동시 추적 → int() 변환 N회만
        스트리밍 환경에서도 적용 가능

    제약 조건 "둘 이상 정수" 보장:
        next(nums)로 첫 원소 초기화 후 나머지 순회
        숫자가 하나뿐이어도 for 루프 안 돌고 정확히 처리되나
        이 문제에선 둘 이상 보장이므로 안전
    """
    nums = map(int, s.split())
    min_v = max_v = next(nums)

    for n in nums:
        if n < min_v: min_v = n
        if n > max_v: max_v = n

    return f"{min_v} {max_v}"


# ================================================================================
# Best solution - map 이터레이터 + 단일 순회 (mine_four 주석 보강)
# ================================================================================
def solution_best(s: str) -> str:
    """
    map 이터레이터 + 단일 순회로 O(N) 시간, O(1) 공간에 최적 처리하는 풀이

    mine_four와 동일한 로직, 선정 근거 주석 보강:
        리스트 생성 없음 → 메모리 효율 O(1)
        int() 변환 N회만 → 풀이1의 N회와 동일, 풀이3의 2N회보다 효율적
        실측 숫자 1,000개: 0.132ms (풀이1 0.144ms, 풀이3 0.255ms 대비 우위)
    """
    nums = map(int, s.split())
    min_v = max_v = next(nums)

    for n in nums:
        if n < min_v: min_v = n
        if n > max_v: max_v = n

    return f"{min_v} {max_v}"


# ================================================================================
# Sub solution - list(map(int)) + min/max (mine_one 주석 보강)
# ================================================================================
def solution_sub(s: str) -> str:
    """
    정수 리스트 변환 후 min/max로 최솟값/최댓값을 구하는 서브 풀이

    Best 대비 특징:
        list(map(int, ...)): 전체를 정수 리스트로 한 번에 변환
        min/max: C 레벨 내장 함수로 이미 변환된 정수 비교
        가독성 우위 → 의도가 코드에 직접 드러남
        공간 O(N): 정수 리스트 생성
    """
    nums = list(map(int, s.split()))
    return f"{min(nums)} {max(nums)}"


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, str]] = [
        # (s, 기댓값)
        # 공식 예시
        ("1 2 3 4",      "1 4"),
        ("-1 -2 -3 -4",  "-4 -1"),
        ("-1 -1",        "-1 -1"),
        # 추가 케이스:
        ("1 1",          "1 1"),   # 최솟값 == 최댓값
        ("-5 0 5",       "-5 5"),  # 음수/양수 혼합
    ]

    solutions = [
        ("Mine_one   (list+min/max)  ", solution_mine_one),
        ("Mine_two   (sorted+인덱스) ", solution_mine_two),
        ("Mine_three (key=int)       ", solution_mine_three),
        ("Mine_four  (map+단일순회)  ", solution_mine_four),
        ("Best       (map+단일순회)  ", solution_best),
        ("Sub        (list+min/max)  ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
