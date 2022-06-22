from interpreter.utils.blcolors import blcolors

def splitByArg(line: str, errorCallback) -> list:
	"""
	--Split By Argument--
	Inputs: line(str)
	Returns: split(list)

	"(156, 256, 356, 256, (255, 255, 255))" ->
	["156", "256", "356", "256", "(255, 255, 255)"]
	"""

	# In recursive calls, there can be spaces at the beginning
	# This removes them
	line = findFirstRealChar(line)

	# In recursive calls, it will have parenthesis or brackets at the start and end
	# This removes them
	if line[0] == "(" or line[0] == "[":
		line = line[1: len(line) - 1]

	ranges = findBrackets(line, errorCallback)
	if ranges is None:
		return ["\x1b[31m[\x1b[1mERROR\x1b[0m\x1b[31m]\x1b[0m"]
	nestedIndices = generateAllNumbsInRange(ranges)
	# print(findBrackets(line))

	out = list()
	lastIndex = -1
	for x in range(len(line)):
		if line[x] == "," and x not in nestedIndices:
			out.append(line[lastIndex + 1: x])
			# out.append(line[x])
			lastIndex = x
	out.append(line[lastIndex + 1: len(line)])

	return out


def findBrackets(line: str, errorCallback):
	lists = list()
	openingBrackets = list()  # To keep track of used indices

	for x in range(len(line)):
		if line[x] == "]":
			for y in range(x)[::-1]:
				if line[y] == "[" and y not in openingBrackets:
					openingBrackets.append(y)
					lists.append({'start': y, 'end': x})
					break
		elif line[x] == ")":
			for y in range(x)[::-1]:
				if line[y] == "(" and y not in openingBrackets:
					openingBrackets.append(y)
					lists.append({'start': y, 'end': x})
					break

	if len(lists) != line.count("(") + line.count("[") or len(lists) != line.count(")") + line.count("]"):
		errorCallback(
			f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter | Split By Argument{blcolors.CLEAR}{blcolors.RED}]" +
			f"{blcolors.RED}  Statement {repr(line)} is missing closing or opening parenthesis!{blcolors.CLEAR}"
		)
		return None

	return lists


def generateAllNumbsInRange(ranges: list) -> list:
	out = list()
	for part in ranges:
		for x in range(part['start'], part['end'] + 1):
			out.append(x)
	return out


def findFirstRealChar(line: str) -> str:
	for x in range(len(line)):
		if line[x] != " ":
			return line[x:]
