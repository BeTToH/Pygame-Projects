import pygame
import os
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", 'bird1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", 'bird2.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", 'bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -9.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 14:
            d = 16

        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -80:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -70:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_win(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(210, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    clock = pygame.time.Clock()
    score = 0

    draw_win(win, bird, pipes, base, score)
    font = pygame.font.SysFont('verdana', 50)
    for i in reversed(range(1, 4)):
        num = font.render(str(i), 4, pygame.Color('red'))
        win.blit(num, [230, 230])
        pygame.display.update()
        pygame.time.delay(700)
        draw_win(win, bird, pipes, base, score)
        pygame.display.update()
        pygame.time.delay(300)

    text = font.render('GO', 3, pygame.Color('red'))
    win.blit(text, [210, 230])
    pygame.display.update()
    pygame.time.delay(300)

    run = True
    while run:
        clock.tick(28)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # player 1 moves
                if event.key == pygame.K_SPACE:
                    bird.jump()

        lixo = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                run = False

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True    
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                lixo.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(550))

        for p in lixo:
            pipes.remove(p)

    
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False   

        bird.move()
        base.move()
        draw_win(win, bird, pipes, base, score)

        #if score > 20:
            #break


def menu():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.blit(BG_IMG, (0, 0))

        font = pygame.font.Font(None, 10)
        develop = font.render("Developed by Roberto 'BeTToH' Branco", True, (0, 255, 0))
        win.blit(develop, [500, 700])

        font = pygame.font.SysFont("comicsans", 40)

        title_1 = font.render("Robert's", 1, (150, 0, 160))
        win.blit(title_1, (70, 150))

        font = pygame.font.SysFont("arial black", 60)
        title_2 = font.render("Flappy Bird", 1, pygame.Color('green'))
        win.blit(title_2, (70, 190))

        pygame.display.update()

        font = pygame.font.SysFont("comicsans", 50)
        pygame.time.delay(800)
        play = font.render('Click to Play', 1, (255, 0, 0))
        win.blit(play, (150, 500))
        pygame.display.update()
        pygame.time.delay(800)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False


def lost():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        font = pygame.font.Font(None, 10)
        develop = font.render("Developed by Roberto 'BeTToH' Branco", True, (0, 255, 0))
        win.blit(develop, [500, 700])

        font = pygame.font.SysFont("comicsans", 40)

        font = pygame.font.SysFont("arial black", 60)
        title_2 = font.render("You Lost!", 1, pygame.Color('red'))
        win.blit(title_2, (80, 190))

        pygame.display.update()

        font = pygame.font.SysFont("comicsans", 50)
        pygame.time.delay(800)
        play = font.render('Click to Play Again', 1, (255, 0, 0))
        win.blit(play, (100, 500))
        pygame.display.update()
        pygame.time.delay(800)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

menu()
main()
lost()