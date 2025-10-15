from datetime import datetime
from typing import Callable, Any
import logging
import re
import time
import dearpygui.dearpygui as dpg
from .GuiModules.constants import CraftingTarget
from . import decorators
from . import autogui
from . import gui_tags
from . import item_processing

@decorators.timeit
def __apply_craft(craft_func: Callable[..., None], map_count: int | None = None) -> item_processing.ItemInfo:
    if map_count is not None:
        craft_func(map_count)
    else:
        craft_func()

    adv_desc: str = autogui.get_map_description(map_count) if map_count is not None else autogui.get_item_advanced_description()
    item_info = item_processing.ItemInfo(adv_desc)
    if map_count is None:
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
        t17 = dpg.get_value(gui_tags.MAP_TYPE_CHECK)
        attempt = 1
        map_count = 1

        while attempt <= max_attempts and map_count <= map_amount:
            logging.info(f"Map {map_count}, attempt: {attempt}")
            crating_function = autogui.use_alch if not t17 else autogui.use_chaos

            if t17:
                description = autogui.get_map_description(map_count)
                item_info = item_processing.ItemInfo(description)
                if item_info.match(regex, is_regex_inverted):
                    logging.info(f"Map {map_count} has matched the criteria, moving on to next map.")
                    map_count += 1
                    continue

            item = __apply_craft(craft_func=crating_function, map_count=map_count)

            if item.match(regex, is_regex_inverted):
                logging.info(f"Map {map_count} has matched the criteria, moving on to next map.")
                map_count += 1
            elif not t17:
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
        logging.info("No regex detected, ensure a regex is present before beginning crafting.")

    # --- End timestamp ---
    end_time = datetime.now()
    elapsed = end_time - start_time
    logging.info(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")