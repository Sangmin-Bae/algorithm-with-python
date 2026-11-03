"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6305. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 2. 자료구조 -리스트, 튜플 27
    유형       : Filter (중복 제거), Dictionary, Set
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcWAjaa5RkDFAU4
    풀이일자   : 2026-11-03
================================================================================
[문제 요약]
    리스트의 중복되는 항목을 제거하는 함수를 정의하고, 이 함수로
    [12, 24, 35, 24, 88, 120, 155, 88, 120, 155]에서 중복이 제거된 리스트를 출력

    입력 방식 : 입력 없음 (리스트가 지문에 고정)
    적용 방식 : 고정된 리스트 → 매개변수 nums, output → 중복을 제거한 리스트를 반환
    지문 조건 : 중복 제거 함수를 정의하고 그 함수를 이용
    참고      : 출력 예시는 처음 등장한 순서를 유지한 형태 (이 예시는 오름차순과도 같음)
================================================================================
[입출력 예시]
    공식 예시
    nums                                                | return
    ----------------------------------------------------|--------------------------------
    [12, 24, 35, 24, 88, 120, 155, 88, 120, 155]        | [12, 24, 35, 88, 120, 155]

    자체 검증 케이스 (전부 손 계산, 처음 등장한 순서 유지)
    nums                | return
    --------------------|-----------------
    []                  | []
    [5]                 | [5]
    [1, 1, 1, 1]        | [1]
    [3, 1, 2, 3]        | [3, 1, 2]        (뒤의 3만 제거, 순서 유지)
    [2, 1, 2, 1]        | [2, 1]
    [0, ..., 999] * 3   | [0, ..., 999]    (대용량, 처음 등장한 순서)
================================================================================
[풀이 전략]
    핵심: 이미 나온 값을 기억해 두고 처음 등장한 값만 남기기
        결과에 이미 있는지(또는 이미 본 값인지) 검사한 뒤 없을 때만 추가

    풀이 구성:
        mine_one   : 결과 리스트에 없을 때만 append
                     n not in result : 리스트를 앞에서부터 비교하므로 O(결과 길이)
        mine_two   : list(dict.fromkeys(lst))
                     dict.fromkeys : 값을 key로 하는 딕셔너리 생성, 같은 key는 한 번만 저장
                     딕셔너리는 key를 넣은 순서를 유지 (파이썬 3.7부터 언어 명세)
        mine_three : list(set(lst))
                     집합은 중복을 자동으로 제거하나 순회 순서는 보장되지 않음
        best       : mine_two와 동일 (한 줄, 등장 순서 유지, 선형 시간)
        sub        : 본 값을 집합에 기록하며 처음 본 값만 append
                     mine_one의 not in result를 집합 조회로 개선, dict.fromkeys의 동작을 풀어 쓴 형태

    집합의 순회 순서:
        정수 집합의 순서는 해시 값과 내부 테이블 크기로 정해지고 언어가 보장하지 않음
        공식 예시에 list(set(nums))를 적용하면 파이썬 3.12.3에서 [35, 12, 155, 24, 88, 120]
        (원소는 같고 순서가 다름)
        오름차순이 필요하면 sorted(set(nums))로 순서를 지정

    해시 가능한 값:
        dict.fromkeys와 set은 값이 해시 가능해야 함 (정수, 문자열, 튜플은 가능, 리스트는 불가)
        not in 검사만 쓰는 mine_one은 리스트 원소에도 동작

    손 추적 (공식 예시) best:
        12 → 키 추가   24 → 키 추가   35 → 키 추가   24 → 이미 있음
        88 → 키 추가   120 → 키 추가  155 → 키 추가  88, 120, 155 → 이미 있음
        키 순서 [12, 24, 35, 88, 120, 155] ✓
================================================================================
[개선 포인트]
    solution_mine_one   : 개선 여지 있음 - 리스트 안의 not in 검사로 O(N * U), 집합 조회로 O(N)
    solution_mine_two   : 개선 여지 없음 - 한 줄, 선형 시간, 순서 유지
    solution_mine_three : 개선 여지 있음 - 순서가 보장되지 않아 지문 예시와 다른 순서가 나올 수 있음
    solution_best       : mine_two와 동일 로직 - Best
    solution_sub        : not in result를 집합 조회로 개선 - 순서 유지 + 선형 시간
================================================================================
[복잡도 분석]
    N = len(nums), U = 중복을 제거한 원소 수

    Mine_one   - 시간: O(N * U) | 공간: O(U) - 원소마다 결과 리스트를 앞에서부터 비교
    Mine_two   - 시간: O(N)     | 공간: O(U) - 해시 조회로 중복 확인
    Mine_three - 시간: O(N)     | 공간: O(U) - 순서 보장 없음
    Best       - 시간: O(N)     | 공간: O(U) - mine_two와 동일
    Sub        - 시간: O(N)     | 공간: O(U) - 집합과 결과 리스트를 따로 저장
"""

import time


# ================================================================================
# Mine solution one - not in 으로 검사하며 append
# ================================================================================
def solution_mine_one(nums: list[int]) -> list[int]:
    """
    결과 리스트에 없는 값만 append하는 풀이

    핵심:
        n not in result : 결과에 이미 있는지 검사
        처음 등장한 값만 추가되어 순서 유지
        검사가 리스트 순회라 중복이 적고 길이가 길면 느림
    """
    def remove_duplicated(lst: list[int]) -> list[int]:
        result = []

        for n in lst:
            if n not in result:
                result.append(n)

        return result

    return remove_duplicated(nums)


# ================================================================================
# Mine solution two - dict.fromkeys
# ================================================================================
def solution_mine_two(nums: list[int]) -> list[int]:
    """
    dict.fromkeys로 값을 key로 만들어 중복을 제거하는 풀이

    핵심:
        dict.fromkeys(lst) : 값을 key로 하는 딕셔너리, 같은 key는 한 번만 저장
        key를 넣은 순서가 유지되어 처음 등장한 순서 유지
        list(...)로 key 목록을 리스트로 변환
    """
    def remove_duplicated(lst: list[int]) -> list[int]:
        return list(dict.fromkeys(lst))

    return remove_duplicated(nums)


# ================================================================================
# Mine solution three - set
# ================================================================================
def solution_mine_three(nums: list[int]) -> list[int]:
    """
    set으로 중복을 제거하는 풀이

    핵심:
        set(lst) : 중복 자동 제거
        순회 순서는 보장되지 않아 처음 등장한 순서와 달라질 수 있음
    """
    def remove_duplicated(lst: list[int]) -> list[int]:
        return list(set(lst))

    return remove_duplicated(nums)


# ================================================================================
# Best solution - mine_two와 동일 로직
# ================================================================================
def solution_best(nums: list[int]) -> list[int]:
    """
    mine_two와 동일한 로직의 최적 풀이

    선정 근거:
        한 줄로 간결, 처음 등장한 순서 유지, 선형 시간
    """
    def remove_duplicated(lst: list[int]) -> list[int]:
        return list(dict.fromkeys(lst))

    return remove_duplicated(nums)


# ================================================================================
# Sub solution - 본 값 집합 + append
# ================================================================================
def solution_sub(nums: list[int]) -> list[int]:
    """
    본 값을 집합에 기록하고 처음 본 값만 append하는 풀이

    핵심:
        seen : 이미 본 값의 집합, 조회가 O(1)
        n not in seen이면 seen에 기록하고 result에 추가
        mine_one의 not in result를 집합 조회로 개선
    """
    def remove_duplicated(lst: list[int]) -> list[int]:
        seen = set()
        result = []

        for n in lst:
            if n not in seen:
                seen.add(n)
                result.append(n)

        return result

    return remove_duplicated(nums)


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (nums, 기댓값) - 전부 손 계산, 처음 등장한 순서 유지
        ([12, 24, 35, 24, 88, 120, 155, 88, 120, 155],
         [12, 24, 35, 88, 120, 155]),                       # 공식 예시
        ([], []),                                           # 빈 리스트 경계
        ([5], [5]),                                         # 원소 1개
        ([1, 1, 1, 1], [1]),                                # 전부 같은 값
        ([3, 1, 2, 3], [3, 1, 2]),                          # 순서 유지
        ([2, 1, 2, 1], [2, 1]),                             # 번갈아 중복
        (list(range(1000)) * 3, list(range(1000))),         # 대용량: 1000개를 3번 반복
    ]

    solutions = [
        ("Mine1 (not in)", solution_mine_one),
        ("Mine2 (fromkeys)", solution_mine_two),
        ("Mine3 (set)", solution_mine_three),
        ("Best (fromkeys)", solution_best),
        ("Sub (seen 집합)", solution_sub),
    ]

    # 워밍업: 첫 테스트 케이스로 모든 풀이를 1회씩 실행
    warmup_args = test_cases[0][:-1]
    for _, func in solutions:
        func(*warmup_args)

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'평균 소요시간':>12}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (*args, expected) in enumerate(test_cases, 1):
            output = func(*args)

            start = time.perf_counter()
            for _ in range(repeat):
                func(*args)
            elapsed = (time.perf_counter() - start) / repeat

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed*1000:>10.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
