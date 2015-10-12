import json

f = open("lowpass.json", "r")
js = json.load(f)
f.close()

bias = 0.5

#axis to integrate
axis = 2	#(1,2,3) = (x,y,z)

a = 0
v = 0
#t = js[0][0]
t = 0
total_v = 0
total_s = 0

fx = []
for reading in js:
	#dt = reading[0] - t
	dt = 0.02
	#total_v += 0.5*(reading[axis] + a - 2 * bias)*dt
	total_v += 0.5*(reading + a - 2 * bias)*dt
	total_s += 0.5*(v+total_v)*dt

	#update with current values of a, v and t for next round
	#a = reading[axis]
	a = reading
	v = total_v
	#t = reading[0]

	fx.append((t,a,v,total_s,))

f = open("lowpassI.json", "w")
json.dump(fx,f)
f.close()