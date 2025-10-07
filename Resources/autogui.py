import pyperclip #used to see what was copied.
import pyautogui
from . import read_config
from . import time_helpers as rtime

CONFIG_DATA = read_config.read_config()
screen_width, screen_height = pyautogui.size()

@rtime.timeit
def hover_item():
    x_item=int(screen_width * CONFIG_DATA['item_x_coordinate_percent'])
    y_item=int(screen_height * CONFIG_DATA['item_y_coordinate_percent'])
    pyautogui.moveTo(x_item,y_item)

@rtime.timeit
def copy_item():
    hover_item()
    pyautogui.hotkey("ctrl", "c")

def check_clipboard_for(keyword):
    text = pyperclip.paste()
    lines = text.splitlines()
    if len(lines) >= 3:
        return keyword in lines[2]
    else: 
        return False

def check_active_base(bases):

    copy_item()
    item_text = pyperclip.paste()
    if not item_text:
        print("Error: Clipboard empty after copy_item().")
        return None

    for base in bases:
        if base in item_text:
            return base
    return None

def get_item_name(item_text=None):
    copy_item()
    item_text = pyperclip.paste()
    if not item_text:
        print("Error: Clipboard empty after copy_item().")
        return None

    lines = item_text.splitlines()
    if len(lines) < 3:
        print("Error: Item text too short.")
        return None

    item_name = lines[2].strip()
    return item_name

@rtime.timeit
def use_alt():
    x_alt=int(screen_width * CONFIG_DATA['alt_x_coordinate_percent'])
    y_alt=int(screen_height * CONFIG_DATA['alt_y_coordinate_percent'])
    pyautogui.moveTo(x_alt,y_alt)
    pyautogui.rightClick()
    hover_item()
    pyautogui.leftClick()

@rtime.timeit
def use_aug():
    x_aug=int(screen_width * CONFIG_DATA['aug_x_coordinate_percent'])
    y_aug=int(screen_height * CONFIG_DATA['aug_y_coordinate_percent'])
    pyautogui.moveTo(x_aug,y_aug)
    pyautogui.rightClick()
    hover_item()
    pyautogui.leftClick()