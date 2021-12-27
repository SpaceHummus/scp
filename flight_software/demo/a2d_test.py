import smbus
import time
import os 

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43
bus = smbus.SMBus(1)

def check_a2d(read):
    bus.write_byte(address,read)
    value = bus.read_byte(address)
    print(read)
    print("AOUT:%d  " %(value))
    time.sleep(1)

while True:
    # bus.write_byte(address,A1)
    # value = bus.read_byte(address)
    # print("AOUT:%1.3f  " %(value*3.3/255))
    # time.sleep(0.1)
    os.system('clear')
    check_a2d(A0)
    check_a2d(A1)
    check_a2d(A2)
    check_a2d(A3)
    time.sleep(10)
    
