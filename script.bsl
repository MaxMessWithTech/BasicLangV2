func:
	print("Func")
	delay(1 )
	drawLine(200, 300, 200, 100, (255, 255, 255))
	drawLine(100, 200, 300, 200, (255, 255, 255))
	drawCircle(200, 200, 100, (255, 255, 255))

	if(testVar + " Miller" == "Max Miller" && testVar != "Max" || "test" != "test"):
		print("hello Max!!!!")
		if(testVar + " Miller" == "Max Miller" && true == false):
			print("TRUE")
		else:
			print("FALSE")
	else if(true != 1):
		print("WEEE!")
	else:
		print("Hello... " + testVar)
	
run:
	print("Run")
	testVar = "Max"
	print(testVar +  " Miller")
	func()