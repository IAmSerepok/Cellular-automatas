import pygame as pg
from random import randrange


class Block:

    def __init__(self, app_, size_):
        self.app = app_
        self.size = size_
        self.mass = 1
        self.height = app_.screen_height//2
        self.speed = 0
        self.delta = 0.001

    def update(self, mid_height):
        self.height += self.speed
        self.speed -= self.delta * (self.height - mid_height)
        # self.speed *= 0.9995

    def draw(self, x):
        size = self.size
        pg.draw.rect(self.app.screen, self.app.color, (x * size + 2, self.height, size - 2, size - 2))


class App:

    def __init__(self, screen_width=1200, screen_height=700, number_of_blocks=150, fps=600):

        pg.init()
        self.movement = 1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pg.display.set_mode([screen_width, screen_height])
        self.clock = pg.time.Clock()

        self.FPS = fps
        self.running = True

        self.color = self.get_random_color()
        self.number_of_blocks = number_of_blocks
        block_size = self.screen_width // number_of_blocks

        self.field = [Block(self, block_size) for i in range(self.number_of_blocks)]

    @staticmethod
    def get_random_color():
        return randrange(30, 220), randrange(30, 220), randrange(30, 220)

    def run(self):

        while True:

            self.screen.fill(pg.Color('black'))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.movement = (self.movement + 1) % 3
                    elif event.button == 3:
                        self.running = not self.running

            for i in range(1, self.number_of_blocks - 1):
                left, right = (self.field[i-1].height, self.field[i+1].height)
                self.field[i].update((left+right)/2)

            for i, block in enumerate(self.field):
                block.draw(i)

            if self.movement == 1:
                self.field[1].speed = 1
            elif self.movement == 2:
                self.field[1].speed = -1
            pg.display.flip()
            self.clock.tick(self.FPS)


app = App()
app.run()
