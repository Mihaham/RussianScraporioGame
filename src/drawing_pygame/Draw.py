from glob import glob

import pygame

from src.Player.player import Player
from src.buttons.button import Button
from src.logger.Logger import Logger, GlobalObject


class Drawing(GlobalObject):
    @staticmethod
    def in_kwargs(find_option, **kwargs):
        if find_option in kwargs.keys():
            return kwargs[find_option]
        else:
            return None

    def __init__(self, **kwargs):
        super().__init__()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.sprites = { None : pygame.image.load("sprites/empty.png").convert_alpha()}
        self.objects : dict = {}
        self.scale = self.in_kwargs("scale", **kwargs)
        self.LENGTH = self.in_kwargs("LENGTH", **kwargs)
        self.HIGHT = self.in_kwargs("HIGHT", **kwargs)
        self.field = self.in_kwargs("field", **kwargs)
        self.step = self.in_kwargs("step", **kwargs)

    def get_image(self, skin : str):
        if skin in self.sprites.keys():
            return self.sprites[skin]

        try:
            self.sprites[skin] = pygame.image.load(skin).convert_alpha()
            return self.sprites[skin]
        except Exception:
            Logger.add_errors(f"Cannot load skin {skin}")
            return self.sprites[None]



    def update_parametrs(self, **kwargs):
        self.scale = kwargs["scale"]
        self.LENGTH = kwargs["LENGTH"]
        self.HIGHT = kwargs["HIGHT"]
        self.field = kwargs["field"]
        self.step = kwargs["step"]

    def draw(self, surface, player=None, board=None, this_single_square=None, object=None,
             inventory=None, pos_x=None,
             pos_y=None, draw_scale=1, button=None, Menu=None, building_menu=None, **kwargs):
        if board is not None:
            self.draw_board(surface=surface, board=board)
        if this_single_square is not None:
            self.draw_single_square(single_square=this_single_square)
        if object is not None:
            self.draw_object(surface, object=object, board=board, pos_x=pos_x, pos_y=pos_y,
                             draw_scale=draw_scale)
        if inventory is not None:
            self.draw_inventory(surface, inventory=inventory)
        if button is not None:
            self.draw_button(surface, button=button)
        if player is not None:
            self.draw_player(surface=surface, player=player, board=board)
        if Menu is not None:
            self.draw_menu(surface=surface, menu=Menu)
        if building_menu is not None:
            self.draw_building_menu(surface = surface, building_menu=building_menu)

    def draw_player(self, surface: pygame, player, board, draw_scale=1):
        text_skin = self.my_font.render(player.get_name(), False, (255, 0, 0))
        text_rect = text_skin.get_rect(
            center=(player.get_x() - board.get_game_pos_x(),
                    player.get_y() - board.get_game_pos_y() - self.scale // 2),
            width=self.scale)
        surface.blit(text_skin, text_rect)
        player_skin = self.get_image(player.get_skin())
        player_skin = pygame.transform.scale(player_skin, (
        2 * draw_scale * self.scale, 2 * draw_scale * self.scale))
        player_rect = player_skin.get_rect(
            center=(
            player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y()),
            width=self.scale)
        surface.blit(player_skin, player_rect)
        if player.get_status() == Player.statuses["inventory"]:
            self.draw_inventory(surface, inventory=player.get_inventory())

    def draw_object(self, surface: pygame, object, board, pos_x, pos_y, draw_scale=1):
        object_skin = self.get_image(object.get_skin())
        object_skin = pygame.transform.scale(object_skin,
                                             (draw_scale * self.scale, draw_scale * self.scale))
        object_rect = object_skin.get_rect(
            topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()),
            width=self.scale)
        surface.blit(object_skin, object_rect)

    def draw_inventory(self, surface: pygame, inventory):
        pygame.draw.rect(surface, (0, 0, 0), (self.LENGTH * 3 / 4, 0, self.LENGTH, self.HIGHT))
        text_skin = self.my_font.render("Inventory", False, (255, 255, 255))
        text_rect = text_skin.get_rect(
            midleft=(self.LENGTH * 3 / 4 + 20, 30),
            width=self.scale)
        surface.blit(text_skin, text_rect)

        small_scale = (self.LENGTH / 4) / (inventory.get_sizes()[0] + 3)
        for i in range(inventory.get_sizes()[0]):
            for j in range(inventory.get_sizes()[1]):
                pygame.draw.rect(surface, (255, 0, 0), (
                    20 + self.LENGTH * 3 / 4 + i * (small_scale + 10), 60 + (small_scale + 10) * j,
                    small_scale,
                    small_scale), 5)
                if inventory.get_grid()[i][j] != None:
                    items = inventory.get_grid()[i][j]
                    amount = inventory.get_amount()[i][j]
                    if items != None:
                        if items not in self.objects:
                            self.objects[items] = items()
                        skin = self.objects[items].get_skin()
                        object_skin = self.get_image(skin)
                        object_skin = pygame.transform.scale(object_skin,
                                                             (small_scale - 10, small_scale - 10))
                        object_rect = object_skin.get_rect(
                            topleft=(
                                20 + self.LENGTH * 3 / 4 + i * (small_scale + 10) + 5,
                                60 + (small_scale + 10) * j + 5),
                            width=self.scale)
                        surface.blit(object_skin, object_rect)
                        text_skin = self.my_font.render(f"{amount}", False, (255, 0, 0))
                        text_rect = text_skin.get_rect(
                            topleft=(
                                20 + self.LENGTH * 3 / 4 + i * (small_scale + 10) + 5,
                                60 + (small_scale + 10) * j + 5),
                            width=self.scale)
                        surface.blit(text_skin, text_rect)

        selected = inventory.is_selected()
        if selected:
            x, y = inventory.get_selected_item()
            pygame.draw.rect(surface, (0, 0, 255), (
                20 + self.LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y,
                small_scale,
                small_scale), 5)
        x, y = inventory.get_cursor()
        pygame.draw.rect(surface, (0, 255, 0), (
            20 + self.LENGTH * 3 / 4 + x * (small_scale + 10), 60 + (small_scale + 10) * y,
            small_scale, small_scale),
                         5)

    def draw_single_square(self, surface: pygame, single_square, board, pos_x, pos_y, draw_scale=1):
        if (board.get_game_pos_x() - self.scale <= pos_x <= board.get_game_pos_x() + (
                self.LENGTH) + self.scale and board.get_game_pos_y() - self.scale <= pos_y <= board.get_game_pos_y() + (
                self.HIGHT) + self.scale):
            square_skin = self.get_image(single_square.get_skin())
            square_skin = pygame.transform.scale(square_skin,
                                                 (draw_scale * self.scale, draw_scale * self.scale))
            square_rect = square_skin.get_rect(
                topleft=(pos_x - board.get_game_pos_x(), pos_y - board.get_game_pos_y()),
                width=self.scale)
            surface.blit(square_skin, square_rect)
            for object in single_square.get_buildings():
                self.draw_object(surface, object=object, pos_x=pos_x,
                                 pos_y=pos_y, board=board)
            for object in single_square.get_miners():
                self.draw_object(surface, board=board, object=object, pos_x=pos_x,
                                 pos_y=pos_y)

    def draw_board(self, surface: pygame, board):
        pygame.draw.rect(surface, (0, 0, 255), (0, 0, self.LENGTH, self.HIGHT))
        for i in range(max(0, board.get_game_pos_x() // self.scale),
                       min((board.get_game_pos_x() + self.LENGTH) // self.scale + 1, self.field)):
            for j in range(max(0, board.get_game_pos_y() // self.scale),
                           min((board.get_game_pos_y() + self.HIGHT) // self.scale + 1,
                               self.field)):
                self.draw_single_square(surface, board=board, pos_x=i * self.scale,
                                        pos_y=j * self.scale,
                                        single_square=board.get_grid()[i][j])

    def draw_button(self, surface: pygame, button: Button):
        image = pygame.transform.scale(self.get_image(button.skin), (button.width, button.height))
        rect = image.get_rect(topright=button.position)
        surface.blit(image, rect.topright)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(button.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=rect.topright)
        surface.blit(text_surface, text_rect)

    def draw_menu(self, surface: pygame, menu):
        square_skin = self.get_image(menu.background)
        square_skin = pygame.transform.scale(square_skin, (menu.width, menu.height))
        square_rect = square_skin.get_rect(
            topleft=(menu.x, menu.y))
        surface.blit(square_skin, square_rect)
        for button_line in menu.buttons:
            for button in button_line:
                self.draw_button(surface=surface, button=button)

    def draw_building_menu(self, surface: pygame, building_menu = None):
        pygame.draw.rect(surface, (20, 20, 20), (building_menu.x, building_menu.y, building_menu.width, building_menu.height))
        pygame.draw.rect(surface, (30, 30, 30), (
        building_menu.x, building_menu.y, building_menu.width/2, building_menu.height))
        pygame.draw.rect(surface, (10, 10, 10), (
        building_menu.x + building_menu.width/2, building_menu.y, building_menu.width/2, building_menu.height/2))
        image = pygame.transform.scale(self.get_image(building_menu.building.get_skin()), (building_menu.width/2, building_menu.height))
        rect = image.get_rect(topright=(building_menu.x,building_menu.y))
        surface.blit(image, rect.topright)
        self.draw_button(surface=surface, button=building_menu.buttons[0][0])


