from GPIO import gpio_init, activate_resistor
from modbus import ModBusFunction
from states import STATES_AIRFYER
import time

def alarm_handler(): 
    while(True): 
        response_user = read_commands()
        # Comando para ligar a AirFryer
        if(response_user == '0x01'):
            pass
        # Comando para desligar a AirFryer
        elif(response_user == '0x02'):
            pass
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


def main(): 
    gpio_init()
    modbus = ModBusFunction()
    modbus.config_uart()
    modbus.send_integer('0xD3', 0)
    modbus.send_float('0xD2', 12.2)
    # time.sleep(1)
    # modbus.receive_data()

    modbus.ask_value('0xC1')
    time.sleep(1)
    modbus.receive_data()
    activate_resistor(100)
    # send_data('0x16', '0xD2', uart0_filestream)
    # signal.signal(signal.SIGALRM, alarm_handler)

    # signal.alarm(0.2)  

main()