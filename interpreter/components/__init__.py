from .print import Print
from .delay import Delay

from .functionCall import FunctionCall
from .var import Var
from .For import For

from .IF import If
from .ELSEIF import ElseIf
from .ELSE import Else


objects = [
	Print,  # print()
	Delay,  # delay()
	For,
	ElseIf,  # else if()
	If,  # if()
	Else,  # else
	FunctionCall,  # ()
	Var  # =
]
