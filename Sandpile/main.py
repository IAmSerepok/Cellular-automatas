import pygame as pg
import numpy as np

from copy import deepcopy
from math import ceil


class App:
    def __init__(self, columns=250, rows=250, tile_size=3, fps=60, speed=1):
        pg.init()

        self.tile_size = tile_size
        self.rows, self.columns = rows, columns
        self.screen = pg.display.set_mode([columns * tile_size, rows * tile_size])
        self.clock = pg.time.Clock()

        self.is_grid = False

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True

        self.next_field = np.zeros((self.columns + 2, self.rows + 2), dtype=int)
        self.current_field = np.zeros((self.columns + 2, self.rows + 2), dtype=int)

    def generate_grid(self):
        [pg.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.rows * self.tile_size), 1)
         for x in range(0, self.columns * self.tile_size, self.tile_size)]
        [pg.draw.line(self.screen, (30, 30, 30), (0, y), (self.columns * self.tile_size, y), 1)
         for y in range(0, self.rows * self.tile_size, self.tile_size)]

    def get_cords(self, pos):
        x, y = pos
        x = ceil(x / self.tile_size)
        y = ceil(y / self.tile_size)
        return x, y

    def drop(self, x, y):
        self.next_field[x, y] -= 4
        self.next_field[x + 1, y] += 1
        self.next_field[x - 1, y] += 1
        self.next_field[x, y + 1] += 1
        self.next_field[x, y - 1] += 1

    def drop_fast(self, x, y):
        delta = self.current_field[y][x] // 4
        new = self.current_field[y][x] % 4
        self.next_field[x, y] = new
        self.next_field[x + 1, y] += delta
        self.next_field[x - 1, y] += delta
        self.next_field[x, y + 1] += delta
        self.next_field[x, y - 1] += delta

    def run(self, fast):
        while True:
            self.screen.fill(pg.Color('black'))
            if self.is_grid:
                self.generate_grid()

            self.next_field = deepcopy(self.current_field)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = self.get_cords(event.pos)
                    if event.button == 1:
                        self.next_field[x, y] += 1
                    elif event.button == 3:
                        self.running = not self.running

            # draw life
            for x in range(1, self.columns + 1):
                for y in range(1, self.rows + 1):
                    color = 'black'
                    if self.current_field[x, y] == 1:
                        color = 'yellow'
                    if self.current_field[x, y] == 2:
                        color = 'orange'
                    if self.current_field[x, y] == 3:
                        color = 'red'
                    if self.current_field[x, y] >= 4:
                        color = 'violet'
                        if (self.time % self.speed) == 0 and self.running:
                            if fast:
                                self.drop_fast(x, y)
                            else:
                                self.drop(x, y)

                    size = self.tile_size
                    delta = 2 if self.is_grid else 0
                    pg.draw.rect(self.screen, color, ((x - 1) * size + delta, (y - 1) * size + delta, size - delta, size - delta))

            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = App(speed=1)
    # app.current_field[app.rows // 2][app.columns // 2] = 10 ** 9
    for delta in range(app.columns // 2): app.current_field[app.columns // 4 + delta, app.rows // 2] = 10 ** 6
    app.run(fast=False)
