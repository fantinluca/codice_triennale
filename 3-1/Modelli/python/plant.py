#!/usr/bin/env python
# encoding: utf-8

from pyomo.environ import *
from pyomo.opt import SolverFactory

# Sets
estates = ["A", "B", "C"]
crops = ["corn", "wheat", "barley"]

# Data
dim = {"A": 600, "B": 700, "C": 500}
water = {"A": 8000, "B": 5500, "C": 6000}
profit = {"corn": 6500, "wheat": 5000, "barley": 6000}
consume = {"corn": 16, "wheat": 12, "barley": 14}
rest = 200

def obj(model):
    return sum(sum(model.profit[j]*model.x[i,j] for i in model.estates) for j in model.crops)

def buildmodel():
    # Model
    model = pe.ConcreteModel()
    # sets
    model.estates = Set(initialize=estates)
    model.crops = Set(initialize=crops)
    # params
    model.dim = Param(model.estates, initialize=dim)
    model.water = Param(model.estates, initialize=water)
    model.profit = Param(model.crops, initialize=profit)
    model.consume = Param(model.crops, initialize=consume)
    model.rest = Param(rest)
    # variables
    model.x = Var(model.estates, model.crops, domain=NonNegativeIntegers)
    model.y = Var(model.estates, domain=Boolean)
    # objective
    model.obj = Objective(rule=obj, sense=maximize)
    # constraints
    model.c1 = Constraint(expr=sum(model.y[i] for i in model.estates)==1)
    model.c2 = Constraint(model.estates, expr=sum(sum(model.consume[j]*model.x[i,j] for ))
