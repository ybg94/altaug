import logging
import os
import dearpygui.dearpygui as dpg
from . import crafting_processor as crafting_processor
from . import gui_tags as gui_tags
from . import logging_handlers
from Resources.GuiModules import configuration_window
from Resources.GuiModules import crafting_window
from Resources.GuiModules import log_window
from Resources.GuiModules import regex_library_modal

def init_gui() -> None:
    dpg.create_context()
    dpg.configure_app(init_file=os.path.join('src', 'gui_layout.ini'), docking=True, docking_space=True)

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

    dpg.create_viewport(title="Alt-Aug GUI", width=800)

    configuration_window_tag = dpg.generate_uuid()
    crafting_window_tag = dpg.generate_uuid()
    script_log_tag = dpg.generate_uuid()

    configuration_window.init(configuration_window_tag)
    regex_library_modal.init()
    crafting_window.init(crafting_window_tag)
    log_window.init(script_log_tag)

    gui_log_handler = logging_handlers.GuiLogHandler(tag=gui_tags.OUTPUT_LOG_TAG, level=logging.INFO)
    gui_log_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
    logging.getLogger().addHandler(gui_log_handler)

    configuration_window.set_pyautogui_pause()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()