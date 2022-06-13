from DGA import nonogram
from numpy import random

def print_solution(sol, constraints):
    """
    생성한 솔루션을 콘솔에 출력해주는 함수입니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints
    print(nonogram.Game(n_lines,  n_columns, sol.points))

def read_rules_file(fileName):
    """
    파일을 읽어오는 함수입니다.
    """
    with open(fileName) as rules_file:
        reading_lines = True
        lines   = []
        columns = []

        for file_line in rules_file:
            if(file_line == '-\n'):
                reading_lines = False
                continue

            rules_in_file_line = [[int(rule) for rule in file_line.split()]]
            if(reading_lines):
                lines   += rules_in_file_line
            else:
                columns += rules_in_file_line

    return nonogram.Rules(lines=lines, columns=columns)

def create_constraints(rules, n_population):
    """
    제약조건들을 정리하여 반환해주는 함수입니다.
    """
    # 가로줄 수
    n_lines   = len(rules.lines) 
    # 세로줄 수        
    n_columns = len(rules.columns)
    # 검정셀 수       
    n_points  = 0                        

    # 포인트 들의 전체 갯수를 세어준다.
    for line in rules.lines:
        for rule in line:
            n_points += rule

    #       힌트 숫자, 가로줄 수, 세로줄 수, 검정셀 수, 인구수
    return (rules, n_lines, n_columns, n_points, n_population)
   
def fitness(sol, constraints):
    """
    각각의 줄마다 규칙과 얼마나 일치하지 않는지를 계산합니다. 
    규칙을 어긴 횟수를 0에서 차감하는 방식이기때문에 적합도는 항상 0이하의 정수값을 가집니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints

    # rules의 수를 세어준다
    count = 0
    game  = nonogram.Game(n_lines, n_columns, sol)
    board = sol

    # 오름차순인 컬럼의 수를 세어준다.
    for col_idx in range(n_columns):
        rules_qtt = len(rules.columns[col_idx])

        line_idx = 0
        rule_idx = 0

        while line_idx < n_lines or rule_idx < rules_qtt:
            cnt_segment = 0
            curr_rule     = rules.columns[col_idx][rule_idx] if rule_idx < rules_qtt else 0

            while line_idx < n_lines and not board[line_idx*n_columns + col_idx]:
                line_idx += 1

            while line_idx < n_lines and board[line_idx*n_columns + col_idx]:
                cnt_segment += 1
                line_idx    += 1

            count     -= abs(cnt_segment - curr_rule)
            rule_idx += 1
    return count