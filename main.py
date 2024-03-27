import pygame

from src.Menu import MainMenu
from src.SingleGame import SingleGame

def main() -> None:
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    Menu = MainMenu(width=screen_width, height=screen_height)
    Menu.show()
    # Game = SingleGame()
    # Game.update_screen_size(screen_width, screen_height)
    # Game.play()


if __name__ == "__main__":
    main()
