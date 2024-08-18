import pygame
import pygame as pg
from copy import deepcopy
from math import floor


class App:
    def __init__(self, screen_width=1400, screen_height=700, tile_size=35, fps=60, speed=15):
        pg.init()

        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

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
        x = floor(x / self.screen_width * self.columns)
        y = floor(y / self.screen_height * self.rows)
        return x, y

    def signal(self, x, y):
        if ((self.time % self.speed) == 0) and self.running:
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if self.current_field[j][i] == 2:
                        count += 1

            if (count == 1) or (count == 2):
                self.next_field[y][x] = 2

    def run(self):
        while True:
            self.screen.fill(pg.Color('black'))
            self.generate_grid()

            self.next_field = deepcopy(self.current_field)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.get_cords(event.pos)
                    if event.button == 1:
                        self.next_field[y][x] = (self.current_field[y][x] + 1) % 4
                    elif event.button == 3:
                        self.running = not self.running

            # draw life
            for x in range(1, self.columns - 1):
                for y in range(1, self.rows - 1):
                    color = 'black'
                    if self.current_field[y][x] == 1:
                        self.signal(x, y)
                        color = 'yellow'
                    if self.current_field[y][x] == 3:
                        if ((self.time % self.speed) == 0) and self.running:
                            self.next_field[y][x] = 1
                        color = 'red'
                    if self.current_field[y][x] == 2:
                        if ((self.time % self.speed) == 0) and self.running:
                            self.next_field[y][x] = 3
                        color = 'blue'
                    size = self.tile_size

                    pg.draw.rect(self.screen, color, (x * size + 2, y * size + 2, size - 2, size - 2))

            self.current_field = deepcopy(self.next_field)
            pg.display.flip()
            self.time += 1
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = App()
    app.run()
