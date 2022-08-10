from interpreter.components.ELSE import Else
from interpreter.components.IF import If
from interpreter.components.ELSEIF import ElseIf
from interpreter.utils.blcolors import blcolors
from interpreter.utils.interpretObj import interpretObj


class Function:
	def __init__(self, name, usePackages=list, headless=False, sendCommandCallback=None):
		self.lines = list()
		self.name = name
		self.comp = list()
		self.headless = headless
		self.sendCommandCallback = sendCommandCallback
		self.usePackages = usePackages

	# PURPOSE: Convert file lines to objects
	def compile(self):
		parents = list()
		lastParent = None  # Keeps track of the last object to add to

		# Loop through all the lines and add to the right list or obj
		for line in self.lines:
			fixedLine = self.fixLine(line)
			indent = self.getIndent(line)
			self.printLn(f"Reading line: {fixedLine}, with an indent: {indent}.")

			if indent > 1:
				# SEND TO OBJECT
				try:
					lastParent.addLine(line)
					if lastParent not in parents:
						parents.append(lastParent)
				except AttributeError:
					self.sendError(
						f"{blcolors.RED}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
						f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.RED}]" +
						f"{blcolors.RED}  INVALID INDENTION AT LINE {fixedLine}, WITH INDENT OF {indent}{blcolors.CLEAR}"
					)
			else:
				obj = interpretObj(
					fixedLine,
					self.sendError,
					usePackages=self.usePackages,
					headless=self.headless, 
					sendCommandCallback=self.sendCommandCallback)
				
				if obj:
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
								f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.RED}]" +
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
								f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.RED}]" +
								f"{blcolors.RED}  INVALID ELSE DEFINITION: \"{fixedLine}\", " + 
								f"there isn't an if or else if statement to inherit from{blcolors.CLEAR}"
							)
					else:
						self.comp.append(obj)
						lastParent = obj

		# Loop Through all the parents that were created
		for parent in parents:
			parent.compile()

	# PURPOSE: Run Functions
	def run(self, varAddCallback, varGetCallback, funcCallback):
		for obj in self.comp:
			obj.run(varAddCallback, varGetCallback, funcCallback)

	@staticmethod
	def getIndent(line):
		return line.count("\t")

	@staticmethod
	def fixLine(line):
		line = line.replace("\t", "")
		return line.replace("\n", "")

	def addLine(self, line):
		self.lines.append(line)

	def printLn(self, text):
		if not self.headless:
			if self.sendCommandCallback:
				self.sendCommandCallback("debug", 
					f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
					f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.BLUE}]" +
					f"{blcolors.BLUE}  {text}{blcolors.CLEAR}")
			else:
				print(
					f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
					f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.BLUE}]" +
					f"{blcolors.BLUE}  {text}{blcolors.CLEAR}")

	def sendError(self, msg):
		if self.sendCommandCallback:
			self.sendCommandCallback("error", msg)
		else:
			print(msg)
