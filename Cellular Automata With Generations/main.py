import pygame as pg
from random import random
from copy import deepcopy
from colorsys import hsv_to_rgb


class App:
    def __init__(
            self, columns=150, rows=150, tile_size=5,
            fps=60, random_field=False, probability=0.5, speed=2,
            cmap=None
    ):
        pg.init()

        self.cmap = cmap

        self.rows, self.columns = rows, columns
        self.screen_width = self.columns * tile_size
        self.screen_height = self.rows * tile_size
        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        self.clock = pg.time.Clock()
        self.rule_b, self.rule_s, self.generations = None, None, None

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True

        self.tile_size = tile_size
        self.colors = None

        self.next_field = [[0 for _1 in range(self.columns + 2)] for _2 in range(self.rows + 2)]
        self.current_field = [[0 for _1 in range(self.columns + 2)] for _2 in range(self.rows + 2)]
        if random_field:
            for x in range(1, self.columns + 1):
                for y in range(1, self.rows + 1):
                    if random() < probability:
                        self.current_field[y][x] = 1

    def check_cell(self, current_field_, x, y):
        count = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if current_field_[j][i] == 1:
                    count += 1

        val = current_field_[y][x]
        if val == 1:
            count -= 1
            if count in self.rule_s:
                return 1
            return (val + 1) % self.generations
        elif current_field_[y][x] == 0:
            if count in self.rule_b:
                return 1
            return 0
        else:
            return (val + 1) % self.generations

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.screen_height), 1) for x in
             range(0, self.screen_width, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.screen_width, y), 1) for y in
             range(0, self.screen_height, self.tile_size)]

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
        for _1 in range(n + 1):
            r, g, b = (hsv_to_rgb(h0 + (h1 - h0) * _1 / n,
                                  s0 + (s1 - s0) * _1 / n,
                                  v0 + (v1 - v0) * _1 / n))
            colors.append((255 * r, 255 * g, 255 * b))
        self.colors = colors

    def draw_life(self, grid_visible):
        for x in range(1, self.columns + 1):
            for y in range(1, self.rows + 1):
                size = self.tile_size
                if grid_visible:
                    pg.draw.rect(self.screen, self.colors[self.current_field[y][x] - 1],
                                 ((x - 1) * size + 2, (y - 1) * size + 2, size - 2, size - 2))
                else:
                    pg.draw.rect(self.screen, self.colors[self.current_field[y][x] - 1],
                                 ((x - 1) * size, (y - 1) * size, size, size))
                if ((self.time % self.speed) == 0) and self.running:
                    self.next_field[y][x] = self.check_cell(self.current_field, x, y)

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
    app = App(random_field=False, probability=0.3, tile_size=5, speed=1,
              cmap=None)
    app.set_rules([3], [1, 2, 3, 4, 5], 16)
    for i in range(20):
        for j in range(20):
            app.current_field[app.rows // 2 - 9 + i][app.columns // 2 - 9 + j] = 1
    app.run(grid_visible=False)
