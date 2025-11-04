import random
import copy
import time
import statistics

# create a 3SAT problem with c clauses of 3 prepositions out of n possible variables
def createSat(c, n):
    problem = []

    while len(problem) != c: # keep adding clauses until desired amount
        var1 = (random.randint(1,n), random.randint(0,1)) # randomly choose a variable out of n options and whether it is negated (1) or not (0)
        var2 = (random.randint(1,n), random.randint(0,1))
        var3 = (random.randint(1,n), random.randint(0,1))
        problem.append((var1,var2,var3)) # append clause to current problem list
        problem = list(set(i for i in problem)) # use set logic to remove dupes from list

    return problem


# generate m 3SAT problems of c clauses and n variables
def generateProblems(m,c,n):
    problems = [None]*m

    for x in range(0,m):
        problems[x] = createSat(c,n)

    return problems


# given a problem and interpretation, find all unsatisfied clauses
def clausesUnsatisfied(problem, interp):
    clauses = []
    for i in problem: # for each clause
        disjunc = False
        for j in i: # for each prep in a clause
            val = j[0]-1
            if j[1] == 1: # if prep is negated
                disjunc = disjunc or not interp[val]
            else:
                disjunc = disjunc or interp[val]
        if disjunc == False:
            clauses.append(i)

    return clauses


# given a SAT problem, flips a var in an unsatisfied clause until it either finds a model or times out after 10 sec
def walkSAT(problem, n):
    model = [random.getrandbits(1)]*n # create a random assignment of T/F to vars

    unsatisfied = clausesUnsatisfied(problem,model)
    flipCounter = 0

    timeout_start = time.time()

    while time.time() < timeout_start + 10: # if model is not found in <10 sec, return none
        if len(unsatisfied) == 0: # if model is found (no clause unsatisfied), return
            break

        # choose a random unsatisfied clause
        randIdx = random.randint(0,len(unsatisfied)-1)
        clause = unsatisfied[randIdx]

        # makes copies of the current interp with a flipped var from the unsatisfied clause
        var1 = copy.deepcopy(model)
        var1[clause[0][0]-1] = not model[clause[0][0]-1]
        var2 = copy.deepcopy(model)
        var2[clause[1][0] - 1] = not model[clause[1][0] - 1]
        var3 = copy.deepcopy(model)
        var3[clause[2][0] - 1] = not model[clause[2][0] - 1]

        unsatisfiedVars = [(var1, clausesUnsatisfied(problem,var1)), (var2, clausesUnsatisfied(problem,var2)), (var3, clausesUnsatisfied(problem,var3))]

        if random.getrandbits(1) == 1: # 0.5 prob to choose greedily (flip var that minimizes unsatisfied)
            greedyChoice = min(unsatisfiedVars, key=lambda x: len(x[1]))
            model = greedyChoice[0]
            unsatisfied = greedyChoice[1]
        else: # 0.5 prob to choose randomly (flip random var)
            match random.randint(1,3):
                case 1:
                    model = var1
                    unsatisfied = unsatisfiedVars[0][1]
                case 2:
                    model = var2
                    unsatisfied = unsatisfiedVars[1][1]
                case 3:
                    model = var3
                    unsatisfied = unsatisfiedVars[2][1]
        flipCounter += 1

    if len(unsatisfied) == 0:
        return flipCounter
    else:
        return -1

# for a list of problems, return number of flips to solve each problem or -1 if timeout
def walkProblems(problems, n):
    numFlipsToSolve = []

    for problem in problems:
        numFlipsToSolve.append(walkSAT(problem, n))

    return numFlipsToSolve

# from list of flips, remove any timeout terminations (-1), find median and number of success
def lenAndMedian(flipSolution):
    successful = list(filter(lambda x: x != -1, flipSolution))
    if len(successful) == 0:
        return 0, 0
    else:
        median = statistics.median(successful)
        return median, len(successful)


# 50 3SAT problems for each integer value of c/n from 1 to 10
cn1 = generateProblems(50,20,20)
cn2 = generateProblems(50,40,20)
cn3 = generateProblems(50,60,20)
cn4 = generateProblems(50,80,20)
cn5 = generateProblems(50,100,20)
cn6 = generateProblems(50,120,20)
cn7 = generateProblems(50,140,20)
cn8 = generateProblems(50,160,20)
cn9 = generateProblems(50,180,20)
cn10 = generateProblems(50,200,20)

cn1result = walkProblems(cn1, 20)
cn1med = lenAndMedian(cn1result)
print("cn1 ", cn1result)
print(cn1med)

cn2result = walkProblems(cn2, 20)
cn2med = lenAndMedian(cn2result)
print("cn2 ", cn2result)
print(cn2med)

cn3result = walkProblems(cn3, 20)
cn3med = lenAndMedian(cn3result)
print("cn3 ", cn3result)
print(cn3med)

cn4result = walkProblems(cn4, 20)
cn4med = lenAndMedian(cn4result)
print("cn4 ", cn4result)
print(cn4med)

cn5result = walkProblems(cn5, 20)
cn5med = lenAndMedian(cn5result)
print("cn5 ", cn5result)
print(cn5med)

cn6result = walkProblems(cn6, 20)
cn6med = lenAndMedian(cn6result)
print("cn6 ", cn6result)
print(cn6med)

cn7result = walkProblems(cn7, 20)
cn7med = lenAndMedian(cn7result)
print("cn7 ", cn7result)
print(cn7med)

cn8result = walkProblems(cn8, 20)
cn8med = lenAndMedian(cn8result)
print("cn8 ", cn8result)
print(cn8med)

cn9result = walkProblems(cn9, 20)
cn9med = lenAndMedian(cn9result)
print("cn9 ", cn9result)
print(cn9med)

cn10result = walkProblems(cn10, 20)
cn10med = lenAndMedian(cn10result)
print("cn10 ", cn10result)
print(cn10med)