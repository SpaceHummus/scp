import time
import board
import adafruit_ina260
import smbus
import time
import os 


i2c = board.I2C()
ina260 = adafruit_ina260.INA260(i2c, address=0x40)

while True:

    # print(check_a2d(0x00))
    # print(
    #     "Current: %.4f mA Voltage: %.4f V Power:%.4f mW"
    #     % (ina260._raw_current, ina260._raw_voltage, ina260._raw_power)
    # )
    ina260 = adafruit_ina260.INA260(i2c, address=0x40)
    ina260.mode = adafruit_ina260.Mode.CONTINUOUS
    print(
        "Current: %.4f mA Voltage: %.4f V Power%.4f mW"
        % (ina260.current, ina260.voltage, ina260.power)
    )
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
    time.sleep(5)
    
