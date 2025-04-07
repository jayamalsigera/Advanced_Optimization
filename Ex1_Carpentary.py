from pyscipopt import Model,quicksum

# Sets
products = ["std", "lux"]
components = ["assembly", "finish"]

# Data
time = {"std": {"assembly": 2, "finish": 3},
          "lux": {"assembly": 4, "finish": 5}}
revenue = {"std": 300, "lux": 400}
employees = {"assembly": 20, "finish": 30}
weekly_hrs = 40
maxProd = {"std":500,"lux":300 }


def buildmodel():
	# Model
	model = Model()
	# variables
	x = {}
	for p in products:
		x[p] = model.addVar(name="x[%s]" % p)
	# objective
	model.setObjective(quicksum(revenue[p] * x[p] for p in products), sense="maximize")
	# constraints
	for c in components:
		model.addCons(quicksum(time[p][c] * x[p] for p in products) <= employees[c]*weekly_hrs)
		model.addCons(x["lux"] <= 0.5* quicksum(x[p] for p in products))
		model.addCons(x[p]>=0)
		model.addCons(x[p]<=maxProd[p])
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

