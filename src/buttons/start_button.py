from src.buttons.button import Button
from src.SingleGame import start_game


class start_button(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func = start_game
