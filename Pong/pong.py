import pygame as pg
from racket import Racket
from ball import Ball
from button import Button
from constants import BACKGROUND, PINK, PURPLE, ORANGE, LIGHT_GREEN, LIGHT_RED


class Pong:
    def __init__(self, win: pg.Surface, players_num: int, goals_round: int, difficulty: int):
        self.win = win
        self.players_num = players_num
        self.goals_round = goals_round
        self.difficulty = difficulty
        self._time = 0
        self._count_goals = 0
        self._ball_vel = None
        self._rkt1 = None
        self._rkt2 = None
        self._ball = None

    def _prepare(self):
        self._rkt1 = Racket(100, 10, 180, LIGHT_GREEN)  # player 1
        self._rkt2 = Racket(100, 10, 180, LIGHT_RED, 70, score_pos=(20, 260))  # player 2 or bot
        self._ball = Ball(8, ORANGE, 4, 100, 300)

        if self.difficulty == 0:
            self._bot_vel = 4
        elif self.difficulty == 1:
            self._bot_vel = 6
        elif self.difficulty == 2:
            self._bot_vel = 9

    def _has_scored(self):
        return self._ball.y < 1 or self._ball.y > 599

    # draw when someone score
    def _score_break(self):
        font = pg.font.SysFont('fixedsys', 80)
        go = font.render("GOAAAAL", 1, PINK)
        self.win.blit(go, [120, 200])
        pg.display.update()
        pg.time.delay(400)

        self.win.blit(BACKGROUND, [0, 0])
        self._ball.draw(self.win)
        self._rkt1.draw(self.win)
        self._rkt2.draw(self.win)
        pg.display.update()
        pg.time.delay(500)

        go = font.render("GO", 1, PINK)
        self.win.blit(go, [210, 250])
        pg.display.update()

        pg.time.delay(500)

    def restart_positions(self):
        self._count_goals += 1
        self._rkt1.set_x(250)
        self._rkt2.set_x(250)

        if self._ball.y < 1:
            self._rkt1.score()
        elif self._ball.y > 599:
            self._rkt2.score()

        if self._count_goals % 4 == 0:
            self._ball.vel_x = self._ball.vel_init * -1
            self._ball.vel_y = -self._ball.vel_init
            self._ball.x = 200
            self._ball.y = 150
        elif self._count_goals % 4 == 1:
            self._ball.vel_x = -self._ball.vel_init
            self._ball.vel_y = self._ball.vel_init
            self._ball.x = 300
            self._ball.y = 150
        elif self._count_goals % 4 == 2:
            self._ball.vel_x = self._ball.vel_init
            self._ball.vel_y = -self._ball.vel_init
            self._ball.x = 200
            self._ball.y = 350
        else:
            self._ball.vel_x = self._ball.vel_init
            self._ball.vel_y = self._ball.vel_init
            self._ball.x = 300
            self._ball.y = 350

    def _score_actions(self):
        has_scored = self._has_scored()
        if has_scored:
            self._time = 0
            self._score_break()
            self.restart_positions()

    def run_match(self):
        self._prepare()
        clock = pg.time.Clock()
        last_key1 = -1
        last_key2 = -1

        self._ball.vel_y = 8
        self._ball.vel_x = 7

        self.win.blit(BACKGROUND, [0, 0])

        font = pg.font.SysFont('fixedsys', 60)
        for i in reversed(range(1, 4)):
            num = font.render(str(i), 4, PURPLE)
            self.win.blit(num, [240, 230])
            pg.display.update()
            pg.time.delay(700)
            self.win.blit(BACKGROUND, [0, 0])
            pg.display.update()
            pg.time.delay(300)

        text = font.render('GO', 3, PINK)
        self.win.blit(text, [215, 230])
        pg.display.update()
        pg.time.delay(300)

        self.win.blit(BACKGROUND, [0, 0])
        pg.display.update()

        run = True
        while run:
            self._time += 50/1000

            self.win.blit(BACKGROUND, [0, 0])

            clock.tick(60)

            for event in pg.event.get():
                pg.key.get_pressed()

                if event.type == pg.QUIT:
                    pg.quit()
                    run = False

                if event.type == pg.KEYDOWN:
                    # player 1 moves
                    if event.key == pg.K_LEFT:
                        self._rkt1.move(0)
                        last_key1 = 0
                    if event.key == pg.K_RIGHT:
                        self._rkt1.move(1)
                        last_key1 = 1

                    # player 2 moves
                    if event.key == pg.K_a:
                        self._rkt2.move(0)
                        last_key2 = 0
                    if event.key == pg.K_d:
                        self._rkt2.move(1)
                        last_key2 = 1

                # stop the racket move
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT and last_key1 == 0:
                        last_key1 = -1
                    if event.key == pg.K_RIGHT and last_key1 == 1:
                        last_key1 = -1

                    if self.players_num == 2:
                        if event.key == pg.K_a and last_key2 == 0:
                            last_key2 = -1
                        if event.key == pg.K_d and last_key2 == 1:
                            last_key2 = -1

            if last_key1 == 0:
                self._rkt1.move(0)
            if last_key1 == 1:
                self._rkt1.move(1)

            if last_key2 == 0:
                self._rkt2.move(0)
            if last_key2 == 1:
                self._rkt2.move(1)

            # bot action
            if self.players_num == 1:
                self._execute_bot_action()

            self._ball.move()
            self._ball.draw(self.win)
            self._rkt1.draw(self.win)
            self._rkt2.draw(self.win)
            self._ball.rkt_collision(self._rkt1, self._rkt2, self._time)

            pg.display.update()

            self._score_actions()

            if self._rkt1.current_score == self.goals_round or self._rkt2.current_score == self.goals_round:
                run = False

    def restart(self) -> int:
        self.win.blit(BACKGROUND, [0, 0])
        font = pg.font.SysFont('fixedsys', 80)

        if self._rkt1.current_score > self._rkt2.current_score:
            winner = 'Player 1 won'
        else:
            winner = 'Player 2 won'

        txt = font.render(winner, 2, PINK)
        self.win.blit(txt, [75, 200])
        pg.display.update()
        pg.time.delay(1000)

        restart_btn = Button('Restart', 70, 400, LIGHT_GREEN)
        exit_ = Button('Exit', 280, 400, LIGHT_RED)
        restart_btn.draw(self.win)
        exit_.draw(self.win)
        pg.display.update()
        pg.time.delay(2000)

        options = Button("Options", 175, 500, PINK)
        options.draw(self.win)
        pg.display.update()

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if restart_btn.click(pos):
                        self._rkt1.current_score = 0
                        self._rkt2.current_score = 0
                        return 1
                    if exit_.click(pos):
                        return -1
                    if options.click(pos):
                        self._rkt1.current_score = 0
                        self._rkt2.current_score = 0
                        return 0

    def _execute_bot_action(self):
        bot_speed = self._bot_vel
        d = 500

        bot_pos = self._rkt2.return_pos()

        ball_pos_x, ball_pos_y = self._ball.return_pos()

        if ball_pos_y <= d:
            if self.difficulty == 2:
                if bot_pos > 633 - 30:
                    self._rkt2.set_x(633 - 30)
                elif bot_pos < 30:
                    self._rkt2.set_x(30)
                else:
                    self._rkt2.set_x(ball_pos_x)
            else:
                if bot_pos > 633 - 30:
                    self._rkt2.set_x(633 - 30)
                elif bot_pos < 30:
                    self._rkt2.set_x(30)

                if ball_pos_y - self._rkt1.pos_y <= 10:
                    if bot_pos > ball_pos_x:
                        self._rkt2.set_x(bot_pos - bot_speed)
                    elif bot_pos < ball_pos_x:
                        self._rkt2.set_x(bot_pos + bot_speed)
                else:
                    if bot_pos > ball_pos_x:
                        self._rkt2.set_x(bot_pos - bot_speed)
                    elif bot_pos < ball_pos_x:
                        self._rkt2.set_x(bot_pos + bot_speed)
