import logging
import os
import dearpygui.dearpygui as dpg
from . import crafting_processor as crafting_processor
from . import gui_tags as gui_tags
from . import logging_handlers
from .config_manager import manager, Section
from .GuiModules import configuration_window
from .GuiModules import crafting_state
from .GuiModules.constants import AffixMode, MapModifier, MapStat
from .GuiModules import crafting_window
from .GuiModules import log_window
from .GuiModules import regex_favorites_modal
from .GuiModules import regex_library_modal

SECTION_TAGS: dict[Section, str] = {
    Section.CONFIGURATION: gui_tags.CONFIGURATION_SECTION_TAG,
    Section.CRAFTING: gui_tags.CRAFTING_SECTION_TAG,
    Section.SCRIPT_LOG: gui_tags.SCRIPT_LOG_SECTION_TAG,
}

def __save_state_to_config() -> None:
    config = manager.cfg
    config.last_state.open_sections = {str(section): bool(dpg.get_value(tag)) for section, tag in SECTION_TAGS.items()}

    config.app_settings.pyautogui_pause = dpg.get_value(gui_tags.PYAUTOGUI_PAUSE_TAG)
    config.app_settings.enable_performance_logging = dpg.get_value(gui_tags.PERFORMANCE_LOGGING_TAG)

    config.last_state.crafting_target = str(crafting_state.get_crafting_target())
    config.last_state.map_craft_amount = dpg.get_value(gui_tags.MAP_AMOUNT_INPUT_TAG)
    config.last_state.is_t17 = dpg.get_value(gui_tags.MAP_TYPE_CHECK)
    config.last_state.map_regex_string = dpg.get_value(gui_tags.MAP_REGEX_INPUT_TAG)
    config.last_state.gear_regex_string = dpg.get_value(gui_tags.GEAR_REGEX_INPUT_TAG)
    config.last_state.max_currency_use = dpg.get_value(gui_tags.MAX_ATTEMPT_INPUT_TAG)
    affix_mode = crafting_state.get_affix_mode()
    config.last_state.is_pre = affix_mode == AffixMode.PREFIX
    config.last_state.is_suff = affix_mode == AffixMode.SUFFIX

    config.last_state.map_stat_filters = {
        str(stat): {'enabled': dpg.get_value(gui_tags.map_stat_check_tag(stat)), 'minimum': dpg.get_value(gui_tags.map_stat_input_tag(stat))}
        for stat in MapStat
    }
    config.last_state.map_modifier_filters = {
        str(modifier): dpg.get_value(gui_tags.map_modifier_check_tag(modifier))
        for modifier in MapModifier
    }

    manager.save_config(config)
    pass

def init_gui() -> None:
    dpg.create_context()
    dpg.set_exit_callback(__save_state_to_config)
    dpg.configure_app(init_file=os.path.join('src', 'gui_layout.ini'))
    try:
        with dpg.font_registry():
            with dpg.font(os.path.join(os.environ['WINDIR'], 'Fonts', 'seguiemj.ttf'), 16) as emoji_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range(0x2600, 0x26FF) # Miscellaneous Symbols
                dpg.add_font_range(0x2700, 0x27BF) # Dingbats
                dpg.add_font_range(0x1F300, 0x1F6FF) # Misc Symbols and Pictographs

        dpg.bind_font(emoji_font)
    except Exception:
        logging.error('Unable to load Bahnschrift font, using default.', exc_info=True)
    dpg.create_viewport(title="Alt-Aug GUI", width=800, height=855)


    open_sections = manager.cfg.last_state.open_sections

    configuration_window.load_images()
    regex_library_modal.init()
    regex_favorites_modal.init()

    # One window filling the viewport, each part is a collapsible section stacked top to bottom
    with dpg.window(tag=gui_tags.MAIN_WINDOW_TAG):
        configuration_window.init(gui_tags.CONFIGURATION_SECTION_TAG, open_sections[Section.CONFIGURATION])
        crafting_window.init(gui_tags.CRAFTING_SECTION_TAG, open_sections[Section.CRAFTING])
        log_window.init(gui_tags.SCRIPT_LOG_SECTION_TAG, open_sections[Section.SCRIPT_LOG])
    dpg.set_primary_window(gui_tags.MAIN_WINDOW_TAG, True)

    gui_log_handler = logging_handlers.GuiLogHandler(tag=gui_tags.OUTPUT_LOG_TAG, level=logging.INFO)
    gui_log_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
    logging.getLogger().addHandler(gui_log_handler)

    configuration_window.__set_pyautogui_pause()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()