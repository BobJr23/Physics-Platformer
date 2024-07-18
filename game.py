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


# Player class created with create_player
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


# Door and Button created together, will go in dict
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


class Complete:
    def __init__(self) -> None:
        self.fire_in = False
        self.water_in = False

    def check(self, c):
        if self.water_in and self.fire_in:
            return True
        return False


def create_wall(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20), 2],
        [(width / 2, 10), (width, 20), 3],
        [(10, height / 2), (20, height), 3],
        [(width - 10, height / 2), (20, height), 3],
    ]
    for x in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = x[0]
        shape = pymunk.Poly.create_box(body, x[1])
        shape.elasticity = 0
        shape.friction = 0.1
        shape.collision_type = x[2]
        shape.color = (*grey, 100)
        space.add(body, shape)


def create_structure(space, pos, size, color, mass):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Poly.create_box(body, size, radius=1)
    shape.color = (*color, 100)
    shape.mass = mass
    shape.elasticity = 0
    shape.friction = 0.4
    shape.collision_type = 8
    space.add(body, shape)


def create_player(space, pos, size, color, mass):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Poly.create_box(body, size, radius=1)
    shape.color = color
    shape.mass = mass
    shape.elasticity = 0
    shape.friction = 0.1
    shape.collision_type = 1
    space.add(body, shape)
    return body, shape

def create_ball(space, radius, mass, pos):
    body = pymunk.Body()
    body.position = pos
    # SHAPE STATS
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (*black, 100)
    shape.elasticity = 0
    shape.friction = 0.4
    shape.collision_type = 8
    # ADD TO SIMULATION
    space.add(body, shape)
    return shape

def create_swing(space, top_pos, bottom_pos, mass, shape):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = top_pos

    body = pymunk.Body()
    body.position = bottom_pos
    line = pymunk.Segment(body, (0, 0), (0, 0), 5)
    circle = pymunk.Poly.create_box(
        body,
        shape,
    )
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = mass
    circle.elasticity = 0.95
    circle.collision_type = 2
    circle.color = (*black, 100)
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)
    return body


def create_level_1(WIDTH, height):
    button_dict = {}
    space = pymunk.Space()
    space.gravity = (0, 980)

    buttons = {}
    x = 50
    rects = [
        # (X, Y),            (WIDTH,HEIGHT), COLOR
        [(WIDTH / 3, height - 225), (WIDTH, 10), grey, 2],
        [(WIDTH - 100, height - 50), (300, 100), grey, 2],
        [(500, 550), (300, 20), grey, 2],
        [(500, 300), (300, 20), grey, 2],
        [(1300, 500), (50, 20), grey, 2],
        [(WIDTH / 2, height - 10), (100, 30), green, 4],
        [(WIDTH - 500, 200), (80, 20), green, 4],
        [(WIDTH / 3, height - 10), (100, 30), blue, 5],
        [(WIDTH - 300, height - 10), (100, 30), red, 6],
        [(WIDTH - 200, 350), (100, 10), red, 6]

    ]

    for z in range(3, 8):
        rects.append([(WIDTH - 70, z * 100 + 100), (x, 10), red, 6])
    for x in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = x[0]
        shape = pymunk.Poly.create_box(body, x[1])
        shape.elasticity = 0
        shape.friction = 0.5
        shape.collision_type = x[-1]
        shape.color = (*x[2], 100)
        space.add(body, shape)

    #CREATE Objects
    create_wall(space, WIDTH, height)
    create_ball(space, 20, 20, (300, 300))
    create_structure(space, (100, 100), (50, 50), black, 100)
    create_swing(space, (900, 100), (800, 300), 2000, (200, 20))
    b, s = create_player(space, (200, height - 100), (40, 59), (*red, 100), 100)
    player_fire = Player(100, b, s, (200, height - 100))
    b, s = create_player(space, (300, height - 100), (40, 60), (*blue, 100), 100)
    player_water = Player(100, b, s, (300, height - 100))

    return player_fire, player_water, space, button_dict


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
player_fire, player_water, space, button_dict = create_level_1(
    width, height
)
while run:
    if keys[pygame.K_a]:
        player_fire.body.position -= (speed, 0)
    if keys[pygame.K_d]:
        player_fire.body.position += (speed, 0)
    if keys[pygame.K_w] and player_fire.jumps > 0:
        player_fire.body.apply_impulse_at_local_point((0, -50000))
        player_fire.jumps = 0
        # WATER CONTROLS
    if keys[pygame.K_LEFT]:
        player_water.body.position -= (speed, 0)
    if keys[pygame.K_RIGHT]:
        player_water.body.position += (speed, 0)
    if keys[pygame.K_UP] and player_water.jumps > 0:
        player_water.body.apply_impulse_at_local_point((0, -50000))
        player_water.jumps = 0

    # places character at mouse for game testing
    if pygame.mouse.get_pressed(3)[0]:  # left
        player_fire.body.position = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed(3)[2]:  # right
        player_water.body.position = pygame.mouse.get_pos()

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
