import dearpygui.dearpygui as dpg
from . import elements
from .. import gui_tags

def init(script_log_tag: int | str, default_open: bool = True) -> None:
    with dpg.collapsing_header(tag=script_log_tag, label="Script log", default_open=default_open):
        with dpg.group(horizontal=True):
            elements.add_button(label="Clear log", callback=lambda: dpg.set_value(gui_tags.OUTPUT_LOG_TAG, ""))
        with dpg.group(horizontal=False, width=-1):
            dpg.add_input_text(
                tag=gui_tags.OUTPUT_LOG_TAG,
                multiline=True,
                readonly=True,
                width=-1,
                height=-1     
            )