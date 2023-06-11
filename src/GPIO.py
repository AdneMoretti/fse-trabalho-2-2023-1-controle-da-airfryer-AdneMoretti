# Módulo de configutação da GPIO
from RPi import GPIO
from time import sleep

# Variáveis globais para cada pino a ser utilizado na GPIO
temperature = True
clk = 16
dt = 20
sw = 21
resistor = 23
ventoinha = 24
pwm_resistor = 0
pwm_fan = 0

def gpio_init():
    global pwm_resistor, pwm_ventoinha

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sw, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(resistor, GPIO.OUT)
    GPIO.setup(ventoinha, GPIO.OUT)

    pwm_resistor = GPIO.PWM(resistor, 1000)
    pwm_fan = GPIO.PWM(ventoinha, 1000)
    pwm_resistor.start(0)
    pwm_fan.start(0)

def activate_fan(control_signal): 
    if(control_signal < 0 and control_signal > -40): 
        control_signal = 40

    pwm_fan.ChangeDutyCycle(control_signal)


def desactivate_ventoinha(): 
    pwm_fan.ChangeDutyCycle(0)


def activate_resistor(control_signal): 
    pwm_resistor.ChangeDutyCycle(control_signal)


def desactivate_resistor(): 
    pwm_resistor.ChangeDutyCycle(0)


# TO DO
# Botão do encoder e leitura da temperatura/tempo
def read_sw_encoder(): 
    if(GPIO.event_detected(sw, GPIO.RISING)):
        temperature = not temperature
        sleep(0.01)
        if(temperature): 
            read_clock()
        else: 
            read_clock()

def read_clock(): 
    counter = 0
    clkLastState = GPIO.input(clk)

    try:
        while True:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                sleep(0.1)
                if dtState != clkState:
                    counter += 1
                else:
                    counter -= 1
                print(counter)
            clkLastState = clkState
    finally:
        GPIO.cleanup()