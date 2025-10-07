#Authors billy_smalls and kipper86

import dearpygui.dearpygui as dpg
import Resources.read_config
import Resources.read_file
import Resources.autogui
import Resources.gui_tags as gui_tags
import Resources.config_manager as cfg
import pyautogui
import time
from datetime import datetime
import sys
import io
import os

class RedirectText(io.StringIO):
    def __init__(self, tag) -> None:
        super().__init__()
        self.tag = tag

    def write(self, input: str) -> None:
        current: str = dpg.get_value(self.tag)
        dpg.set_value(self.tag, current + input)

def use_json(max_attempts: int) -> None:
    CONFIG_DATA = Resources.read_config.read_config()
    active_affixes, base_names = Resources.read_file.read_json_data()
    #sleep to give user 3 seconds to switch to PoE client
    time.sleep(3)
    active_base = Resources.autogui.check_active_base(base_names)

    #for affix in active_affixes:
    #    print(affix[0]) 0 will return the affix Name
    #    print(affix[1]) 1 will return Prefix or Suffix

    found_affix = False
    attempts = 0

    while not found_affix and attempts < max_attempts:
        attempts += 1

        # Copy item text
        Resources.autogui.copy_item()

        # Check clipboard against all known affixes
        for affix in active_affixes:
            if Resources.autogui.check_clipboard_for(affix[0]):
                print(f"✅ Found the modifier '{affix[0]}' on attempt #{attempts}")
                found_affix = True
                break

        # If still not found, use Alteration and reroll
        if not found_affix:
            #print(f"No affix found (attempt #{attempts}). Using Alteration orb...")
            Resources.autogui.use_alt()

            # Copy the new item and analyze prefixes/suffixes
            Resources.autogui.copy_item()
            item_name = Resources.autogui.get_item_name()

            if item_name:
                before, _, after = item_name.partition(active_base)
                prefix = before.strip()
                suffix = after.strip()

                if prefix and suffix:
                    print(f"Prefix: {prefix} | Suffix: {suffix}")
                elif prefix and not suffix:
                    #print("No suffix found → Using Augmentation orb.")
                    Resources.autogui.use_aug()
                elif not prefix and suffix:
                    #print("No prefix found → Using Augmentation orb.")
                    Resources.autogui.use_aug()
                else:
                    print("Normal item (no affixes).")
            else:
                print("Error: could not read item name after alteration.")

    if not found_affix:
        print(f"⚠️ No matching affix found after {max_attempts} attempts.")
    else:
        print(f"🎯 Success after {attempts} attempts.")

    # found_affix = False
    # while not found_affix:
    #     Resources.autogui.copy_item()
    #     for affix in active_affixes:
    #         check_paste = Resources.autogui.check_clipboard_for(affix[0])
    #         if check_paste:
    #             print(f"Found the modifier '{affix[0]}'")
    #             found_affix = True
    #         else:
    #             found_affix = True

        #else if affix['affix] == Pre
            #if item has open pre
                #aug
                #check paste
        #else if affix['affix'] == Suff
            #if item has open suff
                #aug
                #check paste
        #else
            #alt 
            #loop and it will check affixes at start of loop again

        
def use_regex(regex_text: str, max_attempts: int) -> None:
    print(f"You have entered: {regex_text}")

def start_crafting(sender, app_data, user_data):
    regex_input: str = dpg.get_value(gui_tags.REGEX_INPUT_TAG)
    max_attempts: int = dpg.get_value(gui_tags.MAX_ATTEMPT_INPUT_TAG)

    start_time: datetime = datetime.now()
    print(f"🔹 Started rolling at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if (len(regex_input) > 0):
        use_regex(regex_input, max_attempts)
    else:
        use_json(max_attempts)

    # --- End timestamp ---
    end_time = datetime.now()
    elapsed = end_time - start_time
    print(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")

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

dpg.create_context()
dpg.configure_app(init_file=os.path.join('src', 'gui_layout.ini'), docking=True, docking_space=True)
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
    dpg.add_text("Enter regex for 'Regex' mode:")
    dpg.add_input_text(tag=gui_tags.REGEX_INPUT_TAG)
    dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, label="Max crafting attempts", default_value=10)
    dpg.add_button(label="Start crafting", callback=start_crafting)

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
