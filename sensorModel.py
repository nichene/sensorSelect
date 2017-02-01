from gurobipy import *
import traceback

n = 4 #sensores(i) por tipo
m = 5 #numero de tipos(j)
B = 9 #Budget do usuário


try:
	#CREATE MODEL
	model = Model("SensorSelect")

	#CREATE VARIABLES

	#matriz sensor i tipo j. 5 tipos, cada tipo tem 4 sensores.
	#matching é indice de 0-1.
	# M é o matching dos requisitos.  
	M = [[0.2, 0.3, 0.4, 0, 0],
	    [0, 0, 0.5, 0, 0],
	    [0, 0, 0.6, 0, 0],
	    [0.8, 1, 1, 1, 0]]

	nrange = range(n)
	mrange = range(m)

	#DECISION VARIABLE: X[i,j] == 1 if sensor is selected
	X = model.addVars(nrange, mrange, vtype=GRB.BINARY, name="X")
	#print(X[(0,0)])

	#SET OBJECTIVE
	listaProdutosMX = []
	for i in nrange:
		for j in mrange:
			listaProdutosMX.append(M[i][j] * X[(i,j)])

	model.setObjective(sum(listaProdutosMX),GRB.MAXIMIZE)

	#ADD CONSTRAINTS

	# Value. valores dos sensores i do tipo j. 
	V = [[20, 10, 1, 2, 3],
	     [ 2,  3, 5, 4,30],
	     [ 6,  8, 8, 9,10],
	     [ 1,  2, 4, 3, 5]]
	# Número de sensores escolhidos por tipo.
	N = [1, 1, 1, 1, 1]  	

	listaProdutosVX = []
	for i in nrange:
		for j in mrange:
			listaProdutosVX.append(V[i][j] * X[(i,j)])

	model.addConstr(sum(listaProdutosVX), GRB.LESS_EQUAL, B, "c0")
	
	for j in mrange:
		model.addConstr(X.sum('*',j), GRB.GREATER_EQUAL, N[j], "c1")

	#OPTIMIZE
	model.optimize()

	#PRINT DECISION VARIABLES
	for v in model.getVars():
		print(v.varName, v.x)

	print ('Obj: ', model.objVal)

except GurobiError:
	print('Error reported: ')
	traceback.print_exc()


