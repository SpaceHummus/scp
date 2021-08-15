from gpiozero import LED
from time import sleep

led = LED(12)
led2 = LED(13)
led.on()
led2.on()
sleep(100000) 
