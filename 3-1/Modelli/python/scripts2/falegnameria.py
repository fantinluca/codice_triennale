#!/usr/bin/env python
# encoding: utf-8

from pyomo.environ import *
from pyomo.opt import SolverFactory


def bounds_rule(model, p):
	return (0, model.Ub[p])

def obj_rule(model):
	return sum(model.Ricavo[p] * model.x[p] for p in model.Porte)

def fasi_rule(model, f):
	return sum(model.Ore[p,f] * model.x[p] for p in model.Porte) <= model.Operai[f]*model.OreSettimana

def ratio_rule(model):
	return model.x["lusso"] <= 0.5 * sum(model.x[p] for p in model.Porte)


def buildmodel():
	# Model
	model = AbstractModel()
	# sets
	model.Porte = Set()
	model.Fasi = Set()
	# params
	model.Ore = Param(model.Porte, model.Fasi)
	model.Ub = Param(model.Porte)
	model.Ricavo = Param(model.Porte)
	model.Operai = Param(model.Fasi)
	model.OreSettimana = Param()
	# variables
	model.x = Var(model.Porte, domain=NonNegativeIntegers, bounds=bounds_rule)
	# objective
	model.obj = Objective(rule=obj_rule, sense=maximize)
	# constraints
	model.fc = Constraint(model.Fasi, rule=fasi_rule)
	model.rc = Constraint(rule=ratio_rule)
	return model


if __name__ == '__main__':
	import sys
	model = buildmodel()
	opt = SolverFactory('cplex_persistent')
	instance = model.create_instance(sys.argv[1])
	opt.set_instance(instance)
	res = opt.solve(tee=False)
	for p in instance.x:
		print("x[{}] = {}".format(p, value(instance.x[p])))
