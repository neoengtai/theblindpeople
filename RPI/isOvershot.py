def isOvershot(currentNode, nextNode, currX, currY):
	
	diffX = nextNode['x'] - currentNode['x'] 
	diffY = nextNode['y'] - currentNode['y']
	overshotY = False
	overshotX = False
	
	if(diffY > 0):
		if(currY > nextNode['y']):
			overshotY = True
	elif(diffY < 0):
		if(currY < nextNode['y']):
			overshotY = True
	else:
		overshotY = True	

	if(diffX > 0):
		if(currX > nextNode['x']):
			overshotX = True
	elif(diffX < 0):
		if(currX < nextNode['x']):
			overshotX = True
	else:
		overshotX = True
	
	return (overshotX and overshotY)