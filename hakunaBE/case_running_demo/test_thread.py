import threading
import time
import os

def fun1():
    for i in range(3):
        print('1')
        time.sleep(1)

def fun2():
    for i in range(3):
        print('2')
        time.sleep(3)

if __name__ == '__main__':
    sing_thread = threading.Thread(target=fun1)
    song_thread = threading.Thread(target=fun2)

    sing_thread.start()
    song_thread.start()
