from contextlib import contextmanager
from typing import Iterator
import dearpygui.dearpygui as dpg
from . import constants

DEFAULT_BUTTON_HEIGHT = 32
DEFAULT_LABEL_WIDTH = 170

def add_button(**kwargs) -> int | str:
    if 'height' not in kwargs:
        kwargs['height'] = DEFAULT_BUTTON_HEIGHT

    return dpg.add_button(**kwargs)

def add_hint_text(text: str, **kwargs) -> int | str:
    return dpg.add_text(text, color=constants.HINT_TEXT_COLOR, **kwargs)

@contextmanager
def form_table(label_width: int = DEFAULT_LABEL_WIDTH) -> Iterator[int | str]:
    """Two column table used to line up labels with their inputs; add rows with form_row()."""
    with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit) as table:
        dpg.add_table_column(width_fixed=True, init_width_or_weight=label_width)
        dpg.add_table_column(width_stretch=True)
        yield table

@contextmanager
def form_row(label: str) -> Iterator[int | str]:
    with dpg.table_row() as row:
        dpg.add_text(label)
        yield row
