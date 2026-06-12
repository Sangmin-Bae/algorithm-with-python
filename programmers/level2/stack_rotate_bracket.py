"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 괄호 회전하기
    유형       : Stack
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/76502
    풀이일자   : 2026-06-12
================================================================================
[문제 요약]
    문자열 s를 왼쪽으로 x칸 회전(0 ≤ x < len(s))했을 때
    올바른 괄호 문자열이 되는 x의 개수를 반환

    올바른 괄호 문자열 조건:
        (), [], {} 자체가 올바름
        A가 올바르면 (A), [A], {A}도 올바름
        A, B가 올바르면 AB도 올바름

    제약 조건
        - s 길이: 1 이상 1,000 이하
        - s는 (, ), {, }, [, ]로만 구성
================================================================================
[입출력 예시]
    s          | result
    -----------|-------
    "[](){}"   | 3
    "}]()[{"   | 2
    "[)(]"     | 0
    "}}}"      | 0
================================================================================
[내 초기 풀이]
    solution_mine_one: re 라이브러리 정규표현식 + 치환 반복
        회전: s = s[1:] + s[0]으로 문자열 슬라이싱 회전
        판별: re.search()로 괄호 존재 확인, re.sub()로 치환 반복
        빈 문자열이면 올바른 괄호 문자열로 판단

    solution_mine_two: any() + str.replace() + 치환 반복
        mine_one과 동일 로직, re 라이브러리 대신 any() + replace() 사용
        고정 리터럴 3개 탐색에 정규표현식 엔진이 오버스펙이라 판단

[개선 포인트]
    solution_mine_one:
        sub_s = s = s[1:] + s[0]: Python 연쇄 할당 (chained assignment)
            오른쪽 expr을 한 번만 평가 후 왼쪽 변수들에 동일한 객체를 순서대로 할당
            s → 다음 루프의 회전 기준 문자열로 갱신
            sub_s → 현재 루프의 치환 소모용 복사본
        re 라이브러리: 고정 리터럴 3개 치환에 정규표현식 엔진 → 오버스펙

    solution_mine_one/two 공통:
        while 치환 반복 판별: O(N) 치환 × O(N/2) 반복 = O(N²) 판별 비용
        → 스택 방식으로 O(N) 판별로 개선 가능
================================================================================
[스택 기반 괄호 판별 원리]
    여는 괄호는 스택에 쌓고, 닫는 괄호가 나오면 스택 top과 쌍 확인

    손 추적 "([{}])":
        문자  스택          동작
        (   → ['(']        여는 괄호 → push
        [   → ['(','[']    여는 괄호 → push
        {   → ['(','[','{'] 여는 괄호 → push
        }   → ['(','[']    stack[-1]='{', '}'와 쌍 → pop ✓
        ]   → ['(']        stack[-1]='[', ']'와 쌍 → pop ✓
        )   → []           stack[-1]='(', ')'와 쌍 → pop ✓
        끝  → 스택 비어있음 → True ✓

    손 추적 "([)]":
        문자  스택          동작
        (   → ['(']
        [   → ['(','[']
        )   → stack[-1]='[', ')'와 쌍 불일치 → False ✗

    조기 종료 조건:
        1. 닫는 괄호인데 스택이 비어있음 → 쌍 없음 → False
        2. 닫는 괄호인데 stack[-1]과 쌍 불일치 → False
        3. 순회 후 스택에 원소 남음 → 닫히지 않은 괄호 → False
================================================================================
[회전 방식 비교 — 문자열 슬라이싱 vs deque.rotate()]
    문자열 슬라이싱 s[1:] + s[0]:
        길이 N 문자열 복사 → O(N) 시간, O(N) 공간 (새 객체 생성)
        N번 회전 → O(N²) 회전 비용, 매번 새 문자열 객체 힙 생성

    deque.rotate(-1):
        내부 포인터 이동 → O(1) 시간, O(1) 추가 공간
        N번 회전 → O(N) 회전 비용, 추가 객체 생성 없음

    실질 성능 차이:
        N=1,000: 슬라이싱 O(N²)=100만, deque O(N)=1,000
        판별 비용(O(N²))이 지배적이라 회전 방식 차이는 상대적으로 작음
        그러나 슬라이싱의 반복적 객체 생성은 GC 부하로 이어짐
================================================================================
[복잡도 분석]
    N = len(s) (최대 1,000)

    Mine_one/two - 시간: O(N³) | 공간: O(N)
        회전 O(N) × 판별 O(N²) [치환 반복]
        N=1,000: 최대 10억 연산 → 시간 초과 가능성

    Best         - 시간: O(N²) | 공간: O(N)
        회전 O(N) × 판별 O(N) [스택 1회 순회]
        N=1,000: 최대 100만 연산 → 여유롭게 통과

    Sub          - 시간: O(N³) | 공간: O(N) — Mine_two와 동일, 주석 보강
    Ref          - 시간: O(N²) | 공간: O(N) — deque O(1) 회전 + 스택 O(N) 판별
"""

import re
from collections import deque
from typing import List, Tuple


# ================================================================================
# 공통 헬퍼 - 스택 기반 괄호 유효성 판별
# ================================================================================
def is_valid(s: str) -> bool:
    """
    스택으로 괄호 쌍을 확인해 올바른 괄호 문자열인지 판별

    O(N) 단일 순회로 판별 완료
    치환 반복 O(N²) 대비 핵심 개선 포인트
    """
    stack = []
    pair = {')': '(', '}': '{', ']': '['}  # 닫는 괄호 → 대응 여는 괄호

    for c in s:
        if c in '({[':
            stack.append(c)             # 여는 괄호 → push
        else:
            if not stack or stack[-1] != pair[c]:
                return False            # 스택 비었거나 쌍 불일치
            stack.pop()                 # 쌍 일치 → pop

    return not stack                    # 스택 비어야 올바른 괄호 문자열


# ================================================================================
# Mine solution one - re 정규표현식 + 치환 반복
# ================================================================================
def solution_mine_one(s: str) -> int:
    """
    정규표현식으로 괄호를 탐색/치환하는 초기 풀이

    핵심:
        pattern = r'[()][)][{][}][[]]' 형태로 괄호 3쌍을 찾는 정규표현식
        괄호가 정규표현식 특수문자이므로 raw string + 백슬래시로 이스케이프
        re.search(): 패턴 존재 여부 확인 → while 조건
        re.sub(): 패턴 매칭 문자열을 '' 으로 치환

    개선 포인트:
        고정 리터럴 3개 치환에 정규표현식 엔진 → 오버스펙
        while 치환 반복 → O(N²) 판별 비용
    """
    answer = 0
    pattern = r"\(\)|\{\}|\[\]"

    for _ in range(len(s)):
        sub_s = s = s[1:] + s[0]    # 연쇄 할당: s 회전 갱신 + sub_s에 동일 객체 할당

        while re.search(pattern, sub_s):
            sub_s = re.sub(pattern, '', sub_s)

        if not sub_s:
            answer += 1

    return answer


# ================================================================================
# Mine solution two - any() + str.replace() + 치환 반복
# ================================================================================
def solution_mine_two(s: str) -> int:
    """
    any() + replace()로 mine_one을 re 없이 구현한 풀이

    mine_one 대비 개선:
        re 라이브러리 제거 → 고정 리터럴 탐색에 더 적합
        any(b in sub_s for b in brackets): 괄호 하나라도 존재하면 True
        str.replace(b, ''): 매칭 문자열 제거

    공통 한계:
        while 치환 반복 → O(N²) 판별 비용 유지
    """
    answer = 0
    brackets = ["()", "{}", "[]"]

    for _ in range(len(s)):
        s = s[1:] + s[0]        # 왼쪽으로 1칸 회전
        sub_s = s               # 판별용 복사본

        while any(b in sub_s for b in brackets):
            for b in brackets:
                sub_s = sub_s.replace(b, '')

        if not sub_s:
            answer += 1

    return answer


# ================================================================================
# Best solution - 스택 판별 + 문자열 슬라이싱 회전
# ================================================================================
def solution_best(s: str) -> int:
    """
    스택 기반 O(N) 판별로 치환 반복 O(N²)을 개선한 최적 풀이

    mine_one/two 대비 개선:
        치환 반복(O(N²)) → 스택 1회 순회(O(N)) 판별
        전체: O(N³) → O(N²)

    회전: s[1:] + s[0] 문자열 슬라이싱 (O(N) 복사)
    판별: is_valid() 스택 O(N) 단일 순회
    """
    answer = 0

    for _ in range(len(s)):
        s = s[1:] + s[0]        # 왼쪽으로 1칸 회전

        if is_valid(s):
            answer += 1

    return answer


# ================================================================================
# Sub solution - any() + replace() (mine_two 주석 보강)
# ================================================================================
def solution_sub(s: str) -> int:
    """
    any() + replace() 치환 반복 방식 서브 풀이 (mine_two 주석 보강)

    Best 대비 특징:
        스택 개념 없이 직관적으로 이해 가능
        "안쪽 괄호부터 제거하면 올바른 괄호 문자열은 빈 문자열이 됨" 원리
        O(N²) 판별 비용으로 Best 대비 느림
        N=1,000 입력에서 시간 초과 가능성 있음

    any() 단락 평가:
        하나라도 True이면 즉시 True 반환 → 모든 brackets 확인 불필요
    """
    answer = 0
    brackets = ["()", "{}", "[]"]

    for _ in range(len(s)):
        s = s[1:] + s[0]
        sub_s = s

        while any(b in sub_s for b in brackets):
            for b in brackets:
                sub_s = sub_s.replace(b, '')

        if not sub_s:
            answer += 1

    return answer


# ================================================================================
# Ref solution - deque.rotate() + 스택 판별
# ================================================================================
def solution_ref(s: str) -> int:
    """
    deque.rotate()로 O(1) 회전, 스택으로 O(N) 판별하는 참고 풀이

    Best 대비 특징:
        회전: deque.rotate(-1) O(1) → 추가 문자열 객체 생성 없음
                s[1:]+s[0] O(N) 복사 대비 회전 비용 절감
        판별: 스택 O(N) 동일

        시간복잡도 동일 O(N²)이나 회전 상수 인자 차이:
            슬라이싱: N번 × O(N) = O(N²) 회전 비용
            deque:   N번 × O(1) = O(N)  회전 비용

    deque.rotate(-1): 왼쪽으로 1칸 회전
        [a,b,c,d] → rotate(-1) → [b,c,d,a]
    """
    answer = 0
    queue = deque(s)
    pair = {')': '(', '}': '{', ']': '['}

    for _ in range(len(s)):
        queue.rotate(-1)        # O(1) 왼쪽 회전

        stack = []
        valid = True
        for c in queue:         # deque 직접 순회
            if c in '({[':
                stack.append(c)
            else:
                if not stack or stack[-1] != pair[c]:
                    valid = False
                    break
                stack.pop()

        if valid and not stack:
            answer += 1

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: List[Tuple[str, int]] = [
        # (s, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # "[](){}": x=0 ✓, x=1 ✗, x=2 ✓, x=3 ✗, x=4 ✓, x=5 ✗ → 3
        ("[](){}", 3),
        # "}]()[{": x=0 ✗, x=1 ✗, x=2 ✓, x=3 ✗, x=4 ✓, x=5 ✗ → 2
        ("}]()[{", 2),
        # "[)(]": 어떻게 회전해도 올바른 괄호 불가 → 0
        ("[)(]",   0),
        # "}}}": 닫는 괄호만 존재, 여는 괄호 없음 → 0
        ("}}}",    0),
        # 추가 케이스:
        # "()": x=0 "()" ✓, x=1 ")(" ✗ → 1
        ("()",     1),
        # "([{}])": x=0 ✓, 나머지 ✗ → 1
        ("([{}])", 1),
    ]

    solutions = [
        ("Mine_one (re 치환반복)      ", solution_mine_one),
        ("Mine_two (replace 치환반복) ", solution_mine_two),
        ("Best     (스택 판별)        ", solution_best),
        ("Sub      (replace 치환반복) ", solution_sub),
        ("Ref      (deque+스택)       ", solution_ref),
    ]

    print("=" * 72)
    print(f"{'풀이':<32} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 72)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = __import__('time').perf_counter()
            output = func(s)
            elapsed = __import__('time').perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<32} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 72)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
