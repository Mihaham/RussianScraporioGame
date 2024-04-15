from typing import Optional

import pygame

from src.logger.Logger import Logger, GlobalObject


class Button(GlobalObject):
    id = 0

    def __init__(self, text: str = "START", width: int = 100, height: int = 100,
                 hovered_skin: str = "sprites/empty.png",
                 not_hovered_skin: str = "sprites/empty.png", func=None,
                 position: list[int] = None, parent: Optional = None,
                 parent_position: str = "absolute", argument=None, **kwargs) -> None:
        super().__init__()
        Button.id += 1
        self.__id = Button.id

        self.text: str = text
        self.position: list[int] = position
        self.is_hovered: bool = False
        self.not_hovered_skin: str = not_hovered_skin
        self.hovered_skin: str = hovered_skin
        self.skin: str = self.not_hovered_skin
        self.func = func
        self.width: int = width
        self.height: int = height
        self.parent_position: str = parent_position
        self.parent = parent
        self.argument = argument

        self.image = pygame.image.load(self.hovered_skin)
        if self.parent_position == "absolute":
            self.buttonRect = pygame.Rect(self.position[0], self.position[1], self.width,
                                          self.height)
        else:
            pass
        Logger.add_info(f"Button is initialized with id {self.__id}")

    def handle_hover(self) -> None:
        self.is_hovered = self.buttonRect.collidepoint(pygame.mouse.get_pos())
        self.change_skin()

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.func:
                if self.argument:
                    self.func(self.argument)
                else:
                    self.func()

    def update(self, event: pygame.event) -> None:
        self.handle_hover()
        self.handle_event(event)

    def change_skin(self) -> None:
        if self.is_hovered:
            self.skin = self.hovered_skin
        else:
            self.skin = self.not_hovered_skin
