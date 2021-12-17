import board
import neopixel
import time
import RPi.GPIO as GPIO
 

NUM_OF_PIXELS = 12


pixels = neopixel.NeoPixel(board.D21, NUM_OF_PIXELS,brightness=0.5)
GPIO.setmode(GPIO.BCM) 
GPIO.setup  (12, GPIO.OUT)
pwm0_neopixel = GPIO.PWM(12, 100)
pwm0_neopixel.start(0)

def start_LED ():
    pixels.fill((255, 255, 255))

def stop_LED():
    pixels.fill((0, 0, 0))

# Set Neopixel intensity
# Inputs:
#   from_pixle, to_pixle - pixel index to set intensity (0 to 19)
#   R,G,B from 0 to 255
def light_pixel(from_pixle,to_pixle,R,G,B):
    for i in range(from_pixle,to_pixle+1):
        pixels[i] = (R,G,B)

# Set far red intensity 
# Inputs:
#   duty_cycle - from 0 to 100
def light_far_red(duty_cycle):
    pwm0_neopixel.ChangeDutyCycle(duty_cycle)




if __name__ == "__main__":
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
    time.sleep(1)
    stop_LED()
    print("end")
