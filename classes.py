from pygame import *


class Tile:
    def __init__(self, code, elem):
        self.obj = code
        self.unit = elem


class Unit:
    def __init__(self, code, anim, pl):
        self.x = pl[0]
        self.y = pl[1]
        self.img = anim
        self.code = code

    def pl(self):
        return self.x, self.y

    def anim(self):
        # TODO:стоит на месте
        pass

class Static(Unit):
    def 