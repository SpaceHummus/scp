from gpiozero import LED
from time import sleep

led = LED(26)

led.on()
sleep(100000)
