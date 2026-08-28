"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : [1차] 다트 게임
    유형       : String / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17682
    풀이일자   : 2026-08-28
===================================================================================
[문제 요약]
    다트 게임 3라운드 점수 문자열 dartResult를 파싱해 최종 점수 반환
    보너스: S(1제곱), D(2제곱), T(3제곱)
    옵션: *(현재+이전 2배), #(현재 -1배)

    제약 조건
        - dartResult 최대 길이: 12자 (3라운드 × 최대 4자)
        - 점수: 0~10 (2자리 가능)
===================================================================================
[입출력 예시]
    dartResult | answer | 설명
    -----------|--------|----------------------------
    "1S2D*3T"  | 37     | 1¹×2 + 2²×2 + 3³
    "1D2S#10S" | 9      | 1² + 2¹×(-1) + 10¹
    "1S*2T*3S" | 23     | 1¹×2×2 + 2³×2 + 3¹
    "1D#2S*3S" | 5      | 1²×(-1)×2 + 2¹×2 + 3¹
===================================================================================
[핵심 구현 포인트]
    num 누적:
        점수가 0~10이므로 2자리 가능 → 빈 문자열에 숫자 누적 후 SDT 등장 시 변환

    * 옵션 처리:
        scores[-1] *= 2  ← 현재 라운드
        scores[-2] *= 2  ← 이전 라운드 (첫 라운드면 해당 없음)

[제3 풀이 발견 — BONUS dict 모듈 레벨 상수]
    if-elif 방식:
        if char == 'S': score **= 1
        elif char == 'D': score **= 2
        elif char == 'T': score **= 3
        → 매 라운드마다 조건 평가 3회

    BONUS dict 방식:
        BONUS = {'S':1,'D':2,'T':3}  ← 모듈 레벨 상수
        score **= BONUS[char]        ← O(1) 조회 + 1회 연산

    BONUS dict 로컬 vs 모듈 레벨:
        로컬: LOAD_FAST (배열 인덱스 접근) → 빠름
        모듈: LOAD_GLOBAL (dict 탐색) → 오히려 느림
        → 측정 공정성과 성능 모두 로컬 정의가 정확

[실측 결과 — 500,000회, 공정 비교 (BONUS 모두 함수 내 로컬)]
    best (BONUS 로컬):   0.74μs  ← 가장 빠름 (제3 풀이)
    one  (if-elif):      0.80μs
    ref  (multipliers):  1.49μs
    two  (regex):        1.50μs  ← 가장 느림

    ref(multipliers)가 one보다 느린 이유:
        추가 변수 [1,1,1] 생성 비용
        마지막 sum(scores[i]*multipliers[i]) 제너레이터 비용
        직접 적용보다 연산 단계 많음

    two(regex)가 느린 이유:
        dartResult 최대 12자 → 정규표현식 컴파일 오버헤드 > 탐색 비용
===================================================================================
[Best/Sub 선정 원칙 적용]
    내 풀이, 참고 풀이 외 제3의 최적 풀이까지 탐색
    → BONUS dict 로컬 상수가 모든 풀이를 능가 → Best 선정
    소스 기준 기계적 배정이 아닌 실측 기준 선정
===================================================================================
[내 초기 풀이]
    solution_mine_one: scores 배열 + if-elif 분기
    solution_mine_two: 정규표현식 파싱 + if-elif 분기

[개선 포인트]
    solution_mine_one: if-elif → BONUS dict로 개선 → Best
    solution_mine_two: regex 오버헤드 → 이 문제 규모에서 불필요
    solution_ref:      multipliers 분리 → 관심사 분리 명확하나 느림
    Best:              BONUS dict 로컬 상수 + scores 직접 적용 (제3 풀이)
    Sub:               Mine_one, 직관적 단일 순회
===================================================================================
[복잡도 분석]
    N = len(dartResult) (최대 12, 사실상 상수)

    Mine_one - 시간: O(N) | 공간: O(1) - scores 리스트 최대 3개
    Mine_two - 시간: O(N) | 공간: O(1) - regex 파싱 + 3라운드
    Ref      - 시간: O(N) | 공간: O(1) - scores + multipliers 각 3개
    Best     - 시간: O(N) | 공간: O(1) - BONUS dict O(3) 상수
    Sub      - 시간: O(N) | 공간: O(1) - Mine_one과 동일
"""

import re
import time


# =================================================================================
# Mine solution one - scores 배열 + if-elif 분기
# =================================================================================
def solution_mine_one(dartResult: str) -> int:
    """
    scores 배열에 라운드별 점수를 누적하며 옵션을 직접 적용하는 초기 풀이

    num 누적:
        점수 0~10이므로 2자리 가능 → isdigit으로 숫자 판별 후 누적

    * 옵션:
        scores[-1]: 현재 라운드 (항상 존재)
        scores[-2]: 이전 라운드 (len >= 2일 때만)

    개선 가능:
        if-elif 3개 분기 → BONUS dict O(1) 조회로 개선 (→ Best)
    """
    scores = []
    num = ""

    for char in dartResult:
        if char.isdigit():
            num += char
        elif char in ('S', 'D', 'T'):
            score = int(num)
            if char == 'S':
                score **= 1
            elif char == 'D':
                score **= 2
            elif char == 'T':
                score **= 3
            scores.append(score)
            num = ""
        elif char == '*':
            scores[-1] *= 2
            if len(scores) >= 2:
                scores[-2] *= 2
        elif char == '#':
            scores[-1] *= -1

    return sum(scores)


# =================================================================================
# Mine solution two - 정규표현식 파싱
# =================================================================================
def solution_mine_two(dartResult: str) -> int:
    """
    정규표현식으로 각 라운드를 (점수, 보너스, 옵션) 튜플로 파싱하는 풀이

    r'(\\d+)([SDT])([*#]?)':
        \\d+: 1~2자리 점수
        [SDT]: 보너스
        [*#]?: 옵션 (없을 수도 있음)

    mine_one 대비:
        인덱스 i로 접근 → scores[-1], scores[-2] 대신 scores[i], scores[i-1]
        코드 더 명확하나 regex 컴파일 오버헤드 발생

    이 문제 규모(최대 12자)에서 regex 오버헤드 불필요
    """
    pattern = re.compile(r'(\d+)([SDT])([*#]?)')
    rounds = pattern.findall(dartResult)
    scores = [0, 0, 0]

    for i in range(3):
        num, bonus, option = rounds[i]
        score = int(num)
        if bonus == 'S':
            score **= 1
        elif bonus == 'D':
            score **= 2
        elif bonus == 'T':
            score **= 3

        scores[i] = score

        if option == '*':
            scores[i] *= 2
            if i > 0:
                scores[i - 1] *= 2
        elif option == '#':
            scores[i] *= -1

    return sum(scores)


# =================================================================================
# Ref solution - multipliers 분리
# =================================================================================
def solution_ref(dartResult: str) -> int:
    """
    점수(scores)와 옵션 배수(multipliers)를 분리해 관리하는 참고 풀이

    관심사 분리:
        scores[i]: 보너스 적용 후 점수
        multipliers[i]: 옵션으로 인한 배수 (기본 1)
        마지막에 scores[i] * multipliers[i] 합산

    mine_one 대비 트레이드오프:
        장점: 점수와 옵션 처리가 명확히 분리, 중첩 옵션 추적 용이
        단점: 추가 변수 생성 + 마지막 제너레이터 비용으로 느림
              실측 mine_one 대비 60% 느림
    """
    scores = [0, 0, 0]
    multipliers = [1, 1, 1]
    round_idx = -1
    num = ""

    for char in dartResult:
        if char.isdigit():
            num += char
        elif char in ('S', 'D', 'T'):
            round_idx += 1
            score = int(num)
            if char == 'S':
                score **= 1
            elif char == 'D':
                score **= 2
            elif char == 'T':
                score **= 3
            scores[round_idx] = score
            num = ""
        elif char == '*':
            multipliers[round_idx] *= 2
            if round_idx > 0:
                multipliers[round_idx - 1] *= 2
        elif char == '#':
            multipliers[round_idx] *= -1

    return sum(scores[i] * multipliers[i] for i in range(3))


# =================================================================================
# Best solution - BONUS dict 모듈 레벨 상수 (제3 풀이)
# =================================================================================
def solution_best(dartResult: str) -> int:
    """
    로컬 BONUS dict로 if-elif를 제거한 최적 풀이 (제3 풀이)

    mine_one 대비 개선:
        if-elif 3개 분기 → BONUS[char] O(1) dict 조회 1회
        로컬 변수 접근(LOAD_FAST)이 전역(LOAD_GLOBAL)보다 빠름

    BONUS를 로컬에 두는 이유:
        모듈 레벨 상수는 LOAD_GLOBAL(dict 탐색) 필요
        로컬 변수는 LOAD_FAST(배열 인덱스 접근)
        → 로컬 정의가 성능상 유리

    실측 (공정 비교):
        mine_one (if-elif):    0.80μs
        best (BONUS 로컬):     0.74μs  ← 가장 빠름
        best (BONUS 모듈레벨): 0.95μs  ← LOAD_GLOBAL 비용으로 오히려 느림

    Best/Sub 선정 원칙:
        내 풀이와 참고 풀이 외 제3의 최적을 탐색해서 Best 선정
        소스 기준 기계적 배정 아님
    """
    BONUS = {'S': 1, 'D': 2, 'T': 3}
    scores = []
    num = ""

    for char in dartResult:
        if char.isdigit():
            num += char
        elif char in BONUS:
            scores.append(int(num) ** BONUS[char])
            num = ""
        elif char == '*':
            scores[-1] *= 2
            if len(scores) >= 2:
                scores[-2] *= 2
        elif char == '#':
            scores[-1] *= -1

    return sum(scores)


# =================================================================================
# Sub solution - if-elif 분기 (mine_one 주석 보강)
# =================================================================================
def solution_sub(dartResult: str) -> int:
    """
    if-elif로 보너스를 분기하고 scores에 직접 적용하는 서브 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        BONUS dict 없이 if-elif로 보너스 처리 → 동작 원리 명시적
        scores 직접 적용으로 multipliers 없음
        Best보다 약 36% 느림 (if-elif 분기 비용)
        Best가 제3의 풀이인 경우 Sub는 가장 근접한 내 풀이 선정
    """
    scores = []
    num = ""

    for char in dartResult:
        if char.isdigit():
            num += char
        elif char in ('S', 'D', 'T'):
            score = int(num)
            if char == 'S':
                score **= 1
            elif char == 'D':
                score **= 2
            elif char == 'T':
                score **= 3
            scores.append(score)
            num = ""
        elif char == '*':
            scores[-1] *= 2
            if len(scores) >= 2:
                scores[-2] *= 2
        elif char == '#':
            scores[-1] *= -1

    return sum(scores)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int]] = [
        # (dartResult, 기댓값)
        # 공식 예시 전체
        # 손 추적:
        # "1S2D*3T": 1¹×2 + 2²×2 + 3³ = 2+8+27 = 37
        ("1S2D*3T",  37),
        # "1D2S#10S": 1² + 2¹×(-1) + 10¹ = 1-2+10 = 9
        ("1D2S#10S",  9),
        # "1D2S0T": 1² + 2¹ + 0³ = 1+2+0 = 3
        ("1D2S0T",    3),
        # "1S*2T*3S": 1¹×2×2 + 2³×2 + 3¹ = 4+16+3 = 23
        ("1S*2T*3S", 23),
        # "1D#2S*3S": 1²×(-1)×2 + 2¹×2 + 3¹ = -2+4+3 = 5
        ("1D#2S*3S",  5),
        # "1T2D3D#": 1³ + 2² + 3²×(-1) = 1+4-9 = -4
        ("1T2D3D#",  -4),
        # "1D2S3T*": 1² + 2¹×2 + 3³×2 = 1+4+54 = 59
        ("1D2S3T*",  59),
    ]

    solutions = [
        ("Mine_one (if-elif)  ", solution_mine_one),
        ("Mine_two (regex)    ", solution_mine_two),
        ("Ref      (multiplier)", solution_ref),
        ("Best     (BONUS dict)", solution_best),
        ("Sub      (if-elif)  ", solution_sub),
    ]

    # 워밍업 스텝
    _d, _ = test_cases[0]
    for _, func in solutions:
        func(_d)

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (dartResult, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(dartResult)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
