import pygame

from src.Menu import MainMenu
from src.SingleGame import SingleGame
import src.Menu

def main() -> None:

    Game = MainGame()
    Game.play()

class MainGame:
    def __init__(self):
        self.Status = "Menu"
        pygame.init()
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        self.Menu = MainMenu(width=screen_width, height=screen_height, start = self.change)
        self.Menu.show()

    def change(self, Status : str):
        self.Status = Status



    def play(self):
        while (True):
            if self.Status == "Menu":
                self.Menu.draw_menu()
                self.Menu.loop()
            elif self.Status == "Start_game":
                self.Menu.show()
                del self.Menu
                self.Status = "Game"
                self.Game = SingleGame()
            elif self.Status == "Game":
                self.Game.play()



if __name__ == "__main__":
    main()
