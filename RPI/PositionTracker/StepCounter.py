import json
from PositionTracker import lowPassFilter as lpf
import collections
import math

# Number of data points in 1 step(pace/sampling_rate)
# Use the longest time(slowest pace) taken for 1 step here
MAX_WINDOW_SIZE = 90
# Use the shortest time(fastest pace) taken for 1 step here
# For removing any attemps to find steps if the current window has lesser data points than this
MIN_WINDOW_SIZE = 55

# Too low may result in more false positives. Too high results in less counts
MIN_AMP_X = 0.15 # peak to peak
MIN_AMP_Y = 0.10 # min amplitude for moving around on the spot
MIN_AMP_Z = 0.25

# Filter Params
FILTER_ORDER = 3
FILTER_FS = 50.0       # sample rate, Hz
FILTER_CUTOFF = 3.667  # desired cutoff frequency of the filter, Hz

xWindow = collections.deque(maxlen = MAX_WINDOW_SIZE)
yWindow = collections.deque(maxlen = MAX_WINDOW_SIZE)
zWindow = collections.deque(maxlen = MAX_WINDOW_SIZE)

def decideX(data, minAmplitude):
	maxpoint = max(data)
	minpoint = min(data)
	amplitude = maxpoint - minpoint

	# Step is valid if this pattern is observed:
	# center -> down -> min/max point -> center -> max/min point -> center
	if amplitude >= minAmplitude:
		zeroRange = (minpoint + 0.25*amplitude, maxpoint - 0.25*amplitude)
		# print ("Amp ", amplitude)
		# Conditions to be met
		bools = {	"center1":False,
					"center2":False,
					"center3":False,
					"max":False,
					"min":False}

		for x in data:
			if bools["center1"] == False:
				if x >= zeroRange[0] and x <= zeroRange[1]:
					# print ("C1 reached")
					bools["center1"] = True

			elif bools["max"] == False and bools["min"] == False:
				if x == maxpoint:
					bools["max"] = True
					# print ("Max1 reached")
				if x == minpoint:
					bools["min"] = True
					# print ("Min1 reached")

			elif bools["center2"] == False:
				if x >= zeroRange[0] and x <= zeroRange[1]:
					bools["center2"] = True
					# print ("C2 reached")

			elif bools["max"] ^ bools["min"]: #XOR here
				if x == maxpoint:
					bools["max"] = True
					# print ("Max2 reached")
				if x == minpoint:
					bools["min"] = True
					# print ("Min2 reached")

			elif bools["center3"] == False:
				if x >= zeroRange[0] and x <= zeroRange[1]:
					bools["center3"] = True
					print ("-------------X ", amplitude)
					return True

	return False

def decideY(data, minAmplitude):
	#return decideX(data, minAmplitude)
	return 0

def decideZ(data, minAmplitude):
	if (max(data) - min(data)) >= minAmplitude:
		print ("--------------Z ", (max(data)-min(data)))
		return True;
	return False;

# data in the format of [(timestamps,x,y,z,heading),(...),...]
def findSteps(data):
	# Total data points is lesser than fastest pace, hence no steps will be found
	# Just append the data and return
	if (len(data) + len(xWindow)) < MIN_WINDOW_SIZE:
		timestamps,x,y,z,headings = zip(*data)
		xWindow.extend(x)
		yWindow.extend(y)
		zWindow.extend(z)
		return None
	# Potential steps exists in the data
	else:
		rv = []
		for reading in data:
			# Append until min window reached
			xWindow.append(reading[1])
			yWindow.append(reading[2])
			zWindow.append(reading[3])
			if len(xWindow) < MIN_WINDOW_SIZE:
				continue

			# Convert to x,y,z list
			listX, listY, listZ = list(xWindow), list(yWindow), list(zWindow)

			# Identify steps
			# X given high priority, since y,z can be true if user moves on the spot
			if decideX(listX, MIN_AMP_X):
				yd = decideY(listY, MIN_AMP_Y) 
				zd = decideZ(listZ, MIN_AMP_Z)

				#print ("Y ", yd, " Z ", zd)

				# If step found, clear windows, restart from top
				# if not (ySlope == slope) or decideZ(fz, MIN_AMP_Z):
				if yd or zd:
					xWindow.clear()
					yWindow.clear()
					zWindow.clear()
					rv.append(reading[4])
					#print(reading[4]) # printing the timestamps

		
		return rv
def calculateStepDistance(averagePacing, headingMoved, northAt):

	#averagePacing is distance per step
	xTravel = 0
	yTravel = 0
	
	for heading in headingMoved:
		if heading < 0:
			heading = heading+2*math.pi
		headingInMap = (math.radians(northAt)+heading)%(2*math.pi)
		distX = math.sin(headingInMap) * averagePacing
		distY = math.cos(headingInMap) * averagePacing
		xTravel = xTravel + distX
		yTravel = yTravel + distY
	
	#print("xTravel", xTravel)
	#print("yTravel", yTravel)
	
	return xTravel, yTravel
#TEST
#f = open("accel.json","r")
#js = json.load(f)

#for val in js:
#	val.append(0)

#steps = findSteps(js)
#print (len(steps))
