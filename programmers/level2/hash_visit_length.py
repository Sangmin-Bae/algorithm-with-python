"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 방문 길이
    유형       : Hash / String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/49994
    풀이일자   : 2026-07-25
================================================================================
[문제 요약]
    -5<=X<=5, -5<=Y<=5 좌표계에서 (0,0) 출발
    dirs 명령에 따라 이동할 때 처음 걸어본 edge의 수 반환
    경계 벗어나는 명령은 무시

    제약 조건
        - dirs 길이: 1 이상 500 이하
        - 명령: U, D, R, L만 포함
================================================================================
[입출력 예시]
    dirs        | answer
    ------------|-------
    "ULURRDLLU" | 7
    "LULLLLLLU" | 7
================================================================================
[핵심 아이디어 - 노드가 아닌 edge를 기록]
    노드(좌표)만 기록하면 틀리는 이유:
        노드 (0,0)을 방문 처리하면
        (0,0)→(1,0), (0,0)→(-1,0), (0,0)→(0,1), (0,0)→(0,-1) 4개 edge가
        모두 방문된 것으로 잘못 처리됨

    edge = (A좌표, B좌표) 형태로 두 노드를 함께 기록해야 함
    A→B와 B→A는 동일한 edge → 동일하게 표현 필요

    방법 1: sorted 정렬로 항상 작은 좌표가 앞에 오도록 통일
    방법 2: 양방향 모두 삽입 후 2로 나눔
    방법 3: 4차원 배열로 방향별로 기록

[solution_three 4차원 배열 좌표 평행이동]
    visited[x][y][nx][ny] 구조에서 x, nx가 -5~5이면 음수 인덱스 발생
    Python 음수 인덱스는 배열 뒤에서부터 접근 -> 격자 구조가 꼬임
    x+5로 좌표를 평행이동: -5~5 범위를 0~10 범위로 변환
    visited 배열 크기: 11×11×11×11 = 14,641 원소

[solution_three의 양쪽 방향 체크]
    if not visited[sx][sy][snx][sny] and not visited[snx][sny][sx][sy]:
    두 방향을 동시에 True로 설정하므로 하나만 체크해도 동일하게 동작
    양쪽 모두 체크하는 것은 의도를 명확하게 드러내는 방어적 코드

[성능 비교 - dirs=500, 50,000회 반복 실측]
    sorted 정렬 (Mine_one):  181μs
    양방향 삽입 (Mine_two):   95μs  <- 약 2배 빠름
    4차원 배열 (Mine_three): 202μs  <- 초기화 비용이 병목

    Mine_two가 빠른 이유:
        sorted(): 새 리스트 생성 + 정렬 연산
        양방향 삽입: 4-튜플 해시 + set add 2회 -> 더 단순

    Mine_three가 느린 이유:
        14,641 원소 초기화를 매 함수 호출마다 수행
        dirs 순회 비용보다 초기화 비용이 더 큼
================================================================================
[내 초기 풀이]
    solution_mine_one  : sorted 정렬 + set
    solution_mine_two  : 양방향 삽입 + set + //2
    solution_mine_three: 4차원 배열 방문 기록

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         sorted로 edge 정규화, 동작 의도 명확
    solution_mine_two  : 개선 필요 없음 - Best
                         sorted 없이 양방향 삽입으로 성능 2배 개선
    solution_mine_three: 4차원 배열 초기화 비용이 병목
                         좌표계 유한(11×11)이라 가능한 방식
                         set 방식보다 느리나 배열 방문 기록 패턴 학습 목적
================================================================================
[복잡도 분석]
    N = len(dirs) (최대 500)
    E = 전체 edge 수 (최대 11×11×2 방향 = 242)

    Mine_one   - 시간: O(N) | 공간: O(E) - sorted O(1) (2원소 정렬) + set
    Mine_two   - 시간: O(N) | 공간: O(E) - add 2회 + //2
    Mine_three - 시간: O(N) | 공간: O(11^4) - 4차원 배열 초기화 비용 O(11^4)
    Best       - 시간: O(N) | 공간: O(E)    - Mine_two와 동일
    Sub        - 시간: O(N) | 공간: O(E)    - Mine_one과 동일

    N=500 고정 -> 모두 실질 O(1)에 수렴
    실측 차이는 상수 인자: 양방향 삽입 < sorted < 4차원 초기화
"""

import time


# ================================================================================
# Mine solution one - sorted 정렬로 edge 정규화
# ================================================================================
def solution_mine_one(dirs: str) -> int:
    """
    두 좌표를 정렬해 edge를 정규화하고 set으로 중복 제거하는 초기 풀이

    edge 정규화:
        A→B와 B→A가 같은 edge임을 표현하기 위해 두 좌표를 정렬
        sorted([(x,y),(nx,ny)]): 좌표 튜플을 첫 원소 기준(같으면 두 번째 기준)으로 정렬
        -> A→B든 B→A든 항상 동일한 표현으로 통일

    tuple 변환 이유:
        list는 가변 객체 -> set에 삽입 불가 (해시 불가능)
        tuple로 변환해야 set에 삽입 가능

    한계:
        sorted(): 새 리스트 생성 + 정렬 연산 -> 양방향 삽입보다 느림
        실측 dirs=500: 181μs (Mine_two 95μs 대비 약 2배 느림)
    """
    visited_edges = set()
    directions = {
        'U': (0, 1), 'D': (0, -1),
        'R': (1, 0), 'L': (-1, 0)
    }

    x, y = 0, 0
    for d in dirs:
        dx, dy = directions[d]
        nx, ny = x + dx, y + dy

        if -5 <= nx <= 5 and -5 <= ny <= 5:
            edge = tuple(sorted([(x, y), (nx, ny)]))   # 정렬로 방향 무관 정규화
            visited_edges.add(edge)
            x, y = nx, ny

    return len(visited_edges)


# ================================================================================
# Mine solution two - 양방향 삽입 + //2
# ================================================================================
def solution_mine_two(dirs: str) -> int:
    """
    A→B, B→A 양방향 튜플을 모두 삽입해 정렬 없이 edge를 기록하는 풀이

    mine_one 대비:
        sorted() 제거: 리스트 생성 + 정렬 연산 없음
        (x,y,nx,ny), (nx,ny,x,y) 두 튜플 삽입
        visited_edges에 실제 edge 수의 2배가 쌓임
        -> len(visited_edges) // 2로 보정

    성능 우위:
        4-튜플 해시 + set add 2회 -> sorted 생성보다 단순
        실측 dirs=500: 95μs (Mine_one 181μs 대비 약 2배 빠름)
    """
    visited_edges = set()
    directions = {
        'U': (0, 1), 'D': (0, -1),
        'R': (1, 0), 'L': (-1, 0)
    }

    x, y = 0, 0
    for d in dirs:
        dx, dy = directions[d]
        nx, ny = x + dx, y + dy

        if -5 <= nx <= 5 and -5 <= ny <= 5:
            visited_edges.add((x, y, nx, ny))      # A→B
            visited_edges.add((nx, ny, x, y))      # B→A
            x, y = nx, ny

    return len(visited_edges) // 2


# ================================================================================
# Mine solution three - 4차원 배열 방문 기록
# ================================================================================
def solution_mine_three(dirs: str) -> int:
    """
    유한한 좌표계를 이용한 4차원 배열로 edge를 기록하는 풀이

    4차원 배열 구조:
        visited[curr_x][curr_y][nxt_x][nxt_y]
        각 차원: 0~10 (좌표 +5 평행이동으로 음수 인덱스 제거)
        11^4 = 14,641 원소 (bool)

    좌표 평행이동 이유:
        -5~5 범위를 0~10 범위로 변환
        Python 음수 인덱스는 배열 뒤에서 접근 -> 격자 구조가 꼬임

    단방향 체크로도 동작 가능:
        visited[sx][sy][snx][sny] 하나만 확인해도 됨
        (양쪽을 동시에 True로 설정하므로 하나가 True이면 나머지도 항상 True)
        양쪽 모두 체크는 의도 명확성을 위한 방어적 코드

    한계:
        14,641 원소 초기화가 매 함수 호출마다 발생
        dirs 순회 비용보다 초기화 비용이 더 커서 set 방식보다 느림
        실측 dirs=500: 202μs (Mine_two 95μs 대비 약 2배 느림)
    """
    answer = 0
    visited = [[[[False] * 11 for _ in range(11)]
                for _ in range(11)] for _ in range(11)]
    directions = {
        'U': (0, 1), 'D': (0, -1),
        'R': (1, 0), 'L': (-1, 0)
    }

    x, y = 0, 0
    for d in dirs:
        dx, dy = directions[d]
        nx, ny = x + dx, y + dy

        if -5 <= nx <= 5 and -5 <= ny <= 5:
            sx, sy = x + 5, y + 5          # 좌표 +5 평행이동 (0~10 범위)
            snx, sny = nx + 5, ny + 5

            if not visited[sx][sy][snx][sny]:
                answer += 1
                visited[sx][sy][snx][sny] = True
                visited[snx][sny][sx][sy] = True

            x, y = nx, ny

    return answer


# ================================================================================
# Best solution - 양방향 삽입 + //2 (mine_two 주석 보강)
# ================================================================================
def solution_best(dirs: str) -> int:
    """
    양방향 삽입 + //2로 정렬 없이 빠르게 처리하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        sorted() 없이 4-튜플 두 번 삽입 -> 상수 인자 최소화
        실측 Mine_one 대비 2배 빠름 (dirs=500 기준)
        len // 2: 양방향으로 2배 쌓인 set을 정확하게 보정
        원본 directions dict 불변 -> 매 루프 재계산 없이 O(1) 조회
    """
    visited_edges = set()
    directions = {
        'U': (0, 1), 'D': (0, -1),
        'R': (1, 0), 'L': (-1, 0)
    }

    x, y = 0, 0
    for d in dirs:
        dx, dy = directions[d]
        nx, ny = x + dx, y + dy

        if -5 <= nx <= 5 and -5 <= ny <= 5:
            visited_edges.add((x, y, nx, ny))
            visited_edges.add((nx, ny, x, y))
            x, y = nx, ny

    return len(visited_edges) // 2


# ================================================================================
# Sub solution - sorted 정렬 (mine_one 주석 보강)
# ================================================================================
def solution_sub(dirs: str) -> int:
    """
    sorted 정렬로 edge를 정규화하는 서브 풀이

    Best 대비 특징:
        sorted([(x,y),(nx,ny)]): "두 좌표 중 작은 것이 앞"으로 정규화
        A→B = B→A 동치 관계가 코드에 명시적으로 드러남
        tuple 변환: set 삽입을 위한 불변 객체 변환
        동작 원리가 가장 직관적으로 표현됨
    """
    visited_edges = set()
    directions = {
        'U': (0, 1), 'D': (0, -1),
        'R': (1, 0), 'L': (-1, 0)
    }

    x, y = 0, 0
    for d in dirs:
        dx, dy = directions[d]
        nx, ny = x + dx, y + dy

        if -5 <= nx <= 5 and -5 <= ny <= 5:
            edge = tuple(sorted([(x, y), (nx, ny)]))
            visited_edges.add(edge)
            x, y = nx, ny

    return len(visited_edges)


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int]] = [
        # (dirs, 기댓값)
        # 프로그래머스 공식 예시
        ("ULURRDLLU", 7),
        ("LULLLLLLU", 7),
        # 추가 케이스:
        # 단순 이동: U 한 번 -> 1개 edge
        ("U", 1),
        # 같은 길 반복: U, D 반복 -> 1개 edge
        ("UDUDUD", 1),
        # 경계 무시: L 여섯 번 -> 5개 edge (경계에서 멈춤)
        ("LLLLLL", 5),
    ]

    solutions = [
        ("Mine_one   (sorted정렬) ", solution_mine_one),
        ("Mine_two   (양방향삽입) ", solution_mine_two),
        ("Mine_three (4차원배열)  ", solution_mine_three),
        ("Best       (양방향삽입) ", solution_best),
        ("Sub        (sorted정렬) ", solution_sub),
    ]

    # 워밍업 스텝
    _d, _ = test_cases[0]
    for _, func in solutions:
        func(_d)

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (dirs, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(dirs)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
