"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : [1차] 뉴스 클러스터링
    유형       : Hash / String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/17677
    풀이일자   : 2026-08-19
================================================================================
[문제 요약]
    두 문자열의 자카드 유사도를 구해 65536을 곱한 정수부 반환
    다중집합: 2글자씩 끊어서 생성, 영문자 쌍만 유효, 대소문자 무시
    공집합이면 유사도 1 → 65536 반환

    제약 조건
        - str1, str2 길이: 2 이상 1,000 이하
================================================================================
[입출력 예시]
    str1       | str2        | answer
    -----------|-------------|-------
    "FRANCE"   | "french"    | 16384
    "handshake"| "shake hands"| 65536
    "aa1+aa2"  | "AAAA12"    | 43690
    "E=M*C^2"  | "e=m*c^2"   | 65536
================================================================================
[다중집합 교집합/합집합 공식]
    원소 e의 등장 횟수: freq1 (집합1), freq2 (집합2)

    교집합에서 e의 개수: min(freq1, freq2)
    합집합에서 e의 개수: max(freq1, freq2)

    지문 예시: A={1,1,2,2,3}, B={1,2,2,4,5}
        1: min(2,1)=1개(교), max(2,1)=2개(합)
        2: min(2,2)=2개(교), max(2,2)=2개(합)
        → 교집합={1,2,2}=3개, 합집합={1,1,2,2,3,4,5}=7개 ✓

[Counter |, & 연산]
    일반 dict |: 중복 키는 오른쪽 값으로 덮어씀 (다중집합 아님)
    Counter |:  다중집합 합집합 = max(freq1, freq2)
    Counter &:  다중집합 교집합 = min(freq1, freq2)
    → Counter가 dict를 상속받아 |, &를 다중집합 연산으로 오버라이딩

[ref_one set 접근 — 중복을 비중복으로 변환]
    "aa"가 3번 등장 → {"aa_1", "aa_2", "aa_3"}으로 변환
    중복 원소를 서로 다른 원소로 만들어 set 사용 가능

    set1 & set2: "aa_1"이 양쪽에 있으면 교집합 포함 = min 공식과 동치
    set1 | set2: 한쪽에만 있는 "aa_3"는 합집합에만 = max 공식과 동치

    실측에서 가장 느린 이유:
        f"{text}_{count_dict[text]}" 문자열 포맷팅 매 원소마다 발생
        Counter 연산보다 문자열 생성 비용이 무거움

[ref_two 정렬+포인터 — 병합 정렬 병합 단계와 동일]
    정렬된 두 리스트를 동시 순회하며:
        sub1[p1] == sub2[p2] → 교집합+1, 합집합+1, 양쪽 포인터 전진
        sub1[p1] < sub2[p2]  → 합집합+1, p1 전진 (sub1 원소가 더 작음)
        sub1[p1] > sub2[p2]  → 합집합+1, p2 전진 (sub2 원소가 더 작음)
    while 종료 후 남은 원소 → 합집합에만 추가

    손 추적 (FRANCE, french):
        sub1=["an","ce","fr","nc","ra"], sub2=["ch","en","fr","nc","re"]
        "fr"==>"fr" → 교집합+1, "nc"=="nc" → 교집합+1
        → 교집합=2, 합집합=8, 2/8×65536=16384 ✓

[실측 결과 — 긴 문자열, 10,000회]
    풀이2 (Counter):     0.210ms  ← 가장 빠름
    풀이1 (dict+min/max):0.222ms
    ref2  (정렬+포인터): 0.283ms  (O(N log N) vs Counter O(N))
    ref1  (set+접미사):  0.498ms  ← 가장 느림 (문자열 포맷팅 오버헤드)
================================================================================
[내 초기 풀이]
    solution_mine_one: 직접 dict + min/max 공식
    solution_mine_two: Counter + | & 연산자

[개선 포인트]
    solution_mine_one: all_elements 구성 시 리스트 in 연산 O(N) 사용
                       → set() | set()으로 O(1) 탐색으로 개선 후 Sub 선정
    solution_mine_two: 개선 필요 없음 - Best
                       Counter | & 연산으로 가장 간결하고 빠름
    solution_ref_one:  set 접근 독창적이나 문자열 포맷팅 오버헤드로 느림
    solution_ref_two:  정렬+포인터로 추가 자료구조 최소화 시도
                       O(N log N)로 Counter O(N)보다 느림
================================================================================
[복잡도 분석]
    N = len(str1) + len(str2) (최대 2,000)
    K = 고유 2글자 쌍 수 (최대 26×26 = 676)

    Mine_one - 시간: O(N+K) | 공간: O(K) - dict 집계 + min/max 순회
    Mine_two - 시간: O(N+K) | 공간: O(K) - Counter 집계 + | & 연산
    Ref_one  - 시간: O(N+K) | 공간: O(N) - set + 문자열 포맷팅
    Ref_two  - 시간: O(N log N) | 공간: O(N) - 정렬 + 포인터
    Best     - 시간: O(N+K) | 공간: O(K) - Mine_two와 동일
    Sub      - 시간: O(N+K) | 공간: O(K) - Mine_one과 동일
"""

from collections import Counter
import time


# ================================================================================
# Mine solution one - 직접 dict + min/max 공식
# ================================================================================
def solution_mine_one(str1: str, str2: str) -> int:
    """
    직접 dict로 빈도를 집계하고 min/max 공식으로 교집합/합집합을 구하는 초기 풀이

    다중집합 공식:
        교집합: min(freq1, freq2)
        합집합: max(freq1, freq2)

    all_elements 개선:
        list + in 연산(O(N)) → set | 연산(O(1))으로 교체
        두 dict의 키 합집합을 O(K)에 구성
    """
    s1, s2 = str1.lower(), str2.lower()
    sub1, sub2 = {}, {}

    for i in range(len(s1) - 1):
        text = s1[i:i + 2]
        if text.isalpha():
            sub1[text] = sub1.get(text, 0) + 1

    for i in range(len(s2) - 1):
        text = s2[i:i + 2]
        if text.isalpha():
            sub2[text] = sub2.get(text, 0) + 1

    all_elements = set(sub1.keys()) | set(sub2.keys())
    union_count = intersection_count = 0

    for key in all_elements:
        f1, f2 = sub1.get(key, 0), sub2.get(key, 0)
        union_count += max(f1, f2)
        intersection_count += min(f1, f2)

    if union_count == 0:
        return 65536

    return int((intersection_count / union_count) * 65536)


# ================================================================================
# Mine solution two - Counter + | & 연산자
# ================================================================================
def solution_mine_two(str1: str, str2: str) -> int:
    """
    Counter와 | & 연산자로 다중집합 교집합/합집합을 구하는 파이써닉한 풀이

    Counter | : 다중집합 합집합 = max(freq1, freq2)
    Counter & : 다중집합 교집합 = min(freq1, freq2)

    일반 dict |와의 차이:
        dict |: 중복 키는 오른쪽 값으로 덮어씀
        Counter |: max(freq1, freq2) (다중집합 연산으로 오버라이딩)

    :=  할당 표현식:
        동일한 슬라이싱을 if 조건과 결과에 두 번 쓰는 중복 제거
    """
    s1, s2 = str1.lower(), str2.lower()

    sub1 = [text for i in range(len(s1) - 1) if (text := s1[i:i + 2]).isalpha()]
    sub2 = [text for i in range(len(s2) - 1) if (text := s2[i:i + 2]).isalpha()]

    c1, c2 = Counter(sub1), Counter(sub2)

    union_count = sum((c1 | c2).values())
    intersection_count = sum((c1 & c2).values())

    if union_count == 0:
        return 65536

    return int((intersection_count / union_count) * 65536)


# ================================================================================
# Ref solution one - set + 접미사 변환
# ================================================================================
def solution_ref_one(str1: str, str2: str) -> int:
    """
    중복 원소를 "원소_번호" 형태로 변환해 set을 사용하는 참고 풀이

    핵심 아이디어:
        "aa"가 3번 → {"aa_1","aa_2","aa_3"} (중복→비중복 변환)
        set 집합 연산으로 교집합/합집합 계산 가능

    Counter 대비 느린 이유:
        f"{text}_{count_dict[text]}" 문자열 포맷팅이 매 원소마다 발생
        문자열 생성 비용이 Counter 연산보다 무거움
    """
    s1, s2 = str1.lower(), str2.lower()

    def make_set(s: str) -> set:
        result = set()
        count_dict = {}
        for i in range(len(s) - 1):
            if (text := s[i:i + 2]).isalpha():
                count_dict[text] = count_dict.get(text, 0) + 1
                result.add(f"{text}_{count_dict[text]}")
        return result

    set1 = make_set(s1)
    set2 = make_set(s2)

    intersection_count = len(set1 & set2)
    union_count = len(set1 | set2)

    return int((intersection_count / union_count) * 65536) if union_count > 0 else 65536


# ================================================================================
# Ref solution two - 정렬 + 투포인터
# ================================================================================
def solution_ref_two(str1: str, str2: str) -> int:
    """
    정렬된 두 리스트를 투포인터로 순회해 교집합/합집합을 구하는 참고 풀이

    병합 정렬 병합 단계와 동일한 구조:
        sub1[p1] == sub2[p2]: 공통 원소 → 교집합+1, 합집합+1
        sub1[p1] < sub2[p2]:  sub1만의 원소 → 합집합+1, p1 전진
        sub1[p1] > sub2[p2]:  sub2만의 원소 → 합집합+1, p2 전진
    while 종료 후 남은 원소 → 합집합에만 추가

    O(N log N): 정렬 비용으로 Counter O(N)보다 느림
    """
    s1, s2 = str1.lower(), str2.lower()

    sub1 = sorted([text for i in range(len(s1) - 1) if (text := s1[i:i + 2]).isalpha()])
    sub2 = sorted([text for i in range(len(s2) - 1) if (text := s2[i:i + 2]).isalpha()])

    p1 = p2 = intersection_count = union_count = 0

    while p1 < len(sub1) and p2 < len(sub2):
        if sub1[p1] == sub2[p2]:
            intersection_count += 1
            union_count += 1
            p1 += 1
            p2 += 1
        elif sub1[p1] < sub2[p2]:
            union_count += 1
            p1 += 1
        else:
            union_count += 1
            p2 += 1

    union_count += (len(sub1) - p1) + (len(sub2) - p2)

    if union_count == 0:
        return 65536

    return int((intersection_count / union_count) * 65536)


# ================================================================================
# Best solution - Counter + | & 연산자 (mine_two 주석 보강)
# ================================================================================
def solution_best(str1: str, str2: str) -> int:
    """
    Counter | & 연산으로 가장 빠르고 간결하게 자카드 유사도를 구하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        Counter가 다중집합 연산을 직접 지원 → 별도 공식 구현 불필요
        실측 가장 빠름 (문자열 포맷팅, 정렬 오버헤드 없음)
        :=  할당 표현식으로 리스트 컴프리헨션 내 중복 슬라이싱 제거
    """
    s1, s2 = str1.lower(), str2.lower()

    sub1 = [text for i in range(len(s1) - 1) if (text := s1[i:i + 2]).isalpha()]
    sub2 = [text for i in range(len(s2) - 1) if (text := s2[i:i + 2]).isalpha()]

    c1, c2 = Counter(sub1), Counter(sub2)

    union_count = sum((c1 | c2).values())
    intersection_count = sum((c1 & c2).values())

    if union_count == 0:
        return 65536

    return int((intersection_count / union_count) * 65536)


# ================================================================================
# Sub solution - 직접 dict + min/max (mine_one 주석 보강)
# ================================================================================
def solution_sub(str1: str, str2: str) -> int:
    """
    직접 dict로 빈도를 집계하고 min/max 공식으로 처리하는 서브 풀이

    Best 대비 특징:
        Counter 없이 직접 dict로 빈도 집계 → 동작 원리 명시적
        min/max 공식이 코드에 직접 드러남
        set | 연산으로 전체 키 합집합 O(K) 구성
        실측 Best와 거의 동일한 성능
    """
    s1, s2 = str1.lower(), str2.lower()
    sub1, sub2 = {}, {}

    for i in range(len(s1) - 1):
        text = s1[i:i + 2]
        if text.isalpha():
            sub1[text] = sub1.get(text, 0) + 1

    for i in range(len(s2) - 1):
        text = s2[i:i + 2]
        if text.isalpha():
            sub2[text] = sub2.get(text, 0) + 1

    all_elements = set(sub1.keys()) | set(sub2.keys())
    union_count = intersection_count = 0

    for key in all_elements:
        f1, f2 = sub1.get(key, 0), sub2.get(key, 0)
        union_count += max(f1, f2)
        intersection_count += min(f1, f2)

    if union_count == 0:
        return 65536

    return int((intersection_count / union_count) * 65536)


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, str, int]] = [
        # (str1, str2, 기댓값)
        ("FRANCE",    "french",      16384),
        ("handshake", "shake hands", 65536),
        ("aa1+aa2",   "AAAA12",      43690),
        ("E=M*C^2",   "e=m*c^2",     65536),
    ]

    solutions = [
        ("Mine_one (dict+min/max)  ", solution_mine_one),
        ("Mine_two (Counter)       ", solution_mine_two),
        ("Ref_one  (set+접미사)    ", solution_ref_one),
        ("Ref_two  (정렬+포인터)   ", solution_ref_two),
        ("Best     (Counter)       ", solution_best),
        ("Sub      (dict+min/max)  ", solution_sub),
    ]

    # 워밍업 스텝
    _s1, _s2, _ = test_cases[0]
    for _, func in solutions:
        func(_s1, _s2)

    print("=" * 68)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (str1, str2, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(str1, str2)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
