import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setup  (12, GPIO.OUT)
pwm = GPIO.PWM(12, 100)
GPIO.setup  (13, GPIO.OUT)
pwm2 = GPIO.PWM(13, 100)


dc=100   # set dc variable to 0 for 0%
pwm.start(dc)
pwm.ChangeDutyCycle(dc)
pwm2.start(dc)
pwm2.ChangeDutyCycle(dc)
time.sleep(100000) 

# while True:
#     pwm.ChangeDutyCycle(10)
#     time.sleep(5) 
#     pwm.ChangeDutyCycle(100) 
#     time.sleep(5)
