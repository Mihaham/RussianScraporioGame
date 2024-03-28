import pygame

from src.buttons.button import Button
from src.buttons.startbutton import StartButton
from src.drawing_pygame.Draw import Drawing
from src.logger.Logger import Logger, GlobalObject

class Menu(GlobalObject):
    id : int = 0
    def __init__(self, background=None, buttons = [[]], width=2000, height=1000, x=0, y=0, **kwargs):
        super().__init__()
        Menu.id += 1
        self.__id = Menu.id
        self.surface = pygame.display.get_surface()
        self.buttons: list[list[Button]] = buttons
        self.background: str = background
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y
        self.Draw : Drawing = Drawing()
        self.is_active = False
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
        self.is_active = not(self.is_active)

    def draw_menu(self):
        self.Draw.draw(surface=self.surface, Menu=self)

    def loop(self):
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
        super().__init__(buttons = [[]],**kwargs)
        k = 1
        self.buttons[0].append(StartButton(width=600 // k,
                                           height=200 // k,
                                           text="",
                                           not_hovered_skin="sprites/Large Buttons/Large Buttons/Start Button.png",
                                           hovered_skin="sprites/Large Buttons/Colored Large Buttons/Start  col_Button.png",
                                           # position=[self.LENGTH - self.LENGTH // 15, 100],
                                           position=[self.width // 2 - (600 // k) // 2, 200],
                                           start = kwargs["start"]))
        self.buttons[0].append(Button(width=600 // k,
                                      height=200 // k,
                                      text="",
                                      not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                      hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                      position=[self.width // 2 - (600 // k) // 2, 500],
                                      func=exit))
        self.background = "sprites/menu_back.png"
        Logger.add_info("MainMenu is initialized")

class BuildingMenu(Menu):
    def __init__(self,pos_x, pos_y, width, hight, building, recipes, function, **kwargs):
        super().__init__(buttons = [[]],**kwargs)
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = hight
        self.building = building
        self.recipes : list = recipes
        self.buttons[0].append(Button(width=100,
                                      height=30,
                                      text="",
                                      not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                      hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                      position=[pos_x + width - 100, pos_y],
                                      func=function))

        self.buttons.append([])
        for i,recipe in enumerate(self.recipes):
            self.buttons[1].append(Button(width=50,
                                          height=50,
                                          text="",
                                          not_hovered_skin="sprites/Square Buttons/Square Buttons/V Square Button.png",
                                          hovered_skin="sprites/Square Buttons/Colored Square Buttons/V col_Square Button.png",
                                          position=[self.x + self.width/2 + 20, self.y + 20 + i * (50 + 10) ],
                                          func=self.activate_recipe,
                                          argument = recipe))

        self.buttons.append([])
        self.buttons[2].append(Button(width=50,
                                          height=50,
                                          text="",
                                          not_hovered_skin="sprites/Square Buttons/Square Buttons/On Off Square Button.png",
                                          hovered_skin="sprites/Square Buttons/Colored Square Buttons/On Off col_Square Button.png",
                                          position=[self.x + self.width/2 - 50, self.y],
                                          func=self.building.change_active))
        self.has_active_recipe = False
        self.active_recipe = None


    def activate_recipe(self, recipe):
        self.building.activate_recipe(recipe)
        if self.buttons[0][-1].func != self.delete_recipe:
            self.buttons[0].append(Button(width=50,
                                      height=50,
                                      text="",
                                      not_hovered_skin="sprites/Square Buttons/Square Buttons/Return Square Button.png",
                                      hovered_skin="sprites/Square Buttons/Colored Square Buttons/Return col_Square Button.png",
                                      position=[self.x + self.width - 50, self.y + self.height*3/4],
                                      func=self.delete_recipe))
    def delete_recipe(self):
        self.building.delete_recipe()
        self.buttons[0].pop()
