import importlib
import os
from interpreter.utils.blcolors import blcolors


objects = list()  # This stores all the object references.  Ex: Print
sectionedTypesOfObjects = list()  # This stores all the types of objects, along with where they came from Ex: [{name: "draw", "objs": []}]
typesOfObjects = list()  # This stores all the object declaration vars.  Ex: "print("
errors = list()  # Stores the errors incurred while loading modules

# This opens the ./interpreter/components directory and finds all directories and files in it recursively
for (root, dirs, files) in os.walk('./interpreter/components', topdown=True):

	# If there's an __init__.py file we need to find the objects in that python package
	if "__init__.py" in files:
		# This imports the __init__.py file, and sets its reference to the module var
		module = importlib.import_module(root[2:].replace("/", ".") + ".__init__")

		try:
			# Adds the list from the __init__.py
			objects = objects + module.objects

			# root[25:] Gets rid of ./interpreter/components
			if root[25:] != "":
				tempObjList = list()

				# Loops through the objects list in the __init__.py file
				for x in module.objects:
					# Grabs the _declaration from each class
					x._declaration = f"{root[25:]}.{x._declaration}"
					tempObjList = tempObjList + [x._declaration]
					print(f"found object: {x._declaration}")

				sectionedTypesOfObjects.append({'name': root[25:], 'objs': tempObjList})
			# typesOfObjects = typesOfObjects + [f"{root[25:]}.{x._declaration}" for x in module.objects]
			else:
				# If it's the main directory, we can just do this
				typesOfObjects = typesOfObjects + [x._declaration for x in module.objects]
		except AttributeError:
			errors.append(
				f"{blcolors.RED}[{blcolors.BOLD}interpretObj() [Creates Object From String]{blcolors.CLEAR}{blcolors.RED}]" +
				f"{blcolors.RED}  INVALID MODULE __init__.py file: {repr(root[2:].replace('/', '.') + '.__init__')}{blcolors.CLEAR}"
			)


# PURPOSE - This is gonna figure out which object should be created 
#           as I'm stupid and this is annoying
def interpretObj(line, errorCallback, usePackages=list, headless=False, sendCommandCallback=None) -> any:
	"""
	--Interpret Object--
	Inputs: line(str)
	Returns: object(any)

	Creates an object based on the declaration
	https://github.com/MaxMessWithTech/BasicLangV2/wiki/Utility-File-Reference
	"""

	global typesOfObjects

	if len(usePackages) != 0:
		for _module in sectionedTypesOfObjects:
			if _module['name'] in usePackages:
				typesOfObjects = typesOfObjects + _module['objs']

	# Loop through errors from above
	for error in errors:
		errorCallback(error)

	obj = None
	for type in typesOfObjects:
		if type in line:
			try:
				obj = objects[typesOfObjects.index(type)](
					line,
					usePackages=usePackages,
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
