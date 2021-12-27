import board
import adafruit_bme680
import time
import busio
import adafruit_veml7700
from datetime import datetime
import csv
import logging
import adafruit_ina260
import smbus

TELE_FILE = 'telematry.csv'


class TelematryHandler:
    i2c = None

    def __init__(self):
        self.i2c = board.I2C()

    def get_bme680_telemetry(self):
        try:
            bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
            logging.debug("Temperature:%d, Gas: %d ohms, Humidity: %d, Pressure: %d hPa", bme680.temperature,
                          bme680.gas,
                          bme680.humidity, bme680.pressure)
            return [bme680.temperature, bme680.gas, bme680.humidity, bme680.pressure]
        except Exception as e:
            logging.error(
                f"error while reading from the bme680: \n{e}"
            )
            return ['N/A temperature', 'N/A gas', 'N/A humidity', 'N/A pressure']

    def get_veml7700_telemetry(self):
        try:
            veml7700 = adafruit_veml7700.VEML7700(self.i2c)
            logging.debug("Ambient light:%d, Lux: %d",
                          veml7700.light, veml7700.lux)
            return [veml7700.light, veml7700.lux]

        except Exception as e:
            logging.error(
                f"error while reading from the veml7700: \n{e}"
            )
            return ['N/A light', 'N/A lux']

    def get_ina260_telemetry(self):
        try:
            ina260 = adafruit_ina260.INA260(self.i2c)
            ina260.mode = adafruit_ina260.Mode.CONTINUOUS
            logging.debug(
                "Current: %.4f mA Voltage: %.4f V Power%.4f mW"
                % (ina260.current, ina260.voltage, ina260.power)
            )
            return [ina260.current, ina260.voltage, ina260.power]
        except Exception as e:
            logging.error(
                f"error while reading from the ina260: \n{e}"
            )
            return ['N/A current', 'N/A voltage', 'N/A power']

    def get_a2d_telemetry(self):
        a2d_address = 0x48
        bus_address = [0x40, 0x41, 0x42, 0x43]
        try:
            i2c_read = [self.read_i2c_value(a2d_address, bus_addres)
                        for bus_addres in bus_address]
            logging.debug(f"A2D returned values: {i2c_read}")
            return i2c_read

        except Exception as e:
            logging.error(f"error reading from A2D i2c channel: \n{e}")
            return [f"N/A A2D-{b}" for b in range(4)]

    def write_telemetry_csv(self):
        with open(TELE_FILE, 'a', encoding='UTF8', newline='') as f:
            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")

            bme680_list = self.get_bme680_telemetry()
            veml7700_list = self.get_veml7700_telemetry()
            ina260_list = self.get_ina260_telemetry()
            a2d_list = self.get_a2d_telemetry()

            writer = csv.writer(f)
            row = list()
            row.append(date_time)
            row = row + bme680_list + veml7700_list + ina260_list + a2d_list

            writer.writerow(row)

    @staticmethod
    def read_i2c_value(i2c_address, bus_addr):
        bus = smbus.SMBus(1)
        bus.write_byte(i2c_address, bus_addr)
        value = bus.read_byte(i2c_address)
        return value


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
