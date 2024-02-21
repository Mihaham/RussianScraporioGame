import pygame

from Player.Inventory import inventory
from const import *


class Player:
    __name = "UserName"
    __inventory = None
    __x = 0
    __y = 0
    __direction = [0, 0]
    __skin = "sprites/player1.png"

    __settings = {
        "up": pygame.K_w,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "down": pygame.K_s,
        "set_object": pygame.K_KP_ENTER
    }

    def __init__(self, name="Mihaham", position_x=0, position_y=0, skin="sprites/player1.png"):
        self.__name = name
        self.__inventory = inventory()
        self.__x = position_x
        self.__y = position_y
        self.__skin = skin

    def __repr__(self):
        return f"Player {self.__name}"

    def move(self, event):
        print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == self.__settings["up"]:
                self.__direction[1] = -1
            if event.key == self.__settings["left"]:
                self.__direction[0] = -1
            if event.key == self.__settings["down"]:
                self.__direction[1] = 1
            if event.key == self.__settings["right"]:
                self.__direction[0] = 1
            if event.key == self.__settings["set_object"]:
                print("enter")
        if event.type == pygame.KEYUP:
            if event.key == self.__settings["up"]:
                self.__direction[1] = 0
            if event.key == self.__settings["left"]:
                self.__direction[0] = 0
            if event.key == self.__settings["down"]:
                self.__direction[1] = 0
            if event.key == self.__settings["right"]:
                self.__direction[0] = 0

    def rename(self, new_name):
        self.__name = new_name

    def get_skin(self):
        return self.__skin

    def get_direction(self):
        return self.__direction

    def get_position(self):
        return self.__x, self.__y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_direction(self, new_direction):
        self.__direction = new_direction

    def update_position(self, position):
        self.__x, self.__y = position

    def update(self, board):
        new_x = (self.__direction[0] * step + self.__x)
        new_y = (self.__direction[1] * step + self.__y)
        if 0 <= new_x <= (field - 1) * scale and 0 <= new_y <= (field - 1) * scale:
            if (board.get_grid()[new_x // scale][new_y // scale].is_player_available and board.get_grid()[new_x // scale + 1][
                new_y // scale].is_player_available and board.get_grid()[new_x // scale][
                new_y // scale + 1].is_player_available and board.get_grid()[new_x // scale + 1][
                new_y // scale + 1].is_player_available):
                if not (Center_x - board.get_cat_box()[0] <= new_x - board.get_game_pos_x()  <= Center_x + board.get_cat_box()[
                    0] and Center_y - board.get_cat_box()[1] <= new_y - board.get_game_pos_y()  <= Center_y + board.get_cat_box()[
                            1]):
                    board.increase_coordinates(self.__direction[0] * step, self.__direction[1] * step)
                self.update_position((self.__direction[0] * step + self.__x, self.__direction[1] * step + self.__y))
