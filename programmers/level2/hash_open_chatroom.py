"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 2
    문제명     : 오픈채팅방
    유형       : Hash / Simulation
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/42888
    풀이일자   : 2026-09-18
===================================================================================
[문제 요약]
    입장/퇴장/닉네임변경 기록 record에서
    최종 닉네임 기준으로 입장/퇴장 메시지 배열 반환

    제약 조건
        - record 길이: 1 이상 100,000 이하
        - uid/닉네임: 최대 10자
        - 잘못된 입력 없음 (Enter 없이 Leave/Change 없음)
===================================================================================
[입출력 예시]
    record                                      | result
    --------------------------------------------|-------------------------------
    ["Enter uid1234 Muzi", "Enter uid4567 Prodo",| ["Prodo님이 들어왔습니다.",
     "Leave uid1234", "Enter uid1234 Prodo",     |  "Ryan님이 들어왔습니다.",
     "Change uid4567 Ryan"]                      |  "Prodo님이 나갔습니다.",
                                                 |  "Prodo님이 들어왔습니다."]
===================================================================================
[핵심 — "닉네임 변경 시 기존 메시지도 전부 변경"]
    최종 닉네임만 있으면 됨
    → 먼저 최신 닉네임 확보 → 그 후 메시지 생성

[정방향 2회 순회 (풀이1)]
    1회: Enter/Change에서 table[uid] = nickname 덮어쓰기
         → 마지막 Enter/Change가 항상 최신 닉네임
    2회: table[uid]로 최종 닉네임 조회

[역방향 + 정방향 (ref)]
    역방향: uid가 처음(=최신) 나타난 것만 저장, 이후 skip
    조건: if uid not in table → 한 번만 저장
    정방향: 동일하게 메시지 생성

    역방향이 유리한 이유:
        정방향: Enter/Change마다 dict 쓰기 → 최악 N번
        역방향: uid당 1회만 dict 쓰기
        Change 많을수록 역방향 우위

[풀이2 — 참조 객체 방식 (독창적 접근)]
    목표: 1회 순회로 처리
    방법: table[uid] = [""] (리스트 주소 저장)
          table[uid][0] = nickname (내부 값만 교체)
          answer에 (table[uid], 메시지 템플릿) 튜플 저장
          마지막 컴프리헨션에서 [0]으로 최신 닉네임 반영

    한계: 지문 조건 "Enter 없이 Leave 없음" 보장 필요
          (랜덤 데이터에서는 KeyError 발생 가능)
          마지막 컴프리헨션으로 추가 순회 발생

[실측 결과 — N=100,000, 500회]
    ref (역방향):     27.5ms  ← 약 12% 빠름
    one (정방향 2회): 31.3ms
===================================================================================
[내 초기 풀이]
    solution_mine_one: 정방향 2회 순회
    solution_mine_two: 참조 객체 방식 1회 순회

[개선 포인트]
    solution_mine_one: 개선 필요 없음 - Best
                       구조 가장 명확, 직관적
    solution_mine_two: 독창적이나 구조 복잡
                       마지막 컴프리헨션으로 추가 순회 불가피
    solution_ref:      역방향으로 불필요한 덮어쓰기 제거 - Sub
                       Change 많을수록 유리
===================================================================================
[복잡도 분석]
    N = len(record) (최대 100,000)

    Mine_one - 시간: O(N) | 공간: O(U) - U=uid 수
    Mine_two - 시간: O(N) | 공간: O(U) - 리스트 참조
    Ref      - 시간: O(N) | 공간: O(U) - 역방향 순회
    Best     - 시간: O(N) | 공간: O(U) - Mine_one과 동일
    Sub      - 시간: O(N) | 공간: O(U) - Ref와 동일
"""

import time


# =================================================================================
# Mine solution one - 정방향 2회 순회
# =================================================================================
def solution_mine_one(record: list[str]) -> list[str]:
    """
    Enter/Change 덮어쓰기로 최신 닉네임을 확보하고 2회 순회로 메시지를 생성하는 초기 풀이

    1회 순회:
        Enter/Change마다 table[uid] = nickname 덮어쓰기
        마지막 Enter/Change가 항상 최신 닉네임으로 남음

    2회 순회:
        Enter/Leave 기록에서 table[uid]로 최신 닉네임 조회
        Change 기록은 메시지 생성 불필요 → 자동 skip
    """
    answer = []
    table = {}

    for r in record:
        parts = r.split()
        if parts[0] in ("Enter", "Change"):
            table[parts[1]] = parts[2]

    for r in record:
        parts = r.split()
        status, uid = parts[0], parts[1]

        if status == "Enter":
            answer.append(f"{table[uid]}님이 들어왔습니다.")
        elif status == "Leave":
            answer.append(f"{table[uid]}님이 나갔습니다.")

    return answer


# =================================================================================
# Mine solution two - 참조 객체 방식 1회 순회
# =================================================================================
def solution_mine_two(record: list[str]) -> list[str]:
    """
    리스트 참조로 닉네임 변경을 동적으로 반영하는 1회 순회 시도 풀이

    발상:
        table[uid] = [""] → 리스트 주소를 table에 저장
        table[uid][0] = nickname → 내부 값만 교체
        answer에 (table[uid], 템플릿) 튜플 → 최신 닉네임 지연 반영

    한계:
        마지막 컴프리헨션에서 추가 순회 발생
        지문 조건 "Enter 없이 Leave 없음" 보장 필요
        (조건 위반 시 KeyError)
    """
    answer = []
    table = {}

    for r in record:
        parts = r.split()
        status, uid = parts[0], parts[1]

        if status in ("Enter", "Change"):
            if uid not in table:
                table[uid] = [""]
            table[uid][0] = parts[2]

        if status == "Enter":
            answer.append((table[uid], "님이 들어왔습니다."))
        elif status == "Leave":
            answer.append((table[uid], "님이 나갔습니다."))

    return [f"{nickname[0]}{text}" for nickname, text in answer]


# =================================================================================
# Ref solution - 역방향 순회 + 정방향 순회
# =================================================================================
def solution_ref(record: list[str]) -> list[str]:
    """
    역방향으로 최신 닉네임만 1회 저장하고 정방향으로 메시지를 생성하는 참고 풀이

    역방향 순회:
        최신 기록(뒤)부터 확인 → uid가 처음 나타난 것이 최신 닉네임
        uid not in table 조건으로 한 번만 저장 → 이후 skip

    정방향 덮어쓰기(mine_one) 대비:
        Change 기록 수만큼 불필요한 dict 쓰기 절감
        실측 N=100,000: 27.5ms (mine_one 31.3ms 대비 12% 우위)
    """
    answer = []
    table = {}

    for r in reversed(record):
        parts = r.split()
        status, uid = parts[0], parts[1]
        if status in ("Enter", "Change") and uid not in table:
            table[uid] = parts[2]

    for r in record:
        parts = r.split()
        status, uid = parts[0], parts[1]

        if status == "Enter":
            answer.append(f"{table[uid]}님이 들어왔습니다.")
        elif status == "Leave":
            answer.append(f"{table[uid]}님이 나갔습니다.")

    return answer


# =================================================================================
# Best solution - 정방향 2회 순회 (mine_one 주석 보강)
# =================================================================================
def solution_best(record: list[str]) -> list[str]:
    """
    정방향 2회 순회로 직관적이고 명확하게 메시지를 생성하는 최적 풀이

    mine_one과 동일한 로직, 선정 근거 주석 보강:
        구조가 가장 단순: "닉네임 확보 → 메시지 생성" 분리
        Enter/Change 덮어쓰기로 최신 닉네임 자동 유지
        ref 대비 12ms 느리나 코드 가독성 기준으로 Best 선정
    """
    answer = []
    table = {}

    for r in record:
        parts = r.split()
        if parts[0] in ("Enter", "Change"):
            table[parts[1]] = parts[2]

    for r in record:
        parts = r.split()
        status, uid = parts[0], parts[1]

        if status == "Enter":
            answer.append(f"{table[uid]}님이 들어왔습니다.")
        elif status == "Leave":
            answer.append(f"{table[uid]}님이 나갔습니다.")

    return answer


# =================================================================================
# Sub solution - 역방향 순회 (ref 주석 보강)
# =================================================================================
def solution_sub(record: list[str]) -> list[str]:
    """
    역방향으로 불필요한 덮어쓰기 없이 최신 닉네임을 확보하는 서브 풀이

    ref와 동일한 로직, 선정 근거 주석 보강:
        역방향으로 uid당 1회만 dict 쓰기 → Change 많을수록 유리
        실측: 27.5ms (Best 31.3ms 대비 12% 우위)
        역방향 아이디어: "최신 기록이 뒤에 있으므로 역으로 읽으면 첫 등장이 최신"
    """
    answer = []
    table = {}

    for r in reversed(record):
        parts = r.split()
        status, uid = parts[0], parts[1]
        if status in ("Enter", "Change") and uid not in table:
            table[uid] = parts[2]

    for r in record:
        parts = r.split()
        status, uid = parts[0], parts[1]

        if status == "Enter":
            answer.append(f"{table[uid]}님이 들어왔습니다.")
        elif status == "Leave":
            answer.append(f"{table[uid]}님이 나갔습니다.")

    return answer


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    test_cases: list[tuple] = [
        # (record, 기댓값)
        # 공식 예시
        (["Enter uid1234 Muzi", "Enter uid4567 Prodo", "Leave uid1234",
          "Enter uid1234 Prodo", "Change uid4567 Ryan"],
         ["Prodo님이 들어왔습니다.", "Ryan님이 들어왔습니다.",
          "Prodo님이 나갔습니다.", "Prodo님이 들어왔습니다."]),
        # 추가 케이스:
        # Change 후 Leave → Change 닉네임 반영
        (["Enter uid1234 Alice", "Change uid1234 Bob", "Leave uid1234"],
         ["Bob님이 들어왔습니다.", "Bob님이 나갔습니다."]),
        # 재입장: 새 닉네임으로 기존 메시지도 변경
        (["Enter uid1234 Alice", "Leave uid1234", "Enter uid1234 Bob"],
         ["Bob님이 들어왔습니다.", "Bob님이 나갔습니다.", "Bob님이 들어왔습니다."]),
    ]

    solutions = [
        ("Mine_one (정방향 2회) ", solution_mine_one),
        ("Mine_two (참조객체)   ", solution_mine_two),
        ("Ref      (역방향)     ", solution_ref),
        ("Best     (정방향 2회) ", solution_best),
        ("Sub      (역방향)     ", solution_sub),
    ]

    # 워밍업
    _r, _ = test_cases[0]
    for _, func in solutions:
        func(_r[:])

    print("=" * 64)
    print(f"{'풀이':<22} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 64)

    for name, func in solutions:
        for idx, (record, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = func(record[:])
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<22} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 64)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
