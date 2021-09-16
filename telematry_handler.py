import board
import adafruit_bme680
import time
import busio
import adafruit_veml7700
from datetime import datetime
import csv
import logging


i2c = board.I2C()

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("telematry.log"),
            logging.StreamHandler()
        ]
    )    

def get_bme680_telematry():
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    logging.debug("Temperature:%d, Gas: %d ohms, Humidity: %d, Pressure: %d hPa",bme680.temperature,bme680.gas,bme680.humidity,bme680.pressure)
    return [bme680.temperature,bme680.gas,bme680.humidity,bme680.pressure]

def get_veml7700_telematry():
    veml7700 = adafruit_veml7700.VEML7700(i2c)
    logging.debug("Ambient light:%d, Lux: %d",veml7700.light,veml7700.lux)
    return [veml7700.light,veml7700.lux]


if __name__ == "__main__":
    setup_logging()
    with open('telematry.csv', 'a', encoding='UTF8', newline='') as f:

        while True:
            now = datetime.now() # current date and time
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")
            bme680_list = get_bme680_telematry()
            veml7700_list = get_veml7700_telematry()
            writer = csv.writer(f)
            row =[]
            row.append(date_time) 
            row = row + bme680_list + veml7700_list
            writer.writerow(row)
            time.sleep(10)



