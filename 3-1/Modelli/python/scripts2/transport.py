#!/usr/bin/env python
# encoding: utf-8

from pyomo.environ import *
from pyomo.opt import SolverFactory


def obj_rule(model):
	return sum(model.Costo[i,j] * model.x[i,j] for i in model.Sorgenti for j in model.Destinazioni)

def source_rule(model, i):
	return sum(model.x[i,j] for j in model.Destinazioni) <= model.Produzione[i]

def dest_rule(model, j):
	return sum(model.x[i,j] for i in model.Sorgenti) >= model.Domanda[j]


def buildmodel():
	# Model
	model = AbstractModel()
	# sets
	model.Sorgenti = Set()
	model.Destinazioni = Set()
	# params
	model.Costo = Param(model.Sorgenti, model.Destinazioni)
	model.Produzione = Param(model.Sorgenti)
	model.Domanda = Param(model.Destinazioni)
	# variables
	model.x = Var(model.Sorgenti, model.Destinazioni, domain=NonNegativeReals)
	# objective
	model.obj = Objective(rule=obj_rule)
	# constraints
	model.sc = Constraint(model.Sorgenti, rule=source_rule)
	model.dc = Constraint(model.Destinazioni, rule=dest_rule)
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