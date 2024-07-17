import pygame
import pymunk
import pymunk.pygame_util
import math, sys, random

pygame.init()

# Pygame window setup
width, height = 1600, 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Platformer!")

# Colors
white = (255, 255, 255)
green = (50, 168, 82)
black = (0, 0, 0)
red = (200, 0, 0)
grey = (150, 150, 150)
blue = (66, 185, 189)
brown = (79, 44, 41)

# Pygame variables
FONT = pygame.font.Font(None, 40)
clock = pygame.time.Clock()
FPS = 60
dt = 1 / FPS
run = True


class Player:
    def __init__(self, mass, body, shape, starting) -> None:
        self.mass = mass
        self.body = body
        self.shape = shape
        self.jumps = 1
        self.starting = starting

    def die(self):
        self.body.position = self.starting

class Button:
    def __init__(self, door, body, shape) -> None:
        self.door = door
        self.body = body
        self.shape = shape


class Door:
    def __init__(self, body: pymunk.Body, shape, change_x, change_y, stop=None) -> None:
        self.button = None
        self.body = body
        self.shape = shape
        self.start = body.position
        self.change_x = change_x
        self.change_y = change_y
        self.moving = False
        self.stop = stop

    def button_pressed(
            self,
    ):
        if not self.body.position == self.stop:
            self.body.position += (self.change_x, self.change_y)
            # self.body.velocity = (self.change_x, self.change_y)
        self.moving = True

    def home_state(self):
        self.body.position -= (self.change_x, self.change_y)

def draw(space, window, draw_options, time):
    window.fill((105, 78, 76))
    space.debug_draw(draw_options)
    window.blit(
        FONT.render(
            str(int(time)),
            False,
            (0, 0, 0),
        ),
        (width / 2, 30),
    )
    pygame.display.update()

time = 0
while run:
    space = pymunk.Space()
    space.gravity = (0, 980)
    draw_options = pymunk.pygame_util.DrawOptions(window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw(space, window, draw_options, time)
    space.step(dt)
    clock.tick(FPS)
    time += 1 / 60
pygame.quit()