import board
import neopixel
import time
import RPi.GPIO as GPIO
import switch_handler

NUM_OF_PIXELS = 20

GROUP1_LED_INDEX = [0,1,2,3,4,10,11,12,13,14]
GROUP2_LED_INDEX = [5,6,7,8,9,15,16,17,18,19]

pixels = neopixel.NeoPixel(board.D21, NUM_OF_PIXELS,brightness=0.5)

GPIO.setmode(GPIO.BCM) 
GPIO.setup  (12, GPIO.OUT)
pwm0 = GPIO.PWM(12, 100)
# pwm0.start(0)

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
    pwm0.stop()
    pwm0.start(duty_cycle)
    pwm0.ChangeDutyCycle(duty_cycle)

# light a subset of LEDs    
def light_pixel_by_list(pixels_list,RGB):
    for i in range(len(pixels_list)):
        pixels[pixels_list[i]] = (RGB.R,RGB.G,RGB.B)

# light both groups of LEDs based on thier RGB settings 
def light_all_pixels(RGB_GROUP1,RGB_GROUP2):
    light_pixel_by_list (GROUP1_LED_INDEX,RGB_GROUP1)     
    light_pixel_by_list (GROUP2_LED_INDEX,RGB_GROUP2)     


# Built in test to try all LEDs
def built_in_test ():

    from_pixel = 0
    to_pixel = NUM_OF_PIXELS-1
    
    print("Turn off everything")
    stop_LED()
    light_far_red(0)
    time.sleep(1)
    
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
    light_far_red(50)
    time.sleep(1)
    
    print("Light everything - max intensity")
    light_pixel(from_pixel,to_pixel,255,255,255)
    light_far_red(50)
    time.sleep(1)
    
    print("Turn off everything")
    light_far_red(0)
    stop_LED()
    time.sleep(1)
    print("Done")
    
    
# Shine light at max nominal condition
def built_in_test_nominal_condition ():

    from_pixel = 0
    to_pixel = NUM_OF_PIXELS-1
    
    print("Turn off everything")
    stop_LED()
    light_far_red(0)
    time.sleep(1);
    
    print("Nominal Ilumination")
    light_pixel(from_pixel,to_pixel,150,210,255)
    light_far_red(12)
    time.sleep(10)
    
    print("Extra Umpf")
    light_pixel(from_pixel,to_pixel,255,255,255)
    light_far_red(15)
    time.sleep(10)
    
    print("Turn off everything")
    stop_LED()
    light_far_red(0)
    time.sleep(1);
    print("Done")


if __name__ == "__main__":
    # sw_handler = switch_handler.SwitchHandler()
    # sw_handler.set_switch(switch_handler.SWITCH_LED_PIN,switch_handler.SWITCH_OFF)
    # time.sleep(1)
    # sw_handler.set_switch(switch_handler.SWITCH_LED_PIN,switch_handler.SWITCH_ON)
    # time.sleep(1)
    light_pixel(0,NUM_OF_PIXELS-1,255,255,255)
    # light_far_red(100)
    time.sleep(10)
    light_pixel(0,NUM_OF_PIXELS-1,0,0,0)
    # print("moving to 10 dc")
    # light_far_red(10)
    # time.sleep(20000)
    # light_pixel(0,NUM_OF_PIXELS-1,255,255,255)
    # light_pixel(0,NUM_OF_PIXELS-1,0,0,0)
    # built_in_test()
    # built_in_test_nominal_condition()
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

