import threading
import time
from colorama import Fore

x = int(input("نرخ ورود مشتری در ثانیه را وارد کنید:     "))
y = float(input("مدت زمان خرید مشتریان را وارد کنید:       "))
shop_cap = threading.Semaphore(x)
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
    m = 1 if len(store_cash_register1) <= len(store_cash_register2) else 2
    if m == 1:
        m = 1 if len(store_cash_register1) <= len(store_cash_register3) else 3
    if m == 2:
        m = 2 if len(store_cash_register2) <= len(store_cash_register3) else 3
    return m


def shopping(y):
    current_thread = threading.current_thread()
    input_semaphor.acquire()
    input_semaphor.release()
    shop_cap.acquire()
    input_door_pend.remove(current_thread)
    stor_list.append(current_thread)
    time.sleep(y)
    shop_cap.release()
    stor_list.remove(current_thread)
    if min_store_cash_register() == 1:
        store_cash_register1.append(current_thread)
        store_cash_register1_semaphor.acquire()
        time.sleep(0.05)
        store_cash_register1_semaphor.release()
        output_door_pend.append(
            store_cash_register1.remove(current_thread)
        )
    elif min_store_cash_register() == 2:
        store_cash_register2.append(current_thread)
        store_cash_register2_semaphor.acquire()
        time.sleep(0.05)
        store_cash_register2_semaphor.release()
        output_door_pend.append(
            store_cash_register2.remove(current_thread)
        )
    else:
        store_cash_register3.append(current_thread)
        store_cash_register3_semaphor.acquire()
        time.sleep(0.05)
        store_cash_register3_semaphor.release()
        store_cash_register3.remove(current_thread)
        output_door_pend.append(current_thread)
    output_door_semaphor.acquire()
    time.sleep(0.05)
    output_door_semaphor.release()
    output_door_pend.remove(current_thread)


def pr():
    while True:
        if len(output_door_pend) >= 10:
            print(
                Fore.RED
                + f"in-pend: {len(input_door_pend)} out-pend: {len(output_door_pend)}, all:{len(threading.enumerate())}"
            )
            break


def prr():
    while True:
        print(
            f"cr1:{len(store_cash_register1)} cr2:{len(store_cash_register2)} cr3:{len(store_cash_register3)}"
        )
        print(
            Fore.BLUE
            + f"in-pend: {len(input_door_pend)} shop: {len(stor_list)} out-pend: {len(output_door_pend)}, all:{len(threading.enumerate())}"
        )
        time.sleep(1)


threading.Thread(target=pr).start()
threading.Thread(target=prr).start()

for _ in range(100):
    for _ in range(x):
        th = threading.Thread(target=shopping, args=(y,))
        input_door_pend.append(th)
        th.start()
    time.sleep(1)
print(Fore.BLUE + f"end round with x:{x} y:{y}")


