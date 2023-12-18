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


class ConfigScreen:
    def __init__(self, win):
        self.win = win
        self.players = None
        self.goals_to_win = None
        self.difficulty = None

    def display(self):
        self.win.blit(BACKGROUND, [0, 0])

        font = pg.font.SysFont('fixedsys', 40)
        players_text = font.render('PLAYERS:', 2, WHITE)
        self.win.blit(players_text, [50, 50])

        player1 = Button('1 Player', 50, 100, DARK_GREEN)
        player2 = Button('2 Players', 50, 200, DARK_RED)
        player1.draw(self.win)
        player2.draw(self.win)

        goals = font.render('Goals to Win:', 2, WHITE)
        self.win.blit(goals, [270, 50])

        x_ax = 290
        five = Button('5 Goals', x_ax, 100, DARK_GREEN)
        seven = Button('7 Goals', x_ax, 170, DARK_RED)
        ten = Button('10 Goals', x_ax, 240, DARK_YELLOW)
        five.draw(self.win)
        seven.draw(self.win)
        ten.draw(self.win)

        txt = font.render('DIFFICULTY:', 3, WHITE)
        self.win.blit(txt, [50, 320])
        easy = Button('Normal', 50, 380, DARK_GREEN)
        normal = Button('Hard', 50, 450, DARK_BLUE)
        hard = Button('Impossible', 50, 520, DARK_RED)
        easy.draw(self.win)
        normal.draw(self.win)
        hard.draw(self.win)

        next_ = Button('Next ->', x_ax, 550, PINK)

        pg.display.update()

        aux = 0
        run = True
        while run:
            for event in pg.event.get():
                pos = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False

                # TODO: Improve button state alternation - Radio Btn class?
                if event.type == pg.MOUSEBUTTONDOWN:
                    if player1.click(pos):
                        player1.update_button_color(self.win, LIGHT_GREEN)
                        player2.update_button_color(self.win, DARK_RED)
                        self.players = 1
                        aux += 1

                    if player2.click(pos):
                        player2.update_button_color(self.win, LIGHT_RED)
                        player1.update_button_color(self.win, DARK_BLUE)
                        self.players = 2
                        aux += 1

                    if five.click(pos):
                        five.update_button_color(self.win, LIGHT_GREEN)
                        seven.update_button_color(self.win, DARK_RED)
                        ten.update_button_color(self.win, DARK_YELLOW)
                        self.goals_to_win = 5
                        aux += 1

                    if seven.click(pos):
                        five.update_button_color(self.win, DARK_GREEN)
                        seven.update_button_color(self.win, LIGHT_RED)
                        ten.update_button_color(self.win, DARK_YELLOW)
                        self.goals_to_win = 7
                        aux += 1

                    if ten.click(pos):
                        five.update_button_color(self.win, DARK_GREEN)
                        seven.update_button_color(self.win, DARK_RED)
                        ten.update_button_color(self.win, LIGHT_YELLOW)
                        self.goals_to_win = 10
                        aux += 1

                    if easy.click(pos):
                        easy.update_button_color(self.win, LIGHT_GREEN)
                        normal.update_button_color(self.win, DARK_BLUE)
                        hard.update_button_color(self.win, DARK_RED)
                        self.difficulty = 0

                    if normal.click(pos):
                        easy.update_button_color(self.win, DARK_GREEN)
                        normal.update_button_color(self.win, LIGHT_BLUE)
                        hard.update_button_color(self.win, DARK_RED)
                        self.difficulty = 1

                    if hard.click(pos):
                        easy.update_button_color(self.win, DARK_GREEN)
                        normal.update_button_color(self.win, DARK_BLUE)
                        hard.update_button_color(self.win, LIGHT_RED)
                        self.difficulty = 2

                    if next_.click(pos) and aux >= 2:
                        run = False

            # change the buttons colors
            if None not in (self.players, self.goals_to_win, self.difficulty):
                next_.draw(self.win)

            pg.display.update()


class CreditsScreen:
    @staticmethod
    def display(win):
        run = True

        clock = pg.time.Clock()
        font = pg.font.Font(None, 120)
        orig_surf = font.render("Robert's", True, PURPLE)
        txt_surf = orig_surf.copy()

        font2 = pg.font.Font(None, 60)
        surf2 = font2.render("Production", True, DARK_RED)
        txt_surf2 = surf2.copy()
        timer = 20
        alpha = 255
        pg.time.delay(900)
        count = 0
        font3 = pg.font.Font(None, 30)
        surf3 = font3.render("Developing Games since 2020", True, DARK_BLUE)
        txt_surf3 = surf3.copy()
        while run:
            count += 1
            if timer > 0:
                timer -= 1
            else:
                if alpha > 0:
                    alpha = max(0, alpha - 4)
                    txt_surf = orig_surf.copy()
                    txt_surf.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)

                    txt_surf2 = surf2.copy()
                    txt_surf2.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)
                    txt_surf3 = surf3.copy()
                    txt_surf3.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)

            win.fill(BLACK)
            win.blit(txt_surf, (80, 150))
            win.blit(txt_surf2, (120, 235))
            win.blit(txt_surf3, (85, 460))
            pg.display.update()
            clock.tick(22)

            if count == 130:
                pg.time.delay(70)
                pg.quit()
