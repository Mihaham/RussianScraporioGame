from src.buttons.button import Button
from src.logger.Logger import Logger
import pygame

class StartButton(Button):
    id = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        StartButton.id += 1
        self.__id = StartButton.id
        self.func = kwargs["start"]
        Logger.add_info(f"StartButton is initialized with id {self.__id}")

    def handle_event(self, event : pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.func:
                self.func("Start_game")

