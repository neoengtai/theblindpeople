#assuming arguement is string
import math
import sys
sys.path.append('/home/pi/theblindpeople/RPI/')
import FeedbackGiver as fg

myFG = fg.FeedbackGiver()

def interpretUART(dataSet):
	
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


def obstacleAvoid(dataSet):
	deviceValues = interpretUART(dataSet)
	for device in deviceValues:
		if device[0] == 'B':
			myFG.audioFeedback("beware of steps")
	return deviceValues #for testing purposes only
#deviceValues = obstacleAvoid("F123\nL12\nR9\nB1234\nT100")
#print("deviceValues: ",deviceValues)	
#obstacleAvoid(deviceValues)
#def obstacleAvoid(deviceValues, currHeading, northAt, instructionHeading):
	
	
