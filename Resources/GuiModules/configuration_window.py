import os
import logging
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

def capture_alt_position() -> None:
    capture_and_record_position('alt_in_currency_tab.png', 'Coordinates', 'alt')

def capture_aug_position() -> None:
    capture_and_record_position('aug_in_currency_tab.png', 'Coordinates', 'aug')

def toggle_autogui_failsafe() -> None:
    value = dpg.get_value(gui_tags.PYAUTOGUI_FAILSAFE_TOGGLE_TAG)
    logging.debug(f"Failsafe checkbox state is {value}.")
    pyautogui.FAILSAFE = value

def set_pyautogui_pause() -> None:
    value = dpg.get_value(gui_tags.PYAUTOGUI_PAUSE_TAG)
    logging.debug(f"Setting PAUSE to {value}.")
    pyautogui.PAUSE = value

def init(configuration_window_tag: int | str) -> None:
    with dpg.window(tag=configuration_window_tag, label="Configuration", no_close=True):
        dpg.add_text(default_value="Must restart script to apply config changes")

        with dpg.group(horizontal=True):
            elements.add_button(label="Capture Alteration orb position", callback=capture_alt_position)
            elements.add_button(label="Capture Augmentation orb position", callback=capture_aug_position)

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
                callback=set_pyautogui_pause,
                width=100
            )

        dpg.add_checkbox(
            label="Enable PyAutoGUI Failsafe",
            default_value=True,
            tag=gui_tags.PYAUTOGUI_FAILSAFE_TOGGLE_TAG,
            callback=toggle_autogui_failsafe
        )
        dpg.add_checkbox(label="Enable performance logging", tag=gui_tags.PERFORMANCE_LOGGING_TAG)
