from PIL import Image, ImageTk
from pygame import *
from functions import *
from setup import *


class AnimDrawer:
    def __init__(self, animations, window):
        self.animations = animations
        self.window = window

    def clear(self):
        self.animations = []

    def add(self, animation, coords):
        self.animations.append((animation, coords))

    def draw(self, bg):
        for i in range(5):
            for j in range(len(self.animations)):
                self.animations[j][0].draw(i, self.animations[j][1])
            display.update()
            time.delay(200)
            self.window.blit(bg)


class Animation:
    def __init__(self, paths, window):
        self.pictures = [image.load(path) for path in paths]
        self.window = window

    def draw(self, frame, coords):
        if frame >= len(self.pictures):
            return 0
        self.window.blit(self.pictures[frame], coords)

    def clear(self, frame, coords, bg):
        if frame >= len(self.pictures):
            return 0
        self.window.blit(bg, coords)

    def __len__(self):
        return len(self.pictures)


class Tile:
    def __init__(self, code, elem):
        self.obj = code
        self.unit = elem


class Unit:
    def __init__(self, code, coords, drawer, **animations):
        self.x = coords[0]
        self.y = coords[1]
        self.animations = animations
        self.code = code
        self.drawer = drawer

    def pl(self, coords=(0, 0)):

        return (self.x + coords[0]) * TILE_SIZE, (self.y + coords[1]) * TILE_SIZE  # место в пикселях

    def anim(self):
        # TODO:стоит на месте
        pass


class Hero(Unit):
    def __init__(self, hp, coords, drawer, **animations):
        self.__init__(1, coords, drawer, **animations)
        self.hp = hp

    def move(self, direction):
        # TODO: движение на карте
        if direction[0] >= 0:
            self.drawer.add(self.animations['run_right'], divide_line(self.pl(), self.pl(direction), len(self.animations['run_right'])))
        else:
            self.drawer.add(self.animations['run_left'], divide_line(self.pl(), self.pl(direction), len(self.animations['run_left'])))

    def key_read(self):
        keys = pygame.key.get_pressed()
        res = [key for key in keys.keys() if keys[key]]
        direction = (0, 0)

        # обработка всех кнопок, которые нажаты (пока только движение)
        if MOVE_UP in res:
            direction[1] -= 1
        if MOVE_DOWN in res:
            direction[1] += 1
        if MOVE_LEFT in res:
            direction[0] -= 1
        if MOVE_RIGHT in res:
            direction[0] += 1
        self.move(direction)

