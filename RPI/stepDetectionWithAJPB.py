import adaptiveJerkPaceBuffer as ajpb
import lowPassFilter as lpf

def pull_data(dir_name, file_name):
	f = open(file_name + '.csv')
	xs = []
	ys = []
	zs = []
	rs = []
	timestamps = []
	for line in f:
		value = line.split(',')
		if len(value) > 3:
			timestamps.append(float(value[0]))
			x = float(value[1])
			y = float(value[2])
			z = float(value[3])
			r = math.sqrt(x**2 + y**2 + z**2)
			xs.append(x)
			ys.append(y)
			zs.append(z)
			rs.append(r)
	return np.array(xs), np.array(ys), np.array(zs), np.array(rs), np.array(timestamps)

def stepDetection():
	
	stepsDataCollector()
	
	x,y,z,r,timestamps = pull_data('accelerometer')
	
	# Filter Params
	order = 3
	fs = 50.0       # sample rate, Hz
	cutoff = 3.667  # desired cutoff frequency of the filter, Hz
	
	lowPassR = lpf.butter_lowpass_filter(r,cutoff,fs,order)
	
	peaks,troughs,average = ajpb.adaptive_jerk_pace_buffer(data, timestamps)
	
	print ("Number of steps", len(troughs))