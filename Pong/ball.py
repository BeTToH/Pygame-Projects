import pygame as pg
from random import randint
from racket import Racket


class Ball:
    def __init__(self, radius, color, vel, y, x=500):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.vel_x = vel
        self.vel_y = vel
        self.vel_init = vel

    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius, self.radius)

    def move(self):
        if not 499 > self.x > 1:
            self.vel_x *= -1
            if self.x <= 1:
                self.x = 2
            elif self.x >= 499:
                self.x = 498

        self.y += self.vel_y
        self.x += self.vel_x

    def rkt_collision(self, racket: Racket, racket_2: Racket, tempo: float):
        # TODO: apply real physics to it
        ACC = 2
        COLLISION_X_MARGIN = 2

        prev_pos = (self.x - self.vel_x, self.y - self.vel_y)
        if prev_pos[1] < racket.pos_y < self.y:
            self.y = racket.pos_y
            self.x -= self.vel_x // 2
        if ((racket.pos_x - COLLISION_X_MARGIN - racket.width // 2 < self.x <
                racket.pos_x + racket.width + COLLISION_X_MARGIN - racket.width // 2)
                and self.y == racket.pos_y):
            self.vel_y *= -1
            vel = self.vel_x

            if self.vel_x > 0:
                self.vel_x += ACC
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += ACC
            elif self.vel_x < 0:
                self.vel_x += ACC
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += ACC
            else:
                self.vel_x += randint(-3, 3)

        if prev_pos[1] > racket_2.pos_y + 11 and self.y < 81:
            self.y = 81
            self.x -= self.vel_x // 2

        if racket_2.pos_x-2 - racket_2.width//2 < self.x < racket_2.pos_x + racket_2.width+2 - racket_2.width//2 and self.y == 81:
            self.vel_y *= -1
            vel = self.vel_x
            if vel > 0:
                self.vel_x += ACC
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += randint(-ACC * vel - 1, 4)
            elif self.vel_x < 0:
                self.vel_x += ACC
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += ACC
            else:
                self.vel_x += randint(-3, 3)

    def get_speed(self, speed):
        if self.vel_y > 0:
            self.vel_y = speed
        else:
            self.vel_y = -speed

        if self.vel_x > 0:
            self.vel_x = speed
        else:
            self.vel_x = -speed

    def return_pos(self):
        return self.x, self.y
