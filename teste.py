import threading, time
_stop_thread = False



def timer(): 
    global _stop_thread
    while not _stop_thread: 
        # signal.signal(signal.SIGALRM, temperature_control)
        # signal.alarm(0.5)
        # signal.pause()

            # Define o tempo de alarme para 200 m

        # Aguarda o tempo de alarme
        time.sleep(1)

        # Chama o manipulador do alarme
        temperature_control()
        _stop_thread = int(input())

def control_thread(): 
    global _control_thread
    _control_thread = threading.Thread(target=timer, args=())
    _control_thread.start()
    _control_thread.join()


def temperature_control(): 
    print("oi")

def control_thread_stop():
    global _stop_thread
    _stop_thread = True


control_thread()
