import board
import adafruit_bme680
import time
import busio
import adafruit_veml7700
from datetime import datetime
import csv
import logging


TELE_FILE = 'telematry.csv'

class TelematryHandler:

    i2c = None

    def __init__(self):
        self.i2c =  board.I2C()


    def get_bme680_telematry(self):
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
        logging.debug("Temperature:%d, Gas: %d ohms, Humidity: %d, Pressure: %d hPa",bme680.temperature,bme680.gas,bme680.humidity,bme680.pressure)
        return [bme680.temperature,bme680.gas,bme680.humidity,bme680.pressure]

    def get_veml7700_telematry(self):
        veml7700 = adafruit_veml7700.VEML7700(self.i2c)
        logging.debug("Ambient light:%d, Lux: %d",veml7700.light,veml7700.lux)
        return [veml7700.light,veml7700.lux]



    def write_telematry_csv(self):
        with open(TELE_FILE, 'a', encoding='UTF8', newline='') as f:    
            now = datetime.now() # current date and time
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")
            bme680_list = self.get_bme680_telematry()
            veml7700_list = self.get_veml7700_telematry()
            writer = csv.writer(f)
            row =[]
            row.append(date_time) 
            row = row + bme680_list + veml7700_list
            writer.writerow(row)

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("telematry.log"),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    quit()


