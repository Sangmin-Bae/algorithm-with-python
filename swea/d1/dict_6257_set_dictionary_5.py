"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6257. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 3. 자료구조 - 셋, 딕셔너리 5
    유형       : Dict (딕셔너리 컴프리헨션), String (strip)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcVmIXq464DFAU4&categoryId=AWcVmIXq464DFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=2
    풀이일자   : 2026-10-13
================================================================================
[문제 요약]
    문자열 리스트에서 각 원소의 앞뒤 공백을 제거한 문자열을 키, 그 길이를 값으로 하는
    딕셔너리를 딕셔너리 내포로 생성해 출력

    입력 방식 : 입력 없음 (리스트가 지문에 고정)
    적용 방식 : 고정된 리스트 → 매개변수 fruit, output → 반환값 (딕셔너리)
    지문 조건 : 딕셔너리 내포 사용, 원소의 공백 제거
================================================================================
[입출력 예시]
    공식 예시
    fruit                                   | return
    ----------------------------------------|----------------------------------------
    ['   apple    ', 'banana', '  melon']    | {'apple': 5, 'banana': 6, 'melon': 5}

    자체 검증 케이스 (전부 손 계산)
    fruit                    | return
    -------------------------|-----------------------------
    []                       | {}
    ['a']                    | {'a': 1}
    [' a ', 'a']             | {'a': 1}            (공백 제거 후 중복 키)
    ['\\tab\\n']               | {'ab': 2}           (탭과 개행도 제거)
    ['a b ']                 | {'a b': 3}          (내부 공백은 유지)
    ['', '   ']              | {'': 0}             (빈 문자열 키)
    ['  hi', 'hi  ', ' yo '] | {'hi': 2, 'yo': 2}
================================================================================
[풀이 전략]
    핵심: 공백 제거 → 키, 길이 → 값
        str.strip() : 앞뒤 공백(스페이스, 탭, 개행 등)만 제거, 내부 공백은 유지
        결과 키가 같아지면 한 키로 합쳐짐 (값은 같은 길이라 동일)
        딕셔너리는 Python 3.7+에서 삽입 순서 유지 → 첫 등장 순서대로 출력

    지문 조건 vs mine_one:
        지문은 딕셔너리 내포 사용을 요구하나 mine_one은 for 반복문
        SWEA는 출력 문자열만 비교하므로 통과했으나 지문 조건은 충족하지 않음
        → best에서 지문 조건을 충족하는 형태로 정리

    내포에서 strip 결과를 키와 값에 함께 쓰는 방법:
        1) strip 두 번 호출 : {f.strip(): len(f.strip()) for f in fruit}
           단순하나 호출이 두 배
        2) map(str.strip, fruit)을 순회 대상으로 : {s: len(s) for s in map(str.strip, fruit)}
           strip을 한 번만 호출, 키와 값에서 같은 변수 s 사용 (best)
        3) 월러스 연산자 : {(s := f.strip()): len(s) for f in fruit}  (sub)
           Python 3.8+ 필요 → SWEA(3.7.9)에서는 문법 오류로 제출 불가

    월러스 연산자와 평가 순서 주의:
        3번은 키가 값보다 먼저 평가되어야 s가 정의된 상태로 len(s)가 실행됨
        공식 문서: 3.8 이전 딕셔너리 내포는 값을 키보다 먼저 평가 (CPython 기준)
                   3.8부터 키를 먼저 평가
        → 월러스 사용 시 3.8+가 이중으로 필요 (문법 + 평가 순서)

    풀이 구성:
        mine_one : for 반복문 + strip + 삽입 (직접 작성한 풀이, 지문 조건 미충족)
        best     : 딕셔너리 내포 + map(str.strip, fruit) (Python 3.7 호환)
        sub      : 딕셔너리 내포 + 월러스 연산자 (Python 3.8+ 전용, 로컬 비교용)

    손 추적 (공식 예시) fruit = ['   apple    ', 'banana', '  melon']:
        map(str.strip) : '   apple    ' → 'apple', 'banana' → 'banana', '  melon' → 'melon'
        s = 'apple'  → 'apple': 5
        s = 'banana' → 'banana': 6
        s = 'melon'  → 'melon': 5
        → {'apple': 5, 'banana': 6, 'melon': 5} ✓

    SWEA 제출 형태 (함수 본문 아래에 이어 붙여 제출, 제출 시 함수 정의의 타입 힌트는 제거):
        fruit = ['   apple    ', 'banana', '  melon']
        print(solution_best(fruit))
    주의: dict[str, int] 같은 내장 제네릭 타입 힌트는 3.9+ 문법으로
          3.7.9에서는 정의 시점에 오류가 날 수 있음 (3.7 인터프리터가 없어 직접 검증은 못함)

    제출 이력:
        solution_mine_one과 동일한 로직으로 SWEA 제출 테스트 통과 (2026-10-13)
        solution_sub(월러스)는 SWEA에서 지원되지 않음을 확인 (사용자 확인, 3.7.9)
        solution_best는 로컬 검증만 진행 (사이트 제출 전)
================================================================================
[실측 결과 — 공백 제거 딕셔너리 생성 방식 비교]
    측정: 호출당 중앙값, Python 3.12.3 샌드박스 (python3.12 고정, 입력 크기는 자체 기준)
          공식 예시는 40라운드 x 100,000회, 1,000개는 30라운드 x 1,000회
          1,000,000개는 9라운드 x 2회 (다른 측정 실행)
          1,000개와 1,000,000개는 앞뒤에 0~4개 공백이 붙은 임의 단어 (a~j 문자, 3~9자)
          표의 값은 mine_one 대비 비율

    방식                           공식(3개)   1,000개   1,000,000개
    mine  for + strip + 삽입       1.00       1.00      1.00
    best  내포 + map(str.strip)    1.29       1.07      1.01
    내포 + 리스트로 먼저 strip       1.26       1.06      1.10
    내포 + strip 두 번              1.19       1.42      1.12
    sub   내포 + 월러스 (3.8+)      1.01       0.98      -

    mine의 절대값: 0.359µs (3개) / 105.2µs (1,000개) / 442ms (1,000,000개)
    그 외 방식(별도 실행, 1,000,000개 기준 mine 대비): 내부 제너레이터 1.11, zip + map(len) 1.11,
        dict(제너레이터) 1.18

    해석:
        같은 로직(mine)을 두 번 측정했을 때 차이 약 7.1%, 표준편차는 평균의 약 7~25%
        → 약 10% 이하의 차이는 노이즈로 취급
        공식 예시(3개)에서 내포 변형은 mine보다 1.19~1.29배 느림 (두 번의 실행에서 같은 방향)
            절대값으로는 약 0.1µs 차이
        1,000개 이상에서는 best와 mine이 노이즈 범위 안 (1.01~1.07)
        strip 두 번은 1,000개에서 1.42배로 가장 느림 (strip 호출이 두 배)
        월러스 변형은 mine과 동률 (1.01 / 0.98)
        → 딕셔너리 내포가 for 반복문보다 빠르지는 않음

    Best 선정 근거:
        - 지문 조건(딕셔너리 내포)을 충족하는 형태 중 대규모 입력에서 mine과 동률
        - strip을 한 번만 호출하고 Python 3.7에서 동작
        - 일반성 대가: 입력이 몇 개뿐인 공식 예시에서는 mine보다 약 1.3배 느림 (절대 약 0.1µs)
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 있음 - 지문의 딕셔너리 내포 조건을 충족하지 않음 (성능은 최상위)
    solution_best     : 지문 조건 충족 + strip 1회 + 3.7 호환 - Best
    solution_sub      : 월러스로 내포 한 줄 - Sub (Python 3.8+ 전용)
================================================================================
[복잡도 분석]
    n = len(fruit), L = 원소 문자열의 평균 길이

    Mine_one - 시간: O(n * L) | 공간: O(k * L) - strip이 원소마다 문자열을 복사, k = 서로 다른 키 수
    Best     - 시간: O(n * L) | 공간: O(k * L) - mine_one과 동일
    Sub      - 시간: O(n * L) | 공간: O(k * L) - mine_one과 동일
"""

import time


# ================================================================================
# Mine solution one - for 반복문 + strip
# ================================================================================
def solution_mine_one(fruit: list[str]) -> dict[str, int]:
    """
    각 문자열의 앞뒤 공백을 제거해 키로, 길이를 값으로 딕셔너리에 삽입하는 직접 작성한 풀이

    핵심:
        f.strip() : 앞뒤 공백 제거 (내부 공백은 유지)
        result[f] = len(f) : 공백 제거한 문자열을 키, 길이를 값으로 삽입
        같은 키가 다시 나오면 값을 덮어씀 (길이가 같아 결과 동일)

    한계:
        지문의 딕셔너리 내포 조건을 충족하지 않음
    """
    result = {}
    for f in fruit:
        f = f.strip()
        result[f] = len(f)

    return result


# ================================================================================
# Best solution - 딕셔너리 내포 + map(str.strip)
# ================================================================================
def solution_best(fruit: list[str]) -> dict[str, int]:
    """
    map(str.strip, fruit)을 순회하는 딕셔너리 내포로 strip을 한 번만 호출하는 풀이

    핵심:
        map(str.strip, fruit) : 각 원소를 공백 제거한 이터레이터 (지연 평가)
        {s: len(s) for s in ...} : 같은 변수 s를 키와 값에 사용
        월러스 연산자 없이 Python 3.7에서 동작
        키와 값의 평가 순서에 의존하지 않음
    """
    return {s: len(s) for s in map(str.strip, fruit)}


# ================================================================================
# Sub solution - 딕셔너리 내포 + 월러스 연산자 (Python 3.8+ 전용)
# ================================================================================
def solution_sub(fruit: list[str]) -> dict[str, int]:
    """
    월러스 연산자로 strip 결과를 변수 s에 담아 키와 값에 함께 쓰는 한 줄 풀이

    핵심:
        (s := f.strip()) : 대입과 동시에 값을 키로 사용
        len(s) : 같은 s를 값으로 사용 (키가 먼저 평가되어야 하므로 3.8+ 평가 순서에 의존)

    주의:
        SWEA(Python 3.7.9)에서는 문법 오류로 제출 불가 (로컬 비교용)
    """
    return {(s := f.strip()): len(s) for f in fruit}


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (fruit, 기댓값) - 전부 손 계산
        (['   apple    ', 'banana', '  melon'], {'apple': 5, 'banana': 6, 'melon': 5}),   # 공식 예시
        ([], {}),                                                                          # 빈 리스트
        (['a'], {'a': 1}),                                                                 # 공백 없음
        ([' a ', 'a'], {'a': 1}),                                                          # 공백 제거 후 중복 키
        (['\tab\n'], {'ab': 2}),                                                           # 탭과 개행 제거
        (['a b '], {'a b': 3}),                                                            # 내부 공백 유지
        (['', '   '], {'': 0}),                                                            # 빈 문자열 키
        (['  hi', 'hi  ', ' yo '], {'hi': 2, 'yo': 2}),                                    # 첫 등장 순서
        (['  ab ', 'cd'] * 500_000, {'ab': 2, 'cd': 2}),                                   # 대용량: 서로 다른 키는 2개
    ]

    def is_correct(output: dict[str, int], expected: dict[str, int]) -> bool:
        # 딕셔너리 == 는 순서를 무시하므로 items 순서까지 비교
        return list(output.items()) == list(expected.items())

    solutions = [
        ("Mine (for + strip)",   solution_mine_one),
        ("Best (내포 + map)",     solution_best),
        ("Sub  (내포 + 월러스)",   solution_sub),
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

            status = "PASS" if is_correct(output, expected) else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed*1000:>10.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
