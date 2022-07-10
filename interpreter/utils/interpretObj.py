import importlib
import os

from interpreter.components.print import Print
from interpreter.components.delay import Delay
from interpreter.components.drawLine import DrawLine
from interpreter.components.drawCircle import DrawCircle

from interpreter.components.functionCall import FunctionCall
from interpreter.components.var import Var
from interpreter.components.For import For

from interpreter.components.IF import If
from interpreter.components.ELSEIF import ElseIf
from interpreter.components.ELSE import Else
from interpreter.utils.blcolors import blcolors
importlib.import_module("comport.data.models")

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))

# This is a list, it does things, don't question it future Max
# "()" is for functions
objects = [
	Print,  # print()
	Delay,  # delay()
	DrawLine,  # draw.drawLine()
	DrawCircle,  # draw.drawCircle()
	For,
	ElseIf,  # else if()
	If,  # if()
	Else,  # else
	FunctionCall,  # ()
	Var  # =
]
typesOfObjects = [x.declaration for x in objects]


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
