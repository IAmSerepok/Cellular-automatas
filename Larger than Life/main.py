import pygame as pg
from random import random
from copy import deepcopy
from colorsys import hsv_to_rgb


class App:
    def __init__(
            self, columns=200, rows=200, tile_size=3,
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
        self.rule_b, self.rule_s, self.generations, self.mid, self.radius = None, None, None, None, None

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True

        self.tile_size = tile_size
        self.colors = None

        self.random_field = random_field
        self.probability = probability
        self.next_field, self.current_field = None, None

    def generate_grid(self):
        self.next_field = [[0 for _1 in range(self.columns + 2 * self.radius)]
                           for _2 in range(self.rows + 2 * self.radius)]
        self.current_field = [[0 for _1 in range(self.columns + 2 * self.radius)]
                              for _2 in range(self.rows + 2 * self.radius)]
        if self.random_field:
            for x in range(self.radius, self.columns + self.radius):
                for y in range(self.radius, self.rows + self.radius):
                    if random() < self.probability:
                        self.current_field[y][x] = 1

    def check_cell(self, current_field_, x, y):
        count = 0
        for j in range(y - self.radius, y + self.radius + 1):
            for i in range(x - self.radius, x + self.radius + 1):
                if current_field_[j][i] == 1:
                    count += 1

        val = current_field_[y][x]
        if val == 1:
            if not self.mid:
                count -= 1
            if (self.rule_s[0] <= count) and (count <= self.rule_s[1]):
                return 1
            return (val + 1) % self.generations
        elif current_field_[y][x] == 0:
            if (self.rule_b[0] <= count) and (count <= self.rule_b[1]):
                return 1
            return 0
        else:
            return (val + 1) % self.generations

    def draw_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.screen_height), 1) for x in
             range(0, self.screen_width, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.screen_width, y), 1) for y in
             range(0, self.screen_height, self.tile_size)]

    def set_rules(self, radius, generations, mid, birth, survival):
        self.radius = radius
        self.mid = mid
        self.rule_b = birth
        self.rule_s = survival
        self.generations = generations

        self.generate_grid()

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
        for x in range(self.radius, self.columns + self.radius):
            for y in range(self.radius, self.rows + self.radius):
                size = self.tile_size
                if grid_visible:
                    pg.draw.rect(self.screen, self.colors[self.current_field[y][x] - 1],
                                 ((x - self.radius) * size + 2, (y - self.radius) * size + 2, size - 2, size - 2))
                else:
                    pg.draw.rect(self.screen, self.colors[self.current_field[y][x] - 1],
                                 ((x - self.radius) * size, (y - self.radius) * size, size, size))
                if ((self.time % self.speed) == 0) and self.running:
                    self.next_field[y][x] = self.check_cell(self.current_field, x, y)

    def run(self, grid_visible):
        self.generate_colors()

        while True:
            self.screen.fill(pg.Color('black'))
            self.draw_grid(grid_visible)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.running = not self.running

            self.draw_life(grid_visible)
            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            pg.image.save(self.screen, f'../output/image_{self.time}.jpg')
            self.clock.tick(self.FPS)


app = App(random_field=True, probability=0.4, tile_size=4, speed=1,
          cmap=[(130/350, 1.0, 0.4), (113/360, 0.0, 1.0)])
app.set_rules(7, 5, False, (63, 82), (64, 109))
app.run(grid_visible=False)