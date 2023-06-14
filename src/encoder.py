import RPi.GPIO as GPIO
from time import sleep
import time
from states import states_airfyer

temp = 25
time_manual = 1
state_manual = 1
last_clicked = 0

sw = 23
clk = 24  
dt = 25


def init():
    GPIO.add_event_detect(clk, GPIO.RISING, callback=rotation_decode, bouncetime=10)
    return

def rotation_decode(clk):
    global temp, time_manual, state_manual
    sleep(0.002)
    Switch_clk = GPIO.input(clk)
    Switch_dt = GPIO.input(dt)

    if (Switch_clk == 1) and (Switch_dt == 0):
        if (state_manual == 1):
            states_airfyer["control_mode"] = 1
        if (state_manual == 2 and states_airfyer["control_mode"] == 0):
            temp += 5
            print ("TEMP -> ", temp)
        if (state_manual == 3 and states_airfyer["control_mode"] == 0):
            time_manual += 1
            print ("TIME -> ", time_manual)
        while Switch_dt == 0:
            Switch_dt = GPIO.input(dt)
        while Switch_dt == 1:
            Switch_dt = GPIO.input(dt)
        return

    elif (Switch_clk == 1) and (Switch_dt == 1):
        if (state_manual == 1):
            states_airfyer["control_mode"] = 0
        if (state_manual == 2 and states_airfyer["control_mode"] == 0):
            temp -= 5
            print ("TEMP -> ", temp)
        if (state_manual == 3 and states_airfyer["control_mode"] == 0):
            time_manual -= 1
            print ("TIME -> ", time_manual)
        if (state_manual == 2 and states_airfyer["control_mode"] == 0):
            temp -= 5
            print ("TEMP -> ", temp)
        # while Switch_clk == 1:
        #     Switch_clk = GPIO.input(clk)
        return
    else:
        return


def check_button():
    global sw, last_clicked
    
    if (GPIO.event_detected(sw)):
        current_time = time.time()
        if (current_time - last_clicked <= 2):
            last_clicked = current_time
            return 2
        else:
            last_clicked = current_time
            return 1
    return 0

def show_state():
    global state_manual, time_manual, temp
    
    print(f"Tempo restante: {time_manual}\nTemperatura Atual: 25\nTemperatura referente: {temp}")

def show_value():
    global temp, time_manual, state_manual
    if (state_manual == 1):
        print ("TEMP -> ", temp)
    if (state_manual == 2):
        print ("TIME -> ", time_manual)

def main():
    global state_manual

    try:
        init()
        while True:
            if (check_button() == 1):
                state_manual += 1
                show_value()
            elif (check_button() == 2):
                state_manual -= 1
                show_value()
            elif (state_manual == 4 and states_airfyer["control_mode"] == 0 or state_manual == 3 and states_airfyer["control_mode"] == 1):
                start()
            sleep(0.2)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '_main_':
    main()