import pyperclip #used to see what was copied.
import pyautogui
import time
from . import read_config

CONFIG_DATA = read_config.read_config()
screen_width, screen_height = pyautogui.size()

def hover_item():
    x_item=int(screen_width * CONFIG_DATA['item_x_coordinate_percent'])
    y_item=int(screen_height * CONFIG_DATA['item_y_coordinate_percent'])
    pyautogui.moveTo(x_item,y_item, duration=0.1)

def copy_item():
    hover_item()

    #pyautogui.rightClick() #Just to select the POE screen for now, otherwise it does not copy item text
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)

def check_clipboard_for(keyword):
    text = pyperclip.paste()
    lines = text.splitlines()
    if len(lines) >= 3:
        return keyword in lines[2]
    else: 
        return False

def check_active_base(bases):
    copy_item()
    full_item_desc = pyperclip.paste()
    if full_item_desc is None:
        print("Error: copy_item() returned None. Unable to check base.")
    for base in bases:
        if base in full_item_desc:
            return base
    return None

def get_item_name():
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


def use_alt():
    x_alt=int(screen_width * CONFIG_DATA['alt_x_coordinate_percent'])
    y_alt=int(screen_height * CONFIG_DATA['alt_y_coordinate_percent'])
    pyautogui.moveTo(x_alt,y_alt, duration=0.1)
    pyautogui.rightClick()
    hover_item()

def use_aug():
    x_aug=int(screen_width * CONFIG_DATA['aug_x_coordinate_percent'])
    y_aug=int(screen_height * CONFIG_DATA['aug_y_coordinate_percent'])
    pyautogui.moveTo(x_aug,y_aug, duration=0.1)
    pyautogui.rightClick()
    hover_item()