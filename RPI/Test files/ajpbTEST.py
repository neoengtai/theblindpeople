import adaptiveJerkPaceBuffer as ajpb
import lowPassFilter as lpf
import math
import numpy as np
import json

f = open("accel.json", "r")
values = json.load(f)
f.close()

x = []
timestamps = []
for val in values:
	timestamps.append(val[0])
	x.append(val[3])			#Change the axis where values are used

timestamps = np.array(timestamps)
x = np.array(x)

# Filter Params
order = 3
fs = 50.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

lowPassR = lpf.butter_lowpass_filter(x,cutoff,fs,order)

peaks,troughs,average = ajpb.adaptive_jerk_pace_buffer(lowPassR, timestamps)

print("No of steps: %d" %len(troughs))