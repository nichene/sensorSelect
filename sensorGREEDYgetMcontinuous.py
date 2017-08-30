import traceback
from heapq import nlargest
import sys
import os
import random
import linecache
import datetime
import time
import numpy

global numDotipo
global listaItens

global usedBudget
global somaM

global done
global escolhidos



if len(sys.argv) == 7:
	n = int(sys.argv[1])
	m = int(sys.argv[2])
	B = int(sys.argv[3])
	s = int(sys.argv[4])
	random.seed(s) #inicializa o gerador de número aleatórios
	num_rep = int(sys.argv[5])
	numSensPedidos = int(sys.argv[6])

else:
	print("Informar: n m B s num_rep numSensPedidos")
	print("n = Sensores(i) por tipo")
	print("m = Numero de tipos(j)")
	print("B = Orçamento do usuário")
	print("s = Seed (Int)")
	print("num_rep = número de repetições")
	print("numSensPedidos = número total de sensores pedidos")
	exit(1)

dt = datetime.datetime.now()
dt = dt.strftime('%Y-%m-%d_%H-%M')
nomeDoDiretorio = str(n) + "_" + str(m) + "_" +  str(B) + "_" + str(s) + "_"+ str(num_rep) + "_" + str(numSensPedidos) + "_" + str(dt)
os.makedirs(nomeDoDiretorio)

def criarMatriz(linha, coluna):
	M = [[0 for x in range(coluna)] for y in range(linha)]
	return M


for num_da_rep in range(num_rep):

	usedBudget = 0
	somaM = 0

	arquivo = "/Users/nichenevercosa/SensorSelect/" + str(nomeDoDiretorio) + "/" + str(num_da_rep) + ".txt"
	arquivoRespostas = open(arquivo, "w")


	N = numpy.random.multinomial(numSensPedidos, [1.0/m]*m)

	print ("CRIANDO MATRIZES V, M e DivisaoMV\n")
	V = criarMatriz(n,m)
	M = criarMatriz(n,m)
	DivisaoMV = criarMatriz(n,m)

	for numDeTipos in range(m):
		numLinhas = random.sample(range(1,50001), n)
		numDoSensor = 0
		for numLinha in numLinhas:
			l = linecache.getline("file" + str(numDeTipos)+".csv", numLinha)
			tipo,indiceM,numValor,barraN = l.split(";")
			M[numDoSensor][numDeTipos] = round(float(indiceM),5)
			V[numDoSensor][numDeTipos] = round(float(numValor),2)
			numDoSensor += 1

	nrange = range(n)
	mrange = range(m)

	numDotipo = 0
	print ("OTIMIZANDO\n")

	tTime = time.time()
	done = False
	escolhidos = []
	for numSenEscolhidos in N:
		done = False
		listaItens = []

		if (numSenEscolhidos > 0):
			for i in nrange:
				valorDiv =  (M[i][numDotipo])
				item = ((i,numDotipo), valorDiv)
				listaItens.append(item)

			itensSorted = sorted(listaItens, key = lambda item: item[1], reverse = True) 
			countEscolhidos = 0

			for maioresIndices in itensSorted:
				iSensor, jSensor = maioresIndices[0][0], maioresIndices[0][1]
				valorm = M[iSensor][jSensor]
				valorv = V[iSensor][jSensor]

				if ((usedBudget + valorv) <= B):
					countEscolhidos += 1
					sensorescolhido = (iSensor,jSensor)
					escolhidos.append(sensorescolhido)

					somaM += valorm
					usedBudget += valorv

				if (countEscolhidos == numSenEscolhidos):
					#done = True
					break

			if (countEscolhidos < numSenEscolhidos):
				done = True
			if (done):
				arquivoRespostas.write("Nao exite uma solucao para este problema")
				break

		numDotipo += 1

	tempoDeOtimizacaoTime = time.time() - tTime
	tempoDeOtimizacaoTime = str(tempoDeOtimizacaoTime)

	print("GUARDANDO RESPOSTAS \n")
	if (usedBudget <= B):

		arquivoRespostas.write("N = " + str(N) + "\n")
		arquivoRespostas.write("M = " + str(M) + "\n")
		arquivoRespostas.write("V = " + str(V) + "\n")
		arquivoRespostas.write("MV = " + str(DivisaoMV)+ "\n")
		arquivoRespostas.write("Tempo de otimizacao (time.time) = " + tempoDeOtimizacaoTime + "\n")
		arquivoRespostas.write('The best known bound on the optimal objective  = ')
		arquivoRespostas.write(str(somaM)+ "\n")
		arquivoRespostas.write("O orcamento utilizado foi = "+ str(usedBudget)+ "\n")
		arquivoRespostas.write("Lista dos sensores escolhidos = "+ str(escolhidos))

	print ("\n---FIM da repeticao " + str(num_da_rep) + "---\n")

	arquivoRespostas.close()

print (" - - FIM - - \o/ ")
