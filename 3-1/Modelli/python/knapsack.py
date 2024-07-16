from pyomo.environ import *
from pyomo.opt import SolverFactory

n=7
m=3
profits=[294,93,96,155,294,96,155]
weights=[600,396,195,660,600,195,660]
capacity=884

def cap_rule(model, i):
    return sum(model.Weights[j] * model.x[i,j] for j in model.Items) <= model.Capacity

def take_rule(model, j):
    return sum(model.x[i,j] for i in model.Containers) <= 1

def buildmodel(**kwargs):
    # Model
    model = ConcreteModel()
    # Sets
    model.Items = RangeSet(0, n-1)
    model.Containers = RangeSet(0, m-1)
    # Parameters
    model.Profits = Param(model.Items, initialize=lambda model, j: profits[j])
    #model, j: parametri di lambda; ritorna profits[j]
    model.Weights = Param(model.Items, initialize=lambda model, j: weights[j])
    model.Capacity = capacity
    # Variables
    model.x = Var(model.Containers, model.Items, domain=boolean)
    # Objective
    model.obj = Objective(expr = sum(model.Profits[j]*model.x[i,j] for i in model.Container for j in model.Items), sense=maximize)
    # Constraints
    model.capc = Constraint(model.Containers, rule=cap_rule)
    model.takec = Constraint(model.Items, rule=take_rule)

if __name__=='__main__':
    model = buildmodel()
    opt = SolverFactory('cplex_persistent')
    opt.set_instance(model)
    opt.write("knapsack.lp")
    res = opt.solve(tee=False)
    print("Obj = {}".format(value(model.obj)))
    
