from src.Objects.GameObject import GameObject
from src.Objects.buildings.furnace.furnace import Furnace
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
        self._grid[0][0] = Furnace

    def __repr__(self) -> str:
        return f"Inventory {self._grid}"

    def get_selected_item(self) -> GameObject:
        return self._selected_item

    def get_cursor(self) -> list[int]:
        return self._cursor

    def get_sizes(self) -> tuple:
        return (self._size_x, self._size_y)

    def add_item(self, item, pos=None):
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
            self._amount[pos[0]][pos[1]] += 1

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
