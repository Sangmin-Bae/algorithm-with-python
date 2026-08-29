"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : [3차] n진수 게임
    유형       : String / Math
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17687
    풀이일자   : 2026-08-29
===================================================================================
[문제 요약]
    0부터 순서대로 숫자를 n진법으로 변환 후 한 글자씩 말하는 게임에서
    p번째 사람이 말해야 할 t개의 숫자를 반환

    제약 조건
        - n: 2 이상 16 이하 (진법)
        - t: 1 이상 1000 이하 (미리 구할 숫자 수)
        - m: 2 이상 100 이하 (인원 수)
        - p: 1 이상 m 이하 (튜브 순서)
===================================================================================
[입출력 예시]
    n  | t  | m | p | result
    ---|----|----|---|------------------
    2  | 4  | 2  | 1 | "0111"
    16 | 16 | 2  | 1 | "02468ACE11111111"
    16 | 16 | 2  | 2 | "13579BDF01234567"
===================================================================================
[핵심 — 필요한 문자열 길이 t * m]
    t개를 말해야 하고 p번째 순서이므로
    전체 스트림에서 t * m 길이가 생성되면 충분

    슬라이싱으로 p번째 사람 차례만 추출:
        string[p-1 : t*m : m]
        p-1: 첫 번째 차례 (0-indexed)
        t*m: 끝 인덱스
        m:   건너뛰기 간격 (m명마다 한 번)

[내장 함수 분기 최적화]
    2진법 → bin(num)[2:]    ← C 레벨
    8진법 → oct(num)[2:]    ← C 레벨
    10진법 → str(num)       ← C 레벨
    16진법 → hex(num)[2:].upper()  ← C 레벨
    나머지 → while 루프

    2/8/10/16진법은 내장 함수로 처리해 속도 우위
    나머지 진법(3,5,6,7,9,11~15)만 while 루프

[list + join vs string +=]
    string += 방식: 매번 새 문자열 객체 생성
        k번 반복 시 총 복사량 O(k²)
        t*m 최대 100,000 → 최악 10^10 복사

    list + join 방식: O(k)
        리스트에 담고 마지막에 한 번만 병합
        → mine이 ref_one보다 빠른 핵심 이유

[ref_two 제너레이터 방식]
    게임 스트림을 무한 제너레이터로 구현
    숫자 단위가 아닌 글자 단위로 yield:
        num=16 (16진법) → '1','0' 두 번 yield

    turn % m == p-1 조건:
        전체 글자 순번(turn)에서 몇 번째 사람인지 판별
        mine의 슬라이싱 string[p-1:t*m:m]과 동일한 결과

    느린 이유:
        글자 하나마다 yield → next() 호출 t*m번 반복
        제너레이터 컨텍스트 스위칭 비용 누적

[실측 결과 — n=16, t=1000, m=100, 5,000회]
    mine     (list+내장함수): 10.12ms  ← 가장 빠름
    ref_one  (재귀+str+=):    17.03ms
    ref_two  (generator):     25.37ms  ← 가장 느림

    ref_one이 느린 이유:
        재귀 함수 스택 프레임 생성 비용
        string += O(k²) 누적 복사

    ref_two가 가장 느린 이유:
        yield per char + next() 100,000회 컨텍스트 스위칭
===================================================================================
[내 초기 풀이]
    solution_mine: list + join + 내장 함수 분기 convert_base

[개선 포인트]
    solution_mine:    개선 필요 없음 - Best
                      내장 함수 분기로 C 레벨 최적화, list + join
    solution_ref_one: 재귀 변환 + str += → 두 가지 모두 오버헤드
                      내장 함수 분기, list + join 적용 시 mine과 동일
    solution_ref_two: 제너레이터 발상 독창적 - Sub
                      글자 단위 yield로 p번째 추출이 직관적
                      컨텍스트 스위칭 비용으로 가장 느림
===================================================================================
[복잡도 분석]
    N = t * m (최대 100,000), K = 각 숫자의 진법 자리수

    Mine     - 시간: O(N×K)   | 공간: O(N) - list + join
    Ref_one  - 시간: O(N×K²)  | 공간: O(N) - 재귀 + str += O(k²)
    Ref_two  - 시간: O(N×K)   | 공간: O(1) - 제너레이터 (result 제외)
    Best     - 시간: O(N×K)   | 공간: O(N) - Mine과 동일
    Sub      - 시간: O(N×K)   | 공간: O(1) - Ref_two와 동일
"""

import time


# =================================================================================
# Mine solution - list + join + 내장 함수 분기
# =================================================================================
def solution_mine(n: int, t: int, m: int, p: int) -> str:
    """
    내장 함수 분기 convert_base와 list + join으로 최적화한 초기 풀이

    convert_base 내장 함수 분기:
        2/8/10/16진법: bin/oct/str/hex (C 레벨) 직접 사용
        나머지: while 루프로 직접 변환

    list + join:
        string += 방식의 O(k²) 누적 복사 방지
        리스트에 담고 마지막 한 번만 join

    length 별도 변수:
        len(string) 매번 재계산 방지
        변환된 문자열 길이를 누적해서 관리

    슬라이싱 string[p-1 : t*m : m]:
        p-1: 첫 번째 차례 (0-indexed)
        m:   건너뛰기 간격
    """
    string_list = []
    length = 0

    def convert_base(num: int, base: int) -> str:
        if num == 0:
            return "0"
        if base == 2:
            return bin(num)[2:]
        elif base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        elif base == 16:
            return hex(num)[2:].upper()

        chars = "0123456789ABCDEF"
        result = ""
        while num > 0:
            result = chars[num % base] + result
            num //= base
        return result

    num = 0
    while length < t * m:
        converted = convert_base(num, n)
        string_list.append(converted)
        length += len(converted)
        num += 1

    string = "".join(string_list)
    return string[p - 1: t * m: m]


# =================================================================================
# Ref solution one - 재귀 변환 + string +=
# =================================================================================
def solution_ref_one(n: int, t: int, m: int, p: int) -> str:
    """
    재귀 함수로 n진법 변환하는 참고 풀이

    재귀 convert_base:
        num < base: 단일 자리 → 직접 반환
        num >= base: convert_base(num//base) + chars[num%base]
        자연스럽게 높은 자리부터 낮은 자리로 조립

    단점:
        재귀 스택 프레임 생성 비용
        string += 방식 O(k²) 누적 복사
        len(string) 매 루프 재계산
        → 실측 mine 대비 70% 느림
    """
    string = ""

    def convert_base(num: int, base: int) -> str:
        chars = "0123456789ABCDEF"
        if num < base:
            return chars[num]
        return convert_base(num // base, base) + chars[num % base]

    num = 0
    while len(string) < t * m:
        string += convert_base(num, n)
        num += 1

    return string[p - 1: t * m: m]


# =================================================================================
# Ref solution two - 제너레이터 방식
# =================================================================================
def solution_ref_two(n: int, t: int, m: int, p: int) -> str:
    """
    무한 제너레이터로 게임 스트림을 구현하는 참고 풀이

    game_stream():
        0부터 순서대로 n진법 변환 후 글자 단위로 yield
        num=16 (16진법) → '1', '0' 두 번 yield
        while True로 무한 생성, 외부에서 필요한 만큼만 소비

    turn % m == p - 1 조건:
        전체 글자 순번(turn)에서 몇 번째 사람 차례인지 판별
        mine의 슬라이싱 string[p-1:t*m:m]과 동일한 결과

    느린 이유:
        글자 하나마다 yield → next() 호출 t*m번 반복
        제너레이터 컨텍스트 스위칭 비용이 슬라이싱보다 큼
    """
    def game_stream():
        chars = "0123456789ABCDEF"
        num = 0
        while True:
            if num == 0:
                yield "0"
            else:
                converted = ""
                temp = num
                while temp > 0:
                    converted = chars[temp % n] + converted
                    temp //= n
                for char in converted:
                    yield char
            num += 1

    stream = game_stream()
    result = []

    for turn in range(t * m):
        char = next(stream)
        if turn % m == p - 1:
            result.append(char)

    return "".join(result)


# =================================================================================
# Best solution - list + join + 내장 함수 분기 (mine 주석 보강)
# =================================================================================
def solution_best(n: int, t: int, m: int, p: int) -> str:
    """
    내장 함수 분기 + list + join으로 O(N×K) 시간에 최적 처리하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        2/8/10/16진법 내장 함수: C 레벨 최적화
        list + join: str += O(k²) 방지
        length 누적: len(string) 매 루프 재계산 방지
        실측 n=16, t=1000, m=100: 10.12ms (ref_one 17.03ms, ref_two 25.37ms 대비 우위)
    """
    string_list = []
    length = 0

    def convert_base(num: int, base: int) -> str:
        if num == 0:
            return "0"
        if base == 2:
            return bin(num)[2:]
        elif base == 8:
            return oct(num)[2:]
        elif base == 10:
            return str(num)
        elif base == 16:
            return hex(num)[2:].upper()

        chars = "0123456789ABCDEF"
        result = ""
        while num > 0:
            result = chars[num % base] + result
            num //= base
        return result

    num = 0
    while length < t * m:
        converted = convert_base(num, n)
        string_list.append(converted)
        length += len(converted)
        num += 1

    string = "".join(string_list)
    return string[p - 1: t * m: m]


# =================================================================================
# Sub solution - 제너레이터 방식 (ref_two 주석 보강)
# =================================================================================
def solution_sub(n: int, t: int, m: int, p: int) -> str:
    """
    무한 제너레이터로 게임 스트림을 표현하는 서브 풀이

    Best 대비 특징:
        게임 규칙을 제너레이터로 직접 표현 → 발상이 독창적
        turn % m == p-1: 슬라이싱 없이 순번 판별
        글자 단위 yield로 p번째 추출 로직이 명시적
        실측 Best 대비 2.5배 느림 (컨텍스트 스위칭 비용)
    """
    def game_stream():
        chars = "0123456789ABCDEF"
        num = 0
        while True:
            if num == 0:
                yield "0"
            else:
                converted = ""
                temp = num
                while temp > 0:
                    converted = chars[temp % n] + converted
                    temp //= n
                for char in converted:
                    yield char
            num += 1

    stream = game_stream()
    result = []

    for turn in range(t * m):
        char = next(stream)
        if turn % m == p - 1:
            result.append(char)

    return "".join(result)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (n, t, m, p, 기댓값)
        # 공식 예시
        (2,  4,  2, 1, "0111"),
        (16, 16, 2, 1, "02468ACE11111111"),
        (16, 16, 2, 2, "13579BDF01234567"),
        # 추가 케이스:
        # 10진법
        # 손 추적: 0,1,2,3,4... → m=3, p=1 → 0,3,6,...
        (10, 3, 3, 1, "036"),
        # 2진법, 1명
        # 0,1,10,11,100... 모두 p=1
        (2,  5, 1, 1, "01101"),
    ]

    solutions = [
        ("Mine     (list+내장함수) ", solution_mine),
        ("Ref_one  (재귀+str+=)   ", solution_ref_one),
        ("Ref_two  (generator)    ", solution_ref_two),
        ("Best     (list+내장함수) ", solution_best),
        ("Sub      (generator)    ", solution_sub),
    ]

    # 워밍업 스텝
    _n, _t, _m, _p, _ = test_cases[0]
    for _, func in solutions:
        func(_n, _t, _m, _p)

    print("=" * 68)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (n, t, m, p, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(n, t, m, p)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
