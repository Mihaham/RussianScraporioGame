import datetime
import logging
import os
from typing import Optional


class Logger():

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.date : datetime.datetime = datetime.datetime.now().strftime('%Y%m%d-%H')
        os.makedirs(f"logs/{self.date}", mode=0o777, exist_ok=True)
        self.info : str = f"logs/{self.date}/info.log"
        self.warnings : str = f"logs/{self.date}/warnings.log"
        self.errors : str = f"logs/{self.date}/errors.log"
        self.debug : str = f"logs/{self.date}/debug.log"


        self.add_str_to_file("Game started\n", self.info, filemod="w")
        self.add_str_to_file("Game started\n", self.warnings, filemod="w")
        self.add_str_to_file("Game started\n", self.errors, filemod="w")
        self.add_str_to_file("Game started\n", self.debug, filemod="w")

    def add_str_to_file(self, str_to_write : str, file_name : str, filemod : Optional[str]="a") -> None:
        with open(f"{file_name}", filemod) as file:
            file.write(str_to_write + "\n")

    def add_info(self, text : str) -> None:
        logging.info(text)
        self.add_str_to_file(text, self.info)

    def add_warnings(self, text : str) -> None:
        logging.warning(text)
        self.add_str_to_file(text, self.warnings)

    def add_errors(self, text : str) -> None:
        logging.error(text)
        self.add_str_to_file(text, self.errors)

    def add_debug(self, text : str) -> None:
        logging.debug(text)
        self.add_str_to_file(text, self.debug)
