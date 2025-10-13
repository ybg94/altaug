import logging
import pyautogui
import pyperclip #used to see what was copied.
from . import decorators
from .config_manager import manager

screen_width, screen_height = pyautogui.size()

@decorators.timeit
def hover_item():
    x_item=int(screen_width * manager.cfg.coordinates.item_x)
    y_item=int(screen_height * manager.cfg.coordinates.item_y)
    pyautogui.moveTo(x_item,y_item)

@decorators.timeit
def hover_map(map_count):
    x_map, y_map = calculate_map_coordinates(map_count)
    pyautogui.moveTo(x_map,y_map)

def calculate_map_coordinates(map_count):
    middle_x_map = (CONFIG_DATA['map_top_left_x_coordinate_percent'] + CONFIG_DATA['map_bottom_right_x_coordinate_percent'])/2
    middle_y_map = (CONFIG_DATA['map_top_left_y_coordinate_percent'] + CONFIG_DATA['map_bottom_right_y_coordinate_percent'])/2
    x_differential = int(screen_width * (CONFIG_DATA['map_bottom_right_x_coordinate_percent'] - CONFIG_DATA['map_top_left_x_coordinate_percent']))
    y_differential = int(screen_height * (CONFIG_DATA['map_bottom_right_y_coordinate_percent'] - CONFIG_DATA['map_top_left_y_coordinate_percent']))

    x_map = int(screen_width * middle_x_map)
    y_map = int(screen_height * middle_y_map)

    row = (map_count - 1) // 5
    col = (map_count - 1) % 5

    x_map += row * x_differential
    y_map += col * y_differential

    return x_map, y_map

@decorators.timeit
def copy_item():
    hover_item()
    pyautogui.hotkey("ctrl", "c")

@decorators.timeit
def copy_map(map_count):
    hover_map(map_count)
    pyautogui.hotkey("ctrl", "c")

@decorators.timeit
def get_item_advanced_description() -> str:
    hover_item()
    pyautogui.hotkey("ctrl", "alt", "c")
    return pyperclip.paste()

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
        logging.error("Clipboard empty after copy_item().")
        return None

    for base in bases:
        if base in item_text:
            return base
    return None

def get_item_name(item_text=None):
    copy_item()
    item_text = pyperclip.paste()
    if not item_text:
        logging.error("Clipboard empty after copy_item().")
        return None

    lines = item_text.splitlines()
    if len(lines) < 3:
        logging.error("Item text too short.")
        return None

    item_name = lines[2].strip()
    return item_name

@decorators.timeit
def use_alt():
    x_alt=int(screen_width * manager.cfg.coordinates.alt_x)
    y_alt=int(screen_height * manager.cfg.coordinates.alt_y)
    pyautogui.moveTo(x_alt,y_alt)
    pyautogui.rightClick()
    hover_item()
    pyautogui.leftClick()

@decorators.timeit
def use_aug():
    x_aug=int(screen_width * manager.cfg.coordinates.aug_x)
    y_aug=int(screen_height * manager.cfg.coordinates.aug_y)
    pyautogui.moveTo(x_aug,y_aug)
    pyautogui.rightClick()
    hover_item()
    pyautogui.leftClick()

@decorators.timeit
def use_alch(map_count):
    x_alch=int(screen_width * CONFIG_DATA['alch_x_coordinate_percent'])
    y_alch=int(screen_height * CONFIG_DATA['alch_y_coordinate_percent'])
    pyautogui.moveTo(x_alch,y_alch)
    pyautogui.rightClick()
    hover_map(map_count)
    pyautogui.leftClick()

@decorators.timeit
def use_scour(map_count):
    x_scour=int(screen_width * CONFIG_DATA['scour_x_coordinate_percent'])
    y_scour=int(screen_height * CONFIG_DATA['scour_y_coordinate_percent'])
    pyautogui.moveTo(x_scour,y_scour)
    pyautogui.rightClick()
    hover_map(map_count)
    pyautogui.leftClick()