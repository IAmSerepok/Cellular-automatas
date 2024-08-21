import pygame as pg
import numpy as np

from copy import deepcopy
from math import ceil
from numba import prange


class App:
    def __init__(self, columns=50, rows=50, tile_size=14, fps=60, speed=15):
        pg.init()

        self.screen = pg.display.set_mode([columns * tile_size, rows * tile_size])
        self.clock = pg.time.Clock()

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True

        self.tile_size = tile_size
        self.rows, self.columns = rows, columns

        self.next_field = np.zeros((columns + 2, rows + 2), dtype=int)
        self.current_field = np.zeros((columns + 2, rows + 2), dtype=int)

    def generate_grid(self):
        [pg.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.rows * self.tile_size), 1)
         for x in prange(0, self.columns * self.tile_size, self.tile_size)]
        [pg.draw.line(self.screen, (30, 30, 30), (0, y), (self.columns * self.tile_size, y), 1) 
         for y in prange(0, self.rows * self.tile_size, self.tile_size)]

    def get_cords(self, pos):
        x, y = pos
        x = ceil(x / self.tile_size)
        y = ceil(y / self.tile_size)
        return x, y

    def signal(self, x, y):
        if ((self.time % self.speed) == 0) and self.running:
            count = 0
            for j in prange(y - 1, y + 2):
                for i in prange(x - 1, x + 2):
                    if self.current_field[i, j] == 2:
                        count += 1

            if (count == 1) or (count == 2):
                self.next_field[x, y] = 2

    def run(self):
        while True:
            self.screen.fill(pg.Color('black'))
            self.generate_grid()

            self.next_field = deepcopy(self.current_field)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = self.get_cords(event.pos)
                    if event.button == 1:
                        self.next_field[x, y] = (self.current_field[x, y] + 1) % 4
                    elif event.button == 3:
                        self.running = not self.running

            # draw life
            for x in prange(1, self.columns + 1):
                for y in prange(1, self.rows + 1):
                    color = 'black'
                    if self.current_field[x, y] == 1:
                        self.signal(x, y)
                        color = 'yellow'
                    if self.current_field[x, y] == 3:
                        if ((self.time % self.speed) == 0) and self.running:
                            self.next_field[x, y] = 1
                        color = 'red'
                    if self.current_field[x, y] == 2:
                        if ((self.time % self.speed) == 0) and self.running:
                            self.next_field[x, y] = 3
                        color = 'blue'
                    size = self.tile_size

                    pg.draw.rect(self.screen, color, ((x - 1) * size + 2, (y - 1) * size + 2, size - 2, size - 2))

            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = App()
    app.run()
