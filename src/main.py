import gpio
from modbus import ModBusFunction
from states import states_airfyer
import time, signal
from pid import pid_controle
from commands import Commands
import i2c
import sys

time_start = -1
modbus = ModBusFunction()
commands = Commands()
def alarm_handler(signum, frame): 
    global time_start
    time.sleep(1)
    response_user = commands.read_commands()
    code = str(hex(response_user))
    print(code)
    # Comando para ligar a AirFryer
    if(code == '0x1'):
        commands.send_system_state(1)
        print("forno ligado")
    # Comando para desligar a AirFryer
    elif(code == '0x2'):
        commands.send_system_state(0)
        gpio.stop()
        i2c.clean_lcd()
    # Inicia aquecimento
    elif(code == '0x3'):
        print("entrei aqui")
        commands.send_function_state(1)
        print(states_airfyer["function_state"])
    # Cancela processo    
    elif(code == '0x4'):
        commands.send_function_state(0)
    # Tempo + : adiciona 1 minuto ao timer
    elif(code == '0x5'):
        states_airfyer["time_counter"] += 1
    # Tempo - : diminui 1 minuto ao timer
    elif(code == '0x6'):
        states_airfyer["time_counter"] -= 1
    # Menu : aciona o modo de alimentos pré-programados
    elif(code == '0x7'):
        commands.send_control_mode(1)

    if states_airfyer["system_state"] == 1 and states_airfyer["function_state"] == 1: 
        temperature_control()
        i2c.show_states()
    if states_airfyer["system_state"] == 1 and states_airfyer["function_state"] == 0: 
        i2c.show_mode()

def temperature_control(): 
    if states_airfyer["control_mode"] == 0: 
        commands.ask_reference_temperature()
        commands.send_time_counter()
    else: 
        commands.send_reference_signal(30.0)
        commands.send_time_counter()
    if states_airfyer["intern_temperature"] == states_airfyer["reference_temperature"]: 
        time_start = time.time()
    if(time_start!=-1): 
        now = time.time()
        states_airfyer["time_counter"] = round(((now - time_start)/ 60), 2)
    time.sleep(0.1)
    modbus.receive_data()

    commands.ask_intern_temperature()
    time.sleep(0.1)
    modbus.receive_data()

    control = pid_controle()
    commands.send_control_signal()
    print(control)
    print(states_airfyer["control_signal"])
    gpio.start()
    gpio.change_duty_cycle(control)

def main(): 
    gpio.gpio_init()
    modbus.config_uart()
    try:
        if(sys.argv == 'DASH'):
            while True: 
                signal.signal(signal.SIGALRM, alarm_handler)
                signal.alarm(1)
                signal.pause()
        else: 
            while True: 
                signal.signal(signal.SIGALRM, alarm_handler)
                signal.alarm(1)
                signal.pause()
    except KeyboardInterrupt:
        gpio.stop()
        commands.send_function_state(0)
        commands.send_system_state(0)
        commands.send_control_mode(0)
        i2c.clean_lcd()
        gpio.gpio_clean()
 
main()
