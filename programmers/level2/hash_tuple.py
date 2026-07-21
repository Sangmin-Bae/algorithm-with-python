"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 튜플
    유형       : Hash / String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/64065
    풀이일자   : 2026-07-21
================================================================================
[문제 요약]
    집합 기호로 표현된 문자열 s에서 원래 튜플을 복원해 배열로 반환

    집합 표현: {{a1},{a1,a2},{a1,a2,a3},...,{a1,...,an}}
    -> 집합 내부 순서는 무관, 전체 집합 순서도 무관

    제약 조건
        - s 길이: 5 이상 1,000,000 이하
        - 튜플 원소: 1 이상 100,000 이하 자연수
        - 튜플 길이: 1 이상 500 이하
        - 중복 원소 없음
================================================================================
[입출력 예시]
    s                                   | result
    ------------------------------------|-------------
    "{{2},{2,1},{2,1,3},{2,1,3,4}}"    | [2, 1, 3, 4]
    "{{1,2,3},{2,1},{1,2,4,3},{2}}"    | [2, 1, 3, 4]
    "{{20,111},{111}}"                  | [111, 20]
================================================================================
[핵심 관찰 - 튜플 순서 복원 방법]
    방법 1: 집합 크기 기준 정렬
        크기 1인 집합 -> a1 (가장 먼저 등장)
        크기 2인 집합 -> a1, a2 (a1은 이미 확인, a2가 새로 등장)
        크기 k인 집합 -> 앞 k-1개는 이미 확인, 새로 등장하는 원소가 ak
        -> 길이순 정렬 후 seen에 없는 원소 순서대로 추출

    방법 2: 원소 등장 횟수 기준
        a1은 n개 집합 모두에 등장 -> n회
        a2는 크기 2 이상 집합에 등장 -> n-1회
        ak는 크기 k 이상 집합에 등장 -> n-k+1회
        -> 등장 횟수 내림차순 = 튜플 순서
        -> Counter.most_common()으로 직접 추출 가능

[복잡도 분석 상세]
    N = len(s) (최대 1,000,000)
    n = 튜플 원소 수 (최대 500)
    d = 원소 자릿수 (최대 6)
    전체 원소 수 = 1+2+...+n = n(n+1)/2 <= 125,250

    Mine_one:
        s[2:-2].split("},"): O(N)
        int() 파싱 × n(n+1)/2: O(n² × d) = O(n²)
        sorted(key=len): O(n log n)
        2중 for + set in: O(n²) × O(1)
        전체: O(N + n²)  N이 크면 O(N) 지배

    Mine_two:
        replace × 2: O(N)
        literal_eval(): O(N) - AST 파싱, 상수 인자 큼
        sorted + 2중 for + dict in: O(n log n + n²)
        전체: O(N + n²)  Mine_one과 동일, literal_eval 상수 커서 실제 느림

    Ref:
        re.findall 숫자 추출: O(N) - 미컴파일 패턴 시 컴파일 오버헤드
        Counter(nums): O(n(n+1)/2) = O(n²)
        most_common(): O(n log n) - 힙 정렬 기반
        전체: O(N + n²)

    세 풀이 모두 O(N + n²)에 수렴
    실질 차이는 파싱 방식의 상수 인자:
        Mine_one:  직접 파싱 -> 상수 작음
        Mine_two:  literal_eval -> 상수 큼 (안전성·편의성 트레이드오프)
        Ref:       re.findall -> 중간, 구조 파싱 불필요로 발상 독창적
================================================================================
[내 초기 풀이]
    solution_mine_one: 직접 파싱 + 길이순 정렬 + set seen
    solution_mine_two: literal_eval + 길이순 정렬 + dict seen

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       직접 파싱으로 상수 인자 최소, 동작 원리 명시적
    solution_mine_two: literal_eval 상수 인자 큼
                       dict seen: 순서 보장 set 대용 (Python 3.7+ 삽입 순서 보장)
    solution_ref:      집합 구조 파싱 불필요, 빈도만으로 순서 복원 - Sub
                       Counter.most_common()으로 3줄 완성
================================================================================
"""

import re
from ast import literal_eval
from collections import Counter
import time


# ================================================================================
# Mine solution one - 직접 파싱 + 길이순 정렬 + set seen
# ================================================================================
def solution_mine_one(s: str) -> list[int]:
    """
    문자열을 직접 파싱해 집합 크기순으로 정렬 후 새 원소를 순서대로 추출하는 풀이

    파싱 전략:
        s[2:-2]: 가장 외곽 "{{", "}}" 제거
        .split("},"): 각 집합 문자열로 분리
        int() 변환으로 2차원 정수 리스트 생성

    튜플 순서 복원:
        key=len으로 집합 크기 오름차순 정렬
        크기 k 집합에서 seen에 없는 원소 = 튜플의 k번째 원소

    seen을 set으로:
        list in O(n) -> set in O(1)
        answer 리스트에 직접 추가 -> 순서 유지
    """
    answer = []
    parsed_s = s[2:-2].split("},{")
    tuple_list = sorted(
        [[int(x) for x in group.split(",")] for group in parsed_s],
        key=len
    )

    seen = set()
    for group in tuple_list:
        for num in group:
            if num not in seen:
                seen.add(num)
                answer.append(num)

    return answer


# ================================================================================
# Mine solution two - literal_eval + 길이순 정렬 + dict seen
# ================================================================================
def solution_mine_two(s: str) -> list[int]:
    """
    ast.literal_eval로 문자열을 2차원 리스트로 변환 후 dict로 순서를 유지하는 풀이

    literal_eval 활용:
        "{" -> "[", "}" -> "]" 치환 후 literal_eval로 파이썬 자료형 직접 변환
        set은 2차원 불가, 변환 시 순서 미보장 -> 대괄호로 치환해 리스트로 처리
        편의성 높으나 내부 AST 파싱으로 상수 인자 큼

    dict seen 활용:
        Python 3.7+ dict 삽입 순서 보장 + in O(1)
        순서 보장 set이 없어 dict를 순서 보장 set 대용으로 활용
        seen.keys() -> 삽입 순서 유지된 원소 반환
    """
    tuple_list = literal_eval(s.replace("{", "[").replace("}", "]"))
    tuple_list = sorted(tuple_list, key=len)

    seen = {}
    for group in tuple_list:
        for num in group:
            seen[num] = True

    return list(seen.keys())


# ================================================================================
# Ref solution - re.findall + Counter.most_common()
# ================================================================================
def solution_ref(s: str) -> list[int]:
    """
    원소 등장 횟수로 튜플 순서를 복원하는 참고 풀이

    핵심 발상 - 집합 구조 파싱 불필요:
        a1은 n개 집합 모두에 등장 -> n회
        a2는 크기 2 이상 집합에 등장 -> n-1회
        ak는 크기 k 이상 집합에 등장 -> n-k+1회
        -> 등장 횟수 내림차순 = 튜플 순서

    구현:
        re.findall로 숫자만 모두 추출 -> 집합 구조 무시
        Counter(nums): 각 원소 등장 횟수 집계 O(n²/2)
        most_common(): 등장 횟수 내림차순 정렬 O(n log n)

    주의:
        미컴파일 패턴 사용 -> 호출마다 컴파일 오버헤드
        re.compile로 사전 컴파일하면 반복 호출 시 효율적
    """
    nums = re.findall(r'\d+', s)
    counts = Counter(nums)
    return [int(num) for num, _ in counts.most_common()]


# ================================================================================
# Best solution - 직접 파싱 + 길이순 정렬 (mine_one 주석 보강)
# ================================================================================
def solution_best(s: str) -> list[int]:
    """
    직접 파싱 + 길이순 정렬로 O(N + n²) 시간, 상수 인자 최소인 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        직접 파싱(split + int): literal_eval 대비 상수 인자 작음
        key=len 정렬: 집합 크기 오름차순으로 튜플 순서 복원
        set seen: 중복 제거 O(1) + answer 리스트에 순서 직접 기록
        동작 원리(길이순 정렬 -> 새 원소 순서대로 추출)가 코드에 명시적
    """
    answer = []
    parsed_s = s[2:-2].split("},{")
    tuple_list = sorted(
        [[int(x) for x in group.split(",")] for group in parsed_s],
        key=len
    )

    seen = set()
    for group in tuple_list:
        for num in group:
            if num not in seen:
                seen.add(num)
                answer.append(num)

    return answer


# ================================================================================
# Sub solution - re.findall + Counter (solution_ref 주석 보강)
# ================================================================================
def solution_sub(s: str) -> list[int]:
    """
    원소 등장 횟수 기반으로 집합 구조 파싱 없이 튜플 순서를 복원하는 서브 풀이

    Best 대비 특징:
        집합 구조({}, 크기) 파싱 완전히 생략 -> 발상 독창적
        숫자만 추출 후 빈도로 순서 결정 -> 코드 3줄로 완성
        Counter: C 레벨 구현으로 빈도 집계 효율적
        most_common(): 내부 힙 정렬 O(n log n) 기반
    """
    nums = re.findall(r'\d+', s)
    counts = Counter(nums)
    return [int(num) for num, _ in counts.most_common()]


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, list[int]]] = [
        # (s, 기댓값)
        # 손 추적:
        # "{{2},{2,1},{2,1,3},{2,1,3,4}}"
        # 길이순: [2], [2,1], [2,1,3], [2,1,3,4]
        # [2]: 2 새로 등장 -> [2]
        # [2,1]: 1 새로 등장 -> [2,1]
        # [2,1,3]: 3 새로 등장 -> [2,1,3]
        # [2,1,3,4]: 4 새로 등장 -> [2,1,3,4]
        ("{{2},{2,1},{2,1,3},{2,1,3,4}}", [2, 1, 3, 4]),
        # 집합 내부/외부 순서 뒤섞인 케이스
        ("{{1,2,3},{2,1},{1,2,4,3},{2}}", [2, 1, 3, 4]),
        # 큰 숫자 케이스
        ("{{20,111},{111}}", [111, 20]),
        # 단일 원소
        ("{{123}}", [123]),
        # 집합 순서 뒤섞인 케이스
        ("{{4,2,3},{3},{2,3,4,1},{2,3}}", [3, 2, 4, 1]),
    ]

    solutions = [
        ("Mine_one   (직접파싱+set)  ", solution_mine_one),
        ("Mine_two   (literal+dict)  ", solution_mine_two),
        ("Ref        (Counter)       ", solution_ref),
        ("Best       (직접파싱+set)  ", solution_best),
        ("Sub        (Counter)       ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 68)
    print(f"{'풀이':<28} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<28} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
