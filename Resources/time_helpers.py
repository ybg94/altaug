import time
import logging
import dearpygui.dearpygui as dpg
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