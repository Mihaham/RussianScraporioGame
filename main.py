import pygame

from Game.Board import Board
from Player.player import Player
from const import *
from drawing_pygame.Draw import Drawing


def main():
    fps = 60
    pygame.init()
    info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
    screen_width, screen_height = info.current_w, info.current_h
    update_screen_size(screen_width, screen_height)
    print(LENGTH, HIGHT)
    pygame.font.init()
    surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Really russian game")

    Draw = Drawing()
    board = Board()
    player = Player(position_x=Center_x, position_y=Center_y)

    while True:
        Draw.draw(surface, player=player, board=board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.move(event, board=board)

        player.update(board)
        board.update()

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
