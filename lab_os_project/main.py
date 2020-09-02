import random
import sys
import threading
import time
from colorama import Fore
from os import system

shop_cap = None
input_semaphor = threading.Semaphore(2)
output_door_semaphor = threading.Semaphore(1)
store_cash_register1_semaphor = threading.Semaphore(1)
store_cash_register2_semaphor = threading.Semaphore(1)
store_cash_register3_semaphor = threading.Semaphore(1)
store_cash_register1 = []
store_cash_register2 = []
store_cash_register3 = []
output_door_pend = []
input_door_pend = []
thread_pool = []
stor_list = []

def min_store_cash_register():
    m = 1 if len(store_cash_register1)<=len(store_cash_register2) else 2
    if m == 1:
        m = 1 if len(store_cash_register1)<=len(store_cash_register3) else 3
    if m==2:
        m = 2 if len(store_cash_register2)<=len(store_cash_register3) else 3
    return m
def shopping(x, y):
    current_thread = threading.current_thread()
    input_semaphor.acquire()
    input_semaphor.release()
    shop_cap.acquire()
    input_door_pend.pop(input_door_pend.index(current_thread))
    stor_list.append(current_thread)
    time.sleep(y)
    shop_cap.release()
    stor_list.pop(stor_list.index(current_thread))
    if min_store_cash_register() == 1 :
        store_cash_register1.append(current_thread)
        store_cash_register1_semaphor.acquire()
        time.sleep(.05)
        store_cash_register1_semaphor.release()
        output_door_pend.append(store_cash_register1.pop(store_cash_register1.index(current_thread)))
    elif min_store_cash_register() == 2:
        store_cash_register2.append(current_thread)
        store_cash_register2_semaphor.acquire()
        time.sleep(.05)
        store_cash_register2_semaphor.release()
        output_door_pend.append(store_cash_register2.pop(store_cash_register2.index(current_thread)))
    else:
        store_cash_register3.append(threading.current_thread())
        store_cash_register3_semaphor.acquire()
        time.sleep(.05)
        store_cash_register3_semaphor.release()
        output_door_pend.append(store_cash_register3.pop(store_cash_register3.index(current_thread)))
    output_door_semaphor.acquire()
    time.sleep(.05)
    output_door_semaphor.release()
    output_door_pend.pop(output_door_pend.index(current_thread))
def pr():
    while True:
            if len(output_door_pend) >= 10:
                print(Fore.RED + f'in-pend: {len(input_door_pend)} out-pend: {len(output_door_pend)}, all:{len(threading.enumerate())}')
                break
def prr():
    while True:
        print(f'1:{len(store_cash_register1)} 2:{len(store_cash_register2)} 3:{len(store_cash_register3)}')
        print(Fore.BLUE + f'in-pend: {len(input_door_pend)} shop: {len(stor_list)} out-pend: {len(output_door_pend)}, all:{len(threading.enumerate())}')
        time.sleep(1)
def main(x, y):
    threading.Thread(target=pr).start()
    threading.Thread(target=prr).start()

    for _ in range(100):
        for _ in range(x):
            th = threading.Thread(target=shopping, args=(x,y))
            input_door_pend.append(th)
            thread_pool.append(th)
            th.start()
        time.sleep(1)
    if len(output_door_pend) >= 10:
        sys.exit()
    for th in thread_pool:
        th.join()
    print(Fore.BLUE + f'end round with x:{x} y:{y}')

if __name__ == '__main__':
    x = int(input("نرخ ورود مشتری در ثانیه را وارد کنید:     "))
    y = float(input('مدت زمان خرید مشتریان را وارد کنید:       '))
    shop_cap = threading.Semaphore(x)
    main(x, y)
