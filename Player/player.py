import pygame

from Player.Inventory import inventory
from const import *


class Player:
    name = "UserName"
    inventory = None
    x = 0
    y = 0
    direction = [0,0]
    skin = "sprites/player1.png"


    def __init__(self, name="Mihaham", position_x=0, position_y=0, skin="sprites/player1.png"):
        self.name = name
        self.inventory = inventory()
        self.x = position_x
        self.y = position_y
        self.skin = skin

    def __repr__(self):
        return f"Player {self.name}"

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction[1] = -1
            if event.key == pygame.K_a:
                self.direction[0] = -1
            if event.key == pygame.K_s:
                self.direction[1] = 1
            if event.key == pygame.K_d:
                self.direction[0] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.direction[1] = 0
            if event.key == pygame.K_a:
                self.direction[0] = 0
            if event.key == pygame.K_s:
                self.direction[1] = 0
            if event.key == pygame.K_d:
                self.direction[0] = 0

    def draw(self, surface, board_x, board_y):
        player_skin = pygame.image.load(self.skin)
        player_skin = pygame.transform.scale(player_skin, (scale, scale))
        player_rect = player_skin.get_rect(topleft=(self.x - board_x, self.y - board_y), width=scale)
        surface.blit(player_skin, player_rect)

    def get_position(self):
        return self.x, self.y

    def update_position(self, position):
        self.x, self.y = position

    def update(self, board):
        new_x = (self.direction[0] * step + self.x)
        new_y = (self.direction[1] * step + self.y)
        if 0<=new_x<=(field-1)*scale and 0<=new_y<=(field-1)*scale:
            if (board.grid[new_x // scale][new_y // scale].is_player_available and board.grid[new_x // scale + 1][
                new_y // scale].is_player_available and board.grid[new_x // scale][
                new_y // scale + 1].is_player_available and board.grid[new_x // scale + 1][
                new_y // scale + 1].is_player_available):
                if not(Center_x - board.cat_box[0]<=new_x - board.game_pos_x<=Center_x+board.cat_box[0] and Center_y - board.cat_box[1]<=new_y - board.game_pos_y<=Center_y+board.cat_box[1]):
                    board.increase_coordinates(self.direction[0] * step,self.direction[1]*step)
                self.update_position((self.direction[0] * step + self.x, self.direction[1] * step + self.y))

