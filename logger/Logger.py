import logging
import datetime
import os


class Logger():


    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.date = datetime.datetime.now().strftime('%Y%m%d-%H')
        os.makedirs(f"{self.date}", mode=0o777, exist_ok=True)
        self.info = f"{self.date}/info.log"
        self.warnings = f"{self.date}/warnings.log"
        self.errors = f"{self.date}/errors.log"
        self.debug = f"{self.date}/debug.log"

    def add_str_to_file(self, str_to_write, file_name):
        with open(f"{file_name}", "a") as file:
            file.write(str_to_write + "\n")

    def add_info(self, text):
        logging.info(text)
        self.add_str_to_file(text,self.info)

    def add_warnings(self, text):
        logging.warning(text)
        self.add_str_to_file(text,self.warnings)

    def add_errors(self, text):
        logging.error(text)
        self.add_str_to_file(text,self.errors)

    def add_debug(self, text):
        logging.debug(text)
        self.add_str_to_file(text,self.debug)


