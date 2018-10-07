import sys
import math
import random 

#Create 20 CSVs, one for each type of sensor.
#Each line contains: j; M; V;\n 

if len(sys.argv) == 3:
	seed = int(sys.argv[1])
	random.seed(seed) 
	beta = int(sys.argv[2])
else:
	print("Informar: seed e beta")
	exit(1)


for j in range(20):
	fileName = "file" + str(j) + ".csv"
	csv = open(fileName, "w") 

	for line in range(50000):

		#Sensor type 
		csv.write(str(j)+ ";")

		#Sensor matching: number from 0 to 1. 
		matchingValue = random.betavariate(1, beta) 
		csv.write(str(matchingValue) + ";")

		#Sensor value. Mean = 10. Standard deviation = 5.
		sensorValue = abs(random.gauss(10,5)) #No negative numbers
		sensorValue = "%.2f" % sensorValue
		csv.write(str(sensorValue) + ";\n")
	
	csv.close()

 
