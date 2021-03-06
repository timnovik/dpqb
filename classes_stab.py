import pygame
pygame.init()
from functions import *
from setup import *
import random as rnd


Unit_list = []
statics_list = []


def is_free(pl, size, elem):
    # проверка на то, что во всей области нет препятствий
    res = True
    for i in range(size[0]):
        for j in range(size[1]):
            res = res and Map[pl[0] + i][pl[1] + j] in [None, elem]
    return res


class Object:
    def __init__(self, code, pl, size, anim):
        self.code = code
        self.x = pl[0]
        self.y = pl[1]
        self.size = size
        self.anim = anim
        if code < 0:
            statics_list.append(self)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y] = self

    def pix_pl(self, coords=(0, 0)):
        return (self.x + coords[0]) * TILE_SIZE, (self.y + coords[1]) * TILE_SIZE  # место в пикселях

    def pl(self, coords=(0,0)):
        return self.x + coords[0], self.y + coords[1]

    def clear(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y] = None
        del self


Map = [[None for i in range(MAP_SIZE_Y)] for j in range(MAP_SIZE_X)]


class Unit(Object):
    def __init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim):
        Object.__init__(self, code, pl, size, anim)
        Unit_list.append(self)
        self.die_img = anim['dead_right']
        self.side = True  # True, если смотрит вправо
        self.foe = []  # юниты, бегуще к тебе
        self.max_foe = 2  # максимальное количество юнитов, бегущих к тебе
        self.ang = 1  # параметр, отвечающий за привлекательность для юнитов, атакующих тебя
        self.speed = speed
        self.hp = hp
        self.damage = attack
        self.defence = defence  # defence
        self.timer = cooldown
        self.COOLDOWN = cooldown
        self.hitdist = hitdist

    def attack(self, other):
        if other is not None and other.code >= 0:
            # self атакует other, если закончилась перезарядка
            if self.timer <= 0:
                self.timer = self.COOLDOWN
                damage = self.damage * other.defence
                if damage >= other.hp:
                    other.die()
                else:
                    other.hp -= damage
                return True
        return False

    def die(self):
        # стирает все упоминания себя, создаёт на месте себя труп
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y] = None
        Unit_list.pop(Unit_list.index(self))
        for name in self.foe:
            name.targ = None
        Map[self.x][self.y] = Object(-1, self.pl(), self.size, self.die_img)

    def rebuild(self, pl):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y] = None
        self.x, self.y = pl
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                Map[self.x + x][self.y + y] = self


class Unfriendly(Unit):
    def __init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim):
        Unit.__init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim)
        global Unit_list
        Unit_list.append(self)
        self.targ = None
        self.ang = 0
        self.cnt_mov = 0

    def movement(self):
        if self.targ is not None:
            # вероятность потерять цель
            d = dist(self.pl(), self.targ.pl())
            mab = (((10 - d // 2) if d > 2 * self.hitdist else (self.hitdist - d)) ** 2 - (1 - self.cnt_mov) * 30)
            if self.cnt_mov == 0:
                mab = -1
            if rnd.randrange(100) <= mab:
                self.losetarg()
        if self.targ is not None:
            if dist(self.targ.pl(), self.pl()) <= self.hitdist:
                self.attack(self.targ)
            else:
                movements = bfs(Map, self.pl(), self.targ.pl())[:-1][:self.speed]
                # все точки, которые прошёл юнтит при перемещении
                self.rebuild(movements[-1])
            self.cnt_mov += 1
        else:
            x_m = rnd.randint(-self.speed, self.speed)
            y_m = rnd.randint(-self.speed, self.speed)
            if Map[self.x + x_m][self.y + y_m] is None:
                movements = bfs(Map, self.pl(), self.targ.pl())[:-1][:self.speed]
                # все точки, которые прошёл юнтит при перемещении
                self.rebuild(movements[-1])
                self.findtarg()
            else:
                self.findtarg()
                self.movement()

    def findtarg(self):
        # поиск цели для перемещения
        self.targ = min(Unit_list,
                        key=lambda other: max(abs(other.x - self.x), abs(other.y - self.y)) * other.ang
                        if len(other.foe) < other.max_foe
                        else 0)
        self.targ.foe.append(self)

    def losetarg(self):
        self.targ.foe.pop(self.targ.foe.find(self))
        self.targ = None
        self.cnt_mov = 0


class Hero(Unit):
    def __init__(self, hp, attack, cooldown, defence, pl, anim, size=(2, 2), code=1, speed=1, hitdist=1):
        Unit.__init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim)
        self.ang = 2

    def move(self, direction):
        if is_free(self.pl(coords=direction), self.size, self):
            self.rebuild(self.pl(coords=direction))
            return True
        return False

    def movement(self):
        return []