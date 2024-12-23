from pynput import keyboard
import threading

import screenshot
import listener_control


pressed_keys = set()
text_input = ""
text_input_timer = None
text_input_delay = 2 

shift_pressed = False
caps_lock_on = False
modifier_keys = {'ctrl', 'alt', 'cmd', 'shift'}

def save_text_input():
    global text_input
    if text_input:
        action = f"text_input_{text_input.replace(' ', '-')}"
        print(f"Text input: {action}")

        action_data = {
            "type": "keyboard",
            "action": "text_input",
            "text": text_input
        }
        screenshot.take_screenshots(action, action_data)
        text_input = ""

def on_press(key):
    if not listener_control.started():
        return
    if listener_control.ended():
        return False
    if not listener_control.is_ctrl(key):
        listener_control.clear_cnt()

    global text_input, text_input_timer, shift_pressed, caps_lock_on, pressed_keys

    if key == keyboard.Key.shift:
        shift_pressed = True
    elif key == keyboard.Key.caps_lock:
        caps_lock_on = not caps_lock_on
        
    def get_key(key, shift_pressed, caps_lock_on):
        if isinstance(key, keyboard.KeyCode):
            if key.char:
                if shift_pressed ^ caps_lock_on:  # XOR 
                    return key.char.upper()
                else:
                    return key.char.lower()
        return key.char if isinstance(key, keyboard.KeyCode) else key.name
    
    actual_key = get_key(key, shift_pressed, caps_lock_on)

    modifier_pressed = any(mod in pressed_keys for mod in modifier_keys if mod != 'shift')

    if modifier_pressed:
        if text_input:
            save_text_input()
        if isinstance(key, keyboard.KeyCode):
            pressed_keys.add(actual_key)
        elif isinstance(key, keyboard.Key):
            pressed_keys.add(key.name)
            if key.name in modifier_keys:
                return
        
        combo = '+'.join(sorted(pressed_keys))
        action = f"Hotkey_{combo}"
        print(f"Key combination: {action}")
        
        # not save ctrl + shift 
        # if not (len(pressed_keys) == 2 and 'ctrl' in pressed_keys and 'shift' in pressed_keys):

        action_data = {
            "type": "keyboard",
            "action": "hotkey",
            "keys_pressed": list(pressed_keys)
        }
        screenshot.take_screenshots(action, action_data)
        return

    
    if isinstance(key, keyboard.KeyCode) or (isinstance(key, keyboard.Key) and key.name == 'space'):
        if isinstance(key, keyboard.Key) and key.name == 'space':
            text_input += ' '
        else:
            text_input += actual_key
        if text_input_timer:
            text_input_timer.cancel()
        text_input_timer = threading.Timer(text_input_delay, save_text_input)
        text_input_timer.start()
    
    elif key == keyboard.Key.backspace:
        if text_input:
            text_input = text_input[:-1]
        if text_input_timer:
            text_input_timer.cancel()
        text_input_timer = threading.Timer(text_input_delay, save_text_input)
        text_input_timer.start()
    
    elif key == keyboard.Key.enter:
        if text_input:
            save_text_input()
        else:
            action = "key_press_enter"
            print(f"Key press: {action}")

            action_data = {
                "type": "keyboard",
                "action": "press",
                "keys_pressed": [key.name]
            }
            screenshot.take_screenshots(action, action_data)
    
    elif isinstance(key, keyboard.Key) and key.name not in modifier_keys:
        if text_input:
            save_text_input()
        action = f"key_press_{key.name}"
        print(f"Key press: {action}")

        action_data = {
            "type": "keyboard",
            "action": "press",
            "keys_pressed": [key.name]
        }
        screenshot.take_screenshots(action, action_data)

    
    if isinstance(key, keyboard.Key) and key.name != 'shift':
        pressed_keys.add(key.name)
    elif isinstance(key, keyboard.KeyCode):
        pressed_keys.add(actual_key.lower())  

def on_release(key):
    if not listener_control.is_ctrl(key):
        listener_control.clear_cnt()
    else:
        listener_control.check_ctrl_released(key)
        return

    if not listener_control.started():
        return
    if listener_control.ended():
        return False
    global shift_pressed, pressed_keys
    
    if key == keyboard.Key.shift:
        shift_pressed = False
    
   
    if isinstance(key, keyboard.Key) and key.name != 'shift':
        pressed_keys.discard(key.name)
    elif isinstance(key, keyboard.KeyCode):
        pressed_keys.discard(key.char.lower())


    # if key == keyboard.Key.esc and keyboard.Key.space and keyboard.Key.altP:
    #     return False

def get_keyboard_listener():
    k_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    return k_listener