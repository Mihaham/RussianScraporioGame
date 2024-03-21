import src.SingleGame as sg
from src.buttons.button import Button
from src.logger.Logger import Logger

class StartButton(Button):
    id = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        StartButton.id += 1
        self.__id = StartButton.id
        self.func = sg.start_game
        Logger.add_info(f"StartButton is initialized with id {self.__id}")


