import signal
import time

def alarm_handler(signum, frame):
    print("aqui")

def main():
    while True: 
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(1)
        signal.pause()

main()
