import dearpygui.dearpygui as dpg
from . import constants
from . import elements
from .. import crafting_processor
from .. import gui_tags
from ..config_manager import manager

def init(crafting_window_tag: int | str) -> None:
    MAX_CURRENCY_HINT = """When the craft uses multiple currency stacks, max currency
refers the highest amount used from one of the stacks

e.g.: when crafting with alt/aug with 20 currency max,
      the process will stop when 20 alts are used"""

    def combo_callback(sender, app_data):
        show_map = (app_data == constants.CraftingTarget.MAPS)
        dpg.configure_item(gui_tags.MAP_HIDDEN_GROUP_TAG, show=show_map)

        show_affix = (app_data == constants.CraftingTarget.GEAR)
        dpg.configure_item(gui_tags.AFFIX_HIDDEN_GROUP_TAG, show=show_affix)

    def affix_checkbox_callback(sender, app_data):
        if not app_data:
            return
        if sender == gui_tags.AFFIX_PREFIX_CHECK:
            dpg.set_value(gui_tags.AFFIX_SUFFIX_CHECK, False)
        elif sender == gui_tags.AFFIX_SUFFIX_CHECK:
            dpg.set_value(gui_tags.AFFIX_PREFIX_CHECK, False)

    with dpg.window(tag=crafting_window_tag, label="Crafting target", no_close=True):
        elements.add_button(label="Open RegEx Library", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=True))

        with dpg.group(horizontal=True):
            dpg.add_text("Select crafting target:")
            default_crafting_target = manager.cfg.last_state.crafting_target
            dpg.add_combo(tag=gui_tags.CRAFTING_TARGET_COMBO_TAG, items=constants.CRAFTING_TARGETS, default_value=default_crafting_target, width=128, callback=combo_callback)
            
            default_group_map_show = True if default_crafting_target == constants.CraftingTarget.MAPS else False
            with dpg.group(tag=gui_tags.MAP_HIDDEN_GROUP_TAG, show=default_group_map_show, horizontal=True):
                dpg.add_text("Number of maps to craft:")
                dpg.add_input_int(tag=gui_tags.MAP_AMOUNT_INPUT_TAG, default_value=manager.cfg.last_state.map_craft_amount, width=128)
                dpg.add_text("T17")
                dpg.add_checkbox(tag=gui_tags.MAP_TYPE_CHECK, default_value=manager.cfg.last_state.is_t17)
            
            default_group_affix_show = True if default_crafting_target == constants.CraftingTarget.GEAR else False
            with dpg.group(tag=gui_tags.AFFIX_HIDDEN_GROUP_TAG, show=default_group_affix_show, horizontal=True):
                dpg.add_text("Only looking for:")
                dpg.add_text("Prefix")
                dpg.add_checkbox(tag=gui_tags.AFFIX_PREFIX_CHECK, default_value=manager.cfg.last_state.is_pre, callback=affix_checkbox_callback)
                dpg.add_text("Suffix")
                dpg.add_checkbox(tag=gui_tags.AFFIX_SUFFIX_CHECK, default_value=manager.cfg.last_state.is_suff, callback=affix_checkbox_callback)

        dpg.add_text("RegEx input (crafting stops when RegEx matches the item)")
        dpg.add_text("When copying from poe.re make sure to NOT include quotes")
        dpg.add_input_text(tag=gui_tags.REGEX_INPUT_TAG, height=48, width=764, default_value=manager.cfg.last_state.regex_string)

        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Max currency to use:")
            dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, default_value=manager.cfg.last_state.max_currency_use, width=128)
            with dpg.tooltip(gui_tags.MAX_ATTEMPT_INPUT_TAG):
                dpg.add_text(MAX_CURRENCY_HINT)

        elements.add_button(label="Start crafting", callback=crafting_processor.start_crafting)

