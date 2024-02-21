import pygame

from drawing_pygame.Draw import draw
from Game.Board import Board
from Player.player import Player
from const import *

fps = 60

pygame.init()
surface = pygame.display.set_mode([LENGTH, HIGHT])
clock = pygame.time.Clock()
pygame.display.set_caption("Really russian game")

Board = Board()
player = Player(position_x=Center_x, position_y=Center_y)

while True:
    draw(surface, player = player, board = Board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.move(event)

    player.update(Board)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
