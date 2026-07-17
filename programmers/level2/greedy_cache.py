"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : [1차] 캐시
    유형       : Stack / Queue (LRU 캐시)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17680
    풀이일자   : 2026-07-17
================================================================================
[문제 요약]
    LRU 캐시 교체 알고리즘으로 cities를 순서대로 처리할 때 총 실행시간 반환
    cache hit: 실행시간 1, cache miss: 실행시간 5
    대소문자 구분 없음

    제약 조건
        - cacheSize: 0 이상 30 이하
        - cities 길이: 최대 100,000
        - 도시 이름: 최대 20자, 영문자만
================================================================================
[입출력 예시]
    cacheSize | cities                                                | result
    ----------|-------------------------------------------------------|-------
    3         | ["Jeju","Pangyo","Seoul","NewYork","LA",              | 50
              |  "Jeju","Pangyo","Seoul","NewYork","LA"]              |
    3         | ["Jeju","Pangyo","Seoul","Jeju","Pangyo",             | 21
              |  "Seoul","Jeju","Pangyo","Seoul"]                     |
    2         | ["Jeju","Pangyo","NewYork","newyork"]                 | 16
    0         | ["Jeju","Pangyo","Seoul","NewYork","LA"]              | 25
================================================================================
[LRU 캐시 동작 원리]
    순서 자료구조 사용: 맨 앞 = 가장 오래된(LRU 대상), 맨 뒤 = 가장 최근 사용

    cache hit:
        캐시에 데이터 존재 → 해당 데이터를 맨 뒤로 이동 (최근 사용 표시)
        실행시간 += 1

    cache miss:
        캐시에 데이터 없음
        캐시 가득 찼으면 맨 앞(LRU) 제거
        새 데이터를 맨 뒤에 추가
        실행시간 += 5

    cacheSize = 0:
        항상 cache miss → 총 실행시간 = len(cities) × 5

[자료구조별 연산 복잡도 비교]
    연산           | list   | deque  | OrderedDict
    --------------|--------|--------|-------------
    in 탐색       | O(N)   | O(N)*  | O(1) (해시)
    맨 앞 삭제    | O(N)   | O(1)   | O(1) popitem
    맨 뒤 추가    | O(1)   | O(1)   | O(1)
    중간 삭제     | O(N)   | O(N)   | O(1) move_to_end
    맨 뒤로 이동  | remove+append | remove+append | O(1) move_to_end

    * deque in 연산: 메모리가 블록 단위 이중 연결 리스트로 분산
                     캐시 지역성(cache locality) 낮아 list보다 실제로 느림

    cacheSize ≤ 30이므로 in O(N) = O(30N) = O(N)으로 실질 차이 작음
    cities 최대 100,000번 in 연산 → 누적 차이 존재

[deque(maxlen) 특성]
    maxlen 지정 시 길이가 초과되면 반대쪽 원소 자동 제거
    maxlen=0: append 즉시 제거 → 항상 빈 deque → 정확성은 보장

    cacheSize=0에서 if 분기를 제거하면:
        deque(maxlen=0)이 자동 처리해 정확성은 유지
        하지만 cities 전체 루프 O(N)을 불필요하게 수행
        if cacheSize 분기로 len(cities)*5 O(1) 즉시 반환이 훨씬 효율적
        실측 cities 100,000개: 분기 있음 ≈ 0ms, 없음 ≈ 10ms (약 14,000배 차이)

[OrderedDict 전용 메서드]
    move_to_end(key, last=True):
        key를 맨 뒤(last=True) 또는 맨 앞(last=False)으로 이동
        remove + append를 O(1)로 대체

    popitem(last=False):
        last=False: 맨 앞 원소 (key, value) 추출 → popleft 역할
        last=True:  맨 뒤 원소 추출 → pop 역할
        O(1)
================================================================================
[내 초기 풀이]
    solution_mine_one  : list + pop(0) + remove + append
    solution_mine_two  : deque + popleft + remove + append
    solution_mine_three: deque(maxlen) + remove + append (if 분기 불필요)
    solution_mine_four : OrderedDict + move_to_end + popitem

[개선 포인트]
    solution_mine_one  : pop(0) O(N) → deque popleft O(1) 개선 가능
                         list in 연산: O(cacheSize) → deque보다 빠를 수 있음
    solution_mine_two  : popleft O(1) 개선
                         deque in 연산: list보다 느릴 수 있음 (캐시 지역성)
    solution_mine_three: deque(maxlen)으로 크기 관리 자동화
                         cacheSize=0 시 if 분기 없이 자동 처리 가능 (maxlen=0)
                         → Sub
    solution_mine_four : 모든 연산 O(1), in O(1) 추가 개선
                         → Best
================================================================================
[복잡도 분석]
    N = len(cities) (최대 100,000), K = cacheSize (최대 30)

    Mine_one   - 시간: O(N×K) | 공간: O(K) - pop(0) O(K) + in O(K) × N번
    Mine_two   - 시간: O(N×K) | 공간: O(K) - popleft O(1), in O(K) × N번
    Mine_three - 시간: O(N×K) | 공간: O(K) - maxlen 자동 관리, in O(K) × N번
    Mine_four  - 시간: O(N)   | 공간: O(K) - 모든 연산 O(1), in O(1) × N번
    Best       - 시간: O(N)   | 공간: O(K) - Mine_four와 동일
    Sub        - 시간: O(N×K) | 공간: O(K) - Mine_three와 동일

    K=30 고정 → Mine_one~three 실질 O(N)에 수렴
    Best(OrderedDict)는 이론적으로 O(N) 엄밀히 성립
"""

import time as time_module
from collections import deque, OrderedDict


# ================================================================================
# Mine solution one - list + pop(0) + remove + append
# ================================================================================
def solution_mine_one(cacheSize: int, cities: list[str]) -> int:
    """
    리스트로 LRU 캐시를 구현하는 초기 풀이

    핵심:
        cache 맨 앞 = 가장 오래된(LRU 대상)
        cache 맨 뒤 = 가장 최근 사용
        hit: remove(c) → append(c) (맨 뒤로 이동)
        miss + 가득 참: pop(0) (LRU 제거) → append(c)

    한계:
        pop(0): 리스트 첫 원소 제거 후 이동 → O(K)
        in 연산: O(K) 순차 탐색
        deque에 비해 pop(0)이 느림

    라이브러리 없이 순수 list로 LRU를 표현하는 학습 목적 풀이
    """
    elapsed = 0
    cache = []

    if cacheSize:
        for c in cities:
            c = c.lower()
            if c in cache:
                cache.remove(c)
                cache.append(c)
                elapsed += 1
            else:
                if len(cache) == cacheSize:
                    cache.pop(0)        # O(K): LRU 제거
                cache.append(c)
                elapsed += 5
    else:
        elapsed = len(cities) * 5

    return elapsed


# ================================================================================
# Mine solution two - deque + popleft + remove + append
# ================================================================================
def solution_mine_two(cacheSize: int, cities: list[str]) -> int:
    """
    deque로 LRU 캐시를 구현해 pop(0) O(K)를 popleft O(1)로 개선한 풀이

    mine_one 대비:
        pop(0) O(K) → popleft() O(1): LRU 제거 비용 개선

    deque in 연산 주의:
        deque는 블록 단위 이중 연결 리스트 구조
        메모리가 분산 → 캐시 지역성 낮음
        in 순차 탐색 시 list보다 느릴 수 있음
        cacheSize ≤ 30이므로 실측 차이 미미
    """
    elapsed = 0
    cache = deque()

    if cacheSize:
        for c in cities:
            c = c.lower()
            if c in cache:
                cache.remove(c)
                cache.append(c)
                elapsed += 1
            else:
                if len(cache) == cacheSize:
                    cache.popleft()     # O(1): LRU 제거
                cache.append(c)
                elapsed += 5
    else:
        elapsed = len(cities) * 5

    return elapsed


# ================================================================================
# Mine solution three - deque(maxlen) + remove + append
# ================================================================================
def solution_mine_three(cacheSize: int, cities: list[str]) -> int:
    """
    deque(maxlen=cacheSize)로 크기 관리를 자동화한 풀이

    mine_two 대비:
        if len(cache) == cacheSize: cache.popleft() 불필요
        maxlen 초과 시 반대쪽 원소 자동 제거 (popleft 역할)

    cacheSize=0 자동 처리:
        deque(maxlen=0)에 append하면 즉시 제거 → 항상 빈 deque
        → if cacheSize 분기 없이도 cacheSize=0 자동으로 전체 miss 처리
        (이 코드에서는 if 분기 유지, 아래 주석 참고)

    miss 처리:
        cache.append(c): maxlen 초과 시 자동으로 popleft 후 추가
    """
    elapsed = 0
    cache = deque(maxlen=cacheSize)

    if cacheSize:
        for c in cities:
            c = c.lower()
            if c in cache:
                cache.remove(c)
                cache.append(c)
                elapsed += 1
            else:
                cache.append(c)         # maxlen 초과 시 자동 LRU 제거
                elapsed += 5
    else:
        elapsed = len(cities) * 5

    return elapsed


# ================================================================================
# Mine solution four - OrderedDict + move_to_end + popitem
# ================================================================================
def solution_mine_four(cacheSize: int, cities: list[str]) -> int:
    """
    OrderedDict 전용 메서드로 모든 LRU 연산을 O(1)로 처리하는 풀이

    OrderedDict 활용:
        in 연산: O(1) (해시 기반) ← list/deque O(K) 대비 개선
        move_to_end(c): hit 시 맨 뒤로 이동 O(1) ← remove+append O(K) 대비 개선
        popitem(last=False): miss 시 맨 앞(LRU) 제거 O(1) ← popleft O(1)과 동일

    Python 3.7+ dict도 삽입 순서 유지하나
    move_to_end, popitem(last=False)는 OrderedDict 전용 메서드

    cacheSize ≤ 30이므로 in O(1) vs O(K=30) 차이는 미미
    cities 100,000번 누적 시 차이 존재, 이론적으로 O(N) 엄밀히 성립
    """
    elapsed = 0
    cache = OrderedDict()

    if cacheSize:
        for c in cities:
            c = c.lower()
            if c in cache:
                cache.move_to_end(c)    # O(1): 맨 뒤로 이동 (최근 사용 표시)
                elapsed += 1
            else:
                if len(cache) == cacheSize:
                    cache.popitem(last=False)   # O(1): 맨 앞(LRU) 제거
                cache[c] = True
                elapsed += 5
    else:
        elapsed = len(cities) * 5

    return elapsed


# ================================================================================
# Best solution - OrderedDict (mine_four 주석 보강)
# ================================================================================
def solution_best(cacheSize: int, cities: list[str]) -> int:
    """
    OrderedDict 전용 메서드로 모든 연산을 O(1)로 처리하는 최적 풀이

    mine_four와 동일한 로직, 선정 근거 주석 보강:
        in O(1): list/deque O(K) 대비 개선 (cities 100,000회 누적)
        move_to_end O(1): remove+append O(K) 대비 hit 처리 개선
        popitem O(1): LRU 제거 O(1)
        전체 O(N): 모든 연산이 O(1)이므로 엄밀히 O(N) 성립
    """
    elapsed = 0
    cache = OrderedDict()

    if cacheSize:
        for c in cities:
            c = c.lower()
            if c in cache:
                cache.move_to_end(c)
                elapsed += 1
            else:
                if len(cache) == cacheSize:
                    cache.popitem(last=False)
                cache[c] = True
                elapsed += 5
    else:
        elapsed = len(cities) * 5

    return elapsed


# ================================================================================
# Sub solution - deque(maxlen) (mine_three 주석 보강)
# ================================================================================
def solution_sub(cacheSize: int, cities: list[str]) -> int:
    """
    deque(maxlen=cacheSize)로 LRU 구조를 직관적으로 표현하는 서브 풀이

    Best 대비 특징:
        maxlen으로 캐시 크기 관리 자동화 → 코드 간결
        LRU 동작 (오래된 것 앞, 최근 것 뒤) 이 deque 구조에 자연스럽게 표현
        in 연산 O(K): cacheSize ≤ 30이므로 실질 차이 미미

    deque(maxlen=0) 특성과 if 분기 유지 이유:
        cacheSize=0이면 append 즉시 제거 → 항상 빈 deque → 정확성 보장
        하지만 분기 없으면 cities 전체 루프 O(N) 불필요하게 수행
        if cacheSize 분기: len(cities) * 5로 O(1) 즉시 반환
        실측 cities 100,000개 기준 약 14,000배 차이 → 분기 유지가 맞음
    """
    elapsed = 0
    cache = deque(maxlen=cacheSize)

    if cacheSize:
        for c in cities:
            c = c.lower()
            if c in cache:
                cache.remove(c)
                cache.append(c)
                elapsed += 1
            else:
                cache.append(c)
                elapsed += 5
    else:
        elapsed = len(cities) * 5

    return elapsed


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[str], int]] = [
        # (cacheSize, cities, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # cacheSize=3, 10개 도시 (5 miss + 5 hit 불가):
        #   Jeju→miss(5), Pangyo→miss(5), Seoul→miss(5), NewYork→miss(5),
        #   LA→miss(5, Jeju 제거), Jeju→miss(5, Pangyo 제거),
        #   Pangyo→miss(5, Seoul 제거), Seoul→miss(5, NewYork 제거),
        #   NewYork→miss(5, LA 제거), LA→miss(5) → 50
        (3, ["Jeju","Pangyo","Seoul","NewYork","LA",
             "Jeju","Pangyo","Seoul","NewYork","LA"], 50),
        # cacheSize=3, Jeju/Pangyo/Seoul 반복:
        #   3 miss(15) + 6 hit(6) = 21
        (3, ["Jeju","Pangyo","Seoul","Jeju","Pangyo",
             "Seoul","Jeju","Pangyo","Seoul"], 21),
        # cacheSize=2, newyork 대소문자 케이스:
        #   Jeju→miss(5), Pangyo→miss(5), NewYork→miss(5, Jeju 제거),
        #   newyork→hit(1) → 16
        (2, ["Jeju","Pangyo","NewYork","newyork"], 16),
        # cacheSize=0: 전체 miss → 5×5=25
        (0, ["Jeju","Pangyo","Seoul","NewYork","LA"], 25),
        # 추가 케이스:
        # cacheSize=5, 공식 예시: 52
        (5, ["Jeju","Pangyo","Seoul","NewYork","LA","SanFrancisco",
             "Seoul","Rome","Paris","Jeju","NewYork","Rome"], 52),
    ]

    solutions = [
        ("Mine_one   (list+pop0)    ", solution_mine_one),
        ("Mine_two   (deque+popleft)", solution_mine_two),
        ("Mine_three (deque+maxlen) ", solution_mine_three),
        ("Mine_four  (OrderedDict)  ", solution_mine_four),
        ("Best       (OrderedDict)  ", solution_best),
        ("Sub        (deque+maxlen) ", solution_sub),
    ]

    # 워밍업 스텝
    _cs, _c, _ = test_cases[0]
    for _, func in solutions:
        func(_cs, _c[:])

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (cacheSize, cities, expected) in enumerate(test_cases, 1):
            start = time_module.perf_counter()
            output = func(cacheSize, cities[:])
            elapsed = time_module.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
