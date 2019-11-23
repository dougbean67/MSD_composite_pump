#!/usr/bin/python
from __future__ import division
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import os
from datetime import datetime
import cgi
 
PWM.cleanup()
GPIO.cleanup()
print ("Done") 
