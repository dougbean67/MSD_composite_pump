#!/usr/bin/python
#from __future__ import division
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time
import os
from kosta import encoder
import multiprocessing
from multiprocessing import Manager
from datetime import datetime
import cgi
import sys
try:
    import simplejson as json
except:
    import json
#import chart_studio.plotly as py
#from plotly.graph_objects import *
#from plotly.offline import plot
#from plotly.graph_objs import Scatter, Layout, layout, Figure
#import plotly.io as pio

os.getenv('PORT','8080')
os.getenv('IP','0.0.0.0')

manager = Manager()
degs = manager.list()

# Use ValueLogger to gather angular encoder data
def valuelogger(val, degs, start_time):
    degs += [ round((time.time()-start_time)*1000, 4), val ]

def chngDir(rot,M1,M2,cur_deg,Pdeg):
    if rot: # Rot_Dir == 1 then CW
        GPIO.output(M2, GPIO.HIGH)
        GPIO.output(M1, GPIO.LOW)
        c_deg = cur_deg + Pdeg
    else:
        GPIO.output(M2, GPIO.LOW)
        GPIO.output(M1, GPIO.HIGH)
        c_deg = cur_deg - Pdeg
    return c_deg

# use form to get inputs from the webpage
form = cgi.FieldStorage()
# print form

# Set the Pin numbers for beaglebone
DIR13 ="P9_23"
DIR24 = "P8_9"
PUL1="P9_21"
ENA = "P9_24"
GPIO.setup(DIR13, GPIO.OUT)
GPIO.setup(DIR24, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

f = float(form.getvalue('freq'))
cycles = int(form.getvalue('cycles'))
Rot_Dir = int(form.getvalue('Dir'))
degree = float(form.getvalue('degree'))
cur_deg = float(form.getvalue('curPos'))
# f = 600.0
# cycles =2
# Rot_Dir = False
# degree = 10
# cur_deg = 0

T = 1/f
deg = degree*2
pulsesPerRev = 12800 # this value must be set equal to the number determined by the Dip switches on the motor drivers. 
deg_inc = 360.0/pulsesPerRev
switch_time = 0 # define a variable to account for the time it takes for the motors to switch direction.
nPUL = round(deg/deg_inc) # pulses per revolution 
act_Pdeg = deg_inc*nPUL*0.5
#print ("Pulses: ", nPUL)
#print ("Expected Duration: ", round(T*nPUL*1000, 4), " ms")
#print ("Expected Pulse width: ", round(T*1000, 4), " ms") 
# print ("Expected Degrees", deg_inc*nPUL)
prog_start = time.time()
enc = multiprocessing.Process(target=encoder, args=([valuelogger, degs]))
enc.start()

for k in range (cycles):
  if k%2 == 1:
      PWM_deg = chngDir(Rot_Dir,DIR13,DIR24,cur_deg,act_Pdeg)
  else:
      PWM_deg = chngDir(not Rot_Dir,DIR13,DIR24,cur_deg,act_Pdeg)
  i = 0
  beanfactor = 0
  PWM.start(PUL1, 0, f)  # set PWM (Pin,Duty cycle [%], frequency [Hz]) cur_deg = cur_deg = 
  start_time = time.time() 
  PWM.set_duty_cycle(PUL1, 50) # set duty cycle to 50% to 'turn it on'
  while start_time + T*nPUL + beanfactor > time.time(): # T*nPUL
       pass 
  PWM.stop(PUL1)
  switch_start = time.time() 
  switch_stop = time.time() 
  switch_time += switch_stop - switch_start
  
stop_time = time.time() #datetime.now()  
enc.terminate()
#print ("Actual Duration: ", round((stop_time-start_time)*1000, 4), " ms")  
#print ("Actual number of pulses: ", round((stop_time-start_time-switch_time)/T, 4))
# print ("Actual Degrees: ", round((stop_time-start_time-switch_time)/T*deg_inc, 4))

PWM.cleanup()
GPIO.cleanup()
x = []
y = []
for i in range(0, len(degs),2):
    x.append(degs[i])
    y.append('{0:.15f}'.format(degs[i+1]))

kosta = {}
kosta['x'] = x
kosta['y'] = y
kosta['curPos'] = cur_deg + degs[len(degs)-1]
dump = json.dumps(kosta)

print dump


#sys.stdout.write(json.dumps(result,indent=1))

# data = [
#     Scatter(
#         x=degs[::2],
#         y=degs[1::2],
#         name = "Angular Position",
#         connectgaps = False,
#         line=dict(width=3, color="blue"),
#         )
#     ]

# layout = Layout(title="Angular Position", xaxis=layout.XAxis(title ='time [ms]'), yaxis=layout.YAxis(title = 'Angle [degrees]'))
# fig = Figure(data=data, layout=layout)


#my_plot_div = plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])], output_type='div')
#my_plot_div = plot(fig, output_type='div')

# #print("Took ", time.time() - start, " to render graph")
# res= {}
# res["body"] = div
# sys.stdout.write(json.dumps(res))
# sys.stdout.write("\n")
# sys.stdout.close
#print cur_deg
#out = {'div': my_plot_div, 'curDeg': cur_deg}
#print cur_deg

#print cur_deg

# JSON 