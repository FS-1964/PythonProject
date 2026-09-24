import time
from random import randint
from datetime import datetime
def zufallgame():
    counter = 0
    while True:
        zufallzahl = randint(1, 100)
        counter = counter + 1
        time.sleep(1)
        print(datetime.now().strftime("%H:%M:%S"))
        if counter == 20:
            print(counter, "-", zufallzahl, "exit by 20")
            print("total generated Random number is", counter)
            break
        elif zufallzahl % 2 == 0:
            print(counter, "-", zufallzahl, "is divisible by 2")
        elif zufallzahl % 2 != 0:
            print(counter, "-", zufallzahl, "is divisible by 1")
def addieren(*zahlen):
    return sum(zahlen)