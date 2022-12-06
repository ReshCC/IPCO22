import gurobipy as gp
import numpy as np
from gurobipy import GRB
import re
from itertools import chain, combinations

teami = [0, 1, 2, 3, 4, 5]
teamj = [0, 1, 2, 3, 4, 5]
period = [0, 1, 2]
week = [0, 1, 2, 3, 4]

#creat model
tsp_model = gp.Model("tsp")

#add variables to the tsp_model
xijpw=[]
for i in teami:
    x = []
    for j in teamj:
        xi = []
        for p in period:
            xij = []
            for w in week:
                xij.append(tsp_model.addVar(lb=0.0, ub=1.0, vtype=GRB.INTEGER, name="x_" + str(i) + "_" + str(j) + "_" + str(p) + "_" + str(w)))
            xi.append(xij)
        x.append(xi)
    xijpw.append(x)

#add constraints
#c1: One match per pair of teams
for i in teami:
    for j in teamj:
        if i != j:
            sum = 0
            for p in period:
                for w in week:
                    sum=sum+xijpw[i][j][p][w]+xijpw[j][i][p][w]
            tsp_model.addConstr(sum, GRB.EQUAL, 1,"c1_"+str(i)+str(j))

#c2: Exactly 1 match per week per team
for i in teami:
    for w in week:
        sum1 = 0
        sum2 = 0
        for j in teamj:
            if i != j:
                for w in week:
                    sum1=sum1+xijpw[i][j][p][w]
                    sum2=sum2+xijpw[j][i][p][w]
                    sum=sum1+sum2
        tsp_model.addConstr(sum, GRB.EQUAL, 1,"c2_"+str(i)+str(w))

#c3: Atmost 2 teams per period per week
for w in week:
    for j in teamj:
        sum1=0
        sum2=0
        for i in teami:
            if i != j:
                for p in period:
                    sum1=sum+xijpw[i][j][p][w]
                    sum2=sum+xijpw[j][i][p][w]
                    sum=sum1+sum2
        tsp_model.addConstr(sum, GRB.LESS_EQUAL, 2,"c3_"+str(w)+str(j))

#c4: Each slot gets assigned
for w in week:
    for p in period:
        sum = 0
        for i in teami:
            for j in teamj:
                if i != j:
                   sum=sum+xijpw[i][j][p][w]
        tsp_model.addConstr(sum, GRB.EQUAL, 1,"c4_"+str(p)+str(w))

#c5: Pre-assign initial Week 1 slots
tsp_model.addConstr(x[0][1][0][0], EQUAL, 1,"c51")
tsp_model.addConstr(x[2][3][1][0], EQUAL, 1,"c52")
tsp_model.addConstr(x[4][5][2][0], EQUAL, 1,"c53")

#set objective function
obj=0
for i in teami:
    for j in teamj:
        for p in period:
            for w in week:
                obj = obj + xijpw[i][j][p][w]

tsp_model.setObjective(obj, GRB.MAXIMIZE)

#ask model to optimize
tsp_model.update()
tsp_model.optimize()

tsp_model.write("out.mps")







