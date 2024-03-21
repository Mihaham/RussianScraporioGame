from main import start_game
from src.buttons.button import Button


class StartButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func = start_game
