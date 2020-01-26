from classes_stab import *
from setup import *
from functions import *
from pygame import *


def spawn_enemies(Map, start, n):
    i = 0
    while i < n:
        x, y = randint(start, MAP_SIZE_X), randint(0, MAP_SIZE_Y)
        if Map[x][y] is None:
            # code, speed, hp, attack, cooldown, defence, pl, hitdist, size, anim, die_img
            enemy = Unfriendly(1, 2, 1, 1, 1, 1, (x, y), 1, (1, 1), load_images('Nps/bad_knight'))
            i += 1


def generate_landscape(bg_path, n):
    sizes = [(4, 4), (4, 2), (2, 2), (2, 3), (1, 2)]
    paths = ['images/landscape/house.png',
              'images/landscape/Rock_Big.png',
              'images/landscape/Rock_small.png',
              'images/landscape/tree_big.png',
              'images/landscape/tree_small.png']
    images = [Image.open(path) for path in paths]
    pygame_images = [image.load(path) for path in paths]
    map = Image.open(bg_path)
    bg = map.load()
    i = 0
    while i < n:
        s = randint(0, len(sizes) - 1)
        x, y = randint(TILE_SIZE, map.size[0] - sizes[s][0] * TILE_SIZE - TILE_SIZE) // TILE_SIZE, randint(TILE_SIZE, map.size[1] - sizes[s][1] * TILE_SIZE - TILE_SIZE) // TILE_SIZE
        if are_all_green((x - 1) * TILE_SIZE, (y - 1) * TILE_SIZE, (x + sizes[s][0] + 1) * TILE_SIZE, (y + sizes[s][1] + 1) * TILE_SIZE, bg):
            map.paste(images[s], (x * TILE_SIZE, y * TILE_SIZE))
            i += 1
            if s == 0:
                code = -4
            elif s == 1 or s == 2:
                code = -2
            else:
                code = -3
            obj = Object(code, (x, y), sizes[s], {'stand': [pygame_images[s]] * 5})
    # map.save('test.png')


def calc(hero, dir):
    animations = []
    direction = dir.copy()
    for i in event.get():
        if i.type == QUIT:
            quit()
        if i.type == KEYDOWN:
            # обработка всех кнопок, которые нажаты (пока только движение)
            if i.key == MOVE_UP:
                direction[1] = -1
            if i.key == MOVE_DOWN:
                direction[1] = 1
            if i.key == MOVE_RIGHT:
                direction[0] = 1
            if i.key == MOVE_LEFT:
                direction[0] = -1
            if i.key == ATTACK:
                if direction == [0, 0]:
                    if hero.side:
                        if hero.attack(Map[hero.x + 2][hero.y]) or hero.attack(Map[hero.x + 2][hero.y - 1]):
                            action = 'attack'
                        else:
                            action = 'stand'
                    else:
                        if hero.attack(Map[hero.x - 1][hero.y]) or hero.attack(Map[hero.x - 1][hero.y - 1]):
                            action = 'attack_left'
                        else:
                            action = 'stand'
                    animations.append((hero.anim[action], [hero.pl()] * len(hero.anim[action])))
        if i.type == KEYUP:
            if i.key == MOVE_UP:
                direction[1] = max(direction[1], 0)
            if i.key == MOVE_DOWN:
                direction[1] = min(direction[1], 0)
            if i.key == MOVE_RIGHT:
                direction[0] = min(direction[0], 0)
            if i.key == MOVE_LEFT:
                direction[0] = max(direction[0], 0)
    is_moved = hero.move(direction)
    if is_moved:
        if direction == [0, 0]:
            action = 'stand' if hero.side else 'stand_left'
        elif direction[0] >= 0:
            action = 'move_right'
            hero.side = True
        else:
            action = 'move_left'
            hero.side = False
    else:
        direction = [0, 0]
        action = 'stand' if hero.side else 'stand_left'
    coords = divide_line(hero.pix_pl(), hero.pix_pl(direction), len(hero.anim[action]))
    animations.append((hero.anim[action], coords))

    for unit in Unit_list:
        pass
    for unit in Unit_list:
        way = unit.movement()
        for i in range(1, len(way)):
            if way[i - 1][0] >= way[i][0]:
                action = 'run_left'
            else:
                action = 'run_right'
            start = (way[i - 1][0] * TILE_SIZE, way[i - 1][1] * TILE_SIZE)
            end = (way[i][0] * TILE_SIZE, way[i][1] * TILE_SIZE)
            coords = divide_line(start, end, len(unit.anim[action]))
            animations.append((unit.anim[action], coords))

    for static in statics_list:
        animations.append((static.anim['stand'], [static.pix_pl()] * len(static.anim['stand'])))

    return animations, direction


def single_player():
    generate_landscape('images/map.png', 25)
    direction = [0, 0]
    init()
    FPS = 30
    clock = time.Clock()
    window = display.set_mode((1280, 768))
    hero = Hero(10, 1, 1, 1, (10, 10), load_images('knight'))
    # hp, attack, cooldown, defence, pl, anim, die_img, size=(2, 2), code=1, speed=1, hitdist=1
    bg = image.load('images/map.png')
    while 1:
        animations, direction = calc(hero, direction)
        if animations:
            for frame in range(5):
                window.blit(bg, (0, 0))
                for i in range(len(animations)):
                    try:
                        window.blit(animations[i][0][frame], animations[i][1][frame])
                    except:
                        pass
                display.update()
                clock.tick(FPS)


single_player()