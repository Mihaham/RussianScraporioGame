import pygame

LENGTH = 1500
HIGHT = 1000

def update_screen_size(x,y):
    global LENGTH, HIGHT
    LENGTH = x
    HIGHT = y
    print(LENGTH, HIGHT)

pygame.init()
info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
screen_width, screen_height = info.current_w, info.current_h
update_screen_size(screen_width, screen_height)

step = 12
scale = 72
field = 20

water_amount = 1
water_size = 4

tree_amount = 1

fertile_soil_amount = 10

Center_x = LENGTH // 2
Center_y = HIGHT // 2
