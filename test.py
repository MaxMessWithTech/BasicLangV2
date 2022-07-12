from interpreter.utils import decInterp


class NameOfPackage:
	_declaration = "nameOfPackage("

	def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
		self.line = line
		self.fixedLine = self.fixLine(line)
		self.sendCommandCallback = sendCommandCallback

	# This is called during runtime
	def run(self, varAddCallback, varGetCallback, funcCallback):
		editLine, dataTypes, valid = decInterp.decInterp(self.fixedLine, varGetCallback, self.sendError)

		self.sendCommandCallback("log", editLine[0])

	def fixLine(self, line):
		line = line.replace("\t", "").replace("\n", "")
		for x in range(len(line)):
			if line[::-1][x] == ")":
				break

		return line[:len(line)-x-1].replace(self._declaration, "")

	def sendError(self, msg):
		if self.sendCommandCallback:
			self.sendCommandCallback("error", msg)
		else:
			print(msg)
