import RPi.GPIO as GPIO
from time import sleep
import time

temp = 25
time_manual = 1
state_manual = 1
last_clicked = 0

Enc_C = 21
Enc_A = 16  
Enc_B = 20


def init():
    print ("Rotary Encoder Test Program")
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Enc_A, GPIO.IN)
    GPIO.setup(Enc_B, GPIO.IN)
    GPIO.setup(Enc_C, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=10)
    GPIO.add_event_detect(Enc_C, GPIO.FALLING)
    return

def rotation_decode(Enc_A):
    global temp, time_manual, state_manual
    sleep(0.002)
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)

    if (Switch_A == 1) and (Switch_B == 0):
        if (state_manual == 1):
            temp += 5
            print ("TEMP -> ", temp)
        if (state_manual == 2):
            time_manual += 1
            print ("TIME -> ", time_manual)
        while Switch_B == 0:
            Switch_B = GPIO.input(Enc_B)
        while Switch_B == 1:
            Switch_B = GPIO.input(Enc_B)
        return

    elif (Switch_A == 1) and (Switch_B == 1):
        if (state_manual == 1):
            temp -= 5
            print ("TEMP -> ", temp)
        if (state_manual == 2):
            time_manual -= 1
            print ("TIME -> ", time_manual)
        while Switch_A == 1:
            Switch_A = GPIO.input(Enc_A)
        return
    else:
        return

def check_button():
    global Enc_C, last_clicked
    
    if (GPIO.event_detected(Enc_C)):
        current_time = time.time()
        if (current_time - last_clicked <= 0.7):
            return 2
        else:
            last_clicked = current_time
            return 1
    return 0

def start():
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
            elif (state_manual == 3):
                start()
            sleep(0.2)

    except KeyboardInterrupt:
        GPIO.cleanup()


# def check_button():
#     global sw, last_clicked, now_click, qnt_button
    
#     if (GPIO.event_detected(sw)):
#         now_click = time.time()
#         qnt_button = 1
#         print("clique")
#         print(now_click)
#         print(last_clicked)
#         sleep(0.5)
#         while(True): 
#             if (GPIO.event_detected(sw)):
#                 return 2
#             else: 
#                 now = time.time()
#                 if (now - now_click > 0.5):
#                     return 1

#         #     print("dois cliques")
#         #     last_clicked = now_click
#         #     qnt_button = 2
#         # else:
#         #     print("um clique")
#         #     last_clicked = now_click
#         #     qnt_button = 1

#     # sleep(0.2)
#     # return 0

main()