#assuming arguement is string
import math
def intepretUART(dataSet):
	
	splitData = dataSet.split('\n')
	deviceData = 0
	power = 0
	deviceValues = []
	for data in splitData:
		deviceID = data[0]
		for i in range(len(data) - 1,0,-1):
			#not sure whether int casting will work. need try
			deviceData = deviceData + (int(data[i]) * 10**power)
			power = power + 1
		
		deviceValues.append([deviceID, deviceData])
		deviceData = 0
		power = 0
	
	return deviceValues

deviceValues = intepretUART("F123\nL12\nR9\nD1234")
print("deviceValues: ",deviceValues)	
#def obstacleAvoid(deviceValues, currHeading, northAt, instructionHeading):
	
	
