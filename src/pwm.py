# Módulo de configutação da GPIO
from RPi import GPIO
from time import sleep
from states import states_airfyer
import math

# Variáveis globais para cada pino a ser utilizado na GPIO
temperature = True
clk = 16
dt = 20
sw = 21
resistor = 23
ventoinha = 24
pwm_resistor = 0
pwm_fan = 0

def pwm_init():
    global pwm_resistor, pwm_fan

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(resistor, GPIO.OUT)
    GPIO.setup(ventoinha, GPIO.OUT)

    pwm_resistor = GPIO.PWM(resistor, 200)
    pwm_fan = GPIO.PWM(ventoinha, 200)

def change_duty_cycle(control:int):
    if control>0:
        pwm_resistor.ChangeDutyCycle(control)
        pwm_fan.ChangeDutyCycle(0)
        states_airfyer["resistor_acionamento"] = control
        states_airfyer["fan_acionamento"] = 0

    elif control < -40:
        control = abs(control)
        pwm_resistor.ChangeDutyCycle(0)
        pwm_fan.ChangeDutyCycle(control)
        states_airfyer["resistor_acionamento"] = 0
        states_airfyer["fan_acionamento"] = control
    
    else: 
        pwm_resistor.ChangeDutyCycle(0)
        pwm_fan.ChangeDutyCycle(40)
        states_airfyer["resistor_acionamento"] = 0
        states_airfyer["fan_acionamento"] = 40

def stop():
    pwm_resistor.stop()
    pwm_fan.stop()  

def start():
    pwm_resistor.start(0)
    pwm_fan.start(0)

def gpio_clean(): 
    GPIO.cleanup()