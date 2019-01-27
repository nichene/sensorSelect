# A GurobiPy based Python Program for 0-1 Knapsack problem 
# Returns the maximum value that can be put in Knapsack

from gurobipy import *
import traceback

try:

    # define data 
    profit = [60, 100, 120] 
    weight = [10, 20, 30] 
    capacity = 50
    numberOfItems = range(3)

    # Create dicts for tupledict.prod() function
    objProfit = dict(zip(numberOfItems, profit))
    objWeight = dict(zip(numberOfItems, weight))

    # Create a new model
    m = Model("knapsack")

    # Create variables
    x = m.addVars(numberOfItems, vtype=GRB.BINARY, name="x")

    # Set objective function
    m.setObjective(x.prod(objProfit), GRB.MAXIMIZE)

    # Add constraint
    m.addConstr(x.prod(objWeight), GRB.LESS_EQUAL, capacity)

    #solve model
    m.optimize()

    #Display solution
    #x = 1.0 when selected
    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)

    if m.SolCount > 0:
        m.printAttr('x')

except GurobiError as e:
    print('Error reported: ')
    traceback.print_exc()
