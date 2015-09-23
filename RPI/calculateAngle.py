def calculateAngle(currentX, currentY, nodeX, nodeY, northAt)
	
	#calculate distance
	diffX = nodeX - currentX
	diffY = nodeY - currentY
	
	angleRad = atan2(diffX, diffY)
	
	angleDeg = ((angleRad/math.pi) * 180)
	
	angleDegNorthAt = ((angleDeg + 360) %360)
	
	direction = (angleDegNorthAt - northAt + 360) % 360
	
	return direction