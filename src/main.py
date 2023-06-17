from modbus import ModBusFunction
from states import states_airfyer
from commands import Commands
import encoder, signal, pwm, i2c, sys, time
from control import control_thread, stop

modbus = ModBusFunction()
commands = Commands()

def alarm_dashboard(signum, frame): 
    global time_start
    response_user = commands.read_commands()
    code = str(hex(response_user))
    # Comando para ligar a AirFryer
    if(code == '0x1'): 
        commands.send_system_state(1)
    # Comando para desligar a AirFryer
    elif(code == '0x2'):
        commands.send_system_state(0)
        pwm.stop()
    # Inicia aquecimento
    elif(code == '0x3'):
        commands.send_function_state(1)
        print(states_airfyer["function_state"])
        time.sleep(0.1)
        modbus.receive_data()
    # Cancela processo    
    elif(code == '0x4'):
        commands.send_function_state(0)
        time.sleep(0.1)
        modbus.receive_data()
    # Tempo + : adiciona 1 minuto ao timer
    elif(code == '0x5'):
        states_airfyer["time_counter"] += 1
        commands.send_time_counter()
        time.sleep(0.1)
        modbus.receive_data()
    # Tempo - : diminui 1 minuto ao timer
    elif(code == '0x6'):
        states_airfyer["time_counter"] -= 1
        commands.send_time_counter()
        time.sleep(0.1)
        modbus.receive_data()
    # Menu : aciona o modo de alimentos pré-programados
    elif(code == '0x7'):
        if states_airfyer["control_mode"]: 
            state = 0
        else: 
            state = 1
            states_airfyer["time_counter"] = 3
            commands.send_time_counter()
            time.sleep(0.1)
            modbus.receive_data()
        commands.send_control_mode(state)
        time.sleep(0.1)
        modbus.receive_data()


def program_stop(): 
    pwm.stop()
    commands.send_function_state(0)
    commands.send_system_state(0)
    commands.send_control_mode(0)
    i2c.clean_lcd()
    pwm.gpio_clean()
    stop()

def start_encoder(): 
    encoder.gpio_init()

def main(): 
    pwm.pwm_init()
    modbus.config_uart()
    try:
        if sys.argv[1] == '1':
            control_thread()
            while True: 
                signal.signal(signal.SIGALRM, alarm_dashboard)
                intervalo = 0.2
                signal.setitimer(signal.ITIMER_REAL, intervalo)
                signal.pause()
            
        elif sys.argv[1] == '2': 
            start_encoder()
    except KeyboardInterrupt:
        program_stop()
 
main()
