from GPIO import gpio_init, activate_resistor
from modbus import ModBusFunction
from states import STATES_AIRFYER
import time

modbus = ModBusFunction()
def alarm_handler(): 
    while(True): 
        time.sleep(1)
        response_user = modbus.read_commands()
        print(response_user)
        code = str(hex(response_user))
        print(code)
        # Comando para ligar a AirFryer
        if(code == '0x1'):
            STATES_AIRFYER["system_state"] = 1
            modbus.send_integer('0xD3', STATES_AIRFYER["system_state"])
        # Comando para desligar a AirFryer
        elif(code == '0x2'):
            STATES_AIRFYER["system_state"] = 0
            modbus.send_integer('0xD3', STATES_AIRFYER["system_state"])
        # Inicia aquecimento
        elif(response_user == '0x03'):
            pass
        # Cancela processo    
        elif(response_user == '0x04'):
            pass
        # Tempo + : adiciona 1 minuto ao timer
        elif(response_user == '0x05'):
            pass
        # Tempo - : adiciona 1 minuto ao timer
        elif(response_user == '0x06'):
            pass
        # Menu : aciona o modo de alimentos pré-programados
        elif(response_user == '0x07'):
            pass
        else: 
            continue



def main(): 
    gpio_init()
    modbus.config_uart()
    alarm_handler()
    # modbus.send_integer('0xD3', 0)
    # modbus.send_float('0xD2', 12.2)
    # # time.sleep(1)
    # # modbus.receive_data()


    # modbus.ask_value('0xC2')
    # time.sleep(1)
    # modbus.receive_data()
    # send_data('0x16', '0xD2', uart0_filestream)
    # signal.signal(signal.SIGALRM, alarm_handler)

    # signal.alarm(0.2)  

main()