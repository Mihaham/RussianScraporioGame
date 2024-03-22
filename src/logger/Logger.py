import datetime
import logging
import os
from typing import Optional


def add_str_to_file(str_to_write: str, file_name: str, filemod: Optional[str] = "a") -> None:
    with open(f"{file_name}", filemod) as file:
        file.write(str_to_write + "\n")

class Logger:
    date = datetime.datetime.now().strftime("%Y-%m-%d---%H:%M:%S")
    os.makedirs(f"logs/{date}", mode=0o777, exist_ok=True)
    info: str = f"logs/{date}/info.log"
    warnings: str = f"logs/{date}/warnings.log"
    errors: str = f"logs/{date}/errors.log"
    debug: str = f"logs/{date}/debug.log"
    add_str_to_file("Game started\n", info, filemod="w")
    add_str_to_file("Game started\n", warnings, filemod="w")
    add_str_to_file("Game started\n", errors, filemod="w")
    add_str_to_file("Game started\n", debug, filemod="w")

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.date : datetime.datetime = datetime.datetime.now().strftime('%Y%m%d-%H')
        os.makedirs(f"logs/{self.date}", mode=0o777, exist_ok=True)
        self.info : str = f"logs/{self.date}/info.log"
        self.warnings : str = f"logs/{self.date}/warnings.log"
        self.errors : str = f"logs/{self.date}/errors.log"
        self.debug : str = f"logs/{self.date}/debug.log"


    @classmethod
    def add_info(cls, text : str) -> None:
        logging.info(text)
        add_str_to_file(text, cls.info)

    @classmethod
    def add_warnings(cls, text : str) -> None:
        logging.warning(text)
        add_str_to_file(text, cls.warnings)

    @classmethod
    def add_errors(cls, text : str) -> None:
        logging.error(text)
        add_str_to_file(text, cls.errors)

    @classmethod
    def add_debug(cls, text : str) -> None:
        logging.debug(text)
        add_str_to_file(text, cls.debug)


class GlobalObject:
    id = 0
    objects = {}
    def __init__(self):
        GlobalObject.id += 1
