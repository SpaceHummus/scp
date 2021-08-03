import board
import neopixel
import time
from gpiozero import LED

pixels = neopixel.NeoPixel(board.D21, 12,brightness=0.1)
led = LED(20)

def start_LED ():
    pixels.fill((255, 255, 255))

def stop_LED():
    pixels.fill((0, 0, 0))

def light_pixel(from_pixle,to_pixle,R,G,B):
    for i in range(from_pixle,to_pixle):
        pixels[i] = (R,G,B)



# while True:
#     led.on()
#     time.sleep(1)
#     led.off()
#     time.sleep(1)
start_LED()
time.sleep(1)
stop_LED()
light_pixel(0,6,50,100,200)
light_pixel(6,12,200,0,0)
time.sleep(1)
stop_LED()
