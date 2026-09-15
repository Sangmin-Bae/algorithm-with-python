"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : [PCCE 기출문제] 10번 / 데이터 분석
    유형       : Hash / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/250121
    풀이일자   : 2026-09-15
===================================================================================
[문제 요약]
    data에서 ext 컬럼이 val_ext보다 작은 행을 필터링하고
    sort_by 컬럼 기준 오름차순 정렬 반환

    컬럼 구조: code(0), date(1), maximum(2), remain(3)

    제약 조건
        - data 길이: 1 이상 500 이하
        - ext, sort_by: "code", "date", "maximum", "remain" 중 하나
===================================================================================
[입출력 예시]
    data                                              | ext    | val_ext  | sort_by | result
    --------------------------------------------------|--------|----------|---------|-------
    [[1,20300104,100,80],[2,20300804,847,37],          | "date" | 20300501 | "remain"| [[3,20300401,10,8],
     [3,20300401,10,8]]                               |        |          |         |  [1,20300104,100,80]]
===================================================================================
[핵심 — 컬럼명 → 인덱스 매핑]
    ext, sort_by가 문자열로 주어짐
    → 데이터 인덱스로 변환 필요

    딕셔너리(mine): O(1) 해시 탐색
    리스트 index()(ref): O(4) 선형 탐색 (크기 4, 실질 O(1))

[풀이가 한 줄인 이유]
    필터링: 리스트 컴프리헨션 [d for d in data if 조건]
    정렬:   sorted(... , key=lambda x: x[인덱스])
    체이닝: sorted(필터링 결과, key=...) 단일 표현식

[딕셔너리 생성 비용 vs index() 탐색]
    mine: dict 객체 생성 (4 k-v 쌍) → 비용 발생
    ref:  list 4원소 생성 + index() O(4) 탐색

    실측: ref 19.9μs, mine 30.7μs
    dict 객체 생성 비용이 index() O(4) 탐색보다 큼

    개선 방법: TABLE을 모듈 레벨 상수로 이동
        TABLE = {"code": 0, "date": 1, "maximum": 2, "remain": 3}
        → 생성 비용 1회만 발생

    data 500개 × sorted 비용이 지배적 → 실질 차이 무의미
    코드 가독성/유지보수 기준으로 dict 선택

[세션에서 쌓인 패턴의 합산]
    sorted + key lambda → 추억 점수, 실패율 등
    컬럼 매핑 dict → 대충 만든 자판
    리스트 컴프리헨션 필터링 → 세션 전반
===================================================================================
[내 초기 풀이]
    solution_mine: dict 컬럼 매핑 + 한 줄 체이닝

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
                   dict로 의도 명확, 컬럼 확장 시 유지보수 용이
    solution_ref:  list index() - Sub
                   구조 단순, 실측 약간 빠름 (dict 생성 비용 없음)
===================================================================================
[복잡도 분석]
    N = len(data) (최대 500), 컬럼 수 = 4 고정

    Mine - 시간: O(N log N) | 공간: O(N) - 정렬이 지배
    Ref  - 시간: O(N log N) | 공간: O(N) - Mine과 동일
    Best - 시간: O(N log N) | 공간: O(N) - Mine과 동일
    Sub  - 시간: O(N log N) | 공간: O(N) - Ref와 동일
"""

import time

# 모듈 레벨 상수: 함수 호출마다 재생성 없음
TABLE = {"code": 0, "date": 1, "maximum": 2, "remain": 3}


# =================================================================================
# Mine solution - dict 컬럼 매핑
# =================================================================================
def solution_mine(data: list[list[int]], ext: str, val_ext: int, sort_by: str) -> list[list[int]]:
    """
    딕셔너리로 컬럼명→인덱스를 O(1)로 매핑하고 한 줄 체이닝으로 처리하는 초기 풀이

    table:
        컬럼명을 인덱스로 변환 → O(1) 해시 탐색
        의도가 명확, 컬럼 추가 시 딕셔너리 항목만 추가

    sorted + 리스트 컴프리헨션 체이닝:
        필터링 + 정렬을 단일 표현식으로
    """
    table = {
        "code": 0,
        "date": 1,
        "maximum": 2,
        "remain": 3
    }

    return sorted([d for d in data if d[table[ext]] < val_ext],
                  key=lambda x: x[table[sort_by]])


# =================================================================================
# Ref solution - list index() 컬럼 탐색
# =================================================================================
def solution_ref(data: list[list[int]], ext: str, val_ext: int, sort_by: str) -> list[list[int]]:
    """
    리스트 index()로 컬럼명→인덱스를 탐색하는 참고 풀이

    columns.index(ext): O(4) 선형 탐색
        크기 4 고정 → 실질 O(1)
        dict 객체 생성 비용 없음 → 실측 mine보다 약간 빠름

    data 최대 500개 × sorted가 지배적
    → 두 방식 차이 무의미
    """
    columns = ["code", "date", "maximum", "remain"]
    ext_idx = columns.index(ext)
    sort_idx = columns.index(sort_by)

    return sorted([d for d in data if d[ext_idx] < val_ext],
                  key=lambda x: x[sort_idx])


# =================================================================================
# Best solution - 모듈레벨 TABLE 상수 (mine 개선)
# =================================================================================
def solution_best(data: list[list[int]], ext: str, val_ext: int, sort_by: str) -> list[list[int]]:
    """
    모듈 레벨 TABLE 상수로 dict 생성 비용을 제거한 최적 풀이

    mine 대비 개선:
        TABLE을 함수 밖 모듈 레벨에 정의
        → 함수 호출마다 dict 재생성 없음
        → LOAD_GLOBAL이지만 4원소 dict → 오버헤드 미미

    mine의 가독성 장점 + 생성 비용 제거
    """
    return sorted([d for d in data if d[TABLE[ext]] < val_ext],
                  key=lambda x: x[TABLE[sort_by]])


# =================================================================================
# Sub solution - list index() (ref 주석 보강)
# =================================================================================
def solution_sub(data: list[list[int]], ext: str, val_ext: int, sort_by: str) -> list[list[int]]:
    """
    리스트 index()로 컬럼 인덱스를 찾는 서브 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        구조 단순, dict 객체 생성 없음
        O(4) index() 탐색이지만 크기 4 고정으로 실질 O(1)
        실측 dict보다 약간 빠르나 data 500개 × sorted 비용에 묻힘
    """
    columns = ["code", "date", "maximum", "remain"]
    ext_idx = columns.index(ext)
    sort_idx = columns.index(sort_by)

    return sorted([d for d in data if d[ext_idx] < val_ext],
                  key=lambda x: x[sort_idx])


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (data, ext, val_ext, sort_by, 기댓값)
        # 공식 예시
        ([[1, 20300104, 100, 80], [2, 20300804, 847, 37], [3, 20300401, 10, 8]],
         "date", 20300501, "remain",
         [[3, 20300401, 10, 8], [1, 20300104, 100, 80]]),
        # 추가 케이스:
        # code 기준 필터링 + date 정렬
        ([[1, 20300104, 100, 80], [2, 20300804, 847, 37], [3, 20300401, 10, 8]],
         "code", 3, "date",
         [[1, 20300104, 100, 80], [2, 20300804, 847, 37]]),
        # remain 기준 필터링 + maximum 정렬
        ([[1, 20300104, 100, 80], [2, 20300804, 847, 37], [3, 20300401, 10, 8]],
         "remain", 50, "maximum",
         [[3, 20300401, 10, 8], [2, 20300804, 847, 37]]),
    ]

    solutions = [
        ("Mine (dict 로컬)    ", solution_mine),
        ("Ref  (list index)   ", solution_ref),
        ("Best (dict 모듈레벨)", solution_best),
        ("Sub  (list index)   ", solution_sub),
    ]

    # 워밍업 스텝
    _d, _e, _v, _s, _ = test_cases[0]
    for _, func in solutions:
        func(_d, _e, _v, _s)

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (data, ext, val_ext, sort_by, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(data, ext, val_ext, sort_by)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
