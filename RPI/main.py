# import threading
# import time
# import queue
# sys.path.append('.')
# import time
# import math
# import StepDetector as sd

import os.path
import sys
import RTIMU
import MapManager as MM
import RouteFinder as RF
import FeedbackGiver as FG
import Keypad as KP

SETTINGS_FILE = "Configuration/RTIMULib.ini"

BUILDING_LIST = {	1: "COM1",
					2: "COM2",
				}

def initIMU():
	if not os.path.exists(SETTINGS_FILE):
		print("Settings file not found!")
		sys.exit(1)

	s = RTIMU.Settings(SETTINGS_FILE)
	imu = RTIMU.RTIMU(s)

	if (not imu.IMUInit()):
		print("IMU Init Failed")
		sys.exit(1)

	# Set params for the imu (r,p,y) values calculation
	imu.setSlerpPower(0.02)
	imu.setGyroEnable(True)
	imu.setAccelEnable(True)
	imu.setCompassEnable(True)

def getSrcDestNodes():
	places = {"Source": None, "Destination": None}

	for k,v in places.items():
		if k == "Source":
			clip = "enter starting building"
		elif k == "Destination":
			clip = "enter ending building"

		while v is None:
			building = None

			# feedbackGiver.audioFeedback(clip)
			print(k + " building: ")
			buildingID = int(keypad.dummyGetKey()) #TODO: change to actual keypad getKey
			if buildingID in BUILDING_LIST:
				building = BUILDING_LIST[buildingID]
			else:
				# feedbackGiver.audioFeedback("error")
				print ("Building not in list!")
				continue
			
			# feedbackGiver.audioFeedback("enter level")
			print (k + " level: ")
			level = keypad.dummyGetKey() #TODO: change to actual keypad getKey
				
			if mapManager.get_map(building, level) is None:
				# feedbackGiver.audioFeedback("error")
				print ("Cannot find map!")
				continue
			
			# feedbackGiver.audioFeedback("enter node")
			print(k + " nodeID: ")
			nodeId = keypad.dummyGetKey() #TODO: change to actual keypad getKey

			if mapManager.get_node(building,level,nodeId) is None:
				# feedbackGiver.audioFeedback("error")
				print ("Invalid node!")
				continue
			else:
				v = (building, level, nodeId)
				places.update({k : v})

	return places["Source"], places["Destination"]

# def producer(threadName, delay):
# 	while True:
# 		if q.qsize() >= 3:
# 			print(threadName + " size reached")
# 		else:
# 			_list = []
# 			for i in range(1,11):
# 				_list.append(i)

# 			print (threadName + "putting")
# 			q.put(_list)
# 		time.sleep(delay)

# def consumer(threadName, delay):
# 	while True:
# 		_list = q.get()
# 		print (threadName + ":"  + str(_list))
# 		time.sleep(delay)



# Shared data: 1
# 1 -> Current position (x,y)

# Consumers: 2
# 1 -> PositionTracker takes accelerometer data and determines current position
# 2 -> FeedbackGiver takes UART data and provides feeback

# Producers: 2
# 1 -> Sample accelerometer. Data only used by PositionTracker
# 2 -> UART from arduino. Data only used by FeedbackGiver

# q = queue.Queue()

# producer1 = threading.Thread(target=producer, args = ("P1", 0.5))

# consumer1 = threading.Thread(target=consumer, args = ("C1", 0.7))

# producer1.start()
# consumer1.start()

#START OF PROGRAM
# ---------------------------------Variables-----------------------------------
imu = None
feedbackGiver = None
mapManager = None
keypad = None
source, destination = None, None

# -------------------------------Init Section----------------------------------
initIMU()
keypad = KP.Keypad()
#init Arduino
feedbackGiver = FG.FeedbackGiver()
#init WiFi (just to test for connection)
#init PositionTracker
mapManager = MM.MapManager()

# ----------------------------Start of navigation------------------------------
source, destination = getSrcDestNodes()

# TODO: Change to audio
print (source,destination)

path = RF.findRoute(mapManager, source[2], source[0], source[1], 
					destination[2], destination[0], destination[1])

print (path)