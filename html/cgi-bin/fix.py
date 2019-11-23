import Adafruit_BBIO.GPIO as GPIO
import time
ENA = "P9_24"
GPIO.setup(ENA, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
GPIO.output(ENA, 1)

while (True):
	time.sleep(10000000)
