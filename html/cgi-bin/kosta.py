""" --------------- Angular Encoder Library ------------------------
Made by Kosta Konstas aided by Doug Bean.
* Kosta Made this when doug's professor said not to.
"""
#import Adafruit_BBIO.ADC as ADC
import beaglebone_pru_adc as adc
import time
global degs


class encoder:
	ladc1 = 0
	ladc2 = 0
	step = 0

	freq = 100000
	place = 0
	last = 0
	lastseq = 0
	deg_inc = 360.0/1000/8
	callback = None
	storage = None
	prog_start = None
	capture = adc.Capture()

	def adc1(self):
		if self.ladc1 == 0 and self.capture.values[0]> 1500 :
			self.ladc1 = 1
			return self.ladc1
		elif self.ladc1 == 1 and self.capture.values[0] < 1000 :
			self.ladc1 = 0
			return self.ladc1
		else:
			return self.ladc1


	def adc2(self):
		if self.ladc2 == 0 and self.capture.values[2] > 1500 :
			self.ladc2 = 1
			return self.ladc2
		elif self.ladc2 == 1 and self.capture.values[2] < 1000:
			self.ladc2 = 0
			return self.ladc2
		else:
			return self.ladc2

	def __init__(self, callback, storage):
		self.capture.start()
		self.storage = storage
		self.callback = callback
		self.prog_start = time.time()
		self.run()
	
	def run(self):
		while True:
			# time.sleep(1.0/self.freq)
			vadc1 = self.adc1()
			vadc2 = self.adc2()
			#aadc1 = ADC.read("P9_37") 
			#aadc2 = ADC.read("P9_38") 
			seq = (vadc1 ^ vadc2) | (vadc2 << 1)
			if self.lastseq == seq:
				continue
			else:
				if self.lastseq == 0:
					if seq == 1:
						self.step = -1
					if seq == 3:
						self.step = 1
			
				self.lastseq = seq
				self.last = self.place
				self.place += self.step
			self.callback(self.place * self.deg_inc, self.storage, self.prog_start)

			#self.callback((seq, self.place, aadc1 ,  aadc2, vadc1, vadc2 ), self.storage, self.prog_start)

#A B SEQ		
#0 0 00 LOW 
#0 1 11 B leads A
#1 0 01 A leads B
#1 1 10 HIGH