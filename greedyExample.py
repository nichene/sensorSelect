
# A Greedy Programming based Python Program for 0-1 Knapsack problem 
# Returns the approximate maximum value that can be put in Knapsack

def knapSack(capacity, value, size, numberOfItems):

    capacityInBag = 0
    valueInBag = 0

    #Sorting by vi/wi
    ratios = []
    for i in range(numberOfItems):
        ratios.append( (value[i] / size[i], value[i], size[i])  )

    ratios.sort(key = lambda x: x[0], reverse = True)

    print(ratios)

    for i in range(numberOfItems):
        if (ratios[i][2] + capacityInBag) <= capacity:
            capacityInBag += ratios[i][2]
            valueInBag +=  ratios[i][1]
        else:
            break

    return valueInBag


# Driver program to test above function 
value = [60, 100, 120] 
size = [10, 20, 30] 
capacity = 50
numberOfItems = len(size) 
print(knapSack(capacity, value, size, numberOfItems))