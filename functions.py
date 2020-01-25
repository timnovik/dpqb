from pygame import *


def divide_line(coords1, coords2, n):
    dx = coords1[0] - coords2[0]
    dy = coords1[1] - coords2[1]
    if dx % n:
        dx += n - dx % n
    if dy % n:
        dy += n - dy % n
    return [(coords1[0] + dx // n * i, coords1[1] + dy // n * i) for i in range(n + 1)]


def key_pressed(inputKey):
    keysPressed = key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False