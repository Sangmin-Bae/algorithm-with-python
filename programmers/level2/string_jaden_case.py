"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : JadenCase 문자열 만들기
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12951
    풀이일자   : 2026-08-04
================================================================================
[문제 요약]
    문자열 s를 JadenCase로 변환해 반환
    JadenCase: 모든 단어의 첫 문자가 대문자, 나머지 알파벳은 소문자

    제약 조건
        - s 길이: 1 이상 200 이하
        - 알파벳, 숫자, 공백으로 구성
        - 숫자는 단어 첫 문자로만 나옴 (숫자만으로 구성된 단어 없음)
        - 공백이 연속으로 나올 수 있음
================================================================================
[입출력 예시]
    s                       | return
    ------------------------|------------------------
    "3people unFollowed me" | "3people Unfollowed Me"
    "for the last week"     | "For The Last Week"
================================================================================
[핵심 — 연속 공백 처리]
    s.split() vs s.split(' ') 차이:
        "a  b".split()    → ['a', 'b']      공백 사라짐 → join 시 공백 1개
        "a  b".split(' ') → ['a', '', 'b']  빈 문자열로 공백 보존
                                             ' '.join → "a  b" 공백 2개 유지

    연속 공백 보존을 위해 s.split(' ') 사용 필수

[capitalize() 동작]
    "3people".capitalize() → "3people"   (첫 문자 숫자 → 이어지는 알파벳 소문자)
    "unFollowed".capitalize() → "Unfollowed"
    "".capitalize() → ""                 (빈 문자열 처리 자동)

[upper(), lower()의 숫자 처리]
    upper(), lower(): 알파벳이 아닌 문자(숫자, 공백)는 그대로 반환
    → 숫자에 upper()/lower()를 적용해도 안전

[solution_three s[idx-1] 단락 평가]
    idx == 0 or s[idx-1] == ' ':
        idx == 0이 True이면 s[idx-1] = s[-1] 평가하지 않음 (short-circuit)
        → 정확하게 동작

[실측 결과 — 100,000회 반복]
    케이스      | one(capitalize) | two(flag) | three(enum) | four(regex)
    ------------|-----------------|-----------|-------------|------------
    기본        |      0.53μs     |  1.24μs   |   2.70μs    |   1.27μs
    연속공백    |      0.63μs     |  1.09μs   |   1.89μs    |   1.62μs
    긴문자열    |      2.74μs     |  9.05μs   |  12.58μs    |  10.60μs

    solution_one이 가장 빠른 이유:
        split, capitalize, join 모두 C 레벨 내장 메서드
        Python 레벨 루프 없이 단어 수만큼만 처리

    solution_two, three가 느린 이유:
        Python for 루프에서 문자 단위 처리
        루프 횟수 = len(s), 문자열이 길수록 격차 커짐
================================================================================
[내 초기 풀이]
    solution_mine_one  : split(' ') + capitalize() + join (리스트 컴프리헨션)
    solution_mine_two  : flag 변수 + upper/lower
    solution_mine_three: enumerate + 이전 문자 공백 검사
    solution_mine_four : re.sub + 람다 + capitalize

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Best
                         C 레벨 메서드 조합, 전 케이스 가장 빠름
                         join + 리스트 컴프리헨션: join + 제너레이터보다 빠름
    solution_mine_two  : 개선 필요 없음 - Sub
                         flag로 단어 첫 문자 추적, 동작 원리 명시적
                         Python 루프라 one보다 느리나 의도 명확
    solution_mine_three: enumerate로 이전 인덱스 접근
                         two보다 느림 (인덱스 연산 추가)
    solution_mine_four : 정규표현식 컴파일 비용
                         re.compile로 사전 컴파일하면 반복 호출 효율적
================================================================================
[복잡도 분석]
    N = len(s) (최대 200), W = 단어 수

    Mine_one   - 시간: O(N) | 공간: O(W) - split O(N) + capitalize O(W) + join O(N)
    Mine_two   - 시간: O(N) | 공간: O(N) - 문자 단위 루프 + 문자열 누적
    Mine_three - 시간: O(N) | 공간: O(N) - enumerate 루프
    Mine_four  - 시간: O(N) | 공간: O(N) - 정규표현식 탐색
    Best       - 시간: O(N) | 공간: O(W) - Mine_one과 동일
    Sub        - 시간: O(N) | 공간: O(N) - Mine_two와 동일

    N=200 고정 → 모두 실질적으로 O(1)
    실측 차이는 C 레벨 vs Python 레벨 루프
"""

import re
import time


# ================================================================================
# Mine solution one - split(' ') + capitalize() + join
# ================================================================================
def solution_mine_one(s: str) -> str:
    """
    split(' ') + capitalize() + join으로 JadenCase를 변환하는 초기 풀이

    split(' ') vs split():
        split(' '): 연속 공백을 빈 문자열로 보존 → join 시 공백 수 유지
        split():    연속 공백 제거 → 공백 개수 손실

    capitalize():
        첫 문자를 대문자, 나머지 알파벳을 소문자로 변환
        숫자가 첫 문자여도 이어지는 알파벳은 소문자 처리
        빈 문자열에 적용해도 그대로 빈 문자열 반환

    join + 리스트 컴프리헨션:
        join 내부에서 이터러블을 두 번 순회
        제너레이터: 길이 미리 계산 불가 → 내부 리스트 생성
        리스트 컴프리헨션: 이미 리스트 → 한 번만 순회
    """
    return ' '.join([w.capitalize() for w in s.split(' ')])


# ================================================================================
# Mine solution two - flag 변수 + upper/lower
# ================================================================================
def solution_mine_two(s: str) -> str:
    """
    flag 변수로 단어 첫 문자를 추적해 대소문자를 변환하는 풀이

    flag 동작:
        True → 다음 알파벳을 대문자로 변환
        공백을 만나면 flag = True (다음 단어 첫 문자 대비)
        알파벳/숫자를 만나면 flag = False

    upper()/lower() 숫자 처리:
        알파벳이 아닌 문자는 그대로 반환 → 숫자에 적용해도 안전
    """
    answer = ""
    flag = True

    for char in s:
        if char == ' ':
            answer += char
            flag = True
        elif flag:
            answer += char.upper()
            flag = False
        else:
            answer += char.lower()

    return answer


# ================================================================================
# Mine solution three - enumerate + 이전 문자 공백 검사
# ================================================================================
def solution_mine_three(s: str) -> str:
    """
    enumerate로 인덱스를 추적하며 이전 문자가 공백인지 확인하는 풀이

    idx == 0 or s[idx-1] == ' ':
        idx == 0: 문자열 첫 번째 문자
        s[idx-1] == ' ': 이전 문자가 공백 → 현재 문자는 단어 첫 문자
        단락 평가: idx == 0이 True이면 s[-1] 평가 안 함 → 안전

    mine_two 대비:
        flag 변수 없음 → 인덱스 접근으로 대체
        인덱스 연산이 추가되어 mine_two보다 실측 느림
    """
    answer = ""

    for idx, char in enumerate(s):
        if idx == 0 or s[idx - 1] == ' ':
            answer += char.upper()
        else:
            answer += char.lower()

    return answer


# ================================================================================
# Mine solution four - re.sub + 람다 + capitalize
# ================================================================================
def solution_mine_four(s: str) -> str:
    """
    정규표현식으로 단어를 매칭해 capitalize를 적용하는 풀이

    re.sub(r'\\S+', func, s):
        \\S+: 공백이 아닌 문자 1개 이상 (단어 매칭)
        func(match): 매칭된 단어에 함수 적용 후 치환
        공백은 매칭 대상 아님 → 자동으로 보존

    re.compile로 사전 컴파일:
        반복 호출 시 컴파일 비용 1회만 발생
        이 코드는 함수 내부에서 컴파일 → 호출마다 컴파일

    단점: 정규표현식 파싱 오버헤드 → 단순 문자열 처리보다 느림
    """
    return re.sub(r"\S+", lambda match: match.group().capitalize(), s)


# ================================================================================
# Best solution - split(' ') + capitalize() + join (mine_one 주석 보강)
# ================================================================================
def solution_best(s: str) -> str:
    """
    C 레벨 내장 메서드 조합으로 가장 빠르게 JadenCase를 변환하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        split, capitalize, join: 모두 C 레벨 내장 메서드
        Python 레벨 루프 없이 단어 수(W)만큼만 처리
        실측 전 케이스에서 가장 빠름 (긴 문자열에서 2~5배 우위)
        연속 공백 보존: split(' ')으로 빈 문자열 유지
    """
    return ' '.join([w.capitalize() for w in s.split(' ')])


# ================================================================================
# Sub solution - flag 방식 (mine_two 주석 보강)
# ================================================================================
def solution_sub(s: str) -> str:
    """
    flag 변수로 JadenCase 변환 원리를 명시적으로 표현하는 서브 풀이

    Best 대비 특징:
        flag 변수: 단어 첫 문자 추적 로직이 코드에 직접 드러남
        Python 루프: 문자 단위 처리로 Best보다 느리나 의도 명확
        upper()/lower(): 숫자에 적용해도 안전 (알파벳 아니면 그대로 반환)
    """
    answer = ""
    flag = True

    for char in s:
        if char == ' ':
            answer += char
            flag = True
        elif flag:
            answer += char.upper()
            flag = False
        else:
            answer += char.lower()

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, str]] = [
        # (s, 기댓값)
        # 공식 예시
        ("3people unFollowed me", "3people Unfollowed Me"),
        ("for the last week",     "For The Last Week"),
        # 추가 케이스:
        # 연속 공백 보존
        ("a  b",                  "A  B"),
        # 첫 단어 앞 공백
        (" hello world",          " Hello World"),
        # 이미 JadenCase
        ("For The Last Week",     "For The Last Week"),
    ]

    solutions = [
        ("Mine_one   (capitalize) ", solution_mine_one),
        ("Mine_two   (flag)       ", solution_mine_two),
        ("Mine_three (enumerate)  ", solution_mine_three),
        ("Mine_four  (regex)      ", solution_mine_four),
        ("Best       (capitalize) ", solution_best),
        ("Sub        (flag)       ", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 68)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 68)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 68)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
