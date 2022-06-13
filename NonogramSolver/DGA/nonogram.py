class Game:
    """
    콘솔에 출력할 노노그램 퍼즐을 생성하는 클래스입니다.
    """
    def __init__(self, n_lines, n_columns, points):
        self.n_lines   = n_lines
        self.n_columns = n_columns
        self.board = []

        for _ in range(self.n_lines):
            aux = []
            for _ in range(self.n_columns):
                aux += [False]
            self.board += [aux]
        self.fill(points, n_lines, n_columns)


    def fill(self, points, n_lines, n_columns):
        """
        points에 있는 각 셀들의 ture/false 값을 순서대로 보드에 저장해주는 함수입나다.
        예) 0,0 0,1 0,2.. 
        """
        for i, v in enumerate(points):                      
            self.board[int(i/n_columns)][i%n_columns] = v    

    def __str__(self):
        result = '=' * ((self.n_columns)*2+2) + '\n'

        for l in self.board:
            result += '|'
            for s in l:
                result += (chr(9608) if not s else ' ')*2
            result += '|\n'

        result += '=' * ((self.n_columns)*2+2)
        return result

class Rules:
    """
    힌트 숫자와 관련해 조건들을 정제해주는 클래스입니다.
    예) lines = [[1,2,3], [], [2], [9]]
    """
    def __init__(self, lines, columns):
        self.lines   = lines
        self.columns = columns

    def __str__(self):
        result = 'lines:\n'
        for l in self.lines:
            for n in l:
                result += str(n)
                result += ' '
            result += '\n'

        result += 'columns:\n'
        for c in self.columns:
            for n in c:
                result += str(n)
                result += ' '
            result += '\n'
        return result[:-1]



def check_solution(game, rules):
    """
    퍼즐이 규칙을 만족하는지 확인하는 함수입니다. 
    한 줄씩 비교하며 힌트 숫자 조건을 만조하는지 확인합니다. 
    만족하지 않을경우 바로 False 리턴한다.

    이 함수는 ga연산 끝난 후 나온 최종 best 유전자에 대해서 한번만 실행합니다.
    """
    # 퍼즐 해가 저장되어있는 리스트 ex) [[True, False, True, False, True], [True, True, True, True, True], ... ]]
    board    = game.board
    # 가로줄 개수
    n_lines   = game.n_lines  
    # 세로줄 개수
    n_columns = game.n_columns    
 

    for col_idx in range(n_columns):
        rules_qtt = len(rules.columns[col_idx])

        line_idx = 0
        rule_idx   = 0

        while line_idx < n_lines and rule_idx < rules_qtt:
            cnt_segment = 0

            while(line_idx < n_lines and not board[line_idx][col_idx]):
                line_idx += 1

            while(line_idx < n_lines and board[line_idx][col_idx]):
                cnt_segment += 1
                line_idx  += 1

            curr_rule = rules.columns[col_idx][rule_idx]
            if(cnt_segment != curr_rule):
                return False

            rule_idx += 1

        if rule_idx < rules_qtt:
            return False

        while(line_idx < n_lines):
            if(board[line_idx][col_idx]):
                return False
            line_idx += 1

    return True