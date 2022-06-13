import numpy as np
from numpy import random
from DGA.nonogram import Game, Rules, check_solution
from DGA.util     import read_rules_file, print_solution, create_constraints, fitness as evaluate_fitness
import itertools, random
import time

class Solution:
    """
    답안을 저장하는 솔루션 객체입니다.
    """
    def __init__(self, points, constraints):
        self.points  = points
        self.fitness = evaluate_fitness(points, constraints)

def main(rules, nLines, nColumns, nPoints, nPopulation = 500):
    """
    전반적인 알고리즘을 실행해주는 메인 함수입니다.
    """    
    constraints = rules, nLines, nColumns, nLines*nColumns, nPopulation

    global solutions
    solutions = line_solution(rules)

    my_sol = dga(constraints)
    print(my_sol.points)
    return my_sol.points, iterations

iterations = 0

def line_solution(rules):
	"""
    본격적인 문제 해결에 앞서 힌트를 중족하는 조함을 생성해주는 함수입니다.
    라인솔루션에서 생성된 조합을 바탕으로 모집단을 생성합니다.
    """
	hint = rules.lines
    #가로줄 힌트 리스트 저장 
	n_line = len(rules.columns)
	# 가로줄 칸 수 확인
	sol_set = []
	sol_dic = {}

	for k in range(len(hint)):
		n_hint = len(hint[k])
		
		c_line = n_line - (sum(hint[k]) - n_hint)

		# 가로줄 칸 개수 조정
		num_list = []
		x = 1
		while x < (c_line + 1):
			num_list.append(x)
			x += 1
		# 힌트 인덱스 조합을 해주는 리스트
		result = list(itertools.combinations(num_list, n_hint))
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
		sol_list = [False] * n_line		
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
			sol_list = [False] * n_line

		sol_dic[k] = sol_set
		sol_set = []			
	return sol_dic


def random_solutions(constraints):
    """
    모집단의 생성과 적합도를 평가를 해주는 함수입니다.
    solutions을 기반으로 모집단을 생성합니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints
    S = []
    for _ in range(n_population):
        s = []
        temp = []
        for i in range(len(solutions)):
            s = random.choice(solutions[i])
            temp += s
        S += [Solution(temp, constraints)]
    return S


def dga(constraints):
    """
    개선된 GA 알고리즘 함수입니다.
    교차와 변이 선택을 반복하며 문제의 솔루션을 찾아냅니다.

    변수 P에는 모집단과 각각의 적합도가 저장되어 있습니다.
    종료조건(converge)을 만족할 때까지 실행을 반복합니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints
    P = random_solutions(constraints)

    while not converge(P, constraints):
        PP  = crossover(P, constraints)
        PPP = mutation(PP, constraints)
        P   = select(P, PPP, constraints)

        global iterations
        iterations += 1

        print("iteration", iterations)
        print("fitness", P[0].fitness)
        print_solution(P[0], constraints)

    return best(P, constraints)


def crossover(P, constraints):
    """
    교차선택을 하는 함수입니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints

    PP = []
    P = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (n_population*(n_population+1))/2
    prob=[i/n for i in range(1, n_population+1)]

    for _ in range(n_population):
        child1 = []
        child2 = []
        parent1, parent2 = np.random.choice(P, p=prob, replace=False, size=2)

        for i in range(n_lines):
            s_index = i * n_columns
            f_index = s_index + n_columns

            if random.random() <= 0.5:
                child1 += parent1.points[s_index : f_index]
                child2 += parent2.points[s_index : f_index]
            else:
                child1 += parent2.points[s_index : f_index]
                child2 += parent1.points[s_index : f_index]

        PP    += [Solution(child1, constraints), Solution(child2, constraints)]
    return PP


def mutation(P, constraints):
    """
    변이를 일으키는 함수입니다.
    변이 확률은 여러 차례의 테스트를 통해 결정하였다.
    15*15 이하의 작은 사이즈의 퍼즐은 10%의 변이확룰을 가지며, 15*15 이상의 퍼즐은 20%의 변이확률을 가진다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints

    PP = []
    for s in P:
        if n_lines>=15 and n_columns>=15:
            prob = 20/100
        else:
            prob = 10/100

        new_points = []

        for i in range(n_lines):
            s_index = i * n_columns
            f_index = s_index + n_columns
            if random.random() > prob:
                new_points += s.points[s_index : f_index]
            else:
                new_points += random.choice(solutions[i])
        PP += [Solution(new_points, constraints)]
    return PP



def select(P, PP, constraints):
    """
    crossover와 mutation함수가 만들어낸 교차선택과 변이를 바탕으로 새로운 모집단을 생성합니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints

    P = sorted(P, key = lambda s : (s.fitness, random.random()), reverse = True)
    PP = sorted(PP, key = lambda s : (s.fitness, random.random()), reverse = True)

    n_parents  = int(2*n_population/10)+1
    n_children = int(5*n_population/10)+1
    n_random = n_population - n_children - n_parents

    best_ones = P[:n_parents] + PP[:n_children]
    others   = random_solutions(constraints)
    next_p = best_ones + np.ndarray.tolist(np.random.choice(others, size=n_random, replace=False))

    return next_p


def converge(P, constraints):
    """
    종료조건을 확인하는 함수입니다.
    적합도가 0인 답안지가 있는지 확인합니다.
    적합도가 0인 답안지를 찾아내면 그 답안지를 반환하고 이 dga함수가 종료됩니다.
    만일 답안지가 있지 않다면 자식답안지들을 만들어냅니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints

    end = time.time()
    check = end - start

    # 실행 제한시간
    if check > 1800:        
        print("Time Over")
        return True

    for s in P:
        if s.fitness == 0:
            return True

    for i in range(len(P)-1):
        if P[i].points != P[i+1].points:
            return False
    return True

def best(P, constraints):
    """
    fitness가 0인 경우를 찾아 반환하는 함수입니다.
    """
    rules, n_lines, n_columns, n_points, n_population = constraints

    for s in P:
        if s.fitness == 0:
            return s

    return P[0]

start = time.time()
if __name__ == "__main__":
    main()