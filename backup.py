from random import randint

from Game.Squares.Ground import Ground
from Game.Squares.Water import Water
from Game.single_square import SingleSquare
from Objects.Miners.Fertile_soil.Fertile_soil import Fertile_soil
from Objects.Miners.Trees.Tree import Tree
from Objects.buildings.furnace import Furnace
from const import *


class Board:
    __grid = None
    __game_pos_x = 0
    __game_pos_y = 0
    __cat_box = (300, 150)

    def __init__(self):
        self.__grid = [[None for i in range(field)] for j in range(field)]
        for i in range(field):
            for j in range(field):
                self.__grid[i][j] = SingleSquare(prototipe=Ground())

        for k in range(water_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            for i in range(water_size):
                for j in range(water_size):
                    self.__grid[x + i][y + j].set_skin(prototipe=Water())

        for k in range(tree_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            self.__grid[x][y].add_miner(Tree())

        for k in range(fertile_soil_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            self.__grid[x][y].add_miner(Fertile_soil())

        self.__grid[1][1].add_object(Furnace())

    def __repr__(self) -> str:
        for i in range(field):
            for j in range(field):
                print(self.__grid[i][j])
        return ""

    def increase_coordinates(self, x, y):
        self.update_cordinates(self.__game_pos_x + x, self.__game_pos_y + y)

    def update_cordinates(self, new_x, new_y):
        self.__game_pos_x = new_x
        self.__game_pos_y = new_y

    def get_grid(self) -> list[list[SingleSquare | None]] | None:
        return self.__grid

    def get_grid_size(self) -> int:
        return field

    def get_cat_box(self) -> tuple:
        return self.__cat_box

    def set_grid(self, new_grid):
        self.__grid = new_grid

    def set_cat_box(self, new_cat):
        self.__cat_box = new_cat

    def get_game_pos(self) -> tuple:
        return (self.__game_pos_x, self.__game_pos_y)

    def get_game_pos_x(self) -> int:
        return self.__game_pos_x

    def get_game_pos_y(self) -> int:
        return self.__game_pos_y

    def update(self):
        for i in range(field):
            for j in range(field):
                self.__grid[i][j].update()
from Game.single_square import SingleSquare


class Ground(SingleSquare):
    def __init__(self):
        super().__init__()
        self._skin = "sprites/mishaZemlya.png"
        self.is_player_available = True
from Game.single_square import SingleSquare


class Water(SingleSquare):
    def __init__(self):
        super().__init__()
        self._skin = "sprites/mishaVoda.png"
        self.is_player_available = False
import Objects.Something
from Objects.Miners.miners import Miners
from Objects.Resources.Resources import Resources

id = 0


class SingleSquare:
    __id = 0

    def __take_prototipe__(self, prototipe):
        self._skin = prototipe.get_skin()
        self.is_player_available = prototipe.is_player_available
        self._buildings = prototipe.get_buildings()
        self._miners = prototipe.get_miners()
        self._resources = prototipe.get_resources()

    def __init__(self, skin=None, prototipe=None):
        global id
        id += 1
        self.__id = id
        if prototipe == None:
            self._skin = skin
            self._buildings = []
            self._miners = []
            self._resources = []
        else:
            self.__take_prototipe__(prototipe)

    def __repr__(self) -> str:
        return f"Objects {self._buildings} in single square with id {self.__id} and skin {self.get_skin()}. Also has {self._miners} miners. Also has {self._resources}"

    def set_skin(self, skin=None, prototipe=None):
        self._skin = skin
        if prototipe is not None:
            self.__take_prototipe__(prototipe)

    def get_skin(self) -> str:
        return self._skin

    def add_object(self, object):
        print(f"Adding object to square with id {self.__id}")
        self._buildings.append(object)

    def get_buildings(self) -> list[Objects.Object.Something]:
        return self._buildings

    def get_miners(self) -> list[Miners]:
        return self._miners

    def copy(self):
        return SingleSquare(prototipe=self)

    def update(self):
        for object in self._buildings:
            object.update()

    def add_miner(self, miner):
        print(f"Adding miner to square with id {self.__id}")
        if self.is_player_available and len(self._miners) == 0:
            self._miners.append(miner)

    def mine(self) -> Resources:
        for i in range(len(self._miners)):
            resource = self._miners[i].get_resource()
            if resource is not None:
                return resource
            else:
                self._miners.pop(i)

    def get_resources(self) -> list[Resources]:
        return self._resources
from Objects.Miners.miners import Miners
from Objects.Resources.Soil.Soil import Soil


class Fertile_soil(Miners):

    def __init__(self):
        super().__init__(resource=Soil(), amount=10, skin="sprites/fertile_soil.png")
from Objects.Miners.miners import Miners
from Objects.Resources.Wood.Wood import Wood


class Tree(Miners):

    def __init__(self):
        super().__init__(resource=Wood(), amount=10, skin="sprites/tree.png")
from Objects.Something import Something
from Objects.Resources.Resources import Resources


class Miners(Something):
    _resource = None
    _amount = None
    _skin = None

    def __init__(self, resource=None, amount=None, skin=None):
        self._resource = resource if resource is not None else None
        self._amount = amount if amount is not None else 0
        self._skin = skin if skin is not None else None

    def __repr__(self) -> str:
        return f"_resource {self._resource} _amount {self._amount} _skin {self._skin}"

    def get_resource(self) -> Resources | None:
        if self._amount > 0:
            self._amount -= 1
            return self._resource.copy()
        else:
            return None

    def get_skin(self) -> str:
        return self._skin
from Objects.Something import Something


class Resources(Something):
    _skin = None
    _is_burnable = None

    def __from_prototipe(self, prototipe):
        self._skin = prototipe.get_skin()
        self._is_burnable = prototipe.get_is_burnable()

    def __init__(self, prototipe=None):
        if prototipe:
            self.__from_prototipe(prototipe)

    def get_skin(self) -> str:
        return self._skin

    def get_is_burnable(self) -> bool:
        return self._is_burnable

    def copy(self):
        return Resources(prototipe=self)
from Objects.Resources.Resources import Resources


class Soil(Resources):
    def __init__(self):
        super().__init__()
        self._is_burnable = False
        self._skin = "sprites/soil.jpg"
from Objects.Resources.Resources import Resources


class Wood(Resources):
    def __init__(self):
        super().__init__()
        self._is_burnable = True
        self._skin = "sprites/wood.jpg"
class Something:
    _skin = None
    _type = None

    def __get_prototipe(self, prototipe):
        self._skin = prototipe.get_skin()
        self._type = prototipe.get_type()

    def __init__(self, skin="sprites/furnace.png", type=None, prototype=None):
        self._skin = skin
        self._type = type

        if prototype is not None:
            self.__get_prototipe(prototipe=prototype)

    def get_skin(self) -> str:
        return self._skin

    def get_type(self) -> str:
        return self._type
import time

from Objects.Object import Object


class Furnace(Object):


    def __init__(self):
        print("Initializing Furnace")
        super().__init__()
        self._skin = "sprites/furnace.png"
        self._type = "buildings"
        self.input = {
            "cuprum ore": 1000
        }
        self.output = {
        }
        self.fuel = {
            "name": "coal",
            "amount": 100,
            "burning_time": 1
        }
        self.__input_resources = {
            "cuprum ore": 1
        }
        self.__output_resources = {
            "cuprum": 1
        }
        self.__alowded_fuel = ["coal"]
        self.__is_active = False
        self.__start_of_active = time.time()

    def __repr__(self):
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"

    def change_active(self):
        self.__is_active = not self.__is_active
        self.change_skin()

    def change_skin(self):
        if self.__is_active:
            self._skin = "sprites/burning_furnace.png"
        else:
            self._skin = "sprites/furnace.png"

    def update(self):
        if self.__is_active:
            if self.fuel["burning_time"] < time.time() - self.__start_of_active:
                print(self)
                print(f"burning time: {time.time()}")
                self.__start_of_active = time.time()
                if self.fuel["amount"]:
                    self.fuel["amount"] -= 1
                    for resource, amount in self.__input_resources.copy().items():
                        if self.input[resource] < amount:
                            self.__is_active = False
                            self.change_skin()
                            break
                    if self.__is_active:
                        for resource, amount in self.__input_resources.items():
                            self.input[resource] -= amount
                        for resource, amount in self.__output_resources.items():
                            if resource not in self.output.keys():
                                self.output[resource] = 0
                            self.output[resource] += amount
                else:
                    self.__is_active = False
                    self.change_skin()
import time

from Objects.Something import Something


class Furnace(Something):
    _skin = "sprites/furnace.png"
    _type = "buildings"
    input = {
        "cuprum ore": 1000
    }
    output = {
    }
    fuel = {
        "name": "coal",
        "amount": 100,
        "burning_time": 1
    }
    __input_resources = {
        "cuprum ore": 1
    }
    __output_resources = {
        "cuprum": 1
    }
    __alowded_fuel = ["coal"]
    __is_active = False
    __start_of_active = time.time()

    def __init__(self):
        print("Initializing Furnace")
        super().__init__()
        self.__input_resources["cuprum ore"] = 1
        self.__output_resources["cuprum"] = 1
        self._type = "buildings"

    def __repr__(self) -> str:
        return f"Furnace with {self.input} and {self.output} and {self.fuel}"

    def change_active(self):
        self.__is_active = not self.__is_active
        self.change_skin()

    def change_skin(self):
        if self.__is_active:
            self._skin = "sprites/burning_furnace.png"
        else:
            self._skin = "sprites/furnace.png"

    def update(self):
        if self.__is_active:
            if self.fuel["burning_time"] < time.time() - self.__start_of_active:
                print(self)
                print(f"burning time: {time.time()}")
                self.__start_of_active = time.time()
                if self.fuel["amount"]:
                    self.fuel["amount"] -= 1
                    for resource, amount in self.__input_resources.copy().items():
                        if self.input[resource] < amount:
                            self.__is_active = False
                            self.change_skin()
                            break
                    if self.__is_active:
                        for resource, amount in self.__input_resources.items():
                            self.input[resource] -= amount
                        for resource, amount in self.__output_resources.items():
                            if resource not in self.output.keys():
                                self.output[resource] = 0
                            self.output[resource] += amount
                else:
                    self.__is_active = False
                    self.change_skin()
from Objects.Something import Something
from Objects.buildings.furnace import Furnace
from const import *


class inventory():

    def __init__(self, size_x=5, size_y=10):
        self._grid = [[None for i in range(size_y)] for j in range(size_x)]
        self._size_x = size_x
        self._size_y = size_y
        self._cursor = [0, 0]
        self._selected_item = None
        self._is_selected = False
        self._scale = scale / 2
        self._grid[0][0] = Furnace()

    def __repr__(self) -> str:
        return f"Inventory {self._grid}"

    def get_selected_item(self) -> Something:
        return self._selected_item

    def get_cursor(self) -> list[int]:
        return self._cursor

    def get_sizes(self) -> tuple:
        return (self._size_x, self._size_y)

    def add_item(self, item, pos=None):
        if pos is None:
            for i in range(self._size_x):
                for j in range(self._size_y):
                    if self._grid[i][j] is None:
                        pos = (i, j)
        self._grid[pos[0]][pos[1]] = item

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

    def take_item(self) -> Something | None:
        item = self._grid[self._selected_item[0]][self._selected_item[1]]
        self._grid[self._selected_item[0]][self._selected_item[1]] = None
        return item

    def get_grid(self) -> list[list[Something | None]]:
        return self._grid

    def is_selected(self) -> bool:
        return self._is_selected
import pygame

from Player.Inventory import inventory
from const import *


class Player:
    statuses = {
        'paused': 1,
        'walking': 2,
        'inventory': 3,
        'crafting': 4
    }

    def __init__(self, name="Mihaham", position_x=0, position_y=0, skin="sprites/bottom.png", settings=None):
        self.__name = name
        self.__inventory = inventory()
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

    def move(self, event, board=None):
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
                    if board.get_grid()[self.__x // scale][self.__y // scale].get_buildings() != []:
                        board.get_grid()[self.__x // scale][self.__y // scale].get_buildings()[0].change_active()
                    if board.get_grid()[self.__x // scale][self.__y // scale].get_miners() != []:
                        board.get_grid()[self.__x // scale][self.__y // scale].mine()
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

    def update(self, board):
        new_x = (self.__direction[0] * step + self.__x)
        new_y = (self.__direction[1] * step + self.__y)
        if 0 <= new_x <= (field) * scale and 0 <= new_y <= (field) * scale:
            if (board.get_grid()[min(new_x // scale, field - 1)][min(new_y // scale, field - 1)].is_player_available):
                if not (Center_x - board.get_cat_box()[0] <= new_x - board.get_game_pos_x() <= Center_x +
                        board.get_cat_box()[
                            0] and Center_y - board.get_cat_box()[1] <= new_y - board.get_game_pos_y() <= Center_y +
                        board.get_cat_box()[
                            1]):
                    board.increase_coordinates(self.__direction[0] * step, self.__direction[1] * step)
                self.update_position((self.__direction[0] * step + self.__x, self.__direction[1] * step + self.__y))
import pygame

LENGTH = 1500
HIGHT = 1000

def update_screen_size(x,y):
    global LENGTH, HIGHT
    LENGTH = x
    HIGHT = y
    print(LENGTH, HIGHT)

pygame.init()
info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
screen_width, screen_height = info.current_w, info.current_h
update_screen_size(screen_width, screen_height)

step = 12
scale = 72
field = 20

water_amount = 1
water_size = 4

tree_amount = 1

fertile_soil_amount = 10

Center_x = LENGTH // 2
Center_y = HIGHT // 2
from glob import glob

from Player.player import Player
from const import *


class Drawing():
    def __init__(self):
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.sprites = {}

        for filename in glob('sprites/**/*.png', recursive=True):
            my_filename = filename.replace("\\", "/")
            self.sprites[my_filename] = pygame.image.load(filename).convert_alpha()
        print(self.sprites)

    def draw(self, surface, player=None, board=None, this_single_square=None, object=None, inventory=None, pos_x=None,
             pos_y=None, draw_scale=1):
        if board is not None:
            self.draw_board(surface=surface, board=board)
        if this_single_square is not None:
            self.draw_single_square(single_square=this_single_square)
        if object is not None:
            self.draw_object()
        if inventory is not None:
            self.draw_inventory()

        if player is not None:
            self.draw_player(surface=surface, player=player, board=board)

    def draw_player(self, surface: pygame, player, board, draw_scale=1):
        text_skin = self.my_font.render(player.get_name(), False, (255, 0, 0))
        text_rect = text_skin.get_rect(
            center=(player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y() - scale // 2),
            width=scale)
        surface.blit(text_skin, text_rect)
        player_skin = self.sprites[player.get_skin()]
        player_skin = pygame.transform.scale(player_skin, (2 * draw_scale * scale, 2 * draw_scale * scale))
        player_rect = player_skin.get_rect(
            center=(player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y()),
            width=scale)
        surface.blit(player_skin, player_rect)
        if player.get_status() == Player.statuses["inventory"]:
            self.draw_inventory(surface, inventory=player.get_inventory())

    def draw_object(self, surface: pygame, object, board, pos_x, pos_y, draw_scale=1):
        object_skin = self.sprites[object.get_skin()]
        object_skin = pygame.transform.scale(object_skin, (draw_scale * scale, draw_scale * scale))
        object_rect = object_skin.get_rect(
            topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()), width=scale)
        surface.blit(object_skin, object_rect)

    def draw_inventory(self, surface: pygame, inventory, ):
        pygame.draw.rect(surface, (0, 0, 0), (LENGTH * 3 / 4, 0, LENGTH, HIGHT))
        text_skin = self.my_font.render("Inventory", False, (255, 255, 255))
        text_rect = text_skin.get_rect(
            midleft=(LENGTH * 3 / 4 + 20, 30),
            width=scale)
        surface.blit(text_skin, text_rect)

        small_scale = (LENGTH / 4) / (inventory.get_sizes()[0] + 3)
        for i in range(inventory.get_sizes()[0]):
            for j in range(inventory.get_sizes()[1]):
                pygame.draw.rect(surface, (255, 0, 0), (
                    20 + LENGTH * 3 / 4 + i * (small_scale + 10), 60 + (small_scale + 10) * j, small_scale,
                    small_scale), 5)
                if inventory.get_grid()[i][j] != None:
                    skin = inventory.get_grid()[i][j].get_skin()
                    object_skin = self.sprites[skin]
                    object_skin = pygame.transform.scale(object_skin, (small_scale - 10, small_scale - 10))
                    object_rect = object_skin.get_rect(
                        topleft=(20 + LENGTH * 3 / 4 + i * (small_scale + 10) + 5, 60 + (small_scale + 10) * j + 5),
                        width=scale)
                    surface.blit(object_skin, object_rect)

        selected = inventory.is_selected()
        if selected:
            x, y = inventory.get_selected_item()
            pygame.draw.rect(surface, (0, 0, 255), (
                20 + LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y, small_scale,
                small_scale), 5)
        x, y = inventory.get_cursor()
        pygame.draw.rect(surface, (0, 255, 0), (
            20 + LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y, small_scale, small_scale), 5)

    def draw_single_square(self, surface: pygame, single_square, board, pos_x, pos_y, draw_scale = 1):
        if (board.get_game_pos_x() - scale <= pos_x <= board.get_game_pos_x() + (
                LENGTH) + scale and board.get_game_pos_y() - scale <= pos_y <= board.get_game_pos_y() + (
                HIGHT) + scale):
            square_skin = self.sprites[single_square.get_skin()]
            square_skin = pygame.transform.scale(square_skin, (draw_scale * scale, draw_scale * scale))
            square_rect = square_skin.get_rect(
                topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()), width=scale)
            surface.blit(square_skin, square_rect)
            # print(f"Single Square {this_single_square}")
            for object in single_square.get_buildings():
                self.draw_object(surface, object=object, pos_x=pos_x,
                                 pos_y=pos_y, board=board)
            for object in single_square.get_miners():
                self.draw_object(surface, board=board, object=object, pos_x=pos_x,
                                 pos_y=pos_y)

    def draw_board(self, surface: pygame, board):
        pygame.draw.rect(surface, (0, 0, 255), (0, 0, LENGTH, HIGHT))
        for i in range(max(0, board.get_game_pos_x() // scale),
                       min((board.get_game_pos_x() + LENGTH) // scale + 1, field)):
            for j in range(max(0, board.get_game_pos_y() // scale),
                           min((board.get_game_pos_y() + HIGHT) // scale + 1, field)):
                self.draw_single_square(surface, board=board, pos_x=i * scale, pos_y=j * scale,
                                        single_square=board.get_grid()[i][j])
import logging
import datetime
import os


class Logger():


    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.date = datetime.datetime.now().strftime('%Y%m%d-%H')
        os.mkdir(f"{self.date}")
        self.info = f"{self.date}/info.log"
        self.warnings = f"{self.date}/warnings.log"
        self.errors = f"{self.date}/errors.log"
        self.debug = f"{self.date}/debug.log"

    def add_str_to_file(self, str_to_write, file_name):
        with open(f"{file_name}", "a") as file:
            file.write(str_to_write + "\n")

    def add_info(self, text):
        logging.INFO(text)
        self.add_str_to_file(text,self.info)

    def add_warnings(self, text):
        logging.WARNING(text)
        self.add_str_to_file(text,self.warnings)

    def add_errors(self, text):
        logging.ERROR(text)
        self.add_str_to_file(text,self.errors)

    def add_debug(self, text):
        logging.DEBUG(text)
        self.add_str_to_file(text,self.debug)


import pygame
from logger.Logger import Logger

from Game.Board import Board
from Player.player import Player
from const import *
from drawing_pygame.Draw import Drawing


def main():
    fps = 60
    pygame.init()
    info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
    screen_width, screen_height = info.current_w, info.current_h
    update_screen_size(screen_width, screen_height)
    print(LENGTH, HIGHT)
    pygame.font.init()
    surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Really russian game")

    Log = Logger()

    Draw = Drawing()
    Log.add_info("Drawing is initialized")
    board = Board()
    Log.add_info("Board is initialized")
    player = Player(position_x=Center_x, position_y=Center_y)
    Log.add_info("Player is initialized")

    while True:
        Draw.draw(surface, player=player, board=board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Log.add_info("Game is over")
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.move(event, board=board)

        player.update(board)
        board.update()

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
