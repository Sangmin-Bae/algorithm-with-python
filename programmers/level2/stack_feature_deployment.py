"""
================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 기능개발
    유형       : Stack / Queue
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42586
    풀이일자   : 2026-07-09
================================================================================
[문제 요약]
    각 기능의 진도와 속도가 주어질 때 배포마다 몇 개의 기능이 배포되는지 반환
    앞 기능이 완성되지 않으면 뒤 기능이 먼저 완성돼도 배포 불가
    배포는 하루 끝에 한 번만 가능

    제약 조건
        - 작업 개수: 100 이하
        - 진도: 100 미만 자연수
        - 속도: 100 이하 자연수
================================================================================
[입출력 예시]
    progresses            | speeds            | return
    ----------------------|-------------------|--------
    [93, 30, 55]          | [1, 30, 5]        | [2, 1]
    [95,90,99,99,80,99]   | [1,1,1,1,1,1]     | [1, 3, 2]
================================================================================
[핵심 아이디어 — days 변환 후 그룹핑]
    각 기능 완료까지 필요 일수 계산:
        days[i] = ceil((100 - progresses[i]) / speeds[i])

    그룹핑 규칙:
        days[i] ≤ days[0] (앞 기능 완료일) → 같이 배포
        days[i] > days[0]                  → 다음 배포 기준
        → days[0]이 항상 현재 배포 기준일 (앞 기능이 기준)

    손 추적 ([93,30,55], [1,30,5]):
        days = [7, 3, 9]
        기준 7: 3 ≤ 7 ✓, 9 > 7 → [2, 1]

    손 추적 ([95,90,99,99,80,99], [1,1,1,1,1,1]):
        days = [5, 10, 1, 1, 20, 1]
        기준 5:  10 > 5 → [1]
        기준 10: 1≤10, 1≤10, 20>10 → [3]
        기준 20: 1≤20 → [2]
        결과: [1, 3, 2] ✓

[올림 계산 방식 비교]
    방식 1: 삼항 연산자
        (100-p) // s + 1 if (100-p) % s else (100-p) // s
        나머지 있으면 +1, 없으면 그대로

    방식 2: math.ceil + 실수 나눗셈
        math.ceil((100 - p) / s)
        반드시 / 사용 (// 사용 시 ceil이 무의미)

    방식 3: 음수 내림 트릭 (라이브러리 없이 올림)
        -((p - 100) // s)
        Python //는 음수에서도 수학적 내림 적용
        (p-100)이 음수 → //로 내림 → 음수화하면 올림 효과
        예) p=96, s=5: (96-100)//5 = -4//5 = -1 → -(-1) = 1 ✓

[Ref 풀이 분석]
    solution_ref_one ([d, 1] 2차원 배열):
        max_day와 count를 [d, count] 형태로 묶어 관리
        코드 가독성 향상 효과 있으나 리스트 객체 생성 비용 추가
        풀이 4의 max_day/count 변수를 자료구조로 변형한 것
        불필요한 2차원 배열 → 풀이 4 방식이 더 효율적

    solution_ref_two (try-except + 인접 값 변경):
        daysLeft[i+1] = daysLeft[i]: 다음 값을 현재 기준으로 덮어씀
        인접 두 값 비교 → 윈도우 방식
        IndexError를 except로 처리 → for 루프 마지막 append 처리
        두 가지 문제:
            1. 순회 중 원본 데이터 변경 → 데이터 오염
            2. try-except 오용: 예외는 예외 상황 처리용
               무조건 발생하는 IndexError를 제어 흐름으로 사용
               → 조건문으로 처리하는 게 올바른 방향
================================================================================
[복잡도 분석]
    N = len(progresses) (최대 100)

    Mine_one   - 시간: O(N²) | 공간: O(N) - pop(0) O(N) × N번
    Mine_two   - 시간: O(N)  | 공간: O(N) - [::-1] O(N) + pop() O(1) × N번
    Mine_three - 시간: O(N)  | 공간: O(N) - 음수 트릭 + deque popleft O(1)
    Mine_four  - 시간: O(N)  | 공간: O(N) - 단일 for 순회, days 원본 유지
    Ref_one    - 시간: O(N)  | 공간: O(N) - 2차원 배열 생성 비용 추가
    Ref_two    - 시간: O(N)  | 공간: O(N) - try-except 오용, 원본 데이터 변경
    Best       - 시간: O(N)  | 공간: O(N) - Mine_four와 동일, 주석 보강
    Sub        - 시간: O(N)  | 공간: O(N) - Mine_two와 동일, 주석 보강

    N≤100 고정 → 실질적으로 O(1)에 수렴
    대규모에서 Mine_one의 O(N²) vs 나머지 O(N) 차이 의미 있음
"""

import math
from collections import deque
import time


# ================================================================================
# Mine solution one - 삼항 연산자 + pop(0)
# ================================================================================
def solution_mine_one(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    삼항 연산자로 올림을 계산하고 pop(0)으로 앞에서 추출하는 초기 풀이

    올림 계산:
        (100-p) % s가 있으면 +1 (나머지 존재 → 올림)
        없으면 그대로 (나누어떨어짐)

    한계:
        pop(0): 리스트 첫 원소 제거 → 나머지 원소 이동 → O(N)
        N번 반복 → 전체 O(N²)
    """
    answer = []
    days = [(100 - p) // s + 1 if (100 - p) % s else (100 - p) // s for p, s in zip(progresses, speeds)]

    while days:
        max_day = days.pop(0)       # O(N) — 앞 원소 제거 후 이동
        count = 1
        while days and days[0] <= max_day:
            days.pop(0)
            count += 1
        answer.append(count)

    return answer


# ================================================================================
# Mine solution two - math.ceil + [::-1] + pop()
# ================================================================================
def solution_mine_two(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    math.ceil로 올림, [::-1]로 뒤집어 pop() O(1)로 추출하는 풀이

    mine_one 대비 개선:
        math.ceil((100-p)/s): 삼항 연산자보다 간결 (/ 사용 주의)
        [::-1]: 1회성 O(N) 역순화 → 이후 pop()을 O(1)로 변환
        pop(0) O(N) × N번 → 1회 [::-1] O(N) + pop() O(1) × N번

    주의: math.ceil과 함께 반드시 / 사용
          math.ceil((100-p)//s): //는 이미 정수 → ceil 무의미
    """
    answer = []
    days = [math.ceil((100 - p) / s) for p, s in zip(progresses, speeds)][::-1]  # 뒤집어서 pop()을 O(1)로

    while days:
        max_day = days.pop()        # O(1) — 뒤에서 추출 (원래 앞 원소)
        count = 1
        while days and days[-1] <= max_day:
            days.pop()
            count += 1
        answer.append(count)

    return answer


# ================================================================================
# Mine solution three - 음수 트릭 올림 + deque
# ================================================================================
def solution_mine_three(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    음수 내림 트릭으로 라이브러리 없이 올림 계산하고 deque를 활용하는 풀이

    음수 내림 트릭:
        Python //는 음수에서 수학적 내림(floor) 적용
        (p-100)이 음수 → // 내림 → 음수화(-) 시 올림 효과
        -((p-100)//s): ceil((100-p)/s)와 동치
        예) p=96, s=5: (96-100)//5 = -4//5 = -1 → -(-1) = 1 ✓

    deque + popleft() O(1):
        mine_one의 pop(0) O(N) 대신 popleft() O(1) 사용
        mine_two의 [::-1] 트릭 없이도 O(1) 추출 가능
    """
    answer = []
    days = deque([-((p - 100) // s) for p, s in zip(progresses, speeds)])

    while days:
        max_day = days.popleft()    # O(1)
        count = 1
        while days and days[0] <= max_day:
            days.popleft()
            count += 1
        answer.append(count)

    return answer


# ================================================================================
# Mine solution four - 음수 트릭 + 포인터 방식 단일 for 순회
# ================================================================================
def solution_mine_four(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    days를 갱신하지 않고 포인터 방식으로 단일 for 순회하는 풀이

    핵심:
        max_day: 현재 배포 기준일 (앞 기능 완료일)
        count: 현재 배포에 포함되는 기능 수
        d > max_day: 새 배포 기준 → 현재까지 count 저장, 기준 갱신
        d ≤ max_day: 현재 배포에 포함 → count 증가

    mine_one 대비:
        days 갱신(pop) 없이 단일 for 순회
        마지막 count는 루프 종료 후 별도 append 필요
        (마지막 d 기준 배포가 루프 내 append 구문에 진입 불가)

    포인터 방식:
        max_day가 현재 배포 기준을 가리키는 포인터 역할
        days 원본 유지, 추가 자료구조 없음
    """
    answer = []
    days = [-((p - 100) // s) for p, s in zip(progresses, speeds)]

    max_day = days[0]
    count = 1

    for d in days[1:]:
        if d > max_day:
            answer.append(count)    # 현재 배포 마무리
            max_day = d             # 새 배포 기준
            count = 1
        else:
            count += 1              # 현재 배포에 포함

    answer.append(count)            # 마지막 배포 그룹 추가

    return answer


# ================================================================================
# Ref solution one - [d, count] 2차원 배열로 배포 그룹 관리
# ================================================================================
def solution_ref_one(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    [기준일, 개수] 2차원 배열로 배포 그룹을 관리하는 참고 풀이

    핵심:
        day_count: [[기준일, 개수], ...] 형태
        day_count[-1][0]: 현재 배포 기준일
        day_count[-1][1]: 현재 배포 기능 수
        d > day_count[-1][0]: 새 그룹 → [d, 1] 추가
        d ≤ day_count[-1][0]: 현재 그룹 → day_count[-1][1] += 1

    mine_four 대비:
        max_day/count 변수 → [d, count] 리스트로 묶어 관리
        가독성 측면에서 (일수, 개수)가 명시적으로 보임
        리스트 객체 생성 추가 비용, 불필요한 2차원 구조
    """
    day_count = []
    days = [-((p - 100) // s) for p, s in zip(progresses, speeds)]

    for d in days:
        if not day_count or day_count[-1][0] < d:
            day_count.append([d, 1])
        else:
            day_count[-1][1] += 1

    return [dc[1] for dc in day_count]


# ================================================================================
# Ref solution two - try-except + 인접 값 덮어쓰기
# ================================================================================
def solution_ref_two(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    try-except로 IndexError를 흐름 제어에 활용하는 참고 풀이

    핵심:
        daysLeft[i+1] = daysLeft[i]: 다음 값을 현재 기준으로 덮어씀
        인접 두 값 비교로 같은 배포 그룹 여부 판별
        IndexError 발생(마지막 i+1 접근 시) → except에서 마지막 count 추가

    두 가지 문제:
        1. 원본 데이터 변경: 순회 중 daysLeft 값 변경 → 데이터 오염
           다른 곳에서 원본이 필요하다면 버그 유발 가능

        2. try-except 오용:
           예외 처리는 예외적 상황을 위한 것
           무조건 발생하는 IndexError를 제어 흐름으로 사용
           → 조건문(if i < len(daysLeft) - 1:)이 올바른 방향
           EAFP(Easier to Ask Forgiveness than Permission) 철학의 오용 케이스
    """
    from math import ceil
    answer = []
    days_left = [ceil((100 - progresses[x]) / speeds[x]) for x in range(len(progresses))]
    count = 1

    for i in range(len(days_left)):
        try:
            if days_left[i] < days_left[i + 1]:
                answer.append(count)
                count = 1
            else:
                days_left[i + 1] = days_left[i]  # 다음 값을 현재 기준으로 덮어씀
                count += 1
        except IndexError:
            answer.append(count)    # 마지막 원소 처리 (항상 발생)

    return answer


# ================================================================================
# Best solution - 포인터 방식 단일 for 순회 (mine_four 주석 보강)
# ================================================================================
def solution_best(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    포인터 방식으로 단일 for 순회해 O(N) 시간에 처리하는 최적 풀이

    mine_four와 동일한 로직, 선정 근거 주석 보강:
        days 갱신(pop/popleft) 없이 순회만으로 처리
        추가 자료구조(deque) 불필요, 원본 days 유지
        음수 트릭: -((p-100)//s) = ceil((100-p)/s) (라이브러리 없이 올림)
        마지막 배포 그룹: 루프 후 answer.append(count) 1회 필수

    앞 기능이 기준인 이유:
        배포는 앞 기능 완료 기준 → max_day = 앞 기능 완료일
        뒤 기능이 더 빨리 완성돼도 앞 기능 완료 시점에 함께 배포
        d ≤ max_day → 앞 기능 완료 시점에 이미 완성 → 같이 배포
    """
    answer = []
    days = [-((p - 100) // s) for p, s in zip(progresses, speeds)]

    max_day = days[0]
    count = 1

    for d in days[1:]:
        if d > max_day:
            answer.append(count)
            max_day = d
            count = 1
        else:
            count += 1

    answer.append(count)
    return answer


# ================================================================================
# Sub solution - [::-1] + pop() (mine_two 주석 보강)
# ================================================================================
def solution_sub(progresses: list[int], speeds: list[int]) -> list[int]:
    """
    [::-1] 역순화 후 pop() O(1)로 앞 원소를 O(1) 추출하는 서브 풀이

    Best 대비 특징:
        while 루프 구조로 days를 갱신하며 처리
        [::-1] 1회 O(N) + pop() O(1): mine_one의 pop(0) O(N) 제거
        "days가 빌 때까지" 반복하는 구조가 직관적
        math.ceil((100-p)/s): 올림 계산 가독성 좋음 (/ 필수)
    """
    answer = []
    days = [math.ceil((100 - p) / s) for p, s in zip(progresses, speeds)][::-1]

    while days:
        max_day = days.pop()
        count = 1
        while days and days[-1] <= max_day:
            days.pop()
            count += 1
        answer.append(count)

    return answer


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[int], list[int], list[int]]] = [
        # (progresses, speeds, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # [93,30,55], [1,30,5]:
        #   days = [7, 3, 9]
        #   기준 7: 3≤7✓, 9>7 → [2], 기준 9: 끝 → [1]
        ([93, 30, 55], [1, 30, 5], [2, 1]),
        # [95,90,99,99,80,99], [1,1,1,1,1,1]:
        #   days = [5, 10, 1, 1, 20, 1]
        #   기준 5: 10>5 → [1]
        #   기준 10: 1≤10, 1≤10, 20>10 → [3]
        #   기준 20: 1≤20 → [2]
        ([95, 90, 99, 99, 80, 99], [1, 1, 1, 1, 1, 1], [1, 3, 2]),
        # 추가 케이스:
        # 모든 기능이 같은 날 완성
        # days = [1, 1, 1] → [3]
        ([99, 99, 99], [1, 1, 1], [3]),
        # 올림이 필요한 케이스
        # days = [1, 1] (ceil(0.8)=1, ceil(0.4)=1) → [2]
        ([96, 98], [5, 5], [2]),
    ]

    solutions = [
        ("Mine_one   (삼항+pop0)    ", solution_mine_one),
        ("Mine_two   (ceil+역순pop) ", solution_mine_two),
        ("Mine_three (음수+deque)   ", solution_mine_three),
        ("Mine_four  (음수+포인터)  ", solution_mine_four),
        ("Ref_one    (2차원배열)    ", solution_ref_one),
        ("Ref_two    (try-except)   ", solution_ref_two),
        ("Best       (음수+포인터)  ", solution_best),
        ("Sub        (ceil+역순pop) ", solution_sub),
    ]

    # 워밍업 스텝
    _p, _s, _ = test_cases[0]
    for _, func in solutions:
        func(_p[:], _s[:])

    print("=" * 70)
    print(f"{'풀이':<30} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 70)

    for name, func in solutions:
        for idx, (progresses, speeds, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(progresses[:], speeds[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<30} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 70)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
