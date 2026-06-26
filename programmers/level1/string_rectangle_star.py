"""
===================================================================================
[문제 정보]
    사이트     : Programmers
    레벨       : Level 1
    문제명     : 직사각형 별찍기
    유형       : String
    링크       : https://school.programmers.co.kr/learn/courses/30/lessons/12969
    풀이일자   : 2026-06-26
===================================================================================
[문제 요약]
    표준 입력으로 n, m을 받아 가로 n, 세로 m의 '*' 직사각형을 출력

    제약 조건
        - n, m: 1,000 이하 자연수
        - 반환값 없음, print()로 출력하는 문제
===================================================================================
[입출력 예시]
    입력: 5 3
    출력:
        *****
        *****
        *****
===================================================================================
[내 초기 풀이]
    solution_mine_one  : for 루프 + print() 반복 (가장 명시적)
    solution_mine_two  : '\n'.join() + 제너레이터
    solution_mine_three: print() 언패킹 + sep='\n'
    solution_mine_four : 문자열 산술 연산만으로 구현 (가장 파이써닉)

[개선 포인트]
    solution_mine_one  : 개선 필요 없음 - Sub (명시적, 가독성 우위)
    solution_mine_two  : 개선 필요 없음 - Best (제너레이터로 메모리 효율)
    solution_mine_three: sep 매개변수 활용, 언패킹 방식 (sep으로 표기, seq 아님)
    solution_mine_four : end='' 필요 이유:
                        ('*'*n + '\n') * m 끝에 이미 \n 존재
                        print() 기본 end='\n' → \n\n → 마지막 빈 줄 생성
                        end=''로 print() 자체의 개행 억제
===================================================================================
[출력 결과 검증 방법 — io.StringIO 캡처]
    print()는 반환값이 없어 == 비교 불가
    → sys.stdout을 io.StringIO로 교체해 출력을 문자열로 캡처

    표준 스트림 (Standard Stream):
        프로그램 실행 시 운영체제가 자동으로 열어주는 3개의 I/O 채널
            sys.stdin  : 표준 입력  — 키보드 → 프로그램  (input()이 여기서 읽음)
            sys.stdout : 표준 출력  — 프로그램 → 터미널   (print()가 여기에 씀)
            sys.stderr : 표준 오류  — 프로그램 → 터미널   (예외/오류 메시지 전용)
        sys.__stdout__: Python이 원본 stdout을 보존하는 내장 변수
                        sys.stdout을 교체해도 원본 터미널 객체는 여기에 남아있음

    기존 출력 방식:
        print("hello") 내부 동작:
            sys.stdout.write("hello")   # stdout에 문자열 전송
            sys.stdout.write("\n")      # end='\n' 기본값으로 개행 추가
        stdout이 터미널에 연결되어 있어 write()가 즉시 화면에 출력됨

    File-like Object (파일류 객체):
        Python에서 read(), write(), flush() 메서드를 가지는 모든 객체
        실제 파일인지 메모리 버퍼인지 터미널인지와 무관하게 동일한 인터페이스
            open('a.txt') → 디스크 파일   → write() 호출 시 파일에 저장
            sys.stdout    → 터미널 연결   → write() 호출 시 화면에 출력
            io.StringIO() → 메모리 버퍼  → write() 호출 시 메모리에 저장
        sys.stdout도 File-like Object이기 때문에 교체 가능

    io.StringIO — 메모리 위의 가상 파일:
        buf = io.StringIO()
        buf.write("hello\n")    # 메모리 버퍼에 저장 (화면 출력 없음)
        buf.getvalue()          # 버퍼 전체 내용을 문자열로 반환 → "hello\n"

    sys.stdout 교체로 출력 가로채기:
        sys.stdout = io.StringIO()  → print()의 목적지를 메모리 버퍼로 전환
        print("hello")              → sys.stdout.write("hello\n") 호출
                                    stdout이 StringIO이므로 버퍼에 저장
        captured.getvalue()         → 버퍼 내용 추출 → "hello\n"
        sys.stdout = sys.__stdout__ → 터미널로 복원

    sys.stdin 교체 원리 (입력 주입):
        input() 내부 동작: sys.stdin.readline()으로 입력을 읽음
        sys.stdin = io.StringIO("5 3\n")으로 교체하면
        input() 호출 시 키보드 대신 StringIO 버퍼에서 "5 3\n"을 읽음
        → input()을 사용하는 코드를 자동화된 테스트로 실행 가능

    try/finally 복원 이유:
        func(n, m) 실행 중 예외 발생 시 sys.stdout 복원 코드 미실행 위험
        finally 블록은 예외와 무관하게 항상 실행 → 복원 보장

    이 문제 기댓값 구성:
        n=5, m=3: '*****\n' × 3 = '*****\n*****\n*****\n'
        print()는 항상 마지막에 \n을 추가하므로 기댓값도 \n으로 끝남
        단, solution_mine_four는 end=''로 print() 개행 억제
            → ('*'*n + '\n') * m 자체의 마지막 \n만 남음 (동일한 결과)
===================================================================================
[복잡도 분석]
    N = n (최대 1,000), M = m (최대 1,000)

    Mine_one   - 시간: O(M×N) | 공간: O(N)   - print() M회, '*'×N 문자열 매번 생성
    Mine_two   - 시간: O(M×N) | 공간: O(N)   - 제너레이터: 한 행씩 생성, join 시 O(M×N)
    Mine_three - 시간: O(M×N) | 공간: O(M×N) - 리스트 컴프리헨션으로 전체 생성 후 언패킹
    Mine_four  - 시간: O(M×N) | 공간: O(M×N) - 문자열 산술로 전체 생성 후 출력
    Best       - 시간: O(M×N) | 공간: O(N)   - Mine_two와 동일, 주석 보강
    Sub        - 시간: O(M×N) | 공간: O(N)   - Mine_one과 동일, 주석 보강

    print() 호출 횟수:
        Mine_one/Sub: M번 (행마다 호출) → I/O 비용 M번
        Mine_two/Best: 1번 (join 후 한 번에 출력) → I/O 비용 1번
        Mine_three: 1번 (언패킹 후 한 번에 출력)
        Mine_four: 1번 (문자열 생성 후 한 번에 출력)
    → 대규모(M=1,000)에서 Mine_one은 print() 1,000회 I/O 부담
"""

import io
import sys
import time
from typing import List, Tuple


# =================================================================================
# Mine solution one - for 루프 + print() 반복
# =================================================================================
def solution_mine_one(n: int, m: int) -> None:
    """
    for 루프로 m번 반복하며 '*'×n을 출력하는 가장 명시적인 초기 풀이

    핵심:
        print()는 기본적으로 end='\n' → 자동 개행 → 별도 \n 불필요
        '*' * n: n개의 '*'로 구성된 문자열 생성

    I/O 비용:
        print() m번 호출 → 시스템 콜 m번 발생
        m=1,000이면 print() 1,000회 → Mine_two(1회) 대비 I/O 부담
    """
    for _ in range(m):
        print('*' * n)          # print() 자동 개행으로 줄 구분


# =================================================================================
# Mine solution two - '\n'.join() + 제너레이터
# =================================================================================
def solution_mine_two(n: int, m: int) -> None:
    """
    제너레이터로 각 행을 생성하고 join으로 결합해 한 번에 출력하는 풀이

    핵심:
        ('*' * n for _ in range(m)): 각 행('*'×n)을 하나씩 yield하는 제너레이터
        '\n'.join(...): 제너레이터를 순회하며 '\n'으로 연결
        print() 1회 호출 → I/O 비용 최소화

    제너레이터 메모리 효율:
        리스트 컴프리헨션 [*n for _ in range(m)]: 전체 리스트 메모리 보유
        제너레이터: join()이 순회할 때 한 행씩 생성 → 공간 O(N)
    """
    print('\n'.join('*' * n for _ in range(m)))


# =================================================================================
# Mine solution three - print() 언패킹 + sep='\n'
# =================================================================================
def solution_mine_three(n: int, m: int) -> None:
    """
    print() 언패킹과 sep 매개변수로 구분자를 지정하는 풀이

    핵심:
        ['*' * n for _ in range(m)]: m개 행을 원소로 갖는 리스트
        print(*리스트, sep='\n'): 리스트 언패킹 후 sep으로 구분 출력
        sep(separator, 구분자): 여러 인자 사이의 구분 문자 (기본값 ' ')

    Mine_two 대비:
        리스트 컴프리헨션으로 전체를 메모리에 생성 후 언패킹 → 공간 O(M×N)
        Mine_two의 제너레이터는 공간 O(N) → 대규모에서 Mine_two 유리
    """
    print(*['*' * n for _ in range(m)], sep='\n')  # sep으로 개행 구분


# =================================================================================
# Mine solution four - 문자열 산술 연산
# =================================================================================
def solution_mine_four(n: int, m: int) -> None:
    """
    반복문/join 없이 문자열 산술 연산만으로 구현한 가장 파이써닉한 풀이

    핵심:
        '*' * n + '\n': n개 '*' + 개행문자로 한 행 구성
        (...) * m: 위 문자열을 m번 반복 → 전체 직사각형 문자열
        end='': print() 기본 end='\n' 억제

    end='' 필요 이유:
        ('*'*n + '\n') * m 끝에 이미 '\n' 존재
        print() 기본 end='\n' 그대로면 끝에 '\n\n' → 빈 줄 생성
        end=''로 print() 자체 개행 억제 → 의도한 출력 유지
    """
    print(('*' * n + '\n') * m, end='')    # end=''로 마지막 빈 줄 방지


# =================================================================================
# Best solution - '\n'.join() + 제너레이터 (mine_two 주석 보강)
# =================================================================================
def solution_best(n: int, m: int) -> None:
    """
    제너레이터 + join으로 메모리 효율과 I/O 횟수를 최소화한 최적 풀이

    mine_two와 동일한 로직, 근거 주석 보강:
        제너레이터: 각 행을 순차적으로 생성, 전체 리스트 메모리 불필요
        join(): 제너레이터 1회 순회로 결합, '\n'으로 행 구분
        print() 1회: 시스템 콜 1번, I/O 부담 최소
    """
    print('\n'.join('*' * n for _ in range(m)))


# =================================================================================
# Sub solution - for 루프 (mine_one 주석 보강)
# =================================================================================
def solution_sub(n: int, m: int) -> None:
    """
    for 루프로 각 행을 순서대로 출력하는 서브 풀이

    Best 대비 특징:
        각 행을 개별적으로 출력 → 로직 흐름이 직관적
        print() m번 호출 → I/O 비용 m번 (Best의 1번 대비 많음)
        m=1,000에서 시스템 콜 1,000회 vs 1회 차이 발생
        디버깅 시 특정 행에서 멈추기 쉬움
    """
    for _ in range(m):
        print('*' * n)


# =================================================================================
# 각 풀이 결과 비교 검증 + 성능 측정
# =================================================================================
def solution_comparison():
    """각 풀이의 정확성과 성능을 동시에 검증"""

    # print() 출력을 문자열로 캡처하는 헬퍼
    def capture(func, n, m) -> str:
        """
        sys.stdout을 io.StringIO로 교체해 print() 출력을 문자열로 캡처

        표준 출력 가로채기 원리:
            print()는 내부적으로 sys.stdout.write()를 호출
            sys.stdout을 io.StringIO(메모리 버퍼)로 교체하면
            print()의 write() 호출이 터미널이 아닌 메모리로 향함
            → 화면에 보이지 않고 버퍼에 저장됨

        단계별 동작:
            1. captured = io.StringIO(): 메모리 버퍼 생성
            2. sys.stdout = captured: print() 목적지를 버퍼로 전환
            3. func(n, m): 함수 실행 → print()가 버퍼에 기록
            4.  sys.stdout = sys.__stdout__: 터미널 복원
                sys.__stdout__: Python이 보존하는 원본 stdout 참조
            5. captured.getvalue(): 버퍼 전체 내용을 문자열로 반환

        try/finally 복원 이유:
            func(n, m)에서 예외 발생 시 복원 코드가 실행되지 않으면
            이후 모든 print()가 터미널이 아닌 버퍼로 향해 화면 출력 불가
            finally: 예외 발생 여부와 무관하게 항상 실행 → 복원 보장
        """
        captured = io.StringIO()
        sys.stdout = captured
        try:
            func(n, m)
        finally:
            sys.stdout = sys.__stdout__  # 예외 발생해도 반드시 복원
        return captured.getvalue()

    test_cases: List[Tuple[int, int, str]] = [
        # (n, m, 기댓값)
        # 손 추적 (프로그래머스 공식 예시):
        # n=5, m=3: '*****\n' × 3
        #   print() 출력은 항상 끝에 \n 포함 (end='\n' 기본값)
        #   → '*****\n*****\n*****\n'
        (5, 3, '*****\n*****\n*****\n'),
        # 추가 케이스:
        # n=1, m=1: '*\n'
        (1, 1, '*\n'),
        # n=3, m=2: '***\n***\n'
        (3, 2, '***\n***\n'),
        # n=2, m=4: '**\n**\n**\n**\n'
        (2, 4, '**\n**\n**\n**\n'),
    ]

    solutions = [
        ("Mine_one   (for+print)", solution_mine_one),
        ("Mine_two   (join+gen) ", solution_mine_two),
        ("Mine_three (언패킹)   ", solution_mine_three),
        ("Mine_four  (산술연산) ", solution_mine_four),
        ("Best       (join+gen) ", solution_best),
        ("Sub        (for+print)", solution_sub),
    ]

    # 워밍업 스텝 ──────────────────────────────────────────────────
    _n, _m, _ = test_cases[0]
    for _, func in solutions:
        capture(func, _n, _m)
    # ───────────────────────────────────────────────────────────────

    print("=" * 66)
    print(f"{'풀이':<26} {'케이스':<6} {'결과':<8} {'소요시간':>10}")
    print("=" * 66)

    for name, func in solutions:
        for idx, (n, m, expected) in enumerate(test_cases, 1):
            start = time.perf_counter()
            output = capture(func, n, m)
            elapsed = time.perf_counter() - start

            status = "PASS" if output == expected else "FAIL"
            print(f"{name:<26} TC{idx:<5} {status:<8} {elapsed * 1000:>8.4f}ms")
        print("-" * 66)


# =================================================================================
# 실행 진입점
# =================================================================================
if __name__ == "__main__":
    solution_comparison()
