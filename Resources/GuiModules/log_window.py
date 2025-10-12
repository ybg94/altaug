import dearpygui.dearpygui as dpg
from .. import gui_tags
from . import elements

def init(script_log_tag: int | str) -> None:
    with dpg.window(tag=script_log_tag, label="Script log", no_close=True):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag=gui_tags.OUTPUT_LOG_TAG,
                multiline=True,
                readonly=True,
                width=700,
                height=250
            )
            elements.add_button(label="Clear", callback=lambda: dpg.set_value(gui_tags.OUTPUT_LOG_TAG, ""))