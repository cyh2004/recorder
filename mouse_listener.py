from pynput import mouse
import time
import threading

import screenshot


scroll_accumulator = {"x": 0, "y": 0, "dx": 0, "dy": 0}
scroll_timer = None
scroll_delay = 0.3  

hover_timer = None
hover_delay = 5

is_dragging = False
drag_start = None
drag_threshold_x = 10
drag_threshold_y = 10

last_move_time = 0
last_position = None

screen_width = 1920
screen_height = 1080

def set_screen_dimensions(width, height):
    global screen_width, screen_height
    screen_width = width
    screen_height = height

def check_hover():
    global last_position, last_move_time, hover_delay
    current_time = time.time()
    if current_time - last_move_time >= hover_delay and last_position:
        action = f"hover_at_{last_position[0]}_{last_position[1]}"
        print(f"Hover detected at position: {last_position}")

        action_data = {
            "type": "mouse",
            "action": "hover",
            "point": {
                "x": last_position[0],
                "y": last_position[1],
                "relative_x": last_position[0] / screen_width,
                "relative_y": last_position[1] / screen_height
            }
        }
        screenshot.take_screenshots(action, action_data)

def on_move(x, y):
    global is_dragging, drag_start, last_move_time, last_position, hover_timer
    
    if hover_timer:
        hover_timer.cancel()
    
    last_move_time = time.time()
    last_position = (x, y)
    
    hover_timer = threading.Timer(hover_delay, check_hover)
    hover_timer.start()

def on_click(x, y, button, pressed):
    global is_dragging, drag_start, hover_timer, screen_height, screen_width
    
    if hover_timer:
        hover_timer.cancel()
    
    if pressed:
        if button == mouse.Button.left:
            is_dragging = True
            drag_start = (x, y)
    else:
        if is_dragging:
            dx = abs(x - drag_start[0])
            dy = abs(y - drag_start[1])
            if dx >= drag_threshold_x and dy >= drag_threshold_y:
                action = f"mouse_drag_from_{drag_start[0]}_{drag_start[1]}_to_{x}_{y}"
                print(f"Mouse drag completed from {drag_start} to ({x}, {y})")

                action_data = {
                    "type": "mouse",
                    "action": "drag",
                    "point_from": {
                        "x": drag_start[0],
                        "y": drag_start[1],
                        "relative_x": drag_start[0] / screen_width,
                        "relative_y": drag_start[1] / screen_height
                    },
                    "point_to": {
                        "x": x,
                        "y": y,
                        "relative_x": x / screen_width,
                        "relative_y": y / screen_height
                    }
                }
                screenshot.take_screenshots(action, action_data)
            else:
                action = f"mouse_{button}_clicked_at_{x}_{y}"
                print(f"Mouse {button} clicked at ({x}, {y})")

                action_data = {
                    "type": "mouse",
                    "action": "click",
                    "point": {
                        "x": x,
                        "y": y,
                        "relative_x": x / screen_width,
                        "relative_y": y / screen_height
                    }
                }
                screenshot.take_screenshots(action, action_data)
        else:
            action = f"mouse_{button}_clicked_at_{x}_{y}"
            print(f"Mouse {button} clicked at ({x}, {y})")

            action_data = {
                "type": "mouse",
                "action": "click",
                "point": {
                    "x": x,
                    "y": y,
                    "relative_x": x / screen_width,
                    "relative_y": y / screen_height
                }
            }
            screenshot.take_screenshots(action, action_data)
        is_dragging = False
        drag_start = None

def save_scroll():
    global scroll_accumulator, screen_height, screen_width
    if scroll_accumulator["dx"] != 0 or scroll_accumulator["dy"] != 0:
        action = f"mouse_scrolled_at_{scroll_accumulator['x']}_{scroll_accumulator['y']}_dx_{scroll_accumulator['dx']}_dy_{scroll_accumulator['dy']}"
        print(f"Mouse scrolled at ({scroll_accumulator['x']}, {scroll_accumulator['y']}), total: ({scroll_accumulator['dx']}, {scroll_accumulator['dy']})")

        action_data = {
            "type": "mouse",
            "action": "scroll",
            "point": {
                "x": scroll_accumulator["x"],
                "y": scroll_accumulator["y"],
                "relative_x": scroll_accumulator["x"] / screen_width,
                "relative_y": scroll_accumulator["y"] / screen_height
            },
            "delta_x": scroll_accumulator["dx"],
            "delta_y": scroll_accumulator["dy"]
        }
        screenshot.take_screenshots(action, action_data)
        scroll_accumulator = {"x": 0, "y": 0, "dx": 0, "dy": 0}

def on_scroll(x, y, dx, dy):
    global scroll_accumulator, scroll_timer
    scroll_accumulator["x"] = x
    scroll_accumulator["y"] = y
    scroll_accumulator["dx"] += dx
    scroll_accumulator["dy"] += dy
    
    if scroll_timer:
        scroll_timer.cancel()
    scroll_timer = threading.Timer(scroll_delay, save_scroll)
    scroll_timer.start()

def get_mouse_listener():
    m_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    return m_listener