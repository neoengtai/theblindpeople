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

print ("Press ctrl-c to stop data collection")
try:
	while True:
		if imu.IMURead():
			data = imu.getIMUData()
			timestamps.append(float(data["timestamp"]))
			x.append(float(10*data["accel"][0]))
			y.append(float(10*data["accel"][1]))
			z.append(float(10*data["accel"][2]))
		time.sleep(poll_interval*1.0/1000.0)
except KeyboardInterrupt:
	pass

steps = sd.stepDetection(timestamps,x,y,z)
numSteps = len(steps)
if numSteps == 0:
	print ("No steps detected!")
	exit(0)

distance = float(input("Enter the distance travelled(in centimeters): "))
pace = distance/numSteps
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