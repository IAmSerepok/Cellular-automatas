import pygame as pg
from collections import deque
from random import randrange, randint


class Ant:

    def __init__(self, app_, position):

        self.app = app_
        self.x, self.y = position
        self.step = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        value = self.app.grid[self.y][self.x]
        self.app.grid[self.y][self.x] = (value + 1) % self.app.conditions

        size = self.app.cell_size
        rect = self.x * size, self.y * size, size, size

        pg.draw.rect(self.app.screen, pg.Color(self.app.colors[value]), rect)

        if self.app.rules[value] == 'L':
            self.step.rotate(1)
        elif self.app.rules[value] == 'R':
            self.step.rotate(-1)
        elif self.app.rules[value] == 'N':
            ...
        else:
            raise ValueError(f'Invalid rule: {self.app.rules[value]}')

        dx, dy = self.step[0]

        self.x = (self.x + dx) % self.app.columns
        self.y = (self.y + dy) % self.app.rows


class App:
    def __init__(
            self, screen_width=1000, screen_height=700, cell_size=10,
            number_of_ants=1, speed=1, rule='RL'
    ):
        pg.init()
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

        self.cell_size = cell_size
        self.rows, self.columns = screen_height // cell_size, screen_width // cell_size
        self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]
        self.conditions = len(rule)
        self.colors = [(230, 230, 230)] + [self.get_random_color() for _ in range(self.conditions - 1)]

        rules = {}
        for index, c in enumerate(rule):
            rules[index] = c
        self.rules = rules

        self.speed = speed
        self.time = 0
        self.running = True

        self.ants = [Ant(self, [randrange(self.columns), randrange(self.rows)])
                     for _ in range(number_of_ants)]
        if number_of_ants == 1:
            self.ants[0].x = self.columns // 2
            self.ants[0].y = self.rows // 2

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def generate_grid(self, is_empty):
        if not is_empty:
            self.grid = [[randint(0, 1) for col in range(self.columns)] for row in range(self.rows)]

    def run(self, is_empty=True):

        self.generate_grid(is_empty)

        while True:

            if ((self.time % self.speed) == 0) and self.running:
                for ant in self.ants:
                    ant.run()

            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                if i.type == pg.MOUSEBUTTONDOWN:
                    self.running = not self.running

            pg.display.flip()
            self.time += 1
            self.clock.tick()


app = App(number_of_ants=1, cell_size=5, speed=1, rule='LRRRRRLLR')
app.run(is_empty=True)
