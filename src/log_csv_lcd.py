import csv
import threading
from states import states_airfyer
from datetime import now
import i2c
import signal

class Log: 
    def __init__(self): 
        self.archive_name = 'dados.csv'

    def timer(self): 
        while True: 
            signal.signal(signal.SIGALRM, self.start)
            signal.alarm(0.2)
            signal.pause()

    def log_init(self): 
        thread = threading.Thread(target=self.timer, args=())
        thread.start()
    
    def start(self, signum, frame): 
        self.write()
        self.update_lcd()

    def write(self): 
        with open(self.archive_name, mode='w', newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)  # Cria o escritor CSV

        escritor.writerow(f"{now()}, Intern Temp. : {states_airfyer['intern_temperature']} ºC, Room Temp : {states_airfyer['room_temperature']} ºC, Reference Temp. : {states_airfyer['reference_temperature']} ºC, Val. Acionamento do Resistor : {states_airfyer['resistor_acionamento']} %, Val. Acionamento da Ventoinha = {states_airfyer['fan_acionamento']} % \n")

    def update_lcd(self): 
        if states_airfyer['system_state'] and states_airfyer['function_state']: 
            i2c.clean_lcd()
            i2c.show_states()
        elif states_airfyer['system_state'] and not states_airfyer['function_state']: 
            i2c.clean_lcd()
            i2c.mode()
        else: 
            i2c.clean_lcd()

