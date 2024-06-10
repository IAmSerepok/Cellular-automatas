import pygame as pg
from random import randint
from copy import deepcopy


class App:

    def __init__(self, screen_width=1400, screen_height=700, tile_size=8, fps=60, random_field=False):

        pg.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

        self.FPS = fps
        self.speed = 1
        self.time = 0
        self.running = True

        self.tile_size = tile_size
        self.rows, self.columns = screen_height // tile_size, screen_width // tile_size

        self.next_field = [[0 for i in range(self.columns)] for j in range(self.rows)]
        if random_field:
            self.current_field = [[randint(0, 2) for i in range(self.columns)] for j in range(self.rows)]
        else:
            self.current_field = [[0 for i in range(self.columns)] for j in range(self.rows)]

    def check_cell(self, color, x, y):
        count = 0
        prev_col = color
        col = (color + 1) % 3
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if self.current_field[j][i] == col:
                    count += 1
        if count >= 3:
            return col
        else:
            return prev_col

    def draw_life(self):
        for x in range(1, self.columns - 1):
            for y in range(1, self.rows - 1):
                if self.current_field[y][x] == 0:
                    color = (160, 90, 170)
                elif self.current_field[y][x] == 1:
                    color = (150, 190, 220)
                else:
                    color = (235, 150, 150)
                size = self.tile_size

                pg.draw.rect(self.screen, color, (x * size, y * size, size, size))

                if ((self.time % self.speed) == 0) and self.running:
                    self.next_field[y][x] = self.check_cell(self.current_field[y][x], x, y)

    def run(self):

        while True:

            self.screen.fill(pg.Color('black'))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.running = not self.running

            self.draw_life()
            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


app = App(random_field=True)
app.run()
