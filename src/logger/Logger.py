import datetime
import logging
import os
from typing import Optional


def add_str_to_file(str_to_write: str, file_name: str, filemod: Optional[str] = "a") -> None:
    with open(f"{file_name}", filemod) as file:
        file.write(str_to_write + "\n")

class Logger:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    id = 0
    objects = {}
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
    def __init__(self):
        GlobalObject.id += 1
        Logger.objects[GlobalObject.id] = self

