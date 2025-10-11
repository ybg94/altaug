import dearpygui.dearpygui as dpg

DEFAULT_BUTTON_HEIGHT = 32

def add_button(**kwargs) -> int | str:
    if 'height' not in kwargs:
        kwargs['height'] = DEFAULT_BUTTON_HEIGHT

    return dpg.add_button(**kwargs)