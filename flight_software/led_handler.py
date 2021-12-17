import board
import neopixel
import time
import RPi.GPIO as GPIO
 

NUM_OF_PIXELS = 20


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
#   from_pixle, to_pixle - pixel index to set intensity from pixel to pixel index inclusive (0 to 19)
#   R,G,B from 0 to 255
def light_pixel(from_pixle,to_pixle,R,G,B):
    for i in range(from_pixle,to_pixle+1):
        pixels[i] = (R,G,B)

# Set far red intensity 
# Inputs:
#   duty_cycle - from 0 to 100
def light_far_red(duty_cycle):
    pwm0_neopixel.ChangeDutyCycle(duty_cycle)
    

# Built in test to try all LEDs
def built_in_test ():

    from_pixel = 0
    to_pixel = NUM_OF_PIXELS-1
    
    print("Turn off everything")
    stop_LED()
    light_far_red(0)
    time.sleep(1);
    
    print("Neopixel Red")
    light_pixel(from_pixel,to_pixel,255,0,0)
    time.sleep(1)
    
    print("Neopixel Green")
    light_pixel(from_pixel,to_pixel,0,255,0)
    time.sleep(1)
    
    print("Neopixel Blue")
    light_pixel(from_pixel,to_pixel,0,0,255)
    time.sleep(1)
    
    print("Neopixel White (Max Intensity)")
    light_pixel(from_pixel,to_pixel,255,255,255)
    time.sleep(1)
    
    print("Neopixel off, far RED on max intensity")
    light_pixel(from_pixel,to_pixel,0,0,0)
    light_far_red(100)
    time.sleep(1)
    
    print("Light everything - max intensity")
    light_pixel(from_pixel,to_pixel,255,255,255)
    light_far_red(100)
    time.sleep(1)
    
    print("Turn off everything")
    light_far_red(0)
    stop_LED()
    time.sleep(1)
    print("Done")


if __name__ == "__main__":
    built_in_test()
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

