import numpy as np
import random

# create a 3SAT problem with c clauses of 3 prepositions out of n possible variables
def createSat(c, n):
    problem = []

    while len(problem) != c: # keep adding clauses until desired amount
        var1 = (random.randint(0,n), random.randint(0,1)) # randomly choose a variable out of n options and whether it is negated (1) or not (0)
        var2 = (random.randint(0,n), random.randint(0,1))
        var3 = (random.randint(0,n), random.randint(0,1))
        problem.append((var1,var2,var3)) # append clause to current problem list
        problem = list(set(i for i in problem)) # use set logic to remove dups from list

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
