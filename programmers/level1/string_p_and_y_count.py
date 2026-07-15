"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 문자열 내 p와 y의 개수
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12916
    풀이일자   : 2026-06-07
===================================================================================
[문제 요약]
    문자열 s에서 'p'와 'y'의 개수가 같으면 True, 다르면 False 반환
    대소문자 구분 없음 ('P'와 'p' 동일 취급)
    'p'와 'y' 모두 0개이면 True (개수가 같으므로)

    제약 조건
        - s 길이: 50 이하의 자연수 -> N이 사실상 상수, 모든 풀이 O(1) 수렴
        - s는 알파벳으로만 구성
===================================================================================
[입출력 예시]
    s         | return
    ----------|-------
    "pPoooyY" | True  (p:2, y:2 -> 같음)
    "Pyy"     | False (p:1, y:2 -> 다름)
===================================================================================
[내 초기 풀이]
    solution_mine_one: s.lower() 후 count('p') == count('y') 비교
        초기 시도: return True if s.lower().count('p') == s.lower().count('y') else False
        개선 1: s.lower() 중복 호출 -> l_s 변수로 1회 저장
        개선 2: 삼항 연산자 제거 -> '==' 비교 연산자 자체가 bool 반환

    solution_mine_two: Counter(s.lower())로 빈도 집계 후 'p', 'y' key 비교
        Counter 객체가 {문자: 개수} 딕셔너리를 반환하므로
        table['p'] == table['y']로 직접 비교

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
    solution_mine_two: 비교 문자가 2개뿐인 이 문제에서는 Counter가 오버스펙
                        단, 비교 문자가 늘어나는 경우 Counter 재사용으로 확장성 우위
===================================================================================
[Counter 공간 오버헤드 분석]
    solution_mine_one:
        l_s = s.lower()   -> 길이 N의 새 문자열 객체 1개 -> O(N)
        count() 자체      -> 추가 자료구조 없음 -> O(1)
        전체              -> O(N)

    solution_mine_two:
        s.lower()         -> 길이 N의 새 문자열 객체 1개 -> O(N)
        Counter(...)      -> 고유 문자 수 K개의 딕셔너리 -> O(K)
        전체              -> O(N + K)

    K = 고유 문자 수 (영소문자만 입력 시 최대 26, 사실상 상수)
    Python Counter 객체 기본 메모리: 약 200~240 bytes (해시 테이블 버킷 구조)
    -> N <= 50 고정인 이 문제에서는 Counter 쪽 고정 오버헤드가 상대적으로 더 큼
===================================================================================
[복잡도 분석]
    N = len(s) (최대 50, 사실상 상수)
    K = 고유 문자 수 (최대 26, 상수)

    Mine_one - 시간: O(N)     | 공간: O(N)     - lower() 문자열 + count() 2회 순회
    Mine_two - 시간: O(N)     | 공간: O(N + K) - lower() 문자열 + Counter 딕셔너리
    Best     - 시간: O(N)     | 공간: O(N)     - Mine_one과 동일
    Sub      - 시간: O(N)     | 공간: O(N + K) - Mine_two와 동일

    N <= 50 고정 -> 모든 풀이 실질적으로 O(1)에 수렴
    단, Counter의 고정 오버헤드(200~240 bytes)는 N이 작을수록 상대적으로 큼
"""

import time
from collections import Counter
from typing import List, Tuple


# =================================================================================
# Mine solution one - lower() + count() 2회
# =================================================================================
def solution_mine_one(s: str) -> bool:
    """
    s를 소문자화한 뒤 count()로 'p'와 'y' 개수를 비교하는 초기 풀이

    발상 진화:
        1단계: return True if s.lower().count('p') == s.lower().count('y') else False
                -> s.lower() 중복 호출 비효율
        2단계: l_s = s.lower()으로 1회 저장해 중복 제거
                -> 삼항 연산자도 '==' 비교만으로 bool 반환 가능해 제거

    count() 동작:
        문자열을 처음부터 끝까지 순회하며 일치 횟수 집계 O(N)
        'p', 'y' 각각 1회씩 -> 2회 순회 발생
    """
    l_s = s.lower()                         # 대소문자 통일: 1회만 호출
    return l_s.count('p') == l_s.count('y') # '==' 자체가 bool 반환 -> 삼항 연산자 불필요


# =================================================================================
# Mine solution two - Counter로 빈도 집계 후 key 비교
# =================================================================================
def solution_mine_two(s: str) -> bool:
    """
    Counter로 문자열 빈도를 1회 집계한 뒤 'p', 'y' key로 비교하는 풀이

    Counter 동작:
        문자열을 1회 순회해 {문자: 개수} 딕셔너리 생성
        table['p'], table['y']: O(1) 해시 탐색

    Mine_one 대비 특징:
        문자열 순회 횟수: 2회 -> 1회
        대신 딕셔너리 객체 생성 오버헤드(약 200~240 bytes) 발생
        비교 문자가 늘어날 때 Counter 재사용으로 확장성 우위
    """
    table = Counter(s.lower())              # 1회 순회로 전체 문자 빈도 집계
    return table['p'] == table['y']         # Counter는 없는 key에 대해 0 반환


# =================================================================================
# Best solution - Mine_one (주석 보강)
# =================================================================================
def solution_best(s: str) -> bool:
    """
    소문자화 1회 + count() 2회로 직접 비교하는 최적 풀이

    Mine_one과 동일한 로직, 근거 주석 보강:
        - 비교 대상이 'p', 'y' 2개뿐 -> Counter 오버스펙
        - count()는 추가 자료구조 없이 O(N) 순회만으로 완료
        - Counter 고정 오버헤드(200~240 bytes) 없음

    Counter 미사용이 유리한 조건:
        비교 문자 수가 적고 (2개 이하)
        입력 크기가 작을 때 (N <= 50)
    """
    l_s = s.lower()                         # 대소문자 통일
    return l_s.count('p') == l_s.count('y') # p, y 개수 동일하면 True


# =================================================================================
# Sub solution - Counter (확장성 명시)
# =================================================================================
def solution_sub(s: str) -> bool:
    """
    Counter로 빈도 집계하는 풀이 (Mine_two와 동일, 확장성 관점 주석 보강)

    Best 대비 특징:
        문자열 순회 1회로 모든 문자 빈도 동시 집계
        비교 문자가 'p', 'y' 외에 추가될 경우 Counter 재사용 가능
            예) 'p', 'y', 'a' 개수가 모두 같아야 할 때:
                table['p'] == table['y'] == table['a'] 로 즉시 확장 가능
        Counter는 없는 key에 대해 기본값 0 반환 -> KeyError 없이 안전한 비교
    """
    table = Counter(s.lower())              # 1회 순회로 전체 문자 빈도 집계
    return table['p'] == table['y']         # 없는 key는 0 반환 -> 안전한 비교


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[str, bool]] = [
        # (s, 기댓값)
        # 손 추적:
        # "pPoooyY": lower -> "ppoooyyy" 아니라 "ppoooyyy" -> p:2, y:2 -> True
        ("pPoooyY", True),
        # "Pyy": lower -> "pyy" -> p:1, y:2 -> False
        ("Pyy",     False),
        # "p": lower -> "p" -> p:1, y:0 -> False
        ("p",       False),
        # "ab": lower -> "ab" -> p:0, y:0 -> True (둘 다 0)
        ("ab",      True),
        # "PpYy": lower -> "ppyy" -> p:2, y:2 -> True
        ("PpYy",    True),
        # "ppy": lower -> "ppy" -> p:2, y:1 -> False
        ("ppy",     False),
        # "Y": lower -> "y" -> p:0, y:1 -> False
        ("Y",       False),
    ]

    solutions = [
        ("Mine_one (lower+count×2)", solution_mine_one),
        ("Mine_two (Counter)      ", solution_mine_two),
        ("Best     (lower+count×2)", solution_best),
        ("Sub      (Counter)      ", solution_sub),
    ]

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
