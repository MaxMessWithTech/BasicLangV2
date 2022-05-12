func:
	print("Func")
	delay(1 )
	draw(0, 0, 100, -2, (255, 255, 255))

	if(testVar + " Miller" == "Max Miller" && testVar != "Max" || "test" != "test"):
		print("hello Max!!!!")
		if(testVar + " Miller" == "Max Miller" && true == false):
			print("TRUE")
		else:
			print("FALSE")
	else if(true == false):
		print("WEEE!")
	else:
		print("Hello... " + testVar)
	
run:
	print("Run")
	testVar = "Max"
	print(testVar +  " Miller")
	func()