import pygame as pg
from pong import Pong
from screens import IntroScreen, ConfigScreen, CreditsScreen

width = 500
height = 633


def main():
    pg.init()
    pg.font.init()
    win = pg.display.set_mode((width, height))
    pg.display.set_caption("Robert's Pong Game")
    IntroScreen().display(win)
    config_screen = ConfigScreen(win)
    config_screen.display()
    while True:
        pong = Pong(win, config_screen.players, config_screen.goals_to_win, config_screen.difficulty)
        pong.run_match()
        next_screen = pong.restart()
        if next_screen == 1:
            ConfigScreen(win).display()
        if next_screen == -1:
            break

    CreditsScreen().display(win)


if __name__ == "__main__":
    main()
