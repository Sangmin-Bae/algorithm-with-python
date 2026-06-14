"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 모의고사
    유형       : 완전탐색 (Brute Force)
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42840
    풀이일자   : 2026-06-14
===================================================================================
[문제 요약]
    수포자 3명의 고정 패턴과 정답 배열 answers가 주어질 때
    가장 많은 문제를 맞힌 수포자 번호를 오름차순으로 반환

    수포자 패턴:
        1번: [1,2,3,4,5] 반복
        2번: [2,1,2,3,2,4,2,5] 반복
        3번: [3,3,1,1,2,2,4,4,5,5] 반복

    제약 조건
        - answers 길이: 1 이상 10,000 이하
        - 정답: 1~5 중 하나
        - 최고 점수 동점자 여럿이면 오름차순 반환
===================================================================================
[입출력 예시]
    answers     | return
    ------------|-------
    [1,2,3,4,5] | [1]     (수포자1 전부 맞힘, 2,3번 전부 틀림)
    [1,3,2,4,2] | [1,2,3] (모두 2문제씩 맞힘)
===================================================================================
[완전탐색(Brute Force) 개념]
    가능한 모든 경우의 수를 빠짐없이 탐색해서 답을 찾는 방식
    핵심 철학: "최적 경로를 추론하지 않는다. 전부 다 해본다."

    이 문제에서의 완전탐색:
        수포자 1의 패턴으로 answers 전체 비교 → 점수 계산
        수포자 2의 패턴으로 answers 전체 비교 → 점수 계산
        수포자 3의 패턴으로 answers 전체 비교 → 점수 계산
        → 3가지 경우를 전부 탐색

    완전탐색이 유효한 조건:
        탐색 공간이 충분히 작을 때
        이 문제: 수포자 3명(고정) × answers 10,000 → 30,000번 연산

    완전탐색 대표 유형:
        단순 반복  : 모든 원소/경우를 순회 (이 문제)
        순열/조합  : 모든 순서/선택 조합을 열거
        BFS/DFS   : 모든 경로를 탐색
        백트래킹   : 완전탐색 + 불필요한 분기 조기 종료
===================================================================================
[내 초기 풀이]
    solution_mine_one: idx % len(p) 나머지 연산으로 패턴 반복, set으로 중복 확인
        answers 전체 순회하며 p[idx % len(p)]로 패턴 순환 접근
        중복 확인: len(score) == len(set(score)) → "모든 점수가 다른가" 간접 확인

    solution_mine_two: 슬라이싱 + zip으로 패턴 길이만큼 끊어 비교, count로 중복 확인
        answers를 p 길이(l)만큼 슬라이싱해서 zip으로 쌍 비교
        슬라이싱: answers 길이가 p 길이의 배수 아니어도 out of range 없음
        zip: 두 리스트 길이 달라도 짧은 쪽 기준으로 나머지 버림
        중복 확인: score.count(max_score) == 1 → 의도를 직접 표현

[개선 포인트]
    solution_mine_one:
        len(score) == len(set(score)): "모든 점수가 다른가"를 간접 확인
            → score.count(max_score) == 1이 "최고 점수가 1개인가"를 직접 표현
            → Best에서 count 방식으로 교체
    solution_mine_two: 개선 필요 없음 - Sub
===================================================================================
[중복 확인 방식 비교]
    len(score) == len(set(score)):
        set 변환으로 중복 제거 후 개수 비교
        "모든 점수가 다른가"를 확인 → 최고 점수 1명을 간접 표현
        score = [5,3,4]: len=3, set len=3 → 같음 → 단독 1명 ✓
        score = [5,5,3]: len=3, set len=2 → 다름 → 동점자 존재 ✓
        공간: set 객체 생성 O(N)

    score.count(max_score) == 1:
        최고 점수 개수를 직접 확인
        "최고 점수가 정확히 1개인가"를 직접 표현 → 의도 명확
        시간: O(N) 순회, 공간: O(1)
        → 이 문제 목적에 더 직접적인 방식

    sorted(i+1 for i, c in enumerate(score) if c == max_score):
        제너레이터 표현식을 sorted()에 직접 전달
        중간 리스트 객체 생성 없음 → 메모리 효율적
        sorted()는 이터러블을 직접 받아 정렬된 리스트 반환
===================================================================================
[복잡도 분석]
    N = len(answers) (최대 10,000)
    P = 수포자 수 = 3 (상수)
    L = 패턴 최대 길이 = 10 (상수)

    Mine_one - 시간: O(P × N)     | 공간: O(P) - 패턴별 N번 순회
    Mine_two - 시간: O(P × N)     | 공간: O(L) - 슬라이싱 L개 리스트 생성
    Best     - 시간: O(P × N)     | 공간: O(P) - Mine_one + count 방식 교체
    Sub      - 시간: O(P × N)     | 공간: O(L) - Mine_two와 동일

    P=3, L=10 상수 → 사실상 O(N)
    N=10,000: 최대 30,000번 연산 → 완전탐색으로 충분
"""

import time
from typing import List, Tuple


# =================================================================================
# Mine solution one - idx % len(p) 나머지 연산 + set 중복 확인
# =================================================================================
def solution_mine_one(answers: List[int]) -> List[int]:
    """
    나머지 연산으로 패턴을 순환하며 점수를 계산하는 초기 풀이

    핵심:
        p[idx % len(p)]: idx가 p 길이를 넘어도 나머지 연산으로 순환 접근
        enumerate(answers): 인덱스와 정답을 동시에 순회
        len(score) == len(set(score)): 모든 점수가 다른지 확인 (간접 중복 확인)

    개선 가능:
        len(score) == len(set(score)) → score.count(max_score) == 1
        최고 점수가 1개인지 직접 확인하는 방식이 의도를 명확히 표현
    """
    pattern = (
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    )

    score = []
    for p in pattern:
        c = 0
        for idx, q in enumerate(answers):
            if q == p[idx % len(p)]:    # 나머지 연산으로 패턴 순환 접근
                c += 1
        score.append(c)

    max_score = max(score)
    if len(score) == len(set(score)):   # 모든 점수가 다름 → 최고 점수 1명
        return [score.index(max_score) + 1]
    else:
        return sorted(i + 1 for i, c in enumerate(score) if c == max_score)


# =================================================================================
# Mine solution two - 슬라이싱 + zip + count 중복 확인
# =================================================================================
def solution_mine_two(answers: List[int]) -> List[int]:
    """
    슬라이싱 + zip으로 패턴 길이만큼 끊어 비교하는 풀이

    핵심:
        answers[i:i+l]: p 길이만큼 슬라이싱
            answers 길이가 l의 배수 아니어도 out of range 없음 (슬라이싱 특성)
        zip(p, answers[i:i+l]): 짧은 쪽 기준 쌍 생성, 나머지 버림 (zip 특성)
        sum(a == b for a, b in zip(...)): bool 합산으로 일치 개수 계산
        score.count(max_score) == 1: 최고 점수가 1개인지 직접 확인

    sorted()에 제너레이터 직접 전달:
        sorted(i+1 for ...): 중간 리스트 객체 생성 없이 이터러블 직접 전달
    """
    pattern = (
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    )

    score = []
    for p in pattern:
        c = 0
        l = len(p)
        for i in range(0, len(answers), l):
            c += sum(a == b for a, b in zip(p, answers[i:i + l]))  # bool 합산
        score.append(c)

    max_score = max(score)
    if score.count(max_score) == 1:     # 최고 점수가 1개 → 단독 1명
        return [score.index(max_score) + 1]
    else:
        return sorted(i + 1 for i, c in enumerate(score) if c == max_score)


# =================================================================================
# Best solution - 나머지 연산 + count 중복 확인 (Mine_one 개선)
# =================================================================================
def solution_best(answers: List[int]) -> List[int]:
    """
    나머지 연산 순환 + count로 최고 점수 단독 여부를 직접 확인하는 최적 풀이

    Mine_one 대비 개선:
        len(score) == len(set(score)) → score.count(max_score) == 1
        "모든 점수가 다른가(간접)" → "최고 점수가 1개인가(직접)"
        set 객체 생성 O(N) 공간 → O(1) 공간

    나머지 연산 순환이 슬라이싱+zip 대비 유리한 이유:
        answers를 1회 순회하며 p[idx % len(p)]로 직접 접근
        슬라이싱은 매 청크마다 새 리스트 객체 생성 → 추가 공간 비용
    """
    pattern = (
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    )

    score = []
    for p in pattern:
        c = 0
        for idx, q in enumerate(answers):
            if q == p[idx % len(p)]:    # 나머지 연산으로 패턴 순환
                c += 1
        score.append(c)

    max_score = max(score)
    if score.count(max_score) == 1:     # 최고 점수가 정확히 1개 → 단독
        return [score.index(max_score) + 1]
    else:                               # 동점자 존재 → 오름차순 반환
        return sorted(i + 1 for i, c in enumerate(score) if c == max_score)


# =================================================================================
# Sub solution - 슬라이싱 + zip (Mine_two 주석 보강)
# =================================================================================
def solution_sub(answers: List[int]) -> List[int]:
    """
    슬라이싱 + zip으로 패턴 길이만큼 끊어 비교하는 서브 풀이

    Best 대비 특징:
        answers를 p 길이(l) 단위로 청크로 나눠 비교
        슬라이싱: answers[i:i+l] — 범위 초과 시 가능한 원소까지만 반환 (out of range 없음)
        zip: 두 시퀀스 중 짧은 쪽 기준으로 쌍 생성, 나머지 원소 버림
            → answers 길이가 l의 배수 아니어도 정확히 동작

        슬라이싱이 매 청크마다 새 리스트 객체 생성 → Best 대비 공간 비용 있음
        패턴 단위로 비교하는 구조가 직관적으로 드러남
    """
    pattern = (
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    )

    score = []
    for p in pattern:
        c = 0
        l = len(p)
        for i in range(0, len(answers), l):
            c += sum(a == b for a, b in zip(p, answers[i:i + l]))
        score.append(c)

    max_score = max(score)
    if score.count(max_score) == 1:
        return [score.index(max_score) + 1]
    else:
        return sorted(i + 1 for i, c in enumerate(score) if c == max_score)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[List[int], List[int]]] = [
        # (answers, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [1,2,3,4,5]:
        #   수포자1: p=[1,2,3,4,5], 모두 일치 → 5점
        #   수포자2: p[0]=2≠1, p[1]=1≠2, p[2]=2≠3, p[3]=3≠4, p[4]=2≠5 → 0점
        #   수포자3: p[0]=3≠1, p[1]=3≠2, p[2]=1≠3, p[3]=1≠4, p[4]=2≠5 → 0점
        #   최고=5, 단독 1번 → [1]
        ([1, 2, 3, 4, 5],   [1]),
        # [1,3,2,4,2]:
        #   수포자1: 1=1✓, 3≠2, 2≠3, 4=4✓, 2≠5 → 2점
        #   수포자2: p[0%8]=2≠1, p[1%8]=1≠3, p[2%8]=2=2✓, p[3%8]=3≠4, p[4%8]=2=2✓ → 2점
        #   수포자3: p[0%10]=3≠1, p[1%10]=3=3✓, p[2%10]=1≠2, p[3%10]=1≠4, p[4%10]=2=2✓ → 2점
        #   모두 2점 동점 → [1,2,3]
        ([1, 3, 2, 4, 2],   [1, 2, 3]),
        # 추가 케이스:
        # [2,1,2,3,2,4,2,5]: 수포자2 패턴과 완전 일치
        #   수포자1: 2≠1, 1≠2, 2≠3, 3≠4, 2≠5, → ...  → 점수 낮음
        #   수포자2: 전부 일치 → 8점
        #   수포자3: 점수 낮음
        ([2, 1, 2, 3, 2, 4, 2, 5], [2]),
    ]

    solutions = [
        ("Mine_one (나머지+set)  ", solution_mine_one),
        ("Mine_two (슬라이싱+zip)", solution_mine_two),
        ("Best     (나머지+count)", solution_best),
        ("Sub      (슬라이싱+zip)", solution_sub),
    ]

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (answers, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(answers[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
