import pygame


class GameConstants:
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # GameConstants
    fps = 60
    step: int = 12
    scale: int = 72
    field: int = 20
    water_amount: int = 1
    water_size: int = 4
    tree_amount: int = 1
    fertile_soil_amount: int = 10
    LENGTH: int = screen_width
    HIGHT: int = screen_height

    # Button Constants
    exit_width = 100
    exit_height = 50

    screen_button_width = 100
    screen_button_height = 100

    menu_width = 2000
    menu_height = 1000

    start_button_width = 600
    start_button_height = 200

    start_button_position = [LENGTH // 2 - start_button_width // 2, 200]

    menu_exit_button_position = [LENGTH // 2 - start_button_width // 2, 500]

    very_small_button_size = 50
    small_button_size = 100
    big_button_size = 200

    small_offset = 10
    medium_offset = 20
    large_offset = 30
    huge_offset = 50
    ambiguous_offset = 100

    # INventoryConstants
    inventory_size_x = 5
    inventory_size_y = 10

    # DefaultBuildingsConstants
    miner_tree_wood_amount = 10
    miner_fertile_soil_amount = 10

    building_default_fuel_amount = 10
    building_default_input_amount = 10

    game_cat_box = (300, 150)

    default_draw_scale = 2

    # COLORS
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)

    alfa_transperent = 200
    grey_1 = (10, 10, 10)
    grey_2 = (20, 20, 20)
    grey_3 = (30, 30, 30)
    grey_4 = (40, 40, 40)
    grey_5 = (50, 50, 50)
    grey_6 = (60, 60, 60)

    # FontSizeConstants

    small_font = 36
    large_font = 72

    # Positions

    last_quarter = 3 / 4
    last_half = 1 / 2
    second_quarter = 1 / 4
