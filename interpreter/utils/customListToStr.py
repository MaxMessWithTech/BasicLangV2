def customListToStr(_list: list) -> str:
	"""
	-- Custom List to String Converter --

	Converts for the Decloration Interpreter,
	as it needs a for loop to be converted into something
	that looks like multiple args to the Decloration Interpreter
	"""
	string = "("
	for x in _list:
		if len(string) > 1:
			string = f"{string}, {x}"
		else:
			string = string + x
	string = string + ")"

	return string
