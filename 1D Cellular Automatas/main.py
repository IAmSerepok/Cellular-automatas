import pygame as pg
import numpy as np

from random import randint, randrange
from numba import prange
from copy import deepcopy


class App:
    def __init__(self, columns=600, rows=300, tile_size=2, fps=60, speed=1, random_field=False):
        pg.init()

        self.rows, self.columns = rows, columns
        self.screen = pg.display.set_mode([columns * tile_size, rows * tile_size])
        self.clock = pg.time.Clock()
        self.rules = {}

        self.FPS = fps

        self.speed = speed
        self.time = 0
        self.depth = 1
        self.running = True

        self.color = self.get_random_color()
        self.tile_size = tile_size

        self.current_field = self.next_field = np.zeros((self.columns, self.rows), dtype=int)
        if random_field:
            for x in prange(self.columns):
                self.current_field[x, 1] = randint(0, 1)

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def set_rule(self, rule):
        numb = rule
        rules = dict()
        for i in prange(8):
            value = numb % 2
            numb = numb // 2
            rules[i] = value

        self.rules = rules

    def check_cell(self, x, y):
        a, b, c = x - 1, x, x + 1

        a = self.columns - 1 if a == -1 else a
        c = 0 if c == self.columns else c

        s = ""
        s += str(self.current_field[a, y])
        s += str(self.current_field[b, y])
        s += str(self.current_field[c, y])

        return self.rules[int(s, 2)]

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.rows * self.tile_size), 1)
             for x in range(0, self.columns * self.tile_size, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.columns * self.tile_size, y), 1)
             for y in range(0, self.rows * self.tile_size, self.tile_size)]

    def run(self, grid_visible):
        while True:
            self.screen.fill(pg.Color('black'))
            self.generate_grid(grid_visible)

            self.next_field = deepcopy(self.current_field)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.running = not self.running

            # draw life
            for x in prange(self.columns):
                for y in prange(1, self.rows - 1):
                    if self.current_field[x, y]:
                        size = self.tile_size
                        if grid_visible:
                            pg.draw.rect(self.screen, self.color, (x * size + 2, y * size + 2, size - 2, size - 2))
                        else:
                            pg.draw.rect(self.screen, self.color, (x * size, y * size, size, size))

                    if ((self.time % self.speed) == 0) and self.running and (y == self.depth):
                        if self.depth < self.rows:
                            self.next_field[x, y + 1] = self.check_cell(x, y)

            if (self.depth >= self.rows) and ((self.time % self.speed) == 0) and self.running:
                for i in prange(self.columns):
                    for j in prange(1, self.rows - 2):
                        self.next_field[i, j] = self.current_field[i, j + 1]

                for i in prange(self.columns):
                    self.next_field[i, self.rows - 2] = self.check_cell(i, self.rows - 2)

            self.current_field = deepcopy(self.next_field)

            pg.display.flip()
            if ((self.time % self.speed) == 0) and self.running:
                self.depth += 1
            self.time += 1
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = App(random_field=True, speed=1)
    app.set_rule(184)
    # app.current_field[1][app.columns//2] = 1
    app.run(grid_visible=False)
