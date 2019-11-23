import Adafruit_BBIO.ADC as ADC
import time

milli = lambda: int(round(time.time() * 1000))
ADC.setup()

ladc1 = 0

ladc2 = 0

freq = 1000
while True:
    print ADC.read("P9_37"), ",", ADC.read("P9_38")
    time.sleep(1/freq)

def adc1():
	global ladc1
	if ladc1 == 0 and ADC.read("P9_37") > 0.6:
		ladc1 = 1
		return ladc1
	elif ladc1 == 1 and ADC.read("P9_37") < 0.3:
		ladc1 = 0
		return ladc1
	else:
		return ladc1


def adc2():
	global ladc2
	if ladc2 == 0 and ADC.read("P9_38") > 0.6:
		ladc2 = 1
		return ladc2
	elif ladc2 == 1 and ADC.read("P9_38") < 0.3:
		ladc2 = 0
		return ladc2
	else:
		return ladc2

step = 0

freq = 1000
place = 0
last = 0
lastseq = 0
while True:
	time.sleep(1/freq)
	seq = (adc1() ^ adc2()) | (adc2() << 1)
	if lastseq == seq:
		continue
	
	if lastseq == 0:
		if seq == 1:
			step = -1
		if seq == 3:
			step = 1
	
	lastseq = seq
	last = place
	place += step
	if last != place:
		print place, ", ", ADC.read("P9_39"), ", ", ADC.read("P9_38"), ", ", seq

	
#0 0 00 low
#0 1 11 high 
#1 0 01 A  B
#1 1 10 B  A
