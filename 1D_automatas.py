import pygame as pg
from random import randint, randrange
from copy import deepcopy


class App:

    def __init__(self, screen_width=1400, screen_height=700, tile_size=10, fps=60, speed=1, random_field=False):

        pg.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()
        self.rules = dict()

        self.FPS = fps

        self.speed = speed
        self.time = 0
        self.depth = 1
        self.running = True

        self.color = self.get_random_color()
        self.tile_size = tile_size
        self.rows, self.columns = screen_height // tile_size, screen_width // tile_size

        self.current_field = self.next_field = [[0 for i in range(self.columns)] for j in range(self.rows)]
        if random_field:
            for j in range(self.columns):
                self.current_field[1][j] = randint(0, 1)

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def set_rule(self, rule):
        numb = rule
        rules = dict()
        for i in range(8):
            value = numb % 2
            numb = numb // 2
            rules[i] = value

        self.rules = rules

    def check_cell(self, x, y):
        s = ""
        s += str(self.current_field[y][x - 1])
        s += str(self.current_field[y][x])
        s += str(self.current_field[y][x + 1])
        return self.rules[int(s, 2)]

    def generate_grid(self, grid_visible):
        if grid_visible:
            [pg.draw.line(self.screen, 'gray', (x, 0), (x, self.screen_height), 1) for x in
             range(0, self.screen_width, self.tile_size)]
            [pg.draw.line(self.screen, 'gray', (0, y), (self.screen_width, y), 1) for y in
             range(0, self.screen_height, self.tile_size)]

    def run(self, grid_visible):

        while True:

            self.screen.fill(pg.Color('black'))
            self.generate_grid(grid_visible)

            self.next_field = deepcopy(self.current_field)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.running = not self.running

            # draw life
            for x in range(1, self.columns - 1):
                for y in range(1, self.rows - 1):
                    if self.current_field[y][x]:
                        size = self.tile_size
                        if grid_visible:
                            pg.draw.rect(self.screen, self.color, (x * size + 2, y * size + 2, size - 2, size - 2))
                        else:
                            pg.draw.rect(self.screen, self.color, (x * size + 2, y * size + 2, size - 2, size - 2),
                                         border_radius=self.tile_size // 5)

                    if ((self.time % self.speed) == 0) and self.running and (y == self.depth):
                        if self.depth < self.rows:
                            self.next_field[y+1][x] = self.check_cell(x, y)

            if (self.depth >= self.rows) and ((self.time % self.speed) == 0) and self.running:
                for i in range(1, self.columns - 1):
                    for j in range(1, self.rows - 2):
                        self.next_field[j][i] = self.current_field[j + 1][i]

                for i in range(1, self.columns - 1):
                    self.next_field[self.rows - 2][i] = self.check_cell(i, self.rows - 2)

            self.current_field = deepcopy(self.next_field)

            pg.display.flip()
            if ((self.time % self.speed) == 0) and self.running:
                self.depth += 1
            self.time += 1
            self.clock.tick(self.FPS)


app = App(random_field=True, speed=2)
app.set_rule(110)
app.run(grid_visible=False)
