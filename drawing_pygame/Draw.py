import pygame

from const import *


def draw(surface, player=None, board=None, single_square=None, object=None, pos_x = None, pos_y = None):
    if board is not None and single_square is None:
        for i in range(max(0, board.game_pos_x // scale), min((board.game_pos_x + LENGTH) // scale + 1, field)):
            for j in range(max(0, board.game_pos_y // scale), min((board.game_pos_y + HIGHT) // scale + 1, field)):
                draw(surface, board=board, pos_x=i * scale, pos_y=j * scale, single_square=board.grid[i][j])
    if single_square is not None:
        if (board.game_pos_x - scale <= pos_x <= board.game_pos_x + (
                LENGTH) + scale and board.game_pos_y - scale <= pos_y <= board.game_pos_y + (
                HIGHT) + scale):
            square_skin = pygame.image.load(single_square.skin)
            square_skin = pygame.transform.scale(square_skin, (scale, scale))
            square_rect = square_skin.get_rect(
                topleft=(pos_x - board.game_pos_x, pos_y - board.game_pos_y), width=scale)
            surface.blit(square_skin, square_rect)
    if player is not None:
        player_skin = pygame.image.load(player.get_skin())
        player_skin = pygame.transform.scale(player_skin, (scale, scale))
        player_rect = player_skin.get_rect(
            topleft=(player.get_x() - board.game_pos_x, player.get_y() - board.game_pos_y),
            width=scale)
        surface.blit(player_skin, player_rect)
    if object is not None:
        pass
