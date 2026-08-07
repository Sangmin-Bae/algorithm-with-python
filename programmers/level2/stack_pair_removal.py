"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 짝지어 제거하기
    유형       : Stack / Queue
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12973
    풀이일자   : 2026-08-07
================================================================================
[문제 요약]
    알파벳 소문자 문자열에서 같은 알파벳 2개가 붙어있는 짝을 제거
    반복 후 문자열이 모두 제거되면 1, 아니면 0 반환

    제약 조건
        - s 길이: 1,000,000 이하
        - 소문자 알파벳으로만 구성
================================================================================
[입출력 예시]
    s       | result
    --------|-------
    "baabaa" | 1
    "cdcd"   | 0
================================================================================
[핵심 아이디어 — 스택으로 단일 순회]
    문자를 하나씩 순회하며:
        스택 최상단과 현재 문자가 같으면 → 쌍 제거 (pop)
        다르면 → 스택에 push

    순회 후 스택이 비어있으면 모든 쌍 제거 완료 → 1
    남아있으면 → 0

    조기 반환: len(s) % 2 != 0이면 쌍을 완전히 이룰 수 없음 → 즉시 0

    "올바른 괄호" 문제와 동일한 스택 패턴
        올바른 괄호: '(' push, ')' 만나면 pop (불일치 시 즉시 False)
        짝지어 제거: 이전 문자 push, 같은 문자 만나면 pop

[solution_ref 포인터 방식 — 손 추적]
    s="baabaa", arr=['b','a','a','b','a','a'], top=-1

    char='b': top=-1 → 비교 불가
               top=0, arr[0]='b'        (push: top+=1 후 덮어쓰기)
    char='a': arr[0]='b' != 'a'
               top=1, arr[1]='a'        (push)
    char='a': arr[1]='a' == 'a'
               top=0                    (pop: top-=1만)
    char='b': arr[0]='b' == 'b'
               top=-1                   (pop)
    char='a': top=-1 → 비교 불가
               top=0, arr[0]='a'        (push, 이전 'b' 위치 덮어쓰기)
    char='a': arr[0]='a' == 'a'
               top=-1                   (pop)
    top==-1 → return 1 ✓

    top은 스택의 인덱스, arr의 앞부분이 스택의 내용
    push: top += 1 후 arr[top] 덮어쓰기
    pop:  top -= 1 만 (덮어쓴 위치는 무시, 다음 push 시 재사용)

[메모리 비교]
    stack 방식:
        빈 리스트 [] 에서 시작
        문자 추가마다 동적 크기 조절 (dynamic resizing)
        최악 O(N) 공간, 재할당 O(log N)회 발생

    ref 포인터 방식:
        list(s)로 고정 크기 N 리스트 생성
        in-place 덮어쓰기만 → 크기 변동 없음
        항상 O(N) 공간, 재할당 0회

    ref가 재할당 없어 메모리 안정적
    stack은 실제 쌓인 만큼만 사용하므로 입력에 따라 더 적은 메모리 가능
================================================================================
[내 초기 풀이]
    solution_mine: 스택(리스트) 방식

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
                   직관적, 동작 원리 명확
                   "올바른 괄호"와 동일한 스택 패턴
    solution_ref:  포인터 방식 - Sub
                   재할당 없어 메모리 안정적
                   동작 원리 해석이 필요한 방식
================================================================================
[복잡도 분석]
    N = len(s) (최대 1,000,000)

    Mine - 시간: O(N) | 공간: O(N) - 스택 최대 N/2 크기, 재할당 O(log N)회
    Ref  - 시간: O(N) | 공간: O(N) - list(s) 고정 크기, 재할당 없음
    Best - 시간: O(N) | 공간: O(N) - Mine과 동일
    Sub  - 시간: O(N) | 공간: O(N) - Ref와 동일
"""

import time


# ================================================================================
# Mine solution - 스택 방식
# ================================================================================
def solution_mine(s: str) -> int:
    """
    스택으로 짝을 즉시 제거하며 단일 순회하는 초기 풀이

    핵심:
        stack[-1] == char: 스택 최상단과 현재 문자가 같으면 쌍 → pop
        그 외: 스택에 push
        최종 not stack: 스택이 비었으면 모두 제거 완료 → 1

    조기 반환:
        len(s) % 2 != 0: 홀수 길이는 완전한 쌍 불가 → 즉시 0

    "올바른 괄호" 문제와 동일한 스택 패턴:
        괄호: 여는/닫는 구분 → 이 문제: 동일 문자 쌍
    """
    if len(s) % 2 != 0:
        return 0

    stack = []

    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)

    return 1 if not stack else 0


# ================================================================================
# Ref solution - 포인터 방식 (in-place)
# ================================================================================
def solution_ref(s: str) -> int:
    """
    top 포인터로 arr 앞부분을 스택처럼 사용하는 in-place 풀이

    top 포인터 역할:
        스택의 인덱스를 나타냄
        top == -1: 스택 비어있음
        top >= 0: arr[top]이 스택 최상단

    push 동작: top += 1 후 arr[top] = char (덮어쓰기)
    pop 동작:  top -= 1 만 (arr 값은 유지, 무시되는 공간)

    메모리 효율:
        list(s): 고정 크기 N, 크기 변동 없음
        스택 방식의 동적 재할당(O(log N)회) 없음
    """
    if len(s) % 2 != 0:
        return 0

    arr = list(s)
    top = -1

    for char in arr:
        if top >= 0 and arr[top] == char:
            top -= 1
        else:
            top += 1
            arr[top] = char

    return 1 if top == -1 else 0


# ================================================================================
# Best solution - 스택 방식 (mine 주석 보강)
# ================================================================================
def solution_best(s: str) -> int:
    """
    스택으로 O(N) 시간, O(N) 공간에 짝을 제거하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        직관적: push/pop으로 쌍 제거 의도가 코드에 직접 드러남
        단일 순회 O(N): replace/정규표현식의 반복 순회 대비 효율적
        not stack: 빈 스택 = 모든 쌍 제거 완료
    """
    if len(s) % 2 != 0:
        return 0

    stack = []

    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)

    return 1 if not stack else 0


# ================================================================================
# Sub solution - 포인터 방식 (ref 주석 보강)
# ================================================================================
def solution_sub(s: str) -> int:
    """
    top 포인터 + in-place 덮어쓰기로 메모리 재할당 없이 처리하는 서브 풀이

    Best 대비 특징:
        list(s) 고정 크기 → 동적 재할당 0회
        스택 방식의 재할당 O(log N)회 없음
        동작 원리: top이 스택 인덱스, arr 앞부분이 스택 내용
        직관성은 낮으나 메모리 사용이 더 안정적
    """
    if len(s) % 2 != 0:
        return 0

    arr = list(s)
    top = -1

    for char in arr:
        if top >= 0 and arr[top] == char:
            top -= 1
        else:
            top += 1
            arr[top] = char

    return 1 if top == -1 else 0


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[str, int]] = [
        # (s, 기댓값)
        # 공식 예시
        # 손 추적:
        # "baabaa": b→push, a→push, a→pop(aa제거), b→pop(bb제거),
        #           a→push, a→pop(aa제거) → 스택 비어있음 → 1
        ("baabaa", 1),
        # "cdcd": c→push, d→push, c≠d→push, d≠c→push → 스택 ['c','d','c','d'] → 0
        ("cdcd",   0),
        # 추가 케이스:
        ("aa",     1),   # 최소 쌍
        ("ab",     0),   # 제거 불가
        ("aabb",   1),   # aa제거→bb제거
        ("abba",   1),   # a→b→b 제거→a 제거
        ("a",      0),   # 홀수 길이
    ]

    solutions = [
        ("Mine (스택)  ", solution_mine),
        ("Ref  (포인터)", solution_ref),
        ("Best (스택)  ", solution_best),
        ("Sub  (포인터)", solution_sub),
    ]

    # 워밍업 스텝
    _s, _ = test_cases[0]
    for _, func in solutions:
        func(_s)

    print("=" * 58)
    print(f"{'풀이':<16} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 58)

    for name, func in solutions:
        for idx, (s, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(s)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<16} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 58)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
