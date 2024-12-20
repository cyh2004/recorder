import pyautogui
import json
from typing import Dict
import platform
from pyxcursor import Xcursor
from PIL import Image, ImageGrab
import ctypes
platform_name: str = platform.system()

if platform_name == "Windows":
    import win32ui, win32gui

screenshot_counter = 0
last_screenshot = None
screenshots_folder = None
screen_width = 1920
screen_height = 1080

actions = []

def set_screen_dimensions(width, height):
    global screen_width, screen_height
    screen_width = width
    screen_height = height

def init(folder_name):
    global screenshots_folder, last_screenshot
    screenshots_folder = folder_name
    screenshot = pyautogui.screenshot()
    screenshot = capture_cursor(screenshot)
    screenshot.save(f"{screenshots_folder}/init.png")
    last_screenshot = "init.png"

def take_screenshots(action, action_data: Dict):
    global screenshot_counter, last_screenshot, screenshots_folder, actions
    screenshot_counter += 1
    
    screenshot_after = pyautogui.screenshot()
    screenshot_after = capture_cursor(screenshot_after)
    filename_after = f"{screenshots_folder}/{screenshot_counter:06d}_{action}.png"
    screenshot_after.save(filename_after)
    print(f"Screenshot saved: {filename_after}")

    action_data["screenshot_before"] = last_screenshot
    action_data["screenshot_after"] = f"{screenshot_counter:06d}_{action}.png"
    action_data["width"] = screen_width
    action_data["height"] = screen_height
    actions.append(action_data)

    with open(f"{screenshots_folder}/actions.json", "w") as f:
        json.dump(actions, f, indent=4, ensure_ascii=False)
    
    last_screenshot = f"{screenshot_counter:06d}_{action}.png"

def capture_cursor(screenshot):
    user_platform = platform.system()
    if user_platform == "Windows":
        def get_cursor():
            hcursor = win32gui.GetCursorInfo()[1]
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, 36, 36)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0,0), hcursor)

            bmpinfo = hbmp.GetInfo()
            bmpstr = hbmp.GetBitmapBits(True)
            cursor = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1).convert("RGBA")

            win32gui.DestroyIcon(hcursor)
            win32gui.DeleteObject(hbmp.GetHandle())
            hdc.DeleteDC()

            pixdata = cursor.load()

            width, height = cursor.size
            for y in range(height):
                for x in range(width):
                    if pixdata[x, y] == (0, 0, 0, 255):
                        pixdata[x, y] = (0, 0, 0, 0)

            hotspot = win32gui.GetIconInfo(hcursor)[1:3]

            return (cursor, hotspot)

        ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        try:
            cursor, (hotspotx, hotspoty) = get_cursor()

            pos_win = win32gui.GetCursorPos()
            pos = (round(pos_win[0]*ratio - hotspotx), round(pos_win[1]*ratio - hotspoty))

            screenshot.paste(cursor, pos, cursor)
        except:
            pass

        return screenshot
    elif user_platform == "Linux":
        cursor_obj = Xcursor()
        imgarray = cursor_obj.getCursorImageArrayFast()
        cursor_img = Image.fromarray(imgarray)
        cursor_x, cursor_y = pyautogui.position()
        screenshot.paste(cursor_img, (cursor_x, cursor_y), cursor_img)
        return screenshot