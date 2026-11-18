import dearpygui.dearpygui as dpg
from .constants import AffixMode, CraftingTarget, MapModifier, MapStat
from .. import gui_tags

TARGET_TO_TAB_TAG: dict[str, str] = {
    CraftingTarget.MAPS: gui_tags.CRAFTING_TARGET_MAPS_TAB_TAG,
    CraftingTarget.GEAR: gui_tags.CRAFTING_TARGET_GEAR_TAB_TAG,
}

TARGET_TO_REGEX_INPUT_TAG: dict[str, str] = {
    CraftingTarget.MAPS: gui_tags.MAP_REGEX_INPUT_TAG,
    CraftingTarget.GEAR: gui_tags.GEAR_REGEX_INPUT_TAG,
}

def get_crafting_target() -> CraftingTarget:
    active_tab = dpg.get_value(gui_tags.CRAFTING_TARGET_TAB_BAR_TAG)
    return CraftingTarget(dpg.get_item_user_data(active_tab))

def set_crafting_target(target: CraftingTarget) -> None:
    dpg.set_value(gui_tags.CRAFTING_TARGET_TAB_BAR_TAG, TARGET_TO_TAB_TAG[target])
    pass

def get_regex() -> str:
    return dpg.get_value(TARGET_TO_REGEX_INPUT_TAG[get_crafting_target()])

def get_map_stat_minimums() -> dict[MapStat, int]:
    """Minimum value for each map stat filter that is ticked."""
    return {
        stat: dpg.get_value(gui_tags.map_stat_input_tag(stat))
        for stat in MapStat
        if dpg.get_value(gui_tags.map_stat_check_tag(stat))
    }

def get_wanted_map_modifiers() -> set[MapModifier]:
    """Map modifiers that are ticked, a map needs at least one of them."""
    return {modifier for modifier in MapModifier if dpg.get_value(gui_tags.map_modifier_check_tag(modifier))}

def get_affix_mode() -> AffixMode:
    return AffixMode(dpg.get_value(gui_tags.AFFIX_MODE_RADIO))

def affix_mode_from_flags(is_pre: bool, is_suff: bool) -> AffixMode:
    if is_pre:
        return AffixMode.PREFIX
    if is_suff:
        return AffixMode.SUFFIX
    return AffixMode.ANY
