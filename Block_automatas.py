import pygame
import pygame as pg
from copy import deepcopy
from random import randrange, randint
from math import floor


class App:

    def __init__(self, screen_width=1400, screen_height=700, tile_size=35, fps=60, speed=3):

        pg.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

        self.FPS = fps
        self.speed = speed
        self.time = 0
        self.iter = 0
        self.running = False
        self.reverse = False

        self.delta = 0
        self.reverse_rules = dict()
        self.normal_rules = dict()

        self.color = self.get_random_color()
        self.tile_size = tile_size
        self.rows, self.columns = screen_height // tile_size, screen_width // tile_size

        self.next_field = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.current_field = [[randint(0, 0) for i in range(self.columns)] for j in range(self.rows)]

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def generate_grid(self):
        [pg.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.screen_height), 1) for x in
         range(0, self.screen_width, self.tile_size)]
        [pg.draw.line(self.screen, (30, 30, 30), (0, y), (self.screen_width, y), 1) for y in
         range(0, self.screen_height, self.tile_size)]

    def set_rule(self, *rules):
        for source, aim in rules:
            self.normal_rules[source] = aim
            self.reverse_rules[aim] = source

    def check_cell(self, x, y):
        s = str(self.current_field[y][x])
        s += str(self.current_field[y][x + 1])
        s += str(self.current_field[y + 1][x])
        s += str(self.current_field[y + 1][x + 1])
        self.set_next(s, x, y)

    def set_next(self, rule, x, y):
        if self.reverse:
            s = self.reverse_rules[rule]
            if self.iter == 0:
                return
        else:
            s = self.normal_rules[rule]
        self.next_field[y][x] = int(s[0])
        self.next_field[y][x + 1] = int(s[1])
        self.next_field[y + 1][x] = int(s[2])
        self.next_field[y + 1][x + 1] = int(s[3])

    def get_cords(self, pos):
        x, y = pos
        x = floor(x/self.screen_width*self.columns)
        y = floor(y/self.screen_height*self.rows)
        return x, y

    def control(self, keys):
        if keys[pg.K_LEFT]:
            self.speed = min(self.speed + 1, 40)
        if keys[pg.K_RIGHT]:
            self.speed = max(self.speed - 1, 2)

    def draw_life(self):
        for x in range(self.columns):
            for y in range(self.rows):
                color = 'black'
                if self.current_field[y][x] == 1:
                    color = self.color

                size = self.tile_size
                pg.draw.rect(self.screen, color, (x * size + 2, y * size + 2, size - 2, size - 2))

    def run(self):

        while True:

            self.screen.fill(pg.Color('black'))
            self.generate_grid()

            self.next_field = deepcopy(self.current_field)

            self.control(pg.key.get_pressed())

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.get_cords(event.pos)
                    if event.button == 1:
                        self.next_field[y][x] = int(not self.current_field[y][x])
                    elif event.button == 2:
                        self.reverse = not self.reverse
                        self.delta = not self.delta
                    elif event.button == 3:
                        self.running = not self.running

            self.draw_life()
            for x in range(self.delta, self.columns - 1, 2):
                for y in range(self.delta, self.rows - 1, 2):
                    if ((self.time % self.speed) == 0) and self.running:
                        self.check_cell(x, y)

            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            if ((self.time % self.speed) == 0) and self.running:
                self.delta = not self.delta
                if self.reverse:
                    if self.iter > 0:
                        self.iter -= 1
                else:
                    self.iter += 1
            self.time += 1
            self.clock.tick(self.FPS)


app = App()

app.set_rule(
    ('0000', '0000'), ('0001', '0010'), ('0010', '1000'), ('0011', '0011'),
    ('0100', '0001'), ('0101', '0101'), ('0110', '0110'), ('0111', '0111'),
    ('1000', '0100'), ('1001', '1001'), ('1010', '1010'), ('1011', '1011'),
    ('1100', '1100'), ('1101', '1101'), ('1110', '1110'), ('1111', '1111'),
)

app.run()
