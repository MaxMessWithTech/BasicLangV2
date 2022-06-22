def splitByCustom(line: str, splitBy: list) -> list:
	allIndices = list()
	for opp in splitBy:
		res = [i for i in range(len(line)) if line.startswith(opp, i)]
		for index in res:
			try:
				# Case for negative numbers
				if (opp == "-" and not line[index + 1].isnumeric()) or opp != "-":
					allIndices.append({'index': index, 'opp': opp})
			except IndexError:
				allIndices.append({'index': index, 'opp': opp})

	out = list()
	lastIndex = -1
	for indexDict in sorted(allIndices, key=lambda d: d['index']):
		# Makes sure that when there are tuples we don't have weird gaps
		if indexDict['opp'] != "(" and indexDict['opp'] != "[":
			out.append(line[lastIndex + 1:indexDict['index']])

		out.append(line[indexDict['index']:indexDict['index'] + len(indexDict['opp'])])
		lastIndex = indexDict['index'] + len(indexDict['opp']) - 1
	# REPLACE HERE GETS RID OF ":"

	if len(out) == 0:
		out.append(line[lastIndex + 1:].replace(":", ""))
	elif out[len(out) - 1] != ")" and out[len(out) - 1] != "]":
		out.append(line[lastIndex + 1:].replace(":", ""))

	return out
