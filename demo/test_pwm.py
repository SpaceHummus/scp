import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setup  (13, GPIO.OUT)
pwm = GPIO.PWM(13, 100)
dc=0   # set dc variable to 0 for 0%
pwm.start(dc)
pwm.ChangeDutyCycle(dc)
while True:
    pwm.ChangeDutyCycle(10)
    time.sleep(2) 
    pwm.ChangeDutyCycle(100) 
    time.sleep(2)
