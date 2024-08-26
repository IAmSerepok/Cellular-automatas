import pygame as pg
import numpy as np

from random import random
from copy import deepcopy
from colorsys import hsv_to_rgb
from numba import prange

from general.neighborhood import neighborhood_funcs


class App:
    def __init__(
            self, columns=200, rows=200, tile_size=3,
            fps=60, random_field=False, probability=0.5, speed=2,
            cmap=None
    ):
        pg.init()

        self.cmap = cmap
        self.rows, self.columns = rows, columns
        self.tile_size = tile_size
        self.screen = pg.display.set_mode([self.columns * self.tile_size, self.rows * self.tile_size])
        self.clock = pg.time.Clock()
        self.rule_b, self.rule_s, self.generations = None, None, None

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True
        self.colors = None

        self.next_field = np.zeros((self.columns + 2, self.rows + 2), dtype=int)
        self.current_field = np.zeros((self.columns + 2, self.rows + 2), dtype=int)
        if random_field:
            for x in prange(1, self.columns + 1):
                for y in prange(1, self.rows + 1):
                    if random() < probability:
                        self.current_field[x, y] = 1

    def check_cell(self, current_field_, x, y):
        count = neighborhood_funcs['M'](current_field_, x, y, 1, 1)

        val = current_field_[x, y]
        if val == 1:
            if count in self.rule_s:
                return 1
            return (val + 1) % self.generations
        elif current_field_[x, y] == 0:
            if count in self.rule_b:
                return 1
            return 0
        else:
            return (val + 1) % self.generations

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.rows * self.tile_size), 1)
             for x in prange(0, self.columns * self.tile_size, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.columns * self.tile_size, y), 1)
             for y in prange(0, self.rows * self.tile_size, self.tile_size)]

    def set_rules(self, birth, survival, generations):
        self.rule_b = birth
        self.rule_s = survival
        self.generations = generations

    def generate_colors(self):
        if self.cmap is None:
            self.colors = [(0, 0, 0)] * (self.generations - 1) + [(255, 255, 255)]
            return
        start_color, end_color = self.cmap
        colors = []
        h0, s0, v0 = start_color
        h1, s1, v1 = end_color
        n = self.generations - 1
        for _1 in prange(n + 1):
            r, g, b = (hsv_to_rgb(h0 + (h1 - h0) * _1 / n,
                                  s0 + (s1 - s0) * _1 / n,
                                  v0 + (v1 - v0) * _1 / n))
            colors.append((255 * r, 255 * g, 255 * b))
        self.colors = colors

    def draw_life(self, grid_visible):
        for x in prange(1, self.columns + 1):
            for y in prange(1, self.rows + 1):
                size = self.tile_size
                if grid_visible:
                    pg.draw.rect(self.screen, self.colors[self.current_field[x, y] - 1],
                                 ((x - 1) * size + 2, (y - 1) * size + 2, size - 2, size - 2))
                else:
                    pg.draw.rect(self.screen, self.colors[self.current_field[x, y] - 1],
                                 ((x - 1) * size, (y - 1) * size, size, size))
                if ((self.time % self.speed) == 0) and self.running:
                    self.next_field[x, y] = self.check_cell(self.current_field, x, y)

    def run(self, grid_visible):
        self.generate_colors()

        while True:
            self.screen.fill(pg.Color('black'))
            self.generate_grid(grid_visible)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.running = not self.running

            self.draw_life(grid_visible)
            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = App(random_field=True, probability=0.5, speed=1,
              cmap=[(358/360, 1.0, 0.4), (50/360, 0.0, 1.0)])
    app.set_rules([2], [2], 25)
    app.run(grid_visible=False)
