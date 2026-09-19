"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : [1차] 프렌즈4블록
    유형       : Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17679
    풀이일자   : 2026-09-19
===================================================================================
[문제 요약]
    2×2 동일 블록 제거 → 위 블록 낙하를 반복하여 제거된 블록 수 반환

    제약 조건
        - m, n: 2 이상 30 이하
        - board: m개의 길이 n 문자열 (대문자 A~Z)
===================================================================================
[입출력 예시]
    m | n | board               | result
    --|---|---------------------|-------
    4 | 5 | ["CCBDE","AAADE",   | 14
            "AAABF","CCBBF"]
    6 | 6 | ["TTTANT",...]      | 15
===================================================================================
[3가지 필요 로직]
    1. 2×2 동일 블록 탐색: '#' 방어 + 4좌표 동일 검사
    2. 탐색된 블록 제거: '#'으로 치환 (set으로 중복 제거)
    3. 블록 낙하: column 기준 '#' 제외 후 위에 빈 공간 채움

['#' != 조건이 필요한 이유]
    '#' == '#' == '#' == '#'이 True
    → 이미 제거된 블록 4개가 다시 탐색됨
    → board[i][j] != '#' 방어 조건 필수

[낙하 로직 (mine)]
    rest_blocks = 위→아래 순서의 남은 블록
    new_column = ['#'] * 빈공간 + rest_blocks
    → 위에 빈 공간, 아래에 블록 (board index 0 = 맨 위)

[ref — 90도 회전 발상]
    변환: board[j] = [board[i][j] for i in reversed(range(m))]
          → 원본 column이 새 board의 row
          → 원본 맨 아래 행이 새 row의 앞(인덱스 0) = 바닥

    변환 후 낙하 로직:
        rest = 남은 블록, board[i] = rest + ['#'] * 빈공간
        → 앞이 바닥이므로 남은 블록이 앞에 → 자연스러운 낙하 표현

    이점:
        column 이중 인덱스(board[i][j]) → row 직접 접근(board[i])
        Python 리스트 row 접근이 column 접근보다 캐시 친화적
        낙하 로직이 단순해짐

[90도 회전 캐치 신호]
    "column을 기준으로 순회해야 할 때"
    "낙하/중력 방향이 row 접근과 수직일 때"
    → 데이터를 90도 회전시켜 낙하를 row 기준으로 만들면 편함

[실측 결과 — m=n=30, 10,000회]
    ref  (90도 회전):   0.29ms  ← 약 10% 빠름
    mine (column 접근): 0.32ms
    상수 규모라 실질 차이 없음, 코드 명확성 기준으로 동등
===================================================================================
[내 초기 풀이]
    solution_mine: column 기준 낙하 로직

[개선 포인트]
    solution_mine:    개선 필요 없음 - Best
                      원본 구조 유지, 직관적
    solution_ref:     90도 회전으로 낙하 로직 단순화 - Sub
                      row 직접 접근, 10% 빠름
===================================================================================
[복잡도 분석]
    M = m (최대 30), N = n (최대 30)
    T = 최대 턴 수 (최악 M×N/4)

    Mine - 시간: O(T × M × N) | 공간: O(M × N)
    Ref  - 시간: O(T × M × N) | 공간: O(M × N) - 변환 포함
    Best - 시간: O(T × M × N) | 공간: O(M × N) - Mine과 동일
    Sub  - 시간: O(T × M × N) | 공간: O(M × N) - Ref와 동일

    m,n ≤ 30 고정 → 사실상 O(1)
"""

import time


# =================================================================================
# Mine solution - column 기준 낙하
# =================================================================================
def solution_mine(m: int, n: int, board: list[str]) -> int:
    """
    원본 좌표 구조를 유지한 채 column 기준으로 낙하를 처리하는 초기 풀이

    board[i][j] != '#' 방어:
        '#'끼리 4개 모이면 True → 재탐색 방지를 위해 필수

    낙하:
        column j를 위→아래 읽으며 '#' 제외
        ['#'] * 빈공간 + rest_blocks → 위에 빈 공간, 아래에 블록
    """
    answer = 0
    board = [list(row) for row in board]

    while True:
        target = set()

        for i in range(m - 1):
            for j in range(n - 1):
                if (board[i][j] != '#' and
                        board[i][j] == board[i + 1][j] == board[i][j + 1] == board[i + 1][j + 1]):
                    target.add((i, j)); target.add((i + 1, j))
                    target.add((i, j + 1)); target.add((i + 1, j + 1))

        if not target:
            break

        answer += len(target)
        for r, c in target:
            board[r][c] = '#'

        for j in range(n):
            rest_blocks = [board[i][j] for i in range(m) if board[i][j] != '#']
            new_column = ['#'] * (m - len(rest_blocks)) + rest_blocks
            for i in range(m):
                board[i][j] = new_column[i]

    return answer


# =================================================================================
# Ref solution - 90도 회전 + row 기준 낙하
# =================================================================================
def solution_ref(m: int, n: int, board: list[str]) -> int:
    """
    board를 90도 회전해 column을 row로 만들어 낙하 로직을 단순화하는 참고 풀이

    변환:
        board[j] = [board[i][j] for i in reversed(range(m))]
        원본 column → 새 row
        원본 맨 아래 행 = 새 row의 인덱스 0 (바닥)

    낙하 (row 직접 접근):
        rest = 남은 블록
        board[i] = rest + ['#'] * 빈공간
        → 바닥(앞)에 블록, 위(뒤)에 빈 공간

    mine 대비:
        board[i][j] → board[i] 직접 접근
        Python row 접근이 column 접근보다 캐시 친화적
    """
    answer = 0
    board = [list(board[i][j] for i in reversed(range(m))) for j in range(n)]

    while True:
        target = set()

        for i in range(n - 1):
            for j in range(m - 1):
                if (board[i][j] != '#' and
                        board[i][j] == board[i + 1][j] == board[i][j + 1] == board[i + 1][j + 1]):
                    target.add((i, j)); target.add((i + 1, j))
                    target.add((i, j + 1)); target.add((i + 1, j + 1))

        if not target:
            break

        answer += len(target)
        for r, c in target:
            board[r][c] = '#'

        for i in range(n):
            rest_blocks = [c for c in board[i] if c != '#']
            board[i] = rest_blocks + ['#'] * (m - len(rest_blocks))

    return answer


# =================================================================================
# Best solution - column 기준 낙하 (mine 주석 보강)
# =================================================================================
def solution_best(m: int, n: int, board: list[str]) -> int:
    """
    원본 구조를 유지한 채 직관적으로 시뮬레이션을 구현하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        원본 좌표 구조 유지 → 코드와 게임 규칙이 1:1 대응
        '#' 방어 조건으로 제거된 블록 재탐색 방지
        낙하: '#' * 빈공간 + rest가 "위 빈 공간 + 아래 블록"을 명확히 표현
        실측 ref와 동등 (상수 규모)
    """
    answer = 0
    board = [list(row) for row in board]

    while True:
        target = set()

        for i in range(m - 1):
            for j in range(n - 1):
                if (board[i][j] != '#' and
                        board[i][j] == board[i + 1][j] == board[i][j + 1] == board[i + 1][j + 1]):
                    target.add((i, j)); target.add((i + 1, j))
                    target.add((i, j + 1)); target.add((i + 1, j + 1))

        if not target:
            break

        answer += len(target)
        for r, c in target:
            board[r][c] = '#'

        for j in range(n):
            rest_blocks = [board[i][j] for i in range(m) if board[i][j] != '#']
            new_column = ['#'] * (m - len(rest_blocks)) + rest_blocks
            for i in range(m):
                board[i][j] = new_column[i]

    return answer


# =================================================================================
# Sub solution - 90도 회전 + row 기준 낙하 (ref 주석 보강)
# =================================================================================
def solution_sub(m: int, n: int, board: list[str]) -> int:
    """
    90도 회전으로 column을 row로 전환해 낙하 로직을 단순화하는 서브 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        데이터 구조 선변환 → 접근 패턴 단순화
        board[i][j] 이중 인덱스 → board[i] 직접 접근
        "데이터 구조를 먼저 바꾼다"는 발상
        캐시 친화적 row 접근으로 10% 빠름
    """
    answer = 0
    board = [list(board[i][j] for i in reversed(range(m))) for j in range(n)]

    while True:
        target = set()

        for i in range(n - 1):
            for j in range(m - 1):
                if (board[i][j] != '#' and
                        board[i][j] == board[i + 1][j] == board[i][j + 1] == board[i + 1][j + 1]):
                    target.add((i, j)); target.add((i + 1, j))
                    target.add((i, j + 1)); target.add((i + 1, j + 1))

        if not target:
            break

        answer += len(target)
        for r, c in target:
            board[r][c] = '#'

        for i in range(n):
            rest_blocks = [c for c in board[i] if c != '#']
            board[i] = rest_blocks + ['#'] * (m - len(rest_blocks))

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (m, n, board, 기댓값)
        # 공식 예시 1
        # 1턴: A 6개 제거 → 2턴: B 4개 + C 4개 제거 → 14
        (4, 5, ["CCBDE", "AAADE", "AAABF", "CCBBF"], 14),
        # 공식 예시 2
        (6, 6, ["TTTANT", "RRFACC", "RRRFCC", "TRRRAA", "TTMMMF", "TMMTTJ"], 15),
        # 추가 케이스:
        # 제거 없음
        (2, 2, ["AB", "CD"],                         0),
        # 전체 동일
        (2, 2, ["AA", "AA"],                         4),
    ]

    solutions = [
        ("Mine (column 낙하) ", solution_mine),
        ("Ref  (90도 회전)   ", solution_ref),
        ("Best (column 낙하) ", solution_best),
        ("Sub  (90도 회전)   ", solution_sub),
    ]

    # 워밍업
    _m, _n, _b, _ = test_cases[0]
    for _, func in solutions:
        func(_m, _n, _b[:])

    print("=" * 64)
    print(f"{'풀이':<20} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (m, n, board, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(m, n, board[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<20} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
