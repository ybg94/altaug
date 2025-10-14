import logging
import time
from typing import Callable 
import dearpygui.dearpygui as dpg
import pyautogui
from . import elements
from .. import gui_tags
from ..config_manager import manager, Configuration

def __wait_for_confirmation(poll_rate:int = 20, failsafe_seconds: int = 10) -> bool:
    for _ in range(0, poll_rate * failsafe_seconds):
        if dpg.is_key_down(dpg.mvKey_Spacebar):
            return True
        
        if dpg.is_key_down(dpg.mvKey_Escape):
            return False
        
        time.sleep(1 / poll_rate)
    return False

def __get_target_position() -> tuple[int, int] | None:
    if __wait_for_confirmation():
        return pyautogui.position()
    
    return None

def __record_position(sender, app_data, config_updater: Callable[[Configuration, tuple[int, int]], Configuration]) -> None:
    dpg.configure_item(gui_tags.CONFIGURATION_INFO_MODAL_TAG, show=True)

    position = __get_target_position()
    if position:
        logging.info(f"Executing {config_updater.__name__} with x = {position[0]} and y = {position[1]}")

        updated_config = config_updater(manager.cfg, position)
        manager.save_config(updated_config)
        pass

    dpg.configure_item(gui_tags.CONFIGURATION_INFO_MODAL_TAG, show=False)    
    pass

def __update_alt_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.alt = new_pos
    return new_config

def __update_aug_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.aug = new_pos
    return new_config

def __update_alch_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.alch = new_pos
    return new_config

def __update_scour_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.scour = new_pos
    return new_config

def __update_chaos_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.chaos = new_pos
    return new_config

def __update_map_first_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.map_top_left = new_pos
    return new_config

def __toggle_autogui_failsafe() -> None:
    value = dpg.get_value(gui_tags.PYAUTOGUI_FAILSAFE_TOGGLE_TAG)
    logging.debug(f"Failsafe checkbox state is {value}.")
    pyautogui.FAILSAFE = value
    pass

def __set_pyautogui_pause() -> None:
    value = dpg.get_value(gui_tags.PYAUTOGUI_PAUSE_TAG)
    logging.debug(f"Setting PAUSE to {value}.")
    pyautogui.PAUSE = value
    pass

def init(configuration_window_tag: int | str) -> None:
    with dpg.window(tag=gui_tags.CONFIGURATION_INFO_MODAL_TAG, modal=True, show=False, no_title_bar=True, pos=(302, 70), width=178, height=60, no_resize=True, no_move=True):
        dpg.add_text(default_value="Press Space to record")
        dpg.add_text(default_value="Press Esc to cancel")
        pass

    with dpg.window(tag=configuration_window_tag, label="Configuration", no_close=True):
        dpg.add_text(default_value="Must restart script to apply config changes")

        with dpg.group(horizontal=True):
            elements.add_button(label="Capture Alteration orb position", callback=__record_position, user_data=__update_alt_position, width=300)
            elements.add_button(label="Capture Augmentation orb position", callback=__record_position, user_data=__update_aug_position, width=300)

        with dpg.group(horizontal=True):
            elements.add_button(label="Capture Alchemy orb position", callback=__record_position, user_data=__update_alch_position, width=300)
            elements.add_button(label="Capture Scouring orb position", callback=__record_position, user_data=__update_scour_position, width=300)
        
        with dpg.group(horizontal=True):
            elements.add_button(label="Capture First Map position", callback=__record_position, user_data=__update_map_first_position, width=300)
            elements.add_button(label="Capture Chaos orb position", callback=__record_position, user_data=__update_chaos_position, width=300)


        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Set pause after each PyAutoGui action:")
            dpg.add_input_float(
                tag=gui_tags.PYAUTOGUI_PAUSE_TAG,
                default_value=manager.cfg.app_settings.pyautogui_pause,
                max_value=1.0,
                max_clamped=True,
                min_value=0.025,
                min_clamped=True,
                step=0.005,
                callback=__set_pyautogui_pause,
                width=100
            )

        dpg.add_checkbox(
            tag=gui_tags.PYAUTOGUI_FAILSAFE_TOGGLE_TAG,
            label="Enable PyAutoGUI Failsafe",
            default_value=manager.cfg.app_settings.enable_pyautogui_failsafe,
            callback=__toggle_autogui_failsafe
        )
        dpg.add_checkbox(
            tag=gui_tags.PERFORMANCE_LOGGING_TAG,
            label="Enable performance logging",
            default_value=manager.cfg.app_settings.enable_performance_logging
        )
