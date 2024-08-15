import pygame as pg
from collections import deque
from random import randrange, randint


class Ant:
    
    def __init__(self, app_, position, color):
        
        self.app = app_
        self.color = color
        self.x, self.y = position
        self.step = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        
        value = self.app.grid[self.y][self.x]
        self.app.grid[self.y][self.x] = not value

        size = self.app.cell_size
        rect = self.x * size, self.y * size, size - 1, size - 1
        
        if value:
            pg.draw.rect(self.app.screen, pg.Color('white'), rect)
        else:
            pg.draw.rect(self.app.screen, self.color, rect)

        self.step.rotate(1) if value else self.step.rotate(-1)
        dx, dy = self.step[0]
        self.x = (self.x + dx) % self.app.columns
        self.y = (self.y + dy) % self.app.rows


class App:
    
    def __init__(self, screen_width=1200, screen_height=800, cell_size=10, number_of_ants=1, speed=1):
        
        pg.init()
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

        self.cell_size = cell_size
        self.rows, self.columns = screen_height // cell_size, screen_width // cell_size
        self.grid = [[0 for col in range(self.columns)] for row in range(self.rows)]

        self.speed = speed
        self.time = 0
        self.running = True

        self.ants = [Ant(self, [randrange(self.columns), randrange(self.rows)], self.get_random_color())
                     for _ in range(number_of_ants)]

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def grid_draw(self):

        for row in range(self.rows):
            for column in range(self.columns):

                rect = column * self.cell_size, row * self.cell_size, self.cell_size - 1, self.cell_size - 1

                if self.grid[row][column]:
                    pg.draw.rect(self.screen, 'white', rect)
                else:
                    pg.draw.rect(self.screen, (150, 150, 150), rect)

    def generate_grid(self, is_empty, is_visible):
        if not is_empty:
            self.grid = [[randint(0, 1) for col in range(self.columns)] for row in range(self.rows)]
        if is_visible:
            self.grid_draw()

    def run(self, is_empty=True, is_visible=False):

        self.generate_grid(is_empty, is_visible)
        
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


app = App(number_of_ants=3)
app.run(is_empty=True, is_visible=False)
