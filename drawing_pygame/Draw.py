import pygame

from const import *


def draw(surface, player=None, board=None, this_single_square=None, object=None, pos_x = None, pos_y = None):
    if board is not None and this_single_square is None:
        pygame.draw.rect(surface, (0, 0, 255), (0, 0, LENGTH, HIGHT))
        for i in range(max(0, board.get_game_pos_x() // scale), min((board.get_game_pos_x() + LENGTH) // scale + 1, field)):
            for j in range(max(0, board.get_game_pos_y() // scale), min((board.get_game_pos_y() + HIGHT) // scale + 1, field)):
                draw(surface, board=board, pos_x=i * scale, pos_y=j * scale, this_single_square=board.get_grid()[i][j])
    if this_single_square is not None and object is None:
        if (board.get_game_pos_x() - scale <= pos_x <= board.get_game_pos_x() + (
                LENGTH) + scale and board.get_game_pos_y() - scale <= pos_y <= board.get_game_pos_y() + (
                HIGHT) + scale):
            square_skin = pygame.image.load(this_single_square.get_skin())
            square_skin = pygame.transform.scale(square_skin, (scale, scale))
            square_rect = square_skin.get_rect(
                topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()), width=scale)
            surface.blit(square_skin, square_rect)
            #print(f"Single Square {this_single_square}")
            for object in this_single_square.get_objects():
                draw(surface, board=board, this_single_square=this_single_square, object=object, pos_x=pos_x, pos_y=pos_y)
    if object is not None:
        object_skin = pygame.image.load(object.get_skin())
        object_skin = pygame.transform.scale(object_skin, (scale, scale))
        object_rect = object_skin.get_rect(
            topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()), width=scale)
        surface.blit(object_skin, object_rect)
    if player is not None:
        player_skin = pygame.image.load(player.get_skin())
        player_skin = pygame.transform.scale(player_skin, (scale, scale))
        player_rect = player_skin.get_rect(
            topleft=(player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y()),
            width=scale)
        surface.blit(player_skin, player_rect)
