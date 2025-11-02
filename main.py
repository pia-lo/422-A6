import random
import copy
import time

# create a 3SAT problem with c clauses of 3 prepositions out of n possible variables
def createSat(c, n):
    problem = []

    while len(problem) != c: # keep adding clauses until desired amount
        var1 = (random.randint(0,n), random.randint(0,1)) # randomly choose a variable out of n options and whether it is negated (1) or not (0)
        var2 = (random.randint(0,n), random.randint(0,1))
        var3 = (random.randint(0,n), random.randint(0,1))
        problem.append((var1,var2,var3)) # append clause to current problem list
        problem = list(set(i for i in problem)) # use set logic to remove dupes from list

    return problem


# generate m 3SAT problems of c clauses and n variables
def generateProblems(m,c,n):
    problems = [None]*m

    for x in range(0,m):
        problems[x] = createSat(c,n)

    return problems


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


# find the number of unsatisfied clauses for a given 3SAT problem and interpretation
def numUnsatisfied(problem, interp):
    clausesUnsatisfied = 0
    conjuncTrue = False
    for i in problem: # for each clause
        disjuncTrue = False
        for j in i: # for each prep in a clause
            val = j[0]-1
            if j[1] == 1: # if prep is negated
                disjuncTrue = disjuncTrue or not interp[val]
            else:
                disjuncTrue = disjuncTrue or interp[val]
        conjuncTrue = conjuncTrue and disjuncTrue
        if disjuncTrue == False:
            clausesUnsatisfied = clausesUnsatisfied + 1

    return clausesUnsatisfied

# finds a clause that is unsatisfied
def findUnsatisfied(problem, interp):
    for i in problem:
        disjunc = False
        for j in i:
            val = j[0] - 1
            if j[1] == 1:  # if prep is negated
                disjunc = disjunc or not interp[val]
            else:
                disjunc = disjunc or interp[val]
        if disjunc == False:
            return i
    return None


# given a problem and a random interp, flips a var in an unsatisfied clause until it either finds a model or times out after 10 sec
def walkSAT(problem, n):
    model = [random.getrandbits(1)]*n # create a random assignment of T/F to vars

    unsatisfied = numUnsatisfied(problem,model)
    #print("init vals ", model, unsatisfied)

    timeout_start = time.time()

    while time.time() < timeout_start + 10: # if model is not found in <10 sec, return none
        if unsatisfied == 0: # if model is found (no clause unsatisfied), return model
            break

        clause = findUnsatisfied(problem,model) # find an unsatisfied clause

        var1 = copy.deepcopy(model)
        var1[clause[0][0]-1] = not model[clause[0][0]-1] # copy the model and flip the value of a var
        var2 = copy.deepcopy(model)
        var2[clause[1][0] - 1] = not model[clause[1][0] - 1]
        var3 = copy.deepcopy(model)
        var3[clause[2][0] - 1] = not model[clause[2][0] - 1]

        unsatisfiedVars = [(var1, numUnsatisfied(problem,var1)), (var2, numUnsatisfied(problem,var2)), (var3, numUnsatisfied(problem,var3))]
        #print("here are options ", unsatisfiedVars)

        if random.getrandbits(1) == 1: # 0.5 prob to choose greedily (flip var that minimizes unsatisfied)
            greedyChoice = min(unsatisfiedVars, key=lambda x: x[1])
            #print("we are greedy ", greedyChoice)
            model = greedyChoice[0]
            unsatisfied = greedyChoice[1]
        else: # 0.5 prob to choose randomly (flip random var)
            match random.randint(1,3):
                case 1:
                    model = var1
                    unsatisfied = unsatisfiedVars[0][1]
                    #print("we are random 1 ", model, unsatisfied)
                case 2:
                    model = var2
                    unsatisfied = unsatisfiedVars[1][1]
                    #print("we are random 2 ", model, unsatisfied)
                case 3:
                    model = var3
                    unsatisfied = unsatisfiedVars[2][1]
                    #print("we are random 3 ", model, unsatisfied)

    if unsatisfied == 0:
        return model
    else:
        return None

testp = [((2, 1), (2, 1), (2, 1)), ((2, 0), (2, 0), (2, 0))]

result = walkSAT(testp, 3)
print(result)