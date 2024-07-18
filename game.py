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


def create_button(
        space,
        button_pos,
        button_shape,
        door_pos,
        door_shape,
        stop,
        change,
        buttons,
        collision_type_door=2,
        color_door=white,
):
    # BUTTON
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = button_pos
    shape = pymunk.Poly.create_box(body, button_shape)
    shape.elasticity = 0
    shape.friction = 0.5
    shape.collision_type = 7
    shape.color = (*brown, 100)
    space.add(body, shape)
    # DOOR
    body1 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body1.position = door_pos
    shape1 = pymunk.Poly.create_box(body1, door_shape)
    shape1.elasticity = 0
    shape1.friction = 0.5
    shape1.collision_type = collision_type_door
    shape1.color = (*color_door, 100)
    space.add(body1, shape1)
    door = Door(body1, shape1, change[0], change[1], stop)
    button = Button(door, body, shape)
    buttons.update({button: door})
    return buttons


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


def create_level_1(width, height):
    button_dict = {}
    space = pymunk.Space()
    space.gravity = (0, 980)

    buttons = {}
    x = 50
    rects = [
        # (X, Y),            (WIDTH,HEIGHT), COLOR, COLLISION_TYPE
        [(width / 3, height - 225), (width, 10), grey, 2],
        [(width - 100, height - 50), (300, 100), grey, 2],
        [(500, 550), (300, 20), grey, 2],
        [(500, 300), (300, 20), grey, 2],
        [(1300, 500), (50, 20), grey, 2],
        [(width / 2, height - 10), (100, 30), green, 4],
        [(width - 500, 200), (80, 20), green, 4],
        [(width / 3, height - 10), (100, 30), blue, 5],
        [(width - 300, height - 10), (100, 30), red, 6],
        [(width - 200, 350), (100, 10), red, 6],
    ]

    for z in range(3, 8):
        rects.append([(width - 70, z * 100 + 100), (x, 10), red, 6])
    for x in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = x[0]
        shape = pymunk.Poly.create_box(body, x[1])
        shape.elasticity = 0
        shape.friction = 0.5
        shape.collision_type = x[-1]
        shape.color = (*x[2], 100)
        space.add(body, shape)

    button_make = [
        [
            space,  # Space
            (10, 985),
            (100, 20),
            (1200, 30),
            (100, 20),
            (1200, 200),
            (0, 2),
            buttons,
        ],
        [
            space,
            (300, 300),
            (100, 20),
            (1100, 220),
            (80, 20),
            (1100, 190),
            (0, -2),
            buttons,
        ],
        [
            space,
            (500, 300),
            (100, 20),
            (200, 500),
            (80, 20),
            (200, 400),
            (0, -2),
            buttons,
        ],
        [
            space,
            (1500, 300),
            (50, 20),
            (800, 150),
            (80, 20),
            (1100, 150),
            (2, 0),
            buttons,
        ],
    ]
    # space, buttonpos, buttonshape, doorpos, doorshape, stop, change, color, buttons_dict
    for x in button_make:
        buttons = create_button(*x)
    create_wall(space, width, height)
    create_ball(space, 20, 20, (300, 300))
    create_structure(space, (100, 100), (50, 50), black, 100)
    create_swing(space, (900, 100), (800, 300), 2000, (200, 20))
    b, s = create_player(space, (200, height - 100), (40, 59), (*red, 100), 100)
    player_fire = Player(100, b, s, (200, height - 100))
    b, s = create_player(space, (300, height - 100), (40, 60), (*blue, 100), 100)
    player_water = Player(100, b, s, (300, height - 100))
    button_dict.update(buttons)
    create_wall(space, width, height)

    return player_fire, player_water, space, button_dict


def create_level_2(width, height):
    space = pymunk.Space()
    space.gravity = (0, 980)
    buttons = {}
    rects = [
        # (X, Y),            (WIDTH,HEIGHT), COLOR, COLLISION_TYPE
        [(500, 450), (170, 10), grey, 2],
        [(960, 800), (20, 20), grey, 2],
        [(1100, 700), (20, 20), grey, 2],
        [(60, height - 14), (140, 30), grey, 2],

    ]
    for x in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = x[0]
        shape = pymunk.Poly.create_box(body, x[1])
        shape.elasticity = 0
        shape.friction = 0.5
        shape.collision_type = x[-1]
        shape.color = (*x[2], 100)
        space.add(body, shape)

    button_make = [
        [
            space,
            (width - 50, 100),
            (50, 20),
            (310, 150),
            (150, 10),
            (310, height - 550),
            (0, 2),
            buttons,
        ],
        [
            space,
            (880, 250),
            (50, 20),
            (400, 400),
            (20, 200),
            (400, 580),
            (0, 2),
            buttons,
            4,
            green,
        ],
        [
            space,
            (width / 2.5, height / 2 - 20),
            (100, 10),
            (900, 500),
            (300, 10),
            (1300, 100),
            (1, -1),
            buttons,
        ],
    ]
    # space, buttonpos, buttonshape, doorpos, doorshape, stop, change, buttons, collision_type_door {2}
    for x in button_make:
        buttons = create_button(*x)

    create_swing(space, (250, height - 280), (250, height - 140), 2000, (200, 20))
    create_swing(
        space, (width / 2.5, height / 2), (width / 2.5, height - 250), 2000, (200, 20))

    create_structure(space, (320, 150), (50, 50), black, 100)
    create_ball(space, 10, 300, (800, 100))
    f_s, w_s = (30, height - 100), (100, height - 100)  # Starting position
    b, s = create_player(space, f_s, (40, 59), (*red, 100), 100)
    player_fire = Player(100, b, s, f_s)
    b, s = create_player(space, w_s, (40, 60), (*blue, 100), 100)
    player_water = Player(100, b, s, w_s)

    return player_fire, player_water, space, buttons

def play(num=1):
    run = True
    match num:
        case 1:
            player_fire, player_water, space, button_dict = create_level_1(
                width, height
            )
        case 2:
            player_fire, player_water, space, button_dict = create_level_2(
                width, height
            )
    draw_options = pymunk.pygame_util.DrawOptions(window)
    speed = 3

    def pre_solve(arbiter, space, data):
        if (
                player_water.body.velocity[1] >= 0
                and int(arbiter.shapes[0].body.moment) == 43333
        ):
            player_water.jumps = 1
        elif (
                player_fire.body.velocity[1] >= 0
                and int(arbiter.shapes[0].body.moment) != 43333
        ):
            player_fire.jumps = 1
        # 43333 is blue
        # 42341 is red
        return True

    def pre_solve3(arbiter, space, data):
        if not int(arbiter.shapes[0].body.moment) == 43333:
            player_fire.die()
            return False
        elif player_water.body.velocity[1] >= 0:
            player_water.die()
            return False

    def pre_solve4(arbiter, space, data):
        if not int(arbiter.shapes[0].body.moment) == 43333:
            player_fire.die()
            return False
        elif player_water.body.velocity[1] >= 0:
            player_water.jumps = 1
        return True

    def pre_solve5(arbiter, space, data):
        if int(arbiter.shapes[0].body.moment) == 43333:
            player_water.die()
            return False
        elif player_fire.body.velocity[1] >= 0:
            player_fire.jumps = 1
        return True

    def pre_solve6(arbiter, space, data):
        for x in button_dict.keys():
            if arbiter.shapes[1].body.position == x.body.position:
                x.door.button_pressed()
                break
        # print(
        #     "yes" if arbiter.shapes[1].body.position == x.body.position else 1
        #     for x in button_dict
        # )
        return True

    h = space.add_collision_handler(1, 2)  # Ground
    h.pre_solve = pre_solve
    h1 = space.add_collision_handler(1, 1)  # Players
    h1.pre_solve = lambda x, y, z: False
    h3 = space.add_collision_handler(1, 4)  # Poison
    h3.pre_solve = pre_solve3
    h4 = space.add_collision_handler(1, 5)  # Water
    h4.pre_solve = pre_solve4
    h5 = space.add_collision_handler(1, 6)  # Fire
    h5.pre_solve = pre_solve5
    h6 = space.add_collision_handler(1, 7)  # Button and player
    h6.pre_solve = pre_solve6
    h7 = space.add_collision_handler(8, 7)  # Button and object
    h7.pre_solve = pre_solve6
    h8 = space.add_collision_handler(1, 8)  # player and object
    h8.pre_solve = pre_solve
    time = 0
    while run:
        player_fire.body.velocity = pymunk.Vec2d(0, player_fire.body.velocity[1])
        player_water.body.velocity = pymunk.Vec2d(0, player_water.body.velocity[1])
        player_fire.body.angle = 0
        player_water.body.angle = 0
        for x in button_dict.values():
            if not x.moving and x.body.position != x.start:
                x.home_state()
            x.moving = False
        keys = pygame.key.get_pressed()

        # FIRE CONTROLS
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
        # places character at mouse

        if pygame.mouse.get_pressed(3)[0]:  # left
            player_fire.body.position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(3)[2]:  # right
            player_water.body.position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_r,
                    pygame.K_1,
                    pygame.K_2,
            ):
                if event.key == pygame.K_r:
                    play(num)
                elif event.key == pygame.K_1:
                    play(1)
                elif event.key == pygame.K_2:
                    play(2)

        draw(space, window, draw_options, time)
        space.step(dt)
        clock.tick(FPS)
        time += 1 / 60

    pygame.quit()


if __name__ == "__main__":
    play(1)