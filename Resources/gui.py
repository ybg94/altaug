import logging
import os
import dearpygui.dearpygui as dpg
import pyautogui
from . import config_manager as cfg
from . import crafting_processor as crafting_processor
from . import gui_tags as gui_tags
from . import logging_handlers

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

def init_gui() -> None:
    dpg.create_context()
    dpg.configure_app(init_file=os.path.join('src', 'gui_layout.ini'), docking=True, docking_space=True)

    try:
        with dpg.font_registry():
            with dpg.font(os.path.join(os.environ['WINDIR'], 'Fonts', 'seguiemj.ttf'), 16) as emoji_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range(0x2600, 0x26FF) # Miscellaneous Symbols
                dpg.add_font_range(0x2700, 0x27BF) # Dingbats
                dpg.add_font_range(0x1F300, 0x1F6FF) # Misc Symbols and Pictographs

        dpg.bind_font(emoji_font)
    except Exception:
        logging.error('Unable to load Bahnschrift font, using default.', exc_info=True)

    dpg.create_viewport(title="Alt-Aug GUI", width=800, height=650)

    configuration_window = dpg.generate_uuid()
    crafting_window = dpg.generate_uuid()
    script_log = dpg.generate_uuid()

    with dpg.window(tag=configuration_window, label="Configuration"):
        dpg.add_text(default_value="Must restart script to apply config changes")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Capture Alteration orb position", callback=capture_alt_position)
            dpg.add_button(label="Capture Augmentation orb position", callback=capture_aug_position)
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label="Enable PyAutoGUI Failsafe",
                default_value=True,
                tag=gui_tags.PYAUTOGUI_FAILSAFE_TOGGLE_TAG,
                callback=toggle_autogui_failsafe
            )
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
            dpg.add_text(default_value="Set PAUSE (Recommended 0.03)")
        dpg.add_checkbox(label="Enable performance logging", tag=gui_tags.PERFORMANCE_LOGGING_TAG)

    with dpg.window(tag=crafting_window, label="Crafting goal input"):
        dpg.add_text("Enter regex for 'Regex' mode (supports poe.re with 'Match an open affix = OFF'):")
        dpg.add_input_text(tag=gui_tags.REGEX_INPUT_TAG)
        dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, label="Max crafting attempts", default_value=10)
        dpg.add_button(label="Start crafting", callback=crafting_processor.start_crafting)

    with dpg.window(tag=script_log, label="Script log"):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag=gui_tags.OUTPUT_LOG_TAG,
                multiline=True,
                readonly=True,
                width=700,
                height=250
            )
            dpg.add_button(label="Clear", callback=lambda: dpg.set_value(gui_tags.OUTPUT_LOG_TAG, ""))

    gui_log_handler = logging_handlers.GuiLogHandler(tag=gui_tags.OUTPUT_LOG_TAG, level=logging.INFO)
    gui_log_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
    logging.getLogger().addHandler(gui_log_handler)

    set_pyautogui_pause()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()