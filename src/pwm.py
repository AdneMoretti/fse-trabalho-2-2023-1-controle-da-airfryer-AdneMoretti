# Módulo de configutação da GPIO
from RPi import GPIO
from time import sleep
from states import states_airfyer

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

    elif control<=-40:
        pwm_resistor.ChangeDutyCycle(0)
        pwm_fan.ChangeDutyCycle(40)
        states_airfyer["resistor_acionamento"] = 0
        states_airfyer["fan_acionamento"] = 40
    
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
# TO DO
# Botão do encoder e leitura da temperatura/tempo
# def read_sw_encoder(): 
#     if(GPIO.event_detected(sw, GPIO.RISING)):
#         temperature = not temperature
#         sleep(0.01)
#         if(temperature): 
#             read_clock()
#         else: 
#             read_clock()

# def read_clock(): 
#     counter = 0
#     clkLastState = GPIO.input(clk)

#     try:
#         while True:
#             clkState = GPIO.input(clk)
#             dtState = GPIO.input(dt)
#             if clkState != clkLastState:
#                 sleep(0.1)
#                 if dtState != clkState:
#                     counter += 1
#                 else:
#                     counter -= 1
#                 print(counter)
#             clkLastState = clkState
#     finally:
#         GPIO.cleanup()

def gpio_clean(): 
    GPIO.cleanup()