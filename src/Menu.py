import pygame

from src.CONST import GameConstants
from src.buttons.button import Button
from src.buttons.startbutton import StartButton
from src.drawing_pygame.Draw import Drawing
from src.logger.Logger import Logger, GlobalObject

class Menu(GlobalObject):
    id: int = 0

    def __init__(self, background=None, buttons=[[]], width=GameConstants.screen_width,
                 height=GameConstants.screen_height, x=0, y=0, **kwargs):
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
        self.Draw: Drawing = Drawing()
        self.is_active = False
        Logger.add_info("Menu is initialized ")

    def handle_hover(self) -> None:
        for buttons_list in self.buttons:
            for button in buttons_list:
                button.handle_hover()

    def update(self, event: pygame.event) -> None:
        for buttons_list in self.buttons:
            for button in buttons_list:
                button.update(event)

    def show(self) -> None:
        Logger.add_info("Showing menu")
        self.is_active = not (self.is_active)

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
        pygame.time.Clock().tick(GameConstants.fps)


class MainMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(buttons=[[]], **kwargs)
        k = 1
        self.buttons[0].append(StartButton(width=GameConstants.start_button_width,
                                           height=GameConstants.start_button_height,
                                           text="",
                                           not_hovered_skin="sprites/Large Buttons/Large Buttons/Start Button.png",
                                           hovered_skin="sprites/Large Buttons/Colored Large Buttons/Start  col_Button.png",
                                           position=GameConstants.start_button_position,
                                           start=kwargs["start"]))
        self.buttons[0].append(Button(width=GameConstants.start_button_width,
                                      height=GameConstants.start_button_height,
                                      text="",
                                      not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                      hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                      position=GameConstants.menu_exit_button_position,
                                      func=exit))
        self.background = "sprites/menu_back.png"
        Logger.add_info("MainMenu is initialized")


class BuildingMenu(Menu):
    def __init__(self, pos_x, pos_y, width, hight, building, recipes, function, **kwargs):
        super().__init__(buttons=[[]], **kwargs)
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = hight
        self.building = building
        self.recipes: list = recipes
        self.buttons[0].append(Button(width=GameConstants.small_button_size,
                                      height=GameConstants.very_small_button_size,
                                      text="",
                                      not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                      hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                      position=[pos_x + width - GameConstants.small_button_size,
                                                pos_y],
                                      func=function))

        self.buttons[0].append(Button(width=GameConstants.very_small_button_size,
                                      height=GameConstants.very_small_button_size,
                                      text="+1",
                                      not_hovered_skin="sprites/CLEAR.png",
                                      hovered_skin="sprites/CLEAR col.png",
                                      position=[
                                          self.x + self.width / 2 - GameConstants.small_button_size,
                                          self.y + self.height / 2 + GameConstants.small_button_size],
                                      func=self.add_fuel))

        self.buttons[0].append(Button(width=GameConstants.very_small_button_size,
                                      height=GameConstants.very_small_button_size,
                                      text="+5",
                                      not_hovered_skin="sprites/CLEAR.png",
                                      hovered_skin="sprites/CLEAR col.png",
                                      position=[
                                          self.x + self.width / 2 - GameConstants.very_small_button_size,
                                          self.y + self.height / 2 + GameConstants.small_button_size],
                                      func=self.add_fuel,
                                      argument=5))

        self.buttons.append([])
        for i, recipe in enumerate(self.recipes):
            self.buttons[1].append(Button(width=GameConstants.very_small_button_size,
                                          height=GameConstants.very_small_button_size,
                                          text="",
                                          not_hovered_skin="sprites/Square Buttons/Square Buttons/V Square Button.png",
                                          hovered_skin="sprites/Square Buttons/Colored Square Buttons/V col_Square Button.png",
                                          position=[
                                              self.x + self.width / 2 + GameConstants.medium_offset,
                                              self.y + GameConstants.medium_offset + i * (
                                                          GameConstants.very_small_button_size + GameConstants.small_offset)],
                                          func=self.activate_recipe,
                                          argument=recipe))

        self.buttons.append([])
        self.buttons[2].append(Button(width=GameConstants.very_small_button_size,
                                      height=GameConstants.very_small_button_size,
                                      text="",
                                      not_hovered_skin="sprites/Square Buttons/Square Buttons/On Off Square Button.png",
                                      hovered_skin="sprites/Square Buttons/Colored Square Buttons/On Off col_Square Button.png",
                                      position=[
                                          self.x + self.width / 2 - GameConstants.very_small_button_size,
                                          self.y],
                                      func=self.building.change_active))
        self.has_active_recipe = False
        self.active_recipe = None

    def activate_recipe(self, recipe):
        self.building.activate_recipe(recipe)
        if self.buttons[0][-1].func != self.delete_recipe:
            self.buttons[0].append(Button(width=GameConstants.small_button_size,
                                          height=GameConstants.very_small_button_size,
                                          text="ADD",
                                          not_hovered_skin="sprites/CLEAR.png",
                                          hovered_skin="sprites/CLEAR col.png",
                                          position=[
                                              self.x + self.width - 2 * GameConstants.small_button_size - GameConstants.small_button_size - GameConstants.medium_offset,
                                              self.y + self.height * GameConstants.last_quarter],
                                          func=self.add_resources))

            self.buttons[0].append(Button(width=GameConstants.small_button_size,
                                          height=GameConstants.very_small_button_size,
                                          text="GET",
                                          not_hovered_skin="sprites/CLEAR.png",
                                          hovered_skin="sprites/CLEAR col.png",
                                          position=[
                                              self.x + self.width - GameConstants.small_button_size - GameConstants.very_small_button_size - GameConstants.small_offset,
                                              self.y + self.height * GameConstants.last_quarter],
                                          func=self.get_resources))

            self.buttons[0].append(Button(width=GameConstants.very_small_button_size,
                                          height=GameConstants.very_small_button_size,
                                          text="",
                                          not_hovered_skin="sprites/Square Buttons/Square Buttons/Return Square Button.png",
                                          hovered_skin="sprites/Square Buttons/Colored Square Buttons/Return col_Square Button.png",
                                          position=[
                                              self.x + self.width - GameConstants.very_small_button_size,
                                              self.y + self.height * GameConstants.last_quarter],
                                          func=self.delete_recipe))

    def add_fuel(self, amount=1):
        item = self.building.fuel["name"]
        resource = self.building.active_player.get_item(item, amount)
        if resource is not None:
            for item, amount in resource.items():
                self.building.add_fuel(item, amount)

    def add_resources(self, amount=1):
        items = self.building.active_recipe.input_resources
        for item, amount in items.items():
            resource = self.building.active_player.get_item(item, amount)
            if resource is not None:
                for item, amount in resource.items():
                    self.building.add_input(item, amount)

    def get_resources(self):
        need_deleting = []
        for object, amount in self.building.output.items():
            print(object, amount)
            self.building.active_player.add_item(object, amount)
            self.building.output[object] = 0
            need_deleting.append(object)
        for object in need_deleting:
            del self.building.output[object]
            print(self.building.output)

    def delete_recipe(self):
        self.building.delete_recipe()
        self.buttons[0].pop()
        self.buttons[0].pop()
        self.buttons[0].pop()
        self.get_resources()
