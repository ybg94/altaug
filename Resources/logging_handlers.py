import logging
import dearpygui.dearpygui as dpg

class GuiLogHandler(logging.Handler):
    def __init__(self, tag: str, level):
        super().__init__(level)
        self.tag = tag

    def format(self, record):
        # No need to log full callstack to GUI
        record.exc_info = None
        record.exc_text = None
        return super().format(record)

    def emit(self, record):
        try:
            msg = self.format(record)
            current = dpg.get_value(self.tag)
            dpg.set_value(self.tag, current + msg + "\n")
        except Exception:
            self.handleError(record)
