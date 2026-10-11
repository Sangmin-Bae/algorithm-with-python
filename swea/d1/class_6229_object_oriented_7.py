"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6229. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 5. 객체지향 7
    유형       : OOP (클래스 상속, 메서드 오버라이딩)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcU_PF64nYDFAU4&categoryId=AWcU_PF64nYDFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=2
    풀이일자   : 2026-10-11
================================================================================
[문제 요약]
    부모 클래스 Person과 자식 클래스 Male, Female을 정의
    Person.getGender는 "Unknown"을 반환하고, 자식 클래스는 이를 오버라이딩해
    "Male", "Female"을 반환. 각 객체의 getGender 결과를 출력

    입력 방식 : 입력 없음
    적용 방식 : output(두 줄) → 두 문자열을 담은 리스트 ["Male", "Female"]을 반환
                제출 시에는 반환된 리스트의 원소를 한 줄씩 print
    참고      : 지문의 출력 예시에는 두 값 사이에 빈 줄이 표시되어 있으나
                실제 채점 출력의 빈 줄 여부는 확인하지 못함 (원문 코드로 제출 통과)
                메서드명 getGender는 지문이 지정 (PEP 8 관례는 get_gender지만 이름 유지)
================================================================================
[입출력 예시]
    공식 예시
    입력 | return
    -----|--------------------
    없음 | ["Male", "Female"]

    구조 검증 (손 계산, solution_comparison의 구조 검증 항목)
    확인 대상                           | 기대값
    ------------------------------------|---------
    Person().getGender()                | "Unknown"
    issubclass(Male, Person)            | True
    issubclass(Female, Person)          | True
    Male().getGender()                  | "Male"
    Female().getGender()                | "Female"
================================================================================
[풀이 전략]
    핵심: 상속 + 메서드 오버라이딩
        class Male(Person) : Person을 상속
        자식이 부모와 같은 이름의 메서드를 다시 정의하면 자식 객체는 자식의 메서드를 호출
        (메서드 탐색 순서: Male → Person → object, Male.__mro__로 확인)
        Person().getGender()는 "Unknown", Male()은 "Male", Female()은 "Female"

    풀이 구성:
        mine_one : 클래스 3개와 객체 생성을 solution() 함수 안에서 정의 (직접 작성한 풀이)
        best     : 클래스 3개를 함수 밖(모듈 수준)에서 한 번만 정의하고
                   solution()은 객체 생성과 호출만 수행
        Sub는 차별점 있는 변형이 없어 생략
        (객체 변수 없이 Male().getGender()로 쓰는 변형은 실측 차이가 노이즈 범위)

    함수 안 정의의 특성:
        solution()이 호출될 때마다 클래스 3개가 새로 만들어짐
        → 호출 간에 클래스가 공유되지 않음 (매번 서로 다른 Male 클래스)
        → 한 번만 실행하는 SWEA 제출에서는 영향 없음

    손 추적:
        M = Male()    → Male 객체
        F = Female()  → Female 객체
        M.getGender() : Male에 getGender가 있으므로 "Male"
        F.getGender() : Female에 getGender가 있으므로 "Female"
        → ["Male", "Female"] ✓

    SWEA 제출 형태 (클래스 정의와 함수 본문 아래에 이어 붙여 제출):
        for gender in solution_best():
            print(gender)

    제출 이력:
        solution_mine_one과 동일한 로직으로 SWEA 제출 테스트 통과 (2026-10-11)
        solution_best는 로컬 검증만 진행 (사이트 제출 전)
================================================================================
[실측 결과 — 클래스 정의 위치 비교]
    측정: 호출당 중앙값, Python 3.12.3 샌드박스 (python3.12 고정, 입력 크기 해당 없음)
          20,000회 x 15라운드 교차 측정

    방식                                   호출당     비율
    mine  함수 안에서 클래스 정의             18.55µs    1.000
    best  모듈 수준 클래스 + 객체 변수        0.306µs    0.017
    모듈 수준 클래스 + 객체 변수 생략          0.331µs    0.018

    해석:
        함수 안 정의는 호출마다 클래스 3개를 만드는 비용으로 약 60배 느림
        (세부 원인은 확인하지 않음)
        표준편차는 평균의 약 3~13%이고 모듈 수준 두 변형의 차이는 노이즈 범위
        단, 절대값이 마이크로초 단위라 한 번만 실행하는 문제에서는 의미 없음
        반복 호출되는 코드에서 클래스를 함수 안에 두면 비용이 누적된다는 점이 요점

    Best 선정 근거:
        - 클래스 정의는 한 번만 하고 호출은 재사용하는 일반적인 구조
        - 실측에서 함수 안 정의보다 약 60배 빠름
        - 지문이 요구하는 상속과 오버라이딩 구조가 함수 밖에서 직접 드러남
    일반성 대가:
        - best는 solution() 외부에 클래스 정의가 있어, 함수 본문만 따로 떼어 제출하면 NameError
          (제출 시 클래스 정의도 함께 붙여야 함)
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 있음 - 호출마다 클래스를 새로 만듦 (한 번 실행 환경에서는 무관)
    solution_best     : 클래스를 모듈 수준으로 이동 - Best (정의는 한 번만)
================================================================================
[복잡도 분석]
    Mine_one - 시간: O(1) | 공간: O(1) - 클래스 3개 생성 + 객체 2개 + 메서드 호출 2번
    Best     - 시간: O(1) | 공간: O(1) - 객체 2개 + 메서드 호출 2번 (클래스 생성은 1회만)

    입력 크기가 없는 문제라 점근 복잡도는 같고 상수 비용만 차이
"""

import time


# ================================================================================
# Mine solution one - 함수 안에서 클래스 정의
# ================================================================================
def solution_mine_one() -> list[str]:
    """
    Person, Male, Female 클래스를 함수 안에서 정의하고 각 객체의 getGender 결과를 리스트로 반환하는 직접 작성한 풀이

    핵심:
        Male, Female이 Person을 상속하고 getGender를 오버라이딩
        M.getGender() → "Male", F.getGender() → "Female"
        호출마다 클래스를 새로 만들기 때문에 호출 비용이 큼
    """
    class Person:
        def getGender(self):
            return "Unknown"

    class Male(Person):
        def getGender(self):
            return "Male"

    class Female(Person):
        def getGender(self):
            return "Female"

    M = Male()
    F = Female()

    return [M.getGender(), F.getGender()]


# ================================================================================
# Best solution 용 클래스 - 모듈 수준 정의 (한 번만 생성)
# ================================================================================
class Person:
    def getGender(self) -> str:
        return "Unknown"


class Male(Person):
    def getGender(self) -> str:
        return "Male"


class Female(Person):
    def getGender(self) -> str:
        return "Female"


# ================================================================================
# Best solution - 모듈 수준 클래스 + 객체 생성과 호출만 수행
# ================================================================================
def solution_best() -> list[str]:
    """
    모듈 수준에 정의된 클래스를 재사용해 각 객체의 getGender 결과를 리스트로 반환하는 풀이

    핵심:
        클래스는 모듈 로드 시 한 번만 생성
        solution()은 객체 생성과 메서드 호출만 수행
        실측에서 함수 안 정의보다 약 60배 빠름 (호출당 0.3µs 대 18.5µs)

    주의:
        함수 밖 클래스에 의존하므로 제출 시 클래스 정의도 함께 포함해야 함
    """
    M = Male()
    F = Female()

    return [M.getGender(), F.getGender()]


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (기댓값,) - 입력 없음, 손 계산
        (["Male", "Female"],),                                  # 공식 예시
    ]

    # 구조 검증: 반환값만으로는 확인되지 않는 지문 요구사항 (모듈 수준 클래스 대상)
    structure_checks: list[tuple[str, bool]] = [
        ("Person().getGender() == 'Unknown'", Person().getGender() == "Unknown"),
        ("Male은 Person의 자식 클래스",         issubclass(Male, Person)),
        ("Female은 Person의 자식 클래스",       issubclass(Female, Person)),
        ("Male이 getGender를 오버라이딩",       Male.getGender is not Person.getGender),
        ("Female이 getGender를 오버라이딩",     Female.getGender is not Person.getGender),
    ]

    solutions = [
        ("Mine (함수 안 정의)", solution_mine_one),
        ("Best (모듈 수준)",    solution_best),
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

    print("구조 검증 (모듈 수준 클래스)")
    for desc, ok in structure_checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {desc}")
    print("-" * 64)


# ================================================================================
# 실행 진입점
# ================================================================================
if __name__ == "__main__":
    solution_comparison()
