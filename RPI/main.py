
# sys.path.append('.')

import os.path
import sys
import RTIMU
import MapManager as MM
import RouteFinder as RF
import FeedbackGiver as FG
import Keypad as KP
from PositionTracker import PositionTracker as PT
import queue
import threading
import time
import math
import urllib.request
from socket import timeout

SETTINGS_FILE = "Configuration/RTIMULib"
CALIBRATION_FILE = "Configuration/profile.ini"
IMU_SAMPLING_PERIOD = 0.02 	# In seconds

def getSrcDestNodes():
	places = {"Source": None, "Destination": None}

	for k,v in places.items():
		if k == "Source":
			clip = "enter starting building"
		elif k == "Destination":
			clip = "enter ending building"

		while v is None:
			feedbackGiver.audioFeedback(clip)
			print(k + " building: ")
			# buildingID = keypad.getUserInput() #TODO: change to actual keypad getKey
			building = input() #TODO: change to actual keypad getKey
			
			feedbackGiver.audioFeedback("enter level")
			print (k + " level: ")
			# level = keypad.getUserInput() #TODO: change to actual keypad getKey
			level = input() #TODO: change to actual keypad getKey
				
			if mapManager.get_map(building, level) is None:
				feedbackGiver.audioFeedback("error")
				print ("Cannot find map!")
				continue
			
			feedbackGiver.audioFeedback("enter node")
			print(k + " nodeID: ")
			# nodeId = keypad.getUserInput() #TODO: change to actual keypad getKey
			nodeId = input() #TODO: change to actual keypad getKey

			if mapManager.get_node(building,level,nodeId) is None:
				feedbackGiver.audioFeedback("error")
				print ("Invalid node!")
				continue
			else:
				v = (building, level, nodeId)
				places.update({k : v})

	return places["Source"], places["Destination"]

def loadUserProfile():
	if not os.path.exists(CALIBRATION_FILE):
		pace = 35.0
		print("No profile found. Using default pace of 35 cm/step")
	else:
		#Note: no checking of whether or not first line is PACE_AVG
		f = open(CALIBRATION_FILE)
		val = f.readline().split('=')
		pace = float(val[1])
	return pace

def computeHeight(pressure):
	#  computeHeight() - the conversion uses the formula:
	#
	#  h = (T0 / L0) * ((p / P0)**(-(R* * L0) / (g0 * M)) - 1)
	#
	#  where:
	#  h  = height above sea level
	#  T0 = standard temperature at sea level = 288.15
	#  L0 = standard temperatur elapse rate = -0.0065
	#  p  = measured pressure
	#  P0 = static pressure = 1013.25
	#  g0 = gravitational acceleration = 9.80665
	#  M  = mloecular mass of earth's air = 0.0289644
	#  R* = universal gas constant = 8.31432
	#
	#  Given the constants, this works out to:
	#
	#  h = 44330.8 * (1 - (p / P0)**0.190263)
	return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));

def THREAD_IMU():
	while True:
		buf = []
		s_time = time.time()
		
		while True:
			if time.time() - s_time >= 5:
				# pt = time.time()
				imu_Q.put(buf)
				# print ("Put time: ", (time.time() - pt))
				# print ("IMURate: ", len(buf)/(pt - s_time))
				break

			if imu.IMURead():
				data = imu.getIMUData()
				# Z axis facing front, X axis facing left
				heading = math.atan2(data['compass'][0],-data['compass'][2])
				acc = imu.getAccelResiduals()
				buf.append((data['timestamp'],)+acc+(heading,))

			time.sleep(0.5*IMU_SAMPLING_PERIOD)

def THREAD_AUDIO(*args):
	global audioLock

	if audioLock.acquire(blocking=True, timeout=5):
		feedbackGiver.audioFeedback(args[0])
		audioLock.release()

#Returns direction in degree
def resolveRealAngle(currentX, currentY, nodeX, nodeY, northAt):

	#calculate distance
	diffX = nodeX - currentX
	diffY = nodeY - currentY
		
	angleRad = math.atan2(diffX, diffY)
	angleDeg = math.degrees(angleRad)
		
	angleDegPositive = ((angleDeg + 360) %360)
		
	angleResult = (angleDegPositive - northAt + 360) % 360
		
	return angleResult
	
def getDirections (node, northAt, currX, currY, heading): 
	separation = math.hypot((node['x']- currX),(node['y'] - currY))

	# print ("To node: ", tempNode["nodeId"])
	angle = resolveRealAngle(currX, currY, node['x'], node['y'], northAt)

	difference = angle - ((math.degrees(heading) + 360) %360)

	if difference > 180:
		difference -= 360 #left
	elif difference < -180:
		difference += 360 #right		
		
	return separation, difference
	#Return the distance to node and the angle to change
		
	#audioDir = self.dataToString(0,int(difference))
	#audioDist = self.dataToString(1,int(separation/pace)) + " steps"
	#self.audioFeedback(audioDir+' '+audioDist)
		
# Convert data to string format for audio feedback
# function 0 : direction
#def dataToString(function, data):
def feedbackResolver(function, data):
	result = [] 
	if function == 0:
		if data in range(-20,20):
			return "continue straight"
		elif data in range(20,65):
			return "turn slight right"
		elif data in range(65,110):
			return "turn right"
		elif data in range(110,181):
			return "U turn"
		elif data in range(-65,-20):
			return "turn slight left"
		elif data in range(-110,-65):
			return "turn left"
		elif data in range(-180, -110):
			return "U turn"
	elif function == 1:
		return ' '.join(list(str(data)))

def generateFeedback(dist, angle, pace):
	angleString = feedbackResolver(0, int(angle))
	angleDist = feedbackResolver(1,int(dist/pace)) + " steps"
	
	feedbackString = angleString+' '+angleDist
	
	return feedbackString

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

def testConnection():
	connectionFlag = False
	try:
		urllib.request.urlopen("http://www.google.com", timeout = 3)
		connectFlag = True
		print ("Got connection!")
	except urllib.error.URLError as e:
		print ("No Connection")
	except timeout:
		print("timeout!")
	
	return connectionFlag

#START OF PROGRAM
# ---------------------------------Variables-----------------------------------
imu = None
feedbackGiver = None
mapManager = None
keypad = None
positionTracker = None
pace = None
source, destination = None, None
imu_Q = None
currentHeading = None
audioLock = threading.Lock()
continueWalking = False

# -------------------------------Init Section----------------------------------
pace = loadUserProfile()
imu_Q = queue.Queue()
keypad = KP.Keypad()
#init Arduino
feedbackGiver = FG.FeedbackGiver()
wifi = testConnection()
positionTracker = PT.PositionTracker(0,0,pace)
if wifi:
	mapManager = MM.MapManager("Online")
else:
	mapManager = MM.MapManager("Offline")

# IMU init sequence. Can't seem to put it in a function :(
if not os.path.exists(SETTINGS_FILE + ".ini"):
	print("Settings file not found!")
	sys.exit(1)

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

if (not imu.IMUInit()):
	print("IMU Init Failed")
	sys.exit(1)

# Set params for the imu (r,p,y) values calculation
imu.setSlerpPower(0.02)
imu.setGyroEnable(False)
imu.setAccelEnable(False)
imu.setCompassEnable(False)

if (not pressure.pressureInit()):
	print("Pressure sensor Init Failed")
	sys.exit(1)

# ----------------------------Start of navigation------------------------------
source, destination = getSrcDestNodes()

# TODO: Change to audio
print (source,destination)

routes = RF.findRoute(mapManager, source[2], source[0], source[1], 
					destination[2], destination[0], destination[1])
print (routes)

# Initialize the first heading
while True:
	if imu.IMURead():
		compass = imu.getCompass()
		# Z axis facing front, X axis facing left
		currentHeading = math.atan2(compass[0],-compass[2])
		break

t_imu = threading.Thread(target=THREAD_IMU)
# t_uart = threading.Thread(target=THREAD_UART)

t_imu.start()
# t_uart.start()

# Multiple paths will exist if navigating across buildings/levels
for route in routes:
	building = route['building']
	level = route['level']
	northAt = int(mapManager.get_map(building,level)['info']['northAt'])
	path = route['path']

	for i in range(0,len(path)-1):
		currentNode = mapManager.get_node(building,level,path[i])
		nextNode = mapManager.get_node(building,level,path[i+1])
		positionTracker.setCurrentPosition(currentNode['x'],currentNode['y'])
		dist, angle = getDirections(nextNode, northAt, currentNode['x'], currentNode['y'], currentHeading)
		feedbackString = generateFeedback(dist, angle, pace)
		thread_audio = threading.Thread(target=THREAD_AUDIO,args=[feedbackString])
		thread_audio.start()

		while True:
			# This call blocks until the IMU thread puts data into the queue
			imuData = imu_Q.get()
			positionTracker.updatePosition(imuData,northAt)
			imu_Q.task_done()

			currentPos = positionTracker.getCurrentPosition()
			currentHeading = imuData[-1][4]
			print ("X: %f Y: %f" % (currentPos[0],currentPos[1]))
			print ("Current heading: ", currentHeading)

			dist, angle = getDirections(nextNode, northAt, currentPos[0], currentPos[1], currentHeading)
			if(isOvershot(currentNode, nextNode, currentPos[0], currentPos[1])):
				try:
					followingNode = mapManager.get_node(building,level,path[i+2]) #NOTE IF i+2 out of bounds then last ode liao. must cater
					currentAngle = resolveRealAngle(currentNode['x'],currentNode['y'],nextNode['x'],nextNode['y'],northAt)
					nextAngle = resolveRealAngle(nextNode['x'], nextNode['y'], followingNode['x'], followingNode['y'],northAt)
					continueWalking = ((nextAngle <= (currentAngle+15)) or (nextAngle >=(currentAngle-15)))
				except IndexError:
					pass
			else:
				continueWalking = False
			if (math.hypot((nextNode['x']-currentPos[0]),(nextNode['y']-currentPos[1])) <= 150) or continueWalking:
				# audio feedback node reached
				thread_audio = threading.Thread(target=THREAD_AUDIO,args=["node reached"])
				thread_audio.start()
				break
			else:
				#audiofeedback dir and steps
				feedbackString = generateFeedback(dist, angle, pace)
				thread_audio = threading.Thread(target=THREAD_AUDIO,args=[feedbackString])
				thread_audio.start()

feedbackGiver.audioFeedback("reached")
print ("End")