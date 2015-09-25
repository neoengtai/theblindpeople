#Version 1 of step detection
#Every oscillation check whether it is a step
#One oscillation happens when the value crosses zero three times(change from +ve to -ve and vice versa)
#Each oscillation there is a max and min value. If the difference pass threshold considered a step

CONST_STEP_THRESHOLD = 0.3 #adjust this to detect steps
CONST_ZERO_LINE = 1 #adjust this to pick zero line
def calculateAbsoluteMagnitude(x ,y ,z):
	#calculate the magnitude from three axis
	
	magnitude = math.sqrt(math.pow(x,2) + math.pow(y,2) + math.pow(z,2))
	
	return magnitude
	

def stepDecider(max, min):
		
		difference = max - min
		
		if (difference > CONST_STEP_THRESHOLD):
			return 1
		else:
			return 0
			
def countSteps(accelData):
	
	positiveValue = -1
	prevMagnitude = 0
	crossedZero = 0
	max = 0
	min = 0
	numTimesCrossedZero = 0
	numSteps = 0
	#accelData should be a list. In the list each index should contain x,y,z
	for data in accelData:
		#magnitude = calculateAbsoluteMagnitude(data[0],data[1],data[2])
		magntiude = data
		print("Value is:",magnitude)
		if (magnitude > CONST_ZERO_LINE):
			positiveValue = 1
		else:
			positiveValue = 0

		if ((magnitude < CONST_ZERO_LINE) & (prevMagnitude > CONST_ZERO_LINE)): #crossed zero
			print("CROSS")
			crossedZero = 1
			numTimesCrossedZero = numTimesCrossedZero + 1
		elif ((magnitude > CONST_ZERO_LINE) & (prevMagnitude < CONST_ZERO_LINE)):
			print("CROSS")
			crossedZero = 1
			numTimesCrossedZero = numTimesCrossedZero + 1
		else:
			crossedZero = 0
		
		prevMagnitude = magnitude
		
		if (numTimesCrossedZero == 3): #one oscillation
			print("I AM HERE")
			if (stepDecider(max, min)):
				numSteps = numSteps + 1
			numTimesCrossedZero = 0
			max = 0
			min = 0

		if (crossedZero == 0):
			if ((positiveValue == 1) & (magnitude > max)):
				max = magnitude
			elif ((positiveValue == 0) & (magnitude < min)):
				min = magnitude
	
	print("Steps count:",numSteps)

import math
#Testing

testData = [(10,10,10),(20,20,20),(50,50,50),(-50,-50,-50),(10,10,10),(50,50,50)]				
countSteps(testData)
		
					
	
		