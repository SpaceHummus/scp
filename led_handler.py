import board
import neopixel
import time
from gpiozero import LED
# import RPi.GPIO as GPIO

pixels = neopixel.NeoPixel(board.D21, 12,brightness=0.1)
# led = LED(20)

def start_LED ():
    pixels.fill((255, 255, 255))

def stop_LED():
    pixels.fill((0, 0, 0))

def light_pixel(from_pixle,to_pixle,R,G,B):
    for i in range(from_pixle,to_pixle+1):
        pixels[i] = (R,G,B)
# def light_far_red(duty_cycle):
#     pwm.ChangeDutyCycle(duty_cycle)

# GPIO.setmode(GPIO.BOARD) 
# GPIO.setup  (38, GPIO.OUT)
# pwm = GPIO.PWM(38, 100)
# dc=0   # set dc variable to 0 for 0%
# pwm.start(dc)
# pwm.ChangeDutyCycle(dc)
# while True:
#     pwm.ChangeDutyCycle(5)
#     time.sleep(2) 
#     pwm.ChangeDutyCycle(100) 
#     time.sleep(2)

# while True:
#     led.on()
#     time.sleep(1)
#     led.off()
#     time.sleep(1)

print("start")
start_LED()
time.sleep(1)
stop_LED()
light_pixel(0,6,50,100,200)
light_pixel(6,11,200,0,0)
time.sleep(1)
stop_LED()
print("end")
