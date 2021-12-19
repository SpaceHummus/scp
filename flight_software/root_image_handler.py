import serial
from time import sleep
import logging

IMAGE_SIZE = 137244
IMAGES_DIR = "images/"

class RootImageHandler:

    def send_uart_cmd(self,serial, data):
        print("Sending:",data)
        serial.write(data)              
        s = serial.read(1)
        print("recevied:",s)
    
    def white_led_on(self):
        ser = serial.Serial ("/dev/ttyAMA0", 115200,parity='N',stopbits=1, timeout=0.1)    #on PI2
        self.send_uart_cmd(ser,b'\x16')
        ser.close()

    def white_led_off(self):
        ser = serial.Serial ("/dev/ttyAMA0", 115200,parity='N',stopbits=1, timeout=0.1)    #on PI2
        self.send_uart_cmd(ser,b'\x18')
        ser.close()

    def take_pic(self,file_name):
        logging.info("about to take root image...")
        ser = serial.Serial ("/dev/ttyAMA0", 115200,parity='N',stopbits=1, timeout=0.1)    #on PI2
        # reset the cam
        self.send_uart_cmd(ser,b'\x02')
        # configure the cam
        self.send_uart_cmd(ser,b'\x04')
        # take image
        file = open(IMAGES_DIR+file_name+".bin", "wb")
        try:
            for i in range(IMAGE_SIZE):
                ser.write(b'\x00')              
                s = ser.read(1)
                file.write(s)
                # print(s)
            
        finally:
            file.close()
            ser.close()
        logging.info("done taking root image...")        



if __name__ == "__main__":
    root_image = RootImageHandler()
    root_image.white_led_on()
    sleep(0.5)
    root_image.white_led_off()
