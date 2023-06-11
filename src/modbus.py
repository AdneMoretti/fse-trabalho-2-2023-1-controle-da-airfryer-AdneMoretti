import termios
import os
from crc import calcula_crc
import os
import struct
from states import STATES_AIRFYER
import time


uart0_filestream = -1
class ModBusFunction():

    def __init__(self): 
        self.matricula = bytes([int('3', 16), int('1', 16), int('8', 16), int('1', 16)])
        self.destination = bytes([int('0x01', 16)])
        self.code_send = bytes([int('0x16', 16)])
        self.code_ask = bytes([int('0x23', 16)])

    def send_integer(self, subcode, message):
        message = bytes([int(str(message), 16)])
        subcode = bytes([int(subcode, 16)])
        commands = self.destination + self.code_send + subcode + self.matricula + message
        crc = struct.pack('H', calcula_crc(commands))
        self.send_data(bytes(commands+crc))

    def send_float(self, subcode, message): 
        message = struct.pack('f', message)
        subcode = bytes([int(subcode, 16)])
        commands = self.destination + self.code_send + subcode + self.matricula + message
        crc = struct.pack('H', calcula_crc(commands))
        self.send_data(bytes(commands+crc))

    def send_str(self, subcode, message): 
        message = message.encode('utf-8')
        subcode = bytes([int(subcode, 16)])
        commands = self.destination + self.code_send + subcode + self.matricula + message
        crc = struct.pack('H', calcula_crc(commands))
        self.send_data(bytes(commands+crc))

    def ask_value(self, subcode): 
        subcode = bytes([int(subcode, 16)])
        commands = self.destination + self.code_ask + subcode + self.matricula 
        crc = struct.pack('H', calcula_crc(commands))
        self.send_data(bytes(commands+crc))

    def config_uart(self):
        global uart0_filestream
        uart0_filestream = os.open("/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)
        if uart0_filestream == -1:
            print("Erro - Não foi possível iniciar a UART.")
        else:
            print("UART inicializada!")

        options = termios.tcgetattr(uart0_filestream)
        options[2] = options[2] & ~termios.HUPCL
        options[4] = termios.B9600
        options[5] = termios.B9600
        options[6][termios.VMIN] = 0
        options[6][termios.VTIME] = 0
        termios.tcflush(uart0_filestream, termios.TCIFLUSH) 
        termios.tcsetattr(uart0_filestream, termios.TCSANOW, options)

    # Faz a leitura dos comandos de usuário
    def close_uart(self): 
        global uart0_filestream
        os.close(uart0_filestream)

    def send_data(self, command): 
        global uart0_filestream
        if uart0_filestream != -1:
            # print(command)
            count = os.write(uart0_filestream, command)
            # print(count)
            if count < 0:
                print("UART TX error")

    def read_commands(self):
        self.ask_value('0xC3')
        time.sleep(1)
        command = self.receive_data()
        return command

    def get_message(self, message): 
        command = -1
        subcode = str(hex(message[2]))
        if subcode == '0xc1': 
            command = struct.unpack("f", message[3:7])[0]
            STATES_AIRFYER["intern_temperature"] = command
        elif subcode == '0xc2': 
            command = struct.unpack("f", message[3:7])[0]
            STATES_AIRFYER["intern_temperature"] = command
        elif subcode == '0xc3': 
            command = struct.unpack("i", message[3:7])[0]
        return command

    def receive_data(self):
        # Aqui necessário receber mensagem, verificar o crc recebido e ver se nao houve erro ou ruido
        if (uart0_filestream != -1):
            # Read up to 255 characters from the port if they are there
            rx_buffer = os.read(uart0_filestream, 255)
            print("rx_Bufefr", rx_buffer)
            rx_len = len(rx_buffer)
            print(rx_len)
            if rx_len < 0:
                print("Erro na leitura.\n")
                return -1

            elif rx_len == 0:
                print("Nenhum dado disponível.\n")
                return -1

            else:
                last_message = rx_buffer[-9:]
                print(last_message)
                if(len(last_message)==9):
                    # print(last_message)66
                    code = str(hex(last_message[1]))
                    print("code ", code)
                    received_crc = last_message[-2:]
                    data_bytes = last_message[:-2]

                    # # Calcular o CRC dos dados
                    calculated_crc = struct.pack('H',calcula_crc(data_bytes))
                    # Verificar se o CRC calculado corresponde ao CRC recebido
                    if calculated_crc == received_crc:
                        if(code == '0x23'): 
                            command = self.get_message(last_message)

                        # print("%i Bytes lidos: %s\n" % (rx_len, rx_buffer))
                        # Processar os dados aqui
                            return command
                    else:
                        print("Erro no CRC. Dados corrompidos.\n")
                        return -1
                




        # close_uart(uart0_filestream)


