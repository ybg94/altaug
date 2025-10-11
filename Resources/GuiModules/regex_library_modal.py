import dearpygui.dearpygui as dpg
from .. import gui_tags
from . import constants
from . import elements

def init() -> None:
    def item_type_selected() -> None:
        selected_type: str = dpg.get_value(gui_tags.REGEX_WIZARD_MODAL_COMBO_TYPE_TAG)
        dpg.configure_item(
            gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG,
            show=True,
            items=constants.item_base_combo_items[selected_type]
        )
        dpg.set_value(
            gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG,
            constants.ITEM_BASE_COMBO_DEFAULT
        )

        # Reset dependant combos
        dpg.configure_item(
            gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG,
            show=False,
            items=[]
        )
        dpg.set_value(
            gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG,
            constants.REGEX_COMBO_DEFAULT
        )

    def item_base_selected() -> None:
        selected_base: str = dpg.get_value(gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG)
        dpg.configure_item(
            gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG,
            show=True,
            items=constants.regex_combo_items[selected_base]
        )
        dpg.set_value(
            gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG,
            constants.REGEX_COMBO_DEFAULT
        )
    
    def regex_selected() -> None:
        pass

    with dpg.window(tag=gui_tags.REGEX_WIZARD_MODAL_TAG, width=300, height=450, modal=True, show=False, no_title_bar=True):
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_MODAL_COMBO_TYPE_TAG, items=["Armour", "Weapon", "Map"], default_value=constants.ITEM_TYPE_COMBO_DEFAULT, callback=item_type_selected)
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_MODAL_COMBO_BASE_TAG, items=[], default_value=constants.ITEM_BASE_COMBO_DEFAULT, show=False, callback=item_base_selected)
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_MODAL_COMBO_REGEX_TAG, items=[], default_value=constants.REGEX_COMBO_DEFAULT, show=False, callback=regex_selected)

        with dpg.group(horizontal=True):
            elements.add_button(label="OK", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False))
            elements.add_button(label="Cancel", callback=lambda: dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False))