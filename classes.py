from PIL import Image, ImageTk
from pygame import *
from functions import *
from setup import *


Unit_list = []


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
    def __init__(self, code, anim, pl, size):
        self.x = pl[0]
        self.y = pl[1]
        self.img = anim
        self.code = code  # коды статичных элементов отрицательны, код ничего - 0
        self.size = size
        self.foe = 0  # количество юнитов, бегущих к тебе
        self.max_foe = 2  # максимальное количество юнитов, бегущих к тебе
        self.ang = 1  # параметрб отвечающий за привлекательность для юнитов, атакующих тебя
        Unit_list.add(self)
        Map[self.x][self.y].unit = self
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y].code = self.code

    def pl(self, coords=(0, 0)):
        return (self.x + coords[0]) * TILE_SIZE, (self.y + coords[1]) * TILE_SIZE  # место в пикселях

    def anim(self):
        # TODO: стоит на месте (анимация)
        pass


Map = [[Tile(0, None) for i in range(Map_size_y)] for j in range(Map_size_x)]


class Unfriendly(Unit):
    def __init__(self):
        self.__init__()
        self.targ = None
        self.ang = 0

    def movement(self):
        # TODO: алгоритм перемещения
        pass

    def findtarg(self):
        # поиск цели для перемещения
        self.targ = min(Unit_list,
                        key=lambda other: max(abs(other.x - self.x), abs(other.y - self.y)) * other.ang
                        if other.foe < other.max_foe
                        else 0)
        self.targ.foe += 1

    def losetarg(self):
        self.targ.foe -= 1
        self.targ = None
