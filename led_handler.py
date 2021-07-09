import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 12,brightness=2)

def start_LED ():
    pixels.fill((255, 255, 255))

def stop_LED():
    pixels.fill((0, 0, 0))
