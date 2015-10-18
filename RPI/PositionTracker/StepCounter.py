import json
import collections

# Number of data points in 1 step(pace/sampling_rate)
# Use the longest time(slowest pace) taken for 1 step here
MAX_WINDOW_SIZE = 60
# Use the shortest time(fastest pace) taken for 1 step here
# For removing any attemps to find steps if the current window has lesser data points than this
MIN_WINDOW_SIZE = 25

# Too low may result in more false positives. Too high results in less counts
MIN_AMP_X = 0.05
MIN_AMP_Y = 0.1
MIN_AMP_Z = 0.15

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
		zeroRange = (minpoint + 0.35*amplitude, maxpoint - 0.35*amplitude)
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
					# print ("C3 reached")
					return True

	return False

def decideY(data, minAmplitude):
	slope = data[-1] - data[0]

	if abs(slope) >= minAmplitude:
		if slope > 0:
			return 1
		else:
			return -1

	return 0

def decideZ(data, minAmplitude):
	if (max(data) - min(data)) >= minAmplitude:
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
		ySlope = 0
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
				slope = decideY(listY, MIN_AMP_Y)

				yd = not (ySlope == slope) 
				zd = decideZ(listZ, MIN_AMP_Z)

				#print ("Y ", yd, " Z ", zd)

				# If step found, clear windows, restart from top
				# if not (ySlope == slope) or decideZ(fz, MIN_AMP_Z):
				if yd and zd:
					xWindow.clear()
					yWindow.clear()
					zWindow.clear()
					rv.append(reading[3])
					#print(reading[0]) # printing the timestamps

				ySlope = slope
		
		return rv
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
#TEST
# f = open("accel.json","r")
# js = json.load(f)

# for val in js:
# 	val.append(0)

# steps = findSteps(js)
# print (len(steps))