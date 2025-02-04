import logging
import os
import sys

# Logging levels
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

LOG_TO_CONSOLE = True
LOG_TO_FILE = True

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create output directory for logs
os.makedirs("src/output", exist_ok=True)

filepath_logger = "src/output/logger.log"
filepath_logger_archive = "src/output/logger_archive.log"

# Create handlers with UTF-8 encoding
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(filepath_logger, encoding="utf-8")
file_handler_archive = logging.FileHandler(filepath_logger_archive, encoding="utf-8")

# Reset logger.log before running the script
with open(filepath_logger, "w", encoding="utf-8"):
    pass

# Set level and format for handlers
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
file_handler_archive.setLevel(logging.DEBUG)

formatter_lvl_1 = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
formatter_lvl_2 = logging.Formatter("%(levelname)s - %(message)s")
formatter_lvl_3 = logging.Formatter("%(message)s")

if LOG_TO_CONSOLE:
    console_handler.setFormatter(formatter_lvl_2)
    logger.addHandler(console_handler)

if LOG_TO_FILE:
    file_handler.setFormatter(formatter_lvl_2)
    file_handler_archive.setFormatter(formatter_lvl_1)
    logger.addHandler(file_handler)
    logger.addHandler(file_handler_archive)
