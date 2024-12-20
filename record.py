import os
from datetime import datetime
import pyautogui

import mouse_listener
import keyboard_listener
import screenshot


def create_new_screenshots_folder():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]  
    folder_name = f"screenshots/run_{timestamp}"
    
    
    while os.path.exists(folder_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
        folder_name = f"screenshots/run_{timestamp}"
    
    os.makedirs(folder_name)
    print(f"New screenshots folder created: {folder_name}")
    screenshot.init(folder_name)

def main():
    create_new_screenshots_folder()

    # 获取屏幕大小
    width, height = pyautogui.size()
    print(f"Screen size: {width} x {height}")
    mouse_listener.set_screen_dimensions(width, height)
    screenshot.set_screen_dimensions(width, height)

    m_listener = mouse_listener.get_mouse_listener()
    k_listener = keyboard_listener.get_keyboard_listener()

    m_listener.start()
    k_listener.start()

    m_listener.join()
    k_listener.join()

if __name__ == '__main__':
    main()
    