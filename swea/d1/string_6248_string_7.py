"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6248. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 4. 문자열 7
    유형       : String
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?problemLevel=1&problemLevel=2&problemLevel=3&contestProbId=AWcVDLya4swDFAU4&categoryId=AWcVDLya4swDFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=3&pageSize=10&pageIndex=1
    풀이일자   : 2026-09-28
================================================================================
[문제 요약]
    문자열을 입력받아 짝수 인덱스(0부터)의 문자만 이어 출력

    입력 방식 : 표준 입력 한 줄 (input())
    적용 방식 : input → 매개변수 s, output → 반환값 (solution 함수 형태 유지)

    제약 조건
        - 시간   : Python 기준 1초 (테스트케이스 합산)
        - 메모리 : 힙 + 정적 256MB 이내, 스택 1MB 이내
        - 문자열 길이 상한은 지문에 명시되어 있지 않음
          → 아래 성능 측정은 자체 기준(길이 1,000,000)
================================================================================
[입출력 예시]
    공식 예시
    s                     | return
    ----------------------|-------------
    "H1e2l3l4o5w6o7r8l9d" | "Helloworld"

    자체 검증 케이스 (전부 손 계산)
    s              | return
    ---------------|-------
    "abcde"        | "ace"
    "abcdef"       | "ace"
    "Hello, World" | "Hlo ol"
    "0123456789"   | "02468"
================================================================================
[풀이 전략]
    핵심: 짝수 인덱스 = 0, 2, 4, ... → 시작 0, 간격 2인 등차수열

    mine_one : enumerate + idx % 2 == 0
        모든 인덱스(n개)를 순회하며 짝수 여부를 검사한 뒤 리스트 생성 → join

    sub      : range(0, len(s), 2)
        짝수 인덱스만 직접 생성 → 순회 횟수 n → n/2, 나머지 연산 제거

    best     : s[::2]
        확장 슬라이싱 s[start:stop:step]에서 start=0, stop=len(s), step=2가 기본 적용
        → 인덱스 0, 2, 4, ...를 C 레벨에서 한 번에 추출

    손 추적 (공식 예시) s = "H1e2l3l4o5w6o7r8l9d" (길이 19):
        짝수 인덱스 0, 2, 4, ..., 18 → H, e, l, l, o, w, o, r, l, d
        홀수 인덱스(숫자 1~9)는 모두 제외 → "Helloworld" ✓

    손 추적 s = "abcde":
        mine_one: idx0 a 선택, idx1 b 제외, idx2 c 선택, idx3 d 제외, idx4 e 선택 → "ace"
        sub     : range(0, 5, 2) = 0, 2, 4 → a, c, e → "ace"
        best    : s[::2] → 인덱스 0, 2, 4 → "ace" ✓

    SWEA 제출 형태 (함수 본문 아래에 이어 붙여 제출):
        s = input()
        print(solution_best(s))

    제출 이력:
        mine_one과 동일한 로직으로 SWEA 제출 테스트 통과 (2026-09-28)
================================================================================
[실측 결과 — 문자열 길이 1,000,000, 30회 평균, 워밍업 1회 (Python 3.12.3)]
    mine_one (enumerate)  : 43.4ms
    sub      (range step) : 17.6ms
    best     (slicing)    :  0.28ms  ← 가장 빠름 (mine_one 대비 약 150배 이상)

    best가 빠른 이유:
        Python 레벨 루프 자체가 없음 (C 레벨에서 슬라이싱)
        mine_one은 n번, sub는 n/2번 Python 레벨 반복이 발생
    주의: 측정 환경(3.12.3)과 실제 개발 환경(3.12.11)이 달라 절대값은 다를 수 있음
          차이의 방향과 대략적인 배율이 핵심
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 있음 - 순회 횟수 n, 나머지 연산 포함
    solution_sub      : range 스텝으로 순회 횟수 절반 - Sub
    solution_best     : 슬라이싱 한 번으로 해결 - Best
================================================================================
[복잡도 분석]
    n = len(s)

    Mine_one - 시간: O(n) | 공간: O(n) - n번 검사, 리스트 n/2개 + 결과 문자열
    Sub      - 시간: O(n) | 공간: O(n) - n/2번 순회, 리스트 n/2개 + 결과 문자열
    Best     - 시간: O(n) | 공간: O(n) - C 레벨 복사, 결과 문자열 n/2

    점근 복잡도는 모두 동일하며 차이는 상수항
    (Python 레벨 루프 횟수와 인터프리터 오버헤드)
"""

import time


# ================================================================================
# Mine solution one - enumerate + 짝수 인덱스 조건
# ================================================================================
def solution_mine_one(s: str) -> str:
    """
    enumerate로 (인덱스, 문자)를 순회하며 짝수 인덱스만 선택하는 초기 풀이

    핵심:
        idx % 2 == 0: 짝수 인덱스 판별
        리스트 컴프리헨션으로 문자를 모은 뒤 join

    한계:
        홀수 인덱스도 전부 순회한 뒤 버림 → 순회 n번
    """
    return "".join([char for idx, char in enumerate(s) if idx % 2 == 0])


# ================================================================================
# Best solution - 확장 슬라이싱
# ================================================================================
def solution_best(s: str) -> str:
    """
    확장 슬라이싱 s[::2]로 짝수 인덱스 문자를 한 번에 추출하는 풀이

    핵심:
        s[start:stop:step] 기본값: start=0, stop=len(s)
        step=2 → 인덱스 0, 2, 4, ...
        Python 레벨 루프 없이 C 레벨에서 처리
    """
    return s[::2]


# ================================================================================
# Sub solution - range 스텝 순회
# ================================================================================
def solution_sub(s: str) -> str:
    """
    range(0, len(s), 2)로 짝수 인덱스만 직접 순회하는 풀이

    핵심:
        조건 검사 없이 짝수 인덱스만 생성 → 순회 n/2번
        인덱스 접근 s[i]로 문자를 모은 뒤 join
    """
    return "".join([s[i] for i in range(0, len(s), 2)])


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (s, 기댓값) - 전부 손 계산
        ("H1e2l3l4o5w6o7r8l9d", "Helloworld"),  # 공식 예시
        ("abcde", "ace"),
        ("abcdef", "ace"),
        ("a", "a"),
        ("Hello, World", "Hlo ol"),
        ("0123456789", "02468"),
        ("", ""),                               # 빈 문자열 - 제약 확인 전 경계 케이스
        ("ab" * 500_000, "a" * 500_000),        # 대용량: 짝수 인덱스는 전부 'a'
    ]

    solutions = [
        ("Mine (enumerate)", solution_mine_one),
        ("Best (slicing)",   solution_best),
        ("Sub  (range step)", solution_sub),
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
