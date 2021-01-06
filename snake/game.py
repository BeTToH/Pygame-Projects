import pygame as pg
import random

pg.init()

largura = 900
altura = 720

icon = pg.image.load('imgs/king.png')

win = pg.display.set_mode((largura, altura))
pg.display.set_caption("Robert's Snake Game")
pg.display.set_icon(icon)

# cores
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

# moves
right = 1
left = -1
up = -2
down = 2

# tamanho de cada cubo
size = 20

difficulty = 0

# carrega umas paradas
button_sound = pg.mixer.Sound('sounds/button_pressed.wav')
eat_sound = pg.mixer.Sound('sounds/eat.wav')
lost_sound = pg.mixer.Sound('sounds/lost.wav')
lost_sound.set_volume(0.2)

pao_img = pg.image.load('imgs/pao.png')
apple_img = pg.image.load('imgs/apple.png')


class Buttons():
    def __init__(self, text, x, y, color, width, height=50):
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
            button_sound.play()
            pg.time.delay(700)
            return True
        else:
            return False


def menu():
    run = True
    clock = pg.time.Clock()

    pg.mixer.music.load('sounds/music.mp3')
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.1)

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))

        font = pg.font.Font(None, 20)
        develop = font.render("Developed by Roberto 'BeTToH' Branco", True, pink)
        win.blit(develop, [1000, 660])

        font = pg.font.SysFont("comicsans", 50)

        title_1 = font.render("Robert's", 1, (150, 0, 160))
        win.blit(title_1, (220, 150))

        font = pg.font.SysFont("arial black", 60)
        title_2 = font.render("Snake Game", 1, dark_green)
        win.blit(title_2, (220, 190))

        pg.display.update()

        font = pg.font.SysFont("comicsans", 50)
        pg.time.delay(800)
        play = font.render('Click to Play', 1, (255, 0, 0))
        win.blit(play, (320, 500))
        pg.display.update()
        pg.time.delay(800)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                run = False


def select_screen():
    win.fill(black)
    pg.display.update()
    pg.time.delay(300)

    font = pg.font.SysFont('timesnewroman', 40)
    pg.draw.rect(win, (125, 125, 125), (260, 85, 320, 500))
    text = font.render("Select Difficulty:", 3, white)
    win.blit(text, [280, 100])
    pg.display.update()

    easy = Buttons("Easy", 320, 190, light_green, 200, 80)
    medium = Buttons("Normal", 320, 290, dark_green, 200, 80)
    hard = Buttons("Hard", 320, 390, dark_blue, 200, 80)
    impossible = Buttons("Impossible", 320, 490, dark_red, 200, 80)
    easy.draw(win)
    medium.draw(win)
    hard.draw(win)
    impossible.draw(win)
    pg.display.update()

    global difficulty
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if easy.click(pos):
                    difficulty = 6
                    run = False

                if medium.click(pos):
                    difficulty = 9
                    run = False

                if hard.click(pos):
                    difficulty = 12
                    run = False

                if impossible.click(pos):
                    difficulty = 20
                    run = False
    main()


def draw_score(score):
    font = pg.font.SysFont('verdana', 30)
    score = font.render('Score:' + str(score), 1, pink)
    win.blit(score, [5, 10])


def main():
    clock = pg.time.Clock()

    win.fill(black)

    snake_pos = [(370, 340), (350, 340), (330, 340), (310, 340)]
    snake_cube = pg.Surface((size, size))
    snake_cube.fill(dark_green)

    move = right

    random_sort = (random.randint(0, 710), random.randint(0, 710))
    food_pos = random_sort
    food = pg.Surface((size, size))
    food.fill(light_red)

    apple_pao = 0

    if difficulty == 16:
        for i in range(3):
            snake_pos.append((snake_pos[len(snake_pos)-1][0], snake_pos[0][1]))

    font = pg.font.SysFont('verdana', 70)
    for i in reversed(range(1, 4)):
        num = font.render(str(i), 4, dark_red)
        win.blit(num, [430, 230])
        pg.display.update()
        pg.time.delay(700)
        win.fill(black)
        pg.display.update()
        pg.time.delay(300)

    text = font.render('GO', 3, light_red)
    win.blit(text, [400, 230])
    pg.display.update()
    pg.time.delay(300)

    win.fill(black)
    pg.display.update()

    score = 0
    food_count = 0
    run = True
    while run:
        win.fill(black)
        clock. tick(17)

        draw_score(score)
        snake_pos[0] = (snake_pos[0][0] * 10 // 10, snake_pos[0][1]*10 // 10)

        for event in pg.event.get():
            pg.key.get_pressed()
            if event.type == pg.QUIT:
                pg.quit()
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if not move == right:
                        move = left
                if event.key == pg.K_RIGHT:
                    if not move == left:
                        move = right
                if event.key == pg.K_UP:
                    if not move == down:
                        move = up
                if event.key == pg.K_DOWN:
                    if not move == up:
                        move = down

        # faz o movimento só no ponto de virada
        if move == up:
            snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - size)
        if move == down:
            snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + size)
        if move == right:
            snake_pos[0] = (snake_pos[0][0] + size, snake_pos[0][1])
        if move == left:
            snake_pos[0] = (snake_pos[0][0] - size, snake_pos[0][1])

        # detecta se comeu e se, aumenta o tamanho
        if snake_pos[0][0] + size >= food_pos[0] >= snake_pos[0][0] - size and snake_pos[0][1] + size >= food_pos[1] >= \
                snake_pos[0][1] - size:
            eat_sound.play()
            pg.time.delay(20)
            food_count = 0
            for i in range(difficulty + 2):
                snake_pos.append((-20, -20))

        # add o novo x,y do cubo, a partir do cubo da frente
        for i in range(len(snake_pos) - 1, 0, -1):
            snake_pos[i] = (snake_pos[i-1][0], snake_pos[i-1][1])

        # verifica se ela comeu a si msm
        for i in range(len(snake_pos) - 1, 1, -1):
            if snake_pos[0] == snake_pos[i]:
                lost_sound.play()
                run = False

        # verifica se saiu do campo
        if not 899 > snake_pos[0][0] > 1 or not 719 > snake_pos[0][1] > 1:
            lost_sound.play()
            run = False

        # se comeu, gera uma nova posição e pontua
        if food_count == 0:
            apple_pao = random.randint(0, 14)
            food_pos = (random.randint(0, 885), random.randint(0, 705))
            for pos in snake_pos:
                while pos == food_pos:
                    food_pos = (((random.randint(0, 885))*10)//10, ((random.randint(0, 705))*10)//10)
            food_count = 1
            if apple_pao != 14:
                score += 10
            else:
                score += 20

        # define se desenha maça ou pao
        if food_count == 1:
            if apple_pao != 14:
                win.blit(pao_img, food_pos)
            else:
                win.blit(apple_img, food_pos)

        # desenha cada cubo da cobra
        for pos in snake_pos:
            win.blit(snake_cube, pos)

        pg.display.update()

    lost()


def lost():
    font = pg.font.SysFont("verdana", 80)
    text = font.render("You Lost!", 1, dark_red)
    win.blit(text, [225, 230])
    pg.display.update()

    pg.time.delay(800)

    again = Buttons("Restart", 200, 490, dark_blue, 150)
    exit = Buttons("Exit", 500, 490, dark_red, 150)
    select = Buttons("Change Difficulty", 300, 600, pink, 250)

    again.draw(win)
    exit.draw(win)
    select.draw(win)
    pg.display.update()

    run = True
    while run:
        pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if again.click(pos):
                    main()
                if exit.click(pos):
                    bye()
                if select.click(pos):
                    select_screen()

def bye():
    run = True
    win.fill(black)

    pg.mixer.music.stop()
    
    font = pg.font.SysFont('times', 30)
    text = font.render("Thx for playing, hope you've enjoyed!", 1, (200, 0, 100))
    win.blit(text, [180, 100])
    pg.display.update()

    clock = pg.time.Clock()
    font = pg.font.Font(None, 120)
    orig_surf = font.render("Robert", True, light_red)
    txt_surf = orig_surf.copy()

    font2 = pg.font.Font(None, 60)
    surf2 = font2.render("Production", True, dark_red)
    txt_surf2 = surf2.copy()
    timer = 20
    alpha = 255
    pg.time.delay(2000)
    count = 0
    font3 = pg.font.Font(None, 30)
    surf3 = font3.render("Developing Fair Games since 2020", True, dark_blue)
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

        win.fill((30, 30, 30))
        win.blit(txt_surf, (290, 150))
        win.blit(txt_surf2, (320, 280))
        win.blit(txt_surf3, (250, 460))
        pg.display.update()
        clock.tick(22)

        if count == 130:
            pg.time.delay(100)
            pg.quit()


menu()
select_screen()
main()
bye()

