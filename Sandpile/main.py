import pygame as pg
from copy import deepcopy
from math import floor


class App:

    def __init__(self, screen_width=1000, screen_height=700, tile_size=10, fps=60, speed=1):

        pg.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

        self.is_grid = False

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True

        self.tile_size = tile_size
        self.rows, self.columns = screen_height // tile_size, screen_width // tile_size

        self.next_field = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.current_field = [[0 for i in range(self.columns)] for j in range(self.rows)]

    def generate_grid(self):
        [pg.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.screen_height), 1) for x in
         range(0, self.screen_width, self.tile_size)]
        [pg.draw.line(self.screen, (30, 30, 30), (0, y), (self.screen_width, y), 1) for y in
         range(0, self.screen_height, self.tile_size)]

    def get_cords(self, pos):
        x, y = pos
        x = floor(x/self.screen_width*self.columns)
        y = floor(y/self.screen_height*self.rows)
        return x, y

    def drop(self, x, y):
        self.next_field[y][x] -= 4
        self.next_field[y][x+1] += 1
        self.next_field[y][x-1] += 1
        self.next_field[y+1][x] += 1
        self.next_field[y-1][x] += 1

    def drop_fast(self, x, y):
        delta = self.current_field[y][x] // 4
        new = self.current_field[y][x] % 4
        self.next_field[y][x] = new
        self.next_field[y][x+1] += delta
        self.next_field[y][x-1] += delta
        self.next_field[y+1][x] += delta
        self.next_field[y-1][x] += delta

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
                        self.next_field[y][x] += 1
                    elif event.button == 3:
                        self.running = not self.running

            # draw life
            for x in range(1, self.columns - 1):
                for y in range(1, self.rows - 1):
                    color = 'black'
                    if self.current_field[y][x] == 1:
                        color = 'yellow'
                    if self.current_field[y][x] == 2:
                        color = 'orange'
                    if self.current_field[y][x] == 3:
                        color = 'red'
                    if self.current_field[y][x] >= 4:
                        color = 'violet'
                        if (self.time % self.speed) == 0 and self.running:
                            if fast:
                                self.drop_fast(x, y)
                            else:
                                self.drop(x, y)

                    size = self.tile_size
                    delta = 2 if self.is_grid else 0
                    pg.draw.rect(self.screen, color, (x * size + delta, y * size + delta, size - delta, size - delta))

            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


app = App(speed=1)
# app.current_field[app.rows // 2][app.columns // 2] = 10 ** 9
for delta in range(app.columns // 2): app.current_field[app.rows // 2][app.columns // 4 + delta] = 10 ** 6
app.run(fast=False)
