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


class Object:
    def __init__(self, pl, size, **anim):
        self.x = pl[0]
        self.y = pl[1]
        self.animations = anim
        self.size = size
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y].unit = self

    def pl(self, coords=(0, 0)):
        return (self.x + coords[0]) * TILE_SIZE, (self.y + coords[1]) * TILE_SIZE  # место в пикселях

    def animation(self):
        # TODO: стоит на месте (анимация)
        pass


Map = [[None for i in range(Map_size_y)] for j in range(Map_size_x)]


class Unit(Object):
    def __init__(self, pl, size, **anim):
        Object.__init__(self, pl, size, **anim)
        self.foe = 0  # количество юнитов, бегущих к тебе
        self.max_foe = 2  # максимальное количество юнитов, бегущих к тебе
        self.ang = 0  # параметр, отвечающий за привлекательность для юнитов, атакующих тебя

    def rebuild(self, pl):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y].unit = None
        self.x, self.y = pl
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y].unit = self



class Unfriendly(Unit):
    def __init__(self, code, anim, pl, size):
        self.__init__(code, anim, pl, size)
        global Unit_list
        Unit_list.append(self)
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


class Hero(Unit):
    def __init__(self, pl, size=(2, 2), **anim):
        Unit.__init__(self, pl, size, **anim)

    def move(self, direction, Drawer):
        self.rebuild((self.x + direction[0], self.y + direction[1]))
        if direction[0] >= 0:
            Drawer.add(self.animations['run_right'], divide_line(self.pl(), self.pl(direction), len(self.animations['run_right'])))
        else:
            Drawer.add(self.animations['run_left'], divide_line(self.pl(), self.pl(direction), len(self.animations['run_left'])))

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