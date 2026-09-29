"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6303. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 2. 자료구조 -리스트, 튜플 26
    유형       : Set (교집합)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?problemLevel=1&problemLevel=2&problemLevel=3&contestProbId=AWcWAPiq5REDFAU4&categoryId=AWcWAPiq5REDFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=3&pageSize=10&pageIndex=1
    풀이일자   : 2026-09-29
================================================================================
[문제 요약]
    지문에 고정된 두 리스트에서 양쪽에 모두 있는 원소를 리스트로 출력

    입력 방식 : 입력 없음 (두 리스트가 지문에 고정)
    적용 방식 : 고정된 두 리스트 → 매개변수 list_a, list_b, output → 반환값
    참고      : 지문은 결과의 순서와 중복 처리 방식을 명시하지 않음
                (공식 데이터는 공통 원소가 1개라 영향 없음)
================================================================================
[입출력 예시]
    공식 예시
    list_a                | list_b                         | return
    ----------------------|--------------------------------|-------
    [1, 3, 6, 78, 35, 55] | [12, 24, 35, 24, 88, 120, 155] | [35]

    자체 검증 케이스 (전부 손 계산)
    list_a       | list_b       | return
    -------------|--------------|------------
    [1, 2, 3, 4] | [3, 4, 5, 6] | [3, 4]
    [1, 2, 3]    | [4, 5, 6]    | []
    [1, 2, 3]    | [2, 2, 3, 3] | [2, 3]
    [5, 10, 15]  | [15, 10, 5]  | [5, 10, 15]

    의미 차이 예시 (풀이 간 비교 표에는 넣지 않음)
    list_a = [3, 1, 3], list_b = [3, 1]
        mine_one / best : [3, 1, 3]  (list_a의 순서와 중복 유지)
        sub             : [1, 3]     (중복 제거 + 정렬)
================================================================================
[풀이 전략]
    핵심: list_a의 각 원소가 list_b에도 있는지 "멤버십 검사" 반복

    mine_one : [n for n in list_a if n in list_b]
        list에 대한 in은 앞에서부터 순차 탐색 → 원소 하나당 최대 m번 비교

    best     : set_b = set(list_b) 후 [n for n in list_a if n in set_b]
        set의 in은 해시 조회(평균 O(1)) → 원소 하나당 비교 1회 수준
        결과는 mine_one과 완전히 동일 (list_a의 순서·중복 유지)

    sub      : sorted(set(list_a) & set(list_b))
        집합 교집합 연산으로 한 번에 처리
        단, 결과가 중복 제거 + 정렬 → mine_one과 의미가 다를 수 있음

    손 추적 (공식 예시):
        mine_one: 1, 3, 6, 78 → list_b 끝까지 탐색해도 없음
                  35 → list_b 인덱스 2에서 발견 → 선택
                  55 → 없음 → [35]
        best    : set_b = {12, 24, 35, 88, 120, 155} (중복 24는 하나로 합쳐짐)
                  35만 set_b에 있음 → [35]
        sub     : set_a & set_b = {35} → sorted → [35] ✓

    SWEA 제출 형태 (함수 본문 아래에 이어 붙여 제출):
        list_a = [1, 3, 6, 78, 35, 55]
        list_b = [12, 24, 35, 24, 88, 120, 155]
        print(solution_best(list_a, list_b))

    제출 이력:
        mine_one과 동일한 로직으로 SWEA 제출 테스트 통과 (2026-09-29)
================================================================================
[실측 결과 — list_a = 0~1999, list_b = 1000~2999 (n = m = 2,000), 30회 평균, 워밍업 1회]
    mine_one (list in)   : 16.8ms
    sub      (set &)     :  0.13ms
    best     (set lookup):  0.069ms  ← 가장 빠름 (mine_one 대비 약 240배)
    (Python 3.12.3 샌드박스 측정, 입력 크기는 지문에 없어 자체 기준)

    크기별 추이 (n = m, 5회 평균):
        n = 1,000 → mine_one  4.5ms | best 0.033ms
        n = 2,000 → mine_one 16.6ms | best 0.079ms
        n = 4,000 → mine_one 65.5ms | best 0.127ms
        mine_one은 n이 2배가 될 때 약 4배 → n * m에 비례하는 흐름과 일치
        best는 훨씬 완만하게 증가 (측정 오차가 있어 정확한 선형성은 단정하지 않음)
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 있음 - list에 대한 in은 순차 탐색
    solution_sub      : 집합 연산으로 간결하지만 순서·중복 의미가 달라짐
    solution_best     : list_b를 set으로 바꿔 조회 비용을 낮추고 의미는 유지 - Best
================================================================================
[복잡도 분석]
    n = len(list_a), m = len(list_b), k = 결과 원소 수

    Mine_one - 시간: O(n * m)    | 공간: O(k)
    Best     - 시간: O(n + m)    | 공간: O(m + k)   (set 생성 + 결과)
    Sub      - 시간: O(n + m + k log k) | 공간: O(n + m)

    Best/Sub의 O(n + m)은 해시 조회의 평균 기준
"""

import time


# ================================================================================
# Mine solution one - 리스트 컴프리헨션 + list의 in 연산
# ================================================================================
def solution_mine_one(list_a: list[int], list_b: list[int]) -> list[int]:
    """
    list_a를 순회하며 각 원소가 list_b에도 있는지 in으로 확인하는 초기 풀이

    핵심:
        n in list_b: list_b를 앞에서부터 순차 탐색
        list_a의 순서와 중복이 그대로 유지됨

    한계:
        원소 하나당 최대 m번 비교 → 전체 O(n * m)
    """
    return [num for num in list_a if num in list_b]


# ================================================================================
# Best solution - list_b를 set으로 바꿔 조회
# ================================================================================
def solution_best(list_a: list[int], list_b: list[int]) -> list[int]:
    """
    list_b를 set으로 변환한 뒤 조회하는 풀이

    핵심:
        set의 in은 해시 조회 → 평균 O(1)
        list_a를 순회하는 구조는 그대로라 결과가 mine_one과 완전히 동일
    """
    set_b = set(list_b)
    return [num for num in list_a if num in set_b]


# ================================================================================
# Sub solution - 집합 교집합
# ================================================================================
def solution_sub(list_a: list[int], list_b: list[int]) -> list[int]:
    """
    두 리스트를 set으로 바꿔 교집합을 구하는 풀이

    핵심:
        set(list_a) & set(list_b): 양쪽에 있는 값의 집합
        set은 순서가 없으므로 sorted로 결과 순서를 고정

    주의:
        list_a의 순서와 중복이 유지되지 않음 (중복 제거 + 정렬)
    """
    return sorted(set(list_a) & set(list_b))


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    # 비교 표의 케이스는 세 풀이의 결과가 같아지는 입력만 사용
    # (list_a에 중복이 없고, 결과가 list_a 순서 = 오름차순으로 나오는 경우)
    test_cases: list[tuple] = [
        # (list_a, list_b, 기댓값) - 전부 손 계산
        ([1, 3, 6, 78, 35, 55], [12, 24, 35, 24, 88, 120, 155], [35]),  # 공식 예시
        ([1, 2, 3, 4], [3, 4, 5, 6], [3, 4]),
        ([1, 2, 3], [4, 5, 6], []),
        ([1, 2, 3], [2, 2, 3, 3], [2, 3]),
        ([5, 10, 15], [15, 10, 5], [5, 10, 15]),
        ([], [1, 2], []),                                # 빈 리스트 경계
        ([7], [7], [7]),
        (list(range(2000)), list(range(1000, 3000)), list(range(1000, 2000))),  # 대용량
    ]

    solutions = [
        ("Mine (list in)",   solution_mine_one),
        ("Best (set lookup)", solution_best),
        ("Sub  (set &)",     solution_sub),
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
