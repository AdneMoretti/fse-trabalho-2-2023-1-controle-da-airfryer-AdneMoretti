from modbus import ModBusFunction
from states import states_airfyer
from commands import Commands
import encoder, signal, pwm, i2c, sys
from log_csv_lcd import Log
from control import control_thread


time_start = -1
modbus = ModBusFunction()
commands = Commands()
log = Log()

def alarm_dashboard(signum, frame): 
    global time_start
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
        pwm.stop()
    # Inicia aquecimento
    elif(code == '0x3'):
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


def program_stop(): 
    pwm.stop()
    commands.send_function_state(0)
    commands.send_system_state(0)
    commands.send_control_mode(0)
    i2c.clean_lcd()
    pwm.gpio_clean()

def encoder(): 
    pass

def main(): 
    pwm.pwm_init()
    modbus.config_uart()
    try:
        if sys.argv == 1:
            control_thread()
            log.log_init()
            while True: 
                signal.signal(signal.SIGALRM, alarm_dashboard)
                signal.alarm(0.2)
                signal.pause()
        elif sys.argv == 2: 
            encoder()
    except KeyboardInterrupt:
        program_stop()
 
main()
