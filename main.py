#Authors billy_smalls and kipper86

import dearpygui.dearpygui as dpg
import Resources.read_config
import Resources.read_file
import Resources.autogui
import pyautogui
import time
from datetime import datetime
import sys
import io

class RedirectText(io.StringIO):
    def __init__(self, tag) -> None:
        super().__init__()
        self.tag = tag

    def write(self, input: str) -> None:
        current: str = dpg.get_value(self.tag)
        dpg.set_value(self.tag, current + input)

def use_json() -> None:
    CONFIG_DATA = Resources.read_config.read_config()
    active_affixes, base_names = Resources.read_file.read_json_data()
    start_time = datetime.now()
    print(f"🔹 Started rolling at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    #sleep to give user 3 seconds to switch to PoE client
    time.sleep(3)
    active_base = Resources.autogui.check_active_base(base_names)

    #for affix in active_affixes:
    #    print(affix[0]) 0 will return the affix Name
    #    print(affix[1]) 1 will return Prefix or Suffix

    MAX_ATTEMPTS = 10  # safety cap so it doesn't loop forever
    found_affix = False
    attempts = 0

    while not found_affix and attempts < MAX_ATTEMPTS:
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

    # --- End timestamp ---
    end_time = datetime.now()
    elapsed = end_time - start_time

    if not found_affix:
        print(f"⚠️ No matching affix found after {MAX_ATTEMPTS} attempts.")
    else:
        print(f"🎯 Success after {attempts} attempts.")

    print(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")

    found_affix = False
    while not found_affix:
        Resources.autogui.copy_item()
        for affix in active_affixes:
            check_paste = Resources.autogui.check_clipboard_for(affix[0])
            if check_paste:
                print(f"Found the modifier '{affix[0]}'")
                found_affix = True
            else:
                found_affix = True

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

        
def use_regex(regex_text: str) -> None:
    print(f"You have entered: {regex_text}")

def start_crafting(sender, app_data, user_data):
    regex_input: str = dpg.get_value("regex_input")
    if (len(regex_input) > 0):
        use_regex(regex_input)
    else:
        use_json()

dpg.create_context()
dpg.create_viewport(title="Alt-Aug GUI", width=600, height=600)

with dpg.window(label="Crafting goal input", width=600, height=600):
    dpg.add_text("Enter regex for 'Regex' mode:")
    dpg.add_input_text(tag="regex_input")
    dpg.add
    dpg.add_button(label="Start crafting", callback=start_crafting)
    dpg.add_text("Script log")
    dpg.add_input_text(
        tag="output_log",
        multiline=True,
        readonly=True,
        width=570,
        height=300
    )

sys.stdout = RedirectText("output_log")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
