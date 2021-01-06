import pygame as pg
from random import randint, randrange
pg.init()
pg.font.init()

largura = 500
altura = 633

win = pg.display.set_mode((largura, altura))
pg.display.set_caption("Robert's Pong Game")
back = pg.image.load('midia/backgroung.png')
back1 = pg.image.load('midia/back2.png')

# global vars
# colors
light_red = (255, 0, 0)
dark_red = (120, 0, 0)

dark_yellow = (140, 140, 0)

light_green = (0, 255, 0)
dark_green = (0, 130, 0)

light_blue = (0, 0, 255)
dark_blue = (0, 0, 120)

pink = (240, 0, 130)
purple = (51, 0, 102)

black = (0, 0, 0)
white = (255, 255, 255)

# counters
bot_vel = 13# difficulty changes it
players = 0
goals_round = 5
difficulty = 0# 0, 1 ou 2
# obj racket(players) and ball in line ->271


class Buttons():
    def __init__(self, text, x, y, color, width=150, height=50):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
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


# rkt = players
class Racket():
    def __init__(self, largura, altura, pos_x: int, color, pos_y=530, score_pos=(20, 310), vel=15):
        self.largura = largura
        self.altura = altura
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.score = 0
        self.score_pos = score_pos
        self.vel = vel
        self.lado = -1

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.pos_x-self.largura//2, self.pos_y, self.largura, self.altura))
        if self.pos_x > 633 - self.largura:
            self.pos_x = 633 - self.largura

        font = pg.font.SysFont('fixedsys', 50)
        score = font.render(str(self.score), True, self.color)
        win.blit(score, self.score_pos)

    def move(self, lado): # lado --> 0 = left, 1 = right
        global largura
        if lado == 0 and self.pos_x-self.largura//2 > 0:
            self.pos_x -= self.vel
            self.lado = 0
        elif lado == 1 and self.pos_x-self.largura//2 < largura - self.largura:
            self.pos_x += self.vel
            self.lado = 1

    def pos(self):
        return self.pos_x, self.pos_y, self.largura, self.lado

    def get_score(self):
        self.score += 1

    def get_pos(self, pos):
        self.pos_x = pos

    def return_pos(self):
        return self.pos_x


class Balls():
    def __init__(self, raio, color, vel, y, x=500):
        self.raio = raio
        self.color = color
        self.x = x
        self.y = y
        self.vel_x = vel
        self.vel_y = vel
        self.vel_init = vel
        self.count_goal = 4

    def draw(self):
        pg.draw.circle(win, self.color, (self.x, self.y), self.raio, self.raio)

    def move(self):
        # impede q saia do campo
        if not 499 > self.x > 1:
            self.vel_x *= -1
            # anti-bug
            if self.x <= 1:
                self.x = 2
            elif self.x >= 499:
                self.x = 498

        self.y += self.vel_y
        self.x += self.vel_x

    def rkt_collision(self):
        global tempo
        Racket_x, Racket_y, Racket_size, Racket_lado = Racket.pos(rkt1) # p1
        rkt2_x, rkt2_y, rkt2_size, rkt2_lado = rkt2.pos() # p2
        prev_pos = (self.x - self.vel_x, self.y - self.vel_y)

        if prev_pos[1] < Racket_y < self.y:
            self.y = Racket_y
            self.x -= self.vel_x // 2
        if Racket_x-2 - Racket_size//2 < self.x < Racket_x + Racket_size+2 - Racket_size//2 and self.y == Racket_y:

            self.vel_y *= -1
            vel = self.vel_x

            if self.vel_x > 0:
                self.vel_x += randint(-2*vel, 4)
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += randint(-2 * vel, 4)
            elif self.vel_x < 0:
                self.vel_x += randint(-4, -2*vel)
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += randint(-4, -2 * vel)
            else:
                self.vel_x += randint(-3, 3)

            if 13 < tempo < 15.03:
                ball.get_speed(8)

            if 18 < tempo < 20.03:
                ball.get_speed(9)

        if prev_pos[1] > rkt2_y + 11 and self.y < 81:
            self.y = 81
            self.x -= self.vel_x // 2

        if rkt2_x-2 - rkt2_size//2 < self.x < rkt2_x + rkt2_size+2 - rkt2_size//2 and self.y == 81:
            self.vel_y *= -1
            vel = self.vel_x
            if vel > 0:
                self.vel_x += randint(-2*vel - 1, 4)
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += randint(-2 * vel - 1, 4)
            elif self.vel_x < 0:
                self.vel_x += randint(-4, -2*vel)
                while 2 >= self.vel_x >= 1 or -2 <= self.vel_x <= -1:
                    self.vel_x += randint(-4, -2*vel)
            else:
                self.vel_x += randint(-3, 3)
            # increase the ball speed when a rkt hits it
            if 5 < tempo < 8.03:
                ball.get_speed(10)

            if 8.03 < tempo < 13.03:
                ball.get_speed(11)

            if 13.03 < tempo < 19:
                ball.get_speed(12)

            if 19 < tempo < 29.03:
                ball.get_speed(13)

            if 29.03 < tempo < 37:
                ball.get_speed(14)

            if 50 < tempo < 57:
                ball.get_speed(16)

    # actions when someone score
    def scoring(self):
        global tempo

        if self.y < 1:
            rkt1.get_score()
            self.x = 300
            self.y = 300
            tempo = 0
            score_break()
            if self.count_goal % 4 == 0:
                self.vel_x = self.vel_init * -1
                self.vel_y = -self.vel_init
            elif self.count_goal % 4 == 1:
                self.vel_x = -self.vel_init
                self.vel_y = self.vel_init
            elif self.count_goal % 4 == 2:
                self.vel_x = self.vel_init
                self.vel_y = -self.vel_init
            else:
                self.vel_x = self.vel_init
                self.vel_y = self.vel_init
            self.count_goal += 1
            rkt1.get_pos(250)
            rkt2.get_pos(250)

        if self.y > 599:
            rkt2.get_score()
            tempo = 0
            score_break()
            if self.count_goal % 4 == 0:
                self.vel_x = self.vel_init
                self.vel_y = self.vel_init
                self.x = 200
                self.y = 150
            if self.count_goal % 4 == 1:
                self.vel_x = -self.vel_init
                self.vel_y = self.vel_init
                self.x = 300
                self.y = 150
            if self.count_goal % 4 == 2:
                self.vel_x = self.vel_init
                self.vel_y = -self.vel_init
                self.x = 200
                self.y = 350
            else:
                self.vel_x = -self.vel_init
                self.vel_y = -self.vel_init
                self.x = 300
                self.y = 350
            self.count_goal += 1
            rkt1.get_pos(250)
            rkt2.get_pos(250)

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


# players
rkt1 = Racket(60, 6, 180, light_green) # player 1
rkt2 = Racket(60, 6, 180, light_red, 70, score_pos=(20, 260)) # player 2 or bot

ball = Balls(5, (255, 255, 0), 9, 100, 300)


# change selected or non selected button color
def button_light(button, x, y, cor, largura=150, altura=50, word_size=30):
    pg.draw.rect(win, cor, (x, y, largura, altura))
    font = pg.font.SysFont("comicsans", 40)
    text = font.render(button.text, 1, (255, 255, 255))
    win.blit(text, (x + round(largura / 2) - round(text.get_width() / 2),
                    y + round(altura / 2) - round(text.get_height() / 2)))
    pg.display.update()


# (almost) all ball actions in one functions
def ball_actions():
    global goals_round
    rkt1.draw(win)
    rkt2.draw(win)

    ball.rkt_collision()
    if goals_round != rkt1.score and goals_round != rkt2.score:
        ball.scoring()
        ball.draw()
        ball.move()


# draw when someone score
def score_break():
    font = pg.font.SysFont('fixedsys', 80)
    go = font.render("GOAAAAL", 1, pink)
    win.blit(go, [120, 200])
    pg.display.update()
    pg.time.delay(400)

    win.blit(back, [0, 0])
    ball.draw()
    rkt1.draw(win)
    rkt2.draw(win)
    pg.display.update()
    pg.time.delay(500)

    go = font.render("GO", 1, pink)
    win.blit(go, [210, 250])
    pg.display.update()

    pg.time.delay(500)


# first screen
def menu():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(60)
        win.blit(back1, [0, 0])

        font = pg.font.Font(None, 15)
        develop = font.render("Developed by Roberto 'BeTToH' Branco", True, pink)
        win.blit(develop, [300, 620])

        font = pg.font.SysFont("comicsans", 45)

        title_1 = font.render("Robert's", 1, pink)
        win.blit(title_1, (80, 130))

        font = pg.font.SysFont("arial black", 55)
        title_2 = font.render("Pong Game", 1,light_blue)
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


def selection_screen():
    win.blit(back, [0, 0])

    font = pg.font.SysFont('fixedsys', 40)
    players_text = font.render('PLAYERS:', 2, white)
    win.blit(players_text, [50, 50])

    player1 = Buttons('1 Player', 50, 100, dark_green)
    player2 = Buttons('2 Players', 50, 200, dark_red)
    player1.draw(win)
    player2.draw(win)

    goals = font.render('Goals to Win:', 2, white)
    win.blit(goals, [270, 50])

    x_ax = 290
    five = Buttons('5 Goals', x_ax, 100, dark_green)
    seven = Buttons('7 Goals', x_ax, 170, dark_red)
    ten = Buttons('10 Goals', x_ax, 240, dark_yellow)
    five.draw(win)
    seven.draw(win)
    ten.draw(win)

    txt = font.render('DIFFICULTY:', 3, white)
    win.blit(txt, [50, 320])
    easy = Buttons('Normal', 50, 380, dark_green)
    normal = Buttons('Hard', 50, 450, dark_blue)
    hard = Buttons('Impossible', 50, 520, dark_red)
    easy.draw(win)
    normal.draw(win)
    hard.draw(win)

    next_ = Buttons('Next ->', x_ax, 550, pink)

    pg.display.update()

    aux = 0
    run = True
    while run:
        global players, goals_round, difficulty
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if player1.click(pos):
                    button_light(player1, 50, 100, light_green)
                    players = 1
                    aux += 1

                if player2.click(pos):
                    button_light(player2, 50, 200, light_red)
                    players = 2
                    aux += 1

                if five.click(pos):
                    button_light(five, x_ax, 100, light_green)
                    goals_round = 5
                    aux += 1

                if seven.click(pos):
                    button_light(seven, x_ax, 170, light_red)
                    goals_round = 7
                    aux += 1

                if ten.click(pos):
                    button_light(ten, x_ax, 240, (220, 220, 0))
                    goals_round = 10
                    aux += 1

                if easy.click(pos):
                    button_light(easy, 50, 380, light_green)
                    difficulty = 0

                if normal.click(pos):
                    button_light(normal, 50, 450, light_blue)
                    difficulty = 1

                if hard.click(pos):
                    button_light(hard, 50, 520, light_red)
                    difficulty = 2

                if next_.click(pos) and aux >= 2:
                    run = False

        # change the buttons colors
        if aux >= 2:
            next_.draw(win)

        if players == 1:
            button_light(player2, 50, 200, dark_red)
        else:
            button_light(player1, 50, 100, dark_green)

        if goals_round == 5:
            button_light(seven, x_ax, 170, dark_red)
            button_light(ten, x_ax, 240, dark_yellow)
        elif goals_round == 7:
            button_light(five, x_ax, 100, dark_green)
            button_light(ten, x_ax, 240, dark_yellow)
        elif goals_round == 10:
            button_light(seven, x_ax, 170, dark_red)
            button_light(five, x_ax, 100, dark_green)

        if difficulty == 0:
            button_light(normal, 50, 450, dark_blue)
            button_light(hard, 50, 520, dark_red)
        elif difficulty == 1:
            button_light(easy, 50, 380, dark_green)
            button_light(hard, 50, 520, dark_red)
        elif difficulty == 2:
            button_light(easy, 50, 380, dark_green)
            button_light(normal, 50, 450, dark_blue)

        pg.display.update()


# screen when the game ends
def restart():
    win.blit(back, [0, 0])
    font = pg.font.SysFont('fixedsys', 80)

    if rkt1.score > rkt2.score:
        winner = 'Player 1 won'
    else:
        winner = 'Player 2 won'

    txt = font.render(winner, 2, pink)
    win.blit(txt, [75, 200])
    pg.display.update()

    pg.time.delay(900)

    restart_btn = Buttons('Restart', 70, 400, light_green)
    exit_ = Buttons('Exit', 280, 400, light_red)
    restart_btn.draw(win)
    exit_.draw(win)
    pg.display.update()

    pg.time.delay(700)
    options = Buttons("Options", 175, 500, pink)
    options.draw(win)
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
                    rkt1.score = 0
                    rkt2.score = 0
                    main()
                    run = False
                if exit_.click(pos):
                    run = False
                if options.click(pos):
                    rkt1.score = 0
                    rkt2.score = 0
                    selection_screen()
                    main()
                    run = False


# run the game
tempo = 0 # time resets when someone score
def main():
    global bot_vel, players, goals_round, difficulty
    clock = pg.time.Clock()
    lastKey1 = -1
    lastKey2 = -1

    ball.vel_y = 8
    ball.vel_x = 7

    if difficulty == 0:
        bot_vel = 9
    elif difficulty == 1:
        bot_vel = 11
    elif difficulty == 2: # isso n muda nada
        bot_vel = 18

    win.blit(back, [0, 0])

    font = pg.font.SysFont('fixedsys', 60)
    for i in reversed(range(1, 4)):
        num = font.render(str(i), 4, purple)
        win.blit(num, [240, 230])
        pg.display.update()
        pg.time.delay(700)
        win.blit(back, [0, 0])
        pg.display.update()
        pg.time.delay(300)

    text = font.render('GO', 3, pink)
    win.blit(text, [215, 230])
    pg.display.update()
    pg.time.delay(300)

    win.blit(back, [0, 0])
    pg.display.update()

    run = True
    while run:
        global tempo
        tempo += 50/1000

        win.blit(back, [0, 0])

        clock.tick(30)

        ball_actions()

        for event in pg.event.get():
            pg.key.get_pressed()

            if event.type == pg.QUIT:
                pg.quit()
                run = False

            if event.type == pg.KEYDOWN:
                # player 1 moves
                if event.key == pg.K_LEFT:
                    rkt1.move(0)
                    lastKey1 = 0
                if event.key == pg.K_RIGHT:
                    rkt1.move(1)
                    lastKey1 = 1

                # player 2 moves
                if event.key == pg.K_a:
                    rkt2.move(0)
                    lastKey2 = 0
                if event.key == pg.K_d:
                    rkt2.move(1)
                    lastKey2 = 1

            # stop the racket move
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and lastKey1 == 0:
                    lastKey1 = -1
                if event.key == pg.K_RIGHT and lastKey1 == 1:
                    lastKey1 = -1

                if players == 2:
                    if event.key == pg.K_a and lastKey2 == 0:
                        lastKey2 = -1
                    if event.key == pg.K_d and lastKey2 == 1:
                        lastKey2 = -1

        if lastKey1 == 0:
            rkt1.move(0)
        if lastKey1 == 1:
            rkt1.move(1)

        if lastKey2 == 0:
            rkt2.move(0)
        if lastKey2 == 1:
            rkt2.move(1)

        # bot action
        if players == 1:
            bot_speed = bot_vel
            d = 500

            bot_pos = rkt2.return_pos()

            ball_pos_x, ball_pos_y = ball.return_pos()

            if ball_pos_y <= d:
                if difficulty == 2:
                    if bot_pos > 633 - 30:
                        rkt2.get_pos(633 - 30)
                    elif bot_pos < 30:
                        rkt2.get_pos(30)
                    else:
                        rkt2.get_pos(ball_pos_x)
                else:
                    if bot_pos > 633 - 30:
                        rkt2.get_pos(633 - 30)
                    elif bot_pos < 30:
                        rkt2.get_pos(30)

                    if ball_pos_y - rkt1.pos_y <= 10:
                        if bot_pos > ball_pos_x:
                            rkt2.get_pos(bot_pos - bot_speed)
                        elif bot_pos < ball_pos_x:
                            rkt2.get_pos(bot_pos + bot_speed)
                    else:
                        if bot_pos > ball_pos_x:
                            rkt2.get_pos(bot_pos - bot_speed)
                        elif bot_pos < ball_pos_x:
                            rkt2.get_pos(bot_pos + bot_speed)

        if rkt1.score == goals_round or rkt2.score == goals_round:
            restart()
            run = False

        pg.display.update()


# credits screen
def bye():
    run = True

    clock = pg.time.Clock()
    font = pg.font.Font(None, 120)
    orig_surf = font.render("Robert's", True, purple)
    txt_surf = orig_surf.copy()

    font2 = pg.font.Font(None, 60)
    surf2 = font2.render("Production", True, dark_red)
    txt_surf2 = surf2.copy()
    timer = 20
    alpha = 255
    pg.time.delay(900)
    count = 0
    font3 = pg.font.Font(None, 30)
    surf3 = font3.render("Developing Games since 2020", True, dark_blue)
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

        win.fill(black)
        win.blit(txt_surf, (80, 150))
        win.blit(txt_surf2, (120, 235))
        win.blit(txt_surf3, (85, 460))
        pg.display.update()
        clock.tick(22)

        if count == 130:
            pg.time.delay(70)
            pg.quit()


menu()
selection_screen()
main()
bye()




