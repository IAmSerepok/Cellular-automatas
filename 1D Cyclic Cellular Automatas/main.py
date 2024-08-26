import pygame as pg
import numpy as np

from random import randint
from numba import prange
from copy import deepcopy
from colorsys import hsv_to_rgb


class App:
    def __init__(
            self, columns=200, rows=200, tile_size=4, fps=60, speed=1,
            random_field=False, cmap=None
    ):
        pg.init()

        self.rows, self.columns = rows + 1, columns
        self.screen = pg.display.set_mode([columns * tile_size, rows * tile_size])
        self.clock = pg.time.Clock()
        self.rules = {}

        self.FPS = fps

        self.speed = speed
        self.time = 0
        self.depth = 0
        self.running = True
        self.random_field = random_field

        self.cmap = cmap
        self.colors, self.states = None, None
        self.tile_size = tile_size

        self.current_field = self.next_field = np.zeros((self.columns, self.rows + 1), dtype=int)

    def generate_field(self):
        if self.random_field:
            for x in prange(self.columns):
                self.current_field[x, 0] = randint(0, self.states - 1)

    def generate_colors(self):
        if self.cmap is None:
            self.colors = [(0, 0, 0)] * (self.states - 1) + [(255, 255, 255)]
            return
        start_color, end_color = self.cmap
        colors = []
        h0, s0, v0 = start_color
        h1, s1, v1 = end_color
        n = self.states - 1
        for _1 in prange(n + 1):
            r, g, b = (hsv_to_rgb(h0 + (h1 - h0) * _1 / n,
                                  s0 + (s1 - s0) * _1 / n,
                                  v0 + (v1 - v0) * _1 / n))
            colors.append((255 * r, 255 * g, 255 * b))
        self.colors = colors

    def set_rule(self, rule, states):
        numb = rule
        rules = dict()
        for i in prange(8):
            value = numb % 2
            numb = numb // 2
            rules[i] = value

        self.rules = rules
        self.states = states

        self.generate_field()

    def check_cell(self, x, y):
        curr_val = self.current_field[x, y]
        next_val = (curr_val + 1) % self.states

        a, c = x - 1, x + 1

        a = self.columns - 1 if a == -1 else a
        c = 0 if c == self.columns else c

        s = ""

        for state in [self.current_field[a, y], curr_val, self.current_field[c, y]]:
            if state == next_val:
                s += '1'
            else:
                s += '0'

        if self.rules[int(s, 2)]:
            return next_val

        return curr_val

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.rows * self.tile_size), 1)
             for x in range(0, self.columns * self.tile_size, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.columns * self.tile_size, y), 1)
             for y in range(0, self.rows * self.tile_size, self.tile_size)]

    def run(self, grid_visible):
        self.generate_colors()

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
                for y in prange(self.rows):
                    size = self.tile_size
                    color = self.colors[self.current_field[x, y] - 1]

                    if grid_visible:
                        pg.draw.rect(self.screen, color, (x * size + 2, y * size + 2, size - 2, size - 2))
                    else:
                        pg.draw.rect(self.screen, color, (x * size, y * size, size, size))

                    if ((self.time % self.speed) == 0) and self.running and (y == self.depth):
                        if self.depth < self.rows:
                            self.next_field[x, y + 1] = self.check_cell(x, y)

            if (self.depth >= self.rows) and ((self.time % self.speed) == 0) and self.running:
                for i in prange(self.columns):
                    for j in prange(self.rows):
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
    app = App(
        random_field=True, speed=1,
        cmap=[(358/360, 1.0, 0.4), (50/360, 0.0, 1.0)]
        )
    app.set_rule(110, 3)
    # app.current_field[1][app.columns//2] = 1
    app.run(grid_visible=False)
