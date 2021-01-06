import random
import pygame as pg

pg.init()
pg.font.init()

# lista do q falta:
#  destuir em cruz
#  printar o tempo do round na lateral


largura = 600
altura = 550
win = pg.display.set_mode((largura, altura))

# global vars

difficulty = 0

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

blocos = []
for bloco in range(6):
    sized_bloco = pg.image.load(f'img/blocos/bloco{bloco}.png')
    sized_bloco = pg.transform.scale(sized_bloco, (50, 50))
    blocos.append(sized_bloco)


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


class Field():
    def __init__(self, largura, altura, blockSize, blocos):
        self.largura = largura - 200
        self.altura = altura
        self.blockSize = blockSize
        self.blocos = blocos
        self.map = [[5 for col in range(largura // 50)] for row in range(altura // 50)]
        self.score = 0

    def init_map(self):
        for row in range(4):
            for col in range(self.largura // self.blockSize):
                self.map[row][col] = random.randint(0, 4)

                try:
                    while self.map[row][col] == self.map[row - 1][col] or self.map[row][col] == self.map[row][col - 1]:
                        self.map[row][col] = random.randint(0, 4)
                except:
                    pass

    def redraw_map(self, win):
        for row in range(altura // self.blockSize):
            for col in range(self.largura // self.blockSize):
                blc = self.map[row][col]

                # se for a nova linha( pq a nova linha recebe -1)
                if blc == -1:
                    blc = random.randint(0, 4)
                    self.map[row][col] = blc
                    try:
                        while (self.map[0][col] == self.map[0][col - 1] and self.map[0][col] == self.map[0][col - 2]) or \
                                (self.map[0][col] == self.map[2][col] and self.map[2][col] == self.map[1][col]):
                            blc = random.randint(0, 4)
                            self.map[row][col] = blc

                    except:
                        while self.map[0][col] == self.map[2][col] and self.map[2][col] == self.map[1][col]:
                            blc = random.randint(0, 4)
                            self.map[row][col] = blc

                win.blit(self.blocos[blc], [self.blockSize * col, self.altura - self.blockSize * (row + 1)])

        pg.draw.rect(win, pg.Color('red'), (0, 45, 400, 5))

        self.repos()

        self.draw_side()

    def create_new_line(self):
        for row in reversed(range(altura // 50)):
            for col in range(self.largura // 50):
                if row == 0:
                    self.map[row][col] = -1  # (nova linha)
                else:
                    self.map[row][col] = self.map[row - 1][col]
        player.repos()

    def lose(self):
        for col in range(largura // self.blockSize):
            if self.map[10][col] != 5:
                return 1
        return 0

    def change_block(self, x, y):
        aux = self.map[x][y]
        self.map[x][y] = self.map[x][y + 1]
        self.map[x][y + 1] = aux

    def destroy(self):
        for row in range(altura // self.blockSize):
            seq_col = 1
            for col in range(self.largura // self.blockSize):
                if row == 0:
                    seq = 1
                    for i in range(self.altura // self.blockSize - 1):
                        if self.map[i][col] == self.map[i + 1][col] and self.map[i][col] != 5 and self.map[i][col] != -1:
                            seq += 1
                        else:
                            if seq >= 3:
                                for j in range(seq):
                                    self.map[i - j][col] = 5

                                self.score += 25 * (seq - 1)
                            seq = 1

                if col < 7:
                    if self.map[row][col] != -1 and self.map[row][col] != 5 and self.map[row][col] == self.map[row][col + 1]:
                        seq_col += 1

                    else:
                        if seq_col >= 3:
                            for j in range(seq_col):
                                self.map[row][col - j] = 5

                            self.score += 25 * (seq_col - 1)
                        seq_col = 1

                if col == 7:
                    if seq_col >= 3:
                        for j in range(seq_col):
                            self.map[row][col - j] = 5
                            self.score += 25 * (seq_col - 1)

    # faz o bloco cair se estiver vazio abaixo dele
    def repos(self):
        for row in reversed(range(altura // self.blockSize)):
            for col in range(largura // self.blockSize):
                if self.map[row][col] == 5 and row < 10:
                    self.map[row][col] = self.map[row + 1][col]
                    self.map[row + 1][col] = 5

    def draw_score(self):
        font = pg.font.SysFont('fixedsys', 45)
        score_txt = font.render('Score: ' + str(self.score), 3, pg.Color('red'))
        win.blit(score_txt, [self.largura + 20, 30])

    def draw_side(self):

        pg.draw.rect(win, pg.Color('gray'), (400, 0, 200, 550))
        global difficulty

        font = pg.font.SysFont('fixedsys', 35)

        if difficulty == 4:
            diff_txt = 'HARD'

        elif difficulty == 5:
            diff_txt = 'NORMAL'

        elif difficulty == 6:
            diff_txt = 'EASY'

        txt = font.render('Difficulty: ', 1, pg.Color('black'))
        txt2 = font.render(diff_txt, 1, pg.Color('blue'))
        win.blit(txt, [self.largura + 30, 100])
        win.blit(txt2, [self.largura + 50, 140])
        self.draw_score()


mapa = Field(largura, altura, 50, blocos)


class Grade():
    def __init__(self, x, y, blockSize, img):
        self.blockSize = blockSize
        self.img = img
        self.x = x
        self.y = y

    def move(self, lado):
        if lado == 1 and self.x < 6:
            self.x += 1  # move right
        if lado == -1 and self.x > 0:
            self.x -= 1  # move left
        if lado == 2 and self.y < 9:
            self.y += 1  # move up
        if lado == -2 and self.y > 0:
            self.y -= 1  # move down

    def draw(self, win):
        win.blit(self.img, [self.x * self.blockSize, altura - (self.y + 1) * self.blockSize])
        win.blit(self.img, [(self.x + 1) * self.blockSize, altura - (self.y + 1) * self.blockSize])

    def action(self):
        mapa.change_block(self.y, self.x)

    def repos(self):
        self.y += 1

grade_img = pg.image.load('img/grade0.png')
grade_img = pg.transform.scale(grade_img, (50, 50))
player = Grade(3, 3, 50, grade_img)


# change selected or non selected button color
def button_light(button, x, y, cor, largura=150, altura=50, word_size=30):
    pg.draw.rect(win, cor, (x, y, largura, altura))
    font = pg.font.SysFont("comicsans", 40)
    text = font.render(button.text, 1, (255, 255, 255))
    win.blit(text, (x + round(largura / 2) - round(text.get_width() / 2),
                    y + round(altura / 2) - round(text.get_height() / 2)))
    pg.display.update()


def selection_screen():
    win.fill(black)

    font = pg.font.SysFont('fixedsys', 40)
    #players_text = font.render('PLAYERS:', 2, white)
    #win.blit(players_text, [50, 50])

    #player1 = Buttons('1 Player', 50, 100, dark_green)
    #player2 = Buttons('2 Players', 50, 200, dark_red)
    #player1.draw(win)
    #player2.draw(win)

    alt = 120
    alt1 = 180
    alt2 = 260
    alt3 = 340

    x1 = 200

    txt = font.render('DIFFICULTY:', 3, white)
    win.blit(txt, [190, alt])

    easy = Buttons('Easy', x1, alt1, dark_green)
    normal = Buttons('Normal', x1, alt2, dark_blue)
    hard = Buttons('Hard', x1, alt3, dark_red)
    easy.draw(win)
    normal.draw(win)
    hard.draw(win)

    next_ = Buttons('Next ->', 400, 450, pink)

    pg.display.update()

    aux = 0
    run = True
    while run:
        global difficulty
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                '''if player1.click(pos):
                    button_light(player1, 50, 100, light_green)
                    players = 1
                    aux += 1

                if player2.click(pos):
                    button_light(player2, 50, 200, light_red)
                    players = 2
                    aux += 1'''

                if easy.click(pos):
                    button_light(easy, x1, alt1, light_green)
                    difficulty = 6
                    aux = 1

                if normal.click(pos):
                    button_light(normal, x1, alt2, light_blue)
                    difficulty = 5
                    aux = 1

                if hard.click(pos):
                    button_light(hard, x1, alt3, light_red)
                    difficulty = 4
                    aux = 1

                if next_.click(pos) and aux == 1:
                    run = False

        # change the buttons colors
        if aux == 1:
            next_.draw(win)

        '''if players == 1:
            button_light(player2, 50, 200, dark_red)
        else:
            button_light(player1, 50, 100, dark_green)'''

        if difficulty == 6:
            button_light(normal, x1, alt2, dark_blue)
            button_light(hard, x1, alt3, dark_red)
        elif difficulty == 5:
            button_light(easy, x1, alt1, dark_green)
            button_light(hard, x1, alt3, dark_red)
        elif difficulty == 4:
            button_light(easy, x1, alt1, dark_green)
            button_light(normal, x1, alt2, dark_blue)

        pg.display.update()


def main():
    win.fill(black)
    clock = pg.time.Clock()
    start_ticks = pg.time.get_ticks()
    new_line_timer = start_ticks

    global difficulty

    mapa.init_map()

    run = True
    while run:
        clock.tick(20)

        win.fill(pg.Color('black'))

        for event in pg.event.get():
            pg.key.get_pressed()

            if event.type == pg.QUIT:
                pg.quit()
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.move(-1)
                elif event.key == pg.K_RIGHT:
                    player.move(1)
                elif event.key == pg.K_UP:
                    player.move(2)
                elif event.key == pg.K_DOWN:
                    player.move(-2)
                elif event.key == pg.K_SPACE:
                    player.action()

        secs = (pg.time.get_ticks() - new_line_timer) / 1000

        if secs > difficulty:
            mapa.create_new_line()
            new_line_timer = pg.time.get_ticks()

        mapa.redraw_map(win)
        mapa.destroy()

        player.draw(win)
        pg.time.delay(50)
        pg.display.update()

        if mapa.lose() == 1:
            lost()
            break


# screen when the game ends
def lost():
    # reseta o jogo
    mapa.score = 0
    mapa.map = [[5 for col in range(largura // 50)] for row in range(altura // 50)]
    player.x = 3
    player.y = 3

    # desenha a tela de derrota
    font = pg.font.SysFont('fixedsys', 60)
    txt = font.render('You Lost!', 1, pg.Color('red'))
    win.blit(txt, [405, 220])
    pg.display.flip()

    pg.time.delay(1000)

    restart_btn = Buttons('Restart', 415, 280, light_green)
    exit_ = Buttons('Exit', 415, 360, light_red)
    restart_btn.draw(win)
    exit_.draw(win)
    pg.display.update()

    pg.time.delay(700)
    options = Buttons("Options", 415, 440, pink)
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
                    main()
                    run = False
                if exit_.click(pos):
                    run = False
                if options.click(pos):
                    selection_screen()
                    main()
                    run = False


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


selection_screen()
main()
bye()
