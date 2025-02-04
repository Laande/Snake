"""
    Original code : https://youtu.be/9bBgyOkoBQ0
"""


import pygame
import sys
import random
from g_python.gextension import Extension


extension_info = {
    "title": "Snake",
    "description": "Play snake",
    "version": "2.0",
    "author": "Lande"
}

extension_settings = {
    "use_click_trigger": True,
    "can_leave": True,
    "can_delete": True
}

ext = Extension(extension_info, sys.argv, extension_settings)
ext.start()

ext.on_event('double_click', lambda: main())


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = right
        self.color = (50, 255, 50)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+(x*gridsize)) % screen_width), (cur[1]+(y*gridsize)) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            global record
            if self.score > record:
                record = self.score
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = right
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (100, 100, 100), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ext.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 50, 50)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, int(grid_width-1))*gridsize, random.randint(0, int(grid_height-1))*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (100, 100, 100), r, 1)


def drawgrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (60, 60, 60), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (50, 50, 50), rr)


screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

record = 0


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawgrid(surface)

    snake = Snake()
    food = Food()

    while True:
        clock.tick(12)
        snake.handle_keys()
        drawgrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.set_caption(f'Score : {snake.score} | Record : {record}')
        pygame.display.update()
