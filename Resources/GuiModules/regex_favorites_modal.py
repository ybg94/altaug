import logging
import dearpygui.dearpygui as dpg
from . import constants
from . import crafting_state
from . import elements
from .. import gui_tags
from .. import regex_favorites
from ..regex_favorites import RegexFavorite

MODAL_WIDTH = 640
MODAL_HEIGHT = 520
REGEX_DISPLAY_LENGTH = 48

favorites: list[RegexFavorite] = []

def __selected_target() -> constants.CraftingTarget:
    return constants.CraftingTarget(dpg.get_value(gui_tags.REGEX_FAVORITES_TARGET_RADIO_TAG))

def __current_regex() -> str:
    return dpg.get_value(crafting_state.TARGET_TO_REGEX_INPUT_TAG[__selected_target()])

def __find_favorite(name: str, target: constants.CraftingTarget) -> RegexFavorite | None:
    return next((favorite for favorite in favorites if favorite.target == target and favorite.name.lower() == name.lower()), None)

def __set_status(text: str) -> None:
    dpg.set_value(gui_tags.REGEX_FAVORITES_STATUS_TAG, text)
    pass

def __refresh_save_controls() -> None:
    name = dpg.get_value(gui_tags.REGEX_FAVORITES_NAME_INPUT_TAG).strip()
    has_regex = bool(__current_regex().strip())
    is_existing = __find_favorite(name, __selected_target()) is not None

    dpg.configure_item(gui_tags.REGEX_FAVORITES_SAVE_TAG, label="Overwrite" if is_existing else "Save", enabled=bool(name) and has_regex)
    pass

def __refresh_current_regex() -> None:
    regex_text = __current_regex()
    dpg.set_value(gui_tags.REGEX_FAVORITES_CURRENT_REGEX_TAG, regex_text or "(the RegEx field is empty)")
    __refresh_save_controls()
    pass

def __shorten(text: str) -> str:
    return text if len(text) <= REGEX_DISPLAY_LENGTH else text[:REGEX_DISPLAY_LENGTH - 3] + "..."

def __rebuild_list() -> None:
    target = __selected_target()
    target_favorites = [favorite for favorite in favorites if favorite.target == target]

    dpg.delete_item(gui_tags.REGEX_FAVORITES_LIST_TAG, children_only=True)
    if not target_favorites:
        elements.add_hint_text(f"No favorites saved for {target} yet.", parent=gui_tags.REGEX_FAVORITES_LIST_TAG)
        return

    with dpg.table(parent=gui_tags.REGEX_FAVORITES_LIST_TAG, header_row=True, policy=dpg.mvTable_SizingFixedFit,
                   row_background=True, borders_innerH=True):
        dpg.add_table_column(label="Name", width_fixed=True, init_width_or_weight=150)
        dpg.add_table_column(label="RegEx", width_stretch=True)
        dpg.add_table_column(width_fixed=True)
        dpg.add_table_column(width_fixed=True)

        for favorite in target_favorites:
            with dpg.table_row():
                dpg.add_text(favorite.name)
                regex_text = dpg.add_text(__shorten(favorite.regex), color=constants.HINT_TEXT_COLOR)
                with dpg.tooltip(regex_text):
                    dpg.add_text(favorite.regex, wrap=400)
                dpg.add_button(label="Use", width=60, callback=__use_favorite, user_data=favorite)
                dpg.add_button(label="Delete", width=60, callback=__delete_favorite, user_data=favorite)
    pass

def __target_changed() -> None:
    __set_status("")
    __refresh_current_regex()
    __rebuild_list()
    pass

def __save_favorite() -> None:
    name = dpg.get_value(gui_tags.REGEX_FAVORITES_NAME_INPUT_TAG).strip()
    regex_text = __current_regex().strip()
    target = __selected_target()
    if not name or not regex_text:
        return

    existing = __find_favorite(name, target)
    if existing is not None:
        existing.regex = regex_text
        __set_status(f"Updated \"{name}\".")
    else:
        favorites.append(RegexFavorite(name=name, target=target, regex=regex_text))
        __set_status(f"Saved \"{name}\".")

    regex_favorites.save(favorites)
    dpg.set_value(gui_tags.REGEX_FAVORITES_NAME_INPUT_TAG, "")
    __refresh_save_controls()
    __rebuild_list()
    pass

def __use_favorite(sender, app_data, favorite: RegexFavorite) -> None:
    dpg.set_value(crafting_state.TARGET_TO_REGEX_INPUT_TAG[favorite.target], favorite.regex)
    crafting_state.set_crafting_target(favorite.target)
    logging.info(f"Using {favorite.target} RegEx favorite \"{favorite.name}\".")
    __close()
    pass

def __delete_favorite(sender, app_data, favorite: RegexFavorite) -> None:
    favorites.remove(favorite)
    regex_favorites.save(favorites)
    __set_status(f"Deleted \"{favorite.name}\".")
    __refresh_save_controls()
    __rebuild_list()
    pass

def __close() -> None:
    dpg.configure_item(gui_tags.REGEX_FAVORITES_MODAL_TAG, show=False)
    pass

def show(sender=None, app_data=None, target: constants.CraftingTarget | None = None) -> None:
    dpg.set_value(gui_tags.REGEX_FAVORITES_TARGET_RADIO_TAG, str(target or crafting_state.get_crafting_target()))
    dpg.set_value(gui_tags.REGEX_FAVORITES_NAME_INPUT_TAG, "")
    __target_changed()

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    pos = [max(0, (viewport_width - MODAL_WIDTH) // 2), max(0, (viewport_height - MODAL_HEIGHT) // 2)]
    dpg.configure_item(gui_tags.REGEX_FAVORITES_MODAL_TAG, show=True, pos=pos)
    pass

def init() -> None:
    global favorites
    favorites = regex_favorites.read()

    with dpg.window(tag=gui_tags.REGEX_FAVORITES_MODAL_TAG, label="RegEx favorites", width=MODAL_WIDTH, height=MODAL_HEIGHT,
                    modal=True, show=False, no_resize=True, no_collapse=True, on_close=__close):
        elements.add_hint_text("Save the RegEx you are using under a name, or pick a saved one to make it the active RegEx.")
        dpg.add_spacer(height=4)

        with elements.form_table(label_width=100):
            with elements.form_row("Crafting tab"):
                dpg.add_radio_button(tag=gui_tags.REGEX_FAVORITES_TARGET_RADIO_TAG, items=[constants.CraftingTarget.MAPS, constants.CraftingTarget.GEAR],
                                     default_value=constants.CraftingTarget.MAPS, horizontal=True, callback=__target_changed)

        dpg.add_spacer(height=4)
        dpg.add_separator()
        dpg.add_spacer(height=4)

        dpg.add_text("Save the current RegEx")
        with dpg.child_window(width=-1, height=60):
            dpg.add_text(tag=gui_tags.REGEX_FAVORITES_CURRENT_REGEX_TAG, wrap=MODAL_WIDTH - 50)
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag=gui_tags.REGEX_FAVORITES_NAME_INPUT_TAG, hint="Name...", width=-108,
                               callback=__refresh_save_controls)
            dpg.add_button(tag=gui_tags.REGEX_FAVORITES_SAVE_TAG, label="Save", width=-1, enabled=False, callback=__save_favorite)
        elements.add_hint_text("", tag=gui_tags.REGEX_FAVORITES_STATUS_TAG)

        dpg.add_spacer(height=4)
        dpg.add_separator()
        dpg.add_spacer(height=4)

        dpg.add_text("Saved favorites")
        with dpg.child_window(tag=gui_tags.REGEX_FAVORITES_LIST_TAG, width=-1, height=-44):
            pass

        dpg.add_spacer(height=4)
        elements.add_button(label="Close", width=100, callback=__close)
    pass
