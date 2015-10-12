#Returns a csv file of x,y,z accelerometer values and magnitude passed through a lowpass filter

import lowPassFilter as lpf
import math
import numpy as np
import json

f = open("accel.json", "r")
js = json.load(f)
f.close()

# option = int(input("Axis?: "))

x = []
y = []
z = []
r = []

for val in js:
	xx,yy,zz = val[1],val[2],val[3]
	x.append(xx)
	y.append(yy)
	z.append(zz)
	r.append(math.sqrt(xx**2 + yy**2 + zz**2))

order = 3
fs = 50.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

lowPassX = lpf.butter_lowpass_filter(x,cutoff,fs,order)
lowPassY = lpf.butter_lowpass_filter(y,cutoff,fs,order)
lowPassZ = lpf.butter_lowpass_filter(z,cutoff,fs,order)
lowPassR = lpf.butter_lowpass_filter(r,cutoff,fs,order)
zipped = zip(lowPassX.tolist(),lowPassY.tolist(),lowPassZ.tolist(),lowPassR.tolist())

f = open("lowpass.csv", "w")
for val in zipped:
	f.write("%.8f,%.8f,%.8f,%.8f\n" % (val[0],val[1],val[2],val[3]))

f.close()