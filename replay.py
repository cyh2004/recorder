import os
import re
import pyautogui
import time
from PIL import Image

# TODO: 原作者写了一份用于回放的代码，但我们似乎暂时不需要，就没改了
# 下面的是原作者的回放代码，目前应该是不能用的状态

time.sleep(3)
action_delay = 2.2

def get_sorted_image_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    return sorted(files, key=lambda x: (int(re.search(r'^(\d+)', x).group(1)), x))

def extract_action(filename):
    parts = filename.split('_')
    action = parts[1]
    params = parts[2:-1]  
    return action, params

def perform_action(action, params, image_path):
    def sort_strings_by_length(string_list):
        return sorted(string_list, key=lambda x: len(x), reverse=True)
    print(f"Performing action: {action} with params: {params}")
    
    if action == 'hover':
        x, y = int(params[1]), int(params[2])
        pyautogui.moveTo(x, y)
        time.sleep(2)  
    elif action == 'mouse':
        if 'drag' in params:
            start_x, start_y = int(params[2]), int(params[3])
            end_x, end_y = int(params[5]), int(params[6])
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(end_x, end_y, duration=0.5)
        elif 'clicked' in params:
            x, y = int(params[3]), int(params[4])
            pyautogui.click(x, y)
        elif 'scrolled' in params:
            x, y = int(params[2]), int(params[3])
            dx, dy = int(params[5]), int(params[7])
            pyautogui.moveTo(x, y)
            time.sleep(0.2)
            pyautogui.scroll(dy)
    elif action == 'Hotkey':
        keys = params[0].split('+')
        keys = sort_strings_by_length(keys)
        pyautogui.hotkey(*keys)
    elif action == 'text':
        text = params[1].replace('-', ' ')
        pyautogui.write(text)
    elif action == 'key':
        key = params[1]
        pyautogui.press(key)

def replay_actions(folder_path):
    image_files = get_sorted_image_files(folder_path)
    grouped_files = {}
    
    for file in image_files:
        number = int(re.search(r'^(\d+)', file).group(1))
        if number not in grouped_files:
            grouped_files[number] = []
        grouped_files[number].append(file)
    
    
    sorted_numbers = sorted(grouped_files.keys())
    new_grouped_files = {}
    new_number = 1
    
    for number in sorted_numbers:
        new_grouped_files[new_number] = grouped_files[number]
        new_number += 1
    
    cnt = 0
    for number in sorted(new_grouped_files.keys()):
        files = new_grouped_files[number]
        unique_actions = {}
        for file in sorted(files):
            action_base = '_'.join(file.split('_')[:-1])  
            if action_base not in unique_actions or file.endswith('_after.png'):
                unique_actions[action_base] = file
        
        for file in sorted(unique_actions.values()):
            action, params = extract_action(file)
            perform_action(action, params, os.path.join(folder_path, file))
            time.sleep(action_delay)  
        
        if cnt == 0:
            time.sleep(3)
        cnt += 1

folder_path = '/home/user/project/screenshots/run_20240627_162633_416'
replay_actions(folder_path)