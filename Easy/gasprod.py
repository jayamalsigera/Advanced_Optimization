#!/usr/bin/env python
# encoding: utf-8

from pyscipopt import Model

def buildmodel():
	# Model
	model = Model()
	# variables
	gas = model.addVar("gas")
	chloride = model.addVar("chloride")
	# objective
	model.setObjective(40 * gas + 50 * chloride, sense="maximize")
	# constraints
	model.addCons(gas + chloride <= 50)
	model.addCons(3 * gas + 4 * chloride <= 180)
	model.addCons(chloride <= 40)
	model.data = gas,chloride
	return model


if __name__ == '__main__':
	model = buildmodel()
	#model.hideOutput() # silent mode
	model.optimize()
	print("Optimal value:", model.getObjVal())
	gas,chloride = model.data
	print("gas =", model.getVal(gas))
	print("chloride =", model.getVal(chloride))
