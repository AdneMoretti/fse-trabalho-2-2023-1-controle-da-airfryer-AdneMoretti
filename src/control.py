import signal, threading, time, pwm
from states import states_airfyer
from modbus import ModBusFunction
from commands import Commands
from log_csv_lcd import Log
from pid import PID

modbus = ModBusFunction()
commands = Commands()
pid = PID()
log = Log()
_control_thread = -1
running = 0
_stop_thread = 0


def timer(): 
    while not _stop_thread: 
        time.sleep(1)
        temperature_control()

def control_thread(): 
    global _control_thread
    _control_thread = threading.Thread(target=timer, args=())
    _control_thread.start()


def temperature_control(): 
    global running
    if states_airfyer["function_state"] and states_airfyer["system_state"]: 
        commands.send_room_temperature()
        if states_airfyer["control_mode"] == 0: 
            commands.ask_reference_temperature()
        else: 
            commands.send_reference_signal(35.0)
            
        commands.ask_intern_temperature()
        print("TEMPERATURE", states_airfyer["reference_temperature"])
        commands.send_time_counter()
        time.sleep(0.1)
        modbus.receive_data()
        if states_airfyer["intern_temperature"] >= states_airfyer["reference_temperature"] - 0.2 and states_airfyer["intern_temperature"] <= states_airfyer["reference_temperature"] + 0.2: 
            running = True

        if running: 
            states_airfyer["time_counter"] -= 0.0166667
            if(states_airfyer["time_counter"] < 0): 
                states_airfyer["time_counter"] = 0

        if(states_airfyer["time_counter"] == 0): 
            running = False
            states_airfyer["reference_temperature"] = states_airfyer["room_temperature"]
            commands.send_reference_signal(states_airfyer["room_temperature"])
            time.sleep(0.1)
            modbus.receive_data()

        states_airfyer["control_signal"] = int(pid.pid_controle())
        print("CONTROL", states_airfyer["control_signal"])
        commands.send_control_signal()
        pwm.start()
        pwm.change_duty_cycle(states_airfyer["control_signal"])
    
    log.start()


def stop(): 
    global _stop_thread
    _stop_thread = 1