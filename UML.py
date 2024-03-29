 
import pygame

from src.Menu import MainMenu
from src.SingleGame import SingleGame
import src.Menu

def main() -> None:
    pygame.init()
    info = pygame.display.Info()
    pygame.display.set_mode((info.current_w, info.current_h))
    Game = MainGame()
    Game.play()

class MainGame:
    def __init__(self):
        self.Status = "Menu"
        pygame.init()
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        self.Menu = MainMenu(width=screen_width, height=screen_height, start = self.change)
        self.Menu.show()

    def change(self, Status : str):
        self.Status = Status



    def play(self):
        while (True):
            if self.Status == "Menu":
                self.Menu.draw_menu()
                self.Menu.loop()
            elif self.Status == "Start_game":
                self.Menu.show()
                del self.Menu
                self.Status = "Game"
                self.Game = SingleGame()
            elif self.Status == "Game":
                self.Game.play()



if __name__ == "__main__":
    main()


from typing import Optional
from src.logger.Logger import Logger, GlobalObject
import pygame


class Button(GlobalObject):
    id = 0
    def __init__(self, text : str="START", width : int =100, height : int = 100, hovered_skin : str= "sprites/empty.png",
                 not_hovered_skin : str="sprites/empty.png", func=None,
                 position : list[int]=None, parent : Optional=None, parent_position : str = "absolute", argument = None, **kwargs) -> None:
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
        self.parent_position : str = parent_position
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

    def handle_event(self, event : pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.func:
                if self.argument:
                    self.func(self.argument)
                else:
                    self.func()

    def update(self, event : pygame.event) -> None:
        self.handle_hover()
        self.handle_event(event)

    def change_skin(self) -> None:
        if self.is_hovered:
            self.skin = self.hovered_skin
        else:
            self.skin = self.not_hovered_skin

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



from glob import glob

import pygame

from src.Player.player import Player
from src.buttons.button import Button
from src.logger.Logger import Logger, GlobalObject


class Drawing(GlobalObject):
    @staticmethod
    def in_kwargs(find_option, **kwargs):
        if find_option in kwargs.keys():
            return kwargs[find_option]
        else:
            return None

    def __init__(self, **kwargs):
        super().__init__()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.sprites = { None : pygame.image.load("sprites/empty.png").convert_alpha()}
        self.objects : dict = {}
        self.scale = self.in_kwargs("scale", **kwargs)
        self.LENGTH = self.in_kwargs("LENGTH", **kwargs)
        self.HIGHT = self.in_kwargs("HIGHT", **kwargs)
        self.field = self.in_kwargs("field", **kwargs)
        self.step = self.in_kwargs("step", **kwargs)

    def get_image(self, skin : str):
        if skin in self.sprites.keys():
            return self.sprites[skin]

        try:
            self.sprites[skin] = pygame.image.load(skin).convert_alpha()
            return self.sprites[skin]
        except Exception:
            Logger.add_errors(f"Cannot load skin {skin}")
            return self.sprites[None]

    def get_object_skin(self, items):
        if items not in self.objects:
            self.objects[items] = items()
        skin = self.objects[items].get_skin()
        return skin



    def update_parametrs(self, **kwargs):
        self.scale = kwargs["scale"]
        self.LENGTH = kwargs["LENGTH"]
        self.HIGHT = kwargs["HIGHT"]
        self.field = kwargs["field"]
        self.step = kwargs["step"]

    def draw(self, surface, player=None, board=None, this_single_square=None, object=None,
             inventory=None, pos_x=None,
             pos_y=None, draw_scale=1, button=None, Menu=None, building_menu=None, **kwargs):
        if board is not None:
            self.draw_board(surface=surface, board=board)
        if this_single_square is not None:
            self.draw_single_square(single_square=this_single_square)
        if object is not None:
            self.draw_object(surface, object=object, board=board, pos_x=pos_x, pos_y=pos_y,
                             draw_scale=draw_scale)
        if inventory is not None:
            self.draw_inventory(surface, inventory=inventory)
        if button is not None:
            self.draw_button(surface, button=button)
        if player is not None:
            self.draw_player(surface=surface, player=player, board=board)
        if Menu is not None:
            self.draw_menu(surface=surface, menu=Menu)
        if building_menu is not None:
            self.draw_building_menu(surface = surface, building_menu=building_menu)

    def draw_player(self, surface: pygame, player, board, draw_scale=1):
        text_skin = self.my_font.render(player.get_name(), False, (255, 0, 0))
        text_rect = text_skin.get_rect(
            center=(player.get_x() - board.get_game_pos_x(),
                    player.get_y() - board.get_game_pos_y() - self.scale // 2),
            width=self.scale)
        surface.blit(text_skin, text_rect)
        player_skin = self.get_image(player.get_skin())
        player_skin = pygame.transform.scale(player_skin, (
        2 * draw_scale * self.scale, 2 * draw_scale * self.scale))
        player_rect = player_skin.get_rect(
            center=(
            player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y()),
            width=self.scale)
        surface.blit(player_skin, player_rect)
        if player.get_status() == Player.statuses["inventory"]:
            self.draw_inventory(surface, inventory=player.get_inventory())

    def draw_object(self, surface: pygame, object, board, pos_x, pos_y, draw_scale=1):
        object_skin = self.get_image(object.get_skin())
        object_skin = pygame.transform.scale(object_skin,
                                             (draw_scale * self.scale, draw_scale * self.scale))
        object_rect = object_skin.get_rect(
            topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()),
            width=self.scale)
        surface.blit(object_skin, object_rect)

    def draw_inventory(self, surface: pygame, inventory):
        pygame.draw.rect(surface, (0, 0, 0), (self.LENGTH * 3 / 4, 0, self.LENGTH, self.HIGHT))
        text_skin = self.my_font.render("Inventory", False, (255, 255, 255))
        text_rect = text_skin.get_rect(
            midleft=(self.LENGTH * 3 / 4 + 20, 30),
            width=self.scale)
        surface.blit(text_skin, text_rect)

        small_scale = (self.LENGTH / 4) / (inventory.get_sizes()[0] + 3)
        for i in range(inventory.get_sizes()[0]):
            for j in range(inventory.get_sizes()[1]):
                pygame.draw.rect(surface, (255, 0, 0), (
                    20 + self.LENGTH * 3 / 4 + i * (small_scale + 10), 60 + (small_scale + 10) * j,
                    small_scale,
                    small_scale), 5)
                if inventory.get_grid()[i][j] != None:
                    items = inventory.get_grid()[i][j]
                    amount = inventory.get_amount()[i][j]
                    if items != None:
                        skin = self.get_object_skin(items)
                        object_skin = self.get_image(skin)
                        object_skin = pygame.transform.scale(object_skin,
                                                             (small_scale - 10, small_scale - 10))
                        object_rect = object_skin.get_rect(
                            topleft=(
                                20 + self.LENGTH * 3 / 4 + i * (small_scale + 10) + 5,
                                60 + (small_scale + 10) * j + 5),
                            width=self.scale)
                        surface.blit(object_skin, object_rect)
                        text_skin = self.my_font.render(f"{amount}", False, (255, 0, 0))
                        text_rect = text_skin.get_rect(
                            topleft=(
                                20 + self.LENGTH * 3 / 4 + i * (small_scale + 10) + 5,
                                60 + (small_scale + 10) * j + 5),
                            width=self.scale)
                        surface.blit(text_skin, text_rect)

        selected = inventory.is_selected()
        if selected:
            x, y = inventory.get_selected_item()
            pygame.draw.rect(surface, (0, 0, 255), (
                20 + self.LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y,
                small_scale,
                small_scale), 5)
        x, y = inventory.get_cursor()
        pygame.draw.rect(surface, (0, 255, 0), (
            20 + self.LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y,
            small_scale, small_scale),
                         5)

    def draw_single_square(self, surface: pygame, single_square, board, pos_x, pos_y, draw_scale=1):
        if (board.get_game_pos_x() - self.scale <= pos_x <= board.get_game_pos_x() + (
                self.LENGTH) + self.scale and board.get_game_pos_y() - self.scale <= pos_y <= board.get_game_pos_y() + (
                self.HIGHT) + self.scale):
            square_skin = self.get_image(single_square.get_skin())
            square_skin = pygame.transform.scale(square_skin,
                                                 (draw_scale * self.scale, draw_scale * self.scale))
            square_rect = square_skin.get_rect(
                topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()),
                width=self.scale)
            surface.blit(square_skin, square_rect)
            for object in single_square.get_buildings():
                self.draw_object(surface, object=object, pos_x=pos_x,
                                 pos_y=pos_y, board=board)
            for object in single_square.get_miners():
                self.draw_object(surface, board=board, object=object, pos_x=pos_x,
                                 pos_y=pos_y)

    def draw_board(self, surface: pygame, board):
        pygame.draw.rect(surface, (0, 0, 255), (0, 0, self.LENGTH, self.HIGHT))
        for i in range(max(0, board.get_game_pos_x() // self.scale),
                       min((board.get_game_pos_x() + self.LENGTH) // self.scale + 1, self.field)):
            for j in range(max(0, board.get_game_pos_y() // self.scale),
                           min((board.get_game_pos_y() + self.HIGHT) // self.scale + 1,
                               self.field)):
                self.draw_single_square(surface, board=board, pos_x=i * self.scale,
                                        pos_y=j * self.scale,
                                        single_square=board.get_grid()[i][j])

    def draw_button(self, surface: pygame, button: Button):
        image = pygame.transform.scale(self.get_image(button.skin), (button.width, button.height))
        rect = image.get_rect(topright=button.position)
        surface.blit(image, rect.topright)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(button.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(button.position[0] + button.width/2, button.position[1] + button.height/2))
        surface.blit(text_surface, text_rect)

    def draw_menu(self, surface: pygame, menu):
        square_skin = self.get_image(menu.background)
        square_skin = pygame.transform.scale(square_skin, (menu.width, menu.height))
        square_rect = square_skin.get_rect(
            topleft=(menu.x, menu.y))
        surface.blit(square_skin, square_rect)
        for button_line in menu.buttons:
            for button in button_line:
                self.draw_button(surface=surface, button=button)

    def draw_building_menu(self, surface: pygame, building_menu = None):
        pygame.draw.rect(surface, (20, 20, 20), (building_menu.x, building_menu.y, building_menu.width, building_menu.height))
        pygame.draw.rect(surface, (30, 30, 30), (
        building_menu.x, building_menu.y, building_menu.width/2, building_menu.height))
        pygame.draw.rect(surface, (10, 10, 10), (
        building_menu.x + building_menu.width/2, building_menu.y, building_menu.width/2, building_menu.height/2))
        image = pygame.transform.scale(self.get_image(building_menu.building.get_skin()), (building_menu.width/2, building_menu.height))
        rect = image.get_rect(topright=(building_menu.x,building_menu.y))
        surface.blit(image, rect.topright)
        for button_line in building_menu.buttons:
            for button in button_line:
                self.draw_button(surface=surface, button=button)

        rect_color = (50,50,50)
        size = 100
        boarder_size = 4
        pygame.draw.rect(surface, rect_color, (building_menu.x + building_menu.width/2 - size, building_menu.y + building_menu.height/2, size, size), boarder_size)
        image = pygame.transform.scale(self.get_image(self.get_object_skin(building_menu.building.fuel["name"])),
                                       (size - 2 * boarder_size, size - 2 * boarder_size))
        rect = image.get_rect(topright=(building_menu.x + building_menu.width/2 + boarder_size  - size, building_menu.y + building_menu.height/2 + boarder_size))
        amount = building_menu.building.fuel["amount"]
        surface.blit(image, rect.topright)
        text_skin = self.my_font.render(f"{amount}", False, (255, 0, 0))
        text_rect = text_skin.get_rect(
            topleft=(building_menu.x + building_menu.width/2 + boarder_size  - size, building_menu.y + building_menu.height/2 + boarder_size),
            width=self.scale)
        surface.blit(text_skin, text_rect)
        text_skin = self.my_font.render("Топливо:", False, (255, 0, 0))
        text_rect = text_skin.get_rect(
            topleft=(building_menu.x + building_menu.width / 2 + boarder_size - size,
                     building_menu.y + building_menu.height / 2 - 30),
            width=self.scale)
        surface.blit(text_skin, text_rect)


        for i,recipe in enumerate(building_menu.recipes):
            self.draw_recipe(surface=surface, recipe=recipe, position = [building_menu.x + building_menu.width/2 + 100, building_menu.y + 20 + i * (50 + 10)])

        if building_menu.building.active_recipe == None:
            font = pygame.font.Font(None, 72)
            text_surface = font.render("У вас нет активного рецепта", True, (255,0,0))
            text_rect = text_surface.get_rect(topright=(building_menu.x + building_menu.width - 20, building_menu.y + building_menu.height * 3/4 ))
            surface.blit(text_surface, text_rect)
        else:
            self.draw_recipe(surface, building_menu.building.active_recipe, position = [building_menu.x + building_menu.width/2 +20, building_menu.y + building_menu.height*3/4])




    def draw_recipe(self, surface, recipe, position):
        size = 50
        boarder_size = 4
        rect_color = (40,40,40)
        for i,(item,amount) in enumerate(recipe.input_resources.items()):
            pygame.draw.rect(surface, rect_color, (position[0] + 10 + i * (size + 10), position[1], size, size), boarder_size)
            image = pygame.transform.scale(self.get_image(self.get_object_skin(item)),
                                           (size-2*boarder_size, size-2*boarder_size))
            rect = image.get_rect(topright=(position[0] + 10 + i * (size + 10) + boarder_size, position[1] + boarder_size))
            surface.blit(image, rect.topright)
            text_skin = self.my_font.render(f"{amount}", False, (255, 0, 0))
            text_rect = text_skin.get_rect(
                topleft=(position[0] + 10 + i * (size + 10) + boarder_size, position[1] + boarder_size),
                width=self.scale)
            surface.blit(text_skin, text_rect)

        start_output = 10 + len(recipe.input_resources.keys()) * (size + 10)

        arrow = "sprites/Square Buttons/Square Buttons/Next Square Button.png"
        image = pygame.transform.scale(self.get_image(arrow), (size,size))
        rect = image.get_rect(topright=(position[0] + start_output, position[1]))
        surface.blit(image, rect.topright)



        start_output += 50
        for i,(item,amount) in enumerate(recipe.output_resources.items()):
            pygame.draw.rect(surface, rect_color, (position[0] + 10 + i * (size + 10) + start_output, position[1], size, size), boarder_size)
            image = pygame.transform.scale(self.get_image(self.get_object_skin(item)),
                                           (size-2*boarder_size, size-2*boarder_size))
            rect = image.get_rect(topright=(position[0] + 10 + i * (size + 10) + boarder_size + start_output, position[1] + boarder_size))
            surface.blit(image, rect.topright)
            text_skin = self.my_font.render(f"{amount}", False, (255, 0, 0))
            text_rect = text_skin.get_rect(
                topleft=(position[0] + 10 + i * (size + 10) + boarder_size + start_output, position[1] + boarder_size))
            surface.blit(text_skin, text_rect)







from random import randint

from src.Game.Squares.Ground import Ground
from src.Game.Squares.Water import Water
from src.Game.single_square import SingleSquare
from src.Objects.Miners.Fertile_soil.Fertile_soil import Fertile_soil
from src.Objects.Miners.Trees.Tree import Tree
from src.Objects.buildings.furnace.furnace import Furnace
from typing import Optional
from src.logger.Logger import Logger, GlobalObject


class Board(GlobalObject):
    id = 0

    def __init__(self, field : int=400, water_amount : int=10, water_size : int = 5, tree_amount : int = 10,
                 fertile_soil_amount : int=10):
        super().__init__()
        Board.id +=1
        self.__id = Board.id
        self.__grid : list[list[Optional[SingleSquare]]] = [[None for i in range(field)] for j in range(field)]
        self.__game_pos_x : int = 0
        self.__game_pos_y : int = 0
        self.__cat_box : tuple[int,int] = (300, 150)
        self.field : int = field
        for i in range(field):
            for j in range(field):
                self.__grid[i][j] = Ground()

        for k in range(water_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            for i in range(water_size):
                for j in range(water_size):
                    self.__grid[x + i][y + j]=Water()

        for k in range(tree_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            self.__grid[x][y].add_miner(Tree())

        for k in range(fertile_soil_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            self.__grid[x][y].add_miner(Fertile_soil())

        self.__grid[1][1].add_building(Furnace())
        Logger.add_info(f"Board is initialized with id {self.__id}")

    def __repr__(self) -> str:
        for i in range(self.field):
            for j in range(self.field):
                print(self.__grid[i][j])
        return ""

    def increase_coordinates(self, x : int, y : int) -> None:
        self.update_cordinates(self.__game_pos_x + x, self.__game_pos_y + y)

    def update_cordinates(self, new_x : int, new_y : int) -> None:
        self.__game_pos_x : int = new_x
        self.__game_pos_y : int = new_y

    def get_grid(self) -> Optional[list[list[Optional[SingleSquare]]]]:
        return self.__grid

    def get_grid_size(self) -> int:
        return self.field

    def get_cat_box(self) -> tuple:
        return self.__cat_box

    def set_grid(self, new_grid : list[list[Optional[SingleSquare]]]):
        self.__grid = new_grid

    def set_cat_box(self, new_cat : tuple[int,int]):
        self.__cat_box = new_cat

    def get_game_pos(self) -> tuple:
        return (self.__game_pos_x, self.__game_pos_y)

    def get_game_pos_x(self) -> int:
        return self.__game_pos_x

    def get_game_pos_y(self) -> int:
        return self.__game_pos_y

    def update(self) -> None:
        for i in range(self.field):
            for j in range(self.field):
                    self.__grid[i][j].update()

    def get_active_building_menu(self):
        for i in range(self.field):
            for j in range(self.field):
                for building in self.__grid[i][j].get_buildings():
                    if building.is_active_menu:
                        return building.Menu
        return None


from src.Objects.GameObject import GameObject
from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Resources import Resources
from src.Objects.buildings.Buildings import Building
from typing import Optional
from src.logger.Logger import Logger, GlobalObject


class SingleSquare(GlobalObject):
    id : int = 0

    def __take_prototipe__(self, prototipe) -> None:
        self._skin : Optional[str] = prototipe.get_skin()
        self.is_player_available : bool = prototipe.is_player_available
        self._buildings : list[Building] = prototipe.get_buildings()
        self._miners : list[Miners] = prototipe.get_miners()
        self._resources : list[Resources] = prototipe.get_resources()
        Logger.add_info("Got info for Single Square from prototipe")

    def __init__(self, skin : Optional[str] = None, prototipe =None):
        super().__init__()
        SingleSquare.id += 1
        self.__id : int = SingleSquare.id
        if prototipe == None:
            self._skin : Optional[str] = skin
            self._buildings : list[Building] = []
            self._miners : list[Miners] = []
            self._resources : list[Resources] = []
        else:
            self.__take_prototipe__(prototipe)
        Logger.add_info(f"SingleSquare is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"Objects {self._buildings} in single square with id {self.__id} and skin {self.get_skin()}. Also has {self._miners} miners. Also has {self._resources}"

    def set_skin(self, skin : Optional[str]=None, prototipe=None):
        self._skin : Optional[str] = skin
        if prototipe is not None:
            self.__take_prototipe__(prototipe)

    def get_skin(self) -> str:
        return self._skin

    def add_building(self, object : Building) -> None:
        Logger.add_info(f"Adding building for SingleSquare with id {self.__id}")
        self._buildings.append(object)

    def get_buildings(self) -> list[Building]:
        return self._buildings

    def get_miners(self) -> list[Miners]:
        return self._miners

    def copy(self):
        return SingleSquare(prototipe=self)

    def update(self) -> None:
        for object in self._buildings:
            object.update()

    def add_miner(self, miner : Miners) -> None:
        Logger.add_info(f"Adding miner for SingleSquare with id {self.__id}")
        if self.is_player_available and len(self._miners) == 0:
            self._miners.append(miner)

    def mine(self) -> Optional[Resources]:
        Logger.add_info(f"Mining resources in SingleSquare with id {self.__id}")
        for i in range(len(self._miners)):
            resource = self._miners[i].get_resource()
            if resource is not None:
                return resource
            else:
                self._miners.pop(i)

    def get_resources(self) -> list[Resources]:
        return self._resources


from src.Game.single_square import SingleSquare
from src.logger.Logger import Logger, GlobalObject

class Ground(SingleSquare):
    id = 0
    def __init__(self):
        Ground.id += 1
        self.__id = Ground.id
        super().__init__()
        self._skin = "sprites/mishaZemlya.png"
        self.is_player_available = True
        Logger.add_info(f"Ground is initialized with (id - {self.__id})")


from src.Game.single_square import SingleSquare
from src.logger.Logger import Logger, GlobalObject

class Water(SingleSquare):
    id = 0
    def __init__(self):
        Water.id += 1
        self.__id = Water.id
        super().__init__()
        self._skin = "sprites/mishaVoda.png"
        self.is_player_available = False
        Logger.add_info(f"Water is initialized with (id - {self.__id})")



import datetime
import logging
import os
from typing import Optional


def add_str_to_file(str_to_write: str, file_name: str, filemod: Optional[str] = "a") -> None:
    with open(f"{file_name}", filemod) as file:
        file.write(str_to_write + "\n")

class Logger:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    id = 0
    objects = {}
    date = datetime.datetime.now().strftime("%Y-%m-%d---%H:%M:%S")
    os.makedirs(f"logs/{date}", mode=0o777, exist_ok=True)
    info: str = f"logs/{date}/info.log"
    warnings: str = f"logs/{date}/warnings.log"
    errors: str = f"logs/{date}/errors.log"
    debug: str = f"logs/{date}/debug.log"
    add_str_to_file("Game started\n", info, filemod="w")
    add_str_to_file("Game started\n", warnings, filemod="w")
    add_str_to_file("Game started\n", errors, filemod="w")
    add_str_to_file("Game started\n", debug, filemod="w")


    @classmethod
    def add_info(cls, text : str) -> None:
        logging.info(text)
        add_str_to_file(text, cls.info)

    @classmethod
    def add_warnings(cls, text : str) -> None:
        logging.warning(text)
        add_str_to_file(text, cls.warnings)

    @classmethod
    def add_errors(cls, text : str) -> None:
        logging.error(text)
        add_str_to_file(text, cls.errors)

    @classmethod
    def add_debug(cls, text : str) -> None:
        logging.debug(text)
        add_str_to_file(text, cls.debug)


class GlobalObject:
    id = 0
    def __init__(self):
        GlobalObject.id += 1
        Logger.objects[GlobalObject.id] = self



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

        self.buttons[0].append(Button(width=50,
                                      height=50,
                                      text="+1",
                                      not_hovered_skin="sprites/CLEAR.png",
                                      hovered_skin="sprites/CLEAR col.png",
                                      position=[self.x + self.width/2 - 100, self.y + self.height/2 + 100],
                                      func=self.add_fuel))

        self.buttons[0].append(Button(width=50,
                                      height=50,
                                      text="+5",
                                      not_hovered_skin="sprites/CLEAR.png",
                                      hovered_skin="sprites/CLEAR col.png",
                                      position=[self.x + self.width/2 - 50, self.y + self.height/2 + 100],
                                      func=self.add_fuel,
                                      argument=5))

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

    def add_fuel(self, amount = 1):
        item = self.building.fuel["name"]
        resource = self.building.active_player.get_item(item, amount)
        if resource is not None:
            for item, amount in resource.items():
                self.building.add_fuel(item, amount)

    def delete_recipe(self):
        self.building.delete_recipe()
        self.buttons[0].pop()
        for object, amount in self.building.output.items():
            self.building.active_player.add_item(object, amount)
            self.building.output[object] = 0


import time

from src.Objects.GameObject import GameObject
from src.Objects.Resources.Resources import Resources
from typing import Optional
from src.logger.Logger import Logger
import src.Menu
from src.Objects.buildings.Recipe import Recipe
from src.Objects.Resources.Wood.Wood import Wood
from src.Objects.Resources.Soil.Soil import Soil

class Building(GameObject):
    id : int = 0
    def __init__(self) -> None:
        Building.id += 1
        self.__id = Building.id
        super().__init__()
        self._skin : Optional[str] = None
        self.active_skin : Optional[str] = None
        self.inactive_skin : Optional[str] = None
        self._type : str = "buildings"
        self.input : dict = {}
        self.output : dict = {}
        self.fuel = {}
        self.__is_active : bool = False
        self.__start_of_active : time.time = time.time()
        self.is_active_menu = False
        self.Menu = src.Menu.BuildingMenu(200, 150, 1500,500,self,[Recipe(input={Wood:1}, output={Soil:20}),Recipe(input={Wood:1}, output={Soil:1}),Recipe(input={Wood:1, Soil:100}, output={Soil:1}),Recipe(input={Soil:1}, output={Wood:1})],self.change_menu)
        self.has_active_recipe = False
        self.active_recipe = None
        self.active_player = None
        Logger.add_info(f"Building is initialized with (id - {self.__id})")

    def add_fuel(self, item, amount = 1):
        self.fuel["amount"] += amount

    def activate_recipe(self, recipe):
        self.has_active_recipe = True
        self.active_recipe = recipe
        print(self.active_recipe)

    def delete_recipe(self):
        self.has_active_recipe = False
        self.active_recipe = None
        self.__is_active = False
        self.change_skin()

    def __repr__(self) -> str:
        return f"Building with {self.input} and {self.output}"

    def change_menu(self, player=None) -> None:
        self.is_active_menu = not self.is_active_menu
        self.active_player = player

    def change_active(self) -> None:
        if self.active_recipe == None:
            Logger.add_warnings(f"Trying to activate a building with id {self.__id} without a recipe")
            self.__is_active : bool = False
            self.change_skin()
            return None
        if self.fuel["amount"] < self.fuel["fuel_cost"]:
            Logger.add_warnings(
                f"Trying to activate a building with id {self.__id} without enough fuel")
            self.__is_active: bool = False
            self.change_skin()
            return None
        for item, amount in self.active_recipe.input_resources.items():
            if item not in self.input.keys():
                Logger.add_warnings(f"We don`t have resource {item} in building input with id {self.__id}")
                self.__is_active: bool = False
                self.change_skin()
                return None
            if self.input[item] < amount:
                Logger.add_warnings(f"We don`t have enough resource {item} in building with id {self.__id}")
                self.__is_active: bool = False
                self.change_skin()
                return None
        self.__is_active = not self.__is_active
        self.change_skin()

    def change_skin(self) -> None:
        if self.__is_active:
            self._skin = self.active_skin
        else:
            self._skin = self.inactive_skin

    def update(self) -> None:
        if self.__is_active:
            if self.fuel["burning_time"] < time.time() - self.__start_of_active:
                print(self)
                print(f"burning time: {time.time()}")
                self.__start_of_active = time.time()
                if self.fuel["amount"] >= self.fuel["fuel_cost"]:
                    self.fuel["amount"] -= self.fuel["fuel_cost"]
                    for resource, amount in self.active_recipe.input_resources.items():
                        if self.input[resource] < amount:
                            self.__is_active = False
                            self.change_skin()
                            break
                    if self.__is_active:
                        for resource, amount in self.active_recipe.input_resources.items():
                            self.input[resource] -= amount
                        for resource, amount in self.active_recipe.output_resources.items():
                            if resource not in self.output.keys():
                                self.output[resource] = 0
                            self.output[resource] += amount
                else:
                    self.__is_active = False
                    self.change_skin()

    def get_skin(self) -> str:
        return self._skin

    def get_type(self) -> str:
        return self._type


import time

from src.Objects.buildings.Buildings import Building
from src.logger.Logger import Logger, GlobalObject
from src.Objects.Resources.Wood.Wood import Wood


class Furnace(Building):
    id : int = 0
    def __init__(self):
        Furnace.id += 1
        self.__id = Furnace.id
        super().__init__()
        self._skin : str = "sprites/furnace.png"
        self._type : str = "buildings"
        self.input : dict = {
            Wood : 1000
        }
        self.output : dict[str,int] = {
        }
        self.fuel : dict[str,int | str] = {
            "name": Wood,
            "amount": 10,
            "burning_time": 1,
            "fuel_cost": 1
        }
        self.__is_active : bool = False
        self.__start_of_active : time.time = time.time()
        self.active_skin : str = "sprites/burning_furnace.png"
        self.inactive_skin : str = "sprites/furnace.png"
        Logger.add_info(f"Furnace is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"


from src.logger.Logger import GlobalObject

class Recipe(GlobalObject):
    def __init__(self, input = {}, output = {}):
        super().__init__()
        self.input_resources = input
        self.output_resources = output




from collections.abc import Callable
from typing import Optional
from src.logger.Logger import Logger, GlobalObject

class GameObject(GlobalObject):

    def __get_prototipe(self, prototipe) -> None:
        pass

    def __init__(self):
        super().__init__()

        Logger.add_info(f"GameObject created")

    def get_skin(self) -> str:
        pass

    def get_type(self) -> str:
        pass


from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Soil.Soil import Soil
from src.logger.Logger import Logger, GlobalObject

class Fertile_soil(Miners):
    id : int = 0
    def __init__(self):
        super().__init__(resource=Soil, amount=10, skin="sprites/fertile_soil.png")
        Fertile_soil.id += 1
        self.__id = Fertile_soil.id
        Logger.add_info(f"Fertile_soil is initialized with (id - {self.__id})")


from src.Objects.GameObject import GameObject
from src.Objects.Resources.Resources import Resources
from typing import Optional
from src.logger.Logger import Logger, GlobalObject

class Miners(GameObject):
    id : int = 0
    def __init__(self, resource : Optional[Resources]=None, amount : Optional[int]=0, skin : Optional[str]=None):
        Miners.id += 1
        self.__id = Miners.id
        self._resource : Optional[resource] = resource
        self._amount : int = amount
        self._skin : Optional[str] = skin
        Logger.add_info(f"Miner is initialized with (id - {self.__id})")

    def __repr__(self) -> str:
        return f"_resource {self._resource} _amount {self._amount} _skin {self._skin}"

    def get_resource(self) -> Optional[Resources]:
        if self._amount > 0:
            self._amount -= 1
            return self._resource
        else:
            return None

    def get_skin(self) -> str:
        return self._skin


from src.Objects.Miners.miners import Miners
from src.Objects.Resources.Wood.Wood import Wood
from src.logger.Logger import Logger, GlobalObject

class Tree(Miners):
    id : int = 0
    def __init__(self):
        Tree.id += 1
        self.__id = Tree.id
        super().__init__(resource=Wood, amount=10, skin="sprites/tree.png")
        Logger.add_info(f"Tree is initialized with (id - {self.__id})")


from src.Objects.GameObject import GameObject
from typing import Optional
from src.logger.Logger import Logger, GlobalObject

class Resources(GameObject):

    id : int = 0

    def __from_prototipe(self, prototipe) -> None:
        self._skin = prototipe.get_skin()
        self._is_burnable = prototipe.get_is_burnable()
        Logger.add_info("Getting Resources from prototipe")

    def __init__(self, prototipe : Optional =None):
        Resources.id += 1
        self.__id = Resources.id
        if prototipe:
            self.__from_prototipe(prototipe)
        Logger.add_info(f"Resource is initialized with (id - {self.__id})")

    def get_skin(self) -> str:
        return self._skin

    def get_is_burnable(self) -> bool:
        return self._is_burnable

    def copy(self):
        return Resources(prototipe=self)


from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger, GlobalObject

class Soil(Resources):
    id : int = 0
    def __init__(self) -> None:
        Soil.id += 1
        self.__id = Soil.id
        super().__init__()
        self._is_burnable = False
        self._skin = "sprites/soil.png"
        Logger.add_info(f"Soil is initialized with (id - {self.__id})")




from src.Objects.Resources.Resources import Resources
from src.logger.Logger import Logger, GlobalObject

class Wood(Resources):
    id = 0
    def __init__(self) -> None:
        Wood.id += 1
        self.__id = Wood.id
        super().__init__()
        self._is_burnable = True
        self._skin = "sprites/wood.jpg"
        Logger.add_info(f"Wood is initialized with (id - {self.__id})")




from src.Objects.GameObject import GameObject
from src.Objects.buildings.furnace.furnace import Furnace
from src.Objects.Resources.Wood.Wood import Wood
from src.logger.Logger import Logger, GlobalObject


class inventory(GlobalObject):

    def __init__(self, size_x=5, size_y=10, scale=None):
        super().__init__()
        self._grid = [[None for i in range(size_y)] for j in range(size_x)]
        self._amount = [[0 for i in range(size_y)] for j in range(size_x)]
        self._size_x = size_x
        self._size_y = size_y
        self._cursor = [0, 0]
        self._selected_item = None
        self._is_selected = False
        self._scale = scale / 2
        self.add_item(Furnace)
        self.add_item(Wood, 100)

    def __repr__(self) -> str:
        return f"Inventory {self._grid}"

    def get_selected_item(self) -> GameObject:
        return self._selected_item

    def get_cursor(self) -> list[int]:
        return self._cursor

    def get_sizes(self) -> tuple:
        return (self._size_x, self._size_y)

    def add_item(self, item, amount = 1, pos=None):
        try:
            if item is not None:
                if pos is None:
                    for i in range(self._size_x):
                        for j in range(self._size_y):
                            if self._grid[i][j] != None and item == self._grid[i][j]:
                                pos = (i, j)
                                raise StopIteration
                            if self._grid[i][j] == None:
                                pos = (i, j)
                                self._grid[i][j] = item
                                raise StopIteration
        except StopIteration:
            self._amount[pos[0]][pos[1]] += amount

    def get_item(self, item, amount = 1, pos=None):
        try:
            if item is not None:
                if pos is None:
                    for i in range(self._size_x):
                        for j in range(self._size_y):
                            if self._grid[i][j] != None and item == self._grid[i][j]:
                                pos = (i, j)
                                raise StopIteration
                            if self._grid[i][j] == None:
                                pos = (i, j)
                                self._grid[i][j] = item
                                raise StopIteration

            return None
        except StopIteration:
            if self._amount[pos[0]][pos[1]] < amount:
                can_return = self._amount[pos[0]][pos[1]]
                self._amount[pos[0]][pos[1]] = 0
                self._grid[pos[0]][pos[1]] = None
                return {item : can_return}
            self._amount[pos[0]][pos[1]] -= amount
            return {item : amount}

    def move_right(self):
        self._cursor[0] += 1
        self._cursor[0] %= self._size_x

    def move_left(self):
        self._cursor[0] -= 1
        self._cursor[0] %= self._size_x

    def move_up(self):
        self._cursor[1] -= 1
        self._cursor[1] %= self._size_y

    def move_down(self):
        self._cursor[1] += 1
        self._cursor[1] %= self._size_y

    def select(self):
        self._is_selected = not self._is_selected
        self._selected_item = self._cursor.copy() if self._is_selected else None

    def take_item(self) -> GameObject | None:
        item = self._grid[self._selected_item[0]][self._selected_item[1]]
        self._grid[self._selected_item[0]][self._selected_item[1]] = None
        return item

    def get_grid(self) -> list[list[GameObject | None]]:
        return self._grid

    def get_amount(self) -> list[list[int]]:
        return self._amount

    def is_selected(self) -> bool:
        return self._is_selected


import pygame

from src.Player.Inventory import inventory
from src.logger.Logger import Logger, GlobalObject


class Player(GlobalObject):
    statuses = {
        'paused': 1,
        'walking': 2,
        'inventory': 3,
        'crafting': 4
    }

    def __init__(self, name="Mihaham", position_x=0, position_y=0, skin="sprites/bottom.png",
                 settings=None, scale=72):
        super().__init__()
        self.__name = name
        self.__inventory = inventory(scale=scale)
        self.__x = position_x
        self.__y = position_y
        self.__skin = skin
        self.__direction = [0, 0]
        self.__status = Player.statuses["walking"]
        self.__settings = {
            "up": pygame.K_w,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "down": pygame.K_s,
            "set_object": pygame.K_RETURN,
            "inventory": pygame.K_i
        } if settings is None else settings

    def __repr__(self) -> str:
        return f"Player {self.__name}"

    def move(self, event, board=None, scale=72):
        if self.__status == Player.statuses["walking"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()

                if event.key == self.__settings["up"]:
                    self.__direction[1] = -1
                if event.key == self.__settings["left"]:
                    self.__direction[0] = -1
                if event.key == self.__settings["down"]:
                    self.__direction[1] = 1
                if event.key == self.__settings["right"]:
                    self.__direction[0] = 1
                if event.key == self.__settings["set_object"]:
                    if board.get_grid()[min(self.__x // scale,len(board.get_grid())-1)][min(self.__y // scale,len(board.get_grid()[0])-1)].get_buildings() != []:
                        board.get_grid()[min(self.__x // scale,len(board.get_grid())-1)][min(self.__y // scale,len(board.get_grid()[0])-1)].get_buildings()[
                            0].change_menu(player = self)
                    if board.get_grid()[min(self.__x // scale,len(board.get_grid())-1)][min(self.__y // scale,len(board.get_grid()[0])-1)].get_miners() != []:
                        item = board.get_grid()[min(self.__x // scale,len(board.get_grid())-1)][min(self.__y // scale,len(board.get_grid()[0])-1)].mine()
                        self.__inventory.add_item(item)
                if event.key == self.__settings["inventory"]:
                    self.__direction = [0, 0]
                    self.__status = Player.statuses["inventory"]
            if event.type == pygame.KEYUP:
                if event.key == self.__settings["up"]:
                    self.__direction[1] = 0
                if event.key == self.__settings["left"]:
                    self.__direction[0] = 0
                if event.key == self.__settings["down"]:
                    self.__direction[1] = 0
                if event.key == self.__settings["right"]:
                    self.__direction[0] = 0
            self.update_skin()
        elif self.__status == Player.statuses["inventory"]:
            if event.type == pygame.KEYDOWN:
                if event.key == self.__settings["up"]:
                    self.__inventory.move_up()
                if event.key == self.__settings["down"]:
                    self.__inventory.move_down()
                if event.key == self.__settings["right"]:
                    self.__inventory.move_right()
                if event.key == self.__settings["left"]:
                    self.__inventory.move_left()
                if event.key == self.__settings["set_object"]:
                    self.__inventory.select()

                if event.key == self.__settings["inventory"]:
                    self.__status = self.statuses["walking"]

    def update_skin(self):
        if self.__direction == [0, 0]:
            self.__skin = "sprites/bottom.png"
        if self.__direction == [0, 1]:
            self.__skin = "sprites/bottom.png"
        if self.__direction == [0, -1]:
            self.__skin = "sprites/top.png"
        if self.__direction == [1, 0]:
            self.__skin = "sprites/right.png"
        if self.__direction == [-1, 0]:
            self.__skin = "sprites/left.png"
        if self.__direction == [-1, -1]:
            self.__skin = "sprites/topleft.png"
        if self.__direction == [-1, 1]:
            self.__skin = "sprites/bottomleft.png"
        if self.__direction == [1, 1]:
            self.__skin = "sprites/bottomright.png"
        if self.__direction == [1, -1]:
            self.__skin = "sprites/topright.png"

    def get_inventory(self) -> inventory:
        return self.__inventory

    def get_status(self) -> int:
        return self.__status

    def get_name(self) -> str:
        return self.__name

    def rename(self, new_name):
        self.__name = new_name

    def get_skin(self) -> str:
        return self.__skin

    def get_direction(self) -> list[int]:
        return self.__direction

    def get_position(self) -> tuple[int, int]:
        return self.__x, self.__y

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def set_direction(self, new_direction):
        self.__direction = new_direction

    def update_position(self, position):
        self.__x, self.__y = position

    def update(self, board, step=None, scale=None, field=None, Center_x=0, Center_y=0):
        new_x = (self.__direction[0] * step + self.__x)
        new_y = (self.__direction[1] * step + self.__y)
        if 0 <= new_x <= (field) * scale and 0 <= new_y <= (field) * scale:
            if (board.get_grid()[min(new_x // scale, field - 1)][
                min(new_y // scale, field - 1)].is_player_available):
                if not (Center_x - board.get_cat_box()[
                    0] <= new_x - board.get_game_pos_x() <= Center_x +
                        board.get_cat_box()[
                            0] and Center_y - board.get_cat_box()[
                            1] <= new_y - board.get_game_pos_y() <= Center_y +
                        board.get_cat_box()[
                            1]):
                    board.increase_coordinates(self.__direction[0] * step,
                                               self.__direction[1] * step)
                self.update_position(
                    (self.__direction[0] * step + self.__x, self.__direction[1] * step + self.__y))

    def add_item(self, object, amount = 1):
        self.__inventory.add_item(object, amount)

    def get_item(self, object, amount = 1):
        return self.__inventory.get_item(object, amount)

import pygame

from src.Game.Board import Board
from src.Player.player import Player
from src.buttons.button import Button
from src.drawing_pygame.Draw import Drawing
from src.logger.Logger import Logger, GlobalObject


class SingleGame(GlobalObject):
    id: int = 0

    def __init__(self, ):
        super().__init__()
        SingleGame.id += 1
        self.__id: int = SingleGame.id
        self.fps: int = 60
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        self.LENGTH: int = screen_width
        self.HIGHT: int = screen_height
        self.step: int = 12
        self.scale: int = 72
        self.field: int = 20
        self.water_amount: int = 1
        self.water_size: int = 4
        self.tree_amount: int = 1
        self.fertile_soil_amount: int = 10
        self.center_x: int = self.LENGTH // 2
        self.center_y: int = self.HIGHT // 2
        pygame.font.init()

        self.clock: pygame.time.Clock = pygame.time.Clock()
        pygame.display.set_caption("Really russian game")

        self.surface: pygame.display = pygame.display.set_mode((self.LENGTH, self.HIGHT))
        self.Exit: Button = Button(width=self.LENGTH // 10,
                                   height=self.HIGHT // 10,
                                   text="",
                                   not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                   hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                   position=[self.LENGTH - self.LENGTH // 10, 0],
                                   func=exit)
        self.Screen: Button = Button(width=self.LENGTH // 15,
                                     height=self.HIGHT // 10,
                                     text="FULLSCREEN MODE",
                                     not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                                     hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                                     # position=[self.LENGTH - self.LENGTH // 15, 100],
                                     position=[0, 0],
                                     func=self.change_screen_size)
        self.Draw: Drawing = Drawing(scale=self.scale, LENGTH=self.LENGTH, HIGHT=self.HIGHT,
                                     field=self.field, step=self.step)
        self.board: Board = Board(field=self.field, water_amount=self.water_amount,
                                  water_size=self.water_size,
                                  tree_amount=self.tree_amount,
                                  fertile_soil_amount=self.fertile_soil_amount)
        self.player: Player = Player(position_x=self.center_x, position_y=self.center_y,
                                     scale=self.scale)

        self.active_building_menu = None

        Logger.add_info(f"Game is initialized with (id - {self.__id})")

    def play(self) -> None:
        self.Draw.draw(self.surface, player=self.player, board=self.board, button=self.Exit)
        #self.Draw.draw(self.surface, button=self.Screen)
        self.active_building_menu = self.board.get_active_building_menu()
        self.Draw.draw(self.surface, building_menu=self.active_building_menu)
        self.Exit.handle_hover()
        self.Screen.handle_hover()
        if self.active_building_menu is not None:
            self.active_building_menu.handle_hover()
        for event in pygame.event.get():
            if self.active_building_menu is not None:
                self.active_building_menu.update(event)
            self.Exit.update(event)
            self.Screen.update(event)
            if event.type == pygame.QUIT:
                self.Log.add_info("Game is over")
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.player.move(event, board=self.board, scale=self.scale)
        self.player.update(self.board, scale=self.scale, field=self.field,
                           Center_x=self.center_x,
                           Center_y=self.center_y, step=self.step)
        self.board.update()

        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.fps)

    def update_screen_size(self, x: int, y: int) -> None:
        Logger.add_info(f"Screen sizes are updated with parametrs x = {x}, y = {y}")
        self.LENGTH = x
        self.HIGHT = y

    def change_screen_size(self) -> None:
        Logger.add_info("Screen size is updated")
        if self.LENGTH == pygame.display.Info().current_w:
            self.LENGTH = 2000
            self.surface = pygame.display.set_mode((self.LENGTH, 1000))
        else:
            info = pygame.display.Info()
            self.update_screen_size(info.current_w, info.current_h)
            self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.Draw.update_parametrs(scale=self.scale, LENGTH=self.LENGTH, HIGHT=self.HIGHT,
                                   field=self.field,
                                   step=self.step)


class GameAdapter:
    @classmethod
    def get_game_parameters(cls, Game: SingleGame) -> dict:
        Logger.add_info("Getting info about SingleGame")
        dict = {}
        dict["fps"] = Game.fps
        dict["LENGTH"] = Game.LENGTH
        dict["HIGHT"] = Game.HIGHT
        dict["step"] = Game.step
        dict["scale"] = Game.scale
        dict["field"] = Game.field
        dict["water_amount"] = Game.water_amount
        dict["water_size"] = Game.water_size
        dict["tree_amount"] = Game.tree_amount
        dict["fertile_soil_amount"] = Game.fertile_soil_amount
        dict["Center_x"] = Game.center_x
        dict["Center_y"] = Game.center_y
        dict["surface"] = Game.surface
        dict["Log"] = Game.Log
        dict["Exit"] = Game.Exit
        dict["Screen"] = Game.Screen
        dict["Draw"] = Game.Draw
        dict["board"] = Game.board
        dict["player"] = Game.player
        return dict




