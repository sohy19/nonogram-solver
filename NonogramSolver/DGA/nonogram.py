class Game:
    def __init__(self, nLines, nColumns, points):
        self.nLines   = nLines
        self.nColumns = nColumns
        self.board = []

        for _ in range(self.nLines):
            aux = []
            for _ in range(self.nColumns):
                aux += [False]
            self.board += [aux]


        self.fill(points, nLines, nColumns)


    def fill(self, points, nLines, nColumns):
        for i, v in enumerate(points):                      # points에 있는 각 셀들의 ture/false 값을 순서대로 보드에 저장
            self.board[int(i/nColumns)][i%nColumns] = v     # 0,0 0,1 0,2.. 순서대로

    def __str__(self):
        result = '=' * ((self.nColumns)*2+2) + '\n'

        for l in self.board:
            result += '|'
            for s in l:
                result += (chr(9608) if not s else ' ')*2
            result += '|\n'

        result += '=' * ((self.nColumns)*2+2)
        return result

# 힌트 숫자 관련 클래스
class Rules:
    # example: lines = [[1,2,3], [], [2], [9]]
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


def checkSolution(game, rules):
# 퍼즐이 규칙을 만족하는지 확인. 한 줄씩 내려가며 힌트 숫자와 비교. 만족하지 않을경우 바로 False 리턴
# 이 함수는 ga연산 끝난 후 나온 최종 best 유전자에 대해서 한번만 실행.

    board    = game.board
    # 퍼즐 해가 저장되어있는 리스트 ex) [[True, False, True, False, True], [True, True, True, True, True], ... ]]
    nLines   = game.nLines      # 가로줄 개수
    nColumns = game.nColumns    # 세로줄 개수
 

    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex   = 0

        while lineIndex < nLines and ruleIndex < rulesQtt:
            countSegment = 0

            while(lineIndex < nLines and not board[lineIndex][columnIndex]):
                lineIndex += 1

            while(lineIndex < nLines and board[lineIndex][columnIndex]):
                countSegment += 1
                lineIndex  += 1

            currRule = rules.columns[columnIndex][ruleIndex]
            if(countSegment != currRule):
                return False

            ruleIndex += 1

        if ruleIndex < rulesQtt:
            return False

        while(lineIndex < nLines):
            if(board[lineIndex][columnIndex]):
                return False
            lineIndex += 1

    return True