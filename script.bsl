func:
	print("Func")
	# delay(1)
	draw.drawLine(256, 356, 256, 156, (0, 255, 0))
	draw.drawLine(156, 256, 356, 256, (0, 0, 255))
	draw.drawCircle(256, 256, 100, (255, 0, 0))


	test = 0
	testList = [1, 2, 3, 4, 5]

	for(x in [0, 1, 2, 3, 4, 5]):
		draw.drawLine(256 - x * 10, 356 - x * 10, 256 - x * 10, 156 - x * 10, (x * 50, 0, 0))
		draw.drawLine(156 - x * 10, 256 - x * 10, 356 - x * 10, 256 - x * 10, (x * 50, 0, 0))
		draw.drawCircle(256 - x * 10, 256 - x * 10, 100, (x * 50, 0, 0))

	if(testVar + " Miller" == "Max Miller" && testVar == "Max" || "test" == "test"):
		print("hello Max!!!!")
		# if(testVar + " Miller" == "Max Miller" && true == true):
			# print("TRUE")
		# else:
			# print("FALSE")
	# else if(true != 1):
		# print("WEEE!")
	# else:
		# print("Hello... " + testVar)
	
run:
	# print("Run")
	testVar = "Max"
	# print(testVar +  " Miller")
	# testVar = "Will"
	# print(testVar +  " Miller")
	func()