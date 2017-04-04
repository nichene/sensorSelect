from gurobipy import *
import traceback
import sys 
import random
import linecache
import datetime
import time
import numpy

if len(sys.argv) == 7:
	n = int(sys.argv[1])  
	m = int(sys.argv[2]) 
	B = int(sys.argv[3])
	s = int(sys.argv[4])
	random.seed(s) #inicializa o gerador de número aleatórios
	num_rep = int(sys.argv[5])
	numSensPedidos = float(sys.argv[6])
	 
else:
	print("Informar: n m B s num_rep numSensPedidos")
	print("n = Sensores(i) por tipo")
	print("m = Numero de tipos(j)")
	print("B = Orçamento do usuário")
	print("s = Seed (Int)")
	print("num_rep = número de repetições")
	print("numSensPedidos = número total de sensores pedidos")  
	exit(1) 

nomeDoDiretorio = str(n) + "_" + str(m) + "_" +  str(B) + "_" + str(s) + "_"+ str(num_rep) + "_" + str(datetime.datetime.now())
os.makedirs(nomeDoDiretorio)


def criarMatriz(linha, coluna): 
	M = [[0 for x in range(coluna)] for y in range(linha)]
	return M


for num_da_rep in range(num_rep):

	# N = Número de sensores escolhidos por tipo.
	# exemplo: N = [1, 1, 3, 1, 1, 0, 0]
	#A probabilidade de ocorrer cada um é a mesma. Total de sensores é numSensPedidos.
	#N = numpy.random.multinomial(numSensPedidos, [1/numSensPedidos]*m)
	N = numpy.random.multinomial(numSensPedidos, [1/m]*m)

	try:
		#CRIAÇÃO DO MODELO
		print("CRIANDO O MODELO . . . ")
		model = Model("SensorSelect")

		#M = atendimento dos requisitos, variando entre 0-1
		#Matriz sensor i tipo j.
		#exemplo: 5 tipos, cada tipo tem 4 sensores.  
		#	   M = [[0.2, 0.3, 0.4, 0, 0],
		#    		[0, 0, 0.5, 0, 0],
		#    		[0, 0, 0.6, 0, 0],
		#    		[0.8, 1, 1, 1, 0]]


		#V = custos dos sensores i do tipo j. 
		#exemplo: V = [[20.00, 10.22, 1.12, 2.32, 3.34],
		#     	       [ 2.99,  3.87, 5.22, 4.21,30.34],
		#              [ 6.11,  8.33, 8.44, 4.39,10.00],
		#              [ 1.11,  2.21, 4.34, 4.53, 5.43]]

		print("CRIANDO AS MATIZES M e V . . .") 
		M = criarMatriz(n,m)
		V = criarMatriz(n,m)	 	

		for numDeTipos in range(m): #passar por todos os arquivos CSVs dos tipos de sensores 
		
			#Randomicamente escolhe n linhas de um arquivo.
			#exemplo: pegar 4 sensores de uma lista de 2500.
			#numLinhas = random.sample(range(1,50001), n)
			numLinhas = random.sample(range(1,50001), n)
		
			numDoSensor = 0
			for numLinha in numLinhas:
				l = linecache.getline("file" + str(numDeTipos)+".csv", numLinha)
				tipo,indiceM,numValor,barraN = l.split(";") 
				M[numDoSensor][numDeTipos] = indiceM  
				V[numDoSensor][numDeTipos] = numValor
				numDoSensor += 1

		nrange = range(n)
		mrange = range(m)

		#CRIAÇÃO DAS VARIÁVEIS DE DECISÃO 
		print("CRIANDO AS VARIÁVEIS DE DECISÃO . . .")
		#X[i,j] == 1 se sensor for selecionado; 0 caso contrário
		X = model.addVars(nrange, mrange, vtype=GRB.BINARY, name="X")
		#print(X[(0,0)])

		#ESTRUTURAÇÃO DA FUNÇÃO OBJETIVO
		print("ESTRUTURAÇÃO DA FUNÇÃO OBJETIVO . . .") 
		listaProdutosMX = []
		for i in nrange:
			for j in mrange:
				listaProdutosMX.append(M[i][j] * X[(i,j)])
		#listaProdutosMX = numpy.multiply(M,X)

		model.setObjective(sum(listaProdutosMX),GRB.MAXIMIZE)

		listaProdutosVX = []
		for i in nrange:
			for j in mrange:
				listaProdutosVX.append(V[i][j] * X[(i,j)])

		#DEFINIÇÃO DAS RESTRIÇÕES
		print("ADICIONANDO AS RESTRIÇÕES . . . ")
		
		#listaProdutosVX = numpy.multiply(V,X)
		model.addConstr(sum(listaProdutosVX), GRB.LESS_EQUAL, B, "c0")
	
		for j in mrange:
			model.addConstr(X.sum('*',j), GRB.GREATER_EQUAL, N[j], "c1")

		#OTIMIZAÇÃO
		print("OTIMIZANDO . . .") 
		#time.time = tempo total
		#time.clock = tempo em que procesador trabalhou nas funções	 	
		tClock = time.clock()
		tTime = time.time()
		model.optimize()
		tempoDeOtimizacaoTime = time.time() - tTime 
		tempoDeOtimizacaoClock = time.clock() - tClock 

		tempoDeOtimizacaoTime = str(tempoDeOtimizacaoTime)
		tempoDeOtimizacaoClock = str(tempoDeOtimizacaoClock)	
	
		#ESCRITA DAS RESPOSTAS
		print("SALVANDO AS RESPOSTAS ENCONTRADAS . . . ") 
		arquivo = "/Users/nichenevercosa/SensorSelect/" + str(nomeDoDiretorio) + "/" + str(num_da_rep) + ".txt"	
		arquivoRespostas = open(arquivo, "w") 
		
		if (model.solCount > 0 ):
			arquivoRespostas.write("N = " + str(N) + "\n")
			arquivoRespostas.write("M = " + str(M) + "\n")
			arquivoRespostas.write("V = " + str(V) + "\n") 	
			
			arquivoRespostas.write("Tempo de otimizacao (time.time) = " + tempoDeOtimizacaoTime + "\n")
			arquivoRespostas.write("Tempo de otimizacao (time.clock) = "+ tempoDeOtimizacaoClock + "\n")
	
			arquivoRespostas.write('Objective value for the current solution = ')
			arquivoRespostas.write(str(model.objVal)+ "\n")
			arquivoRespostas.write('The best known bound on the optimal objective = ')
			arquivoRespostas.write(str(model.ObjBoundC)+ "\n")
			
			for v in model.getVars():
				arquivoRespostas.write(str(v.varName)+" = ")
				arquivoRespostas.write(str(v.x)+ "\n")
		
		else:
			arquivoRespostas.write("Nao exite uma solucao para este problema")
		print("FIM DA REPETIÇÃO " + str(num_da_rep) + " . . . ") 
	
	except GurobiError:
		print('Error reported: ')
		traceback.print_exc()

print(" . .  END . .  \o/ ")
