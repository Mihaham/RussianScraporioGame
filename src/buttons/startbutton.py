import src.SingleGame as sg
from src.buttons.button import Button


class StartButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func = sg.start_game


