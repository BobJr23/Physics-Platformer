import pygame
import pymunk
import pymunk.pygame_util
import math, sys, random

pygame.init()
width, height = 1600, 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fireboy and Watergirl!")
white = (255, 255, 255)
green = (50, 168, 82)
black = (0, 0, 0)
red = (200, 0, 0)
grey = (150, 150, 150)
blue = (66, 185, 189)
brown = (79, 44, 41)
FONT = pygame.font.Font(None, 40)
#
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

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(white)
    pygame.display.update()
    clock.tick(FPS)