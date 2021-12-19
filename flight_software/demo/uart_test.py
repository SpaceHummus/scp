'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial
from time import sleep

IMAGE_SIZE = 137244
# ser = serial.Serial ("/dev/ttyS0", 115200,parity='N',stopbits=1, timeout=0.1)    #on PI4
ser = serial.Serial ("/dev/ttyAMA0", 115200,parity='N',stopbits=1, timeout=0.1)    #on PI2

# ser.write(b'\x02')              
# s = ser.read(1)
# print(s)
# sleep(0.5)
# ser.write(b'\x04')              
# s = ser.read(1)
# print(s)
# sleep(0.5)


# take image
# file = open("image.bin", "wb")
# for i in range(IMAGE_SIZE):
#     ser.write(b'\x00')              
#     s = ser.read(1)
#     file.write(s)
#     print(s, i)
    
# file.close()
# ser.close()

# blink both LEDs
while True:
    ser.write(b'\x10')  
    s = ser.read(1)
    print(s)
    ser.write(b'\x18') 
    s = ser.read(1)
    print(s)
    sleep(0.5)
    ser.write(b'\x12')  
    s = ser.read(1)
    print(s)
    
    ser.write(b'\x16') 
    s = ser.read(1)
    print(s)
    sleep(0.5)


ser.close()