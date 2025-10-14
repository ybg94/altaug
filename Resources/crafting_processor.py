from datetime import datetime
from typing import Callable, Any
import logging
import re
import time
import dearpygui.dearpygui as dpg
import pyperclip
from .GuiModules.constants import CraftingTarget
from . import decorators
from . import autogui
from . import gui_tags
from . import read_file
from . import item_processing

def use_json(max_attempts: int) -> None:
    active_affixes, base_names = read_file.read_json_data()
    active_base = autogui.check_active_base(base_names)

    #for affix in active_affixes:
    #    print(affix[0]) 0 will return the affix Name
    #    print(affix[1]) 1 will return Prefix or Suffix

    found_affix = False
    attempts = 0

    while not found_affix and attempts < max_attempts:
        attempts += 1

        # Copy item text
        autogui.copy_item()

        # Check clipboard against all known affixes
        for affix in active_affixes:
            if autogui.check_clipboard_for(affix[0]):
                logging.info(f"✅ Found the modifier '{affix[0]}' on attempt #{attempts}")
                found_affix = True
                break

        # If still not found, use Alteration and reroll
        if not found_affix:
            #logging.info(f"No affix found (attempt #{attempts}). Using Alteration orb...")
            autogui.use_alt()

            # Copy the new item and analyze prefixes/suffixes
            autogui.copy_item()
            item_name = autogui.get_item_name()

            if item_name:
                before, _, after = item_name.partition(active_base)
                prefix = before.strip()
                suffix = after.strip()

                if prefix and suffix:
                    logging.info(f"Prefix: {prefix} | Suffix: {suffix}")
                elif prefix and not suffix:
                    #logging.info("No suffix found → Using Augmentation orb.")
                    autogui.use_aug()
                elif not prefix and suffix:
                    #logging.info("No prefix found → Using Augmentation orb.")
                    autogui.use_aug()
                else:
                    logging.info("Normal item (no affixes).")
            else:
                logging.error("Could not read item name after alteration.")

    if not found_affix:
        logging.info(f"⚠️ No matching affix found after {max_attempts} attempts.")
    else:
        logging.info(f"🎯 Success after {attempts} attempts.")

    # found_affix = False
    # while not found_affix:
    #     autogui.copy_item()
    #     for affix in active_affixes:
    #         check_paste = autogui.check_clipboard_for(affix[0])
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

@decorators.timeit
def __apply_craft(craft_func: Callable[..., None], map_count: int | None = None) -> item_processing.ItemInfo:
    if map_count is not None:
        craft_func(map_count)
    else:
        craft_func()

    adv_desc: str = autogui.get_map_description(map_count) if map_count is not None else autogui.get_item_advanced_description()
    item_info = item_processing.ItemInfo(adv_desc)

    logs: list[str] = item_info.get_affix_logs(True if map_count is not None else False)
    logs.append(f"After executing {craft_func.__name__}")
    log = ''.join(logs)
    logging.info(log)

    return item_info

def use_regex(regex_text: str, max_attempts: int) -> None:
    logging.info(f"Using regex method with pattern: {regex_text}")
    regex: re.Pattern
    is_regex_inverted = regex_text.startswith('!')
    if is_regex_inverted:
        regex = re.compile(regex_text[1:], re.MULTILINE | re.IGNORECASE)
    else:
        regex = re.compile(regex_text, re.MULTILINE | re.IGNORECASE)

    target = dpg.get_value(gui_tags.CRAFTING_TARGET_COMBO_TAG)
    if (target == CraftingTarget.MAPS):
        map_amount = dpg.get_value(gui_tags.MAP_AMOUNT_INPUT_TAG)
        attempt = 1
        map_count = 1

        while attempt <= max_attempts and map_count <= map_amount:
            logging.info(f"Map {map_count}, attempt: {attempt}")

            item = __apply_craft(craft_func=autogui.use_alch, map_count=map_count)
            if item.match(regex, is_regex_inverted):
                logging.info(f"Map {map_count} has matched the criteria, moving on to next map.")
                map_count += 1
            else:
                autogui.use_scour(map_count)
            attempt += 1

    elif (target == CraftingTarget.GEAR):
        item = item_processing.ItemInfo(autogui.get_item_advanced_description())

        if item.match(regex):
            logging.info(f"Item already has correct modifiers")
            return
        
        for attempt in range(max_attempts):
            item = __apply_craft(autogui.use_alt)
            if item.match(regex):
                logging.info(f"Attempt #{attempt}: success")
                break

            if item.is_affixes_full():
                continue

            item = __apply_craft(autogui.use_aug)
            if item.match(regex):
                logging.info(f"Attempt #{attempt}: success")
                break

            logging.info(f"Attempt #{attempt}: fail...")
    pass

def start_crafting() -> None:
    regex_input: str = dpg.get_value(gui_tags.REGEX_INPUT_TAG)
    max_attempts: int = dpg.get_value(gui_tags.MAX_ATTEMPT_INPUT_TAG)

    #sleep to give user 3 seconds to switch to PoE client
    time.sleep(3)

    start_time: datetime = datetime.now()
    logging.info(f"🔹 Started rolling at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if (len(regex_input) > 0):
        use_regex(regex_input, max_attempts)
    else:
        use_json(max_attempts)

    # --- End timestamp ---
    end_time = datetime.now()
    elapsed = end_time - start_time
    logging.info(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")