"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : [PCCE 기출문제] 9번 / 이웃한 칸
    유형       : Graph / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/250125
    풀이일자   : 2026-08-24
===================================================================================
[문제 요약]
    2차원 격자 board에서 (h, w) 위치의 색과 인접한 4방향 칸 중
    같은 색의 칸 개수 반환

    제약 조건
        - board 크기: 1×1 이상 7×7 이하 (정사각형)
        - 색 이름 길이: 1 이상 10 이하 영어 소문자
===================================================================================
[입출력 예시]
    board (4×4), h=1, w=1 | result
    ----------------------|-------
    board[1][1]="red"     | 2      (위=red, 왼=red 두 칸)
===================================================================================
[핵심 — 4방향 탐색 + 경계 검증]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
        (dh, dw): 상/하/좌/우 방향 이동량

    경계 검증:
        0 <= nh < N and 0 <= nw < N
        범위 초과 시 IndexError 방지

    continue 패턴 (조기 탈출):
        경계 초과 시 즉시 다음 루프로
        중첩 if 없이 범위 검증과 색 비교를 명확히 분리
        continue: JUMP_ABSOLUTE 1개 명령어, 비용 무시 가능

[bool의 int 성질 활용 — 풀이2]
    Python에서 bool은 int의 서브클래스
    True == 1, False == 0
    sum(True, False, True) = 2

    단락 평가(short-circuit):
        0 <= nh < N and 0 <= nw < N and board[...] == ...
        범위 초과 시 마지막 조건 평가 안 함 → IndexError 방지

[variation이 적은 이유]
    의사코드가 제공됨 → 접근법이 사실상 하나
    4방향 탐색 + 경계 검증이 전부
    최적화 여지: board 크기 최대 7×7 = 49칸, 연산량 완전 상수
===================================================================================
[내 초기 풀이]
    solution_mine_one: 명시적 for + continue + if
    solution_mine_two: sum + 제너레이터 + 단락 평가

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       continue로 가독성 확보, 동작 원리 명시적
    solution_mine_two: 개선 필요 없음 - Sub
                       sum + bool 성질로 간결하게 표현
                       한 줄이 길어 가독성은 mine_one에 비해 낮음
===================================================================================
[복잡도 분석]
    board 크기 최대 7×7, 방향 4개 고정

    Mine_one - 시간: O(1) | 공간: O(1) - 4방향 상수 루프
    Mine_two - 시간: O(1) | 공간: O(1) - 4방향 제너레이터
    Best     - 시간: O(1) | 공간: O(1) - Mine_one과 동일
    Sub      - 시간: O(1) | 공간: O(1) - Mine_two와 동일
"""

import time


# =================================================================================
# Mine solution one - 명시적 for + continue + if
# =================================================================================
def solution_mine_one(board: list[list[str]], h: int, w: int) -> int:
    """
    continue로 경계 검증을 분리하고 if로 색 비교하는 명시적 초기 풀이

    target_color 미리 캐싱:
        루프 안에서 board[h][w]를 반복 접근하지 않음
        이 문제에서 4번이라 차이 없으나 대규모 루프에서 유효한 습관

    continue 패턴 (조기 탈출):
        경계 초과 시 즉시 다음 방향으로
        중첩 if보다 들여쓰기가 얕아 가독성 향상
        JUMP_ABSOLUTE 1개 명령어, 비용 무시 가능
    """
    N = len(board)
    target_color = board[h][w]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    answer = 0
    for dh, dw in directions:
        nh = h + dh
        nw = w + dw

        if not (0 <= nh < N and 0 <= nw < N):
            continue

        if board[nh][nw] == target_color:
            answer += 1

    return answer


# =================================================================================
# Mine solution two - sum + 제너레이터 + 단락 평가
# =================================================================================
def solution_mine_two(board: list[list[str]], h: int, w: int) -> int:
    """
    sum과 bool의 int 성질로 조건 만족 칸 수를 구하는 압축 풀이

    bool의 int 성질:
        True == 1, False == 0
        sum(조건들) = 참인 조건의 수

    단락 평가 (short-circuit):
        범위 조건이 False이면 board 접근 없이 False 반환
        → IndexError 방지

    가독성:
        한 줄이 길어 mine_one 대비 가독성 낮음
        코딩테스트에서는 간결함, 실무에서는 mine_one 선호
    """
    N = len(board)
    target_color = board[h][w]

    return sum(
        0 <= h + dh < N and 0 <= w + dw < N and board[h + dh][w + dw] == target_color
        for dh, dw in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    )


# =================================================================================
# Best solution - 명시적 for + continue (mine_one 주석 보강)
# =================================================================================
def solution_best(board: list[list[str]], h: int, w: int) -> int:
    """
    continue로 경계 검증을 명시적으로 분리하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        경계 검증 / 색 비교가 명확히 분리
        continue로 중첩 없이 조기 탈출
        이 문제에서 variation이 거의 없어 두 풀이 모두 동급
        가독성 기준으로 mine_one 선택
    """
    N = len(board)
    target_color = board[h][w]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    answer = 0
    for dh, dw in directions:
        nh = h + dh
        nw = w + dw

        if not (0 <= nh < N and 0 <= nw < N):
            continue

        if board[nh][nw] == target_color:
            answer += 1

    return answer


# =================================================================================
# Sub solution - sum + 제너레이터 (mine_two 주석 보강)
# =================================================================================
def solution_sub(board: list[list[str]], h: int, w: int) -> int:
    """
    sum + bool 성질로 간결하게 표현하는 서브 풀이

    Best 대비 특징:
        코드 2줄로 압축
        단락 평가로 경계 검증과 색 비교를 한 표현식에
        bool이 int 서브클래스임을 활용
        가독성은 Best 대비 낮음 (긴 한 줄)
    """
    N = len(board)
    target_color = board[h][w]

    return sum(
        0 <= h + dh < N and 0 <= w + dw < N and board[h + dh][w + dw] == target_color
        for dh, dw in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    )


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (board, h, w, 기댓값)
        # 공식 예시 1
        ([["blue","red","orange","red"],
          ["red","red","blue","orange"],
          ["blue","orange","red","red"],
          ["orange","orange","red","blue"]], 1, 1, 2),
        # 공식 예시 2
        ([["yellow","green","blue"],
          ["blue","green","yellow"],
          ["yellow","blue","blue"]], 0, 1, 1),
        # 추가 케이스:
        # 모서리 (경계 2방향 초과)
        ([["red","blue"],
          ["blue","red"]], 0, 0, 0),
        # 1×1 보드
        ([["red"]], 0, 0, 0),
        # 모든 인접 칸 같은 색
        ([["a","a","a"],
          ["a","a","a"],
          ["a","a","a"]], 1, 1, 4),
    ]

    solutions = [
        ("Mine_one (continue)  ", solution_mine_one),
        ("Mine_two (sum+bool)  ", solution_mine_two),
        ("Best     (continue)  ", solution_best),
        ("Sub      (sum+bool)  ", solution_sub),
    ]

    # 워밍업 스텝
    _b, _h, _w, _ = test_cases[0]
    for _, func in solutions:
        func(_b, _h, _w)

    print("=" * 60)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 60)

    for name, func in solutions:
        for idx, (board, h, w, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(board, h, w)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 60)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
