import threading
from pynput import keyboard

lock = threading.Lock()
start = False
end = False
ctrl_cnt = 0

def is_ctrl(key):
    return key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl, keyboard.Key.cmd, keyboard.Key.cmd_r, keyboard.Key.cmd_l]

def check_ctrl_released(key):
    if is_ctrl(key):
        global ctrl_cnt, lock, start, end
        with lock:
            ctrl_cnt += 1
            if ctrl_cnt == 2:
                if start:
                    end = True
                else:
                    start = True
            print(f"ctrl_cnt: {ctrl_cnt}, start: {start}, end: {end}")

def clear_cnt():
    global ctrl_cnt, lock
    with lock:
        ctrl_cnt = 0

def started():
    global start, lock
    with lock:
        tmp = start
    return tmp

def ended():
    global end, lock
    with lock:
        tmp = end
    return tmp