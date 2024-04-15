import pygame

from src.Player.Inventory import inventory
from src.logger.Logger import GlobalObject
from src.CONST import GameConstants


class Player(GlobalObject):
    statuses = {
        'paused': 1,
        'walking': 2,
        'inventory': 3,
        'crafting': 4
    }

    def __init__(self, name="Mihaham", position_x=0, position_y=0, skin="sprites/bottom.png",
                 settings=None, scale=GameConstants.scale):
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

    def move(self, event, board=None, scale=GameConstants.scale):
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
                    if board.get_grid()[min(self.__x // scale, len(board.get_grid()) - 1)][
                        min(self.__y // scale, len(board.get_grid()[0]) - 1)].get_buildings() != []:
                        board.get_grid()[min(self.__x // scale, len(board.get_grid()) - 1)][
                            min(self.__y // scale, len(board.get_grid()[0]) - 1)].get_buildings()[
                            0].change_menu(player=self)
                    if board.get_grid()[min(self.__x // scale, len(board.get_grid()) - 1)][
                        min(self.__y // scale, len(board.get_grid()[0]) - 1)].get_miners() != []:
                        item = board.get_grid()[min(self.__x // scale, len(board.get_grid()) - 1)][
                            min(self.__y // scale, len(board.get_grid()[0]) - 1)].mine()
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.__inventory.is_selected:
                    mouse_position = pygame.mouse.get_pos()
                    mouse_position = [mouse_position[0] + board.get_game_pos_x(),
                                      mouse_position[1] + board.get_game_pos_y()]
                    board.get_grid()[min(mouse_position[0] // scale, len(board.get_grid()) - 1)][
                        min(mouse_position[1] // scale, len(board.get_grid()[0]) - 1)].add_item(
                        self.__inventory.get_selected_item())

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

    def add_item(self, object, amount=1):
        self.__inventory.add_item(object, amount)

    def get_item(self, object, amount=1):
        return self.__inventory.get_item(object, amount)
