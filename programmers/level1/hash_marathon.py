"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 완주하지 못한 선수
    유형       : Hash
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42576
    풀이일자   : 2026-09-03
===================================================================================
[문제 요약]
    참가자(participant)와 완주자(completion) 배열에서
    완주하지 못한 단 한 명의 이름 반환
    동명이인 존재 가능

    제약 조건
        - participant 길이: 1 이상 100,000 이하
        - completion 길이 = participant 길이 - 1
        - 이름: 1~20자 알파벳 소문자
===================================================================================
[입출력 예시]
    participant                          | completion                     | return
    -------------------------------------|--------------------------------|--------
    ["leo","kiki","eden"]                | ["eden","kiki"]                | "leo"
    ["mislav","stanko","mislav","ana"]   | ["stanko","ana","mislav"]      | "mislav"
===================================================================================
[동명이인 처리]
    set 불가: 중복 원소 허용 안 함
    dict(이름:인원수) 사용:
        completion 집계 후 participant 순회 시 count 감소
        count == 0이면 동명이인 중 완주자가 소진됨 → 미완주자

[Counter 뺄셈 원리]
    Counter(participant) - Counter(completion):
        동일 key의 value끼리 뺄셈
        결과 value > 0인 원소만 남음
        → 미완주자만 남은 Counter

    dict 방식 대비 느린 이유:
        집계 2번(participant, completion) + 차집합 = 3N 순회
        dict 방식: 집계 1번(completion) + 비교 1번 = 2N 순회

[sort+zip 방식]
    두 배열을 정렬 후 동시 순회:
        정렬 후 동명이인도 같은 위치에 정렬됨
        p != c인 첫 지점 = 미완주자
        zip이 completion 기준으로 끝남 → 마지막 원소가 기본 반환

    O(N log N): 정렬 비용으로 dict O(N)보다 느림
    하지만 해시 없이 정렬만으로 해결하는 독창적 발상

[ref — XOR 해시 방식]
    수학적 원리:
        a ^ a = 0 (같은 값 XOR → 0)
        a ^ 0 = a (0과 XOR → 자기 자신)

    participant 해시 전체 XOR ^ completion 해시 전체 XOR:
        짝이 있는 이름: hash(name) ^ hash(name) = 0으로 소거
        짝이 없는 미완주자: hash(name)만 남음

    hash_to_name[xor_sum]: 남은 해시값 → 이름 역매핑

    한계:
        해시 충돌 시 오답 (Python hash()는 충돌 가능)
        외부 hash() 명시적 호출 2N번 → dict보다 느림
        이론적으로 결함 있는 접근이나 실제 통과

[실측 결과 — N=100,000, 500회]
    one   (dict):     29.51ms  ← 가장 빠름
    ref   (XOR):      35.32ms
    two   (Counter-): 38.85ms
    three (sort+zip): 56.11ms  ← 가장 느림
===================================================================================
[내 초기 풀이]
    solution_mine_one:   dict + count 감소
    solution_mine_two:   Counter 뺄셈
    solution_mine_three: sort + zip

[개선 포인트]
    solution_mine_one:   개선 필요 없음 - Best
                         2N 순회로 가장 빠름
    solution_mine_two:   Counter - 연산으로 간결하나 3N 순회
    solution_mine_three: O(N log N) - Sub
                         해시 없이 정렬만으로 해결하는 독창적 발상
    solution_ref:        XOR 해시, 이론적 결함 있음
                         실무에서 사용 부적절
===================================================================================
[복잡도 분석]
    N = len(participant) (최대 100,000)

    Mine_one   - 시간: O(N) | 공간: O(N) - dict
    Mine_two   - 시간: O(N) | 공간: O(N) - Counter ×2
    Mine_three - 시간: O(N log N) | 공간: O(N) - sort
    Ref        - 시간: O(N) | 공간: O(N) - hash_to_name dict
    Best       - 시간: O(N) | 공간: O(N) - Mine_one과 동일
    Sub        - 시간: O(N log N) | 공간: O(N) - Mine_three와 동일
"""

from collections import Counter
import time


# =================================================================================
# Mine solution one - dict + count 감소
# =================================================================================
def solution_mine_one(participant: list[str], completion: list[str]) -> str:
    """
    completion을 dict로 집계하고 participant 순회 시 count 감소하는 초기 풀이

    동명이인 처리:
        c_dict[name] == 0: 동명이인 중 완주자가 소진됨
        → 같은 이름의 다음 참가자가 미완주자

    2N 순회: completion 집계 O(N) + participant 비교 O(N)
    """
    c_dict = {}

    for name in completion:
        c_dict[name] = c_dict.get(name, 0) + 1

    for name in participant:
        if name not in c_dict or c_dict[name] == 0:
            return name
        c_dict[name] -= 1

    return ""


# =================================================================================
# Mine solution two - Counter 뺄셈
# =================================================================================
def solution_mine_two(participant: list[str], completion: list[str]) -> str:
    """
    Counter 뺄셈으로 미완주자를 추출하는 파이써닉한 풀이

    Counter - Counter:
        동일 key의 value끼리 뺄셈
        결과 value <= 0인 원소는 제거됨
        → 미완주자(value=1)만 남은 Counter

    next(iter(answer)):
        list(answer.keys())[0] 대비 리스트 생성 없이 첫 키 추출

    3N 순회(집계 2번 + 차집합)로 mine_one보다 느림
    """
    answer = Counter(participant) - Counter(completion)
    return next(iter(answer))


# =================================================================================
# Mine solution three - sort + zip
# =================================================================================
def solution_mine_three(participant: list[str], completion: list[str]) -> str:
    """
    정렬 후 동시 순회로 불일치 지점을 찾는 풀이

    정렬 후 동시 순회:
        동명이인도 정렬 후 같은 위치에 배치됨
        p != c인 첫 지점 = 미완주자
        zip은 completion(짧은 쪽) 기준으로 종료
        → participant[-1]이 기본 반환값

    O(N log N): 정렬 비용으로 dict O(N)보다 느림
    해시 없이 정렬만으로 해결하는 독창적 발상
    """
    participant.sort()
    completion.sort()

    for p, c in zip(participant, completion):
        if p != c:
            return p

    return participant[-1]


# =================================================================================
# Ref solution - XOR 해시
# =================================================================================
def solution_ref(participant: list[str], completion: list[str]) -> str:
    """
    XOR 해시로 미완주자를 추출하는 참고 풀이

    XOR 성질 활용:
        a ^ a = 0 (짝 소거)
        a ^ 0 = a (나머지)

    participant 전체 XOR ^ completion 전체 XOR:
        = 짝이 없는 미완주자 해시값

    hash_to_name[xor_sum]: 해시값 → 이름 역매핑

    한계:
        해시 충돌 시 오답 (Python hash() 충돌 가능)
        실무 코드에서 사용 부적절
        외부 hash() 명시적 호출 2N번으로 dict보다 느림
    """
    xor_sum = 0
    hash_to_name = {}

    for p in participant:
        h = hash(p)
        hash_to_name[h] = p
        xor_sum ^= h

    for c in completion:
        xor_sum ^= hash(c)

    return hash_to_name[xor_sum]


# =================================================================================
# Best solution - dict + count 감소 (mine_one 주석 보강)
# =================================================================================
def solution_best(participant: list[str], completion: list[str]) -> str:
    """
    dict 2N 순회로 O(N) 시간, O(N) 공간에 미완주자를 찾는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        2N 순회: Counter(3N), sort(N log N) 대비 가장 적은 순회
        실측 N=100,000: 29.51ms (Counter 38.85ms, sort 56.11ms 대비 우위)
        동명이인 처리: count 감소로 명확하게 처리
    """
    c_dict = {}

    for name in completion:
        c_dict[name] = c_dict.get(name, 0) + 1

    for name in participant:
        if name not in c_dict or c_dict[name] == 0:
            return name
        c_dict[name] -= 1

    return ""


# =================================================================================
# Sub solution - sort + zip (mine_three 주석 보강)
# =================================================================================
def solution_sub(participant: list[str], completion: list[str]) -> str:
    """
    정렬 후 동시 순회로 해시 없이 미완주자를 찾는 서브 풀이

    mine_three와 동일한 로직, 선정 근거 주석 보강:
        해시 자료구조 없이 정렬만으로 해결하는 독창적 발상
        동명이인 자동 처리: 정렬 후 같은 위치에 배치됨
        zip 종료 조건: completion이 짧아 participant[-1]이 기본 반환
        O(N log N)으로 Best보다 느리나 공간 복잡도 유사
    """
    participant.sort()
    completion.sort()

    for p, c in zip(participant, completion):
        if p != c:
            return p

    return participant[-1]


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (participant, completion, 기댓값)
        # 공식 예시
        (["leo", "kiki", "eden"],                    ["eden", "kiki"],                     "leo"),
        (["marina","josipa","nikola","vinko","filipa"],["josipa","filipa","marina","nikola"],"vinko"),
        (["mislav","stanko","mislav","ana"],          ["stanko","ana","mislav"],             "mislav"),
        # 추가 케이스:
        # 단일 참가자
        (["solo"],                                    [],                                    "solo"),
    ]

    solutions = [
        ("Mine_one   (dict)    ", solution_mine_one),
        ("Mine_two   (Counter) ", solution_mine_two),
        ("Mine_three (sort+zip)", solution_mine_three),
        ("Ref        (XOR)     ", solution_ref),
        ("Best       (dict)    ", solution_best),
        ("Sub        (sort+zip)", solution_sub),
    ]

    # 워밍업 스텝
    _p, _c, _ = test_cases[0]
    for _, func in solutions:
        func(_p[:], _c[:])

    print("=" * 66)
    print(f"{'풀이':<24} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (participant, completion, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(participant[:], completion[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<24} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
