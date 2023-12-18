import pygame as pg
from button import Button
from constants import (BACKGROUND, BACKGROUND_2, WHITE, BLACK, PURPLE, PINK, LIGHT_BLUE, DARK_BLUE,
                       LIGHT_GREEN, DARK_GREEN, LIGHT_YELLOW, DARK_YELLOW, LIGHT_RED, DARK_RED)


class IntroScreen:
    @staticmethod
    def display(win):
        run = True
        clock = pg.time.Clock()

        while run:
            clock.tick(60)
            win.blit(BACKGROUND_2, [0, 0])

            font = pg.font.Font(None, 15)
            develop = font.render("Developed by Roberto 'BeTToH' Branco", True, PINK)
            win.blit(develop, [300, 620])

            font = pg.font.SysFont("comicsans", 45)

            title_1 = font.render("Robert's", 1, PINK)
            win.blit(title_1, (80, 130))

            font = pg.font.SysFont("arial BLACK", 55)
            title_2 = font.render("Pong Game", 1, LIGHT_BLUE)
            win.blit(title_2, (80, 160))

            pg.display.update()

            font = pg.font.SysFont("comicsans", 40)
            pg.time.delay(800)
            play = font.render('Click to Play', 1, (255, 0, 0))
            win.blit(play, (170, 470))
            pg.display.update()
            pg.time.delay(800)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    run = False
