import logging
import time
from typing import Callable, Any, Tuple
import dearpygui.dearpygui as dpg
import pyautogui
from . import elements
from .. import gui_tags
from ..config_manager import manager, Configuration
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(CURRENT_DIR,"..","..","Images")

def load_images():
    with dpg.texture_registry(show=False):

        alt_path = os.path.join(IMAGES_DIR, "alt_orb.png")
        aug_path = os.path.join(IMAGES_DIR, "aug_orb.png")
        scour_path = os.path.join(IMAGES_DIR, "scour_orb.png")
        alch_path = os.path.join(IMAGES_DIR, "alch_orb.png")
        chaos_path = os.path.join(IMAGES_DIR, "chaos_orb.png")
        map_path = os.path.join(IMAGES_DIR, "map.png")
        bow_item_path = os.path.join(IMAGES_DIR, "bow_item.png")

        width, height, channels, data = dpg.load_image(alt_path)
        dpg.add_static_texture(width, height, data, tag="alt_orb_texture")

        width, height, channels, data = dpg.load_image(aug_path)
        dpg.add_static_texture(width, height, data, tag="aug_orb_texture")

        width, height, channels, data = dpg.load_image(alch_path)
        dpg.add_static_texture(width, height, data, tag="alch_orb_texture")

        width, height, channels, data = dpg.load_image(scour_path)
        dpg.add_static_texture(width, height, data, tag="scour_orb_texture")

        width, height, channels, data = dpg.load_image(chaos_path)
        dpg.add_static_texture(width, height, data, tag="chaos_orb_texture")

        width, height, channels, data = dpg.load_image(map_path)
        dpg.add_static_texture(width, height, data, tag="map_texture")

        width, height, channels, data = dpg.load_image(bow_item_path)
        dpg.add_static_texture(width, height, data, tag="bow_item_texture")

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

def __record_position(sender: int | str, app_data: Any, user_data: Tuple[str, Callable[[Configuration, tuple[int, int]], Configuration]]) -> None:
    label_text, config_updater = user_data

    dpg.set_item_label(gui_tags.CONFIGURATION_INFO_TEXT_TAG, label_text)
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

def __update_map_second_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.map_bottom_right = new_pos
    return new_config

def __update_item_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.item = new_pos
    return new_config

def __record_map_positions(sender, app_data, user_data) -> None:
    update_first, update_second = user_data
    __record_position(sender=sender, app_data=None, user_data=("Capture Top-Left Map corner", update_first))

    while dpg.is_key_down(dpg.mvKey_Spacebar) or dpg.is_key_down(dpg.mvKey_Escape):
        time.sleep(1 / 20)

    __record_position(sender=sender, app_data=None, user_data=("Capture Bottom-Right Map corner",update_second))
    pass

def __set_pyautogui_pause() -> None:
    value = dpg.get_value(gui_tags.PYAUTOGUI_PAUSE_TAG)
    logging.debug(f"Setting PAUSE to {value}.")
    pyautogui.PAUSE = value
    pass

def init(configuration_window_tag: int | str) -> None:
    with dpg.window(tag=gui_tags.CONFIGURATION_INFO_MODAL_TAG, modal=True, show=False, no_title_bar=True, pos=(302, 70), width=314, height=150, no_resize=True, no_move=True):
        dpg.add_spacer(height=2)
        dpg.add_button(tag=gui_tags.CONFIGURATION_INFO_TEXT_TAG, enabled=False, width=300)
        dpg.add_button(label="Press Space to record", enabled=False, width=300)
        dpg.add_button(label="Press Esc to cancel", enabled=False, width=300)
        pass

    with dpg.window(tag=configuration_window_tag, label="Configuration", no_close=True):
        dpg.add_text("Configuration Buttons:")
        
        with dpg.group(horizontal=True):
            dpg.add_image_button(texture_tag="bow_item_texture", callback=__record_position, user_data=("Capture Item Window position", __update_item_position), width=60, height=120)

            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_image_button(texture_tag="alt_orb_texture",callback=__record_position,user_data=("Capture Alteration Orb position", __update_alt_position),width=55, height=55)
                    dpg.add_image_button(texture_tag="aug_orb_texture",callback=__record_position,user_data=("Capture Augmentation Orb position", __update_aug_position),width=55, height=55)
                    dpg.add_image_button(texture_tag="chaos_orb_texture",callback=__record_position,user_data=("Capture Chaos Orb position", __update_chaos_position),width=55, height=55)
                with dpg.group(horizontal=True):  
                    dpg.add_image_button(texture_tag="alch_orb_texture", callback=__record_position, user_data=("Capture Alchemy Orb position", __update_alch_position), width=55, height=55)
                    dpg.add_image_button(texture_tag="scour_orb_texture",callback=__record_position,user_data=("Capture Scouring Orb position", __update_scour_position),width=55, height=55)
                    dpg.add_image_button(texture_tag="map_texture", callback=__record_map_positions, user_data=(__update_map_first_position, __update_map_second_position), width=55, height=55)

        with dpg.group(horizontal=True):
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
            dpg.add_text(default_value="Set pause after each PyAutoGui action (should be higher than ingame ping)")
            
        dpg.add_checkbox(
            tag=gui_tags.PERFORMANCE_LOGGING_TAG,
            label="Enable performance logging",
            default_value=manager.cfg.app_settings.enable_performance_logging
        )
