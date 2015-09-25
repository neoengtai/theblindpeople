import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

def stepsDataCollector():
	SETTINGS_FILE = "RTIMULib"
	
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
	imu.setGyroEnable(True)
	imu.setAccelEnable(True)
	imu.setCompassEnable(True)
	
	poll_interval = imu.IMUGetPollInterval()
	
	try:
		f = open('accelerometer.csv', 'w')
		while True:
			if imu.IMURead():
				data = imu.getIMUData()
				timestamp = data["timestamp"]
				# multiplied by 10 for the steps library
				accX = 10*data["accel"][0]
				accY = 10*data["accel"][1]
				accZ = 10*data["accel"][2]
				f.write("%d,%f,%f,%f\r\n" % (timestamp,accX,accY,accZ))
				time.sleep(poll_interval*1.0/1000.0)
				
	except KeyboardInterrupt:
		f.close()
		print ("File saved...")