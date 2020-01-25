from classes import *
from setup import *
from functions import *
from pygame import *


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
    map.save('test.png')


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
            action = 'stand'
        elif direction[0] >= 0:
            action = 'move_right'
        else:
            action = 'move_left'
    else:
        direction = [0, 0]
        action = 'stand'
    coords = divide_line(hero.pix_pl(), hero.pix_pl(direction), len(hero.anim[action]))
    animations.append((hero.anim[action], coords))

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
    hero = Hero(10, 1, 1, 1, (10, 10), load_images('knight'), image.load('images/map.png'))
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
