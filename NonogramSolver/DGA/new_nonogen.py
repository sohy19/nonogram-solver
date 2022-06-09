import numpy as np
import sys
from numpy import random
from DGA.nonogram import Game, Rules, checkSolution
from DGA.util     import readRulesFile, printSol, createConstraints, fitness as evaluateFitness
import itertools, random

class Solution:
    def __init__(self, points, constraints):
        self.points  = points
        self.fitness = evaluateFitness(points, constraints)


# def main(puzzleName = 'i21021', nPopulation = 500):
def main(rules, nLines, nColumns, nPoints, nPopulation = 500):
    
    # rules = readRulesFile('DGA/puzzles/' + puzzleName + '.txt')
    # constraints = createConstraints(rules, nPopulation)
    
    constraints = rules, nLines, nColumns, nLines*nColumns, nPopulation
    # return print(rules)
    
    global solutions
    solutions = line_solution(rules)

    mySol = DGA(constraints)
    #print("최종결과 밑에 나와여!!!!!!!!!!!!!!!!!!!!")
    #printSol(mySol, constraints)
    #이거는 불리언 값 나열한거
    print(mySol.points)
    return mySol.points, iterations
    # print(checkSolution(Game(nLines, nColumns, mySol.points), rules))
    print("세대 수: ", iterations, " 인구 수: ", nPopulation)
    # printSol(mySol, constraints)

iterations = 0


def line_solution(rules):
	hint = rules.lines
	# 가로줄 힌트 리스트 저장
	nLine = len(rules.columns)
	# 가로줄 칸 수 확인

	sol_set = []
	sol_dic = {}

	for k in range(len(hint)):
		nHint = len(hint[k])
		
		cLine = nLine - (sum(hint[k]) - nHint)
		# 가로줄 칸 개수 조정
	
		num_list = []
		x = 1
		while x < (cLine + 1):
			num_list.append(x)
			x += 1
		# 힌트 인덱스 조합을 위한 리스트
		
		result = list(itertools.combinations(num_list, nHint))
		# 모든 인덱스 조합 생성
		
		cal_index = []
	
		for i in range(len(result)):
			count = 0
			for j in range(len(result[i]) - 1):
				if( (result[i][j]+1) == result[i][j+1]):
					count += 1
			if (count == 0):
				cal_index.append(result[i])
		real_index = [list(row) for row in cal_index]
		#  생성한 조합 중 규칙 위반하는걸 걸러줌
		
		sol_list = [False] * nLine	
		
		# 조합으로 만든 인덱스를 실제 칸에 맞게 수정
		for j in range(len(cal_index)):
			count1 = 0

			for i in range(len(hint[k])):
				if hint[k][i] == 1 and count1 == 0:
					continue
				elif hint[k][i] > 1 and count1 == 0:
					count1 += (hint[k][i] - 1)
				else:
					real_index[j][i] = cal_index[j][i] + count1
					count1 += hint[k][i] - 1
		
			# 수정된 인덱스 위치에 true를 원래 힌트 숫자만큼 삽입해줌
			for i in range(len(cal_index[j])):
				a = real_index[j][i] - 1
				m = 0
				while m < hint[k][i]:
					sol_list[a] = True
					a += 1
					m += 1

			sol_set.append(sol_list)
			sol_list = [False] * nLine

		sol_dic[k] = sol_set
		sol_set = []
			
	return sol_dic


def randomSolutions(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    S = []
    for _ in range(nPopulation):
        s = []
        temp = []
        for i in range(len(solutions)):
            s = random.choice(solutions[i])
            temp += s
        S += [Solution(temp, constraints)]
    
    return S


def DGA(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    P = randomSolutions(constraints)

    while not converge(P, constraints):
        PP  = crossover(P, constraints)
        PPP = mutation(PP, constraints)
        P   = select(P, PPP, constraints)

        global iterations
        iterations += 1

        # 과정 출력
        # print("iteration", iterations)
        # print("fitness", P[0].fitness)
        # printSol(P[0], constraints)

    return best(P, constraints)


def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    P = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    for _ in range(nPopulation):
        child1 = []
        child2 = []
        parent1, parent2 = np.random.choice(P, p=prob, replace=False, size=2)

        for i in range(nLines):
            sIndex = i * nColumns
            fIndex = sIndex + nColumns

            if random.random() <= 0.5:
                child1 += parent1.points[sIndex : fIndex]
                child2 += parent2.points[sIndex : fIndex]

            else:
                child1 += parent2.points[sIndex : fIndex]
                child2 += parent1.points[sIndex : fIndex]

        PP    += [Solution(child1, constraints), Solution(child2, constraints)]

    return PP



def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for s in P:
        prob = 10/100
        newPoints = []

        for i in range(nLines):
            sIndex = i * nColumns
            fIndex = sIndex + nColumns
            if random.random() > prob:
                newPoints += s.points[sIndex : fIndex]
            else:
                newPoints += random.choice(solutions[i])
        PP += [Solution(newPoints, constraints)]

    return PP



def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = sorted(P, key = lambda s : (s.fitness, random.random()), reverse = True)
    PP = sorted(PP, key = lambda s : (s.fitness, random.random()), reverse = True)

    nParents  = int(2*nPopulation/10)+1
    nChildren = int(5*nPopulation/10)+1
    nRandom = nPopulation - nChildren - nParents

    bestOnes = P[:nParents] + PP[:nChildren]
    others   = randomSolutions(constraints)
    nextP = bestOnes + np.ndarray.tolist(np.random.choice(others, size=nRandom, replace=False))

    return nextP


def converge(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    for s in P:
        if s.fitness == 0:
            return True

    for i in range(len(P)-1):
        if P[i].points != P[i+1].points:
            return False

    return True


def best(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    for s in P:
        if s.fitness == 0:
            return s

    return P[0]

if __name__ == '__main__':
    main()