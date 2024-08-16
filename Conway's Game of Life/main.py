import pygame as pg
from random import randint, randrange, random
from copy import deepcopy
from math import floor


class App:

    def __init__(self, screen_width=1000, screen_height=700, tile_size=5, fps=60, random_field=False, probability=0.5):

        pg.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()
        self.rule_b = []
        self.rule_s = []
        self.metric = ''

        self.FPS = fps
        self.speed = 2
        self.time = 0
        self.running = True

        self.color = self.get_random_color()
        self.tile_size = tile_size
        self.rows, self.columns = screen_height // tile_size, screen_width // tile_size

        self.next_field = [[0 for i in range(self.columns)] for j in range(self.rows)]
        if random_field:
            self.current_field = [[1 if random() < probability else 0
                                   for i in range(self.columns)] for j in range(self.rows)]
        else:
            self.current_field = [[0 for i in range(self.columns)] for j in range(self.rows)]

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def check_cell_mur(self, current_field_, x, y):
        count = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if current_field_[j][i]:
                    count += 1

        if current_field_[y][x]:
            count -= 1
            if self.rule_s.count(count):
                return 1
            return 0
        else:
            if self.rule_b.count(count):
                return 1
            return 0

    def control(self, keys):
        if keys[pg.K_LEFT]:
            self.speed = min(self.speed + 1, 40)
        if keys[pg.K_RIGHT]:
            self.speed = max(self.speed - 1, 2)

    def check_cell_von_neumann(self, current_field_, x, y):
        count = 0
        for i in range(x - 1, x + 2):
            if current_field_[y][i]:
                count += 1
        if current_field_[y-1][x]:
            count += 1
        if current_field_[y+1][x]:
            count += 1

        if current_field_[y][x]:
            count -= 1
            if self.rule_s.count(count):
                return 1
            return 0
        else:
            if self.rule_b.count(count):
                return 1
            return 0

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.screen_height), 1) for x in
             range(0, self.screen_width, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.screen_width, y), 1) for y in
             range(0, self.screen_height, self.tile_size)]

    def set_rules(self, birth, survival, metric):
        self.rule_b = birth
        self.rule_s = survival
        self.metric = metric

    def get_cords(self, pos):
        x, y = pos
        x = floor(x / self.screen_width * self.columns)
        y = floor(y / self.screen_height * self.rows)
        return x, y

    def draw_life(self, grid_visible):
        for x in range(1, self.columns - 1):
            for y in range(1, self.rows - 1):
                if self.current_field[y][x]:
                    size = self.tile_size
                    if grid_visible:
                        pg.draw.rect(self.screen, self.color, (x * size + 2,
                                                               y * size + 2, size - 2, size - 2))
                    else:
                        pg.draw.rect(self.screen, self.color, (x * size,
                                                               y * size, size, size))
                if ((self.time % self.speed) == 0) and self.running:
                    if self.metric == "mur":
                        self.next_field[y][x] = self.check_cell_mur(self.current_field, x, y)
                    elif self.metric == "von_neumann":
                        self.next_field[y][x] = self.check_cell_von_neumann(self.current_field, x, y)

    def run(self, grid_visible):

        while True:

            self.screen.fill(pg.Color('black'))
            self.generate_grid(grid_visible)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = self.get_cords(event.pos)
                    if event.button == 1:
                        self.next_field[y][x] = not self.current_field[y][x]
                    elif event.button == 3:
                        self.running = not self.running

            self.control(pg.key.get_pressed())

            self.draw_life(grid_visible)
            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


app = App(random_field=True, probability=0.4, tile_size=4)
app.set_rules([3], [4, 5, 6, 7, 8], 'mur')
app.run(grid_visible=False)
