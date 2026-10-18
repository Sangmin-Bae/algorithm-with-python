"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6208. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 5. 객체지향 2
    유형       : OOP (클래스, 정적 메서드 @staticmethod)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcU556a4g4DFAU4&categoryId=AWcU556a4g4DFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=3
    풀이일자   : 2026-10-18
================================================================================
[문제 요약]
    국적을 나타내는 정적 메서드 printNationality를 가진 Korean 클래스를 정의하고
    메서드를 호출해 결과를 두 줄 출력

    입력 방식 : 입력 없음
    적용 방식 : output(두 줄) → 두 문자열을 담은 리스트 ["대한민국", "대한민국"]을 반환
                제출 시에는 반환된 리스트의 원소를 한 줄씩 print
    참고      : 메서드명 printNationality는 지문이 지정 (PEP 8 관례는 print_nationality지만 이름 유지)
                메서드 이름은 print지만 작성한 풀이는 문자열을 반환하고 호출부에서 출력
                (출력 결과는 동일)
================================================================================
[입출력 예시]
    공식 예시
    입력 | return
    -----|-------------------------
    없음 | ["대한민국", "대한민국"]
================================================================================
[풀이 전략]
    핵심: @staticmethod
        정적 메서드는 인스턴스(self)나 클래스(cls)를 첫 인자로 받지 않는 메서드
        객체를 만들지 않고 클래스 이름으로 바로 호출: Korean.printNationality()
        (인스턴스로도 호출은 가능하나 지문의 의도는 클래스로 직접 호출)

    @staticmethod 유무에 따른 동작:
        데코레이터 있음 : 클래스로 호출, 인스턴스로 호출 모두 동작
        데코레이터 없음 : 클래스로 호출은 동작 (파이썬 3에서 클래스를 통해 접근한 함수는 그냥 함수)
                          인스턴스로 호출하면 TypeError (객체가 self로 자동 전달되어 인자 개수 불일치)
        → 데코레이터가 없으면 정적 메서드가 아니며, 클래스 호출이 되는 것은 우연한 동작

    staticmethod 와 classmethod:
        classmethod : 첫 인자로 클래스(cls)를 받음 → 클래스 상태 접근이 필요할 때
        staticmethod: 첫 인자 없음 → 클래스와 무관한 기능을 클래스 안에 묶어 둘 때

    풀이 구성:
        mine_one : 클래스 정의와 정적 메서드 호출 2번 (직접 작성한 풀이)
        best     : mine_one과 동일한 로직
                   (인스턴스 호출, 데코레이터 없음, classmethod, 한 번 호출 후 재사용 변형은
                    지문 의도와 다르거나 실측 차이가 노이즈 범위)
        Sub는 차별점 있는 변형이 없어 생략

    함수 안 정의의 특성:
        solution()이 호출될 때마다 클래스가 새로 만들어짐 (매번 서로 다른 Korean 클래스)
        → 한 번만 실행하는 SWEA 제출에서는 영향 없음

    손 추적:
        Korean.printNationality() : 객체 생성 없이 클래스로 호출 → "대한민국"
        두 번 호출 → ["대한민국", "대한민국"]
        → 출력 두 줄 "대한민국" ✓
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 작음 - 지문 의도를 그대로 구현, 호출마다 클래스를 새로 만드는 비용만 존재
    solution_best     : mine_one과 동일 로직 - Best
================================================================================
[복잡도 분석]
    Mine_one - 시간: O(1) | 공간: O(1) - 클래스 1개 생성 + 정적 메서드 호출 2번
    Best     - 시간: O(1) | 공간: O(1) - mine_one과 동일

    입력 크기가 없는 문제라 점근 복잡도는 같고 상수 비용만 차이
"""

import time


# ================================================================================
# Mine solution one - 클래스 정의 + 정적 메서드 호출
# ================================================================================
def solution_mine_one() -> list[str]:
    """
    Korean 클래스를 정의하고 정적 메서드를 두 번 호출한 결과를 리스트로 반환하는 직접 작성한 풀이

    핵심:
        @staticmethod : 객체 없이 클래스로 직접 호출 가능한 정적 메서드
        Korean.printNationality() 를 두 번 호출
        호출마다 클래스를 새로 만들기 때문에 호출 비용이 큼
    """
    class Korean:
        @staticmethod
        def printNationality():
            return "대한민국"

    return [Korean.printNationality(), Korean.printNationality()]


# ================================================================================
# Best solution - mine_one과 동일 로직
# ================================================================================
def solution_best() -> list[str]:
    """
    mine_one과 동일한 로직의 최적 풀이

    선정 근거:
        지문 의도를 바꾸지 않는 더 나은 변형이 없음
    """
    class Korean:
        @staticmethod
        def printNationality():
            return "대한민국"

    return [Korean.printNationality(), Korean.printNationality()]


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (기댓값,) - 입력 없음, 손 계산
        (["대한민국", "대한민국"],),                              # 공식 예시
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
