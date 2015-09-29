import adaptiveJerkPaceBuffer as ajpb
import lowPassFilter as lpf
import math
import numpy as np

def pull_data(file_name):
	f = open(file_name + '.csv')
	xs = []
	ys = []
	zs = []
	rs = []
	headings = []
	timestamps = []
	for line in f:
		value = line.split(',')
		if len(value) > 3:
			timestamps.append(float(value[0]))
			x = float(value[1])
			y = float(value[2])
			z = float(value[3])
			r = math.sqrt(x**2 + y**2 + z**2)
			heading = value[4]
			xs.append(x)
			ys.append(y)
			zs.append(z)
			rs.append(r)
			headings.append(heading)
	return np.array(xs), np.array(ys), np.array(zs), np.array(rs), np.array(timestamps), np.array(headings)

def stepDetection(timestamps,x,y,z, headings):
	#calculate r for each x,y,z
	rs = []
	for a,b,c in zip(x,y,z):
		rs.append(math.sqrt(a**2 + b**2 + c**2))

	x,y,z,r,timestamps = np.array(x), np.array(y), np.array(z), np.array(rs), np.array(timestamps)
	headings = np.array(headings)
	
	# Filter Params
	order = 3
	fs = 50.0       # sample rate, Hz
	cutoff = 3.667  # desired cutoff frequency of the filter, Hz
	
	lowPassR = lpf.butter_lowpass_filter(r,cutoff,fs,order)
	
	peaks,troughs,average, headingMoved = ajpb.adaptive_jerk_pace_buffer(lowPassR, timestamps, headings)
	
	#print("peaks", len(peaks))
	#print ("Number of steps", len(troughs))
	#print ("average", len(average))
	#print ("headingMoved", len(headingMoved))
	return headingMoved