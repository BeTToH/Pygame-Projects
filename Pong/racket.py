import pygame as pg


class Racket:
    def __init__(self, width, height, pos_x: int, color, pos_y=530, score_pos=(20, 310), vel=15):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.current_score = 0
        self.score_pos = score_pos
        self.vel = vel
        self.side = -1  # side --> 0 = left, 1 = right

    def draw(self, win):
        (pg.draw.
         rect(win, self.color, (self.pos_x-self.width//2, self.pos_y, self.width, self.height)))
        if self.pos_x > 633 - self.width:
            self.pos_x = 633 - self.width

        font = pg.font.SysFont('fixedsys', 50)
        score = font.render(str(self.current_score), True, self.color)
        win.blit(score, self.score_pos)

    def move(self, side):
        if side == 0 and self.pos_x-self.width//2 > 0:
            self.pos_x -= self.vel
            self.side = 0
        elif side == 1 and self.pos_x-self.width//2 < 699 - self.width:
            self.pos_x += self.vel
            self.side = 1

    def pos(self):
        return self.pos_x, self.pos_y, self.width, self.side

    def score(self):
        self.current_score += 1

    def set_x(self, x):
        self.pos_x = x

    def return_pos(self):
        return self.pos_x
