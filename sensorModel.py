from gurobipy import *
import traceback

n = 4 #Sensores(i) por tipo
m = 5 #Numero de tipos(j)
B = 9 #Orçamento do usuário


try:
	#Criação do modelo
	model = Model("SensorSelect")

	#Matriz sensor i tipo j. 5 tipos, cada tipo tem 4 sensores.
	#M = atendimento dos requisitos, variando entre 0-1.  
	M = [[0.2, 0.3, 0.4, 0, 0],
	    [0, 0, 0.5, 0, 0],
	    [0, 0, 0.6, 0, 0],
	    [0.8, 1, 1, 1, 0]]

	nrange = range(n)
	mrange = range(m)

	#Criação das variáveis de decisão: 
	#X[i,j] == 1 se sensor for selecionado; 0 caso contrário
	X = model.addVars(nrange, mrange, vtype=GRB.BINARY, name="X")
	#print(X[(0,0)])

	#Estruturação da função objetivo
	listaProdutosMX = []
	for i in nrange:
		for j in mrange:
			listaProdutosMX.append(M[i][j] * X[(i,j)])

	model.setObjective(sum(listaProdutosMX),GRB.MAXIMIZE)

	#Definição dos custos dos sensores.
	# V = custos dos sensores i do tipo j. 
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

	#Definição das restrições
	model.addConstr(sum(listaProdutosVX), GRB.LESS_EQUAL, B, "c0")
	
	for j in mrange:
		model.addConstr(X.sum('*',j), GRB.GREATER_EQUAL, N[j], "c1")

	#Otimização
	model.optimize()
	
	#resposta das variáveis de decisão.
	if (model.solCount > 0 ): 
		for v in model.getVars():
			print(v.varName, v.x)

		print ('Obj: ', model.objVal)
	else:
		print("No Vars")

except GurobiError:
	print('Error reported: ')
	traceback.print_exc()


