#Authors billy_smalls and kipper86

import Resources.gui as gui
import logging
from logging.handlers import RotatingFileHandler

file_log_handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=2,)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_log_handler]
)

logging.info("------ Application Started ------")

gui.init_gui()

logging.info("------ Application Closed ------")
