import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import StepDetector as sd

SETTINGS_FILE = "RTIMULib"
CALIBRATION_FILE = "profile.ini"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded");
	
imu.setSlerpPower(0.02)
imu.setGyroEnable(False)
imu.setAccelEnable(False)
imu.setCompassEnable(False)

poll_interval = imu.IMUGetPollInterval()

timestamps = []
x = []
y = []
z = []
headings = []
totalSteps = 0

print ("Press ctrl-c to stop data collection")
try:
	prevTime = 0
	while True:
		if imu.IMURead():
			data = imu.getIMUData()
			timestamps.append(float(data["timestamp"]))
			x.append(float(data["accel"][0]))
			y.append(float(data["accel"][1]))
			z.append(float(data["accel"][2]))
			headings.append(0)
		#calculate steps and clear all buffers every 5 seconds
		if time.time() - prevTime >= 4.0:
			prevTime = time.time()
			steps = sd.stepDetection(timestamps,x,y,z,headings)
			totalSteps += len(steps)
			del timestamps[:]
			del x[:]
			del y[:]
			del z[:]
			del headings[:]
except KeyboardInterrupt:
	steps = sd.stepDetection(timestamps,x,y,z,headings)
	totalSteps += len(steps)
	pass


if totalSteps == 0:
	print ("No steps detected!")
	exit(0)

print ("No. of steps: %d" % totalSteps)
distance = float(input("Enter the distance travelled(in centimeters): "))
pace = distance/totalSteps
print ("Pace(cm/step): ", pace)

#Save calibration data to file
if os.path.exists(CALIBRATION_FILE):
	prevPace = None
	prevMeasurements = None
	f = open(CALIBRATION_FILE, "r+")
	for line in f:
		value = line.split('=')
		if value[0] == "PACE_AVG":
			prevPace = float(value[1])
		elif value[0] == "PACE_MEASUREMENTS":
			prevMeasurements = int(value[1])
	if prevPace is not None:
		newTotal = prevMeasurements + 1
		newAvg = (prevPace*prevMeasurements+pace)/(newTotal)
		f.seek(0)
		f.write("PACE_AVG=%f\r\n" % newAvg)
		f.write("PACE_MEASUREMENTS=%d\r\n" % newTotal)
	else:
		f.seek(0)
		f.write("PACE_AVG=%f\r\n" % pace)
		f.write("PACE_MEASUREMENTS=%d\r\n" % 1)
	f.close()
else:
	f = open(CALIBRATION_FILE, "w")
	f.write("PACE_AVG=%f\r\n" % pace)
	f.write("PACE_MEASUREMENTS=%d\r\n" % 1)
	f.close()