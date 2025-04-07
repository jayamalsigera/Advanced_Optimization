#!/usr/bin/env python
# encoding: utf-8

from pyscipopt import Model,quicksum

# Sets
Sources = ['A', 'B']
Destinations = [1, 2, 3]

# Params
Cost = {}
Cost['A', 1] = 2.5
Cost['A', 2] = 1.7
Cost['A', 3] = 1.8
Cost['B', 1] = 2.5
Cost['B', 2] = 1.8
Cost['B', 3] = 1.4

Production = {'A': 350, 'B': 600 }
Demand =  {1: 325, 2: 300, 3: 275}

def buildmodel():
	# Model
	model = Model()
	# variables
	x = {}
	for s in Sources:
		for d in Destinations:
			x[s,d] = model.addVar(name="x[%s,%i]" % (s,d))
	# objective
	model.setObjective(quicksum(Cost[s,d]*x[s,d] for s in Sources for d in Destinations))
	# constraints
	for s in Sources:
		model.addCons(quicksum(x[s,d] for d in Destinations) <= Production[s])
	for d in Destinations:
		model.addCons(quicksum(x[s,d] for s in Sources) >= Demand[d])
	model.data = x
	return model


if __name__ == '__main__':
	model = buildmodel()
	# model.writeProblem('transport.lp')
	model.hideOutput() # silent mode
	model.optimize()
	print("Optimal value:", model.getObjVal())
	x = model.data
	for s in Sources:
		for d in Destinations:
			print("{} -> {}: {}".format(s, d, model.getVal(x[s,d])))
