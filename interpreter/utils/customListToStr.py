def customListToStr(_list: list) -> str:
	"""
	-- Custom List to String Converter --

	Converts for the Declaration Interpreter,
	as it needs a for loop to be converted into something
	that looks like multiple args to the Declaration Interpreter

	https://github.com/MaxMessWithTech/BasicLangV2/wiki/Utility-File-Reference#customlisttostrnot-for-use-in-custom-modules
	"""
	# string = "("
	string = ""
	for x in _list:
		if len(string) > 1:
			string = f"{string}, {x}"
		else:
			string = string + x
	# string = string + ")"

	return string
