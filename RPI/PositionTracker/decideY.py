def decideY(dataSet):
	
	limit = len(dataSet)
	
	if(dataSet[0] < dataSet[limit]):
		return 1 #increasing
	elif(dataSet[0] > dataSet[limit]):
		return -1 #decreasing
	else:
		return 0