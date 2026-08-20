"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 3
    문제명     : 단어 변환
    유형       : BFS
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/43163
    풀이일자   : 2026-08-20
================================================================================
[문제 요약]
    begin에서 target으로 변환하는 최소 단계 반환
    한 번에 한 글자만 변환 가능, words의 단어로만 변환 가능

    제약 조건
        - 단어 길이: 3 이상 10 이하, 모두 같음
        - words: 3 이상 50 이하, 중복 없음
================================================================================
[입출력 예시]
    begin | target | words                              | return
    ------|--------|-------------------------------------|-------
    "hit" | "cog"  | ["hot","dot","dog","lot","log","cog"] | 4
    "hit" | "cog"  | ["hot","dot","dog","lot","log"]       | 0
================================================================================
[그래프 모델링]
    노드: 각 단어
    간선: 한 글자만 다른 두 단어 사이
    가중치: 모두 1 (변환 1번 = 비용 1)

    hit ─1─ hot ─1─ dot ─1─ dog ─1─ cog
                     │              │
                    lot ─1─ log ─1─┘

    "최소 단계" = 가중치가 동일한 그래프의 최단 경로 → BFS 최적

[BFS가 최단 경로를 보장하는 이유]
    BFS는 가까운 노드(단계 수 적은)부터 탐색
    처음 target에 도달하는 순간의 단계 수 = 최단 단계

[풀이1 vs 풀이2 — 단계 수 관리 방식]
    풀이1: 공통 변수 answer + 레벨별 for 묶음 + for-else
        레벨 단위로 queue를 처리하고 한 레벨이 끝나면 answer += 1
        target 발견 시 break → else 실행 안 됨 → answer 증가 없이 탈출
        target이 queue에 추가되는 단계에서 answer가 이미 계산됨

    풀이2: (word, steps) 튜플로 queue 관리
        각 단어와 변환 단계 수를 함께 저장
        레벨별 묶음 불필요 → target 발견 즉시 return
        visited: list[bool] → set (인덱스 불필요, 코드 간결)

[ref_one — 양방향 BFS (Bidirectional BFS)]
    단방향 BFS: 깊이 d에서 탐색 범위 ≈ b^d (b=분기 수)
    양방향 BFS: begin과 target 양쪽에서 동시 탐색 → 탐색 범위 2×b^(d/2)

    d=4, b=3이면:
        단방향: 3^4 = 81
        양방향: 2 × 3^2 = 18

    front_set: 앞에서 확장 중인 단어들
    back_set:  뒤에서 탐색 대상 (만남 확인용)
    front_set 단어가 back_set에 있으면 → 경로 완성 → return steps+1

    작은 집합을 front로 선택하는 이유:
        더 적은 단어를 확장 → 각 단계 비용 최소화

    이 문제(words≤50)에서는 단방향 BFS로 충분
    노드 수가 많고 경로가 길수록 양방향이 유리

[ref_two — 다익스트라(Dijkstra)]
    BFS:       모든 간선 가중치가 같을 때 최단 경로
    Dijkstra:  간선 가중치가 다를 때도 최단 경로

    핵심 아이디어:
        "현재까지 발견한 거리 중 가장 짧은 것부터 처리"
        → heapq(최소 힙)으로 구현

    visited 대신 거리 비교:
        if current_distance > distances[current_word]: continue
        같은 단어가 큐에 여러 번 들어갈 수 있음
        처음 꺼낼 때가 항상 최단 거리 → 이후는 스킵

    이 문제에서 Dijkstra는 과한 선택:
        모든 가중치=1 → BFS O(V+E)가 Dijkstra O((V+E)logV)보다 빠름
        가중치가 다른 그래프에서 진가 발휘

[알고리즘 선택 기준]
    "최소 이동 횟수", "최소 단계" → BFS
    "최소 비용", "최소 시간", 가중치가 다른 그래프 → Dijkstra
================================================================================
[내 초기 풀이]
    solution_mine_one: BFS + 레벨별 for 묶음 + for-else
    solution_mine_two: BFS + (word, steps) 튜플 + visited set

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Sub
                       레벨별 단계 관리 방식이 코드에 명시적
    solution_mine_two: 개선 필요 없음 - Best
                       튜플로 단계 수 관리, 간결하고 빠름
    solution_ref_one:  양방향 BFS - 이 문제에서 과한 최적화
    solution_ref_two:  Dijkstra - 가중치 동일 문제에서 과한 선택
================================================================================
[복잡도 분석]
    V = len(words) (최대 50), L = 단어 길이 (최대 10)

    Mine_one  - 시간: O(V²×L) | 공간: O(V) - BFS + is_convertible O(L)
    Mine_two  - 시간: O(V²×L) | 공간: O(V) - BFS + set visited
    Ref_one   - 시간: O(V²×L) | 공간: O(V) - 양방향 BFS
    Ref_two   - 시간: O(V²×L×logV) | 공간: O(V) - Dijkstra + heapq
    Best      - 시간: O(V²×L) | 공간: O(V) - Mine_two와 동일
    Sub       - 시간: O(V²×L) | 공간: O(V) - Mine_one과 동일

    V=50, L=10 → 모두 실질적으로 O(1)
"""

import heapq
from collections import deque
import time


# ================================================================================
# Mine solution one - BFS + 레벨별 for 묶음 + for-else
# ================================================================================
def solution_mine_one(begin: str, target: str, words: list[str]) -> int:
    """
    레벨별 for 묶음과 for-else로 변환 단계를 세는 초기 BFS 풀이

    레벨 처리 방식:
        curr_level_size: 현재 레벨의 단어 수
        한 레벨 처리 완료 → answer += 1

    for-else 구조:
        break 없이 for 완료 → else 실행 → answer += 1, continue
        target 발견 → break → else 실행 안 됨 → 바깥 break로 while 종료

    answer가 정확한 이유:
        target이 queue에 추가되는 단계에서 answer가 이미 계산됨
        target을 꺼내는 마지막 레벨에서 answer를 증가시키지 않고 탈출
    """
    if target not in words:
        return 0

    def is_convertible(word1: str, word2: str) -> bool:
        return sum(c1 != c2 for c1, c2 in zip(word1, word2)) == 1

    answer = 0
    queue = deque([begin])
    visited = [False] * len(words)

    while queue:
        curr_level_size = len(queue)

        for _ in range(curr_level_size):
            curr_word = queue.popleft()

            if curr_word == target:
                break

            for i in range(len(words)):
                if not visited[i] and is_convertible(curr_word, words[i]):
                    visited[i] = True
                    queue.append(words[i])
        else:
            answer += 1
            continue

        break

    return answer


# ================================================================================
# Mine solution two - BFS + (word, steps) 튜플 + visited set
# ================================================================================
def solution_mine_two(begin: str, target: str, words: list[str]) -> int:
    """
    (word, steps) 튜플로 단계 수를 개별 관리하는 개선 BFS 풀이

    mine_one 대비 개선:
        visited: list[bool] → set (단어 직접 비교, 인덱스 불필요)
        (word, steps) 튜플: 레벨별 for 묶음 없이 단계 수 관리
        target 발견 즉시 return

    튜플 관리 방식:
        각 단어와 현재까지의 변환 단계 수를 함께 저장
        같은 레벨의 단어들은 모두 같은 steps 값을 가짐
    """
    if target not in words:
        return 0

    def is_convertible(word1: str, word2: str) -> bool:
        return sum(c1 != c2 for c1, c2 in zip(word1, word2)) == 1

    visited = set()
    queue = deque([(begin, 0)])

    while queue:
        curr_word, steps = queue.popleft()

        if curr_word == target:
            return steps

        for word in words:
            if word not in visited and is_convertible(curr_word, word):
                visited.add(word)
                queue.append((word, steps + 1))

    return 0


# ================================================================================
# Ref solution one - 양방향 BFS
# ================================================================================
def solution_ref_one(begin: str, target: str, words: list[str]) -> int:
    """
    begin과 target 양쪽에서 동시 탐색하는 양방향 BFS 참고 풀이

    단방향 BFS: 깊이 d에서 탐색 범위 b^d
    양방향 BFS: 양쪽 깊이 d/2씩 → 2×b^(d/2) (d=4,b=3이면 81→18)

    front_set: 현재 확장 중인 단어들
    back_set:  반대편 탐색 대상 (만남 확인용)
    front 단어가 back_set에 있으면 → 경로 완성 → return steps+1

    작은 집합을 front로 선택:
        len(front_set) > len(back_set)이면 교체
        더 적은 단어를 확장해서 각 단계 비용 최소화

    이 문제(words≤50)에서는 단방향 BFS로 충분
    """
    if target not in words:
        return 0

    front_set = {begin}
    back_set = {target}
    visited = {begin, target}
    steps = 0

    while front_set and back_set:
        if len(front_set) > len(back_set):
            front_set, back_set = back_set, front_set

        next_front = set()

        for word in front_set:
            for next_word in words:
                if sum(c1 != c2 for c1, c2 in zip(word, next_word)) == 1:
                    if next_word in back_set:
                        return steps + 1
                    if next_word not in visited:
                        visited.add(next_word)
                        next_front.add(next_word)

        front_set = next_front
        steps += 1

    return 0


# ================================================================================
# Ref solution two - 다익스트라(Dijkstra)
# ================================================================================
def solution_ref_two(begin: str, target: str, words: list[str]) -> int:
    """
    다익스트라 알고리즘으로 최단 변환 단계를 구하는 참고 풀이

    다익스트라 핵심:
        "현재까지 발견한 거리 중 가장 짧은 것부터 처리"
        → heapq(최소 힙)으로 구현
        → 처음 꺼낼 때가 항상 최단 거리

    visited 없는 이유:
        if current_distance > distances[word]: continue
        이미 더 짧은 경로로 처리된 경우 스킵 (visited와 동일 효과)

    이 문제에서 과한 선택:
        모든 가중치=1 → BFS O(V+E)가 Dijkstra O((V+E)logV)보다 빠름
        가중치가 다른 그래프(예: 도로 통과 시간)에서 진가 발휘
    """
    if target not in words:
        return 0

    distances = {word: float('inf') for word in words}
    distances[begin] = 0

    queue = []
    heapq.heappush(queue, (0, begin))

    while queue:
        current_distance, current_word = heapq.heappop(queue)

        if current_word == target:
            return current_distance

        if current_distance > distances.get(current_word, float('inf')):
            continue

        for next_word in words:
            if sum(c1 != c2 for c1, c2 in zip(current_word, next_word)) == 1:
                cost = current_distance + 1
                if cost < distances[next_word]:
                    distances[next_word] = cost
                    heapq.heappush(queue, (cost, next_word))

    return 0


# ================================================================================
# Best solution - BFS + 튜플 (mine_two 주석 보강)
# ================================================================================
def solution_best(begin: str, target: str, words: list[str]) -> int:
    """
    (word, steps) 튜플 BFS로 최소 변환 단계를 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        가중치=1인 그래프 최단 경로 → BFS 최적 선택
        튜플로 단계 수를 개별 관리 → 레벨별 묶음 불필요
        visited set: O(1) 탐색으로 중복 방문 방지
        target 발견 즉시 return으로 불필요한 탐색 없음
    """
    if target not in words:
        return 0

    def is_convertible(word1: str, word2: str) -> bool:
        return sum(c1 != c2 for c1, c2 in zip(word1, word2)) == 1

    visited = set()
    queue = deque([(begin, 0)])

    while queue:
        curr_word, steps = queue.popleft()

        if curr_word == target:
            return steps

        for word in words:
            if word not in visited and is_convertible(curr_word, word):
                visited.add(word)
                queue.append((word, steps + 1))

    return 0


# ================================================================================
# Sub solution - BFS + 레벨별 for 묶음 (mine_one 주석 보강)
# ================================================================================
def solution_sub(begin: str, target: str, words: list[str]) -> int:
    """
    레벨별 for 묶음으로 BFS 단계를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        curr_level_size로 현재 레벨의 범위를 명시적으로 관리
        for-else로 레벨 완료 시 answer 증가, target 발견 시 탈출
        BFS 레벨 구조가 코드에 직접 드러남
        visited: list[bool] (인덱스 기반)
    """
    if target not in words:
        return 0

    def is_convertible(word1: str, word2: str) -> bool:
        return sum(c1 != c2 for c1, c2 in zip(word1, word2)) == 1

    answer = 0
    queue = deque([begin])
    visited = [False] * len(words)

    while queue:
        curr_level_size = len(queue)

        for _ in range(curr_level_size):
            curr_word = queue.popleft()

            if curr_word == target:
                break

            for i in range(len(words)):
                if not visited[i] and is_convertible(curr_word, words[i]):
                    visited[i] = True
                    queue.append(words[i])
        else:
            answer += 1
            continue

        break

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, str, list[str], int]] = [
        # (begin, target, words, 기댓값)
        # 공식 예시
        # 손 추적: hit→hot→dot→dog→cog = 4단계
        ("hit", "cog", ["hot","dot","dog","lot","log","cog"], 4),
        # target이 words에 없음 → 0
        ("hit", "cog", ["hot","dot","dog","lot","log"],       0),
        # 추가 케이스:
        # begin과 target이 직접 변환 가능
        ("hot", "dot", ["dot","dog"],                         1),
        # 변환 불가
        ("abc", "xyz", ["ayz","axz","axy"],                   0),
    ]

    solutions = [
        ("Mine_one (레벨for-else)  ", solution_mine_one),
        ("Mine_two (튜플BFS)       ", solution_mine_two),
        ("Ref_one  (양방향BFS)     ", solution_ref_one),
        ("Ref_two  (Dijkstra)      ", solution_ref_two),
        ("Best     (튜플BFS)       ", solution_best),
        ("Sub      (레벨for-else)  ", solution_sub),
    ]

    # 워밍업 스텝
    _b, _t, _w, _ = test_cases[0]
    for _, func in solutions:
        func(_b, _t, _w[:])

    print("=" * 68)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (begin, target, words, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(begin, target, words[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
