from interpreter.utils.decInterp import decInterp
from interpreter.utils.blcolors import blcolors

class Else:
	def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
		self.line = line
		# New Handeling method
		self.parent = None
		self.true = False  # Default to False

		self.fixedLine = ""
		self.lines = list()
		self.comp = list()
		self.headless = headless
		self.sendCommandCallback = sendCommandCallback

	def compile(self):
		from interpreter.utils.interpretObj import interpretObj

		parents = list()
		lastParent = None  # Keeps track of the last object to add to
		firstIndent = -1

		# Loop through all the lines and add to the right list or obj
		for line in self.lines:
			fixedLine = line.replace("\t", "").replace("\n", "")
			indent = self.getIndent(line)

			self.printLn(f"Reading line: {fixedLine}, with an indent: {indent}.")

			# If it's the first line we're reading, assume that this is the indent of the children
			if firstIndent == -1:
				firstIndent = indent

			if indent > firstIndent:
				# SEND TO OBJECT
				try:
					lastParent.addLine(line)
					if lastParent not in parents:
						parents.append(lastParent)
				except AttributeError:
					self.sendError(
						f"{blcolors.RED}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
						f"ELSE ({self.fixedLine}){blcolors.CLEAR}{blcolors.RED}]" +
						f"{blcolors.RED}  INVALID INDENTION AT LINE {fixedLine}, WITH INDENT OF {indent}{blcolors.CLEAR}"
					)
			else:
				obj = interpretObj(
					fixedLine, self.sendError, headless=self.headless, 
					sendCommandCallback=self.sendCommandCallback
				)
				if obj:
					from interpreter.components.IF import If
					from interpreter.components.ELSEIF import ElseIf

					if type(obj) == ElseIf:
						if type(lastParent) == If:
							obj.setParent(lastParent)
							obj.hasBeenConnectedToIf = True
							self.comp.append(obj)
							lastParent = obj
						elif type(lastParent) == ElseIf and lastParent.hasBeenConnectedToIf:
							obj.setParent(lastParent)
							self.comp.append(obj)
							lastParent = obj
						else:
							self.sendError(
								f"{blcolors.RED}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
								f"ELSE ({self.fixedLine}){blcolors.CLEAR}{blcolors.RED}]" +
								f"{blcolors.RED}  INVALID ElseIf DEFINITION: \"{fixedLine}\", " + 
								f"there isn't an if or else if statement to inherit from{blcolors.CLEAR}"
							)
			
					# CASE FOR ELSE - Need to inherit value of the previous statement
					elif type(obj) == Else:
						if type(lastParent) == If or type(lastParent) == ElseIf:
							obj.setParent(lastParent)
							self.comp.append(obj)
							lastParent = obj
						else:
							self.sendError(
								f"{blcolors.RED}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
								f"ELSE ({self.fixedLine}){blcolors.CLEAR}{blcolors.RED}]" +
								f"{blcolors.RED}  INVALID ELSE DEFINITION: \"{fixedLine}\", " + 
								f"there isn't an if or else if statement to inherit from{blcolors.CLEAR}"
							)
					else:
						self.comp.append(obj)
						lastParent = obj

		# Loop Through all the parents that were created
		for parent in parents:
			parent.compile()

	# This is called during runtime
	def run(self, varAddCallback, varGetCallback, funcCallback):
		# CHECK IF TRUE
		# editLine should return either "True" or "False"
		if self.parent:
			# print(f"[Else] parent: {self.parent.isTrue()}")
			if not self.parent.isTrue():
				self.true = True
				for obj in self.comp:
					obj.run(varAddCallback, varGetCallback, funcCallback)
			else:
				self.true = True
		else:
			# Should never happen, although there could be an error here
			pass

	def setParent(self, parent):
		self.parent = parent
	
	def isTrue(self):
		return self.true

	def addLine(self, line):
		self.lines.append(line)

	@staticmethod
	def getIndent(line):
		return line.count("\t")

	def removeDeclaration(self, line):
		for x in range(len(line)):
			if line[::-1][x] == ")":
				break

		return line[:len(line)-x-1].replace(self.declaration, "")

	@staticmethod
	def fixLine(line):
		line = line.replace("\t", "")
		return line.replace("\n", "")

	def printLn(self, text):
		if not self.headless:
			if self.sendCommandCallback:
				self.sendCommandCallback("debug", 
					f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
					f"ELSE STATEMENT ({self.fixedLine}){blcolors.CLEAR}{blcolors.BLUE}]" +
					f"{blcolors.BLUE}  {text}{blcolors.CLEAR}")
			else:
				print(
					f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
					f"ELSE STATEMENT ({self.fixedLine}){blcolors.CLEAR}{blcolors.BLUE}]" +
					f"{blcolors.BLUE}  {text}{blcolors.CLEAR}"
				)

	def sendError(self, msg):
		if self.sendCommandCallback:
			self.sendCommandCallback("error", msg)
		else:
			print(msg)

	@property
	def declaration(self):
		return "else"
