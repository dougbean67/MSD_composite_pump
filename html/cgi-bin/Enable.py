#!/usr/bin/python
#from __future__ import division
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import os
import multiprocessing
from multiprocessing import Manager
from datetime import datetime
import cgi

os.getenv('PORT','8080')
os.getenv('IP','0.0.0.0')

ENA = "P9_24"
GPIO.setup(ENA, GPIO.OUT)

# use form to get inputs from the webpage
form = cgi.FieldStorage()
#ENA_val = cgi.getfirst('ENA_Val')
#ENA_val = form.__getattr__("value")
ENA_val = form.getfirst("ENA_Val")
#ENA_val = form.getvalue('Enable')

#if ENA_val == 'Enabled':
if 'n' in ENA_val:
    value = 'Disabled'
    ENA_bool = 1
else:
    value = 'Enabled'
    ENA_bool = 0

GPIO.output(ENA,ENA_bool)

print value