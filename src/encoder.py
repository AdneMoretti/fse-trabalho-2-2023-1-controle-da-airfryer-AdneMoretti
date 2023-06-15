import RPi.GPIO as GPIO
from time import sleep
import time
from states import states_airfyer

temp = 25
time_manual = 1
state_manual = 1
last_clicked = 0

clk = 16
dt = 20
sw = 21


def gpio_init():
    global pwm_resistor, pwm_fan

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sw, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def init():
    GPIO.add_event_detect(clk, GPIO.RISING, callback=rotation_decode, bouncetime=10)
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
            states_airfyer["reference_temperature"] -= 5
            print ("TEMP -> ", states_airfyer["reference_temperature"])

        if (state_manual == 3 and states_airfyer["control_mode"] == 0):
            states_airfyer["reference_time"] += 1
            print ("TIME -> ", states_airfyer["reference_time"])

        if (state_manual == 2 and states_airfyer["control_mode"] == 1):
            states_airfyer["reference_temperature"] = 30.0
            states_airfyer["reference_time"] = 2

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
            states_airfyer["reference_time"] -= 1
            print ("TIME -> ", states_airfyer["reference_time"])
        # Segunda fase do automatico
        if (state_manual == 2 and states_airfyer["control_mode"] == 1):
           states_airfyer["reference_temperature"] = 30.0
           states_airfyer["reference_time"] = 2

        while change_clk == 1:
            change_clk = GPIO.input(clk)
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

def start():
    global state_manual, time_manual, temp
    print("iniciando aquecimento")
    print(f"Tempo restante: {time_manual}\nTemperatura Atual: 25\nTemperatura referente: {temp}")

# def show_value():
#     global temp, time_manual, state_manual
#     if (state_manual == 1):
#         print ("TEMP -> ", temp)
#     if (state_manual == 2):
#         print ("TIME -> ", time_manual)

def show_menu(): 
    print("Linguica (2'', 30ºC)")
    print("Pao (3'', 40º))")

def main():
    global state_manual

    try:
        init()
        while True:
            if (check_button() == 1):
                state_manual += 1
            elif (check_button() == 2):
                state_manual -= 1
                show_menu()
            elif (state_manual == 4 and states_airfyer["control_mode"] == 0) or (state_manual == 3 and states_airfyer["control_mode"] == 1):

                start()
            sleep(0.2)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '_main_':
    main()