"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 가장 가까운 같은 글자
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/142086
    풀이일자   : 2026-07-02
===================================================================================
[문제 요약]
    문자열 s의 각 위치에서 자신보다 앞에 나왔으면서 가장 가까운 같은 글자의
    거리를 반환. 없으면 -1

    제약 조건
        - s 길이: 1 이상 10,000 이하
        - 영어 소문자만 → 26가지 문자
===================================================================================
[입출력 예시]
    s        | result
    ---------|-----------------------
    "banana" | [-1, -1, -1, 2, 2, 2]
    "foobar" | [-1, -1, 1, -1, -1, -1]
===================================================================================
[내 초기 풀이]
    solution_mine_one  : rfind()로 역방향 탐색
    solution_mine_two  : reversed(list(enumerate(s[:idx]))) 역행 순회
    solution_mine_three: range(idx-1, -1, -1) 역행 인덱스 순회

    핵심 판단:
        find/rfind vs index/rindex:
            index/rindex: 문자 없으면 ValueError → 존재 여부 판별에 부적합
            find/rfind: 문자 없으면 -1 반환 → 문제 조건과 일치
        rfind가 find가 아닌 이유: 가장 가까운 = 뒤에서부터 탐색

[개선 포인트]
    solution_mine_one  :
        s[:idx] 슬라이싱 O(i) + rfind O(i) → 총 O(N²)
        rfind는 C 레벨 구현으로 Python 루프보다 빠르나 복잡도 자체는 O(N²)

    solution_mine_two  :
        s[:idx] 슬라이싱 O(i) + enumerate + list 변환 O(i) + reversed O(1)
        역행 탐색 전에 이미 O(N) 비용 두 번 발생
        Mine_one보다 오히려 느림

    solution_mine_three:
        s[rev_idx] 원본 직접 접근으로 슬라이싱 없음
        평균 O(i/2) 역행 루프, 총 O(N²)
        rfind() C 레벨 구현 대비 Python 루프라 상수 인자 큼

    → 세 풀이 모두 탐색 자체를 수행 → O(N²)
    → 해시(dict)로 마지막 등장 위치를 기록하면 탐색 O(1) → 전체 O(N)
===================================================================================
[풀이별 복잡도 비교]
    Mine_one   (rfind):      슬라이싱 O(i) + rfind O(i) × N번 = O(N²)
    Mine_two   (역행+list):  O(N) 전처리 × N번 = O(N²), Mine_one보다 오버헤드 큼
    Mine_three (역행 인덱스): 평균 O(i/2) × N번 = O(N²), C 레벨 아닌 Python 루프
    Best (hash):             dict O(1) 조회 × N번 = O(N)

    N=10,000:
        O(N²): 최대 1억 연산 → 시간 초과 가능성
        O(N):  1만 연산 → 여유롭게 통과
===================================================================================
[해시 방식 핵심 아이디어]
    "탐색하지 않고 기록한다"

    순회하면서 각 문자의 마지막 등장 인덱스를 dict에 O(1)로 저장/조회:
        c가 last_seen에 있으면 → 거리 = 현재 idx - last_seen[c]
        없으면 → -1
        순회 후 last_seen[c] = idx 갱신

    손 추적 ("banana"):
        idx=0, c='b': last_seen={} → -1, last_seen={'b':0}
        idx=1, c='a': 없음 → -1, last_seen={'b':0,'a':1}
        idx=2, c='n': 없음 → -1, last_seen={...,'n':2}
        idx=3, c='a': last_seen['a']=1 → 3-1=2, last_seen['a']=3
        idx=4, c='n': last_seen['n']=2 → 4-2=2, last_seen['n']=4
        idx=5, c='a': last_seen['a']=3 → 5-3=2, last_seen['a']=5
        → [-1,-1,-1,2,2,2] ✓
===================================================================================
[복잡도 분석]
    N = len(s) (최대 10,000)

    Mine_one   - 시간: O(N²) | 공간: O(N) - 슬라이싱 + rfind × N번
    Mine_two   - 시간: O(N²) | 공간: O(N) - O(N) 전처리 + 역행 × N번
    Mine_three - 시간: O(N²) | 공간: O(N) - Python 역행 루프 × N번
    Best       - 시간: O(N)  | 공간: O(1) - dict 26가지 문자 저장 (사실상 O(1))
    Sub        - 시간: O(N²) | 공간: O(N) - Mine_one과 동일, 주석 보강
"""

import time


# =================================================================================
# Mine solution one - rfind() 역방향 탐색
# =================================================================================
def solution_mine_one(s: str) -> list[int]:
    """
    s[:idx].rfind(c)로 가장 가까운 이전 동일 문자를 찾는 초기 풀이

    rfind 선택 이유:
        find: 앞에서부터 탐색 → 가장 가까운(=가장 뒤) 위치를 못 찾음
        rfind: 뒤에서부터 탐색 → 가장 가까운 이전 동일 문자 바로 탐색
        index/rindex 대신 find/rfind: 문자 없으면 ValueError 대신 -1 반환
            → -1이 문제 조건과 일치해 별도 예외 처리 불필요

    한계:
        s[:idx] 슬라이싱 O(i) + rfind O(i) × N번 → O(N²)
    """
    answer = []
    for idx, c in enumerate(s):
        nearest_idx = s[:idx].rfind(c)
        answer.append(idx - nearest_idx if nearest_idx != -1 else -1)
    return answer


# =================================================================================
# Mine solution two - reversed(list(enumerate(s[:idx]))) 역행 순회
# =================================================================================
def solution_mine_two(s: str) -> list[int]:
    """
    s[:idx]를 list로 변환 후 reversed로 역행 순회하는 풀이

    시도 이유:
        rfind의 전체 순회 O(N) 대신 역행 중 조기 탈출로 O(M<N) 기대

    실제 문제:
        s[:idx] O(i) + enumerate + list 변환 O(i) + reversed O(1)
        역행 탐색 전에 이미 O(N) 비용 두 번 발생
        → Mine_one보다 오버헤드가 커서 실제로 더 느림

    idx==0 예외 처리 필요:
        rfind()는 "".rfind(c) = -1로 자동 처리
        역행 루프는 s[:0]="" → for loop 미실행 → gap 미정의 → 명시적 처리 필요
    """
    answer = []
    for idx, c in enumerate(s):
        if idx == 0:
            answer.append(-1)
        else:
            for rev_idx, rev_c in reversed(list(enumerate(s[:idx]))):
                if c == rev_c:
                    gap = idx - rev_idx
                    break
                else:
                    gap = -1
            answer.append(gap)
    return answer


# =================================================================================
# Mine solution three - range(idx-1, -1, -1) 역행 인덱스 순회
# =================================================================================
def solution_mine_three(s: str) -> list[int]:
    """
    원본 문자열에 역행 인덱스로 직접 접근하는 풀이

    Mine_two 대비 개선:
        s[:idx] 슬라이싱 없음 → s[rev_idx] 원본 직접 접근
        역행 탐색 전처리 비용 절감 → Mine_one과 유사한 성능

    여전히 한계:
        Python 레벨 for 루프 → rfind() C 레벨 구현보다 상수 인자 큼
        최악의 경우 O(N²) 유지

    idx==0 예외 처리:
        Mine_two와 동일한 이유로 명시적 처리 필요
    """
    answer = []
    for idx, c in enumerate(s):
        if idx == 0:
            gap = -1
        else:
            for rev_idx in range(idx - 1, -1, -1):
                if c == s[rev_idx]:
                    gap = idx - rev_idx
                    break
                else:
                    gap = -1
        answer.append(gap)
    return answer


# =================================================================================
# Best solution - 해시(dict)로 마지막 등장 위치 기록
# =================================================================================
def solution_best(s: str) -> list[int]:
    """
    각 문자의 마지막 등장 인덱스를 dict에 O(1)로 기록/조회하는 최적 풀이

    핵심 아이디어: "탐색하지 않고 기록한다"
        탐색 방식: 현재 위치에서 뒤로 돌아가며 탐색 → O(N) × N번 = O(N²)
        기록 방식: 순회하며 마지막 위치를 갱신 → O(1) × N번 = O(N)

    last_seen[c] = idx:
        현재 c의 마지막 등장 위치를 갱신
        "직전 등장 위치"를 자동으로 유지

    공간복잡도 O(1):
        영소문자 26가지 → dict 최대 26개 항목 → 사실상 상수
    """
    answer = []
    last_seen: dict[str, int] = {}

    for idx, c in enumerate(s):
        if c in last_seen:
            answer.append(idx - last_seen[c])   # 거리 = 현재 - 마지막 위치
        else:
            answer.append(-1)
        last_seen[c] = idx                       # 현재 위치로 갱신

    return answer


# =================================================================================
# Sub solution - rfind() 방식 (mine_one 주석 보강)
# =================================================================================
def solution_sub(s: str) -> list[int]:
    """
    rfind()로 가장 가까운 이전 동일 문자를 찾는 서브 풀이

    Best 대비 특징:
        각 위치에서 "뒤에서부터 탐색"하는 의도가 코드에 직접 드러남
        rfind(): C 레벨 구현으로 Python 역행 루프보다 빠름
        O(N²) 복잡도 → N=10,000에서 Best(O(N)) 대비 성능 차이 발생

    find vs rfind 선택:
        find: 앞에서 첫 번째 → 가장 먼 위치, 문제 조건과 반대
        rfind: 뒤에서 첫 번째 → 가장 가까운 위치, 문제 조건과 일치
    """
    answer = []
    for idx, c in enumerate(s):
        nearest_idx = s[:idx].rfind(c)
        answer.append(idx - nearest_idx if nearest_idx != -1 else -1)
    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, list[int]]] = [
        # (s, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # "banana":
        #   b(0)→-1, a(1)→-1, n(2)→-1, a(3)→3-1=2, n(4)→4-2=2, a(5)→5-3=2
        ("banana", [-1, -1, -1, 2, 2, 2]),
        # "foobar":
        #   f(0)→-1, o(1)→-1, o(2)→2-1=1, b(3)→-1, a(4)→-1, r(5)→-1
        ("foobar", [-1, -1, 1, -1, -1, -1]),
        # 추가 케이스:
        # 단일 문자: "a" → [-1]
        ("a",      [-1]),
        # 모두 동일: "aaa" → [-1, 1, 1]
        ("aaa",    [-1, 1, 1]),
        # 연속 없는 반복: "abab" → [-1,-1,2,2]
        ("abab",   [-1, -1, 2, 2]),
    ]

    solutions = [
        ("Mine_one   (rfind)       ", solution_mine_one),
        ("Mine_two   (역행+list)   ", solution_mine_two),
        ("Mine_three (역행 인덱스) ", solution_mine_three),
        ("Best       (hash dict)   ", solution_best),
        ("Sub        (rfind)       ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 66)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
