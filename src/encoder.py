import RPi.GPIO as GPIO
from time import sleep
import time
from states import states_airfyer
from control import temperature_control
import i2c

temp = 25
time_manual = 1
state_manual = 1
last_clicked = 0
now_click = 0

clk = 16
dt = 20
sw = 21


def init():
    global pwm_resistor, pwm_fan

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sw, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(clk, GPIO.RISING, callback=rotation_decode, bouncetime=10)
    GPIO.add_event_detect(sw, GPIO.FALLING, bouncetime=100)
    return

def rotation_decode(clk):
    global temp, time_manual, state_manual
    sleep(0.002)
    change_clk = GPIO.input(clk)
    change_dt = GPIO.input(dt)
    if (change_clk == 1) and (change_dt == 0):
        if (state_manual == 1):
            states_airfyer["control_mode"] = 1

        if (state_manual == 2 and states_airfyer["control_mode"] == 0):
            states_airfyer["reference_temperature"] += 5
            print ("TEMP -> ", states_airfyer["reference_temperature"])

        if (state_manual == 3 and states_airfyer["control_mode"] == 0):
            states_airfyer["time_counter"] += 1
            print ("TIME -> ", states_airfyer["time_counter"])

        if (state_manual == 2 and states_airfyer["control_mode"] == 1):
            states_airfyer["reference_temperature"] = 30.0
            states_airfyer["time_counter"] = 2

        while change_dt == 0:
            change_dt = GPIO.input(dt)
        while change_dt == 1:
            change_dt = GPIO.input(dt)

        return

    elif (change_clk == 1) and (change_dt == 1):
        if (state_manual == 1):
            states_airfyer["control_mode"] = 0

        if (state_manual == 2 and states_airfyer["control_mode"] == 0):
            states_airfyer["reference_temperature"] -= 5
            print ("TEMP -> ", states_airfyer["reference_temperature"])

        if (state_manual == 3 and states_airfyer["control_mode"] == 0):
            states_airfyer["time_counter"] -= 1
            print ("TIME -> ", states_airfyer["time_counter"])
        # Segunda fase do automatico
        if (state_manual == 2 and states_airfyer["control_mode"] == 1):
           states_airfyer["reference_temperature"] = 30.0
           states_airfyer["time_counter"] = 2

        while change_clk == 1:
            change_clk = GPIO.input(clk)
        return
    else:
        return

def check_button():
    global sw, last_clicked, now_click, qnt_button
    
    if (GPIO.event_detected(sw)):
        now_click = time.time()
        if (now_click - last_clicked <= 0.5):
            last_clicked = now_click
            qnt_button = 2
        else:
            last_clicked = now_click
            qnt_button = 1

    sleep(0.2)
    return 0

def start():
    temperature_control()

def show_value():
    global temp, time_manual, state_manual
    if(state_manual == 1):
        print("Automatico ->")
        print("Manual <-")
    elif (state_manual == 2 and states_airfyer["control_mode"] == 0):
        print ("TEMP -> ", states_airfyer['reference_temperature'])
    elif (state_manual == 2 and states_airfyer["control_mode"] == 0):
        print ("TIME -> ", states_airfyer['time_counter'])
    elif(state_manual == 2 and states_airfyer["control_mode"] == 1): 
        i2c.show_lcd_menu()

def main():
    global state_manual, qnt_button

    try:
        init()
        show_value()
        while True:
            qnt_button = check_button()
            if (qnt_button == 1):
                print("apertei uma vez o botao")
                state_manual += 1
                show_value()
            elif (qnt_button == 2):
                state_manual -= 2
                print("apertei duas vez o botao")
                show_value()
            elif (state_manual == 4 and states_airfyer["control_mode"] == 0) or (state_manual == 3 and states_airfyer["control_mode"] == 1):
                start()
            sleep(0.2)

    except KeyboardInterrupt:
        GPIO.cleanup()
