import os
import json
import cv2
from pynput import mouse
import prompt

click_box_size = 10
thickness = 2
bbox = []

def on_click(x, y, button, pressed):
    if pressed:
        return
    print(f"Mouse clicked at ({x}, {y}) with {button}")
    assert button == mouse.Button.left
    bbox.append(x)
    bbox.append(y)
    if len(bbox) == 4:
        return False

def add_bbox(run_folder):
    with open(os.path.join(run_folder, "actions.json"), "r") as f:
        actions = json.load(f)
        for action in actions:
            if action["action"] == "click" or action["action"] == "hover":
                while True:
                    image = cv2.imread(os.path.join(run_folder, action["screenshot_before"]))
                    cv2.rectangle(image, (action["point"]["x"] - click_box_size, action["point"]["y"] - click_box_size), (action["point"]["x"] + click_box_size, action["point"]["y"] + click_box_size), (0, 255, 0), thickness)

                    cv2.namedWindow('Fullscreen Image', cv2.WINDOW_NORMAL)
                    cv2.setWindowProperty('Fullscreen Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.imshow('Fullscreen Image', image)
                    cv2.waitKey(1000)
                    listener = mouse.Listener(on_click=on_click)
                    listener.start()
                    listener.join()
                    cv2.destroyAllWindows()
                    del image

                    image = cv2.imread(os.path.join(run_folder, action["screenshot_before"]))
                    cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), thickness)
                    cv2.namedWindow('Fullscreen Image', cv2.WINDOW_NORMAL)
                    cv2.setWindowProperty('Fullscreen Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.imshow('Fullscreen Image', image)
                    cv2.waitKey(1000)
                    if not prompt.ask_retry():
                        cv2.destroyAllWindows()
                        action["bbox"] = {
                            "absolute": bbox[:], # copy the list
                            "relative": [
                                bbox[0] / action["width"], bbox[1] / action["height"],
                                bbox[2] / action["width"], bbox[3] / action["height"]
                            ]
                        }
                        bbox.clear()
                        break
                    cv2.destroyAllWindows()
                    bbox.clear()
    with open(os.path.join(run_folder, "actions.json"), "w") as f:
        json.dump(actions, f, indent=4)

if __name__ == '__main__':
    add_bbox("screenshots/run_20241223_213228_434")
