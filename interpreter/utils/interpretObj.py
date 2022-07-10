import importlib
import os
from interpreter.utils.blcolors import blcolors

objects = list()
typesOfObjects = list()

for (root, dirs, files) in os.walk('./interpreter/components', topdown=True):
	if "__init__.py" in files:
		module = importlib.import_module(root[2:].replace("/", ".") + ".__init__")

		# Adds the list from the __init__.py
		objects = objects + module.objects
		# root[25:] Gets rid of ./interpreter/components
		if root[25:] != "":
			for x in module.objects:
				x._declaration = f"{root[25:]}.{x._declaration}"
				typesOfObjects = typesOfObjects + [x._declaration]
			# typesOfObjects = typesOfObjects + [f"{root[25:]}.{x._declaration}" for x in module.objects]
		else:
			typesOfObjects = typesOfObjects + [x._declaration for x in module.objects]

# print(objects)
# print(typesOfObjects)


# PURPOSE - This is gonna figure out which object should be created 
#           as I'm stupid and this is annoying
def interpretObj(line, errorCallback, headless=False, sendCommandCallback=None) -> any:
	"""
	--Interpret Object--
	Inputs: line(str)
	Returns: object(any)

	Creates an object based on the declaration
	"""

	obj = None
	for type in typesOfObjects:
		if type in line:
			try:
				obj = objects[typesOfObjects.index(type)](
					line,
					headless=headless,
					sendCommandCallback=sendCommandCallback
				)
				break
			except TypeError:
				errorCallback(
					f"{blcolors.RED}{blcolors.BOLD}ERROR at interpretObj() [Creates Object From String]" +
					f"{blcolors.CLEAR}{blcolors.RED} -> Object call of \"{line}\" isn't IMPLEMENTED!" +
					blcolors.CLEAR)
				break

	if obj is None:
		errorCallback(
			f"{blcolors.RED}{blcolors.BOLD}ERROR at interpretObj() [Creates Object From String]" +
			f"{blcolors.CLEAR}{blcolors.RED} -> Object call of \"{line}\" is invalid and doesn't exist" +
			blcolors.CLEAR)
	return obj
