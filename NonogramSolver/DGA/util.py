from DGA import nonogram

from numpy import random

def printSol(sol, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    print(nonogram.Game(nLines,  nColumns, sol.points))

# 파일 읽어오기
def readRulesFile(fileName):
    with open(fileName) as rulesFile:
        readingLines = True
        lines   = []
        columns = []

        for fileLine in rulesFile:
            if(fileLine == '-\n'):
                readingLines = False
                continue

            rulesInFileLine = [[int(rule) for rule in fileLine.split()]]
            if(readingLines):
                lines   += rulesInFileLine
            else:
                columns += rulesInFileLine

    return nonogram.Rules(lines=lines, columns=columns)

def createConstraints(rules, nPopulation):
    nLines   = len(rules.lines)         # 가로줄 수
    nColumns = len(rules.columns)       # 세로줄 수
    nPoints  = 0                        # 검정셀 수

    # Count total number of points
    for line in rules.lines:
        for rule in line:
            nPoints += rule

    return (rules, nLines, nColumns, nPoints, nPopulation)
    #       힌트 숫자, 가로줄 수, 세로줄 수, 검정셀 수, 인구수


def fitness(sol, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    # Count how many rules it is following
    count = 0
    game  = nonogram.Game(nLines, nColumns, sol)
    board = sol

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while lineIndex < nLines and not board[lineIndex*nColumns + columnIndex]:
                lineIndex += 1

            while lineIndex < nLines and board[lineIndex*nColumns + columnIndex]:
                countSegment += 1
                lineIndex    += 1

            count     -= abs(countSegment - currRule)
            ruleIndex += 1

    return count