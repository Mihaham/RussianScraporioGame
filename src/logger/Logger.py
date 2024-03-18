import datetime
import logging
import os


class Logger():

    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.date = datetime.datetime.now().strftime('%Y%m%d-%H')
        os.makedirs(f"logs/{self.date}", mode=0o777, exist_ok=True)
        self.info = f"logs/{self.date}/info.log"
        self.warnings = f"logs/{self.date}/warnings.log"
        self.errors = f"logs/{self.date}/errors.log"
        self.debug = f"logs/{self.date}/debug.log"
        self.add_str_to_file("Game started\n", self.info, filemod="w")
        self.add_str_to_file("Game started\n", self.warnings, filemod="w")
        self.add_str_to_file("Game started\n", self.errors, filemod="w")
        self.add_str_to_file("Game started\n", self.debug, filemod="w")

    def add_str_to_file(self, str_to_write, file_name, filemod="a"):
        with open(f"{file_name}", filemod) as file:
            file.write(str_to_write + "\n")

    def add_info(self, text):
        logging.info(text)
        self.add_str_to_file(text, self.info)

    def add_warnings(self, text):
        logging.warning(text)
        self.add_str_to_file(text, self.warnings)

    def add_errors(self, text):
        logging.error(text)
        self.add_str_to_file(text, self.errors)

    def add_debug(self, text):
        logging.debug(text)
        self.add_str_to_file(text, self.debug)
