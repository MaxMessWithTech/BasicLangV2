from interpreter.utils.operators import conditionalOperators, equalityOperators
import copy


def trueFalse(splitLine, getVars) -> bool:
	"""
	--Conditional Interpreter--
	Takes a if statement and finds a boolean value from it
	"""
	from interpreter.utils.decInterp import decInterp
	from interpreter.utils.operators import operatorList
	
	# Find opperators
	oppIndices = list()
	for x in range(len(splitLine)):
		if splitLine[x] in conditionalOperators:
			opp = conditionalOperators[conditionalOperators.index(splitLine[x])]
			oppIndices.append({'index': x, 'opp': opp})

	# Creates a list of all of the comparisons
	out = list()
	lastIndex = -1
	for indexDict in oppIndices:
		out.append(splitLine[lastIndex + 1:indexDict['index']])
		out.append(splitLine[indexDict['index']])
		lastIndex = indexDict['index']
	out.append(splitLine[lastIndex + 1:])

	# takes list of comparisons and finds all of the values so we can compare
	for x in range(len(out)):
		if type(out[x]) == list:
			string = ""
			for y in out[x]:
				if y.find('"') == -1 and y not in operatorList:
					y = f'"{y}"'
				
				string = string + y
			out[x] = decInterp(string, getVars)[0]

	# Time to actually do the equality comparison

	preComp = list()
	for x in range(len(out)):
		if out[x] in equalityOperators:
			# This means that it is == or !=, take this and create a new list
			# +2 is there because it actually grabs one less then it should
			preComp.append(out[x -1:x+2])
		elif out[x] in conditionalOperators:
			preComp.append(out[x])
	
	# WE NEED TO HAVE THEM BE INSIDE OF EACH OTHER TO GET ONE OUTPUT
	# NVM - I have no idea what I was doing here 
	# It was: "list(list())"
	equalityComp = list()
	handeledIndices = [0]  # Keeps track of the indices that have been added
	for x in range(len(preComp)):
		if preComp[x] not in equalityOperators and preComp[x] in conditionalOperators:
			if len(equalityComp) != 0:
				save = copy.deepcopy(equalityComp)
				equalityComp.clear()
				equalityComp.append(save + preComp[x:x+2])

				handeledIndices.append(x-1)
				handeledIndices.append(x)
				handeledIndices.append(x+1)
			else:
				equalityComp.append(preComp[x-1:x+2])
				handeledIndices.append(x-1)
				handeledIndices.append(x)
				handeledIndices.append(x+1)
		elif len(preComp) == 1:
			equalityComp.append(preComp[x])
		elif x not in handeledIndices:
			return None
		# print(f"{blcolors.YELLOW}PreComp: {preComp}, preComp[x]: {preComp[x]}{blcolors.CLEAR}")
		# print(f"{blcolors.YELLOW}equalityComp: {equalityComp}{blcolors.CLEAR}")

	# print(equalityComp)
	equalityComp = equalityComp[0]

	# COMPARISON HERE | COMPARISON HERE | COMPARISON HERE
	output = False
	while type(equalityComp) != bool:
		equalityComp = equalityCompRecursion(equalityComp)
	
	output = equalityComp
	
	return output
	
def equalityCompRecursion(equalityComp):
	if isListInList(equalityComp):
		for x in range(len(equalityComp)):
			if isListInList(equalityComp[x]):
				equalityComp[x] = equalityCompRecursion(equalityComp[x])
			else:
				if type(equalityComp[x]) == list:
					equalityComp[x] = doIf(equalityComp[x])
	else:
		equalityComp = doIf(equalityComp)

	# print(f"{blcolors.MAGENTA}Returning equalityComp: {equalityComp}{blcolors.CLEAR}")
	return equalityComp


def isListInList(_list) -> bool:
	try:
		for val in _list:
			if type(val) == list:
				return True
				try:
					for val2 in val:
						if type(val2) == list:
							# print(f"Val: {val} -> True")
							return True
				except TypeError:
					pass
	except TypeError:
		pass
	# print(f"Val: {val} -> False")
	return False


# This does the actual comparison because it needs to be in two places
# And it was easier to just make a function for it
def doIf(equalityComp):
	if equalityComp[1] == "==":
		if equalityComp[0] == equalityComp[2]:
			equalityComp = True
		else:
			equalityComp = False
	elif equalityComp[1] == "!=":
		if equalityComp[0] != equalityComp[2]:
			equalityComp = True
		else:
			equalityComp = False
	elif equalityComp[1] == "&&":
		if equalityComp[0] and equalityComp[2]:
			equalityComp = True
		else:
			equalityComp = False
	elif equalityComp[1] == "||":
		if equalityComp[0] or equalityComp[2]:
			equalityComp = True
		else:
			equalityComp = False
	return equalityComp
