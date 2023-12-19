import pygame as pg


class Button:
    def __init__(self, text, x, y, color, font="comicsans", width=150, height=50):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.FONT = font
        self._FONT_SIZE = 40
        self._FONT_COLOR = "black"

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont(self.FONT, self._FONT_SIZE)
        text = font.render(self.text, 1, self._FONT_COLOR)
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            pg.time.delay(100)
            return True
        else:
            return False

    def update_button_color(self, win: pg.Surface, color):
        self.color = color
        self.draw(win)
