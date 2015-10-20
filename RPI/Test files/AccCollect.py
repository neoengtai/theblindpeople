#Collect pure x,y,z acceleration data (without gravity) with timestamps

import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import json

SETTINGS_FILE = "Configuration/RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
print("IMU Name: " + imu.IMUName())

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
print ("Interval: ", poll_interval)

f = open("accel.json", "w")
data = []

input ("Press enter to continue...")
try:
	while True:
		if imu.IMURead():
			dat = imu.getIMUData()
			acc = imu.getAccelResiduals()
			data.append((dat['timestamp'],)+acc)

except KeyboardInterrupt:
	json.dump(data,f)
	f.close()