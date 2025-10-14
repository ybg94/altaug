import logging
import pyautogui
import pyperclip
from . import decorators
from .config_manager import manager

screen_width, screen_height = pyautogui.size()

@decorators.timeit
def hover_item():
    pyautogui.moveTo(manager.cfg.coordinates.item)

@decorators.timeit
def hover_map(map_count):
    map_pos = calculate_map_coordinates(map_count)
    pyautogui.moveTo(map_pos)

def calculate_map_coordinates(map_count) -> tuple[int, int]:
    coordinates = manager.cfg.coordinates
    map_x = (coordinates.map_top_left.x + coordinates.map_bottom_right.x) / 2
    map_y = (coordinates.map_top_left.y + coordinates.map_bottom_right.y) / 2
    step_x = coordinates.map_bottom_right.x - coordinates.map_top_left.x
    step_y = coordinates.map_bottom_right.y - coordinates.map_top_left.y

    row = (map_count - 1) // 5
    col = (map_count - 1) % 5

    map_x += row * step_x
    map_y += col * step_y

    return (map_x, map_y)

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

@decorators.timeit
def get_map_description(map_count: int) -> str:
    hover_map(map_count)
    pyautogui.hotkey("ctrl", "c")
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
    pyautogui.moveTo(manager.cfg.coordinates.alt)
    pyautogui.rightClick()
    hover_item()
    pyautogui.leftClick()

@decorators.timeit
def use_aug():
    pyautogui.moveTo(manager.cfg.coordinates.aug)
    pyautogui.rightClick()
    hover_item()
    pyautogui.leftClick()

@decorators.timeit
def use_alch(map_count):
    pyautogui.moveTo(manager.cfg.coordinates.alch)
    pyautogui.rightClick()
    hover_map(map_count)
    pyautogui.leftClick()

@decorators.timeit
def use_chaos(map_count):
    pyautogui.moveTo(manager.cfg.coordinates.chaos)
    pyautogui.rightClick()
    hover_map(map_count)
    pyautogui.leftClick()

@decorators.timeit
def use_scour(map_count):
    pyautogui.moveTo(manager.cfg.coordinates.scour)
    pyautogui.rightClick()
    hover_map(map_count)
    pyautogui.leftClick()