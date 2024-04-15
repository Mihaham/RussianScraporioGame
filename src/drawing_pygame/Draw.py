import pygame

from src.Player.player import Player
from src.buttons.button import Button
from src.logger.Logger import Logger, GlobalObject
from src.CONST import GameConstants


class Drawing(GlobalObject):
    @staticmethod
    def in_kwargs(find_option, **kwargs):
        if find_option in kwargs.keys():
            return kwargs[find_option]
        else:
            return None

    def __init__(self, **kwargs):
        super().__init__()
        self.my_font = pygame.font.SysFont('Comic Sans MS', GameConstants.small_font)
        self.sprites = {None: pygame.image.load("sprites/empty.png").convert_alpha()}
        self.objects: dict = {}
        self.scale = self.in_kwargs("scale", **kwargs)
        self.LENGTH = self.in_kwargs("LENGTH", **kwargs)
        self.HIGHT = self.in_kwargs("HIGHT", **kwargs)
        self.field = self.in_kwargs("field", **kwargs)
        self.step = self.in_kwargs("step", **kwargs)

    def get_image(self, skin: str):
        if skin in self.sprites.keys():
            return self.sprites[skin]

        try:
            self.sprites[skin] = pygame.image.load(skin).convert_alpha()
            return self.sprites[skin]
        except Exception:
            Logger.add_errors(f"Cannot load skin {skin}")
            return self.sprites[None]

    def get_object_skin(self, items):
        if items not in self.objects:
            self.objects[items] = items()
        skin = self.objects[items].get_skin()
        return skin

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
            self.draw_building_menu(surface=surface, building_menu=building_menu)

    def draw_text(self, surface, text, position):
        text_skin = self.my_font.render(text, False, GameConstants.red)
        text_rect = text_skin.get_rect(
            center=position,
            width=self.scale)
        surface.blit(text_skin, text_rect)

    def draw_player(self, surface: pygame, player, board, draw_scale=GameConstants.default_draw_scale):
        self.draw_text(surface, player.get_name(), (player.get_x() - board.get_game_pos_x(),
                                                    player.get_y() - board.get_game_pos_y() - self.scale // 2))

        player_skin = self.get_image(player.get_skin())
        player_skin = pygame.transform.scale(player_skin, (
            draw_scale * self.scale, draw_scale * self.scale))
        player_rect = player_skin.get_rect(
            center=(
                player.get_x() - board.get_game_pos_x(), player.get_y() - board.get_game_pos_y()),
            width=self.scale)
        surface.blit(player_skin, player_rect)
        if player.get_inventory().is_selected():
            i, j = player.get_inventory().get_selected_position()
            items = player.get_inventory().get_grid()[i][j]
            small_scale = self.scale
            if items != None:
                skin = self.get_object_skin(items)
                object_skin = self.get_image(skin)
                object_skin = pygame.transform.scale(object_skin,
                                                     (small_scale, small_scale))
                object_skin.set_alpha(GameConstants.alfa_transperent)
                object_rect = object_skin.get_rect(
                    center=pygame.mouse.get_pos(),
                    width=self.scale)
                surface.blit(object_skin, object_rect)
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
        pygame.draw.rect(surface, GameConstants.black, (self.LENGTH * GameConstants.last_quarter, 0, self.LENGTH, self.HIGHT))
        text_skin = self.my_font.render("Inventory", False, GameConstants.white)
        text_rect = text_skin.get_rect(
            midleft=(self.LENGTH * GameConstants.last_quarter + GameConstants.medium_offset, GameConstants.large_offset),
            width=self.scale)
        surface.blit(text_skin, text_rect)

        small_scale = (self.LENGTH  * GameConstants.second_quarter) / (inventory.get_sizes()[0] + GameConstants.default_boarder)
        for i in range(inventory.get_sizes()[0]):
            for j in range(inventory.get_sizes()[1]):
                pygame.draw.rect(surface, GameConstants.red, (
                    GameConstants.medium_offset + self.LENGTH * GameConstants.last_quarter + i * (small_scale + GameConstants.small_offset), GameConstants.large_offset * 2 + (small_scale + GameConstants.small_offset) * j,
                    small_scale,
                    small_scale), GameConstants.default_boarder)
                if inventory.get_grid()[i][j] != None:
                    items = inventory.get_grid()[i][j]
                    amount = inventory.get_amount()[i][j]
                    if items != None:
                        skin = self.get_object_skin(items)
                        object_skin = self.get_image(skin)
                        object_skin = pygame.transform.scale(object_skin,
                                                             (small_scale - 2 * GameConstants.default_boarder, small_scale - 2 * GameConstants.default_boarder))
                        object_rect = object_skin.get_rect(
                            topleft=(
                                GameConstants.medium_offset + self.LENGTH * GameConstants.last_quarter + i * (small_scale + GameConstants.small_offset) + GameConstants.default_boarder,
                                2*GameConstants.large_offset + (small_scale + GameConstants.small_offset) * j + GameConstants.default_boarder),
                            width=self.scale)
                        surface.blit(object_skin, object_rect)
                        text_skin = self.my_font.render(f"{amount}", False, GameConstants.red)
                        text_rect = text_skin.get_rect(
                            topleft=(
                                GameConstants.medium_offset + self.LENGTH * GameConstants.last_quarter + i * (small_scale + GameConstants.small_offset) + GameConstants.default_boarder,
                                2*GameConstants.large_offset + (small_scale + GameConstants.small_offset) * j + GameConstants.default_boarder),
                            width=self.scale)
                        surface.blit(text_skin, text_rect)

        selected = inventory.is_selected()
        if selected:
            x, y = inventory.get_selected_position()
            pygame.draw.rect(surface, GameConstants.blue, (
                GameConstants.medium_offset + self.LENGTH * GameConstants.last_quarter + x * (small_scale + GameConstants.small_offset), 2 * GameConstants.large_offset + (small_scale + 2 * GameConstants.default_boarder) * y,
                small_scale,
                small_scale), GameConstants.default_boarder)
        x, y = inventory.get_cursor()
        pygame.draw.rect(surface, GameConstants.green, (
            GameConstants.medium_offset + self.LENGTH * GameConstants.last_quarter + x * (small_scale + GameConstants.small_offset), 2*GameConstants.large_offset + (small_scale + GameConstants.small_offset) * y,
            small_scale, small_scale),
                        GameConstants.default_boarder)

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
        pygame.draw.rect(surface, GameConstants.blue, (0, 0, self.LENGTH, self.HIGHT))
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
        font = pygame.font.Font(None, GameConstants.small_font)
        text_surface = font.render(button.text, True, GameConstants.white)
        text_rect = text_surface.get_rect(
            center=(button.position[0] + button.width * GameConstants.last_half, button.position[1] + button.height  * GameConstants.last_half))
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

    def draw_building_menu(self, surface: pygame, building_menu=None):
        pygame.draw.rect(surface, GameConstants.grey_2, (
        building_menu.x, building_menu.y, building_menu.width, building_menu.height))
        pygame.draw.rect(surface, GameConstants.grey_3, (
            building_menu.x, building_menu.y, building_menu.width * GameConstants.last_half, building_menu.height), GameConstants.default_boarder)
        pygame.draw.rect(surface, GameConstants.grey_1, (
            building_menu.x + building_menu.width * GameConstants.last_half, building_menu.y, building_menu.width * GameConstants.last_half,
            building_menu.height  * GameConstants.last_half))
        pygame.draw.rect(surface, GameConstants.grey_4, (
            building_menu.x + building_menu.width * GameConstants.last_quarter, building_menu.y, building_menu.width * GameConstants.second_quarter,
            building_menu.height * GameConstants.last_half))
        image = pygame.transform.scale(self.get_image(building_menu.building.get_skin()),
                                       (building_menu.width  * GameConstants.last_half, building_menu.height))
        rect = image.get_rect(topright=(building_menu.x, building_menu.y))
        surface.blit(image, rect.topright)
        size = GameConstants.very_small_button_size
        boarder_size = GameConstants.default_boarder
        rect_color = GameConstants.grey_4
        position = [building_menu.x + building_menu.width * GameConstants.last_quarter, building_menu.y + GameConstants.huge_offset]
        text_skin = self.my_font.render(f"ВХОД:", False, GameConstants.red)
        text_rect = text_skin.get_rect(
            topleft=(position[0] + GameConstants.small_offset + boarder_size, position[1] + boarder_size - GameConstants.huge_offset),
            width=self.scale)
        surface.blit(text_skin, text_rect)
        for i, (item, amount) in enumerate(building_menu.building.input.items()):
            pygame.draw.rect(surface, rect_color,
                             (position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset), position[1], size, size),
                             boarder_size)
            image = pygame.transform.scale(self.get_image(self.get_object_skin(item)),
                                           (size - 2 * boarder_size, size - 2 * boarder_size))
            rect = image.get_rect(topright=(
            position[0] + GameConstants.small_offset + boarder_size, position[1] + boarder_size + i * (size + GameConstants.small_offset)))
            surface.blit(image, rect.topright)
            text_skin = self.my_font.render(f"{amount}", False, GameConstants.red)
            text_rect = text_skin.get_rect(
                topleft=(
                position[0] + GameConstants.small_offset + boarder_size, position[1] + boarder_size + i * (size + GameConstants.small_offset)),
                width=self.scale)
            surface.blit(text_skin, text_rect)
        position = [building_menu.x + building_menu.width * GameConstants.last_quarter + GameConstants.small_button_size, building_menu.y + GameConstants.huge_offset]
        text_skin = self.my_font.render(f"ВЫХОД:", False, GameConstants.red)
        text_rect = text_skin.get_rect(
            topleft=(position[0] + GameConstants.small_offset + boarder_size, position[1] + boarder_size - GameConstants.huge_offset),
            width=self.scale)
        surface.blit(text_skin, text_rect)
        for i, (item, amount) in enumerate(building_menu.building.output.items()):
            pygame.draw.rect(surface, rect_color,
                             (position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset), position[1], size, size),
                             boarder_size)
            image = pygame.transform.scale(self.get_image(self.get_object_skin(item)),
                                           (size - 2 * boarder_size, size - 2 * boarder_size))
            rect = image.get_rect(topright=(
                position[0] + GameConstants.small_offset + boarder_size, position[1] + boarder_size + i * (size + GameConstants.small_offset)))
            surface.blit(image, rect.topright)
            text_skin = self.my_font.render(f"{amount}", False, GameConstants.red)
            text_rect = text_skin.get_rect(
                topleft=(
                    position[0] + GameConstants.small_offset + boarder_size, position[1] + boarder_size + i * (size + GameConstants.small_offset)),
                width=self.scale)
            surface.blit(text_skin, text_rect)
        for button_line in building_menu.buttons:
            for button in button_line:
                self.draw_button(surface=surface, button=button)

        rect_color = GameConstants.grey_5
        size = GameConstants.small_button_size
        boarder_size = GameConstants.default_boarder
        pygame.draw.rect(surface, rect_color, (building_menu.x + building_menu.width  * GameConstants.last_half - size,
                                               building_menu.y + building_menu.height * GameConstants.last_half, size,
                                               size), boarder_size)
        image = pygame.transform.scale(
            self.get_image(self.get_object_skin(building_menu.building.fuel["name"])),
            (size - 2 * boarder_size, size - 2 * boarder_size))
        rect = image.get_rect(topright=(
        building_menu.x + building_menu.width * GameConstants.last_half + boarder_size - size,
        building_menu.y + building_menu.height * GameConstants.last_half + boarder_size))
        amount = building_menu.building.fuel["amount"]
        surface.blit(image, rect.topright)
        text_skin = self.my_font.render(f"{amount}", False, GameConstants.red)
        text_rect = text_skin.get_rect(
            topleft=(building_menu.x + building_menu.width * GameConstants.last_half + boarder_size - size,
                     building_menu.y + building_menu.height * GameConstants.last_half + boarder_size),
            width=self.scale)
        surface.blit(text_skin, text_rect)
        text_skin = self.my_font.render("Топливо:", False, GameConstants.red)
        text_rect = text_skin.get_rect(
            topleft=(building_menu.x + building_menu.width * GameConstants.last_half + boarder_size - size,
                     building_menu.y + building_menu.height * GameConstants.last_half - GameConstants.large_offset),
            width=self.scale)
        surface.blit(text_skin, text_rect)

        for i, recipe in enumerate(building_menu.recipes):
            self.draw_recipe(surface=surface, recipe=recipe,
                             position=[building_menu.x + building_menu.width * GameConstants.last_half + GameConstants.small_button_size,
                                       building_menu.y + GameConstants.medium_offset + i * (GameConstants.very_small_button_size + GameConstants.small_offset)])

        if building_menu.building.active_recipe == None:
            font = pygame.font.Font(None, GameConstants.large_font)
            text_surface = font.render("У вас нет активного рецепта", True, GameConstants.red)
            text_rect = text_surface.get_rect(topright=(building_menu.x + building_menu.width - GameConstants.medium_offset,
                                                        building_menu.y + building_menu.height * GameConstants.last_quarter))
            surface.blit(text_surface, text_rect)
        else:
            self.draw_recipe(surface, building_menu.building.active_recipe,
                             position=[building_menu.x + building_menu.width * GameConstants.last_half + GameConstants.medium_offset,
                                       building_menu.y + building_menu.height * GameConstants.last_quarter])

    def draw_recipe(self, surface, recipe, position):
        size = GameConstants.very_small_button_size
        boarder_size = GameConstants.default_boarder
        rect_color = GameConstants.grey_4
        for i, (item, amount) in enumerate(recipe.input_resources.items()):
            pygame.draw.rect(surface, rect_color,
                             (position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset), position[1], size, size),
                             boarder_size)
            image = pygame.transform.scale(self.get_image(self.get_object_skin(item)),
                                           (size - 2 * boarder_size, size - 2 * boarder_size))
            rect = image.get_rect(topright=(
            position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset) + boarder_size, position[1] + boarder_size))
            surface.blit(image, rect.topright)
            text_skin = self.my_font.render(f"{amount}", False, GameConstants.red)
            text_rect = text_skin.get_rect(
                topleft=(
                position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset) + boarder_size, position[1] + boarder_size),
                width=self.scale)
            surface.blit(text_skin, text_rect)

        start_output = GameConstants.small_offset + len(recipe.input_resources.keys()) * (size + GameConstants.small_offset)

        arrow = "sprites/Square Buttons/Square Buttons/Next Square Button.png"
        image = pygame.transform.scale(self.get_image(arrow), (size, size))
        rect = image.get_rect(topright=(position[0] + start_output, position[1]))
        surface.blit(image, rect.topright)

        start_output += GameConstants.very_small_button_size
        for i, (item, amount) in enumerate(recipe.output_resources.items()):
            pygame.draw.rect(surface, rect_color, (
            position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset) + start_output, position[1], size, size),
                             boarder_size)
            image = pygame.transform.scale(self.get_image(self.get_object_skin(item)),
                                           (size - 2 * boarder_size, size - 2 * boarder_size))
            rect = image.get_rect(topright=(
            position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset) + boarder_size + start_output,
            position[1] + boarder_size))
            surface.blit(image, rect.topright)
            text_skin = self.my_font.render(f"{amount}", False, GameConstants.red)
            text_rect = text_skin.get_rect(
                topleft=(position[0] + GameConstants.small_offset + i * (size + GameConstants.small_offset) + boarder_size + start_output,
                         position[1] + boarder_size))
            surface.blit(text_skin, text_rect)
