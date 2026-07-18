"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 옹알이 (2)
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/133499
    풀이일자   : 2026-07-18
===================================================================================
[문제 요약]
    babbling 배열의 각 단어가 ("aya", "ye", "woo", "ma")로만 구성되고
    같은 발음이 연속으로 오지 않는 단어의 개수 반환

    제약 조건
        - babbling 길이: 1 이상 100 이하
        - babbling[i] 길이: 1 이상 30 이하
        - 소문자 알파벳으로만 구성
===================================================================================
[입출력 예시]
    babbling                                     | result
    ---------------------------------------------|-------
    ["aya", "yee", "u", "maa"]                   | 1
    ["ayaye","uuu","yeye","yemawoo","ayaayaa"]   | 2
===================================================================================
[solution_one — replace 공백 치환 트릭]
    핵심: 발음 p를 " " 공백으로 치환
        빈 문자열("")로 치환 시 문제:
            "yayae": aya 제거 → "yye" → ye 제거 → "y" ≠ "" → 탈락 (우연히 맞음)
            "yeaye": ye 제거 → "aye" → aya 탐색 실패 → "aye" ≠ "" → 탈락 (맞음)
            하지만 "ayaye": aya 제거 → "ye" → ye 제거 → "" → 통과 (오류!)
                    "ayaye"는 aya+ye 조합이라 실제 발음 가능하므로 통과가 맞음

        공백(" ")으로 치환 시:
            "yayae": aya 제거 → "y e" → strip 후 "y e" ≠ "" → 탈락
            치환 후 남은 발음 불가 문자가 공백 사이에 드러남

    이중 발음 사전 정의 이유:
        replace가 탐욕적(greedy)으로 왼쪽부터 적용
        먼저 이중 발음(ayaaya 등)을 포함하면 제외하는 방식

    "yeyeye" 처리:
        is_double 체크: "yeye"가 "yeyeye" 안에 부분 문자열로 존재 → True → 제외
        3회 이상 연속도 "yeye"가 포함되므로 자동으로 탐지됨

[solution_two — 문자 단위 포인터 방식]
    curr_p 버퍼에 문자를 하나씩 추가하며 발음 set에 있는지 확인
    발음 매칭 시 prev_p와 비교 → 연속 발음 감지

    사전 이중 발음 정의 불필요:
        prev_p == curr_p 비교로 연속 발음을 동적으로 탐지

    최종 조건 is_double == False and curr_p == "":
        is_double: 연속 발음 없음
        curr_p == "": 모든 문자가 발음으로 소진됨 (남은 발음 불가 문자 없음)

[solution_three — 부정형 전방 탐색 정규표현식]
    ^(aya(?!aya)|ye(?!ye)|woo(?!woo)|ma(?!ma))+$
        ^...$:   단어 전체 매칭
        (...)+:  하나 이상의 발음 그룹
        A(?!B):  부정형 전방 탐색 — "A 뒤에 B가 오면 해당 위치에서 매칭 실패"
                 위치만 확인하고 문자를 소비하지 않음 (위치 이동 없음)

    "바로 None 반환"이 아닌 정확한 동작:
        aya(?!aya) 실패 시 → ye(?!ye), woo(?!woo), ma(?!ma) 대안 탐색
        전부 실패 후 $ 미도달 시 최종 None 반환

    re.compile로 패턴 사전 컴파일 → 반복 사용 시 컴파일 1회 비용 분산

    소규모 제약(babbling ≤ 100, 단어 ≤ 30)에서 초기 컴파일 오버헤드 불리
    대규모 데이터(만 단위 이상)에서는 풀이 1, 2보다 유리할 수 있음

    소규모 제약(babbling ≤ 100, 단어 ≤ 30)에서 초기 컴파일 오버헤드 불리
    대규모 데이터(만 단위 이상)에서는 풀이 1, 2보다 유리할 수 있음
===================================================================================
[내 초기 풀이]
    solution_mine_one  : replace 공백 치환 + 이중 발음 사전 정의
    solution_mine_two  : 문자 단위 포인터 + set 발음 비교
    solution_mine_three: 부정형 전방 탐색 정규표현식

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub
                         직관적, 이중 발음 사전 정의로 명확
                         "yeyeye" 등 N회 연속도 "yeye" 부분 문자열로 탐지
    solution_mine_two  : 개선 필요 없음 - Best
                         이중 발음 사전 정의 불필요, 문자 단위 O(N×M)
                         prev_p == curr_p로 연속 발음 동적 탐지
    solution_mine_three: 학습 목적 — 정규표현식 부정형 전방 탐색 패턴
                         소규모 제약에서 오버헤드 불리
===================================================================================
[복잡도 분석]
    N = len(babbling) (최대 100)
    M = len(babbling[i]) (최대 30)
    P = 발음 종류 수 (4, 상수)
    L = 발음 최대 길이 (3, 상수)

    Mine_one   - 시간: O(N×P×M) | 공간: O(M) - replace O(M) × P번
    Mine_two   - 시간: O(N×M)   | 공간: O(1) - 문자 단위 순회, set in O(L)=O(1)
    Mine_three - 시간: O(N×M)   | 공간: O(1) - 컴파일 O(1) 1회 + match O(M) × N번
    Best       - 시간: O(N×M)   | 공간: O(1) - Mine_two와 동일
    Sub        - 시간: O(N×P×M) | 공간: O(M) - Mine_one과 동일

    P, L 모두 상수 → 전체 실질 O(N×M)
    N≤100, M≤30 → 사실상 O(1)에 수렴
"""

import re
import time


# =================================================================================
# Mine solution one - replace 공백 치환 + 이중 발음 사전 정의
# =================================================================================
def solution_mine_one(babbling: list[str]) -> int:
    """
    이중 발음 먼저 걸러내고 단일 발음을 공백으로 치환해 검증하는 초기 풀이

    공백 치환 이유:
        빈 문자열 치환 시: "ayaye" → aya 제거 → "ye" → ye 제거 → "" ← 정상 통과
        하지만 "yayae" 같은 발음 불가 단어도:
            ye 없음 → aya 제거 → "y e" → y 남음 (OK)
        "yeyeye" 같은 3회 연속:
            is_double 체크 시 "yeye"가 "yeyeye" 안에 포함 → True → 제외 ✓

    replace 순서:
        탐욕적(greedy) 왼쪽부터 적용, 순서 무관하게 결과 동일 (실측 검증)
    """
    answer = 0

    for word in babbling:
        is_double = False
        for p in ("ayaaya", "yeye", "woowoo", "mama"):
            if p in word:
                is_double = True
                break

        if is_double:
            continue

        for p in ("aya", "ye", "woo", "ma"):
            word = word.replace(p, " ")

        if word.strip() == "":
            answer += 1

    return answer


# =================================================================================
# Mine solution two - 문자 단위 포인터 + set 발음 비교
# =================================================================================
def solution_mine_two(babbling: list[str]) -> int:
    """
    문자를 하나씩 버퍼에 쌓으며 발음을 감지하는 포인터 방식 풀이

    핵심:
        curr_p: 현재 누적 중인 문자 버퍼
        prev_p: 직전에 완성된 발음
        발음 매칭 시 prev_p == curr_p이면 연속 발음 → is_double=True

    이중 발음 사전 정의 불필요:
        prev_p == curr_p 비교로 동적 탐지
        "yeyeye": ye 매칭 → prev_p="ye", ye 매칭 → curr_p="ye" == prev_p → 탈락

    최종 조건:
        is_double == False: 연속 발음 없음
        curr_p == "": 모든 문자가 발음으로 소진 (남은 발음 불가 문자 없음)

    변수명 정정: pronuciation → pronunciation (오타이나 원본 유지)
    """
    answer = 0
    pronuciation = {"aya", "ye", "woo", "ma"}

    for word in babbling:
        is_double = False
        curr_p = ""
        prev_p = ""

        for char in word:
            curr_p += char

            if curr_p in pronuciation:
                if prev_p == curr_p:
                    is_double = True
                    break
                prev_p = curr_p
                curr_p = ""

        if not is_double and curr_p == "":
            answer += 1

    return answer


# =================================================================================
# Mine solution three - 부정형 전방 탐색 정규표현식
# =================================================================================
def solution_mine_three(babbling: list[str]) -> int:
    """
    부정형 전방 탐색(negative lookahead)으로 연속 발음을 배제하는 정규표현식 풀이

    패턴: ^(aya(?!aya)|ye(?!ye)|woo(?!woo)|ma(?!ma))+$
        ^...$:   단어 전체 매칭
        (...)+:  하나 이상의 발음 그룹으로 구성
        A(?!B):  부정형 전방 탐색
                 "A 뒤에 B가 오면 해당 위치에서 매칭 실패"
                 위치만 확인하고 문자를 소비하지 않음 → 위치 이동 없음

    "바로 None 반환"이 아닌 정확한 동작:
        aya(?!aya) 실패 시 → ye(?!ye), woo(?!woo), ma(?!ma) 순으로 대안 탐색
        전부 실패해야 해당 위치에서 그룹 전체 실패
        $ 미도달 시 최종 None 반환

    손 추적 ("ayaaya"):
        위치 0: aya(?!aya) → "aya" 매칭, 뒤에 "aya" → lookahead 실패
                ye/woo/ma → 위치 0에서 매칭 실패
                → 그룹 매칭 실패 → + 조건 불충족 → None

    손 추적 ("ayaye"):
        위치 0: aya(?!aya) → "aya" 매칭, 뒤에 "ye" → lookahead 통과
                위치 3으로 이동
        위치 3: ye(?!ye) → "ye" 매칭, 뒤에 없음 → lookahead 통과
                위치 5로 이동
        위치 5: $ → 성공

    re.compile: 패턴 사전 컴파일 → 반복 호출 시 컴파일 비용 1회만 발생

    소규모 제약(N≤100, M≤30)에서 컴파일 오버헤드가 불리
    대규모(N이 만 단위 이상)에서는 컴파일 비용이 분산되어 유리할 수 있음
    """
    answer = 0
    pattern = re.compile(r'^(aya(?!aya)|ye(?!ye)|woo(?!woo)|ma(?!ma))+$')

    for word in babbling:
        if bool(pattern.match(word)):
            answer += 1

    return answer


# =================================================================================
# Best solution - 문자 단위 포인터 (mine_two 주석 보강)
# =================================================================================
def solution_best(babbling: list[str]) -> int:
    """
    문자 단위 포인터 방식으로 연속 발음과 발음 구성을 동시에 검증하는 최적 풀이

    mine_two와 동일한 로직, 선정 근거 주석 보강:
        이중 발음 사전 정의 불필요 → 코드 간결
        prev_p == curr_p: 연속 발음 동적 탐지
        set in O(1): 발음 여부 상수 시간 판별
        curr_p == "": 발음 불가 잔여 문자 없음 검증
        O(N×M): 각 단어를 문자 단위로 단일 순회
    """
    answer = 0
    pronunciation = {"aya", "ye", "woo", "ma"}

    for word in babbling:
        is_double = False
        curr_p = ""
        prev_p = ""

        for char in word:
            curr_p += char

            if curr_p in pronunciation:
                if prev_p == curr_p:
                    is_double = True
                    break
                prev_p = curr_p
                curr_p = ""

        if not is_double and curr_p == "":
            answer += 1

    return answer


# =================================================================================
# Sub solution - replace 공백 치환 (mine_one 주석 보강)
# =================================================================================
def solution_sub(babbling: list[str]) -> int:
    """
    이중 발음 사전 정의 후 단일 발음 공백 치환으로 검증하는 서브 풀이

    Best 대비 특징:
        이중 발음 튜플 명시 → 어떤 패턴을 거르는지 코드에 직접 드러남
        공백 치환: 발음 불가 문자가 공백 사이에 노출되어 strip으로 탐지
        replace O(M) × 발음 4종 → O(N×P×M), P=4 상수라 O(N×M)과 동등
        N회 연속 발음: "yeye"가 "yeyeye" 안에 포함되므로 자동 탐지
    """
    answer = 0

    for word in babbling:
        is_double = False
        for p in ("ayaaya", "yeye", "woowoo", "mama"):
            if p in word:
                is_double = True
                break

        if is_double:
            continue

        for p in ("aya", "ye", "woo", "ma"):
            word = word.replace(p, " ")

        if word.strip() == "":
            answer += 1

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple[list[str], int]] = [
        # (babbling, 기댓값)
        # 프로그래머스 공식 예시:
        # "aya": aya 하나 → 1
        # "yee": ye+e → e가 남음 → 탈락
        # "u": 발음 불가 → 탈락
        # "maa": ma+a → a가 남음 → 탈락
        (["aya", "yee", "u", "maa"], 1),
        # "ayaye": aya+ye → 2개 발음, 연속 없음 → 통과
        # "uuu": 발음 불가 → 탈락
        # "yeye": ye+ye → 연속 발음 → 탈락
        # "yemawoo": ye+ma+woo → 통과
        # "ayaayaa": ayaaya 포함 → 탈락
        (["ayaye", "uuu", "yeye", "yemawoo", "ayaayaa"], 2),
        # 추가 케이스:
        # 모든 발음 조합
        (["ayayewoomawooye"], 1),
        # 발음 불가 문자 포함
        (["woowo", "ayab"], 0),
        # 3회 연속 발음
        (["yeyeye", "ayayaaya"], 0),
    ]

    solutions = [
        ("Mine_one   (replace치환) ", solution_mine_one),
        ("Mine_two   (포인터방식)  ", solution_mine_two),
        ("Mine_three (정규표현식)  ", solution_mine_three),
        ("Best       (포인터방식)  ", solution_best),
        ("Sub        (replace치환) ", solution_sub),
    ]

    # 워밍업 스텝
    _b, _ = test_cases[0]
    for _, func in solutions:
        func(_b[:])

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (babbling, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(babbling[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
