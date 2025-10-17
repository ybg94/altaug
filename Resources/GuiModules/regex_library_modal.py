from typing import NamedTuple
import dearpygui.dearpygui as dpg
from . import constants
from . import elements
from .. import gui_tags
from .. import lookup_manager

class NewItemKey(NamedTuple):
    item_type: str
    item_base: str | None = None
    regex_title: str | None = None

regex_lookup: lookup_manager.RegexLookup
new_item_key: NewItemKey

def __selector_reset_ok_button() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_OK_TAG, show=False)
    pass

def __selector_reset_regex_preview() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_REGEX_PREVIEW_TAG, show=False)
    dpg.set_value(gui_tags.REGEX_WIZARD_SELECTOR_REGEX_PREVIEW_TAG, "")

    __selector_reset_ok_button()
    pass

def __selector_reset_regex_combo(should_hide: bool) -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_REGEX_TAG, constants.REGEX_TITLE_COMBO_DEFAULT)
    if should_hide:
        dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_REGEX_TAG, show=False)

    __selector_reset_regex_preview()
    pass

def __selector_reset_item_base_combo() -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_BASE_TAG, constants.ITEM_BASE_COMBO_DEFAULT)

    __selector_reset_regex_combo(should_hide=True)
    pass

def __selector_item_type_selected(sender, item_type: str) -> None:
    global regex_lookup
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_BASE_TAG, show=True, items=list(regex_lookup[item_type].keys()))

    __selector_reset_item_base_combo()
    pass

def __selector_item_base_selected(sender, item_base: str) -> None:
    global regex_lookup
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_TYPE_TAG)
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_REGEX_TAG, show=True, items=list(regex_lookup[item_type][item_base].keys()))

    __selector_reset_regex_combo(should_hide=False)
    pass

def __selector_regex_selected(sender, regex_title: str) -> None:
    global regex_lookup
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_TYPE_TAG)
    item_base = dpg.get_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_BASE_TAG)
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_REGEX_PREVIEW_TAG, show=True)
    dpg.set_value(gui_tags.REGEX_WIZARD_SELECTOR_REGEX_PREVIEW_TAG, regex_lookup[item_type][item_base][regex_title])
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTOR_OK_TAG, show=True)
    pass

def __selector_confirm_selected_regex() -> None:
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_TYPE_TAG)
    item_base = dpg.get_value(gui_tags.REGEX_WIZARD_SELECTOR_COMBO_BASE_TAG)
    crafting_target = constants.ITEM_TYPE_TO_CRAFTING_TARGET_LOOKUP[item_type]

    dpg.set_value(gui_tags.REGEX_INPUT_TAG, dpg.get_value(gui_tags.REGEX_WIZARD_SELECTOR_REGEX_PREVIEW_TAG))
    dpg.set_value(gui_tags.CRAFTING_TARGET_COMBO_TAG, crafting_target)
    dpg.configure_item(gui_tags.MAP_HIDDEN_GROUP_TAG, show=True if crafting_target == constants.CraftingTarget.MAPS else False)
    dpg.set_value(gui_tags.MAP_TYPE_CHECK, item_base == 'Tier 17')
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False)
    pass

def __selector_switch_to_editor() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=True)
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_SELECTOR_GROUP_TAG, show=False)
    pass

def __editor_save_to_selector() -> None:
    global regex_lookup
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_TYPE_TAG)
    item_base = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_BASE_TAG)
    regex_label = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG)
    regex_string = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_REGEX_INPUT_TAG)

    regex_lookup[item_type][item_base][regex_label] = regex_string
    lookup_manager.update(regex_lookup)

    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_SELECTOR_GROUP_TAG, show=True)
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=False)
    __selector_reset_item_base_combo()
    pass

def __editor_cancel_to_selector() -> None:
    global regex_lookup
    regex_lookup = lookup_manager.read()

    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_SELECTOR_GROUP_TAG, show=True)
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=False)
    pass

def __editor_reset_regex_fields() -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG, constants.REGEX_TITLE_COMBO_DEFAULT)

    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG, show=False)
    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_REGEX_INPUT_TAG, show=False)
    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_SAVE_BTN_TAG, show=False)
    pass

def __editor_reset_item_base_combo() -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_BASE_TAG, constants.ITEM_BASE_COMBO_DEFAULT)

    __editor_reset_regex_fields()
    pass

def __editor_item_type_selected(sender, item_type: str) -> None:
    global regex_lookup
    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_COMBO_BASE_TAG, show=True, items=[*list(regex_lookup[item_type].keys()), constants.EDITOR_ADD_NEW_ITEM])

    __editor_reset_item_base_combo()
    pass

def __editor_item_base_selected(sender, item_base: str) -> None:
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_TYPE_TAG)

    if item_base == constants.EDITOR_ADD_NEW_ITEM:
        global new_item_key
        new_item_key = NewItemKey(item_type=item_type)

        dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_NEW_ITEM_GROUP_TAG, show=True)
        dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=False)
        return

    global regex_lookup
    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG, show=True, items=[*list(regex_lookup[item_type][item_base].keys()), constants.EDITOR_ADD_NEW_ITEM])
    dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG, constants.REGEX_TITLE_COMBO_DEFAULT)
    pass

def __editor_regex_title_selected(sender, regex_title: str) -> None:
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_TYPE_TAG)
    item_base = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_BASE_TAG)

    if regex_title == constants.EDITOR_ADD_NEW_ITEM:
        global new_item_key
        new_item_key = NewItemKey(item_type=item_type, item_base=item_base)

        dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_NEW_ITEM_GROUP_TAG, show=True)
        dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=False)
        return
    
    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_REGEX_INPUT_TAG, show=True)
    pass

def __editor_regex_input_changed(sender, regex_string: str) -> None:
    is_valid = len(regex_string) > 0

    dpg.configure_item(gui_tags.REGEX_WIZARD_EDITOR_SAVE_BTN_TAG, show=is_valid)
    pass

def __editor_save_new_item() -> None:
    global new_item_key
    global regex_lookup

    if not new_item_key.item_base:
        new_item_base = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_NEW_ITEM_INPUT_TAG)
        if new_item_base == "":
            return

        regex_lookup[new_item_key.item_type][new_item_base] = {}
        __editor_item_type_selected(sender=None, item_type=new_item_key.item_type)
        dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_BASE_TAG, new_item_base)
        __editor_item_base_selected(sender=None, item_base=new_item_base)
    elif not new_item_key.regex_title:
        new_regex_title = dpg.get_value(gui_tags.REGEX_WIZARD_EDITOR_NEW_ITEM_INPUT_TAG)
        if new_regex_title == "":
            return
        
        regex_lookup[new_item_key.item_type][new_item_key.item_base][new_regex_title] = {}
        __editor_item_base_selected(sender=None, item_base=new_item_key.item_base)
        dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG, new_regex_title)
        __editor_regex_title_selected(sender=None, regex_title=new_regex_title)
        pass

    dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_NEW_ITEM_INPUT_TAG, "")
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=True)
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_NEW_ITEM_GROUP_TAG, show=False)
    pass

def __editor_cancel_new_item() -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_EDITOR_NEW_ITEM_INPUT_TAG, "")
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=True)
    dpg.configure_item(gui_tags.REGEX_WIZARD_LOOKUP_NEW_ITEM_GROUP_TAG, show=False)
    pass

def init() -> None:
    global regex_lookup
    regex_lookup = lookup_manager.read()

    with dpg.window(tag=gui_tags.REGEX_WIZARD_MODAL_TAG, width=214, height=219, modal=True, show=False, no_title_bar=True, no_resize=True):
        with dpg.group(horizontal=True):
            with dpg.group(tag=gui_tags.REGEX_WIZARD_LOOKUP_SELECTOR_GROUP_TAG, show=True):
                elements.add_button(label="Edit library", callback=__selector_switch_to_editor)

                dpg.add_spacer(height=8)

                dpg.add_combo(tag=gui_tags.REGEX_WIZARD_SELECTOR_COMBO_TYPE_TAG, items=list(regex_lookup.keys()), default_value=constants.ITEM_TYPE_COMBO_DEFAULT, callback=__selector_item_type_selected, width=200)
                dpg.add_combo(tag=gui_tags.REGEX_WIZARD_SELECTOR_COMBO_BASE_TAG, default_value=constants.ITEM_BASE_COMBO_DEFAULT, show=False, callback=__selector_item_base_selected, width=200)
                dpg.add_combo(tag=gui_tags.REGEX_WIZARD_SELECTOR_COMBO_REGEX_TAG, default_value=constants.REGEX_TITLE_COMBO_DEFAULT, show=False, callback=__selector_regex_selected, width=200)
                dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_SELECTOR_REGEX_PREVIEW_TAG, readonly=True, multiline=True, show=False, width=200, height=22)

                dpg.add_spacer(height=8)

                with dpg.group(horizontal=True):
                    elements.add_button(tag=gui_tags.REGEX_WIZARD_SELECTOR_OK_TAG, label="OK", show=False, callback=__selector_confirm_selected_regex)
                    elements.add_button(label="Cancel", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False))
                    pass

            with dpg.group(tag=gui_tags.REGEX_WIZARD_LOOKUP_EDITOR_GROUP_TAG, show=False):
                elements.add_button(label="Back", callback=__editor_cancel_to_selector)

                dpg.add_spacer(show=True, height=8)

                dpg.add_combo(tag=gui_tags.REGEX_WIZARD_EDITOR_COMBO_TYPE_TAG, items=list(regex_lookup.keys()), default_value=constants.ITEM_TYPE_COMBO_DEFAULT, callback=__editor_item_type_selected, width=200)
                dpg.add_combo(tag=gui_tags.REGEX_WIZARD_EDITOR_COMBO_BASE_TAG, default_value=constants.ITEM_BASE_COMBO_DEFAULT, show=False, callback=__editor_item_base_selected, width=200)
                dpg.add_combo(tag=gui_tags.REGEX_WIZARD_EDITOR_COMBO_REGEX_TAG, default_value=constants.REGEX_TITLE_COMBO_DEFAULT, show=False, callback=__editor_regex_title_selected, width=200)
                dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_EDITOR_REGEX_INPUT_TAG, show=False, callback=__editor_regex_input_changed, width=200, height=22)

                dpg.add_spacer(show=True, height=8)

                elements.add_button(label="Save", tag=gui_tags.REGEX_WIZARD_EDITOR_SAVE_BTN_TAG, callback=__editor_save_to_selector)
                pass

            with dpg.group(tag=gui_tags.REGEX_WIZARD_LOOKUP_NEW_ITEM_GROUP_TAG, show=False):
                elements.add_button(label="Cancel", callback=__editor_cancel_new_item)

                dpg.add_spacer(show=True, height=8)

                dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_EDITOR_NEW_ITEM_INPUT_TAG, width=200, height=22)

                dpg.add_spacer(show=True, height=8)

                elements.add_button(label="Save", callback=__editor_save_new_item)
                pass
