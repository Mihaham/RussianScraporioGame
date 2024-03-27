import pygame

from src.buttons.button import Button
from src.buttons.startbutton import StartButton
from src.drawing_pygame.Draw import Drawing
from src.logger.Logger import Logger, GlobalObject

class Menu(GlobalObject):
    id : int = 0
    def __init__(self, background=None, buttons=[[]], width=2000, height=1000, x=0, y=0):
        super().__init__()
        Menu.id += 1
        self.__id = Menu.id
        self.surface = pygame.display.set_mode((width, height))
        self.buttons: list[list[Button]] = buttons
        self.background: str = background
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y
        self.Draw : Drawing = Drawing()
        Logger.add_info("Menu is initialized ")

    def handle_hover(self) -> None:
        for buttons_list in self.buttons:
            for button in buttons_list:
                button.handle_hover()

    def update(self, event : pygame.event) -> None:
        for buttons_list in self.buttons:
            for button in buttons_list:
                button.update(event)

    def show(self) -> None:
        Logger.add_info("Showing menu")
        while True:
            self.Draw.draw(surface=self.surface, Menu=self)
            self.handle_hover()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.update(event)
            pygame.display.flip()
            pygame.display.update()
            pygame.time.Clock().tick(60)


class MainMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        k = 1
        self.buttons[0].append(StartButton(width=600 // k,
                                           height=200 // k,
                                           text="",
                                           not_hovered_skin="sprites/Large Buttons/Large Buttons/Start Button.png",
                                           hovered_skin="sprites/Large Buttons/Colored Large Buttons/Start  col_Button.png",
                                           # position=[self.LENGTH - self.LENGTH // 15, 100],
                                           position=[self.width // 2 - (600 // k) // 2, 200]))
        self.buttons[0].append(Button(width=600 // k,
                                      height=200 // k,
                                      text="",
                                      not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                      hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                      position=[self.width // 2 - (600 // k) // 2, 500],
                                      func=exit))
        self.background = "sprites/menu_back.png"
        Logger.add_info("MainMenu is initialized")