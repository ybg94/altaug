import dearpygui.dearpygui as dpg
from . import constants
from . import crafting_state
from . import elements
from . import regex_favorites_modal
from . import regex_library_modal
from .. import crafting_processor
from .. import gui_tags
from ..config_manager import manager

MAX_CURRENCY_HINT = """When the craft uses multiple currency stacks, max currency
refers the highest amount used from one of the stacks

e.g.: when crafting with alt/aug with 20 currency max,
      the process will stop when 20 alts are used"""

T17_HINT = """T17 maps are rerolled with chaos orbs,
other maps are scoured and alchemied"""

AFFIX_MODE_HINT = """Any: always augment when there is an open affix
Prefix: skip the augment if the alteration already rolled a prefix
Suffix: skip the augment if the alteration already rolled a suffix"""

def __add_tooltip(parent: int | str, text: str) -> None:
    with dpg.tooltip(parent):
        dpg.add_text(text)
    pass

def __add_regex_section(target: constants.CraftingTarget, regex_input_tag: str, default_regex: str, show_generator: bool = False) -> None:
    dpg.add_spacer(height=4)
    dpg.add_text("RegEx")
    elements.add_hint_text("Crafting stops when the RegEx matches the item. Prefix with ! to stop when it does NOT match.")
    elements.add_hint_text("When copying from poe.re make sure to NOT include quotes.")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag=regex_input_tag, width=-196 if show_generator else -96, default_value=default_regex)
        if show_generator:
            dpg.add_button(label="Generator", width=92, callback=regex_library_modal.show)
        dpg.add_button(label="Favorites", width=-1, callback=lambda: regex_favorites_modal.show(target=target))
    pass

MAP_STATS_HINT = """Ticked stats must also reach their minimum before a map counts as done.
A stat missing from the map counts as 0%."""

MAP_MODIFIERS_HINT = """When any modifier is ticked, the map must contain at least one of the ticked ones.
Leave all unticked to ignore these modifiers."""

def __map_stat_toggled(sender, is_checked: bool, stat: constants.MapStat) -> None:
    dpg.configure_item(gui_tags.map_stat_input_tag(stat), enabled=is_checked)
    pass

def __add_map_stat_filters() -> None:
    saved_filters = manager.cfg.last_state.map_stat_filters

    with dpg.theme() as disabled_input_theme:
        with dpg.theme_component(dpg.mvInputInt, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Text, constants.HINT_TEXT_COLOR)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (45, 45, 48))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (45, 45, 48))

    dpg.add_text("Minimum map stats")
    with elements.form_table(label_width=140):
        for stat in constants.MapStat:
            saved_filter = saved_filters[stat]
            with dpg.table_row():
                dpg.add_checkbox(tag=gui_tags.map_stat_check_tag(stat), label=constants.MAP_STAT_LABELS[stat],
                                 default_value=saved_filter['enabled'], callback=__map_stat_toggled, user_data=stat)
                with dpg.group(horizontal=True):
                    dpg.add_input_int(tag=gui_tags.map_stat_input_tag(stat), default_value=saved_filter['minimum'], enabled=saved_filter['enabled'],
                                      min_value=0, min_clamped=True, step=5, width=110)
                    dpg.bind_item_theme(dpg.last_item(), disabled_input_theme)
                    dpg.add_text("% or more")
                __add_tooltip(gui_tags.map_stat_check_tag(stat), MAP_STATS_HINT)
    pass

def __add_map_modifier_filters() -> None:
    saved_filters = manager.cfg.last_state.map_modifier_filters

    dpg.add_text("Map must contain one of")
    for modifier in constants.MapModifier:
        dpg.add_checkbox(tag=gui_tags.map_modifier_check_tag(modifier), label=constants.MAP_MODIFIER_LABELS[modifier],
                         default_value=saved_filters[modifier])
        __add_tooltip(gui_tags.map_modifier_check_tag(modifier), f"{modifier}\n\n{MAP_MODIFIERS_HINT}")
    pass

def __add_map_filters() -> None:
    dpg.add_spacer(height=4)
    elements.add_hint_text("Checked separately from the RegEx, the map has to pass the RegEx and every filter below.")
    with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
        dpg.add_table_column(init_width_or_weight=1.4)
        dpg.add_table_column(init_width_or_weight=1.0)
        with dpg.table_row():
            with dpg.group():
                __add_map_stat_filters()
            with dpg.group():
                __add_map_modifier_filters()
    pass

def __init_maps_tab() -> None:
    last_state = manager.cfg.last_state

    with dpg.tab(tag=gui_tags.CRAFTING_TARGET_MAPS_TAB_TAG, label=f"  {constants.CraftingTarget.MAPS}  ", user_data=constants.CraftingTarget.MAPS):
        dpg.add_spacer(height=4)
        with elements.form_table():
            with elements.form_row("Maps to craft"):
                dpg.add_input_int(tag=gui_tags.MAP_AMOUNT_INPUT_TAG, default_value=last_state.map_craft_amount, min_value=1, min_clamped=True, width=128)
            with elements.form_row("Nightmare map (T17)"):
                dpg.add_checkbox(tag=gui_tags.MAP_TYPE_CHECK, default_value=last_state.is_t17)
                __add_tooltip(gui_tags.MAP_TYPE_CHECK, T17_HINT)

        __add_regex_section(constants.CraftingTarget.MAPS, gui_tags.MAP_REGEX_INPUT_TAG, last_state.map_regex_string, show_generator=True)
        __add_map_filters()
    pass

def __init_gear_tab() -> None:
    last_state = manager.cfg.last_state
    default_affix_mode = crafting_state.affix_mode_from_flags(last_state.is_pre, last_state.is_suff)

    with dpg.tab(tag=gui_tags.CRAFTING_TARGET_GEAR_TAB_TAG, label=f"  {constants.CraftingTarget.GEAR}  ", user_data=constants.CraftingTarget.GEAR):
        dpg.add_spacer(height=4)
        with elements.form_table():
            with elements.form_row("Looking for"):
                dpg.add_radio_button(tag=gui_tags.AFFIX_MODE_RADIO, items=constants.AFFIX_MODES, default_value=default_affix_mode, horizontal=True)
                __add_tooltip(gui_tags.AFFIX_MODE_RADIO, AFFIX_MODE_HINT)

        __add_regex_section(constants.CraftingTarget.GEAR, gui_tags.GEAR_REGEX_INPUT_TAG, last_state.gear_regex_string)
    pass

def init(crafting_window_tag: int | str, default_open: bool = True) -> None:
    last_state = manager.cfg.last_state

    with dpg.collapsing_header(tag=crafting_window_tag, label="Crafting target", default_open=default_open):
        with dpg.tab_bar(tag=gui_tags.CRAFTING_TARGET_TAB_BAR_TAG):
            __init_maps_tab()
            __init_gear_tab()

        crafting_state.set_crafting_target(last_state.crafting_target)

        dpg.add_spacer(height=4)
        dpg.add_separator()
        dpg.add_spacer(height=4)

        with elements.form_table():
            with elements.form_row("Max currency to use"):
                dpg.add_input_int(tag=gui_tags.MAX_ATTEMPT_INPUT_TAG, default_value=last_state.max_currency_use, min_value=1, min_clamped=True, width=128)
                __add_tooltip(gui_tags.MAX_ATTEMPT_INPUT_TAG, MAX_CURRENCY_HINT)

        dpg.add_spacer(height=4)
        elements.add_button(label="Start crafting", width=-1, callback=crafting_processor.start_crafting)
    pass
