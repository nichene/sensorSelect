
# A Dynamic Programming based Python Program for 0-1 Knapsack problem 
# Returns the maximum value that can be put in a knapsack of capacity(Budget) 

def knapSack(budget, matching, costs, numberOfSensors): 
    K = [[0 for x in range(budget+1)] for x in range(numberOfSensors+1)] 
  
    # Build table K[][] in bottom up manner 
    for i in range(numberOfSensors+1): 
        for w in range(budget+1): 
            if i==0 or w==0: 
                K[i][w] = 0
            elif costs[i-1] <= w: 
                K[i][w] = max(matching[i-1] + K[i-1][w-costs[i-1]],  K[i-1][w]) 
            else: 
                K[i][w] = K[i-1][w] 
  
    return K[numberOfSensors][budget] 
  
# Driver program to test above function 
matching = [60, 100, 120] 
costs = [10, 20, 30] 
budget = 50
numberOfSensors = len(costs) 
print(knapSack(budget, matching, costs, numberOfSensors)) 
  
 
