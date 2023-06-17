from modbus import ModBusFunction
from states import states_airfyer
from i2c import get_temperature
import time

modbus = ModBusFunction()
class Commands: 
    def __init__(self): 
        self.subcode_intern_temperature = '0xC1'
        self.subcode_reference_temperature = '0xC2'
        self.subcode_command = '0xC3'
        self.subode_send_state = '0xD3'
        self.subcode_control_signal = '0xD1'
        self.subcode_reference_signal = '0xD2'
        self.subcode_control_mode = '0xD4'
        self.subcode_funcition_state = '0xD5'
        self.subcode_room_temperature = '0xD6'
        self.subcode_time_counter = '0xD7'
        self.subcode_string = '0xD8'

    def read_commands(self):
        modbus.ask_value('0xC3')
        time.sleep(0.1)
        command = modbus.receive_data()
        return command
    
    def send_system_state(self, state: int): 
        states_airfyer["system_state"] = state
        modbus.send_integer(self.subode_send_state, states_airfyer["system_state"])

    def ask_intern_temperature(self): 
        modbus.ask_value(self.subcode_intern_temperature)
        time.sleep(0.1)
        modbus.receive_data()

    def ask_reference_temperature(self): 
        modbus.ask_value(self.subcode_reference_temperature)
        time.sleep(0.1)
        modbus.receive_data()

    def send_function_state(self, state: int): 
        states_airfyer["function_state"] = state
        modbus.send_integer(self.subcode_funcition_state, states_airfyer["function_state"])

    def send_string(self, message): 
        modbus.send_str(self.subcode_string, message)

    def send_room_temperature(self): 
        states_airfyer["room_temperature"] = get_temperature()
        modbus.send_float(self.subcode_room_temperature, states_airfyer["room_temperature"])
        time.sleep(0.1)
        modbus.receive_data()

    # TO DO 
    def send_reference_signal(self, temperature): 
        states_airfyer["reference_temperature"] = temperature
        modbus.send_float(self.subcode_reference_signal, temperature)

    def send_control_mode(self, mode): 
        states_airfyer["control_mode"] = mode
        modbus.send_integer(self.subcode_control_mode, states_airfyer["control_mode"])

    def send_time_counter(self): 
        modbus.send_control(self.subcode_time_counter, int(states_airfyer["time_counter"]))
        time.sleep(0.1)
        modbus.receive_data()

    def send_control_signal(self): 
        modbus.send_control(self.subcode_control_signal,  states_airfyer["control_signal"])