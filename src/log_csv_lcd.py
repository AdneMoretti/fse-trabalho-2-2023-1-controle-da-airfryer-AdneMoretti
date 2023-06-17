import csv
import threading
from states import states_airfyer
from datetime import datetime
import i2c
import time

class Log: 
    def __init__(self): 
        self.archive_name = 'dados.csv'

    # def timer(self): 
    #     while True: 
    #         time.sleep(1)
    #     # Chama o manipulador do alarme
    #         self.start()

    # def log_init(self): 
    #     thread = threading.Thread(target=self.timer, args=())
    #     thread.start()
    
    def start(self): 
        self.write()
        self.update_lcd()

    def write(self): 
        with open(self.archive_name, mode='w', newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)  # Cria o escritor CSV

            # escritor.writerow(f"{datetime.now()}, Intern Temp. : {states_airfyer['intern_temperature']} ºC, Room Temp : {states_airfyer['room_temperature']} ºC, Reference Temp. : {states_airfyer['reference_temperature']} ºC, Val. Acionamento do Resistor : {states_airfyer['resistor_acionamento']} %, Val. Acionamento da Ventoinha = {states_airfyer['fan_acionamento']} % \n")
            row = [
            datetime.now(),
                f"Intern Temp. : {states_airfyer['intern_temperature']} ºC",
                f"Room Temp : {states_airfyer['room_temperature']} ºC",
                f"Reference Temp. : {states_airfyer['reference_temperature']} ºC",
                f"Val. Acionamento do Resistor : {states_airfyer['resistor_acionamento']} %",
                f"Val. Acionamento da Ventoinha = {states_airfyer['fan_acionamento']} %"
            ]
            escritor.writerow(row)
    def update_lcd(self): 
        if states_airfyer['system_state'] and states_airfyer['function_state']: 
            i2c.clean_lcd()
            i2c.show_states()
        elif states_airfyer['system_state'] and not states_airfyer['function_state']: 
            i2c.clean_lcd()
            i2c.show_mode()
        else: 
            i2c.clean_lcd()

