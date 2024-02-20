import pygame

from const import *

from Player.player import Player
from Game.Board import Board

fps = 60

pygame.init()
surface = pygame.display.set_mode([LENGTH, HIGHT])
clock = pygame.time.Clock()
pygame.display.set_caption("Really russian game")

player = Player()
Board = Board()

while True:
    Board.draw(surface)
    player.draw(surface)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.move(event)

    player.update(Board)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
