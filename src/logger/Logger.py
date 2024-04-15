import datetime
import logging
import os
from typing import Optional


def add_str_to_file(str_to_write: str, file_name: str, filemod: Optional[str] = "a") -> None:
    with open(f"{file_name}", filemod) as file:
        file.write(str_to_write + "\n")


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    # Create custom logger logging all five levels
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Define format for logs
    fmt = '%(asctime)s | %(levelname)8s | %(message)s'

    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    # Create file handler for logging to a file (logs all five levels)
    date = datetime.datetime.now().strftime("%Y-%m-%d---%H:%M:%S")
    os.makedirs(f"logs/{date}", mode=0o777, exist_ok=True)
    file_handler = logging.FileHandler(f"logs/{date}/all_logs.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt))

    # Add both handlers to the logger
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    id = 0
    objects = {}

    info: str = f"logs/{date}/info.log"
    warnings: str = f"logs/{date}/warnings.log"
    errors: str = f"logs/{date}/errors.log"
    debug: str = f"logs/{date}/debug.log"
    add_str_to_file("Game started\n", info, filemod="w")
    add_str_to_file("Game started\n", warnings, filemod="w")
    add_str_to_file("Game started\n", errors, filemod="w")
    add_str_to_file("Game started\n", debug, filemod="w")

    logger.debug('This is a debug-level message')
    logger.info('This is an info-level message')
    logger.warning('This is a warning-level message')
    logger.error('This is an error-level message')
    logger.critical('This is a critical-level message')

    @classmethod
    def add_info(cls, text: str) -> None:
        cls.logger.info(text)
        add_str_to_file(text, cls.info)

    @classmethod
    def add_warnings(cls, text: str) -> None:
        cls.logger.warning(text)
        add_str_to_file(text, cls.warnings)

    @classmethod
    def add_errors(cls, text: str) -> None:
        cls.logger.error(text)
        add_str_to_file(text, cls.errors)

    @classmethod
    def add_debug(cls, text: str) -> None:
        cls.logger.debug(text)
        add_str_to_file(text, cls.debug)


class GlobalObject:
    id = 0

    def __init__(self):
        GlobalObject.id += 1
        Logger.objects[GlobalObject.id] = self
