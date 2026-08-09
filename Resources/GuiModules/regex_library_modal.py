import re
import dearpygui.dearpygui as dpg
from . import constants
from . import elements
from .. import gui_tags
from .. import affix_library

affix_data: affix_library.AffixLibrary
selected_prefixes: set[str] = set()
selected_suffixes: set[str] = set()

def __rebuild_regex_preview() -> None:
    parts = [f"^{re.escape(name)}" for name in selected_prefixes] + [f"{re.escape(name)}$" for name in selected_suffixes]
    regex_text = "|".join(parts)

    dpg.set_value(gui_tags.REGEX_WIZARD_REGEX_PREVIEW_TAG, regex_text)
    dpg.configure_item(gui_tags.REGEX_WIZARD_OK_TAG, show=len(parts) > 0)
    pass

def __affix_toggled(sender, is_checked: bool, user_data: tuple[bool, str]) -> None:
    is_prefix, name = user_data
    target_set = selected_prefixes if is_prefix else selected_suffixes

    if is_checked:
        target_set.add(name)
    else:
        target_set.discard(name)

    __rebuild_regex_preview()
    pass

def __populate_affix_list(filter_tag: str, names: list[str], is_prefix: bool) -> None:
    dpg.delete_item(filter_tag, children_only=True)
    for name in sorted(names):
        dpg.add_selectable(parent=filter_tag, label=name, filter_key=name, callback=__affix_toggled, user_data=(is_prefix, name))
    pass

def __reset_selection() -> None:
    selected_prefixes.clear()
    selected_suffixes.clear()

    dpg.set_value(gui_tags.REGEX_WIZARD_PREFIX_SEARCH_TAG, "")
    dpg.set_value(gui_tags.REGEX_WIZARD_SUFFIX_SEARCH_TAG, "")
    dpg.set_value(gui_tags.REGEX_WIZARD_PREFIX_FILTER_TAG, "")
    dpg.set_value(gui_tags.REGEX_WIZARD_SUFFIX_FILTER_TAG, "")

    __rebuild_regex_preview()
    pass

def __type_selected(sender, item_type: str) -> None:
    category = dpg.get_value(gui_tags.REGEX_WIZARD_CATEGORY_COMBO_TAG)
    affixes = affix_data[category][item_type]

    __populate_affix_list(gui_tags.REGEX_WIZARD_PREFIX_FILTER_TAG, affixes.get('prefixes', []), is_prefix=True)
    __populate_affix_list(gui_tags.REGEX_WIZARD_SUFFIX_FILTER_TAG, affixes.get('suffixes', []), is_prefix=False)
    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTION_GROUP_TAG, show=True)

    __reset_selection()
    pass

def __category_selected(sender, category: str) -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_TYPE_COMBO_TAG, show=True, items=list(affix_data[category].keys()))
    dpg.set_value(gui_tags.REGEX_WIZARD_TYPE_COMBO_TAG, constants.TYPE_COMBO_DEFAULT)

    dpg.configure_item(gui_tags.REGEX_WIZARD_SELECTION_GROUP_TAG, show=False)
    __reset_selection()
    pass

def __confirm_selection() -> None:
    category = dpg.get_value(gui_tags.REGEX_WIZARD_CATEGORY_COMBO_TAG)
    item_type = dpg.get_value(gui_tags.REGEX_WIZARD_TYPE_COMBO_TAG)
    crafting_target = constants.CATEGORY_TO_CRAFTING_TARGET_LOOKUP[category]

    dpg.set_value(gui_tags.REGEX_INPUT_TAG, dpg.get_value(gui_tags.REGEX_WIZARD_REGEX_PREVIEW_TAG))
    dpg.set_value(gui_tags.CRAFTING_TARGET_COMBO_TAG, crafting_target)
    dpg.configure_item(gui_tags.MAP_HIDDEN_GROUP_TAG, show=True if crafting_target == constants.CraftingTarget.MAPS else False)
    dpg.set_value(gui_tags.MAP_TYPE_CHECK, item_type == constants.NIGHTMARE_MAP_TYPE)
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False)
    pass

def __cancel_wizard() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False)
    pass

def init() -> None:
    global affix_data
    affix_data = affix_library.read()

    with dpg.window(tag=gui_tags.REGEX_WIZARD_MODAL_TAG, width=560, height=500, modal=True, show=False, no_title_bar=True, no_resize=True):
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_CATEGORY_COMBO_TAG, items=list(affix_data.keys()), default_value=constants.CATEGORY_COMBO_DEFAULT, callback=__category_selected, width=200)
        dpg.add_combo(tag=gui_tags.REGEX_WIZARD_TYPE_COMBO_TAG, default_value=constants.TYPE_COMBO_DEFAULT, show=False, callback=__type_selected, width=200)

        dpg.add_spacer(height=8)

        with dpg.group(tag=gui_tags.REGEX_WIZARD_SELECTION_GROUP_TAG, show=False):
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text("Prefixes")
                    dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_PREFIX_SEARCH_TAG, hint="Search prefixes...", width=260,
                                        callback=lambda sender, search_text: dpg.set_value(gui_tags.REGEX_WIZARD_PREFIX_FILTER_TAG, search_text))
                    with dpg.child_window(width=260, height=260):
                        with dpg.filter_set(tag=gui_tags.REGEX_WIZARD_PREFIX_FILTER_TAG):
                            pass

                with dpg.group():
                    dpg.add_text("Suffixes")
                    dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_SUFFIX_SEARCH_TAG, hint="Search suffixes...", width=260,
                                        callback=lambda sender, search_text: dpg.set_value(gui_tags.REGEX_WIZARD_SUFFIX_FILTER_TAG, search_text))
                    with dpg.child_window(width=260, height=260):
                        with dpg.filter_set(tag=gui_tags.REGEX_WIZARD_SUFFIX_FILTER_TAG):
                            pass
                pass

            dpg.add_spacer(height=8)
            dpg.add_text("Generated RegEx:")
            dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_REGEX_PREVIEW_TAG, readonly=True, multiline=True, width=520, height=40)
            pass

        dpg.add_spacer(height=8)

        with dpg.group(horizontal=True):
            elements.add_button(tag=gui_tags.REGEX_WIZARD_OK_TAG, label="OK", show=False, callback=__confirm_selection)
            elements.add_button(label="Cancel", callback=__cancel_wizard)
            pass
