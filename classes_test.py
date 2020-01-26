import pygame
pygame.init()
from functions_test import *
from setup_test import *
import random as rnd
from math import inf


Unit_list = []


def is_free(pl, size, elem):
    # проверка на то, что во всей области нет препятствий
    res = True
    for i in range(size[0]):
        for j in range(size[1]):
            try:
                res = res and Map[pl[0] + i][pl[1] + j] in [None, elem]
            except IndexError:
                pass
    return res


def is_hitable(st, fn):
    # может ли быть прострел для лучника
    res = True
    for x, y in arrow(st, fn):
        res = res and Map[x][y] in archer_hitval
    return res

class Object:
    def __init__(self, code, pl, size, anim):
        self.code = code
        self.x = pl[0]
        self.y = pl[1]
        self.size = size
        self.anim = anim
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
    def __init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img):
        Object.__init__(self, code, pl, size, anim)
        Unit_list.append(self)
        self.foe = []  # юниты, бегуще к тебе
        self.max_foe = 2  # максимальное количество юнитов, бегущих к тебе
        self.ang = 1  # параметр, отвечающий за привлекательность для юнитов, атакующих тебя
        self.speed = speed
        self.hp = hp
        self.damage = attack
        self.defence = defence  # defence
        self.timer = 0
        self.COOLDOWN = cooldown
        self.die_img = die_img
        self.hitdist = hitdist

    def attack(self, other):
        # self атакует other, если закончилась перезарядка
        if self.timer <= 0:
            self.timer = self.COOLDOWN
            damage = self.damage * other.defence
            if damage >= other.hp:
                other.die()
            else:
                other.hp -= damage

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
    def __init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img):
        Unit.__init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img)
        global Unit_list
        Unit_list.append(self)
        self.targ = None
        self.ang = 0
        self.cnt_mov = 0

    def movement(self):
        if self.targ is not None:
            if dist(self.targ.pl(), self.pl()) <= self.hitdist:
                self.attack(self.targ)
                prob = 10 * self.cnt_mov ** 2
            else:
                movements = bfs(Map, self.pl(), self.targ.pl())[:-1]
                # все точки, которые прошёл юнтит при перемещении
                self.rebuild(movements[self.speed - 1])
                if len(movements) > 5 * self.speed:
                    if dist(self.pl(), self.targ.pl()) > 4 * self.speed:
                        prob = 3  # если юнит далеко от цели
                    else:
                        prob = 90  # если близко, но не может дойти
                elif len(movements) > 2 * self.speed:
                    if dist(self.pl(), self.targ.pl()) < 2 * self.hitdist:
                        prob = 20
                    else:
                        prob = 80
                else:
                    prob = 99
            self.cnt_mov += 1
            if rnd.randint(1, 100) < prob:
                self.losetarg()
        else:
            x_m = rnd.randint(-self.speed * 2, self.speed * 2)
            y_m = rnd.randint(-self.speed * 2, self.speed * 2)
            if is_free(self.pl(coords=(x_m, y_m)), self.size, self):
                movements = bfs(Map, self.pl(), self.pl(coords=(x_m, y_m)))[:-1][:self.speed]
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
                        if len(other.foe) <= other.max_foe
                        else 0)
        self.targ.foe.append(self)

    def losetarg(self):
        self.targ.foe.pop(self.targ.foe.index(self))
        self.targ = None
        self.cnt_mov = 0


class Hero(Unit):
    def __init__(self, hp, attack, cooldown, defence, pl, anim, die_img, size=(2, 2), code=1, speed=1, hitdist=1):
        Unit.__init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img)
        self.ang = 2

    def movement(self, direction):
        if is_free(self.pl(coords=direction), self.size, self):
            self.rebuild(self.pl(coords=direction))

    def attack(self, other):
        def attack(self, other):
            dirr = (0, 0)
            if self.timer <= 0 and other.x - self.x >= -1 and other.y - self.y >= -1:
                self.timer = self.COOLDOWN
                damage = self.damage * other.defence
                if damage >= other.hp:
                    other.die()
                else:
                    other.hp -= damage
            if other.x - self.x == -2:
                dirr[0] -= 1
            if other.y - self.y == -2:
                dirr[1] -= 1
            self.move(dirr)

class EvilMan(Unfriendly):
    def __init__(self, hp, attack, cooldown, defence, pl, anim, die_img, speed=3, hitdist=2, size=(2, 2)):
        Unfriendly.__init__(self, 2, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img)

    def attack(self, other):
        dirr = (0, 0)
        if self.timer <= 0 and other.x - self.x >= -1 and other.y - self.y >= -1:
            self.timer = self.COOLDOWN
            damage = self.damage * other.defence
            if damage >= other.hp:
                other.die()
            else:
                other.hp -= damage
        if other.x - self.x == -2:
            dirr[0] -= 1
        if other.y - self.y == -2:
            dirr[1] -= 1
        self.move(dirr)

    def move(self, direction):
        if is_free(self.pl(coords=direction), self.size, self):
            self.rebuild(self.pl(coords=direction))

    def ultra(self):
        pass
        # TODO: ultra


class EvilArcher(Unfriendly):
    def __init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img):
        Unfriendly.__init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img)
        #TODO: paramethers Archer

    def findtarg(self):
        min_ = inf
        min_name = None
        for name in Unit_list:
            if dist(self.pl(), name.pl()) <= self.hitdist and is_hitable(self.pl,name.pl()) and len(name.foe) <= name.max_foe + 1 and name.hp < min_ and name.ang != 0:
                min_name = name
                min_ = name.hp
        self.targ = min_name
        min_name.foe.append(self)

class EvilHealer(Unfriendly):
    def __init__(self, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img, code=4):
        Unfriendly.__init__(self, code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img)
        #TODO: paramethers Healer

    def findtarg(self):
        min_ = inf
        min_name = None
        for name in Unit_list:
            if dist(self.pl(), name.pl()) <= self.hitdist and len(name.foe) <= name.max_foe + 1 and name.hp < min_ and name.ang == 0:
                min_name = name
                min_ = name.hp
        self.targ = min_name
        min_name.foe.append(self)