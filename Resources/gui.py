import dearpygui.dearpygui as dpg
import io
import os
import pyautogui
import sys
import Resources.config_manager as cfg
import Resources.crafting_processor as crafting_processor
import Resources.gui_tags as gui_tags

class RedirectText(io.StringIO):
    def __init__(self, tag) -> None:
        super().__init__()
        self.tag = tag

    def write(self, input: str) -> None:
        current: str = dpg.get_value(self.tag)
        dpg.set_value(self.tag, current + input)

def capture_image_position(image_file_name: str) -> tuple[int, int] | None:
    try:
        image_path = os.path.join('Images', image_file_name)
        x, y = pyautogui.locateCenterOnScreen(image_path)
        pyautogui.moveTo(x, y)
        print(f"Found image {image_file_name} at ({x}, {y})")
        return (x, y)

    except pyautogui.ImageNotFoundException as ex:
        print(f"Wasn't able to find the image on screen: {image_file_name}, {ex}")
        return None
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
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
    capture_and_record_position('alt_in_currancy_tab.png', 'Coordinates', 'alt')

def capture_aug_position() -> None:
    capture_and_record_position('aug_in_currancy_tab.png', 'Coordinates', 'aug')

def init_gui() -> None:
    dpg.create_context()
    dpg.configure_app(init_file=os.path.join('src', 'gui_layout.ini'), docking=True, docking_space=True)

    try:
        with dpg.font_registry():
            dpg.add_font('C:\\Windows\\Fonts\\Bahnschrift.ttf', 16, tag="best_font")

        dpg.bind_font("best_font")
    except Exception as ex:
        print('Unable to load Bahnschrift font, using default')

    dpg.create_viewport(title="Alt-Aug GUI", width=800, height=600)

    configuration_window = dpg.generate_uuid()
    crafting_window = dpg.generate_uuid()
    script_log = dpg.generate_uuid()

    with dpg.window(tag=configuration_window, label="Configuration"):
        dpg.add_text(default_value="Must restart script to apply config changes")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Capture Alteraton orb position", callback=capture_alt_position)
            dpg.add_button(label="Capture Augmentation orb position", callback=capture_aug_position)

    with dpg.window(tag=crafting_window, label="Crafting goal input"):
        dpg.add_text("Enter regex for 'Regex' mode (supports poe.re with 'Match an open affix = OFF'):")
        dpg.add_input_text(tag=gui_tags.REGEX_INPUT_TAG)
        dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, label="Max crafting attempts", default_value=10)
        dpg.add_button(label="Start crafting", callback=crafting_processor.start_crafting)

    with dpg.window(tag=script_log, label="Script log"):
        dpg.add_input_text(
            tag=gui_tags.OUTPUT_LOG_TAG,
            multiline=True,
            readonly=True,
            height=250
        )

    sys.stdout = RedirectText(gui_tags.OUTPUT_LOG_TAG)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()