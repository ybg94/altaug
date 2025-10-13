import logging
import os
import time
import dearpygui.dearpygui as dpg
import pyautogui
from .. import config_manager as cfg
from .. import gui_tags
from . import elements

def capture_image_position(image_file_name: str) -> tuple[int, int] | None:
    width, height = pyautogui.size()
    match height:
        case 1080:
            pass
        case 1440:
            split = image_file_name.split(os.path.extsep)
            assert(len(split) == 2)
            image_file_name = f"{split[0]}_1440{os.path.extsep}{split[1]}"
        case _:
            raise NotImplementedError("Auto-configure is only supported for 1080p and 1440p resolutions.")

    image_path = os.path.join('Images', image_file_name)
    try:
        x, y = pyautogui.locateCenterOnScreen(image_path)
        logging.info(f"Found image {image_file_name} at ({x}, {y})")
        return (x, y)

    except pyautogui.ImageNotFoundException:
        logging.error(f"Wasn't able to find the image on screen: {image_file_name}.")
        return None
    except Exception:
        logging.error(f"An unexpected error occurred.", exc_info=True)
        return None
    
def capture_and_record_position(image_file_name: str, config_category: str, config_item_prefix: str) -> None:
    position = capture_image_position(image_file_name)
    if position:
        x, y = position
        screen_x, screen_y = pyautogui.size()
        position_ratio_x: float = x / screen_x
        position_ratio_y: float = y / screen_y

        config_values = [
            (config_category, f'{config_item_prefix}_x', '%.3f' % position_ratio_x),
            (config_category, f'{config_item_prefix}_y', '%.3f' % position_ratio_y)
        ]

        cfg.update_config(config_values)
    pass

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

def __record_position(sender, app_data, user_data: tuple[str, str]) -> None:
    dpg.configure_item(gui_tags.CONFIGURATION_INFO_MODAL_TAG, show=True)

    position = __get_target_position()
    if position:
        x, y = position
        width, height = pyautogui.size()
        ratio_x = x / width
        ratio_y = y / height

        config_items = [
            (user_data[0], f'{user_data[1]}_x', '%.3f' % ratio_x),
            (user_data[0], f'{user_data[1]}_y', '%.3f' % ratio_y),
        ]
        cfg.update_config(config_items)
        pass

    dpg.configure_item(gui_tags.CONFIGURATION_INFO_MODAL_TAG, show=False)    
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
    with dpg.window(tag=gui_tags.CONFIGURATION_INFO_MODAL_TAG, modal=True, show=False, no_title_bar=True, pos=(302, 70), width=178, height=60, no_resize=True, no_move=True):
        dpg.add_text(default_value="Press Space to record")
        dpg.add_text(default_value="Press Esc to cancel")
        pass

    with dpg.window(tag=configuration_window_tag, label="Configuration", no_close=True):
        dpg.add_text(default_value="Must restart script to apply config changes")

        with dpg.group(horizontal=True):
            elements.add_button(label="Capture Alteration orb position", callback=__record_position, user_data=('Coordinates', 'alt'))
            elements.add_button(label="Capture Augmentation orb position", callback=__record_position, user_data=('Coordinates', 'aug'))

        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Set pause after each PyAutoGui action:")
            dpg.add_input_float(
                tag=gui_tags.PYAUTOGUI_PAUSE_TAG,
                default_value=0.03,
                max_value=1.0,
                max_clamped=True,
                min_value=0.025,
                min_clamped=True,
                step=0.005,
                callback=__set_pyautogui_pause,
                width=100
            )

        dpg.add_checkbox(
            label="Enable PyAutoGUI Failsafe",
            default_value=True,
            tag=gui_tags.PYAUTOGUI_FAILSAFE_TOGGLE_TAG,
            callback=__toggle_autogui_failsafe
        )
        dpg.add_checkbox(label="Enable performance logging", tag=gui_tags.PERFORMANCE_LOGGING_TAG)
