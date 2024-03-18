import pygame


class Button():
    def __init__(self, text="START", width=None, height=None, hovered_skin=None, not_hovered_skin=None, func=None,
                 position=None, parent=None, parent_position="absolute"):
        self.text: str = text
        self.position: list[int] = position
        self.is_hovered: bool = False
        self.not_hovered_skin: str = not_hovered_skin
        self.hovered_skin: str = hovered_skin
        self.skin: str = self.not_hovered_skin
        self.func = func
        self.width: int = width
        self.height: int = height
        self.parent_position = parent_position
        self.parent = parent

        self.image = pygame.image.load(self.hovered_skin)
        if self.parent_position == "absolute":
            self.buttonRect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        else:
            pass

    def handle_hover(self):
        self.is_hovered = self.buttonRect.collidepoint(pygame.mouse.get_pos())
        self.change_skin()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.func:
                self.func()

    def update(self, event):
        self.handle_hover()
        self.handle_event(event)

    def change_skin(self):
        if self.is_hovered:
            self.skin = self.hovered_skin
        else:
            self.skin = self.not_hovered_skin
