import logging
import re
import time
import dearpygui.dearpygui as dpg
from . import autogui
from . import gui_tags 

def timeit(func):
    def wrapper(*args, **kwargs):
        should_log = dpg.get_value(gui_tags.PERFORMANCE_LOGGING_TAG)
        if not should_log:
            return func(*args, **kwargs)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logging.info(f"{func.__name__} took {end - start:.6f} seconds.")
        return result
    return wrapper

affix_regex = re.compile(
    r"^{ (?:Master Crafted )?(?P<affix_type>Prefix|Suffix) Modifier \"(?P<affix_name>[\w\s']*)\" (?:\((?P<tier>(?:Rank|Tier): \d*)\))?[^(?:\r\n|\n|\r)]*$(?:\r\n|\n|\r)(?P<description>[^{]*)(?={?)",
    re.MULTILINE
)
def log_item_affixes(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        advanced_description = autogui.get_item_advanced_description()
        matches = affix_regex.finditer(advanced_description)
        logs: list[str] = ["Found item affixes:\n"]
        for match in matches:
            affix_type = match.group("affix_type")
            affix_name = match.group("affix_name")
            affix_tier = match.group("tier")
            affix_desc = match.group("description")
            affix_desc = affix_desc.replace("\r\n", " / ")
            affix_desc = affix_desc.replace("\n", " / ")

            logs.append(f"\t{affix_type} | {affix_name} | {affix_tier} | {affix_desc}\n")

        logs.append(f"{func.__name__} returned {result}")
        log = ''.join(logs)
        logging.info(log)

        return result
    return wrapper
