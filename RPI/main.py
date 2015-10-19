
# sys.path.append('.')
# import math

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

SETTINGS_FILE = "Configuration/RTIMULib"
CALIBRATION_FILE = "Configuration/profile.ini"
IMU_SAMPLING_PERIOD = 0.02 	# In seconds

BUILDING_LIST = {	1: "COM1",
					2: "COM2",
				}

def getSrcDestNodes():
	places = {"Source": None, "Destination": None}

	for k,v in places.items():
		if k == "Source":
			clip = "enter starting building"
		elif k == "Destination":
			clip = "enter ending building"

		while v is None:
			building = None

			feedbackGiver.audioFeedback(clip)
			print(k + " building: ")
			buildingID = int(keypad.dummyGetKey()) #TODO: change to actual keypad getKey
			if buildingID in BUILDING_LIST:
				building = BUILDING_LIST[buildingID]
			else:
				feedbackGiver.audioFeedback("error")
				print ("Building not in list!")
				continue
			
			feedbackGiver.audioFeedback("enter level")
			print (k + " level: ")
			level = keypad.dummyGetKey() #TODO: change to actual keypad getKey
				
			if mapManager.get_map(building, level) is None:
				feedbackGiver.audioFeedback("error")
				print ("Cannot find map!")
				continue
			
			feedbackGiver.audioFeedback("enter node")
			print(k + " nodeID: ")
			nodeId = keypad.dummyGetKey() #TODO: change to actual keypad getKey

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
				pt = time.time()
				imu_Q.put(buf)
				print ("Put time: ", (time.time() - pt))
				print ("IMURate: ", len(buf)/(pt - s_time))
				break

			if imu.IMURead():
				data = imu.getIMUData()
				buf.append((data['timestamp'],)+data['accel']+(data['fusionPose'][2],))

			time.sleep(0.5*IMU_SAMPLING_PERIOD)

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
thread_imu_pause_flag = False

# -------------------------------Init Section----------------------------------
pace = loadUserProfile()
imu_Q = queue.Queue()
keypad = KP.Keypad()
#init Arduino
feedbackGiver = FG.FeedbackGiver()
#init WiFi (just to test for connection)
positionTracker = PT.PositionTracker(0,0,pace)
mapManager = MM.MapManager()

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
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

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

		while True:
			# This call blocks until the IMU thread puts data into the queue
			imuData = imu_Q.get()
			positionTracker.updatePosition(imuData,northAt)
			imu_Q.task_done()

			print ("Current pos: ", positionTracker.getCurrentPosition())