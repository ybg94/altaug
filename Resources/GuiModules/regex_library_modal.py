import dearpygui.dearpygui as dpg
from . import constants
from . import crafting_state
from . import elements
from .. import gui_tags
from .. import map_mod_library

MODAL_WIDTH = 740
MODAL_HEIGHT = 600

map_mods: list[map_mod_library.MapMod] = []
mod_checkboxes: list[int | str] = []
mod_rows: list[int | str] = []
selected_mods: set[int] = set()

def __build_regex() -> str:
    # Several mods share the same regex fragment, keep the first occurrence only
    parts = list(dict.fromkeys(map_mods[index].regex for index in sorted(selected_mods)))
    if not parts:
        return ""

    # Selected mods are the ones to avoid, so crafting stops when none of them match
    return "!" + "|".join(parts)

def __rebuild_regex_preview() -> None:
    regex_text = __build_regex()

    dpg.set_value(gui_tags.REGEX_WIZARD_REGEX_PREVIEW_TAG, regex_text)
    dpg.set_value(gui_tags.REGEX_WIZARD_SELECTED_COUNT_TAG, f"{len(selected_mods)} mods selected, {len(regex_text)} characters")
    dpg.configure_item(gui_tags.REGEX_WIZARD_OK_TAG, enabled=len(selected_mods) > 0)
    pass

def __set_selected(index: int, is_selected: bool) -> None:
    if is_selected:
        selected_mods.add(index)
    else:
        selected_mods.discard(index)
    dpg.set_value(mod_checkboxes[index], is_selected)
    pass

def __is_mod_available(mod: map_mod_library.MapMod) -> bool:
    return not mod.nightmare_only or dpg.get_value(gui_tags.REGEX_WIZARD_NIGHTMARE_CHECK_TAG)

def __mod_toggled(sender, is_checked: bool, index: int) -> None:
    __set_selected(index, is_checked)
    __rebuild_regex_preview()
    pass

def __nightmare_toggled(sender, is_nightmare: bool) -> None:
    for index, mod in enumerate(map_mods):
        is_available = __is_mod_available(mod)
        dpg.configure_item(mod_rows[index], show=is_available)
        if not is_available:
            __set_selected(index, False)

    __rebuild_regex_preview()
    pass

def __clear_selection() -> None:
    for index in list(selected_mods):
        __set_selected(index, False)

    __rebuild_regex_preview()
    pass

def __confirm_selection() -> None:
    dpg.set_value(gui_tags.MAP_REGEX_INPUT_TAG, __build_regex())
    dpg.set_value(gui_tags.MAP_TYPE_CHECK, dpg.get_value(gui_tags.REGEX_WIZARD_NIGHTMARE_CHECK_TAG))
    crafting_state.set_crafting_target(constants.CraftingTarget.MAPS)
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False)
    pass

def __cancel_wizard() -> None:
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=False)
    pass

def show() -> None:
    # Match the map type currently selected in the crafting window
    dpg.set_value(gui_tags.REGEX_WIZARD_NIGHTMARE_CHECK_TAG, dpg.get_value(gui_tags.MAP_TYPE_CHECK))
    __nightmare_toggled(None, dpg.get_value(gui_tags.MAP_TYPE_CHECK))

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    pos = [max(0, (viewport_width - MODAL_WIDTH) // 2), max(0, (viewport_height - MODAL_HEIGHT) // 2)]
    dpg.configure_item(gui_tags.REGEX_WIZARD_MODAL_TAG, show=True, pos=pos)
    pass

def __init_mod_table() -> None:
    with dpg.table(tag=gui_tags.REGEX_WIZARD_TABLE_TAG, header_row=False, policy=dpg.mvTable_SizingFixedFit,
                   row_background=True, borders_innerH=True, scrollY=True, height=360):
        dpg.add_table_column(width_fixed=True)
        dpg.add_table_column(width_stretch=True)

        for index, mod in enumerate(map_mods):
            display_text = mod.display_text
            with dpg.table_row(filter_key=display_text) as row:
                mod_checkboxes.append(dpg.add_checkbox(callback=__mod_toggled, user_data=index))
                dpg.add_text(display_text, wrap=MODAL_WIDTH - 100)
            mod_rows.append(row)
    pass

def init() -> None:
    global map_mods
    map_mods = map_mod_library.read()

    with dpg.window(tag=gui_tags.REGEX_WIZARD_MODAL_TAG, label="Map mod RegEx generator", width=MODAL_WIDTH, height=MODAL_HEIGHT,
                    modal=True, show=False, no_resize=True, no_collapse=True, on_close=__cancel_wizard):
        elements.add_hint_text("Tick the map mods you want to avoid. Crafting stops once a map has none of them.")
        dpg.add_spacer(height=4)

        with dpg.group(horizontal=True):
            dpg.add_input_text(tag=gui_tags.REGEX_WIZARD_SEARCH_TAG, hint="Search mods...", width=300,
                               callback=lambda sender, search_text: dpg.set_value(gui_tags.REGEX_WIZARD_TABLE_TAG, search_text))
            dpg.add_spacer(width=16)
            dpg.add_checkbox(tag=gui_tags.REGEX_WIZARD_NIGHTMARE_CHECK_TAG, label="Nightmare map (T17)", callback=__nightmare_toggled)
            dpg.add_spacer(width=16)
            dpg.add_button(label="Clear selection", callback=__clear_selection)

        dpg.add_spacer(height=4)
        __init_mod_table()

        dpg.add_spacer(height=4)
        with dpg.group(horizontal=True):
            dpg.add_text("Generated RegEx")
            elements.add_hint_text("", tag=gui_tags.REGEX_WIZARD_SELECTED_COUNT_TAG)
        with dpg.child_window(width=-1, height=60):
            dpg.add_text(tag=gui_tags.REGEX_WIZARD_REGEX_PREVIEW_TAG, wrap=MODAL_WIDTH - 50)

        dpg.add_spacer(height=4)
        with dpg.group(horizontal=True):
            elements.add_button(tag=gui_tags.REGEX_WIZARD_OK_TAG, label="Use this RegEx", width=160, enabled=False, callback=__confirm_selection)
            elements.add_button(label="Cancel", width=100, callback=__cancel_wizard)

    __rebuild_regex_preview()
    pass
