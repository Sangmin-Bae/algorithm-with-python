"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 전화번호 목록
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42577
    풀이일자   : 2026-07-13
================================================================================
[문제 요약]
    전화번호 목록에서 어떤 번호가 다른 번호의 접두사인 경우가 있으면 False
    없으면 True 반환

    제약 조건
        - phone_book 길이: 1 이상 1,000,000 이하
        - 번호 길이: 1 이상 20 이하
        - 중복 없음
================================================================================
[입출력 예시]
    phone_book                        | return
    ----------------------------------|-------
    ["119","97674223","1195524421"]   | False
    ["123","456","789"]               | True
    ["12","123","1235","567","88"]    | False
================================================================================
[solution_one — 길이순 정렬 + 이중 순회 (효율성 실패)]
    길이순 정렬: 짧은 번호가 접두사 후보
    phone_book[i]를 접두사 대상으로 phone_book[i+1:]과 비교
    슬라이싱 j[:l] == n으로 접두사 여부 확인

    효율성 실패 원인:
        접두사 없는 경우 전체 이중 순회 → O(N²)
        N=1,000,000에서 1조 연산 → 시간 초과

[solution_two/three — 사전순 정렬 + 인접 비교]
    핵심 성질:
        A가 B의 접두사라면 사전순 정렬에서 A와 B는 반드시 인접
        A로 시작하는 모든 번호는 사전순으로 A 바로 다음에 위치
        A와 B 사이에 A의 접두사가 아닌 번호가 끼어들 수 없음
        → 인접한 두 쌍만 비교해도 전체 확인 가능

    예: ["119", "1195524421", "97674223"]
        정렬: ["119", "1195524421", "97674223"]
        (119, 1195524421): 1195524421.startswith("119") → True → False 반환

    solution_two: i+1 < len으로 인덱스 범위 방어
    solution_three: zip(s[:-1], s[1:])으로 인덱스 범위 오류 원천 차단

    시간복잡도: O(N log N) — 정렬이 지배

[solution_four — 해시(dict) 방식]
    해시 방식에 도달하는 사고법:
        1. "탐색이 반복된다" 신호
           풀이 1~3: "번호 A가 번호 B에 있는가?" 를 N번 반복
           → "탐색을 O(1)로 줄일 수 없을까?"

        2. "존재 여부 확인" 패턴
           "어떤 번호가 존재하는가?" = set/dict in 연산 O(1)
           위치나 순서가 필요 없음 → 해시 자연스러운 선택

        3. 지문 신호: "어떤 번호가 다른 번호의 접두어인 경우가 있으면"
           존재 여부 확인 → set/dict in 연산이 최적

    풀이 방향 전환 (풀이 1~3과 반대):
        풀이 1~3: 접두사 후보 A를 지정 → A가 다른 번호에 있는지 탐색
        풀이 4: 번호 B를 지정 → B의 부분 접두사들이 dict에 있는지 O(1) 조회

    손 추적 ("119"와 "1195524421"):
        대상 n="1195524421" 순회:
            prefix="1" → hash_map에 없음
            prefix="11" → hash_map에 없음
            prefix="119" → hash_map에 있음, "119" != "1195524421" → False 반환

    hash_map value = True:
        dict의 in 연산은 key를 대상으로 함 → value는 아무 값이나 가능
        set으로도 대체 가능: phone_set = set(phone_book)

    시간복잡도: O(N×L) — N개 번호 × L 길이 접두사 순회 (L≤20, 사실상 O(N))

[두 접근 방식 비교]
    사전순 정렬 (solution_three):
        O(N log N): 정렬이 지배
        직관적: 인접 비교로 접두사 관계 확인
        정렬로 공간 구조 변경 → 원본 순서 소실

    해시 (solution_four):
        O(N×L): N=100만, L=20 → 최대 2,000만 연산
        정렬 불필요
        문제 유형(해시)의 출제 의도에 부합

    N=1,000,000, L=20:
        solution_three: O(N log N) (랜덤 데이터 기준, 실측으로 L 영향 거의 없음)
        solution_four:  O(N×L) = O(N) (L≤20 상수)
        실측 N=10,000에서 해시가 4배 빠름 (L이 log N보다 작아 해시 유리)
================================================================================
[내 초기 풀이]
    solution_mine_one  : 길이순 정렬 + 이중 순회 (효율성 실패)
    solution_mine_two  : 사전순 정렬 + i+1 인덱스 인접 비교
    solution_mine_three: 사전순 정렬 + zip 인접 비교
    solution_mine_four : 해시(dict) + 접두사 O(1) 조회

[개선 포인트]
    solution_mine_one  : O(N²) → 효율성 실패, 학습 목적
    solution_mine_two  : 개선 필요 없음
                         i+1 < len 조건으로 안전하게 인접 비교
    solution_mine_three: 개선 필요 없음 - Sub
                         zip으로 인덱스 범위 오류 원천 차단, 코드 간결
    solution_mine_four : 개선 필요 없음 - Best
                         L≤20 상수 → O(N×L) = O(N)
                         정렬 O(N log N) 대비 L < log N 조건에서 해시가 유리
                         실측 N=10,000에서 해시가 정렬보다 4배 빠름
================================================================================
[복잡도 분석]
    N = len(phone_book) (최대 1,000,000), L = 번호 최대 길이 (최대 20)

    Mine_one   - 시간: O(N²×L)   | 공간: O(N) - 이중 순회 + 슬라이싱, 효율성 실패
    Mine_two   - 시간: O(N log N) | 공간: O(N) - 정렬 + 단일 순회
    Mine_three - 시간: O(N log N) | 공간: O(N) - 정렬 + zip 인접 비교
    Mine_four  - 시간: O(N×L)    | 공간: O(N) - dict 생성 + 접두사 순회
    Best       - 시간: O(N×L)    | 공간: O(N) - Mine_four와 동일
    Sub        - 시간: O(N log N) | 공간: O(N) - Mine_three와 동일

    정렬 방식이 O(N log N)인 이유:
        이론상 문자열 비교 O(L) 포함해 O(N log N × L)이나
        랜덤 번호에서 비교가 앞 몇 자리에서 끝남 → 실질 O(N log N)
        실측: L=5~1000까지 변해도 정렬 시간 거의 동일 (0.99~1.15ms)

    두 방식 교차점: L = log N
        L < log N → 해시 O(N×L) < 정렬 O(N log N) → 해시 유리
        L > log N → 해시 O(N×L) > 정렬 O(N log N) → 정렬 유리
        L = N이면 해시 O(N²), 정렬은 여전히 O(N log N)

    N=10,000, L=20 실측:
        Mine_three(정렬+zip): 2.04ms
        Mine_four(해시):      0.49ms  ← 4배 빠름 (L≤20 작은 값이므로 해시 유리)
"""

import time


# ================================================================================
# Mine solution one - 길이순 정렬 + 이중 순회 (효율성 실패)
# ================================================================================
def solution_mine_one(phone_book: list[str]) -> bool:
    """
    길이순 정렬 후 이중 순회로 접두사를 확인하는 초기 풀이 (효율성 실패)

    길이순 정렬 이유:
        접두사는 대상 번호보다 길이가 작거나 같음
        → 짧은 번호가 앞에 오면 phone_book[i+1:]만 탐색하면 됨

    효율성 실패 원인:
        접두사 없는 최악의 경우: N×(N-1)/2번 비교 → O(N²×L)
        N=1,000,000에서 약 20조 연산 → 시간 초과
    """
    s_phone_book = sorted(phone_book, key=lambda x: len(x))

    for i in range(len(s_phone_book)):
        n = s_phone_book[i]
        l = len(n)

        for j in s_phone_book[i + 1:]:
            if n == j[:l]:
                return False

    return True


# ================================================================================
# Mine solution two - 사전순 정렬 + i+1 인덱스 인접 비교
# ================================================================================
def solution_mine_two(phone_book: list[str]) -> bool:
    """
    사전순 정렬 후 인접한 두 번호만 비교하는 풀이

    핵심 성질:
        A가 B의 접두사라면 사전순 정렬에서 A와 B는 반드시 인접
        → 인접 쌍만 비교해도 전체 접두사 관계 확인 가능

    i+1 < len(s_phone_book):
        마지막 원소에서 i+1 인덱스 범위 초과 방지

    startswith(phone_book[i]):
        슬라이싱 j[:l] == n 대신 내장 메서드 사용 → 더 직관적
    """
    s_phone_book = sorted(phone_book)

    for i in range(len(s_phone_book)):
        if i + 1 < len(s_phone_book) and s_phone_book[i + 1].startswith(s_phone_book[i]):
            return False

    return True


# ================================================================================
# Mine solution three - 사전순 정렬 + zip 인접 비교
# ================================================================================
def solution_mine_three(phone_book: list[str]) -> bool:
    """
    zip으로 인접 쌍을 생성해 인덱스 범위 오류 없이 비교하는 풀이

    mine_two 대비:
        i+1 < len 조건 제거 → zip이 자동으로 짧은 쪽 기준 처리
        (cur_n, nxt_n) 언패킹으로 코드 더 읽기 쉬움
        s_phone_book[1:]: 슬라이싱으로 한 칸 밀린 리스트 생성

    zip(s[:-1], s[1:]) vs zip(s, s[1:]):
        둘 다 동일한 결과 (zip이 짧은 쪽 기준으로 처리하므로)
        후자가 더 간결
    """
    s_phone_book = sorted(phone_book)

    for cur_n, nxt_n in zip(s_phone_book, s_phone_book[1:]):
        if nxt_n.startswith(cur_n):
            return False

    return True


# ================================================================================
# Mine solution four - 해시(dict) + 접두사 O(1) 조회
# ================================================================================
def solution_mine_four(phone_book: list[str]) -> bool:
    """
    dict에 모든 번호를 등록하고 각 번호의 접두사를 O(1)로 조회하는 풀이

    해시 방식 사고법:
        1. "탐색이 N번 반복" → "O(1) 탐색으로 줄이자" → dict
        2. "존재 여부 확인" → set/dict in 연산 O(1) 최적
        3. 지문: "어떤 번호가 접두어인 경우가 있으면" → 존재 확인

    방향 전환 (풀이 1~3과 반대):
        풀이 1~3: 접두사 후보 A 지정 → B에서 A를 탐색 (O(N) 반복)
        풀이 4:   번호 B 지정 → B의 부분 접두사가 dict에 있는지 O(1) 조회

    prefix != n 조건:
        B 자신과 동일한 접두사는 제외 (자기 자신을 접두사로 판단하면 안 됨)

    hash_map value = True:
        dict in 연산은 key 대상 → value는 임의 값 가능
        set(phone_book)으로도 동일하게 구현 가능
    """
    hash_map = {n: True for n in phone_book}

    for n in phone_book:
        prefix = ""
        for char in n:
            prefix += char
            if prefix in hash_map and prefix != n:
                return False

    return True


# ================================================================================
# Best solution - 사전순 정렬 + zip 인접 비교 (mine_three 주석 보강)
# ================================================================================
def solution_best(phone_book: list[str]) -> bool:
    """
    hash_map으로 접두사를 O(1) 조회해 O(N×L) = O(N)에 처리하는 최적 풀이

    mine_four와 동일한 로직, 선정 근거 주석 보강:
        L≤20 상수 → O(N×L) = O(N) 실질
        정렬 방식 O(N log N) 대비 L < log N인 이 문제 조건에서 유리
        실측 N=10,000에서 정렬+zip보다 4배 빠름
        문제 유형(해시)의 출제 의도와 일치
    """
    hash_map = {n: True for n in phone_book}

    for n in phone_book:
        prefix = ""
        for char in n:
            prefix += char
            if prefix in hash_map and prefix != n:
                return False

    return True


# ================================================================================
# Sub solution - 해시(dict) (mine_four 주석 보강)
# ================================================================================
def solution_sub(phone_book: list[str]) -> bool:
    """
    사전순 정렬과 zip 인접 비교로 접두사를 확인하는 서브 풀이

    Best 대비 특징:
        정렬로 접두사 관계인 번호를 인접하게 배치 → 인접 쌍만 비교
        zip: 인덱스 범위 오류 없이 인접 쌍 자동 생성
        O(N log N): 정렬이 지배 (랜덤 데이터 기준, L 영향 거의 없음)
        직관적 구조: 정렬 후 인접 비교로 동작 원리 명확
    """
    s_phone_book = sorted(phone_book)

    for cur_n, nxt_n in zip(s_phone_book, s_phone_book[1:]):
        if nxt_n.startswith(cur_n):
            return False

    return True


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[str], bool]] = [
        # (phone_book, 기댓값)
        # 프로그래머스 공식 예시:
        # "119"가 "1195524421"의 접두사 → False
        (["119", "97674223", "1195524421"], False),
        # 접두사 없음 → True
        (["123", "456", "789"], True),
        # "12"가 "123"의 접두사 → False
        (["12", "123", "1235", "567", "88"], False),
        # 추가 케이스:
        # 단일 번호 → True
        (["119"], True),
        # 동일 길이 번호들, 접두사 없음 → True
        (["100", "200", "300"], True),
    ]

    solutions = [
        ("Mine_one   (길이정렬+이중)", solution_mine_one),
        ("Mine_two   (사전정렬+i+1) ", solution_mine_two),
        ("Mine_three (사전정렬+zip) ", solution_mine_three),
        ("Mine_four  (해시)         ", solution_mine_four),
        ("Best       (해시)         ", solution_best),
        ("Sub        (사전정렬+zip) ", solution_sub),
    ]

    # 워밍업 스텝
    _pb, _ = test_cases[0]
    for _, func in solutions:
        func(_pb[:])

    print("=" * 68)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (phone_book, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(phone_book[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
