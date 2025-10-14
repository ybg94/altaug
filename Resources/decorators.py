from typing import TypeVar, Callable, Dict, Any
import logging
import time
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

    wrapper.__name__ = func.__name__
    return wrapper

T = TypeVar('TClass')
def singleton(cls: Callable[..., T]) -> Callable[..., T]:
    instances: Dict[type, T] = {}

    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
