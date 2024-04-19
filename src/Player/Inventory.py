from src.Objects.GameObject import GameObject
from src.Objects.Resources.Soil.Soil import Soil
from src.Objects.Resources.Wood.Wood import Wood
from src.Objects.buildings.furnace.furnace import Furnace
from src.Objects.buildings.Steel_furnace.steel_furnace import Steel_furnace
from src.Objects.buildings.Worker_lvl1.worker_lvl1 import Worker_lvl1
from src.Objects.buildings.Worker_lvl2.worker_lvl2 import Worker_lvl2
from src.Objects.buildings.Worker_lvl3.worker_lvl3 import Worker_lvl3

from src.logger.Logger import GlobalObject
from src.CONST import GameConstants


class Inventory(GlobalObject):

    def __init__(self, size_x=GameConstants.inventory_size_x, size_y=GameConstants.inventory_size_y, scale=None):
        super().__init__()
        self._grid = [[None for i in range(size_y)] for j in range(size_x)]
        self._amount = [[0 for i in range(size_y)] for j in range(size_x)]
        self._size_x = size_x
        self._size_y = size_y
        self._cursor = [0, 0]
        self._selected_item = None
        self._is_selected = False
        self._scale = scale / 2


        #Adding objects for test
        self.add_item(Furnace, 10)
        self.add_item(Wood, 100)
        self.add_item(Soil, 100)
        self.add_item(Steel_furnace,10)
        self.add_item(Worker_lvl1,10)
        self.add_item(Worker_lvl2,10)
        self.add_item(Worker_lvl3,10)

    def __repr__(self) -> str:
        return f"Inventory {self._grid}"

    def get_selected_item(self) -> GameObject:
        if self._is_selected:
            if self._grid[self._selected_item[0]][self._selected_item[1]] is not None:
                item = self._grid[self._selected_item[0]][self._selected_item[1]]
            else:
                item = None
            if self._amount[self._selected_item[0]][self._selected_item[1]] > 0:
                self._amount[self._selected_item[0]][self._selected_item[1]] -= 1
                if self._amount[self._selected_item[0]][self._selected_item[1]] == 0:
                    self._grid[self._selected_item[0]][self._selected_item[1]] = None
                    self._is_selected = False
            return item() if item is not None else None

    def get_selected_item_class(self):
        return self._grid[self._selected_item[0]][self._selected_item[1]]

    def get_selected_position(self) -> list[int]:
        return self._selected_item

    def get_cursor(self) -> list[int]:
        return self._cursor

    def get_sizes(self) -> tuple:
        return (self._size_x, self._size_y)

    def add_item(self, item, amount=1, pos=None):
        try:
            if item is not None:
                if pos is None:
                    for j in range(self._size_y):
                        for i in range(self._size_x):
                            if self._grid[i][j] != None and item == self._grid[i][j]:
                                pos = (i, j)
                                raise StopIteration
                            if self._grid[i][j] == None:
                                pos = (i, j)
                                self._grid[i][j] = item
                                raise StopIteration
        except StopIteration:
            self._amount[pos[0]][pos[1]] += amount

    def get_item(self, item, amount=1, pos=None):
        try:
            if item is not None:
                if pos is None:
                    for j in range(self._size_y):
                        for i in range(self._size_x):
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
                return {item: can_return}
            self._amount[pos[0]][pos[1]] -= amount

            if self._amount[pos[0]][pos[1]] == 0:
                self._grid[pos[0]][pos[1]] = None
            return {item: amount}

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
