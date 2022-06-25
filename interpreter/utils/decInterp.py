from typing import Tuple

from interpreter.utils.blcolors import blcolors
from interpreter.utils.splitByArg import splitByArg
from interpreter.utils.partInterp import partInterp
from interpreter.utils.splitByCustom import splitByCustom
from interpreter.utils.customListToStr import customListToStr


def decInterp(
		line, getVars, errorCallback, returnOutputStr=True, createVarCallback=None, parent=True, splitByFirst=None
) -> Tuple[list, list, bool]:
	"""
	--Declaration Interpreter--
	Inputs: parts(list) - Current Value, getVars(def) - call back
	Returns: Formatted Line(str), Data Type(list), valid(bool)

	Finding Var references and replaces them with their value in the line
	"""

	"""
	1) "draw.drawLine(156, 256, 356, 256, (255, 255, 255))" ->
	2) "(156, 256, 356, 256, (255, 255, 255))" -> 
	3) decInterp() ->
	4) ["156", "256", "356", "256", "(255, 255, 255)"]
	5) for each -> decInterp() recall, check if ( or [
	"""

	# print(f"PRE PRE LINE: {line}")
	# This splits by a custom list of chars first, specifically in the case of for statement
	if type(splitByFirst) == list:
		line = customListToStr(splitByCustom(line, splitByFirst))
	# print(f"PRE LINE: {line}")

	split = splitByArg(line, errorCallback)  # "1" -> ["1"]  |  ['1', '2']
	# print(f"Split: {split}")

	if len(split) > 1:
		valid = True
		types = list()
		for x in range(len(split)):
			_out, _types, _valid = decInterp(
				split[x], getVars, errorCallback,
				returnOutputStr=returnOutputStr, createVarCallback=createVarCallback, parent=False
			)
			split[x] = _out[0]
			types.append(_types)

			if not _valid:
				valid = False
		# print(f"Line: {line}")
		if line.replace(" ", "")[0] == "[":
			split = [split]

		# print(f"Finalized Split: {split}, valid: {valid}")
		if not parent:
			return [split], types, valid

		# Case for lists, so they stay when they get to the object
		return split, types, valid

	else:
		part = split[0]  # ["1"] -> "1"
		# print(f"Found part: {part}")

		_out, _types, _valid = partInterp(
			part, getVars, errorCallback,
			returnOutputStr=returnOutputStr, createVarCallback=createVarCallback
		)  # "1" -> 1

		part = _out

		# 1 -> [1]
		return [part], _types, _valid
