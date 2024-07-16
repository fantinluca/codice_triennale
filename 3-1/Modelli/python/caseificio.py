#!/usr/bin/env python
# encoding: utf-8

import pyomo.environ as pe
from pyomo.opt import SolverFactory

def obj_rule(model):
    return sum(model.Tempo[p]*model.hours[p]*(model.Ricavo[p]-model.CostoLatte*model.Latte[p]) for p in model.Formaggi)

def buildmodel():
	# Model
	model = pe.AbstractModel()
	# sets
	model.Formaggi = pe.Set()
	# params
	model.Lb = pe.Param(model.Formaggi)
	model.Ricavo = pe.Param(model.Formaggi)
	model.Tempo = pe.Param(model.Formaggi)
	model.Latte = pe.Param(model.Formaggi)
	model.DispOre = pe.Param()
	model.DispLatte = pe.Param()
	model.CostoLatte = pe.Param()
	# variables
	model.hours = pe.Var(model.Formaggi, domain=pe.NonNegativeReals)
	# objective
	model.obj = pe.Objective(rule=obj_rule, sense=pe.maximize)
	# constraints
	model.c1 = pe.Constraint(expr = sum(model.hours[p] for p in model.Formaggi) <= model.DispOre)
	model.c2 = pe.Constraint(expr = 3 * model.gas + 4 * model.chloride <= 180)
	model.c3 = pe.Constraint(expr = model.chloride <= 40)
	return model


if __name__ == '__main__':
	model = buildmodel()
	opt = SolverFactory('cplex_persistent')
	opt.set_instance(model)
	res = opt.solve(tee=False)
	print("gas =", pe.value(model.gas))
	print("chloride =", pe.value(model.chloride))
