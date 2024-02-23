from Objects.buildings.furnace import Furnace


class inventory():

    def __init__(self, size = 5):
        self._grid = [[None for i in range(size)] for j in range(size)]
        self._size = size
        self._cursor = [0,0]
        self._selected_item = None
        self._is_selected = False


        self._grid[0][0] = Furnace()


    def __repr__(self):
        return f"Inventory {self._grid}"

    def add_item(self, item, pos = None):
        if pos is None:
            for i in range(self._size):
                for j in range(self._size):
                    if self._grid[i][j] is None:
                        pos = (i,j)
        self._grid[pos[0]][pos[1]] = item

    def move_right(self):
        self._cursor[1] += 1
        self._cursor[1] %= self._size

    def move_left(self):
        self._cursor[1] -= 1
        self._cursor[1] %= self._size

    def move_up(self):
        self._cursor[0] -= 1
        self._cursor[0] %= self._size

    def move_down(self):
        self._cursor[0] += 1
        self._cursor[0] %= self._size


    def select(self):
        self._selected_item = self._cursor.copy() if self._is_selected else None
        self._is_selected = not self._is_selected

    def take_item(self):
        item = self._grid[self._selected_item[0]][self._selected_item[1]]
        self._grid[self._selected_item[0]][self._selected_item[1]] = None
        return item



