import signal, threading, time, pwm
from states import states_airfyer
from modbus import ModBusFunction
from commands import Commands
from pid import pid_controle

modbus = ModBusFunction()
commands = Commands()

def timer(): 
    while True: 
        signal.signal(signal.SIGALRM, temperature_control)
        signal.alarm(0.5)
        signal.pause()

def control_thread(): 
    _control_thread = threading.Thread(target=timer, args=())
    _control_thread.start()

def temperature_control(): 
    if states_airfyer["function_state"] and states_airfyer["system_state"]: 
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
        pwm.start()
        pwm.change_duty_cycle(control)
