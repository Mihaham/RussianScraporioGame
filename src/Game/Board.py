from random import randint

from src.Game.Squares.Ground import Ground
from src.Game.Squares.Water import Water
from src.Game.single_square import SingleSquare
from src.Objects.Miners.Fertile_soil.Fertile_soil import Fertile_soil
from src.Objects.Miners.Trees.Tree import Tree
from src.Objects.buildings.furnace.furnace import Furnace


class Board:

    def __init__(self, field=400, water_amount=10, water_size=5, tree_amount=10,
                 fertile_soil_amount=10):
        self.__grid = [[None for i in range(field)] for j in range(field)]
        self.__game_pos_x = 0
        self.__game_pos_y = 0
        self.__cat_box = (300, 150)
        self.field = field
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
        for i in range(self.field):
            for j in range(self.field):
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
        return self.field

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
        for i in range(self.field):
            for j in range(self.field):
                self.__grid[i][j].update()
