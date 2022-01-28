import serial
from time import sleep
import logging

IMAGE_SIZE = 137244
IMAGES_DIR = "images/"

class RootImageHandler:


    def get_serial_connection(self):
        return serial.Serial ("/dev/ttyAMA0", 115200,parity='N',stopbits=1, timeout=0.1)    #on PI2
    
    def send_uart_cmd(self,serial, data, read_back_bytes=1):
        logging.info("Sending:%s",data)
        serial.write(data)
        sleep(0.5)
        if read_back_bytes>0:
            s = serial.read(read_back_bytes)
            logging.info("recevied:%s",s)
            return s
    
    def white_led_on(self):
        ser = self.get_serial_connection()
        self.send_uart_cmd(ser,b'\x16')
        self.send_uart_cmd(ser,b'\x17')
        ser.close()

    def white_led_off(self):
        ser = self.get_serial_connection()
        self.send_uart_cmd(ser,b'\x18')
        self.send_uart_cmd(ser,b'\x19')
        ser.close()

    def IR_led_on(self):
        ser = self.get_serial_connection()
        self.send_uart_cmd(ser,b'\x10')
        self.send_uart_cmd(ser,b'\x11')
        ser.close()

    def IR_led_off(self):
        ser = self.get_serial_connection()
        self.send_uart_cmd(ser,b'\x12')
        self.send_uart_cmd(ser,b'\x13')
        ser.close()
   
    def IR_controlled_by_imager(self):
        ser = self.get_serial_connection()
        self.send_uart_cmd(ser,b'\x14')
        self.send_uart_cmd(ser,b'\x15')
        ser.close()

    def White_led_controlled_by_imager(self):
        ser = self.get_serial_connection()
        self.send_uart_cmd(ser,b'\x1A')
        self.send_uart_cmd(ser,b'\x1B')
        ser.close()

    def get_config(self, file_name, sector):
        ser = self.get_serial_connection()
        cmd = 10+sector
        values = bytearray([cmd,0]) # first byte in mem is the size of the whole memory 
        m_size = self.send_uart_cmd(ser,values,2)   
        logging.info("config size:%d",m_size[0])
        file = open(IMAGES_DIR+file_name, "wb")
        try:
            for adress in range(0,m_size[0]+1):
                values = bytearray([cmd,adress])
                data = self.send_uart_cmd(ser,values,2) 
                file.write(data)
        finally:
            file.close()

    def set_config(self, file_name, sector):
        ser = self.get_serial_connection()
        #first eraze the memory
        ack = self.send_uart_cmd(ser,b'\x02')
        ack = self.send_uart_cmd(ser,b'\x0C')
        if ack != b'\x0C':
            logging.error("unable to eraze UFM")
            return
        cmd = 14+sector
        file = open(IMAGES_DIR+file_name, "rb")
        try:
            adress=0
            while True:
                data = file.read(2)
                if len(data)==0:
                    break
                else:
                    values = bytearray([cmd,adress,data[0],data[1]])
                    adress+=1
                    self.send_uart_cmd(ser,values) 
        finally:
            file.close()






    def take_pic(self,file_name):
        logging.info("about to take root image...")
        ser = self.get_serial_connection()
        # reset the cam 0
        ret1 = self.send_uart_cmd(ser,b'\x02')
        # configure the cam 0
        ret2 =self.send_uart_cmd(ser,b'\x04')
        if ret1 != b'' and ret2 != b'':
            # take image 0
            file = open(IMAGES_DIR+file_name+"C0.bin", "wb")
            try:
                self.send_uart_cmd(ser,b'\x00',0)
                for i in range(IMAGE_SIZE):
                    s = ser.read(1)
                    if s == b'':
                        logging.error("unable to take pic from root imager 0")
                        break
                    file.write(s)
            finally:
                file.close()
        else:
            logging.error("unable to take pic from root imager 0")

        # reset the cam 0
        ret1 = self.send_uart_cmd(ser,b'\x03')
        # configure the cam 0
        ret2 =self.send_uart_cmd(ser,b'\x05')
        if ret1 != b'' and ret2 != b'':
            # take image 1
            file = open(IMAGES_DIR+file_name+"C1.bin", "wb")
            try:
                self.send_uart_cmd(ser,b'\x01',0)
                for i in range(IMAGE_SIZE):
                    s = ser.read(1)
                    if s == b'':
                        logging.error("unable to take pic from root imager 0")
                        break
                    file.write(s)
            finally:
                file.close()
                ser.close()
        else:
            logging.error("unable to take pic from root imager 1")
        logging.info("done taking root image...")        

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )    

if __name__ == "__main__":
    setup_logging()
    root_image = RootImageHandler()
    # root_image.get_config("root0.cfg",0)
    # root_image.get_config("root1.cfg",1)
    # root_image.set_config("root1.cfg",0)
    # root_image.set_config("root1.cfg",1)
    # root_image.white_led_on()
    # sleep(1)
    # root_image.white_led_off()
    # sleep(1)  
    root_image.take_pic("first_pic")
    # root_image.White_led_controlled_by_imager()
    # sleep(10000)
    # root_image.white_led_on()
    # root_image.take_pic("ttt")
    # sleep(1)
