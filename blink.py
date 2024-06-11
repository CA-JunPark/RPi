#!./env/bin/python3

import RPi.GPIO as GPIO
from time import sleep

LED = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(LED, GPIO.HIGH)
    sleep(1)
    GPIO.output(LED, GPIO.LOW)
    sleep(1)
