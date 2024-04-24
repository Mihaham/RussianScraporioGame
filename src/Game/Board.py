from random import randint
from typing import Optional

from src.Game.Squares.Ground import Ground
from src.Game.Squares.Water import Water
from src.Game.single_square import SingleSquare
from src.Objects.Miners.Fertile_soil.Fertile_soil import Fertile_soil
from src.Objects.Miners.Trees.Tree import Tree
from src.Objects.buildings.furnace.furnace import Furnace
from src.logger.Logger import Logger, GlobalObject
from src.CONST import GameConstants

class Board(GlobalObject):
    id = 0

    def __init__(self, field: int = GameConstants.field, water_amount: int = GameConstants.water_amount, water_size: int = GameConstants.water_size,
                 tree_amount: int = GameConstants.tree_amount,
                 fertile_soil_amount: int = GameConstants.fertile_soil_amount):
        super().__init__()
        Board.id += 1
        self.__id = Board.id
        self.__grid: list[list[Optional[SingleSquare]]] = [[None for i in range(field)] for j in
                                                           range(field)]
        self.__game_pos_x: int = 0
        self.__game_pos_y: int = 0
        self.__cat_box: tuple[int, int] = GameConstants.game_cat_box
        self.field: int = field
        for i in range(field):
            for j in range(field):
                self.__grid[i][j] = Ground()

        for k in range(water_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            for i in range(water_size):
                for j in range(water_size):
                    self.__grid[x + i][y + j] = Water()

        for k in range(tree_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            self.__grid[x][y].add_miner(Tree())

        for k in range(fertile_soil_amount):
            x = randint(0, field - water_size)
            y = randint(0, field - water_size)

            self.__grid[x][y].add_miner(Fertile_soil())


        #Adding Building for tests
        self.__grid[1][1].add_building(Furnace())
        Logger.add_info(f"Board is initialized with id {self.__id}")

    def __repr__(self) -> str:
        for i in range(self.field):
            for j in range(self.field):
                print(self.__grid[i][j])
        return ""

    def increase_coordinates(self, x: int, y: int) -> None:
        self.update_cordinates(self.__game_pos_x + x, self.__game_pos_y + y)

    def update_cordinates(self, new_x: int, new_y: int) -> None:
        self.__game_pos_x: int = new_x
        self.__game_pos_y: int = new_y

    def get_grid(self) -> Optional[list[list[Optional[SingleSquare]]]]:
        return self.__grid

    def get_grid_size(self) -> int:
        return self.field

    def get_cat_box(self) -> tuple:
        return self.__cat_box

    def set_grid(self, new_grid: list[list[Optional[SingleSquare]]]):
        self.__grid = new_grid

    def set_cat_box(self, new_cat: tuple[int, int]):
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
