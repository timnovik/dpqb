from pygame import *


def dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def divide_line(coords1, coords2, n):
    dx = coords1[0] - coords2[0]
    dy = coords1[1] - coords2[1]
    if dx % n:
        dx += n - dx % n
    if dy % n:
        dy += n - dy % n
    return [(coords1[0] + dx // n * i, coords1[1] + dy // n * i) for i in range(n + 1)]


def lin2(x, d1, d2):
    # прямая, проходящая через 2 заданные точки
    x1, y1 = d1
    x2, y2 = d2
    return ((y1 - y2) * x + x1 * y2 - x2 * y1) / (x1 - x2)


def arrow(st, fn):
    # переделывает прямую в "змейку" от st до fn
    x, y = st
    if x == fn[0]:
        res = []
        for i in range(min(y, fn[1]), max(y, fn[1])):
            res += [(x, i)]
        return res + [fn]
    elif y == fn[1]:
        res = []
        for i in range(min(x, fn[0]), max(x, fn[0])):
            res += [(i, y)]
        return res + [fn]
    else:
        x = st[0]
        y = st[1]
        res = []
        x_w = -1 if fn[0] - x < 0 else 1  # полуплоскость по x
        y_w = -1 if fn[1] - y < 0 else 1  # по y
        while (x, y) != fn:
            # двигаемся от % к @
            print(x, y)
            dirr = [0, 0]
            """
            ###
            @%@
            ###
            """
            if y - 0.5 <= lin2(x + 0.5, fn, st) <= y + 0.5:
                dirr[0] += 1

            """
            #@#
            #%#
            #@#
            """
            if x - 0.5 <= lin2(y + 0.5, fn[::-1], st[::-1]) <= x + 0.5:
                dirr[1] += 1

            res += [(x, y)]
            x += dirr[0] * x_w
            y += dirr[1] * y_w
        return res + [(x, y)]


def bfs(map, coords1, coords2):
    m = len(map)
    n = len(map[0])
    s = {i: [] for i in range(m * n)}
    used = [0] * n * m
    sum_used = 0
    for i in range(1, m):
        for j in range(1, n):
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if map[i][j] == map[i + di][j + dj] is None:
                        s[j + (i - 1) * n - 1].append(j + dj - 1 + (i + di - 1) * n)
                    if map[i][j] is None and not used[j + (i - 1) * n - 1]:
                        used[j + (i - 1) * n - 1] = 1
                        sum_used += 1
    cur = [[coords1]]
    while cur:
        new = []
        for way in cur:
            for node in s[way[-1]]:
                if not used[node]:
                    new.append(way + [node])
                    used[node] = 1
                    if node == coords2[0] + coords2[1] * n:
                        return new[-1]
        cur = new