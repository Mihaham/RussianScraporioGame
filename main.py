import pygame

from const import *

from Player.player import Player
from Game.Board import Board

fps = 60

pygame.init()
surface = pygame.display.set_mode([LENGTH, HIGHT])
clock = pygame.time.Clock()
pygame.display.set_caption("Really russian game")

Board = Board()
player = Player(position_x=Center_x, position_y=Center_y)

while True:
    pygame.draw.rect(surface, (0,0,255), (0, 0, LENGTH, HIGHT))
    Board.draw(surface)
    player.draw(surface, board_x=Board.game_pos_x, board_y=Board.game_pos_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.move(event)

    player.update(Board)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
