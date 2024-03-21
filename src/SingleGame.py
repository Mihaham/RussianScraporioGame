import pygame

from src.Game.Board import Board
from src.Player.player import Player
from src.buttons.button import Button
from src.drawing_pygame.Draw import Drawing
from src.logger.Logger import Logger

class SingleGame():
    def __init__(self):
        self.fps : int = 60
        pygame.init()
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        self.LENGTH : int = screen_width
        self.HIGHT : int = screen_height
        self.step : int = 12
        self.scale : int = 72
        self.field : int = 20
        self.water_amount : int = 1
        self.water_size : int = 4
        self.tree_amount : int = 1
        self.fertile_soil_amount : int = 10
        self.center_x : int = self.LENGTH // 2
        self.center_y : int = self.HIGHT // 2
        pygame.font.init()

        self.clock : pygame.time.Clock = pygame.time.Clock()
        pygame.display.set_caption("Really russian game")

        self.surface : pygame.display = pygame.display.set_mode((self.LENGTH, self.HIGHT))
        self.Exit : Button = Button(width=self.LENGTH // 15,
                           height=self.HIGHT // 10,
                           text="",
                           not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                           hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                           position=[self.LENGTH - self.LENGTH // 15, 0],
                           func=exit)
        self.Screen : Button = Button(width=self.LENGTH // 15,
                             height=self.HIGHT // 10,
                             text="FULLSCREEN MODE",
                             not_hovered_skin="sprites/Large Buttons/Large Buttons/Exit Button.png",
                             hovered_skin="sprites/Large Buttons/Colored Large Buttons/Exit  col_Button.png",
                             # position=[self.LENGTH - self.LENGTH // 15, 100],
                             position=[0, 0],
                             func=self.change_screen_size)
        self.Draw : Drawing = Drawing(scale=self.scale, LENGTH=self.LENGTH, HIGHT=self.HIGHT,
                            field=self.field, step=self.step)
        self.board : Board = Board(field=self.field, water_amount=self.water_amount,
                           water_size=self.water_size,
                           tree_amount=self.tree_amount,
                           fertile_soil_amount=self.fertile_soil_amount)
        self.player : Player = Player(position_x=self.center_x, position_y=self.center_y, scale=self.scale)
        Logger.add_info("Game is initialized")

    def play(self) -> None:
        Logger.add_info("Started single game")
        while True:
            self.Draw.draw(self.surface, player=self.player, board=self.board, button=self.Exit)
            self.Draw.draw(self.surface, button=self.Screen)
            self.Exit.handle_hover()
            self.Screen.handle_hover()
            for event in pygame.event.get():
                self.Exit.update(event)
                self.Screen.update(event)
                if event.type == pygame.QUIT:
                    self.Log.add_info("Game is over")
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.player.move(event, board=self.board, scale=self.scale)
            self.player.update(self.board, scale=self.scale, field=self.field,
                               Center_x=self.center_x,
                               Center_y=self.center_y, step=self.step)
            self.board.update()

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(self.fps)

    def update_screen_size(self, x : int, y : int) -> None:
        Logger.add_info(f"Screen sizes are updated with parametrs x = {x}, y = {y}")
        self.LENGTH = x
        self.HIGHT = y

    def change_screen_size(self) -> None:
        Logger.add_info("Screen size is updated")
        if self.LENGTH == pygame.display.Info().current_w:
            self.LENGTH = 2000
            self.surface = pygame.display.set_mode((self.LENGTH, 1000))
        else:
            info = pygame.display.Info()
            self.update_screen_size(info.current_w, info.current_h)
            self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.Draw.update_parametrs(scale=self.scale, LENGTH=self.LENGTH, HIGHT=self.HIGHT,
                                   field=self.field,
                                   step=self.step)


class GameAdapter():

    def __init__(self, Game : SingleGame) -> None:
        self.SingleGame = Game
        Logger.add_info("GameAdapter is initialized")

    def get_game_parameters(self) -> dict:
        Logger.add_info("Getting info about SingleGame")
        dict = {}
        dict["fps"] = self.SingleGame.fps
        dict["LENGTH"] = self.SingleGame.LENGTH
        dict["HIGHT"] = self.SingleGame.HIGHT
        dict["step"] = self.SingleGame.step
        dict["scale"] = self.SingleGame.scale
        dict["field"] = self.SingleGame.field
        dict["water_amount"] = self.SingleGame.water_amount
        dict["water_size"] = self.SingleGame.water_size
        dict["tree_amount"] = self.SingleGame.tree_amount
        dict["fertile_soil_amount"] = self.SingleGame.fertile_soil_amount
        dict["Center_x"] = self.SingleGame.center_x
        dict["Center_y"] = self.SingleGame.center_y
        dict["surface"] = self.SingleGame.surface
        dict["Log"] = self.SingleGame.Log
        dict["Exit"] = self.SingleGame.Exit
        dict["Screen"] = self.SingleGame.Screen
        dict["Draw"] = self.SingleGame.Draw
        dict["board"] = self.SingleGame.board
        dict["player"] = self.SingleGame.player

        return dict


def start_game() -> None:
    Logger.add_info("Starting SingleGame")
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    Game = SingleGame()
    Game.update_screen_size(screen_width, screen_height)
    Game.play()