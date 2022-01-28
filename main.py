import pygame
import os
import sys

fps = 60
pygame.init()
size = width, height = 807, 807
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
tile_width = tile_height = 70


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Star Warrior",
                  "A game for two players",
                  "solve puzzles and complete levels",
                  "Good luck!"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('castellar', 30)
    for line in intro_text:
        y = 770
        while y > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN and 664 <= event.pos[0] <= 760 and \
                        134 <= event.pos[1] <= 180:
                    return
            pygame.draw.rect(screen, pygame.Color(80, 80, 80), (664, 134, 96, 46),
                             border_radius=3)
            pygame.draw.rect(screen, pygame.Color(133, 133, 133), (670, 140, 90, 40),
                             border_radius=3)
            screen.blit(font.render('Play', True, pygame.Color('white')), (675, 142))
            y -= 2
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect(center=(width / 2, y))
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()
            clock.tick(fps)
            screen.blit(fon, (0, 0))


def select_a_level():
    x = 200
    y = 200
    levels = ["1", "2", "3", "4", '5']
    levels_coords = {'1': (0, 0),
                     '2': (0, 0),
                     '3': (0, 0),
                     '4': (0, 0),
                     '5': (0, 0)}
    fon = pygame.transform.scale(load_image('levels_fon.jpg'), (select_width, select_height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('castellar', 30)
    for level in levels:
        string_rendered = font.render(level, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = y
        intro_rect.x = x
        levels_coords[level] = (x - 30, x + intro_rect.width + 34)
        x += intro_rect.width
        pygame.draw.rect(screen, pygame.Color(80, 80, 80), (x - 34, y - 4, intro_rect.width + 34, 44), border_radius=3)
        pygame.draw.rect(screen, pygame.Color(133, 133, 133), (x - 30, y, intro_rect.width + 30, 40), border_radius=3)
        screen.blit(string_rendered, intro_rect)
        x += 100

    while True:
        global level_num
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if levels_coords['1'][0] <= event.pos[0] <= levels_coords['1'][1] and 200 <= event.pos[1] <= 244:
                    level_num = '1'
                    return level_num
                elif levels_coords['2'][0] <= event.pos[0] <= levels_coords['2'][1] and 200 <= event.pos[1] <= 244:
                    level_num = '2'
                    return level_num
                elif levels_coords['3'][0] <= event.pos[0] <= levels_coords['3'][1] and 200 <= event.pos[1] <= 244:
                    level_num = '3'
                    return level_num
                elif levels_coords['4'][0] <= event.pos[0] <= levels_coords['4'][1] and 200 <= event.pos[1] <= 244:
                    level_num = '4'
                    return level_num
                elif levels_coords['5'][0] <= event.pos[0] <= levels_coords['5'][1] and 200 <= event.pos[1] <= 244:
                    level_num = '5'
                    return level_num
        pygame.display.flip()
        clock.tick(fps)


def load_level(filename):
    filename = "data/map" + str(filename) + '.txt'
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class Skywalker(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player1_group)
        self.image = skywalker_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class DarthVader(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player2_group)
        self.image = darth_vader_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class SkywalkerDoor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, special_group)
        self.image = skywalker_door_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class DarthVaderDoor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, special_group)
        self.image = darth_vader_door_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'button':
            params = buttons_group, all_sprites, rigid_group
        elif tile_type == 'box':
            params = rigid_group, tiles_group
        elif tile_type == 'vertical':
            params = vertical_group, all_sprites, rigid_group
        elif tile_type != 'empty':
            params = tiles_group, all_sprites, rigid_group
        else:
            params = empty_tiles_group
        super().__init__(*params)
        self.type = tile_type
        if self.type != 'empty':
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            self.mask = pygame.mask.from_surface(self.image)
        if self.type == 'horizontal' or self.type == 'vertical':
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y - 10)
        if self.type == 'button':
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y + 45)
        if self.type == 'box':
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y + 15)


def generate_level(level):
    skywalker = None
    darth_vader = None
    s_door = None
    d_door = None
    box_1, box_2 = None, None
    vertical, button_1, button_2 = None, None, None
    box_c = 0
    button_c = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == 'h':
                Tile('horizontal', x, y)
            elif level[y][x] == 's':
                skywalker = Skywalker(x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 'd':
                darth_vader = DarthVader(x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 'b' and box_c == 0:
                box_1 = Tile('box', x, y)
                Tile('horizontal', x, y)
                box_c += 1
            elif level[y][x] == 'b' and box_c > 0:
                box_2 = Tile('box', x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 'u' and button_c == 0:
                button_1 = Tile('button', x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 'u' and button_c > 0:
                button_2 = Tile('button', x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 't':
                vertical = Tile('vertical', x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 'w':
                s_door = SkywalkerDoor(x, y)
                Tile('horizontal', x, y)
            elif level[y][x] == 'v':
                d_door = DarthVaderDoor(x, y)
                Tile('horizontal', x, y)
    return skywalker, darth_vader, s_door, d_door, box_1, box_2, vertical, button_1, button_2


def motion_handler_s(motion):
    global motion_s, ctr_s, lc_s, rc_s, stop_s, skywalker_win, sv_c, b1_c, b2_c
    if door1.rect.x <= player1.rect.x <= door1.rect.x + 10 and \
            door1.rect.y <= player1.rect.y <= door1.rect.y + 30:
        skywalker_win = True
    if motion_s == motion and stop_s != motion:
        ctr_s = (ctr_s + 1) % speed
        if ctr_s == 0:
            if motion == 'left':
                player1.image = pygame.transform.scale(lf_images_s[lc_s], (35, 53))
                lc_s = (lc_s + 1) % len(lf_images_s)
            elif motion == 'right':
                player1.image = pygame.transform.scale(rg_images_s[rc_s], (35, 53))
                rc_s = (rc_s + 1) % len(rg_images_s)
        if not any(pygame.sprite.collide_mask(player1, spr) for spr in rigid_group.sprites()):
            prev_x, prev_y = player1.rect.x, player1.rect.y
            if not any(pygame.sprite.collide_mask(box1, spr) for spr in all_sprites.sprites()):
                while not any(pygame.sprite.collide_mask(box1, spr) for spr in all_sprites.sprites()):
                    box1.rect.y += 1
            if not any(pygame.sprite.collide_mask(box2, spr) for spr in all_sprites.sprites()):
                while not any(pygame.sprite.collide_mask(box2, spr) for spr in all_sprites.sprites()):
                    box2.rect.y += 1
            if motion == 'left':
                if 0 <= player1.rect.x - step:
                    player1.rect.x -= step
            if motion == 'right':
                if player1.rect.x + step <= 987:
                    player1.rect.x += step
            if motion == 'down':
                if player1.rect.y + step <= 497:
                    player1.rect.y += step
            if motion == 'up':
                if 0 <= player1.rect.y - step:
                    player1.rect.y -= step
            if pygame.sprite.collide_mask(player1, box1) and \
                    not any(pygame.sprite.collide_mask(box1, spr) for spr in vertical_group.sprites()):
                if motion_s == 'left' and motion_s != 'up' and motion_s != 'down':
                    box1.rect.x -= step
                    player1.rect.x -= step
                else:
                    box1.rect.x += step
                    player1.rect.x += step
            if pygame.sprite.collide_mask(player1, box2) and \
                    not any(pygame.sprite.collide_mask(box2, spr) for spr in vertical_group.sprites()):
                if motion_s == 'left' and motion_s != 'up' and motion_s != 'down':
                    box2.rect.x -= step
                    player1.rect.x -= step
                else:
                    box2.rect.x += step
                    player1.rect.x += step
            if any(pygame.sprite.collide_mask(player1, spr) for spr in buttons_group.sprites()) and \
                    sv_c == 0:
                vertical1.rect.y += 77
                sv_c += 1
            elif not any(pygame.sprite.collide_mask(player1, spr) for spr in buttons_group.sprites()) \
                    and sv_c != 0:
                vertical1.rect.y -= 77
                sv_c -= 1
            if any(pygame.sprite.collide_mask(box1, spr) for spr in buttons_group.sprites()) and \
                    b1_c == 0:
                vertical1.rect.y += 77
                b1_c += 1
            elif not any(pygame.sprite.collide_mask(box1, spr) for spr in buttons_group.sprites()) \
                    and b1_c != 0:
                vertical1.rect.y -= 77
                b1_c -= 1
            if any(pygame.sprite.collide_mask(box2, spr) for spr in buttons_group.sprites()) and \
                    b2_c == 0:
                vertical1.rect.y += 77
                b2_c += 1
            elif not any(pygame.sprite.collide_mask(box2, spr) for spr in buttons_group.sprites()) \
                    and b2_c != 0:
                vertical1.rect.y -= 77
                b2_c -= 1
            if any(pygame.sprite.collide_mask(player1, spr) for spr in rigid_group.sprites()):
                player1.rect.x, player1.rect.y = prev_x, prev_y
        else:
            motion_s = 'stop'


def change_s_position(events):
    global motion_s, stop_s
    for event in events:
        if not skywalker_win:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    motion_s = 'left'
                    if stop_s == motion_s:
                        stop_s = 'disable'
                if event.key == pygame.K_d:
                    motion_s = 'right'
                    if stop_s == motion_s:
                        stop_s = 'disable'
                if event.key == pygame.K_w:
                    motion_s = 'up'
                    if stop_s == motion_s:
                        stop_s = 'disable'
                if event.key == pygame.K_s:
                    motion_s = 'down'
                    if stop_s == motion_s:
                        stop_s = 'disable'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    stop_s = 'left'
                if event.key == pygame.K_d:
                    stop_s = 'right'
                if event.key == pygame.K_w:
                    stop_s = 'up'
                if event.key == pygame.K_s:
                    stop_s = 'down'
        else:
            motion_s = 'stop'
    motion_handler_s('left')
    motion_handler_s('right')
    motion_handler_s('up')
    motion_handler_s('down')


def motion_handler_dv(motion):
    global motion_dv, ctr_dv, lc_dv, rc_dv, stop_dv, darth_vader_win, dv_c, up_c_dv, b1_c, b2_c
    if door2.rect.x <= player2.rect.x <= door2.rect.x + 10 and \
            door2.rect.y <= player2.rect.y <= door2.rect.y + 30:
        darth_vader_win = True
    if motion_dv == motion and stop_dv != motion:
        ctr_dv = (ctr_dv + 1) % speed
        if ctr_dv == 0:
            if motion == 'left':
                player2.image = pygame.transform.scale(lf_images_dv[lc_dv], (35, 53))
                lc_dv = (lc_dv + 1) % len(lf_images_dv)
            elif motion == 'right':
                player2.image = pygame.transform.scale(rg_images_dv[rc_dv], (35, 53))
                rc_dv = (rc_dv + 1) % len(rg_images_dv)
        if not any(pygame.sprite.collide_mask(player2, spr) for spr in rigid_group.sprites()):
            prev_x, prev_y = player2.rect.x, player2.rect.y
            if not any(pygame.sprite.collide_mask(box1, spr) for spr in all_sprites.sprites()):
                while not any(pygame.sprite.collide_mask(box1, spr) for spr in all_sprites.sprites()):
                    box1.rect.y += 1
            if not any(pygame.sprite.collide_mask(box2, spr) for spr in all_sprites.sprites()):
                while not any(pygame.sprite.collide_mask(box2, spr) for spr in all_sprites.sprites()):
                    box2.rect.y += 1
            if motion == 'left':
                if 0 <= player2.rect.x - step:
                    player2.rect.x -= step
            if motion == 'right':
                if player2.rect.x + step <= 987:
                    player2.rect.x += step
            if motion == 'down':
                if player2.rect.y + step <= 497:
                    player2.rect.y += step
            if motion == 'up':
                if 0 <= player2.rect.y - step:
                    player2.rect.y -= step
            if pygame.sprite.collide_mask(player2, box1) and \
                    not any(pygame.sprite.collide_mask(box1, spr) for spr in vertical_group.sprites()):
                if motion_dv == 'left' and motion_dv != 'up' and motion_dv != 'down':
                    box1.rect.x -= step
                    player2.rect.x -= step
                else:
                    box1.rect.x += step
                    player2.rect.x += step
            if pygame.sprite.collide_mask(player2, box2) and \
                    not any(pygame.sprite.collide_mask(box2, spr) for spr in vertical_group.sprites()):
                if motion_dv == 'left' and motion_dv != 'up' and motion_dv != 'down':
                    box2.rect.x -= step
                    player2.rect.x -= step
                else:
                    box2.rect.x += step
                    player2.rect.x += step
            if any(pygame.sprite.collide_mask(player2, spr) for spr in buttons_group.sprites()) and \
                    dv_c == 0:
                vertical1.rect.y += 77
                dv_c += 1
            elif not any(pygame.sprite.collide_mask(player2, spr) for spr in buttons_group.sprites()) \
                    and dv_c != 0:
                vertical1.rect.y -= 77
                dv_c -= 1
            if any(pygame.sprite.collide_mask(box1, spr) for spr in buttons_group.sprites()) and \
                    dv_c == 0:
                vertical1.rect.y += 77
                b1_c += 1
            elif not any(pygame.sprite.collide_mask(box1, spr) for spr in buttons_group.sprites()) \
                    and b1_c != 0:
                vertical1.rect.y -= 77
                b1_c -= 1
            if any(pygame.sprite.collide_mask(box2, spr) for spr in buttons_group.sprites()) and \
                    b2_c == 0:
                vertical1.rect.y += 77
                b2_c += 1
            elif not any(pygame.sprite.collide_mask(box2, spr) for spr in buttons_group.sprites()) \
                    and b2_c != 0:
                vertical1.rect.y -= 77
                b2_c -= 1
            if any(pygame.sprite.collide_mask(player2, spr) for spr in rigid_group.sprites()):
                player2.rect.x, player2.rect.y = prev_x, prev_y
        else:
            motion_dv = 'stop'


def change_dv_position(events):
    global motion_dv, stop_dv
    for event in events:
        if not darth_vader_win:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    motion_dv = 'left'
                    if stop_dv == motion_dv:
                        stop_dv = 'disable'
                if event.key == pygame.K_RIGHT:
                    motion_dv = 'right'
                    if stop_dv == motion_dv:
                        stop_dv = 'disable'
                if event.key == pygame.K_UP:
                    motion_dv = 'up'
                    if stop_dv == motion_dv:
                        stop_dv = 'disable'
                if event.key == pygame.K_DOWN:
                    motion_dv = 'down'
                    if stop_dv == motion_dv:
                        stop_dv = 'disable'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    stop_dv = 'left'
                if event.key == pygame.K_RIGHT:
                    stop_dv = 'right'
                if event.key == pygame.K_UP:
                    stop_dv = 'up'
                if event.key == pygame.K_DOWN:
                    stop_dv = 'down'
        else:
            motion_dv = 'stop'
    motion_handler_dv('left')
    motion_handler_dv('right')
    motion_handler_dv('up')
    motion_handler_dv('down')
    change_s_position(events)


def new_game():
    pygame.display.set_mode((select_width, select_height))
    select_a_level()
    while True:
        screen.blit(play_fon, (0, 0))
        change_dv_position(pygame.event.get())
        rigid_group.draw(screen)
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        if not skywalker_win:
            player1_group.draw(screen)
        if not darth_vader_win:
            player2_group.draw(screen)
        if skywalker_win and darth_vader_win:
            exit()
        rigid_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    FPS = 60
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player1_group = pygame.sprite.Group()
    player2_group = pygame.sprite.Group()
    rigid_group = pygame.sprite.Group()
    special_group = pygame.sprite.Group()
    empty_tiles_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    vertical_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    start_screen()
    size = width, height = 1500, 800
    screen = pygame.display.set_mode(size)
    level_num = ''
    select_width, select_height = 940, 500
    pygame.display.set_mode((select_width, select_height))
    select_a_level()
    pygame.display.set_mode((1050, 560))
    skywalker_image = pygame.transform.scale(load_image('skywalker_stay(1).png'), (35, 53))
    darth_vader_image = pygame.transform.scale(load_image('darth_vader_stay.png'), (35, 53))
    darth_vader_door_image = pygame.transform.scale(load_image('darth_vader_door.png'), (63, 63))
    skywalker_door_image = pygame.transform.scale(load_image('skywalker_door.png'), (63, 63))
    play_fon = pygame.transform.scale(load_image('play_fon.jpg'), (1050, 560))
    tile_images = {
        'horizontal': pygame.transform.scale(load_image('horizontal_wall.png'), (70, 7)),
        'box': pygame.transform.scale(load_image('box.png'), (45, 45)),
        'button': pygame.transform.scale(load_image('button.png'), (40, 15)),
        'teleport': load_image('teleport.png'),
        'vertical': pygame.transform.scale(load_image('vertical_wall.png'), (7, 70))}
    lf_images_s = list(map(load_image, ['s_l1.png',
                                        's_l2.png',
                                        's_l3.png',
                                        's_l4.png']))
    rg_images_s = list(map(load_image, ['s_r1.png',
                                        's_r2.png',
                                        's_r3.png',
                                        's_r4.png']))
    lf_images_dv = list(map(load_image, ['dv_l1.png',
                                         'dv_l2.png',
                                         'dv_l3.png',
                                         'dv_l4.png']))
    rg_images_dv = list(map(load_image, ['dv_r1.png',
                                         'dv_r2.png',
                                         'dv_r3.png',
                                         'dv_r4.png']))
    player1, player2, door1, door2, box1, box2, vertical1, button1, button2 = generate_level(load_level(level_num))
    skywalker_win = False
    darth_vader_win = False
    motion_s = 'stop'
    motion_dv = 'stop'
    up_c_dv = 0
    dv_c = 0
    sv_c = 0
    b1_c = 0
    b2_c = 0
    step = 6
    ctr_s, w_ctr_s, w_dir_ctr_s = 0, 0, 0
    ctr_dv, w_ctr_dv, w_dir_ctr_dv = 0, 0, 0
    speed = 10
    stop_s = 'disable'
    stop_dv = 'disable'
    lc_s, rc_s = 0, 0
    lc_dv, rc_dv = 0, 0
    player1_prev_x, player1_prev_y = player1.rect.x, player1.rect.y
    player2_prev_x, player2_prev_y = player2.rect.x, player2.rect.y
    while True:
        play_fon = pygame.transform.scale(load_image('play_fon.jpg'), (1050, 560))
        screen.blit(play_fon, (0, 0))
        all_sprites.draw(screen)
        change_dv_position(pygame.event.get())
        if not skywalker_win:
            player1_group.draw(screen)
        if not darth_vader_win:
            player2_group.draw(screen)
        if skywalker_win and darth_vader_win:
            exit()
        rigid_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
