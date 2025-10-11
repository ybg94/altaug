import dearpygui.dearpygui as dpg
from .. import gui_tags
from . import constants
from . import elements

def __reset_ok_button() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_OK_TAG, show=False)
    pass

def __reset_regex_preview() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_REGEX_PREVIEW_TAG, show=False)
    dpg.set_value(gui_tags.REGEX_WIZARD_MODAL_REGEX_PREVIEW_TAG, "")

    __reset_ok_button()
    pass

def __reset_regex_combo(should_hide: bool) -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG, constants.REGEX_COMBO_DEFAULT)
    if should_hide:
        dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG, show=False)

    __reset_regex_preview()
    pass

def reset_item_base_combo() -> None:
    dpg.set_value(gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG, constants.ITEM_BASE_COMBO_DEFAULT)

    __reset_regex_combo(should_hide=True)
    pass

def __item_type_selected(sender, app_data) -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG, show=True, items=constants.ITEM_BASES_LOOKUP[app_data])

    reset_item_base_combo()
    pass

def __item_base_selected(sender, app_data) -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG, show=True, items=constants.REGEX_PRESETS_LOOKUP[app_data])

    __reset_regex_combo(should_hide=False)
    pass

def __regex_selected(sender, app_data) -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_REGEX_PREVIEW_TAG, show=True)
    dpg.set_value(gui_tags.REGEX_WIZARD_MODAL_REGEX_PREVIEW_TAG, constants.REGEX_LOOKUP[app_data])
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_OK_TAG, show=True)
    pass

def __confirm_selected_regex() -> None:
    dpg.set_value(gui_tags.REGEX_INPUT_TAG, dpg.get_value(gui_tags.REGEX_WIZARD_MODAL_REGEX_PREVIEW_TAG))
    dpg.set_value(gui_tags.CRAFTING_TARGET_COMBO_TAG, constants.CRAFTING_TARGET_LOOKUP[dpg.get_value(gui_tags.REGEX_WIZARD_MODAL_COMBO_TYPE_TAG)])
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False)
    pass

def init() -> None:
    with dpg.window(tag=gui_tags.REGEX_WIZARD_MODAL_TAG, width=300, height=450, modal=True, show=False, no_title_bar=True):
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_MODAL_COMBO_TYPE_TAG, items=constants.ITEM_TYPES, default_value=constants.ITEM_TYPE_COMBO_DEFAULT, callback=__item_type_selected)
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG, default_value=constants.ITEM_BASE_COMBO_DEFAULT, show=False, callback=__item_base_selected)
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG, default_value=constants.REGEX_COMBO_DEFAULT, show=False, callback=__regex_selected)
        dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_MODAL_REGEX_PREVIEW_TAG, readonly=True, multiline=True, show=False)

        with dpg.group(horizontal=True):
            elements.add_button(tag=gui_tags.REGEX_WIZARD_MODAL_OK_TAG, label="OK", show=False, callback=__confirm_selected_regex)
            elements.add_button(label="Cancel", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False))
