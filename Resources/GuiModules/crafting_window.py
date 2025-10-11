import dearpygui.dearpygui as dpg
from .. import crafting_processor
from .. import gui_tags
from . import elements

CRAFTING_TARGETS: list[str] = ["Gear", "Maps"]

def init(crafting_window_tag: int | str) -> None:
    with dpg.window(tag=crafting_window_tag, label="Crafting target", no_close=True):
        elements.add_button(label="Open RegEx Library", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=True))

        with dpg.group(horizontal=True):
            dpg.add_text("Select crafting target:")
            dpg.add_combo(tag=gui_tags.CRAFTING_TARGET_COMBO_TAG, items=CRAFTING_TARGETS, default_value=CRAFTING_TARGETS[0], width=128)

        dpg.add_text("RegEx input (crafting stops when RegEx matches the item):")
        dpg.add_input_text(tag=gui_tags.REGEX_INPUT_TAG, height=48)

        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Max crafting attempts:")
            dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, default_value=10, width=128)

        elements.add_button(label="Start crafting", callback=crafting_processor.start_crafting)
