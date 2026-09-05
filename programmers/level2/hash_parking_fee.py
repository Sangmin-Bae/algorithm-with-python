"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 주차 요금 계산
    유형       : Hash / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/92341
    풀이일자   : 2026-09-05
===================================================================================
[문제 요약]
    요금표 fees와 입출차 기록 records가 주어질 때
    차량 번호 오름차순으로 주차 요금을 배열에 담아 반환

    요금 계산:
        누적 시간 ≤ 기본 시간: 기본 요금
        누적 시간 > 기본 시간: 기본 요금 + ⌈(누적-기본)/단위시간⌉ × 단위 요금

    제약 조건
        - records 길이: 1 이상 1,000 이하
        - 시각 기준 오름차순으로 주어짐
        - 입차 후 당일 미출차 시 23:59 출차로 간주 (1439분)
===================================================================================
[입출력 예시]
    fees           | result
    ---------------|---------------------
    [180,5000,10,600]| [14600, 34400, 5000]
    [120,0,60,591]   | [0, 591]
    [1,461,1,10]     | [14841]
===================================================================================
[스택이 아닌 딕셔너리를 선택한 이유]
    스택(LIFO): 맨 위만 접근 가능
        여러 차량이 섞여 있을 때 특정 차량 번호를 꺼낼 수 없음

    딕셔너리: 차량 번호(key)로 O(1) 직접 접근
        parking[car_num] = 입차 시각
        OUT 만나면 pop()으로 입차 시각 추출 → 주차 시간 계산

[parking.pop(car_num) 설계]
    pop()으로 꺼내면 parking에서 해당 차량 제거
    → parking.items() 순회 시 미출차 차량만 남음 보장

[ref — 정렬 + 투포인터]
    (차량 번호, 시각, 내역) 튜플 정렬:
        차량 번호 오름차순 → 같은 번호 안에서 시각 오름차순
        IN → OUT 순서는 지문 조건("시각 기준 오름차순")으로 보장

    정렬 후 IN/OUT 순서:
        같은 차량 번호 내 시각 오름차순 → IN이 OUT보다 먼저
        "IN 다음에 OUT"이 정렬로 만들어지는 게 아니라
        지문 조건에서 이미 보장됨

    투포인터 구조:
        외부 while: 전체 기록 i가 N에 도달할 때까지
        내부 while: 현재 차량 번호가 같은 기록을 처리
        i+1이 같은 차량의 OUT이면 → i += 2
        아니면 → 미출차 처리 i += 1

    dict 없이 정렬만으로 해결 → 독창적 발상

[실측 결과 — 50,000회]
    mine (dict): 6.2μs
    ref  (sort): 6.3μs  (records 최대 1,000개로 차이 없음)
===================================================================================
[내 초기 풀이]
    solution_mine: dict (parking + total_time)

[개선 포인트]
    solution_mine: 개선 필요 없음 - Best
                   직관적, 간결, 실측 동률
    solution_ref:  정렬+투포인터 - Sub
                   dict 없이 정렬만으로 차량별 집계
===================================================================================
[복잡도 분석]
    N = len(records) (최대 1,000)
    C = 차량 수 (최대 N/2)

    Mine - 시간: O(N + C log C) | 공간: O(C) - dict + sorted
    Ref  - 시간: O(N log N + C) | 공간: O(N) - parsed_records 정렬
    Best - 시간: O(N + C log C) | 공간: O(C) - Mine과 동일
    Sub  - 시간: O(N log N + C) | 공간: O(N) - Ref와 동일
"""

import math
import time


# =================================================================================
# Mine solution - dict 기반 (parking + total_time)
# =================================================================================
def solution_mine(fees: list[int], records: list[str]) -> list[int]:
    """
    두 딕셔너리로 입차 중 차량과 누적 시간을 분리 관리하는 초기 풀이

    parking: {차량번호: 입차 시각(분)}
        OUT 만나면 pop()으로 입차 시각 추출 → 미출차 차량만 잔류

    total_time: {차량번호: 누적 주차 시간(분)}
        복수 입출차 차량도 누적 관리

    미출차 처리:
        parking에 남은 차량 → 1439 - in_time으로 당일 종료 시각 처리

    정렬:
        sorted(total_time.keys())로 차량 번호 오름차순 정렬
    """
    base_time, base_fee, unit_time, unit_fee = fees

    def get_minutes(t: str) -> int:
        h, m = t.split(':')
        return int(h) * 60 + int(m)

    parking = {}
    total_time = {}

    for record in records:
        time_str, car_num, status = record.split()
        time_int = get_minutes(time_str)

        if status == "IN":
            parking[car_num] = time_int
        else:
            in_time = parking.pop(car_num)
            total_time[car_num] = total_time.get(car_num, 0) + (time_int - in_time)

    for car_num, in_time in parking.items():
        total_time[car_num] = total_time.get(car_num, 0) + (1439 - in_time)

    answer = []
    for car_num in sorted(total_time.keys()):
        t = total_time[car_num]
        if t <= base_time:
            answer.append(base_fee)
        else:
            answer.append(base_fee + math.ceil((t - base_time) / unit_time) * unit_fee)

    return answer


# =================================================================================
# Ref solution - 정렬 + 투포인터
# =================================================================================
def solution_ref(fees: list[int], records: list[str]) -> list[int]:
    """
    정렬 후 투포인터로 차량별 주차 시간을 집계하는 참고 풀이

    (차량번호, 시각, 내역) 튜플 정렬:
        차량번호 오름차순 → 같은 번호 안에서 시각 오름차순
        IN → OUT 순서는 지문 조건으로 이미 보장

    투포인터 구조:
        외부 while: 포인터 i가 N에 도달할 때까지 전체 기록 순회
        내부 while: 현재 차량 번호가 같은 기록을 모두 처리

    IN 처리:
        i+1이 같은 차량의 OUT이면 → 두 시각 차이 누적, i+=2
        아니면 → 미출차(1439-입차시각) 누적, i+=1

    dict 없이 정렬만으로 해결하는 독창적 접근
    """
    base_time, base_fee, unit_time, unit_fee = fees

    def get_minutes(t: str) -> int:
        h, m = t.split(':')
        return int(h) * 60 + int(m)

    parsed_records = []
    for record in records:
        time_str, car_num, status = record.split()
        parsed_records.append((car_num, get_minutes(time_str), status))

    parsed_records.sort()

    answer = []
    i = 0
    N = len(parsed_records)

    while i < N:
        current_car = parsed_records[i][0]
        total_duration = 0

        while i < N and parsed_records[i][0] == current_car:
            car_num, time_int, status = parsed_records[i]

            if status == "IN":
                if (i + 1 < N
                        and parsed_records[i + 1][0] == current_car
                        and parsed_records[i + 1][2] == "OUT"):
                    total_duration += parsed_records[i + 1][1] - time_int
                    i += 2
                else:
                    total_duration += 1439 - time_int
                    i += 1

        if total_duration <= base_time:
            answer.append(base_fee)
        else:
            answer.append(
                base_fee + math.ceil((total_duration - base_time) / unit_time) * unit_fee
            )

    return answer


# =================================================================================
# Best solution - dict 기반 (mine 주석 보강)
# =================================================================================
def solution_best(fees: list[int], records: list[str]) -> list[int]:
    """
    두 딕셔너리로 직관적이고 간결하게 주차 요금을 계산하는 최적 풀이

    mine과 동일한 로직, 선정 근거 주석 보강:
        parking.pop(): 미출차 차량 자동 분리 보장
        total_time.get(car, 0): 복수 입출차 차량 누적 처리
        실측 ref와 동률 (records ≤ 1,000으로 차이 없음)
        코드 간결성 기준으로 Best 선정
    """
    base_time, base_fee, unit_time, unit_fee = fees

    def get_minutes(t: str) -> int:
        h, m = t.split(':')
        return int(h) * 60 + int(m)

    parking = {}
    total_time = {}

    for record in records:
        time_str, car_num, status = record.split()
        time_int = get_minutes(time_str)

        if status == "IN":
            parking[car_num] = time_int
        else:
            in_time = parking.pop(car_num)
            total_time[car_num] = total_time.get(car_num, 0) + (time_int - in_time)

    for car_num, in_time in parking.items():
        total_time[car_num] = total_time.get(car_num, 0) + (1439 - in_time)

    answer = []
    for car_num in sorted(total_time.keys()):
        t = total_time[car_num]
        if t <= base_time:
            answer.append(base_fee)
        else:
            answer.append(base_fee + math.ceil((t - base_time) / unit_time) * unit_fee)

    return answer


# =================================================================================
# Sub solution - 정렬 + 투포인터 (ref 주석 보강)
# =================================================================================
def solution_sub(fees: list[int], records: list[str]) -> list[int]:
    """
    정렬 + 투포인터로 dict 없이 차량별 주차 시간을 집계하는 서브 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        정렬로 차량번호 오름차순 + 시각 오름차순 자동 확보
        dict 없이 포인터만으로 IN/OUT 쌍을 처리
        O(N log N) 정렬 비용으로 Best O(N + C log C)보다 이론상 불리
        그러나 records ≤ 1,000으로 실측 동률
    """
    base_time, base_fee, unit_time, unit_fee = fees

    def get_minutes(t: str) -> int:
        h, m = t.split(':')
        return int(h) * 60 + int(m)

    parsed_records = []
    for record in records:
        time_str, car_num, status = record.split()
        parsed_records.append((car_num, get_minutes(time_str), status))

    parsed_records.sort()

    answer = []
    i = 0
    N = len(parsed_records)

    while i < N:
        current_car = parsed_records[i][0]
        total_duration = 0

        while i < N and parsed_records[i][0] == current_car:
            car_num, time_int, status = parsed_records[i]

            if status == "IN":
                if (i + 1 < N
                        and parsed_records[i + 1][0] == current_car
                        and parsed_records[i + 1][2] == "OUT"):
                    total_duration += parsed_records[i + 1][1] - time_int
                    i += 2
                else:
                    total_duration += 1439 - time_int
                    i += 1

        if total_duration <= base_time:
            answer.append(base_fee)
        else:
            answer.append(
                base_fee + math.ceil((total_duration - base_time) / unit_time) * unit_fee
            )

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases = [
        # (fees, records, 기댓값)
        # 공식 예시
        ([180, 5000, 10, 600],
         ["05:34 5961 IN", "06:00 0000 IN", "06:34 0000 OUT",
          "07:59 5961 OUT", "07:59 0148 IN", "18:59 0000 IN",
          "19:09 0148 OUT", "22:59 5961 IN", "23:00 5961 OUT"],
         [14600, 34400, 5000]),
        ([120, 0, 60, 591],
         ["16:00 3961 IN", "16:00 0202 IN", "18:00 3961 OUT",
          "18:00 0202 OUT", "23:58 3961 IN"],
         [0, 591]),
        ([1, 461, 1, 10],
         ["00:00 1234 IN"],
         [14841]),
        # 추가 케이스:
        # 미출차 없음
        ([60, 1000, 10, 100],
         ["00:00 0001 IN", "01:00 0001 OUT"],
         [1000]),
    ]

    solutions = [
        ("Mine (dict)       ", solution_mine),
        ("Ref  (sort+2ptr)  ", solution_ref),
        ("Best (dict)       ", solution_best),
        ("Sub  (sort+2ptr)  ", solution_sub),
    ]

    # 워밍업 스텝
    _f, _r, _ = test_cases[0]
    for _, func in solutions:
        func(_f, _r)

    print("=" * 64)
    print(f"{'풀이':<20} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (fees, records, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(fees, records[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<20} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
