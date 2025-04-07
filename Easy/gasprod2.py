#!/usr/bin/env python
# encoding: utf-8

from pyscipopt import Model,quicksum

# Sets
products = ["gas", "chloride"]
components = ["nitrogen", "hydrogen", "chlorine"]

# Data
demand = {"gas": {"nitrogen": 1, "hydrogen": 3, "chlorine": 0},
          "chloride": {"nitrogen": 1, "hydrogen": 4, "chlorine": 1}}
profit = {"gas": 40, "chloride": 50}
stock = {"nitrogen": 50, "hydrogen": 180, "chlorine": 40}


def buildmodel():
	# Model
	model = Model()
	# variables
	x = {}
	for p in products:
		x[p] = model.addVar(name="x[%s]" % p)
	# objective
	model.setObjective(quicksum(profit[p] * x[p] for p in products), sense="maximize")
	# constraints
	for c in components:
		model.addCons(quicksum(demand[p][c] * x[p] for p in products) <= stock[c])
	model.data = x
	return model


if __name__ == '__main__':
	model = buildmodel()
	model.hideOutput() # silent mode
	model.writeProblem("prova.lp")
	model.optimize()
	print("Optimal value:", model.getObjVal())
	x = model.data
	for p in products:
		print("{} = {}".format(p, model.getVal(x[p])))
