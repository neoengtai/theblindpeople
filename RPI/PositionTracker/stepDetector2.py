import adaptiveJerkPaceBuffer as ajpb
import lowPassFilter as lpf
import math
import numpy as np

def stepDetection(dataSet):
	xs = []
	ys = []
	zs = []
	timestamps = []
	headings = []
	for data in dataSet:
		xs.append(data[1])
		ys.append(data[2])
		zs.append(data[3])
		timestamps.append(data[0])
		headings.append(data[4])

	x,y,z,timestamps,headings = np.array(xs), np.array(ys),np.array(zs), np.array(timestamps), np.array(headings)
		
	# Filter Params
	order = 3
	fs = 50.0       # sample rate, Hz
	cutoff = 3.667  # desired cutoff frequency of the filter, Hz
		
	lowPassX = lpf.butter_lowpass_filter(x,cutoff,fs,order)
	peaks,troughs,average, headingMovedX = ajpb.adaptive_jerk_pace_buffer(lowPassX, timestamps, headings)
	
	lowPassY = lpf.butter_lowpass_filter(y,cutoff,fs,order)
	peaks,troughs,average, headingMovedY = ajpb.adaptive_jerk_pace_buffer(lowPassY, timestamps, headings)
	
	lowPassZ = lpf.butter_lowpass_filter(z,cutoff,fs,order)
	peaks,troughs,average, headingMovedZ = ajpb.adaptive_jerk_pace_buffer(lowPassZ, timestamps, headings)
	
	print("X: ",headingMovedX)
	print("Y: ",headingMovedY)
	print("Z: ",headingMovedZ)
	
	return headingMovedY
		
def calculateStepDistance(averagePacing, headingMoved, northAt):

	#averagePacing is distance per step
	xTravel = 0
	yTravel = 0
	
	for heading in headingMoved:
		if heading < 0:
			heading = heading + 360
		headingInMap =((northAt + heading) % 360)
		distX = math.sin(math.radians(headingInMap)) * averagePacing
		distY = math.cos(math.radians(headingInMap)) * averagePacing
		xTravel = xTravel + distX
		yTravel = yTravel + distY
	
	#print("xTravel", xTravel)
	#print("yTravel", yTravel)
	
	return xTravel, yTravel