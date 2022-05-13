func:
	print("Func")
	delay(1 )
	draw.drawLine(256, 356, 256, 156, (255, 255, 255))
	draw.drawLine(156, 256, 356, 256, (255, 255, 255))
	draw.drawCircle(256, 256, 100, (0, 255, 255))
	draw.drawCircle(256, 256, 100, (0, 255, 255))

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