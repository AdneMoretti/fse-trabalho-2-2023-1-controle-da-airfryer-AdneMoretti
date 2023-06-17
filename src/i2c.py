import time
from bmp280 import BMP280
from smbus import SMBus
import I2C_LCD_driver as I2C_LCD_driver
from states import states_airfyer

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)
lcdi2c = I2C_LCD_driver.lcd()

def get_temperature(): 
    temperature = bmp280.get_temperature()
    return temperature

def show_lcd_menu(): 
    lcdi2c.lcd_clear()
    lcdi2c.lcd_display_string("Frango (5'', 35ºC)", 1,0)
    lcdi2c.lcd_display_string("Mandioca (2'', 40ºC)", 2,0)

def clean_lcd(): 
    lcdi2c.lcd_clear()

def show_mode():
    clean_lcd()
    if states_airfyer["control_mode"]: 
        lcdi2c.lcd_display_string("Modo: Automático", 1,0)
    else: 
        lcdi2c.lcd_display_string("Modo: Manual", 1 ,0)

def show_states(): 
    clean_lcd()
    temperature = round(states_airfyer["intern_temperature"], 2)
    lcdi2c.lcd_display_string(f'TI:{temperature}', 1, 0)
    lcdi2c.lcd_display_string(f'TC:{int(states_airfyer["time_counter"])}', 1, 9)
    lcdi2c.lcd_display_string(f'TR:{int(states_airfyer["reference_temperature"])}', 2, 0)
    if states_airfyer["control_mode"]: 
        lcdi2c.lcd_display_string("Automático", 2,7)
    else: 
        lcdi2c.lcd_display_string("Manual", 2 ,7)


