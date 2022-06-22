from typing import Tuple
from collections import OrderedDict

from interpreter.utils.blcolors import blcolors
from interpreter.utils.splitByOpp import splitByOpp
from interpreter.utils.removeSpacesNotInStr import removeSpacesNotInStr
from interpreter.utils.operators import operatorList, conditionalOperators
from interpreter.utils.mathHandler import printLn, stringToMath
from interpreter.utils.trueFalse import trueFalse


def partInterp(
		line, getVars, errorCallback, returnOutputStr=True, createVarCallback=None
) -> Tuple[any, list, bool]:
	"""
	--Part Interpreter--
	Inputs: line(str) - Current Value, getVars(def) - call back
	Returns: Formatted Line(str), Data Type(list), valid(bool)

	Finding Var references and replaces them with their value in the line
	"""

	# getVars gets a list with all the currently defined vars in runtime
	varList = getVars()
	splitLine = splitByOpp(line)
	dataTypes = list()  # Keeps track of the data types of every value
	valid = True  # Stays True until we find a var of a different type

	# ! CHECK FOR: str and int - EVENTUALLY: list, float, and bool
	for x in range(len(splitLine)):
		# Checks for a string
		if splitLine[x].find('"') != -1:
			if "str" not in dataTypes and len(dataTypes) != 0 and valid:
				valid = False
			dataTypes.append("str")
			try:
				splitLine[x] = removeSpacesNotInStr(splitLine[x])
			except ValueError:
				errorCallback(
					f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
					f"{blcolors.RED}  Statement {repr(splitLine[x])} was detected as a string, but is invalid!{blcolors.CLEAR}"
				)

		# Checks for a number
		elif splitLine[x].replace(" ", "").replace("-", "").isnumeric():
			if "numb" not in dataTypes and len(dataTypes) != 0 and valid:
				valid = False
			dataTypes.append("numb")

			splitLine[x] = splitLine[x].replace(" ", "")

		# Checks for boolean
		elif splitLine[x].replace(" ", "") in ["true", "false"]:
			if "bool" not in dataTypes and len(dataTypes) != 0 and valid:
				valid = False
			dataTypes.append("bool")

			splitLine[x] = splitLine[x].replace(" ", "")

		# Checks for a var
		elif splitLine[x] not in operatorList and "\x1b[31m[\x1b[1mERROR\x1b[0m\x1b[31m]\x1b[0m" not in splitLine[x]:

			splitLine[x] = splitLine[x].replace(" ", "")
			# THIS IS SUPER INEFFICIENT - IF THINGS ARE SLOW, THIS IS PROBABLY A PROBLEM
			for var in varList:
				if var.name == splitLine[x]:

					# Since type() gives a weird string, this converts it
					if type(var.value) is str:
						splitLine[x] = f"\"{var.value}\""
						varType = "str"
					elif type(var.value) is int or type(var.value) is float:
						splitLine[x] = var.value
						varType = "numb"
					elif type(var.value) is list:
						splitLine[x] = var.value
						varType = "list"
					else:
						varType = None
					if varType not in dataTypes and len(dataTypes) != 0 and valid:
						valid = False
					dataTypes.append(varType)
					break
			else:
				# !!ERROR!! VAR DOESN'T EXIST
				if createVarCallback:
					from interpreter.components.var import Var

					var = Var(f"{splitLine[x]} = 0")
					createVarCallback(var)
				else:

					valid = False
					dataTypes.append(None)

					errorCallback(
						f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
						f"{blcolors.RED}  Statement {repr(splitLine[x])} [in line {repr(line)}] " +
						f"was detected as a var, but didn't exist or is invalid!{blcolors.CLEAR}"
					)
					splitLine[x] = f"{blcolors.RED}[{blcolors.BOLD}ERROR{blcolors.CLEAR}{blcolors.RED}]{blcolors.CLEAR}"

		# Check for a conditional operator
		elif splitLine[x] in conditionalOperators:
			dataTypes.append("conditional")

		# Check for an operator
		elif splitLine[x] in operatorList:
			# Nothing needs to be changed because of the way the splitByOpp function works

			# Check to make sure that if it's a string, it's using "+"
			if "str" in dataTypes and splitLine[x] != "+":
				valid = False

		# The data type doesn't exist, but we don't want to falsely detect an error
		elif "\x1b[31m[\x1b[1mERROR\x1b[0m\x1b[31m]\x1b[0m" not in splitLine[x]:
			# !!ERROR!! INVALID DATA TYPE
			errorCallback(
				f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
				f"{blcolors.RED}  INVALID DATA TYPE:  {repr(splitLine[x])}{blcolors.CLEAR}"
			)
			splitLine[x] = f"{blcolors.RED}[{blcolors.BOLD}ERROR{blcolors.CLEAR}{blcolors.RED}]{blcolors.CLEAR}"

	# Rebuild string
	# THIS IS ALSO NOT GREAT, OH WELL
	output = ""
	# print("SplitLine: ", splitLine)

	# If it's a number, keep the operators
	if valid and "numb" in dataTypes:
		output = ""
		for line in splitLine:
			output = output + line

		output = stringToMath(output, errorCallback)

	# If it's an if statement, keep the operators
	elif "conditional" in dataTypes:
		# print(f"Dec Out (trueFalse): {splitLine}")
		value = trueFalse(splitLine, getVars, errorCallback)
		if value is None:
			output = ""
			for line in splitLine:
				output = output + line
			errorCallback(
				f"{blcolors.RED}[{blcolors.BOLD}Conditional Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
				f"{blcolors.RED}  INVALID IF STATEMENT: {repr(output)}{blcolors.CLEAR}"
			)
			output = False
		else:
			valid = True  # If it gives us a value, then it's not an invalid concatenation
			output = value

	# If it's only a bool and nothing else, True False?
	elif valid and "bool" in dataTypes and len(splitLine) == 1:
		if splitLine[0] == "true":
			output = True
		else:
			output = False

	# If it's a string, don't keep the operators
	elif valid and "str" in dataTypes:
		output = ""
		for line in splitLine:
			if line not in operatorList:
				output = output + line
		# This removes ALL quotation marks,
		# if I eventually want to add support for \" then this will need to be changed
		# print(f"Dec Out: {output}")
		if returnOutputStr:
			output = output.replace('"', "")
		else:
			output = output.replace('"', "")
			output = '"' + output + '"'

	elif valid and "list" in dataTypes:
		output = splitLine
		# print(f"Output: {output}")
	else:
		# print(splitLine)
		output = ""
		for line in splitLine:
			output = output + line

	# Check to see if they are different types, if so throw an error
	if not valid:
		errorCallback(
			f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
			f"{blcolors.RED}  INVALID CONCATENATION OF DIFFERENT TYPES:  {repr(output)}{blcolors.CLEAR}"
		)

	return output, dataTypes, valid
