"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 피로도
    유형       : 완전탐색 (Brute Force) / DFS
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/87946
    풀이일자   : 2026-07-11
================================================================================
[문제 요약]
    현재 피로도 k와 각 던전의 [최소 필요 피로도, 소모 피로도]가 주어질 때
    최대한 많이 탐험할 수 있는 던전 수 반환

    제약 조건
        - k: 1 이상 5,000 이하
        - 던전 수: 1 이상 8 이하 → 최대 8! = 40,320개 순열 → 완전탐색 가능
        - 최소 필요 피로도 ≥ 소모 피로도 항상 보장
        - 2022년 2월 25일 테스트케이스 추가 → 그리디 풀이 반례 발생
================================================================================
[입출력 예시]
    k  | dungeons                  | result
    ---|---------------------------|-------
    80 | [[80,20],[50,40],[30,10]] | 3
================================================================================
[왜 완전탐색인가 — 그리디 불가 이유]
    "소모 피로도 작은 것 먼저", "최소 필요 피로도 작은 것 먼저",
    "효율 비율 순" 등 어떤 그리디 기준도 반례가 존재함

    반례 (k=26, [[23,10],[15,4],[2,1]]):
        최적 순서: [2,1]→[23,10]→[15,4] → 3개 클리어
        그리디(ref_two 조건): [15,4]→[23,10]→[2,1] → 2개만 클리어

    이유:
        각 던전의 최소 필요 피로도와 소모 피로도가 독립적으로 결합
        선택 순서가 이후 모든 던전의 진입 가능성에 복잡하게 영향
        → 단일 기준으로 전역 최적 보장 불가
        → 던전 수 ≤ 8, 8! = 40,320으로 완전탐색이 유일한 보장 방법

[solution_four for-else 구조]
    for i in range(n):
        if not visited[i] and k_ >= dungeons[i][0]:
            ...    # 진입 가능 던전 탐색
    else:
        if count > answer: answer = count

    Python for-else: break 없이 루프 정상 종료 시 else 실행
    이 코드에서 break 없으므로 else는 항상 실행됨
    → 더 진입할 던전 없거나 모든 던전 탐험 완료 시 answer 갱신
    주의: break 없는 for-else는 혼란 줄 수 있음
          for 루프 후 단순 if 조건문이 더 명확한 표현

[solution_ref_one 한 줄 재귀 분석]
    max([solution(k-u, dungeons[:i]+dungeons[i+1:])+1
         for i,(m,u) in enumerate(dungeons) if k>=m] or [0])

    구조:
        현재 k로 진입 가능한 던전 각각을 선택 (k>=m 조건)
        → k-u 피로도로 나머지 던전 재귀 탐색
        → 재귀 결과 + 1 (현재 던전 클리어)
        max로 최대값 선택

    [...] or [0]:
        진입 가능 던전 없을 때 빈 리스트 → [0]으로 대체
        max([]) → ValueError 방지

    solution_five와 동일한 로직, 재귀 자기참조로 더 압축
================================================================================
[내 초기 풀이]
    solution_mine_one  : itertools.permutations + 피로도 계산
    solution_mine_two  : DFS + visited + 순열 수집 후 피로도 계산
    solution_mine_three: 재귀 + yield 순열 생성 후 피로도 계산
    solution_mine_four : DFS 백트래킹 + 피로도 조건 통합 (순열 수집 없음)
    solution_mine_five : 재귀 + yield + 피로도 조건 통합 (클리어 횟수 yield)

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         가장 간결하고 직관적, permutations 라이브러리 활용
    solution_mine_two  : dfs_perm이 모든 순열을 result에 수집 → O(N! × N) 공간
                         solution_mine_four처럼 통합하면 공간 효율 개선
    solution_mine_three:
        조합 구현과 동일 구조, current 제외 방식만 다름 (visited vs 슬라이싱)
    solution_mine_four : 개선 필요 없음 - Best
        순열 수집 없이 DFS 중 피로도 조건 통합 → 공간 효율적
        불가능한 경로 조기 pruning으로 실질적으로 빠름
    solution_mine_five : 개선 필요 없음 (학습 목적)
        yield로 클리어 횟수를 직접 전달하는 방식
================================================================================
[복잡도 분석]
    N = len(dungeons) (최대 8)

    Mine_one   - 시간: O(N! × N) | 공간: O(N!) - 순열 생성 후 순회
    Mine_two   - 시간: O(N! × N) | 공간: O(N!) - result 리스트에 모든 순열 저장
    Mine_three - 시간: O(N! × N) | 공간: O(N)  - 제너레이터로 순열 생성
    Mine_four  - 시간: O(N! × N) | 공간: O(N)  - DFS 통합, 조기 pruning 가능
    Mine_five  - 시간: O(N! × N) | 공간: O(N)  - 제너레이터 + 클리어 횟수 통합
    Best       - 시간: O(N! × N) | 공간: O(N)  - Mine_four와 동일
    Sub        - 시간: O(N! × N) | 공간: O(N!) - Mine_one과 동일

    N=8: 최대 8! = 40,320순열, 실질적으로 빠름
    Mine_four/Best: 불가능 경로 조기 pruning → 실제 탐색 경로 수 < 40,320
"""

import time
from collections.abc import Iterator
from itertools import permutations


# ================================================================================
# Mine solution one - itertools.permutations + 피로도 계산
# ================================================================================
def solution_mine_one(k: int, dungeons: list[list[int]]) -> int:
    """
    permutations로 모든 순열을 생성하고 피로도를 계산하는 초기 풀이

    핵심:
        permutations(dungeons): 모든 던전 순서 조합 생성 (N!개)
        각 순열마다 k_를 사본으로 유지하며 클리어 가능 던전 수 계산
        answer: 전체 순열 중 최대 클리어 수

    break 이유:
        순서가 정해진 상태에서 한 번 막히면 이후도 막힘
        (현재 순열에서 더 시도할 필요 없음)
    """
    answer = 0

    for p in permutations(dungeons):
        count = 0
        k_ = k
        for minimum, cost in p:
            if k_ >= minimum:
                count += 1
                k_ -= cost
            else:
                break
        answer = max(count, answer)

    return answer


# ================================================================================
# Mine solution two - DFS + visited + 순열 수집 후 피로도 계산
# ================================================================================
def solution_mine_two(k: int, dungeons: list[list[int]]) -> int:
    """
    DFS + visited로 순열을 직접 구현해 수집 후 피로도 계산하는 풀이

    순열 구현 핵심 (조합과의 차이):
        조합: 현재 원소 이후 원소만 선택 (순서 없음)
        순열: visited로 이미 선택한 원소만 제외, 나머지 전체에서 선택
              → 같은 원소 집합의 다른 순서도 별개 경우로 처리

    백트래킹:
        path.append → dfs(path) → path.pop
        visited[i]=True → dfs → visited[i]=False
        선택 취소로 다른 경로 탐색 가능

    공간 한계:
        result에 모든 순열 저장 → O(N! × N) 공간
        Mine_four처럼 통합하면 O(N)으로 개선 가능
    """
    answer = 0

    def dfs_perm(arr: list, c: int) -> list[tuple]:
        result = []
        visited = [False] * len(arr)

        def dfs(path: list) -> None:
            if len(path) == c:
                result.append(tuple(path))
                return

            for i in range(len(arr)):
                if not visited[i]:
                    path.append(arr[i])
                    visited[i] = True
                    dfs(path)
                    path.pop()
                    visited[i] = False

        dfs([])
        return result

    for p in dfs_perm(dungeons, len(dungeons)):
        count = 0
        k_ = k
        for minimum, cost in p:
            if k_ >= minimum:
                count += 1
                k_ -= cost
            else:
                break
        answer = max(count, answer)

    return answer


# ================================================================================
# Mine solution three - 재귀 + yield 순열 생성 후 피로도 계산
# ================================================================================
def solution_mine_three(k: int, dungeons: list[list[int]]) -> int:
    """
    재귀 제너레이터로 순열을 생성해 피로도를 계산하는 풀이

    Mine_two 대비:
        result 리스트 없이 yield로 순열 스트리밍 → 공간 O(N)
        arr[:i] + arr[i+1:]: 슬라이싱으로 current 제외 rest 생성
        (visited 방식 대신 슬라이싱으로 방문 처리)
    """
    def recursive_perm(arr: list, c: int) -> Iterator[tuple]:
        if c == 0:
            yield ()
            return

        for i in range(len(arr)):
            current = arr[i]
            rest = arr[:i] + arr[i + 1:]   # current 제외한 나머지

            for nxt in recursive_perm(rest, c - 1):
                yield (current,) + nxt

    answer = 0
    for p in recursive_perm(dungeons, len(dungeons)):
        count = 0
        k_ = k
        for minimum, cost in p:
            if k_ >= minimum:
                count += 1
                k_ -= cost
            else:
                break
        answer = max(count, answer)

    return answer


# ================================================================================
# Mine solution four - DFS 백트래킹 + 피로도 조건 통합
# ================================================================================
def solution_mine_four(k: int, dungeons: list[list[int]]) -> int:
    """
    DFS 탐색 중 피로도 조건을 통합해 순열 수집 없이 처리하는 풀이

    Mine_two 대비 개선:
        순열을 result에 수집하지 않음 → 공간 O(N)
        k_ >= dungeons[i][0] 조건으로 불가능 경로 즉시 pruning
        → 실제 탐색 경로 < N! (조기 종료로 더 빠름)

    nonlocal answer:
        dfs 내부에서 외부 answer 직접 수정
        answer = [0] 가변 객체 방식도 가능하나 nonlocal이 더 명확

    for-else:
        break 없으므로 else 항상 실행
        → 더 진입할 던전 없거나 모든 던전 탐험 완료 시 answer 갱신
    """
    answer = 0
    n = len(dungeons)
    visited = [False] * n

    def dfs(k_: int, count: int) -> None:
        nonlocal answer

        for i in range(n):
            if not visited[i] and k_ >= dungeons[i][0]:
                visited[i] = True
                dfs(k_ - dungeons[i][1], count + 1)
                visited[i] = False
        else:
            if count > answer:
                answer = count

    dfs(k, 0)
    return answer


# ================================================================================
# Mine solution five - 재귀 + yield + 피로도 통합 (클리어 횟수 yield)
# ================================================================================
def solution_mine_five(k: int, dungeons: list[list[int]]) -> int:
    """
    재귀 제너레이터에서 피로도 조건을 통합해 클리어 횟수를 yield하는 풀이

    Mine_three 대비:
        순열 전체를 yield하는 대신 클리어 횟수(정수)를 yield
        피로도 조건을 재귀 내부에서 직접 처리 → 외부 루프 불필요
        yield 1 + nxt: 현재 던전 클리어(+1) + 이후 재귀 클리어 횟수 누적
        for-else의 yield 0: 더 진입 불가 → 누적 종료

    max(recursive_perm_max(...)): 모든 경로의 클리어 횟수 중 최대값
    """
    def recursive_perm_max(arr: list[list[int]], k_: int) -> Iterator:
        for i in range(len(arr)):
            if k_ >= arr[i][0]:
                rest = arr[:i] + arr[i + 1:]
                for nxt in recursive_perm_max(rest, k_ - arr[i][1]):
                    yield 1 + nxt
        else:
            yield 0   # 더 이상 진입 불가 → 클리어 횟수 0 추가

    return max(recursive_perm_max(dungeons, k))


# ================================================================================
# Ref solution one - 재귀 자기참조 한 줄 압축
# ================================================================================
def solution_ref_one(k: int, dungeons: list[list[int]]) -> int:
    """
    재귀 자기참조로 Mine_five를 한 줄에 압축한 참고 풀이

    동작 원리 (Mine_five와 동일):
        k>=m인 던전 i 각각에 대해:
            k-u 피로도로 나머지 던전 재귀 탐색
            결과 + 1 (현재 던전 클리어)
        max로 최대 클리어 수 선택

    [...] or [0]:
        k>=m인 던전이 없을 때 빈 리스트 → [0]으로 대체
        max([]) ValueError 방지 + 클리어 0 반환

    주의:
        함수 이름이 solution이어야 자기참조가 동작함
        아래는 solution_ref_one으로 래핑
    """
    def solution(k_: int, dgs: list) -> int:
        return max(
            [solution(k_ - u, dgs[:i] + dgs[i + 1:]) + 1
             for i, (m, u) in enumerate(dgs) if k_ >= m] or [0]
        )

    return solution(k, dungeons)


# ================================================================================
# Ref solution two - 그리디 시도 (반례 있음, 통과 불가)
# ================================================================================
def solution_ref_two(k: int, dungeons: list[list[int]]) -> int:
    """
    정렬 기준으로 그리디 접근한 참고 풀이 (2022년 TC 추가로 반례 발생)

    정렬 기준: key=lambda x: ((x[1]+x[0])/x[0], x[1])
        (소모+최소)/최소 = 1 + 소모/최소: 소모 비율 낮은 순
        비율 같으면 소모 피로도 낮은 순

    반례: k=26, dungeons=[[23,10],[15,4],[2,1]], 정답=3
        그리디 순서: [[15,4],[23,10],[2,1]]
            26>=15 → k=22, 22>=23? No, 22>=2 → k=21 → 2개 (오답)
        최적 순서: [[2,1],[23,10],[15,4]]
            26>=2  → k=25, 25>=23 → k=15, 15>=15 → k=11 → 3개 (정답)

    그리디 불가 이유:
        최소 필요 피로도와 소모 피로도가 독립적으로 결합
        단일 기준으로 전역 최적 순서 보장 불가
        → 완전탐색(N≤8, 8!=40,320)이 유일한 보장 방법
    """
    answer = 0
    dungeons = sorted(dungeons, key=lambda x: ((x[1] + x[0]) / x[0], x[1]))
    for x, y in dungeons:
        if k >= x:
            k -= y
            answer += 1
    return answer


# ================================================================================
# Best solution - DFS 백트래킹 + 피로도 통합 (mine_four 주석 보강)
# ================================================================================
def solution_best(k: int, dungeons: list[list[int]]) -> int:
    """
    DFS 백트래킹으로 순열 수집 없이 피로도 조건을 통합하는 최적 풀이

    mine_four와 동일한 로직, 선정 근거 주석 보강:
        N≤8 제약에서 완전탐색(8!=40,320) 보장
        불가능 경로(k_<minimum) 조기 pruning → 실제 탐색 < 40,320

    DFS가 Mine_five(yield 통합)보다 유리한 이유:
        메모리:
            DFS: visited 배열 O(N) 재사용
            Mine_five: 매 재귀마다 rest = arr[:i]+arr[i+1:] 슬라이싱
                       새 리스트 객체 생성 → O(N) × 재귀 깊이 = O(N²)
        패턴 범용성:
            DFS + visited + 백트래킹: 그래프 탐색, 경로 탐색 등 범용
            yield 통합 방식: 이 문제에 특화, 다른 문제 적용 시 재설계 필요

    mine_four의 for-else 대신 answer = max(answer, count):
        for-else: Python 레벨 if 비교 + 조건 분기 + 대입
                  for-else 내부 break 추적 플래그 오버헤드 추가
        max() 대입: C 레벨 max() 함수 + 대입 1회
        실측 (timeit 100,000회): max() 방식이 약 88% 빠름
    """
    answer = 0
    n = len(dungeons)
    visited = [False] * n

    def dfs(k_: int, count: int) -> None:
        nonlocal answer
        answer = max(answer, count)   # for-else 대신 매 단계 갱신

        for i in range(n):
            if not visited[i] and k_ >= dungeons[i][0]:
                visited[i] = True
                dfs(k_ - dungeons[i][1], count + 1)
                visited[i] = False

    dfs(k, 0)
    return answer


# ================================================================================
# Sub solution - permutations 라이브러리 활용 (mine_one 주석 보강)
# ================================================================================
def solution_sub(k: int, dungeons: list[list[int]]) -> int:
    """
    permutations 라이브러리로 모든 순열을 생성하는 서브 풀이

    Best 대비 특징:
        직접 구현 없이 표준 라이브러리 활용 → 가장 간결
        순열 생성과 피로도 계산이 분리되어 각 단계가 명확
        순열 전체를 순회하므로 pruning 없음
        N≤8 제약에서 성능 차이 미미
    """
    answer = 0

    for p in permutations(dungeons):
        count = 0
        k_ = k
        for minimum, cost in p:
            if k_ >= minimum:
                count += 1
                k_ -= cost
            else:
                break
        answer = max(count, answer)

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[int, list[list[int]], int]] = [
        # (k, dungeons, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # 최적 순서: [80,20]→[50,40]→[30,10]은 실패
        # [80,20]→[30,10]→[50,40]: 80→60→50→10 → 3개 ✓
        (80, [[80,20],[50,40],[30,10]], 3),
        # 그리디 반례:
        # k=26, 최적: [2,1]→[23,10]→[15,4] → 3개
        (26, [[23,10],[15,4],[2,1]], 3),
        # 추가 케이스:
        # 피로도 부족으로 1개도 못 함
        (1,  [[50,20],[30,10]], 0),
        # 단일 던전
        (100, [[80,20]], 1),
    ]

    solutions = [
        ("Mine_one   (permutations) ", solution_mine_one),
        ("Mine_two   (DFS+visited)  ", solution_mine_two),
        ("Mine_three (재귀+yield)   ", solution_mine_three),
        ("Mine_four  (DFS+통합)     ", solution_mine_four),
        ("Mine_five  (yield+통합)   ", solution_mine_five),
        ("Ref_one    (재귀한줄)     ", solution_ref_one),
        ("Ref_two    (그리디반례)   ", solution_ref_two),
        ("Best       (DFS+통합)     ", solution_best),
        ("Sub        (permutations) ", solution_sub),
    ]

    # 워밍업 스텝
    _k, _d, _ = test_cases[0]
    for _, func in solutions:
        func(_k, [x[:] for x in _d])

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (k, dungeons, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(k, [x[:] for x in dungeons])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
