import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import StepDetector as sd
import calculateStepDistanceTravelled as tracker

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

def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));

SETTINGS_FILE = "RTIMULib"
CALIBRATION_FILE = "profile.ini"

# 0: Z point front, X point down
# 1: Z point left, X point front
# 2: Z point up, X point front
IMU_MOUNT_DIRECTION = 2
NORTH_AT = 0

if not os.path.exists(CALIBRATION_FILE):
	pace = 50.0
	print("No profile found. Using default pace of 50 cm/step")
else:
	#Note: no checking of whether or not first line is PACE_AVG
	f = open(CALIBRATION_FILE)
	val = f.readline().split('=')
	pace = float(val[1])


if not os.path.exists(SETTINGS_FILE + ".ini"):
	print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

if (not imu.IMUInit()):
	print("IMU Init Failed")
	sys.exit(1)
else:
	print("IMU Init Succeeded");

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

if (not pressure.pressureInit()):
    print("Pressure sensor Init Failed")
else:
    print("Pressure sensor Init Succeeded")

poll_interval = imu.IMUGetPollInterval()*1.0/1000.0

timestamps = []
x = []
y = []
z = []
headings = []
currX = 0
currY = 0

input ("Press enter to begin navigation...")
loopTime = printTime = time.time()
dt = 0
while True:
	#time passed since last loop
	dt = time.time() - loopTime
	if dt >= poll_interval:
		loopTime = time.time()
		if imu.IMURead():
			data = imu.getIMUData()
			# multiplied by 10 for the steps library
			timestamps.append(float(data["timestamp"]))
			x.append(float(data["accel"][0]))
			y.append(float(data["accel"][1]))
			z.append(float(data["accel"][2]))
			headings.append(math.degrees(data["fusionPose"][IMU_MOUNT_DIRECTION]))
			
			if loopTime - printTime >= 4.0:
				printTime = loopTime
				
				heading = math.degrees(math.atan2(data["compass"][1], data["compass"][0]))* (-1)
				(data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
				if (data["pressureValid"]):
					altitude = computeHeight(data["pressure"])
				moved = sd.stepDetection(timestamps,x,y,z,headings)
				tempX, tempY = tracker.calculateStepDistance(pace,moved,NORTH_AT)
				currX += tempX
				currY += tempY
				distance = math.hypot(currX, currY)

				print ("Distance: %6.0f Heading: %3.1f Altitude: %6.0f X: %d Y: %d" % (distance, heading, altitude, currX, currY))

				del timestamps[:]
				del x[:]
				del y[:]
				del z[:]
				del headings[:]
				

			#just to check performance
			# if dt >= 0.01:
			# 	print ("dt: %f" % dt)