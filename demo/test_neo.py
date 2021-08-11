import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D21, 30)
pixels.fill((0, 0, 0))
time.sleep(100000)