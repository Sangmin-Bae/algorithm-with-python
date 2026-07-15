"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : H-Index
    유형       : Sort
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42747
    풀이일자   : 2026-07-10
================================================================================
[문제 요약]
    논문 n편 중 h번 이상 인용된 논문이 h편 이상이고
    나머지 논문이 h번 이하 인용되었을 때 h의 최댓값 반환

    제약 조건
        - 논문 수: 1 이상 1,000 이하
        - 인용 횟수: 0 이상 10,000 이하
================================================================================
[입출력 예시]
    citations       | return
    ----------------|-------
    [3, 0, 6, 1, 5] | 3
================================================================================
[핵심 관찰 — 내림차순 정렬 후 편수와 인용횟수 비교]
    내림차순 정렬: [6, 5, 3, 1, 0]
    인덱스 i의 의미: i+1번째까지 논문을 선택했을 때 선택된 논문 수 = i+1

    비교 조건: desc[i] >= i+1
        내림차순이므로 0~i 인덱스 논문 모두 desc[i] 이상 보장
        → i+1편의 논문이 모두 i+1회 이상 인용됨 = H-Index 조건 충족

    손 추적 ([3,0,6,1,5]):
        정렬: [6,5,3,1,0]
        i=0: 6 >= 1 → h=1
        i=1: 5 >= 2 → h=2
        i=2: 3 >= 3 → h=3 ✓
        i=3: 1 < 4  → break → return 3

[Ref_one 수식 분석 — max(map(min, enumerate(citations, start=1)))]
    내림차순 정렬 후:
        enumerate(citations, start=1): (편수, 인용횟수) 쌍 생성
            (1,6), (2,5), (3,3), (4,1), (5,0)

        map(min, ...): 각 쌍에서 min 취함
            min(1,6)=1, min(2,5)=2, min(3,3)=3, min(4,1)=1, min(5,0)=0

        max(...) = 3

    min(편수, 인용횟수)의 의미:
        편수 < 인용횟수: 편수가 h의 상한 (편수가 부족)
        편수 > 인용횟수: 인용횟수가 h의 상한 (인용이 부족)
        편수 = 인용횟수: 정확히 h 성립
        → 각 위치에서 보장 가능한 h의 최대치
        max로 이 중 최댓값 선택 = H-Index

[Ref_two default return 0의 의미]
    오름차순 정렬 후 l-i가 h 후보:
        i에서 l-i는 "i번째 논문 포함 이후 논문 수"

    return 0 케이스: 모든 논문 인용횟수가 0일 때
        citations = [0, 0, 0]
        i=0: 0 >= 3? No
        i=1: 0 >= 2? No
        i=2: 0 >= 1? No
        → for 루프 종료 → return 0 (h=0이 맞음)

    solution_two return len(desc_citations) 케이스와 대비:
        solution_two: 모든 인용횟수 >= 편수인 최적 케이스 처리
            [99,98,97]: for 루프 break 없이 끝 → return 3
        solution_ref_two: 모든 인용횟수 = 0인 최악 케이스 처리
            [0,0,0]: for 루프 탈출 조건 없음 → return 0
================================================================================
[내 초기 풀이]
    solution_mine_one  : 내림차순 정렬 + h_index 갱신 + break
    solution_mine_two  : 내림차순 정렬 + 조기 탈출 (조건 반전)
    solution_mine_three: 정렬 없이 O(N²) 완전탐색 (학습 목적)

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
        h_index 변수를 갱신하며 전체 조건이 코드에 명시적으로 드러남
    solution_mine_two  : 개선 필요 없음 - Best
        조건 반전 + 조기 탈출로 break 없이 간결하게 표현
        default return len(desc_citations): 모든 논문 인용횟수 >= 편수 케이스
    solution_mine_three: 정렬 없이 구현 가능함을 확인하는 학습용
                         O(N²) → 대규모에서 비효율
================================================================================
[복잡도 분석]
    N = len(citations) (최대 1,000)

    Mine_one   - 시간: O(N log N) | 공간: O(N) - sorted + 단일 순회
    Mine_two   - 시간: O(N log N) | 공간: O(N) - sorted + 조기 탈출 순회
    Mine_three - 시간: O(N²)      | 공간: O(1) - 이중 순회 (정렬 없음)
    Ref_one    - 시간: O(N log N) | 공간: O(N) - sorted + enumerate + map
    Ref_two    - 시간: O(N log N) | 공간: O(N) - sorted + 오름차순 순회
    Best       - 시간: O(N log N) | 공간: O(N) - Mine_two와 동일
    Sub        - 시간: O(N log N) | 공간: O(N) - Mine_one과 동일
"""

import time


# ================================================================================
# Mine solution one - 내림차순 정렬 + h_index 갱신 + break
# ================================================================================
def solution_mine_one(citations: list[int]) -> int:
    """
    내림차순 정렬 후 h_index를 갱신하며 조건 불만족 시 break하는 초기 풀이

    핵심:
        desc[i] >= i+1: i+1편의 논문이 모두 i+1회 이상 인용 → h=i+1 가능
        desc[i] < i+1:  이미 1편 탈락 → 이후는 조건 충족 불가 → break
        h_index: 조건 만족하는 최댓값을 순회하며 갱신

    break 이유:
        내림차순 정렬이므로 한 번 조건 불만족이면 이후 모든 위치도 불만족
        (편수 i+1은 증가, 인용횟수 desc[i]는 감소 또는 동일)
    """
    h_index = 0
    desc_citations = sorted(citations, reverse=True)

    for i in range(len(desc_citations)):
        if desc_citations[i] >= i + 1:
            h_index = i + 1             # 조건 만족 → h 갱신
        else:
            break                       # 이후 조건 불만족 확정 → 탈출

    return h_index


# ================================================================================
# Mine solution two - 내림차순 정렬 + 조기 탈출 (조건 반전)
# ================================================================================
def solution_mine_two(citations: list[int]) -> int:
    """
    mine_one의 if-else를 반전 조건으로 전환해 조기 탈출하는 풀이

    mine_one 대비:
        h_index 변수 제거 → 조기 탈출 시 i를 직접 반환
        조건 반전: desc[i] >= i+1(mine_one) → desc[i] < i+1(mine_two)
        조기 탈출 시 이전까지 유효한 h = i (현재 인덱스 i, 편수 i+1에서 실패)

    default return len(desc_citations):
        for 루프가 break 없이 끝 = 모든 논문이 편수 이상 인용
        예) [99,98,97]: 모든 desc[i] >= i+1 → return 3 = len
    """
    desc_citations = sorted(citations, reverse=True)

    for i in range(len(desc_citations)):
        if desc_citations[i] < i + 1:  # 조건 불만족 → 이전까지 h = i
            return i

    return len(desc_citations)          # 모든 논문 인용횟수 >= 편수 케이스


# ================================================================================
# Mine solution three - 정렬 없이 O(N²) 완전탐색 (학습 목적)
# ================================================================================
def solution_mine_three(citations: list[int]) -> int:
    """
    정렬 없이 h 후보를 역방향으로 탐색하는 학습 목적 풀이

    핵심:
        range(len(citations), -1, -1): h 후보를 최댓값부터 감소하며 탐색
        sum(1 for x in citations if x >= i): i회 이상 인용된 논문 수 직접 계산
        조건 만족 첫 번째 i가 h의 최댓값 → 즉시 반환

    정렬 없이 동작 가능하나:
        각 h 후보마다 전체 citations 순회 O(N)
        전체 O(N²) → 정렬 방식 O(N log N) 대비 비효율
        N=1,000에서 약 1,000,000 연산
    """
    for i in range(len(citations), -1, -1):
        if sum(1 for x in citations if x >= i) >= i:
            return i

    return len(citations)


# ================================================================================
# Ref solution one - max(map(min, enumerate(citations, start=1)))
# ================================================================================
def solution_ref_one(citations: list[int]) -> int:
    """
    enumerate + min + max를 조합해 한 줄에 H-Index를 구하는 참고 풀이

    동작 원리:
        내림차순 정렬 후 enumerate(start=1) → (편수, 인용횟수) 쌍
        min(편수, 인용횟수): 해당 위치에서 보장 가능한 h의 최대치
            편수 < 인용횟수: 편수가 h 상한 (편수 부족)
            편수 > 인용횟수: 인용횟수가 h 상한 (인용 부족)
            편수 = 인용횟수: 정확히 h 성립
        max(...): 모든 위치 중 최대 h값 선택 = H-Index

    손 추적 ([3,0,6,1,5]):
        정렬: [6,5,3,1,0]
        (1,6)→min=1, (2,5)→min=2, (3,3)→min=3, (4,1)→min=1, (5,0)→min=0
        max(1,2,3,1,0) = 3 ✓

    간결하지만 min/max 의미 파악이 어려워 가독성 낮음
    """
    citations.sort(reverse=True)
    return max(map(min, enumerate(citations, start=1)))


# ================================================================================
# Ref solution two - 오름차순 정렬 + l-i 비교 + return 0
# ================================================================================
def solution_ref_two(citations: list[int]) -> int:
    """
    오름차순 정렬 후 l-i(이후 논문 수)와 비교하는 참고 풀이

    핵심:
        오름차순 정렬: 현재 위치가 h 조건 만족하면 뒤는 모두 만족 보장
        l-i: i번째 논문 포함 이후 논문 수 (h 후보)
        citations[i] >= l-i: i 이후 모든 논문이 l-i회 이상 인용 → h=l-i

    손 추적 ([3,0,6,1,5]):
        정렬: [0,1,3,5,6], l=5
        i=0: 0 >= 5? No
        i=1: 1 >= 4? No
        i=2: 3 >= 3? Yes → return 3 ✓

    return 0의 의미:
        모든 인용횟수가 0일 때 → for 루프 탈출 조건 없음 → return 0
        예) [0,0,0]: 0>=3? No, 0>=2? No, 0>=1? No → return 0 (h=0 정답)
        solution_two return len(...)과 대비:
            내림차순 최적 케이스 처리 vs 오름차순 최악 케이스 처리
    """
    citations = sorted(citations)
    l = len(citations)
    for i in range(l):
        if citations[i] >= l - i:
            return l - i
    return 0                            # 모든 인용횟수 = 0인 케이스


# ================================================================================
# Best solution - 내림차순 + 조기 탈출 (mine_two 주석 보강)
# ================================================================================
def solution_best(citations: list[int]) -> int:
    """
    내림차순 정렬 후 조건 불만족 시 즉시 반환하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        h_index 변수 없이 i를 직접 반환 → 간결
        desc[i] < i+1이면 이전까지 유효한 h = i → return i
        전체 순회 없이 조기 탈출 → 실질적으로 빠름
        default return: 모든 인용횟수가 편수 이상인 케이스 처리
    """
    desc_citations = sorted(citations, reverse=True)

    for i in range(len(desc_citations)):
        if desc_citations[i] < i + 1:
            return i

    return len(desc_citations)


# ================================================================================
# Sub solution - 내림차순 + h_index 갱신 (mine_one 주석 보강)
# ================================================================================
def solution_sub(citations: list[int]) -> int:
    """
    h_index를 갱신하며 전체 동작 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        h_index 변수로 "현재까지 가장 큰 h"를 명시적으로 추적
        desc[i] >= i+1 조건과 h = i+1의 관계가 코드에 직접 드러남
        break 후에도 h_index에 최댓값이 보존됨
        H-Index 정의를 코드로 직접 표현하는 학습 목적에 적합
    """
    h_index = 0
    desc_citations = sorted(citations, reverse=True)

    for i in range(len(desc_citations)):
        if desc_citations[i] >= i + 1:
            h_index = i + 1
        else:
            break

    return h_index


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], int]] = [
        # (citations, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [3,0,6,1,5] → 정렬: [6,5,3,1,0]
        # i=0: 6>=1✓ h=1, i=1: 5>=2✓ h=2, i=2: 3>=3✓ h=3
        # i=3: 1<4 → break → return 3
        ([3, 0, 6, 1, 5], 3),
        # 추가 케이스:
        # 모든 인용횟수 > 편수: return len
        # [99,98,97] → 정렬: [99,98,97]
        # i=0: 99>=1✓, i=1: 98>=2✓, i=2: 97>=3✓ → return 3
        ([99, 98, 97], 3),
        # 모든 인용횟수 = 0: h=0
        ([0, 0, 0], 0),
        # 단일 논문 인용 없음
        ([0], 0),
        # 단일 논문 인용 있음
        ([5], 1),
        # 동점 케이스
        # [3,3,3] → 정렬: [3,3,3]
        # i=0: 3>=1✓, i=1: 3>=2✓, i=2: 3>=3✓ → return 3
        ([3, 3, 3], 3),
    ]

    solutions = [
        ("Mine_one   (갱신+break)  ", solution_mine_one),
        ("Mine_two   (반전+조기탈출)", solution_mine_two),
        ("Mine_three (O(N²)정렬없음)", solution_mine_three),
        ("Ref_one    (min+max)     ", solution_ref_one),
        ("Ref_two    (오름차순)    ", solution_ref_two),
        ("Best       (반전+조기탈출)", solution_best),
        ("Sub        (갱신+break)  ", solution_sub),
    ]

    # 워밍업 스텝
    _c, _ = test_cases[0]
    for _, func in solutions:
        func(_c[:])

    print("=" * 68)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (citations, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(citations[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
