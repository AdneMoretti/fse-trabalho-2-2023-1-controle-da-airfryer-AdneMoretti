import termios
import os
from modbus import send_data, receive_data

uart0_filestream = -1

def config_uart():
    global uart0_filestream
    uart0_filestream = os.open("/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)
    if uart0_filestream == -1:
        print("Erro - Não foi possível iniciar a UART.")
    else:
        print("UART inicializada!")

    options = termios.tcgetattr(uart0_filestream)
    options[2] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD 
    options[0] = termios.IGNPAR 
    options[1] = 0
    options[3] = 0 
    termios.tcflush(uart0_filestream, termios.TCIFLUSH) 
    termios.tcsetattr(uart0_filestream, termios.TCSANOW, options)
    return uart0_filestream

# Faz a leitura dos comandos de usuário
def read_commands(): 
    send_data('0x23', '0xC3')
    command = receive_data()
    return command

def close_uart(): 
    global uart0_filestream
    os.close(uart0_filestream)