import pygame

from drawing_pygame.Draw import draw
from Game.Board import Board
from Player.player import Player
from const import *

def main():
    fps = 60
    pygame.init()
    surface = pygame.display.set_mode([LENGTH, HIGHT])
    clock = pygame.time.Clock()
    pygame.display.set_caption("Really russian game")

    board = Board()
    player = Player(position_x=Center_x, position_y=Center_y)
    print(board)

    while True:
        draw(surface, player = player, board = board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.move(event, board = board)

        player.update(board)
        board.update()

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    main()
