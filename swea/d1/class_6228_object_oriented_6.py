"""
================================================================================
[문제 정보]
    사이트     : SWEA (SW Expert Academy)
    레벨       : D1
    문제명     : 6228. [파이썬 프로그래밍 기초(2) 파이썬의 기본 응용] 5. 객체지향 6
    유형       : OOP (클래스 상속, 메서드 오버라이딩, 필드)
    링크       : https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWcU-ky64mkDFAU4&categoryId=AWcU-ky64mkDFAU4&categoryType=CODE&problemTitle=&orderBy=PASS_RATE&selectCodeLang=ALL&select-1=&pageSize=10&pageIndex=2
    풀이일자   : 2026-10-15
================================================================================
[문제 요약]
    부모 클래스 Shape(area는 0 반환)와 자식 클래스 Square를 정의
    Square는 length 필드를 가지며 area를 오버라이딩해 length * length를 반환
    길이 3인 정사각형의 면적을 출력

    입력 방식 : 입력 없음
    적용 방식 : output → 출력 문자열을 그대로 반환 ("정사각형의 면적: 9")
                제출 시에는 반환된 문자열을 print
    참고      : 길이 3은 지문 예시값이라 solution() 안에 고정
================================================================================
[입출력 예시]
    공식 예시
    입력 | return
    -----|----------------------
    없음 | "정사각형의 면적: 9"

    구조 검증 (손 계산, solution_comparison의 구조 검증 항목)
    확인 대상                    | 기대값
    -----------------------------|--------
    Shape().area()               | 0
    issubclass(Square, Shape)    | True
    Square.area is not Shape.area| True (오버라이딩)
    Square(3).length             | 3
    Square(1).area()             | 1
    Square(3).area()             | 9
    Square(4).area()             | 16
    Square(0).area()             | 0
    Square(-3).area()            | 9      ((-3) * (-3))
================================================================================
[풀이 전략]
    핵심: 상속 + 메서드 오버라이딩 + 인스턴스 필드
        class Square(Shape) : Shape를 상속
        __init__에서 length를 필드로 저장
        Shape.area()는 0, Square.area()는 length * length (자식이 같은 이름으로 재정의)
        Square(3).area()는 Square의 area가 호출되어 9
        (메서드 탐색 순서: Square → Shape → object)

    풀이 구성:
        mine_one : 클래스 2개와 객체 생성을 solution() 함수 안에서 정의 (직접 작성한 풀이)
                   필드는 self.__length (이름 변환), 면적은 length ** 2
        best     : 클래스 2개를 함수 밖(모듈 수준)에서 한 번만 정의, 필드는 self.length,
                   면적은 length * length (지문 표현 그대로)
        Sub는 차별점 있는 변형이 없어 생략
        (__slots__, f-string, 이름 변환 유지, ** 2 변형 모두 실측 차이가 노이즈 범위)

    이름 변환(name mangling) 주의:
        self.__length 는 클래스 안에서 self._Square__length 로 변환되어 저장
        → 외부에서 square.length 로 접근하면 AttributeError (hasattr(square, "length")는 False)
        지문은 "length 필드를 가진다"고 했으므로 best는 공개 필드 self.length 사용
        (이름 변환은 상속 시 이름 충돌을 막는 용도, 완전한 접근 차단은 아님)
        캡슐화 관례가 필요하면 _length(밑줄 하나) 또는 property를 사용

    ** 2 와 length * length:
        정수에서 결과 동일, 지문 표현은 length * length
        실측 차이는 노이즈 범위

    출력 포맷 "%d":
        %d 는 소수를 버림 (3.5 * 3.5 = 12.25 → "12"), f-string은 "12.25"
        지문의 길이가 정수 3이라 해당 없음

    함수 안 정의의 특성:
        solution()이 호출될 때마다 클래스가 새로 만들어짐 (매번 서로 다른 Square 클래스)
        → 한 번만 실행하는 SWEA 제출에서는 영향 없음

    손 추적:
        sq = Square(3)    → length = 3
        sq.area()         : Square에 area가 있으므로 length * length = 3 * 3 = 9
        "정사각형의 면적: %d" % 9 → "정사각형의 면적: 9" ✓

    SWEA 제출 형태 (클래스 정의와 함수 본문 아래에 이어 붙여 제출):
        print(solution_best())

    제출 이력:
        solution_mine_one과 동일한 로직으로 SWEA 제출 테스트 통과 (2026-10-15)
        solution_best는 로컬 검증만 진행 (사이트 제출 전)
================================================================================
[실측 결과 — 클래스 정의 위치와 표현 비교]
    측정: 호출당 중앙값, Python 3.12.3 샌드박스 (python3.12 고정, 입력 크기 해당 없음)
          20,000회 x 15라운드 교차 측정

    방식                                   호출당     mine 대비
    mine  함수 안 정의, __length, ** 2      13.50µs    1.000
    best  모듈 수준, length, 곱셈           0.449µs    0.033
    모듈 수준 + __length + ** 2             0.454µs    0.034
    모듈 수준 + length + ** 2               0.446µs    0.033
    best + __slots__                        0.440µs    0.033
    best + f-string                         0.414µs    0.031

    해석:
        함수 안 정의는 호출마다 클래스 2개를 만드는 비용으로 약 30배 느림
        (세부 원인은 확인하지 않음)
        모듈 수준 변형끼리의 차이(이름 변환, ** 2, __slots__, f-string)는 약 0~9%
        표준편차가 평균의 약 4~31%라 노이즈 범위 안
        절대값이 마이크로초 단위라 한 번만 실행하는 문제에서는 의미 없음

    Best 선정 근거:
        - 클래스 정의는 한 번만 하고 호출은 재사용하는 일반적인 구조 (약 30배 빠름)
        - 지문의 "length 필드"와 "length * length"를 그대로 반영 (성능 차이는 없음)
    일반성 대가:
        - best는 solution() 외부에 클래스 정의가 있어 함수 본문만 따로 제출하면 NameError
          (제출 시 클래스 정의도 함께 붙여야 함)
        - 공개 필드(length)는 외부에서 값을 바꿀 수 있음 (이름 변환보다 캡슐화가 약함)
================================================================================
[개선 포인트]
    solution_mine_one : 개선 여지 있음 - 호출마다 클래스를 새로 만들고, length 필드가 외부에서 접근 불가
    solution_best     : 클래스를 모듈 수준으로 이동 + 지문 표현 반영 - Best
================================================================================
[복잡도 분석]
    Mine_one - 시간: O(1) | 공간: O(1) - 클래스 2개 생성 + 객체 1개 + 메서드 호출 1번
    Best     - 시간: O(1) | 공간: O(1) - 객체 1개 + 메서드 호출 1번 (클래스 생성은 1회만)

    입력 크기가 없는 문제라 점근 복잡도는 같고 상수 비용만 차이
"""

import time


# ================================================================================
# Mine solution one - 함수 안에서 클래스 정의
# ================================================================================
def solution_mine_one() -> str:
    """
    Shape, Square 클래스를 함수 안에서 정의하고 정사각형 면적 문자열을 반환하는 직접 작성한 풀이

    핵심:
        Square가 Shape를 상속하고 area를 오버라이딩
        self.__length : 이름 변환으로 외부에서 length로 접근 불가
        "%d" % Squ.area() : 정수 포맷
        호출마다 클래스를 새로 만들기 때문에 호출 비용이 큼
    """
    class Shape:
        def area(self):
            return 0

    class Square(Shape):
        def __init__(self, length):
            self.__length = length

        def area(self):
            return self.__length ** 2

    Squ = Square(3)

    return "정사각형의 면적: %d" % Squ.area()


# ================================================================================
# Best solution 용 클래스 - 모듈 수준 정의 (한 번만 생성)
# ================================================================================
class Shape:
    def area(self) -> int:
        return 0


class Square(Shape):
    def __init__(self, length: int) -> None:
        self.length = length

    def area(self) -> int:
        return self.length * self.length


# ================================================================================
# Best solution - 모듈 수준 클래스 + 객체 생성과 호출만 수행
# ================================================================================
def solution_best() -> str:
    """
    모듈 수준에 정의된 클래스를 재사용해 정사각형 면적 문자열을 반환하는 풀이

    핵심:
        클래스는 모듈 로드 시 한 번만 생성
        self.length : 지문의 length 필드를 공개 필드로 구현
        length * length : 지문 표현 그대로
        실측에서 함수 안 정의보다 약 30배 빠름 (호출당 0.45µs 대 13.5µs)

    주의:
        함수 밖 클래스에 의존하므로 제출 시 클래스 정의도 함께 포함해야 함
    """
    sq = Square(3)

    return "정사각형의 면적: %d" % sq.area()


# ================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# ================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    repeat = 30

    test_cases: list[tuple] = [
        # (기댓값,) - 입력 없음, 손 계산
        ("정사각형의 면적: 9",),                                  # 공식 예시
    ]

    # 구조 검증: 반환 문자열만으로는 확인되지 않는 지문 요구사항 (모듈 수준 클래스 대상)
    structure_checks: list[tuple[str, bool]] = [
        ("Shape().area() == 0",              Shape().area() == 0),
        ("Square는 Shape의 자식 클래스",         issubclass(Square, Shape)),
        ("Square가 area를 오버라이딩",           Square.area is not Shape.area),
        ("Square(3).length == 3 (length 필드)", Square(3).length == 3),
        ("Square(1).area() == 1",             Square(1).area() == 1),
        ("Square(3).area() == 9",             Square(3).area() == 9),
        ("Square(4).area() == 16",            Square(4).area() == 16),
        ("Square(0).area() == 0",             Square(0).area() == 0),
        ("Square(-3).area() == 9",            Square(-3).area() == 9),
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
