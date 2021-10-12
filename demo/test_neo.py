import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D21, 12,brightness=0.5)
pixels.fill((255,255,255))
time.sleep(5)
pixels.fill((0,0,0))




# pixels[0] = (250,250,250)
# pixels.show()

# while True:
#     for i in range(12):
#         pixels[i]=(255,0,255)
#         pixels[11-i]=(100,200,0)
#         pixels.show()
#         time.sleep(0.3)
#         pixels[i]=(0,0,0)
#         pixels[11-i]=(0,0,0)


# time.sleep(2)
# pixels.fill((0, 0, 0))
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