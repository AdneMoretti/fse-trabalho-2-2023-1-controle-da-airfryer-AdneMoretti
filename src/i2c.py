import time
from bmp280 import BMP280
from smbus2 import SMBus

# try:
#     from smbus2 import SMBus
# except ImportError:
#     from smbus import SMBus

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


def get_temperature(): 
    temperature = bmp280.get_temperature()
    
# while True:
#     temperature = bmp280.get_temperature()
#     pressure = bmp280.get_pressure()
#     print('{:05.2f}*C {:05.2f}hPa'.format(temperature, pressure))
#     time.sleep(1)