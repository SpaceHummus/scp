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
from gpiozero import CPUTemperature
from gpiozero import LoadAverage
import file_maintenance
import os

TELE_FILE = 'telematry.csv'


class TelematryHandler:
    i2c = None
    current_logic_state_name = ""

    def __init__(self):
        self.i2c = board.I2C()
        
    
    ############# Functions for Telemetry Gathering ##########################################################
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

    def get_veml7700_telemetry(self, chunnel = None): #chunnel can be 1 or 2
        try:
            if chunnel:
                self.swith_i2c_chunnel(chunnel)

            veml7700 = adafruit_veml7700.VEML7700(self.i2c)
            logging.debug("Ambient light:%d, Lux: %d || on chunnel: %d",
                          veml7700.light, veml7700.lux, chunnel)
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
            time.sleep(0.05)
            logging.debug(
                "Current: %.4f mA Voltage: %.4f V Power: %.4f mW"
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
    
    def get_raspberry_telemetry(self):
        try:
            cpu_temp = CPUTemperature()
            cpu_load = int(LoadAverage(minutes=1).load_average*100)
            ###########
            used_space = file_maintenance.check_used_space(file_maintenance.IMAGES_PATH)
            logging.debug("CPUTemperature:%d, cpu_load: %d %% used_space: %d ", cpu_temp.temperature, cpu_load, used_space)
            return [cpu_temp.temperature, cpu_load, used_space]
        except Exception as e:
            logging.error(
                f"error while reading from the raspberry telemetry: \n{e}"
            )
            return ['N/A cpu_temp', 'N/A cpu_load', 'N/A used_space']

    ############# END Functions for Telemetry Gathering ######################################################
    ############# Functions I2C Management ###################################################################
    def swith_i2c_chunnel(self,chunnel):
        switch_addres =0x73 
        bus = smbus.SMBus(1)
        bus.write_byte(switch_addres ,chunnel)
        
    @staticmethod
    def read_i2c_value(i2c_address, bus_addr):
        bus = smbus.SMBus(1)
        bus.write_byte(i2c_address, bus_addr)
        value = bus.read_byte(i2c_address)
        return value
        
    ############# Functions for Writing Telemetry to File ####################################################
    
    # Starts a telemetry csv file if it doesn't exist and place header line.
    def start_telemetry_csv_file(self):
        if os.path.exists(TELE_FILE):
            # File exist, no need to do anything
            return
    
        # Telemetry file doesn't exist, make sure to open a new one and write header
        with open(TELE_FILE, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date&Time','Logic State',
                'BME680_Temperature[C]',
                'BME680_Gas[Ohm]',
                'BME680_Humidity[%]',
                'BME680_Pressure[hPa]',
                'VEML7700_1_Raw_Value[N/A]',
                'VEML7700_1_Lux[Lux]',
                'VEML7700_2_Raw_Value[N/A]',
                'VEML7700_2_Lux[Lux]',
                'INA260_Current[mA]',
                'INA260_Voltage[v]',
                'INA260_Power[mW]',
                'A2D_0[V]','A2D_1[V]','A2D_2[V]','A2D_3[V]',
                'RPI_CPU_Temperature[C]',
                'RPI_CPU_Load[%]',
                'RPI_Used_Space[%]',
                ])
                

    ############# High Level Functionality ###################################################################
    
    # Gather all telemetry and write it to CSV file
    def write_telemetry_csv(self):
        with open(TELE_FILE, 'a', encoding='UTF8', newline='') as f:
            
            # Gather all telemetry
            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")
            bme680_list, veml7700_list_1, veml7700_list_2, ina260_list, a2d_list , rasp_list = self.read_all_telemetry()

            writer = csv.writer(f)
            row = list()
            row.append(date_time)
            row.append(self.current_logic_state_name)
            row = row + bme680_list + veml7700_list_1 + veml7700_list_2 + ina260_list + a2d_list + rasp_list

            writer.writerow(row)
            
    def set_current_logic_state_name(self,new_logic_state_name):
        self.current_logic_state_name = new_logic_state_name

    def read_all_telemetry(self):
        bme680_list = self.get_bme680_telemetry()
        veml7700_list_1 = self.get_veml7700_telemetry(0x1)
        veml7700_list_2 = self.get_veml7700_telemetry(0x2)
        ina260_list = self.get_ina260_telemetry()
        a2d_list = self.get_a2d_telemetry()
        raspberry_list = self.get_raspberry_telemetry()
        return bme680_list,veml7700_list_1,veml7700_list_2,ina260_list,a2d_list,raspberry_list


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("telematry.log"),
            logging.StreamHandler()
        ]
    )


def read_all_telemetry():
    tm = TelematryHandler()
    while True:
        print(tm.read_all_telemetry())
        time.sleep(0.05)



if __name__ == "__main__":
    tel = TelematryHandler()
    data = tel.get_raspberry_telemetry()
    print(data)