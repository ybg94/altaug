from enum import StrEnum
from typing import Callable 
import logging
import time
import dearpygui.dearpygui as dpg
import pyautogui
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
    dpg.set_item_label(gui_tags.CONFIGURATION_INFO_TEXT_TAG, app_data)
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

def __update_item_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.item = new_pos
    return new_config

def __update_map_first_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.map_top_left = new_pos
    return new_config

def __update_map_second_position(config: Configuration, new_pos: tuple[int, int]) -> Configuration:
    new_config = config
    new_config.coordinates.map_bottom_right = new_pos
    return new_config

def __record_map_positions(sender, app_data, config_updater) -> None:
    __record_position(sender=sender, app_data="Capture Top-Left Map corner", config_updater=__update_map_first_position)

    while dpg.is_key_down(dpg.mvKey_Spacebar) or dpg.is_key_down(dpg.mvKey_Escape):
        time.sleep(1 / 20)

    __record_position(sender=sender, app_data="Capture Bottom-Right Map corner", config_updater=__update_map_second_position)
    pass

class CoordinateLocation(StrEnum):
    Pending = 'Capture position for...'
    Item = 'Item'
    Map = 'Map'
    Alt = 'Alteration orb'
    Aug = 'Augmentation orb'
    Alch = 'Alchemy orb'
    Scour = 'Scouring orb'
    Chaos = 'Chaos orb'

callback_lookup: dict[
    CoordinateLocation,
    tuple[Callable[..., Configuration], None], Callable[..., Configuration]
] = {
    CoordinateLocation.Item: (__record_position, __update_item_position),
    CoordinateLocation.Map: (__record_map_positions, __update_map_first_position),
    CoordinateLocation.Alt: (__record_position, __update_alt_position),
    CoordinateLocation.Aug: (__record_position, __update_aug_position),
    CoordinateLocation.Alch: (__record_position, __update_alch_position),
    CoordinateLocation.Scour: (__record_position, __update_scour_position),
    CoordinateLocation.Chaos: (__record_position, __update_chaos_position),
}
modal_title_lookup: dict[CoordinateLocation, str] = {
    CoordinateLocation.Item: 'Capture Item position',
    CoordinateLocation.Map: 'This is hardcoded in __record_map_positions',
    CoordinateLocation.Alt: 'Capture Alteration orb position',
    CoordinateLocation.Aug: 'Capture Augmentation orb position',
    CoordinateLocation.Alch: 'Capture Alchemy orb position',
    CoordinateLocation.Scour: 'Caption Scouring orb position',
    CoordinateLocation.Chaos: 'Capture Chaos orb position',
}

def __update_select_target_state(sender, app_data) -> None:
    is_show = app_data != CoordinateLocation.Pending
    dpg.configure_item(gui_tags.CONFIGURATION_CONFIGURE_BTN_TAG, show=is_show)
    pass

def __select_configuration_handler() -> None:
    target = CoordinateLocation(dpg.get_value(gui_tags.CONFIGURATION_TARGET_COMBO_TAG))
    record_callback, update_callback = callback_lookup[target]
    record_callback(sender=gui_tags.CONFIGURATION_TARGET_COMBO_TAG, app_data=modal_title_lookup[target], config_updater=update_callback)
    pass

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
    with dpg.window(tag=gui_tags.CONFIGURATION_INFO_MODAL_TAG, modal=True, show=False, no_title_bar=True, pos=(302, 70), width=314, height=80, no_resize=True, no_move=True):
        dpg.add_spacer(height=2)
        dpg.add_button(tag=gui_tags.CONFIGURATION_INFO_TEXT_TAG, enabled=False, width=300)
        dpg.add_button(label="Press Space to record", enabled=False, width=300)
        dpg.add_button(label="Press Esc to cancel", enabled=False, width=300)
        pass

    with dpg.window(tag=configuration_window_tag, label="Configuration", no_close=True):
        with dpg.group(horizontal=True):
            dpg.add_combo(tag=gui_tags.CONFIGURATION_TARGET_COMBO_TAG, default_value=CoordinateLocation.Pending, items=[e.value for e in CoordinateLocation], callback=__update_select_target_state)
            dpg.add_button(tag=gui_tags.CONFIGURATION_CONFIGURE_BTN_TAG, label="Configure position", show=False, width=200, callback=__select_configuration_handler)

        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Set PyAutoGui PAUSE (should be >ping in game):")
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
