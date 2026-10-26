"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6225. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 5. 객체지향 5
    유형       : OOP (클래스, 생성자 __init__, 인스턴스 변수, 메서드)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcU-MXK4mADFAU4&categoryId=AWcU-MXK4mADFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=4
    풀이일자   : 2026-10-26
================================================================================
[문제 요약]
    가로, 세로 정보를 갖고 사각형의 면적을 계산하는 메서드를 갖는 Rectangle 클래스를 정의하고
    생성한 객체의 면적을 출력

    입력 방식 : 입력 없음
    적용 방식 : output → 출력 문자열을 그대로 반환 ("사각형의 면적: 20")
    참고      : 가로, 세로 값은 지문에 없고 출력(면적 20)만 주어짐, 가로 5, 세로 4 사용
================================================================================
[입출력 예시]
    공식 예시
    입력 | return
    -----|-------------------
    없음 | "사각형의 면적: 20"
================================================================================
[풀이 전략]
    핵심: 생성자 __init__ + 인스턴스 변수 + 메서드
        __init__(self, width, height) : 객체를 만들 때 가로, 세로를 받아 self에 저장
        area(self) : 저장된 가로, 세로로 면적(가로 * 세로)을 계산해 반환
        Rectangle(5, 4)로 객체를 만들고 area()를 호출

    인스턴스 변수와 클래스 변수:
        self.width = width : 인스턴스 변수, 객체마다 따로 저장
        클래스 변수는 클래스 본문에 직접 정의한 변수(width = 0)로 모든 객체가 공유
        가로, 세로는 사각형마다 다른 값이라 인스턴스 변수가 맞음

    풀이 구성:
        mine_one : 클래스 정의 + 객체 생성 + 면적 출력 문자열을 반환 (직접 작성한 풀이)
        best     : mine_one과 동일
                   (생성자를 직접 정의하는 것이 문제 의도라
                    dataclass처럼 생성자를 자동 생성하는 방식은 제외)
        Sub는 차별점 있는 변형이 없어 생략

    함수 안 정의의 특성:
        solution()이 호출될 때마다 클래스가 새로 만들어짐 (매번 서로 다른 Rectangle 클래스)

    손 추적:
        r = Rectangle(5, 4) → width = 5, height = 4
        r.area() → 5 * 4 = 20
        f"사각형의 면적: {20}" → "사각형의 면적: 20" ✓
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 작음 - 지문 요구(생성자, 메서드)를 그대로 구현
    solution_best     : mine_one과 동일 로직 - Best
================================================================================
[복잡도 분석]
    Mine_one - 시간: O(1) | 공간: O(1) - 클래스 1개 생성 + 객체 1개 + 메서드 호출 1번
    Best     - 시간: O(1) | 공간: O(1) - mine_one과 동일

    입력 크기가 없는 문제라 점근 복잡도는 같고 상수 비용만 차이
"""

import time


# ================================================================================
# Mine solution one - 클래스 정의 + 객체 생성
# ================================================================================
def solution_mine_one() -> str:
    """
    Rectangle 클래스를 함수 안에서 정의하고 면적 문자열을 반환하는 직접 작성한 풀이

    핵심:
        __init__ : 가로, 세로를 인스턴스 변수로 저장
        area : 가로 * 세로를 반환
        호출마다 클래스를 새로 만들기 때문에 호출 비용이 큼
    """
    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

    r = Rectangle(5, 4)

    return f"사각형의 면적: {r.area()}"


# ================================================================================
# Best solution - mine_one과 동일 로직
# ================================================================================
def solution_best() -> str:
    """
    mine_one과 동일한 로직의 최적 풀이

    선정 근거:
        지문 요구(생성자, 메서드)를 그대로 구현, 더 나은 변형이 없음
    """
    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

    r = Rectangle(5, 4)

    return f"사각형의 면적: {r.area()}"


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (기댓값,) - 입력 없음, 손 계산
        ("사각형의 면적: 20",),                                  # 공식 예시
    ]

    solutions = [
        ("Mine", solution_mine_one),
        ("Best", solution_best),
    ]

    # 워밍업: 첫 테스트 케이스로 모든 풀이를 1회씩 실행
    warmup_args = test_cases[0][:-1]
    for _, func in solutions:
        func(*warmup_args)

    print("=" * 64)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'평균 소요시간':>12}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (*args, expected) in enumerate(test_cases, 1):
            output = func(*args)

            start = time.perf_counter()
            for _ in range(repeat):
                func(*args)
            elapsed = (time.perf_counter() - start) / repeat

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed*1000:>10.4f}ms")
        print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
