#Authors
#billy_smalls
#kipper86
#niirn

from logging.handlers import RotatingFileHandler
import logging
import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

from Resources import gui

file_log_handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=2, encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_log_handler],
    encoding='utf-8'
)

logging.info("------ Application Started ------")

gui.init_gui()

logging.info("------ Application Closed ------")
