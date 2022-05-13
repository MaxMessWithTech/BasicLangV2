from interpreter.utils import decInterp


class Print:
	_decloration = "print("

	def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
		self.line = line
		self.fixedLine = self.removeDeclaration(self.fixLine(line))
		self.sendCommandCallback = sendCommandCallback

	# This is called during runtime
	def run(self, varAddCallback, varGetCallback, funcCallback):
		editLine, dataTypes, valid = decInterp.decInterp(self.fixedLine, varGetCallback, self.sendError)

		# This removes ALL quotation marks,
		# if I eventually want to add support for \" then this will need to be changed
		if self.sendCommandCallback:
			self.sendCommandCallback("log", editLine)
		else:
			print(editLine)

	def removeDeclaration(self, line):
		for x in range(len(line)):
			if line[::-1][x] == ")":
				break

		return line[:len(line)-x-1].replace(self._decloration, "")

	@staticmethod
	def fixLine(line):
		line = line.replace("\t", "")
		return line.replace("\n", "")

	def sendError(self, msg):
		if self.sendCommandCallback:
			self.sendCommandCallback("error", msg)
		else:
			print(msg)
