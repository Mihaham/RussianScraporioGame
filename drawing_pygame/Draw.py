from glob import glob

import pygame

from Player.player import Player
from const import *


def load_sprites():
    global sprites
    global my_font
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    sprites = {}

    for filename in glob('sprites/**/*.png', recursive=True):
        my_filename = filename.replace("\\", "/")
        sprites[my_filename] = pygame.image.load(filename).convert_alpha()
    print(sprites)


def draw(surface, player=None, board=None, this_single_square=None, object=None, inventory=None, pos_x=None, pos_y=None,
         draw_scale=1):
    global sprites
    global my_font
    if board is not None and this_single_square is None:
        pygame.draw.rect(surface, (0, 0, 255), (0, 0, LENGTH, HIGHT))
        for i in range(max(0, board.get_game_pos_x() // scale),
                       min((board.get_game_pos_x() + LENGTH) // scale + 1, field)):
            for j in range(max(0, board.get_game_pos_y() // scale),
                           min((board.get_game_pos_y() + HIGHT) // scale + 1, field)):
                draw(surface, board=board, pos_x=i * scale, pos_y=j * scale, this_single_square=board.get_grid()[i][j])
    if this_single_square is not None and object is None:
        if (board.get_game_pos_x() - scale <= pos_x <= board.get_game_pos_x() + (
                LENGTH) + scale and board.get_game_pos_y() - scale <= pos_y <= board.get_game_pos_y() + (
                HIGHT) + scale):
            square_skin = sprites[this_single_square.get_skin()]
            square_skin = pygame.transform.scale(square_skin, (draw_scale * scale, draw_scale * scale))
            square_rect = square_skin.get_rect(
                topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()), width=scale)
            surface.blit(square_skin, square_rect)
            # print(f"Single Square {this_single_square}")
            for object in this_single_square.get_buildings():
                draw(surface, board=board, this_single_square=this_single_square, object=object, pos_x=pos_x,
                     pos_y=pos_y)
            for object in this_single_square.get_miners():
                draw(surface, board=board, this_single_square=this_single_square, object=object, pos_x=pos_x,
                     pos_y=pos_y)
    if object is not None:
        object_skin = sprites[object.get_skin()]
        object_skin = pygame.transform.scale(object_skin, (draw_scale * scale, draw_scale * scale))
        object_rect = object_skin.get_rect(
            topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()), width=scale)
        surface.blit(object_skin, object_rect)
    if inventory is not None:
        pygame.draw.rect(surface, (0, 0, 0), (LENGTH * 3 / 4, 0, LENGTH, HIGHT))
        text_skin = my_font.render("Inventory", False, (255, 255, 255))
        text_rect = text_skin.get_rect(
            midleft=(LENGTH * 3 / 4 + 20, 30),
            width=scale)
        surface.blit(text_skin, text_rect)

        small_scale = (LENGTH / 4) / (inventory.get_sizes()[0] + 3)
        for i in range(inventory.get_sizes()[0]):
            for j in range(inventory.get_sizes()[1]):
                pygame.draw.rect(surface, (255, 0, 0), (
                20 + LENGTH * 3 / 4 + i * (small_scale + 10), 60 + (small_scale + 10) * j, small_scale, small_scale), 5)


        selected = inventory.is_selected()
        if selected:
            x,y = inventory.get_selected_item()
            pygame.draw.rect(surface, (0, 0, 255), (
                20 + LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y, small_scale, small_scale), 5)
        x,y = inventory.get_cursor()
        pygame.draw.rect(surface, (0, 255, 0), (
            20 + LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y, small_scale, small_scale), 5)





    if player is not None:
        text_skin = my_font.render(player.get_name(), False, (255, 0, 0))
        text_rect = text_skin.get_rect(
            center=(player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y() - scale // 2),
            width=scale)
        surface.blit(text_skin, text_rect)

        player_skin = sprites[player.get_skin()]
        player_skin = pygame.transform.scale(player_skin, (2 * draw_scale * scale, 2 * draw_scale * scale))
        player_rect = player_skin.get_rect(
            center=(player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y()),
            width=scale)
        surface.blit(player_skin, player_rect)
        if player.get_status() == Player.statuses["inventory"]:
            draw(surface, inventory=player.get_inventory())
