from datetime import datetime
from typing import Callable
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

def use_regex(regex_text: str, max_currency_use: int) -> None:
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
        crating_function = autogui.use_alch if not t17 else autogui.use_chaos
        currency_used = 0

        for map_count in range(1, map_amount + 1):
            logging.info(f"Map {map_count}, Total currency used: {currency_used}")

            description = autogui.get_map_description(map_count)
            item_info = item_processing.ItemInfo(description)
            if item_info.match(regex, is_regex_inverted):
                logging.info(f"Map {map_count} has matched the criteria, moving on to next map.")
                continue

            while currency_used < max_currency_use:
                item = __apply_craft(craft_func=crating_function, map_count=map_count)
                currency_used += 1

                if item.match(regex, is_regex_inverted):
                    logging.info(f"Map {map_count} has matched the criteria, moving on to next map.")
                    break
                elif not t17:
                    autogui.use_scour(map_count)
                pass

            if (currency_used == max_currency_use):
                logging.info(f"Used all allowed currency, stopping the crafting.")
                break
            pass
        logging.info(f"Finished crafting {map_count} maps, total currency used: {currency_used}.")

    elif (target == CraftingTarget.GEAR):
        item = item_processing.ItemInfo(autogui.get_item_advanced_description())

        if item.match(regex):
            logging.info(f"Item already has correct modifiers")
            return
        
        for currency_used in range(1, max_currency_use + 1):
            item = __apply_craft(autogui.use_alt)
            if item.match(regex):
                logging.info(f"Total currency used #{currency_used}: success")
                break

            if item.is_affixes_full():
                continue

            item = __apply_craft(autogui.use_aug)
            if item.match(regex):
                logging.info(f"Total currency used #{currency_used}: success")
                break

            logging.info(f"Total currency used #{currency_used}: fail...")
    pass

def start_crafting() -> None:
    regex_input: str = dpg.get_value(gui_tags.REGEX_INPUT_TAG)
    max_currency_use: int = dpg.get_value(gui_tags.MAX_ATTEMPT_INPUT_TAG)
    if (len(regex_input) == 0):
        logging.info("No regex detected, ensure a regex is present before beginning crafting.")

    #sleep to give user 3 seconds to switch to PoE client
    time.sleep(3)

    start_time: datetime = datetime.now()
    logging.info(f"🔹 Started rolling at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    use_regex(regex_input, max_currency_use)

    # --- End timestamp ---
    end_time = datetime.now()
    elapsed = end_time - start_time
    logging.info(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")
