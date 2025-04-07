#!/usr/bin/env python
# encoding: utf-8

from pyscipopt import Model,quicksum

n = 7
m = 3
profits = [294, 93, 96, 155, 294, 96, 155]
weights = [600, 396, 195, 660, 600, 195, 660]
capacity = 884


def buildmodel():
	# Model
	model = Model()
	# variables
	x= {}
	for i in range(m):
		for j in range(n):
			x[(i,j)] = model.addVar(name="x[%d,%d]" % (i,j), vtype='B')
	# objective
	model.setObjective(quicksum(profits[j] * x[(i,j)] for i in range(m) for j in range(n)), sense="maximize")
	# constraints
	for j in range(n):
		model.addCons(quicksum(x[(i,j)] for i in range(m)) <= 1)
	for i in range(m):
		model.addCons(quicksum(weights[j] * x[(i,j)] for j in range(n)) <= capacity)
	model.data = x
	return model


if __name__ == '__main__':
	model = buildmodel()
	model.hideOutput() # silent mode
	model.optimize()
	print("Optimal value:", model.getObjVal())
	x = model.data
	for i in range(m):
		for j in range(n):
			print("{} = {}".format((i,j), model.getVal(x[(i,j)])))
