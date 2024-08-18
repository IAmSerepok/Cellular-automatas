import pygame as pg
from random import randrange, random
from copy import deepcopy
from math import floor

from hensel import hensel


class App:
    def __init__(
            self, columns=140, rows=140, tile_size=5, fps=60,
            random_field=False, probability=0.5, speed=1
    ):
        pg.init()
        self.rows, self.columns = rows, columns
        self.screen_width = columns * tile_size
        self.screen_height = rows * tile_size
        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        self.clock = pg.time.Clock()

        self.rule_b, self.rule_s = None, None

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.running = True

        self.color = self.get_random_color()
        self.tile_size = tile_size

        self.next_field = [[0 for i in range(self.columns)] for j in range(self.rows)]
        if random_field:
            self.current_field = [[1 if random() < probability else 0
                                   for i in range(self.columns)] for j in range(self.rows)]
        else:
            self.current_field = [[0 for i in range(self.columns)] for j in range(self.rows)]

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def check_cell(self, current_field_, x, y):
        count = 0
        binary = 0
        index = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if (i != x) or (j != y):
                    x0, y0 = i, j
                    if x0 >= self.columns:
                        x0 = 0
                    if y0 >= self.rows:
                        y0 = 0
                    if current_field_[y0][x0]:
                        count += 1
                        binary += 2 ** index
                    index += 1

        if current_field_[y][x]:
            try:
                for letter in self.rule_s[str(count)]:
                    if binary in hensel[letter][str(count)]:
                        return 1
            except:
                ...
            return 0
        else:
            try:
                for letter in self.rule_b[str(count)]:
                    if binary in hensel[letter][str(count)]:
                        return 1
            except:
                ...
            return 0

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.screen_height), 1) for x in
             range(0, self.screen_width, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.screen_width, y), 1) for y in
             range(0, self.screen_height, self.tile_size)]

    @staticmethod
    def convert_rule(string):
        rules = {}
        rule = []
        for c in string:
            if c in ['8', '7', '6', '5', '4', '3', '2', '1', '0']:
                if (c == '0') or (c == '8'):
                    rule = ['']
                elif not len(rule):
                    rule = ['c', 'e', 'k', 'a', 'i', 'n', 'y', 'q', 'j', 'r', 't', 'w', 'z']
                rules[c] = rule
                rule = []
            elif c in ['z', 'w', 't', 'r', 'j', 'q', 'y', 'n', 'i', 'a', 'k', 'e', 'c']:
                rule.append(c)
        return rules

    def set_rules(self, birth, survival):
        self.rule_b = self.convert_rule(birth[::-1])
        self.rule_s = self.convert_rule(survival[::-1])

    def get_cords(self, pos):
        x, y = pos
        x = floor(x / self.screen_width * self.columns)
        y = floor(y / self.screen_height * self.rows)
        return x, y

    def draw_life(self, grid_visible):
        for x in range(self.columns):
            for y in range(self.rows):
                if self.current_field[y][x]:
                    size = self.tile_size
                    if grid_visible:
                        pg.draw.rect(self.screen, self.color, (x * size + 2,
                                                               y * size + 2, size - 2, size - 2))
                    else:
                        pg.draw.rect(self.screen, self.color, (x * size,
                                                               y * size, size, size))
                if ((self.time % self.speed) == 0) and self.running:
                    self.next_field[y][x] = self.check_cell(self.current_field, x, y)

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

            self.draw_life(grid_visible)
            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = App(random_field=False, probability=0.5)
    app.set_rules('2cei3cekanyqjr4z5cekinyqjr6cekin78', '1c2ik3y4q5cekinyqjr678')
    for i in range(80):
        for j in range(80):
            if random() < 0.5:
                app.current_field[app.rows // 2 - 40 + i][app.columns // 2 - 40 + j] = 1
    app.run(grid_visible=False)
