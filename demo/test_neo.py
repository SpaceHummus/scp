import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D21, 12)
pixels.fill((255, 0, 0))
time.sleep(2)
pixels.fill((0, 0, 0))
quit()
# while True:
#     pixels.fill((255, 0, 0))
#     time.sleep(2)
#     pixels.fill((0, 255, 0))
#     time.sleep(2)
#     pixels.fill((0, 0, 255))
#     time.sleep(2)


pixels.fill((0, 0, 0))

time.sleep(100000)