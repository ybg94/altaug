import dearpygui.dearpygui as dpg
from .. import crafting_processor
from .. import gui_tags
from . import constants
from . import elements

def init(crafting_window_tag: int | str) -> None:
    def combo_callback(sender, app_data):
        target_values = [constants.CRAFTING_TARGETS[1]]
        if app_data in target_values:
            dpg.show_item(gui_tags.MAP_HIDDEN_GROUP_TAG)
        else:
            dpg.hide_item(gui_tags.MAP_HIDDEN_GROUP_TAG)

    with dpg.window(tag=crafting_window_tag, label="Crafting target", no_close=True):
        elements.add_button(label="Open RegEx Library", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=True))

        with dpg.group(horizontal=True):
            dpg.add_text("Select crafting target:")
            dpg.add_combo(tag=gui_tags.CRAFTING_TARGET_COMBO_TAG, items=constants.CRAFTING_TARGETS, default_value=constants.CRAFTING_TARGETS[0], width=128, callback=combo_callback)
            
            with dpg.group(tag=gui_tags.MAP_HIDDEN_GROUP_TAG, show=False, horizontal=True):
                dpg.add_text("Number of maps to craft:")
                dpg.add_input_int(tag=gui_tags.MAP_AMOUNT_INPUT_TAG, default_value=5, width=128)

        dpg.add_text("RegEx input (crafting stops when RegEx matches the item)")
        dpg.add_text("When copying from poe.re make sure to NOT include quotes")
        dpg.add_input_text(tag=gui_tags.REGEX_INPUT_TAG, height=48, width=764)

        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Max crafting attempts:")
            dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, default_value=10, width=128)

        elements.add_button(label="Start crafting", callback=crafting_processor.start_crafting)

